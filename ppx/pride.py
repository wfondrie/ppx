"""A class for PRIDE datasets"""
import re
import json
from pathlib import Path

import requests

from .ftp import FTPParser
from .config import config
from .project import BaseProject


class PrideProject(BaseProject):
    """Retrieve information about a PRIDE project.

    PRIDE Archive: `<https://www.ebi.ac.uk/pride/archive/>`_

    Parameters
    ----------
    pride_id : str
        The PRIDE identifier.
    local : str or pathlib.Path object, optional
        The local data directory in which to download project files.
    fetch : bool, optional
        Should ppx check the remote repository for updated metadata?
    timeout : float, optional
        The maximum amount of time to wait for a server response.

    Attributes
    ----------
    id : str
    local : Path object
    url : str
    title : str
    description : str
    doi : str
    data_processing_protocol : str
    sample_processing_protocol : str
    metadata : dict
    fetch : bool
    timeout : float
    """

    rest = "https://www.ebi.ac.uk/pride/ws/archive/v2/projects/"
    file_rest = "https://www.ebi.ac.uk/pride/ws/archive/v2/files/byProject"

    def __init__(self, pride_id, local=None, fetch=False, timeout=10.0):
        """Instantiate a PrideDataset object"""
        super().__init__(pride_id, local, fetch, timeout)
        self._rest_url = self.rest + self.id

    def _validate_id(self, identifier):
        """Validate a PRIDE identifier.

        Parameters
        ----------
        identifier : str
            The project identifier to validate.

        Returns
        -------
        str
            The validated identifier
        """
        identifier = str(identifier).upper()
        if not re.match("P[RX]D[0-9]{6}", identifier):
            raise ValueError("Malformed PRIDE identifier.")

        return identifier

    @property
    def url(self):
        """The FTP address associated with this project."""
        if self._url is None:
            self._url = self.metadata["_links"]["datasetFtpUrl"]["href"]

            # Hotfix for the latest PRIDE FTP change. See issue #18.
            # Hopefully we can delete this once the REST API is updated.
            self._url = self._url.replace(
                "pride/data/archive",
                "pride-archive",
            )

        return self._url

    @property
    def metadata(self):
        """The project metadata as a nested dictionary."""
        if self._metadata is None:
            metadata_file = self.local / ".pride-metadata"
            # Try to update metadata first:
            try:
                # Only fetch file if it doesn't exist and self.fetch is true:
                if metadata_file.exists():
                    assert self.fetch

                # Fetch the data from the remote repository
                self._metadata = get(self._rest_url)
                with metadata_file.open("w+") as ref:
                    json.dump(self._metadata, ref)

            except (AssertionError, requests.ConnectionError) as err:
                if not metadata_file.exists():
                    raise err

                with metadata_file.open() as ref:
                    self._metadata = json.load(ref)

        return self._metadata

    @property
    def title(self):
        """The title of this project."""
        return self.metadata["title"]

    @property
    def description(self):
        """A description of this project."""
        return self.metadata["projectDescription"]

    @property
    def sample_processing_protocol(self):
        """The sample processing protocol for this project."""
        return self.metadata["sampleProcessingProtocol"]

    @property
    def data_processing_protocol(self):
        """The data processing protocol for this project."""
        return self.metadata["dataProcessingProtocol"]

    @property
    def doi(self):
        """The DOI for this project."""
        return self.metadata["doi"]


def get(url, **kwargs):
    """Perform a GET command at the specified url."""
    res = requests.get(url, **kwargs)
    if res.status_code != 200:
        raise requests.HTTPError(f"Error {res.status_code}: {res.text}")

    return res.json()


def list_projects(timeout=10.0):
    """List all available projects on PRIDE

    PRIDE Archive: `<https://www.ebi.ac.uk/pride/archive/>`_

    Parameters
    ----------
    timeout : float, optional
        The maximum amount of time to wait for a response from the server.

    Returns
    -------
    list of str
        A list of PRIDE identifiers.
    """
    url = "https://www.ebi.ac.uk/pride/ws/archive/v2/misc/sitemap"
    res = requests.get(url, timeout=timeout)
    if res.status_code != 200:
        raise requests.HTTPError(f"Error {res.status_code}: {res.text})")

    res = [p.split("/")[-1] for p in res.text.splitlines()]
    projects = [p for p in res if re.match("P[RX]D[0-9]{6}", p)]
    projects.sort()
    return projects
