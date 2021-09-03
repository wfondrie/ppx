"""A base dataset class"""
from pathlib import Path
from abc import ABC, abstractmethod

from . import utils
from .config import config
from .ftp import FTPParser


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
    timeout : float, optional
        The maximum amount of time to wait for a server response.
    """

    def __init__(self, identifier, local=None, fetch=False, timeout=10.0):
        """Initialize a BaseDataset"""
        self._id = self._validate_id(identifier)
        self.local = local
        self.fetch = fetch
        self.timeout = timeout
        self._url = None
        self._parser_state = None
        self._metadata = None
        self._remote_files = None
        self._remote_dirs = None

    @property
    def timeout(self):
        """The maximum amount of time to wait for a server response."""
        return self._timeout

    @timeout.setter
    def timeout(self, wait):
        """Set the timeout for requests"""
        self._timeout = wait
        self._parser_state = None  # Reset the connection for new timeout.

    @property
    def _parser(self):
        """The FTPParser"""
        if self._parser_state is None:
            self._parser_state = FTPParser(self.url, timeout=self._timeout)

        return self._parser_state

    @property
    def _remote_files(self):
        """The cached remote files"""
        return self._cached_remote_files

    @_remote_files.setter
    def _remote_files(self, files):
        """Cache the remote files if not None"""
        cache_file = self.local / ".remote_files"
        self._cached_remote_files = cache(files, cache_file, self.fetch)

    @property
    def _remote_dirs(self):
        """The cached remote files"""
        return self._cached_remote_dirs

    @_remote_dirs.setter
    def _remote_dirs(self, dirs):
        """Cache the remote files if not None"""
        cache_file = self.local / ".remote_dirs"
        self._cached_remote_dirs = cache(dirs, cache_file, self.fetch)

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
            if config.path == Path(Path.home(), ".ppx"):
                config.path.mkdir(exist_ok=True)

            self._local = Path(config.path, self.id)
        else:
            self._local = Path(path)

        self._local.mkdir(exist_ok=True)

    @property
    def url(self):
        """The FTP address associated with this project."""
        return self._url

    @abstractmethod
    def _validate_id(self, identifier):
        """Validate that the identifier is correct."""
        return identifier

    def remote_dirs(self, glob=None):
        """List the project directories in the remote repository.

        Parameters
        ----------
        glob : str, optional
            Use Unix wildcards to return specific files. For example,
            :code:`"*peak"` would return all directories ending in "peak".

        Returns
        -------
        list of str
            The remote directories available for this project.
        """
        if self.fetch or self._remote_dirs is None:
            self._remote_dirs = self._parser.dirs

        if glob is not None:
            dirs = [d for d in self._remote_dirs if Path(d).match(glob)]
        else:
            dirs = self._remote_dirs

        return dirs

    def remote_files(self, glob=None):
        """List the project files in the remote repository.

        Parameters
        ----------
        glob : str, optional
            Use Unix wildcards to return specific files. For example,
            :code:`"*.mzML"` would return all of the mzML files.

        Returns
        -------
        list of str
            The remote files available for this project.
        """
        if self.fetch or self._remote_files is None:
            self._remote_files = self._parser.files

        if glob is not None:
            files = [f for f in self._remote_files if Path(f).match(glob)]
        else:
            files = self._remote_files

        return files

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
            glob = "**/[!.]*"

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
            glob = "**/[!.]*"

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
            Force the files to be downloaded, even if they already exist.
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


def cache(files, cache_file, fetch):
    """Save and retrieve the file or directory lists.

    Parameters
    ----------
    files : list of str
        The file names to save
    cache_file : Path
        The file to save them to.
    fetch : bool
        Overide the cached file if True

    Returns
    -------
    list of str
        The newly cached or loaded files.
    """
    if not fetch and files is None:
        if cache_file.exists():
            with cache_file.open() as ref:
                return ref.read().splitlines()
        else:
            return None

    elif files is not None:
        files = utils.listify(files)
        with cache_file.open("w+") as ref:
            ref.write("\n".join(files))

        return files

    return None
