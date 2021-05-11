"""A class for PRIDE datasets"""
import re
from pathlib import Path

import requests

from .ftp import FTPParser
from .config import config
from .project import BaseProject


class PrideProject(BaseProject):
    """Retrieve information about a PRIDE project

    Parameters
    ----------
    pride_id : str
        The PRIDE identifier.
    local : str or Path-like object, optional
        The local data directory in which to download project files.

    Attributes
    ----------
    id : str
    local : Path object
    url : str
    description : str
    doi : str
    data_processing_protocol : str
    sample_processing_protocol : str
    metadata : dict
    """
    rest = "https://www.ebi.ac.uk/pride/ws/archive/v2/projects/"

    def __init__(self, pride_id, local=None):
        """Instantiate a PrideDataset object"""
        super().__init__(pride_id, local)
        self._url = self.rest + self.id
        self._remote_files = None
        self._parser = None
        self._metadata = None

    def _validate_id(self, identifier):
        """Validate a PRIDE identifier

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
        """The project metadata as a nested dictionary"""
        if self._metadata is None:
            self._metadata = get(self.url)

        return self._metadata

    @property
    def title(self):
        """The title of the study associated with this project."""
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
            The remote files avaiable for this project.
        """
        if self._remote_files is None:
            res = get(self.url + "/files")["_embedded"]["files"]
            self._remote_files = [f["fileName"] for f in res]

        files = self._remote_files
        if glob is not None:
            files = [f for f in files if Path(f).match(glob)]

        return files

    def download(self, files, force_=False):
        """Download files from the remote repository

        These files are downloaded to this project's local data directory
        (:py:attr:`~ppx.PrideProject.local`). By default, ppx will not
        redownload files with matching file names already present in the
        local data directory.

        Parameters
        ----------
        files : str or list of str
            One or more files to be downloaded from the remote repository.
        force_ : bool, optional
            Redownload files when files of the of the same name already appear
            in the local data directory

        Returns
        -------
        list of Path objects
            The paths of the downloaded files.
        """
        if self._parser is None:
            ftp_url = self.metadata["_links"]["datasetFtpUrl"]["href"]
            self._parser = FTPParser(ftp_url)

        return super().download(files=files, force_=force_)


def get(url):
    """Perform a GET command at the specified url."""
    res = requests.get(url)
    if res.status_code != 200:
        raise requests.HTTPError(
            f"Error {res.status_code}: {res.text}"
        )

    return res.json()
