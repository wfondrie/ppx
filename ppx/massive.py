"""MassIVE datasets."""
import re
import socket
import logging
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

from .ftp import FTPParser
from .project import BaseProject

LOGGER = logging.getLogger(__name__)


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
    timeout : float, optional
        The maximum amount of time to wait for a server response.

    Attributes
    ----------
    id : str
    local : Path object
    url : str
    title : str
    description : str
    metadata : dict
    fetch : bool
    timeout : float
    """

    _api = "https://gnps-datasetcache.ucsd.edu/datasette/database/filename.csv"

    def __init__(self, msv_id, local=None, fetch=False, timeout=10.0):
        """Instantiate a MSVDataset object"""
        super().__init__(msv_id, local, fetch, timeout)
        self._url = f"ftp://massive.ucsd.edu/{self.id}"
        self._params = dict(
            _stream="on",
            _sort="filepath",
            dataset__exact=self.id,
            _size="max",
        )

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
            try:
                info = self.file_info().splitlines()[1:]
                self._remote_files = [
                    r.split(",")[0].split("/", 1)[1] for r in info
                ]
            except (
                ConnectionRefusedError,
                ConnectionResetError,
                socket.timeout,
                socket.gaierror,
                socket.herror,
                EOFError,
                OSError,
            ):
                LOGGER.debug("Scraping the FTP server for files...")
                self._remote_files = self._parser.files

        if glob is not None:
            files = [f for f in self._remote_files if Path(f).match(glob)]
        else:
            files = self._remote_files

        return files

    def file_info(self):
        """Retrieve information about the project files.

        Returns
        -------
        str
            Information about the files in a CSV format.
        """
        file_info_path = self.local / ".file_info.csv"
        if file_info_path.exists() and not self.fetch:
            with file_info_path.open("r") as ref:
                return ref.read()

        res = requests.get(
            self._api,
            params=self._params,
            timeout=self.timeout,
        )

        if res.status_code != 200:
            raise requests.HTTPError(f"Error {res.status_code}: {res.text}")

        with file_info_path.open("w+") as ref:
            ref.write(res.text)

        return res.text


def list_projects(timeout=10.0):
    """List all available projects on MassIVE.

    MassIVE: `<https://massive.ucsd.edu>`_

    Parameters
    ----------
    timeout : float, optional
        The maximum amount of time to wait for a response from the server.

    Returns
    -------
    list of str
        A list of MassIVE identifiers.
    """
    url = "https://gnps-datasetcache.ucsd.edu/datasette/database.csv"
    params = dict(sql="select distinct dataset from filename", _size="max")
    try:
        res = requests.get(url, params, timeout=timeout).text.splitlines()[1:]
        res.sort()
        return res

    except (
        ConnectionRefusedError,
        ConnectionResetError,
        socket.timeout,
        socket.gaierror,
        socket.herror,
        EOFError,
        OSError,
    ):
        LOGGER.debug("Scraping the FTP server for projects...")

    parser = FTPParser("ftp://massive.ucsd.edu/", max_depth=0, timeout=timeout)
    return parser.dirs
