"""General utilities for working with the repository FTP sites."""
import re
import logging
from ftplib import FTP
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
    """Handle FTP connections

    Parameters
    ----------
    url : str
        The url for the FTP connection.
    max_depth : int, optional
        The maximum resursion depth when looking for files.
    """

    def __init__(self, url, max_depth=4):
        """Initialize an FTPParser"""
        if not url.startswith("ftp://"):
            raise ValueError("The URL does not appear to be an FTP server")

        self.server, self.path = url.replace("ftp://", "").split("/", 1)
        self.max_depth = max_depth
        self._files = None
        self._dirs = None
        self._depth = 0

    def _get_files(self):
        """Recursively list files from the FTP connection.

        Parameters
        ----------
        max_depth : int
            The maximum recursion depth.
        """
        with FTP(self.server) as repo:
            repo.login()
            repo.cwd(self.path)
            self._files, self._dirs = self._parse_files(repo)
            self._depth = 0

    def _parse_files(self, conn):
        """A recursive function to parse the files

        Parameters
        ----------
        conn : FTP object
            The FTP connection.
        """
        files, dirs = parse_response(conn)
        new_files = []
        new_dirs = []
        for rpath in dirs:
            self._depth += 1
            if self._depth <= self.max_depth:
                conn.cwd(rpath)
                curr_files, curr_dirs = self._parse_files(conn)
                new_files += ["/".join([rpath, f]) for f in curr_files]
                new_dirs += ["/".join([rpath, d]) for d in curr_dirs]
                conn.cwd("..")

            self._depth -= 1

        return files + new_files, dirs + new_dirs

    def download(self, files, dest_dir, force_=False, silent=False):
        """Download the files"""
        files = listify(files)
        with FTP(self.server, timeout=1000) as repo:
            repo.login()
            repo.cwd(self.path)

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
                if not force_ and out_file.exists():
                    continue

                out_file.parent.mkdir(parents=True, exist_ok=True)
                size = repo.size(fname)
                desc = f"{fname} ["
                pbar = tqdm(
                    desc=str(fname),
                    total=size,
                    position=1,
                    unit="b",
                    unit_divisor=1024,
                    unit_scale=True,
                    leave=False,
                    disable=silent,
                )
                with out_file.open("wb+") as out:
                    write = partial(write_file, fhandle=out, pbar=pbar)
                    repo.retrbinary(f"RETR {fname}", write)
                    pbar.close()

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
