"""
MassIVE datasets.
"""
from .utils import list_files, list_dirs, download


class MSVDataset:
    """Retrieve information about a MassIVE project

    Parameters
    ----------
    msv_id : str
        The MassIVE identifier.

    Attributes
    ----------
    url : str
    """
    def __init__(self, msv_id):
        """Instantiate a MSVDataset object"""
        if not isinstance(msv_id, str):
            raise TypeError("'msv_id' must be a string (str).")

        self._msv_id = msv_id = msv_id.upper()
        self._url = (f"ftp://massive.ucsd.edu/{self.msv_id}")

    @property
    def msv_id(self):
        """The MassIVE identifier for the project."""
        return self._msv_id

    @property
    def url(self):
        """The URL of the FTP server associated with the project"""
        return self._url

    def list_dirs(self, path=None):
        """
        List available directories on the FTP server.

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
        return list_dirs(self.url, path)

    def list_files(self, path=None):
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
        return list_files(self.url, path)

    def download(self, files=None, dest_dir=None, force_=False):
        """
        Download MassIVE files from the FTP location.

        By default, it will not download files that have a file
        with a matching name in the destination directory, `dest_dir`.

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
        return download(self.url, files, dest_dir, force_)
