"""This module contains the configuration details for ppx"""
import os
from pathlib import Path


class _PPXDataDir:
    """Configure the data directory for ppx

    Attributes
    ----------
    path : pathlib.Path object
    """
    def __init__(self):
        """Initialize the _PPXDataDir"""
        path = os.getenv("PPX_DATA_DIR")
        if path is None:
            self._path = Path(Path.home(), ".ppx")
            self._path.mkdir(exist_ok=True)
        else:
            self._path = Path(path).expanduser().resolve()
            if not self._path.exists():
                raise FileNotFoundError(
                    "The directory specified by the PPX_DATA_DIR environment "
                    f"variable does not exist ({self._path})."
                )

    @property
    def path(self):
        """The current ppx data directory."""
        return self._path

    @path.setter
    def path(self, path=None):
        """Set the current ppx data directory"""
        if path is None:
            path = Path(Path.home(), ".ppx")
            path.mkdir(exist_ok=True)
        else:
            path = Path(path).expanduser().resolve()
            if not path.exists():
                raise FileNotFoundError(
                    f"The specified directory ({path}) does not exist."
                )

        self._path = path
