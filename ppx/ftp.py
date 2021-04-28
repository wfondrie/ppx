"""General utilities for working with the repository FTP sites."""
import re
import logging
from ftplib import FTP

LOGGER = logging.getLogger(__name__)

# Constants -------------------------------------------------------------------
# UNIX FTP server regex from:
# https://github.com/stevemayne/pyftpparser/blob/master/ftpparser/parse.py
UNIX = re.compile(
    "^([-bcdlps])" # type
    "([-rwxXsStT]{1,9})" # permissions
    "\\s+(\\d+)" # hard link count
    "\\s+(\\w+)" # owner
    "\\s+(\\w+)" # group
    "\\s+(\\d+)" # size
    "\\s+([A-Za-z]{3}\\s+\\d{1,2}\\s+[:\\d]{4,5})" # modification date
    "\\s(.+)$" # name
)

UNIX_TIME = re.compile(
    "^([A-Za-z]{3})" # month
    "\\s+(\\d{1,2})" # day of month
    "\\s+([:\\d]{4,5})$" # time of day or year
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
    def __init__(self, url, max_depth=3):
        """Initialize an FTPParser"""
        if not url.startswith("ftp://"):
            raise ValueError("The URL does not appear to be an FTP server")

        self.server, self.path = url.replace("ftp://", "").split("/", 1)
        self.max_depth = max_depth
        self._files = None
        self._dates = None
        self._depth = 1

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
            self._files, self._dates = self._parse_files(repo)
            self._depth = 0

    def _parse_files(self, conn):
        """A recursive function to parse the files

        Parameters
        ----------
        conn : FTP object
            The FTP connection.
        """
        files, dirs = parse_response(conn)
        for rpath in dirs:
            self._depth += 1
            if self._depth <= self.max_depth:
                conn.cwd(rpath)
                new_res = []
                for res in zip(*self._parse_files(conn)):
                    new_res.append("/".join([rpath, f] for f in res))

                conn.cwd("..")
            else:
                new_res = [[], []]

            self._depth -= 1

        return files + new_res[0], dirs + new_res[1]


    @property
    def files(self):
        """List the files form the FTP connection"""
        if self._files is None:
            self._get_files()


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
        line = line.split(maxsplit=8)
        if line[0].startswith("d"):
            dirs.append(line[-1])
        else:
            files.append(line[-1])

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
    match = UNIX.full_match(line)
    is_dir = match[1] == "d" or match[1] == "l"
    name = match[8]
    date = match[7]


def parse_time(time):
    """Parse the FTP modification time.

    Parameters
    """
    pass
