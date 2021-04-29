"""A base dataset class"""
from pathlib import Path
from abc import ABC, abstractmethod

from .config import config


class BaseDataset(ABC):
    """A base class for ppx dataset classes.

    Paramters
    ---------
    identifier : str
        The identifier for the project in the repository
    local : str or Path-like, optional
        The local data directory in which this project's files will be
        downloaded.
    """
    def __init__(self, identifier, local=None):
        """Initialize a BaseDataset"""
        self.id = self._validate_id(identifier)
        self.local = local
        self._url = None
        self._parser = None

    @property
    def local(self):
        """The local data directory for this project"""
        return self._local

    @local.setter
    def local(self, path):
        """Set the local data directory for this project"""
        if path is None:
            self._local = Path(config.path, self.id)
        else:
            self._local = Path(path)

        self._local.mkdir(exist_ok=True)

    @property
    def url(self):
        """The web address associated with this project"""
        return self._url

    @abstractmethod
    def _validate_id(self, identifier):
        """Validate that the identifier is correct"""
        return identifier

    def local_dirs(self, glob=None):
        """List the local directories in the project"""
        if glob is None:
            glob = "**/*"

        dirs = self.local.glob(glob)
        return sorted([d for d in dirs if d.is_dir()])

    def local_files(self, glob=None):
        """List the local files in the project"""
        if glob is None:
            glob = "**/*"

        files = self.local.glob(glob)
        return sorted([f for f in files if f.is_file()])

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
