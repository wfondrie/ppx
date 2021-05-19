"""MassIVE datasets."""
import re
import socket
import xml.etree.ElementTree as ET
from pathlib import Path

from .ftp import FTPParser
from .project import BaseProject


class MassiveProject(BaseProject):
    """Retrieve information about a MassIVE project.

    MassIVE: `<https://massive.ucsd.edu>`_

    Parameters
    ----------
    msv_id : str
        The MassIVE identifier.
    local : str or pathlib.Path object, optional
        The local data directory in which to download project files.
    fetch : bool, optional
        Should ppx check the remote repository for updated metadata?

    Attributes
    ----------
    id : str
    local : Path object
    url : str
    title : str
    description : str
    metadata : dict
    fetch : bool
    """

    def __init__(self, msv_id, local=None, fetch=False):
        """Instantiate a MSVDataset object"""
        super().__init__(msv_id, local, fetch)
        self._url = f"ftp://massive.ucsd.edu/{self.id}"

    def _validate_id(self, identifier):
        """Validate a MassIVE identifier.

        Parameters
        ----------
        identifier : str
            The project identifier to validate.

        Returns
        -------
        str
            The validated identifier.
        """
        identifier = str(identifier).upper()
        if not re.match("(MSV|RMS)[0-9]{9}", identifier):
            raise ValueError("Malformed MassIVE identifier.")

        return identifier

    @property
    def metadata(self):
        """The project metadata as a dictionary."""
        if self._metadata is None:
            remote_file = "ccms_parameters/params.xml"
            metadata_file = self.local / remote_file
            try:
                # Only fetch file if it doesn't exist and self.fetch is true:
                if metadata_file.exists():
                    assert self.fetch

                # Fetch the data from the remote repository:
                self.download(remote_file, force_=True, silent=True)

            except (AssertionError, socket.gaierror) as err:
                if not metadata_file.exists():
                    raise err

            # Parse the XML
            root = ET.parse(metadata_file).getroot()
            self._metadata = {e.attrib["name"]: e.text for e in root}

        return self._metadata

    @property
    def title(self):
        """The title of this project."""
        return self.metadata["desc"]

    @property
    def description(self):
        """A description of this project."""
        return self.metadata["dataset.comments"]


def list_projects():
    """List all available projects on MassIVE.

    MassIVE: `<https://massive.ucsd.edu>`_

    Returns
    -------
    list of str
        A list of MassIVE identifiers.
    """
    parser = FTPParser("ftp://massive.ucsd.edu/", max_depth=0)
    return parser.dirs
