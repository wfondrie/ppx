"""A base dataset class"""
from pathlib import Path
from abc import ABC, abstractmethod

from . import utils
from .config import config


class BaseProject(ABC):
    """A base class for ppx project classes.

    Paramters
    ---------
    identifier : str
        The identifier for the project in the repository
    local : str or Path object, optional
        The local data directory in which this project's files will be
        downloaded.
    fetch : bool, optional
        Should ppx check the remote repository for updated metadata?
    """

    def __init__(self, identifier, local=None, fetch=False):
        """Initialize a BaseDataset"""
        self._id = self._validate_id(identifier)
        self.local = local
        self._url = None
        self._parser = None
        self._metadata = None
        self.fetch = fetch

    @property
    def fetch(self):
        """Should ppx check the remote repository for updated metadata?"""
        return self._fetch

    @fetch.setter
    def fetch(self, val):
        """Set the value of fetch."""
        self._fetch = bool(val)

    @property
    def id(self):
        """The repository identifier."""
        return self._id

    @property
    def local(self):
        """The local data directory for this project."""
        return self._local

    @local.setter
    def local(self, path):
        """Set the local data directory for this project."""
        if path is None:
            self._local = Path(config.path, self.id)
        else:
            self._local = Path(path)

        self._local.mkdir(exist_ok=True)

    @property
    def url(self):
        """The web address associated with this project."""
        return self._url

    @abstractmethod
    def _validate_id(self, identifier):
        """Validate that the identifier is correct."""
        return identifier

    @abstractmethod
    def remote_files(self, glob=None):
        """List the project files in the remote repository.

        Parameters
        ----------
        glob : str, optional
            Use Unix wildcards to return specific files. For example,
            "*.mzML" would return the mzML files.

        Returns
        -------
        list of str
            The files available for the project.
        """
        return None

    def local_dirs(self, glob=None):
        """List the local directories associated with this project.

        Parameters
        ----------
        glob : str, optional
            Use Unix wildcards to return specific files. For example,
            :code:`"*peak"` would return all directories ending in "peak".

        Returns
        -------
        list of str
            The local directories available for this project.
        """
        if glob is None:
            glob = "**/*"

        dirs = self.local.glob(glob)
        return sorted([d for d in dirs if d.is_dir()])

    def local_files(self, glob=None):
        """List the local files associated with this project.

        Parameters
        ----------
        glob : str, optional
            Use Unix wildcards to return specific files. For example,
            :code:`"*.mzML"` would return all of the mzML files.

        Returns
        -------
        list of str
            The local files available for this project.
        """
        if glob is None:
            glob = "**/*"

        files = self.local.glob(glob)
        return sorted([f for f in files if f.is_file()])

    def download(self, files, force_=False, silent=False):
        """Download files from the remote repository.

        These files are downloaded to this project's local data directory
        (:py:attr:`~ppx.MassiveProject.local`). By default, ppx will not
        redownload files with matching file names already present in the local
        data directory.

        Parameters
        ----------
        files : str or list of str
            One or more files to be downloaded from the remote repository.
        force_ : bool, optional
            Redownload files when files of the of the same name already appear
            in the local data directory?
        silent : bool, optional
            Hide download progress bars?

        Returns
        -------
        list of Path objects
            The paths of the downloaded files.

        """
        files = utils.listify(files)
        in_remote = [f in self.remote_files() for f in files]
        if not all(in_remote):
            missing = [f for i, f in zip(in_remote, files) if not i]

            raise FileNotFoundError(
                "The following files were not found in the remote repository: "
                f"{', '.join(missing)}"
            )

        return self._parser.download(
            files, self.local, force_=force_, silent=silent
        )
