"""MassIVE datasets."""
import re
from pathlib import Path

from .ftp import FTPParser
from .project import BaseProject


class MassiveProject(BaseProject):
    """Retrieve information about a MassIVE project.

    Parameters
    ----------
    msv_id : str
        The MassIVE identifier.
    local : str or path object, optional
        The local directory where data for this project will be downloaded.

    Attributes
    ----------
    id : str
    local : pathlib.Path object
    url : str


    """
    def __init__(self, msv_id, local=None):
        """Instantiate a MSVDataset object"""
        super().__init__(msv_id, local)
        self._url = f"ftp://massive.ucsd.edu/{self.id}"
        self._parser = FTPParser(self._url)

    def _validate_id(self, identifier):
        """Validate a MassIVE identifier"""
        identifier = str(identifier).upper()
        if not re.match("MSV[0-9]{9}", identifier):
            raise ValueError("Malformed MassIVE identifier.")

        return identifier

    def remote_dirs(self, glob=None):
        """List the project directories.

        Parameters
        ----------
        path : str or list of str, optional
            The subdirectory on the FTP server to look in. A list
            will be concatenated into a single URL.

        Returns
        -------
        list of str
             The directories available on the FTP server.
        """
        dirs = self._parser.dirs
        if glob is not None:
            dirs = [d for d in dirs if Path(d).match(glob)]

        return dirs

    def remote_files(self, glob=None):
        """
        List available files on the FTP server.

        Parameters
        ----------
        path : str or list of str, optional
            The subdirectory on the FTP server to look in. A list
            will be concatenated into a single URL.

        Returns
        -------
        list of str
            The available files on the FTP server.
        """
        files = self._parser.files
        if glob is not None:
            files = [f for f in files if Path(f).match(glob)]

        return self._parser.files


def list_projects():
    """List all available projects on MassIVE.

    Returns
    -------
    list of str
        A list of MassIVE identifiers.
    """
    parser = FTPParser("ftp://massive.ucsd.edu/", max_depth=0)
    return parser.dirs
