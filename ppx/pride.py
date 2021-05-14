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
    local : str or Path-like object, optional
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
    doi : str
    data_processing_protocol : str
    sample_processing_protocol : str
    metadata : dict
    fetch : bool
    """

    rest = "https://www.ebi.ac.uk/pride/ws/archive/v2/projects/"

    def __init__(self, pride_id, local=None, fetch=False):
        """Instantiate a PrideDataset object"""
        super().__init__(pride_id, local, fetch)
        self._url = self.rest + self.id
        self._remote_files = None
        self._parser = None
        self._metadata = None

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
                self._metadata = get(self.url)
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
        if self._remote_files is None:
            res = get(self.url + "/files")["_embedded"]["files"]
            self._remote_files = [f["fileName"] for f in res]

        files = self._remote_files
        if glob is not None:
            files = [f for f in files if Path(f).match(glob)]

        return files

    def download(self, files, force_=False, silent=False):
        """Download files from the remote repository.

        These files are downloaded to this project's local data directory
        (:py:attr:`~ppx.PrideProject.local`). By default, ppx will not
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
        if self._parser is None:
            ftp_url = self.metadata["_links"]["datasetFtpUrl"]["href"]
            self._parser = FTPParser(ftp_url)

        return super().download(files=files, force_=force_, silent=silent)


def get(url):
    """Perform a GET command at the specified url."""
    res = requests.get(url)
    if res.status_code != 200:
        raise requests.HTTPError(f"Error {res.status_code}: {res.text}")

    return res.json()


def list_projects():
    """List all available projects on PRIDE

    PRIDE Archive: `<https://www.ebi.ac.uk/pride/archive/>`_

    Returns
    -------
    list of str
        A list of PRIDE identifiers.
    """
    url = "https://www.ebi.ac.uk/pride/ws/archive/v2/misc/sitemap"
    res = requests.get(url)
    if res.status_code != 200:
        raise requests.HTTPError(f"Error {res.status_code}: {res.text})")

    res = [p.split("/")[-1] for p in res.text.splitlines()]
    return [p for p in res if re.match("P[RX]D[0-9]{6}", p)]
