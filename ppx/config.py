"""This module contains the configuration details for ppx"""
import os
import logging
from pathlib import Path

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
                path = Path(os.environ["PPX_DATA_DIR"]).expanduser().resolve()
            except KeyError:
                path = Path(Path.home(), ".ppx")
                path.mkdir(exist_ok=True)
        else:
            path = Path(path).expanduser().resolve()
            if not path.exists():
                raise FileNotFoundError(
                    f"The specified directory ({path}) does not exist."
                )

        self._path = path


def get_data_dir():
    """Retrieve the current data directory for ppx."""
    return config.path


def set_data_dir(path=None):
    """Set the data dir"""
    config.path = path


# Initialize the configuration when loaded:
config = PPXConfig()
