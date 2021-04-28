"""General utilities for working with the repository FTP sites."""
import re
from ftplib import FTP


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


def list_files(url):
    """Recursively list files on the FTP server.

    Parameters
    ----------
    url : str
        The url of the FTP server

    Returns
    -------
    list of str
        A list of files on the FTP server, including paths.
    """
    server, path = parse_ftp_url(url)
    with FTP(server) as repo:
        repo.login()
        repo.cwd(path)
        files = parse_files(repo)

    return files


def parse_files(conn):
    """Recursive function to parse the files

    Parameter
    ---------
    conn : ftplib.FTP connection
        The connection to the FTP server.

    Returns
    -------
    list of tuples
        Each tuple contains the file name with path, and the time when it was
        last modified on the FTP server
    """
    files, dirs = parse_response(conn)
    new_files = []
    for path in dirs:
        conn.cwd(path)
        new_files += ["/".join([path, f]) for f in parse_files(conn)]
        conn.cwd("..")

    return files + new_files


def parse_ftp_url(url):
    """Parse an FTP URL

    Parameters
    ----------
    url : str
        A URL for an FTP server. Must start with 'ftp://'.

    Returns
    -------
    server : str
        The FTP server address.
    path : str
        The requested path on the server.
    """
    if not url.startswith("ftp://"):
        raise ValueError("The URL does not appear to be an FTP server")

    url = url.replace("ftp://", "").split("/", 1)
    return url


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
            print(line)
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
