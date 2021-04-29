"""MassIVE datasets."""
import re
from pathlib import Path

from .ftp import FTPParser
from .dataset import BaseDataset


class MassiveDataset(BaseDataset):
    """Retrieve information about a MassIVE project

    Parameters
    ----------
    msv_id : str
        The MassIVE identifier.

    Attributes
    ----------
    url : str
    """
    def __init__(self, msv_id, local=None):
        """Instantiate a MSVDataset object"""
        super().__init__(msv_id, local)
        self._url = f"ftp://massive.ucsd.edu/{self.msv_id}"
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

    def download(self, files, force_=False):
        """
        Download MassIVE files from the FTP location.

        By default, it will not download files that have a file
        with a matching name and path in the destination directory.

        Parameters
        ----------
        files : str or tuple of str, optional
            Specifies the files to be downloaded. The default, None,
            downloads all files found with MSVDataset.list_files().
        dest_dir : str, optional
            Specifies the directory to download files into. If the
            directory does not exist, it will be created. The default
            is the current working directory.
        force_ : bool, optional
            When False, files with matching name is dest_dir will not be
            downloaded again. True overides this, overwriting the
            matching file.

        Returns
        -------
        list of str
            A list of the downloaded files.
        """
        return self._parser.download(files, self.local, force_)
