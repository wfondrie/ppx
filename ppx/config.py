"""This module contains the configuration details for ppx"""

import logging
import os
from pathlib import Path

from cloudpathlib import AnyPath

LOGGER = logging.getLogger(__name__)


class PPXConfig:
    """Configure the data directory for ppx

    Attributes
    ----------
    path : pathlib.Path object

    """

    def __init__(self):
        """Initialize the _PPXDataDir"""
        self._path = None
        self.path = os.getenv("PPX_DATA_DIR")

    @property
    def path(self):
        """The current ppx data directory."""
        return self._path

    @path.setter
    def path(self, path):
        """Set the current ppx data directory"""
        if path is None:
            try:
                path = self._resolve_path(os.environ["PPX_DATA_DIR"])
                if not path.exists():
                    raise FileNotFoundError(
                        f"The specified PPX_DATA_DIR ({path}) does not exist."
                    )
            except KeyError:
                path = Path.home() / ".ppx"
        else:
            path = self._resolve_path(path)
            if not path.exists():
                raise FileNotFoundError(
                    f"The specified directory or bucket ({path}) "
                    "does not exist."
                )

        self._path = path

    @staticmethod
    def _resolve_path(path):
        """Resolve a Path or CloudPath

        Parameters
        ----------
        path : str
            The path to resolve.

        Returns
        -------
        Path or CloudPath
            The resolved path.

        """
        path = AnyPath(path)
        try:
            path = path.expanduser().resolve()
        except AttributeError:
            pass

        return path


def get_data_dir():
    """Retrieve the current data directory for ppx."""
    return config.path


def set_data_dir(path=None):
    """Set the ppx data directory.

    Parameters
    ----------
    path : str or pathlib.Path object, optional
        The path for ppx to use as its data directory.

    """
    config.path = path


# Initialize the configuration when loaded:
config = PPXConfig()
