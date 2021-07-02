"""General utilities for working with the repository FTP sites."""
import re
import logging
import socket
from ftplib import FTP, error_temp
from pathlib import Path
from functools import partial

from tqdm import tqdm

from .utils import listify

LOGGER = logging.getLogger(__name__)

# Constants -------------------------------------------------------------------
# UNIX FTP server regex from:
# https://github.com/stevemayne/pyftpparser/blob/master/ftpparser/parse.py
UNIX = re.compile(
    "^([-bcdlps])"  # type
    "([-rwxXsStT]{1,9})"  # permissions
    "\\s+(\\d+)"  # hard link count
    "\\s+(\\w+)"  # owner
    "\\s+(\\w+)"  # group
    "\\s+(\\d+)"  # size
    "\\s+([A-Za-z]{3}\\s+\\d{1,2}\\s+[:\\d]{4,5})"  # modification date
    "\\s(.+)$"  # name
)

UNIX_TIME = re.compile(
    "^([A-Za-z]{3})"  # month
    "\\s+(\\d{1,2})"  # day of month
    "\\s+([:\\d]{4,5})$"  # time of day or year
)


# Classes ---------------------------------------------------------------------
class FTPParser:
    """Download files from the FTP server.

    The parts for reconnection were adapted from:
    https://github.com/Parquery/reconnecting-ftp

    Parameters
    ----------
    url : str
        The url for the FTP connection.
    max_depth : int, optional
        The maximum resursion depth when looking for files.
    """

    def __init__(self, url, max_depth=4, max_reconnects=10):
        """Initialize an FTPParser"""
        if not url.startswith("ftp://"):
            raise ValueError("The URL does not appear to be an FTP server")

        self.server, self.path = url.replace("ftp://", "").split("/", 1)
        self.connection = None
        self.max_depth = max_depth
        self.max_reconnects = max_reconnects
        self._files = None
        self._dirs = None
        self._depth = 0

        # The directory at the time of disconnect:
        self.last_pwd = None

    def connect(self):
        """Connect to the FTP server"""
        if self.connection is not None and self.connection.file is None:
            self.connection.close()
            self.connection = None

        if self.connection is None:
            self.connection = FTP()
            self.connection.connect(self.server)
            self.connection.login()
            self.connection.cwd(self.path)

    def quit(self):
        """Close the connection."""
        if self.connection is not None:
            self.connection.quit()
            self.connection = None

    def _download_file(self, remote_file, out_file, force_, silent):
        """Download a single file.

        This wraps the ftplib.FTP.retrbinary to enable reconnects. It also
        adds a progress bar.

        Parameters
        ----------
        remote_file : str
            The file to download.
        out_file : pathlib.Path object
            The local file.
        silent : bool
            Disable the progress bar?
        force_ : bool
            Force the file to be redownloaded, even if it exists.
        """
        if self.connection is None:
            self.connect()

        size = self.connection.size(remote_file)
        pbar = tqdm(
            desc=str(remote_file),
            total=size,
            position=1,
            unit="b",
            unit_divisor=1024,
            unit_scale=True,
            leave=False,
            disable=silent,
        )
        last_err = None
        mode = "wb+" if force_ else "ab+"
        with out_file.open(mode) as out:
            start_pos = out.tell()
            pbar.update(start_pos)

            # Exit if all bytes are present:
            if start_pos == size:
                pbar.close()
                return

            # Download file if not:
            write = partial(write_file, fhandle=out, pbar=pbar)
            for _ in range(0, self.max_reconnects):
                try:
                    if self.connection is None:
                        self.connect()

                    self.connection.retrbinary(
                        f"RETR {remote_file}",
                        write,
                        rest=out.tell(),
                    )
                    pbar.close()
                    return

                except (
                    ConnectionRefusedError,
                    socket.timeout,
                    socket.gaierror,
                    socket.herror,
                    error_temp,
                    EOFError,
                    OSError,
                ) as err:
                    self.connection.close()
                    self.connection = None
                    last_err = err

        raise error_temp(
            f"Failed after {self.max_reconnects} reconnect(s), "
            f"the last error was: {last_err}"
        )

    def _get_files(self):
        """Recursively list files from the FTP connection."""
        self.connect()
        self._files, self._dirs = self._parse_files()
        self._depth = 0
        self.quit()

    def _parse_files(self):
        """A recursive function to parse the files."""
        files, dirs = parse_response(self.connection)
        new_files = []
        new_dirs = []
        for rpath in dirs:
            self._depth += 1
            if self._depth <= self.max_depth:
                self.connection.cwd(rpath)
                curr_files, curr_dirs = self._parse_files()
                new_files += ["/".join([rpath, f]) for f in curr_files]
                new_dirs += ["/".join([rpath, d]) for d in curr_dirs]
                self.connection.cwd("..")

            self._depth -= 1

        return files + new_files, dirs + new_dirs

    def download(self, files, dest_dir, force_=False, silent=False):
        """Download the files

        Parameters
        ----------
        remote_file : str
            The file to download.
        out_file : pathlib.Path object
            The local file.
        force_ : bool
            Force the files to be redownloaded, even they already exist.
        silent : bool
            Disable the progress bar?
        """
        files = listify(files)
        out_files = []
        overall_pbar = partial(
            tqdm,
            desc="TOTAL",
            position=0,
            unit="files",
            disable=silent,
        )

        for fname in overall_pbar(files):
            out_file = Path(dest_dir, fname)
            out_files.append(out_file)
            out_file.parent.mkdir(parents=True, exist_ok=True)
            self._download_file(fname, out_file, silent=silent, force_=force_)

        return out_files

    @property
    def files(self):
        """List the files form the FTP connection"""
        if self._files is None:
            self._get_files()

        return self._files

    @property
    def dirs(self):
        """List the directories form the FTP connection"""
        if self._dirs is None:
            self._get_files()

        return self._dirs


# Functions -------------------------------------------------------------------
def write_file(data, fhandle, pbar):
    """Write a file with progress."""
    fhandle.write(data)
    pbar.update(len(data))


def parse_response(conn):
    """Parse the FTP server response.

    Parameters
    ----------
    url : str
        The url of the FTP server.

    Returns
    -------
    files : list of str
    directories : list of str
    """
    lines = []
    conn.dir(lines.append)

    files = []
    dirs = []
    for line in lines:
        parsed, is_dir = parse_line(line)
        if is_dir:
            dirs.append(parsed)
        else:
            files.append(parsed)

    return files, dirs


def parse_line(line):
    """Parse one line of the FTP response

    Parameters
    ----------
    line : str
        One line from the FTP response

    Returns
    -------
    is_dir : bool
        Whether or not the line is a directory.
    name : str
        The file or directory name.
    date : date
        The modification date.
    """
    match = UNIX.fullmatch(line)
    is_dir = match[1] == "d" or match[1] == "l"
    name = match[8]
    return name, is_dir
