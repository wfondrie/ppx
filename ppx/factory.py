"""
This module contains the PXDataset class and its associated methods,
which are the foundation of the ppx package.
"""
import re
import logging
from urllib.parse import urlparse

import requests

from .pride import PrideProject
from .massive import MassiveProject

LOGGER = logging.getLogger(__name__)


class PXDFactory:
    """Retrieve information about a ProteomeXchange project.

    Parameters
    ----------
    pxid : str
        A ProteomeXchange identifier.
    local : str or Path object, optional
        The local data directory in which this project's files will be
        downloaded.
    fetch : bool, optional
        Should ppx check the remote repository for updated metadata?
    timeout : float, optional
        The maximum amount of time to wait for a server response.
    """

    rest = "http://proteomecentral.proteomexchange.org/cgi/GetDataset"

    repo_cv = {
        "MS:1002487": "MassIVE",
        "MS:1002632": "jPOST",
        "MS:1002836": "iProx",
        "MS:1002872": "Panorama",
    }

    ftp_map = {
        "ftp.pride.ebi.ac.uk": "PRIDE",
        "massive.ucsd.edu": "MassIVE",
    }

    def __init__(self, pxid, local=None, fetch=False, timeout=10.0):
        """Instantiate a PXDataset"""
        self._id = self._validate_id(pxid)
        self._local = local
        self._fetch = fetch
        self._timeout = timeout

        # Retrieve the data:
        params = {"ID": self.id, "outputMode": "JSON", "test": "no"}
        res = requests.get(self.rest, params=params, timeout=self._timeout)
        if res.status_code != 200:
            raise requests.HTTPError(f"Error {res.status_code}: {res.text}")

        self._url = res.url
        self._data = res.json()

        # Determine the partner repository
        self._repo, self._repo_id = self._resolve_repo()
        if self._repo_id != self.id:
            LOGGER.warning(
                "Repository ID %s differed from provided ID %s",
                self._repo_id,
                self.id,
            )

    @property
    def id(self):
        """The ProteomeXchange project identifier"""
        return self._id

    def find(self):
        """Find the dataset at the partner repository"""
        kwargs = dict(
            local=self._local,
            fetch=self._fetch,
            timeout=self._timeout,
        )

        if self._repo == "PRIDE":
            return PrideProject(self._repo_id, **kwargs)

        if self._repo == "MassIVE":
            return MassiveProject(self._repo_id, **kwargs)

        raise RuntimeError("Unsupported partner repository.")

    def _resolve_repo(self):
        """Resolve what repository the data is in."""
        repos = {}
        for repo_id in self._data["identifiers"]:
            repo_name = self.repo_cv.get(repo_id["accession"])
            if repo_name is not None:
                repos[repo_name] = repo_id["value"]

        for link in self._data["fullDatasetLinks"]:
            if link["name"] == "Dataset FTP location":
                repo_name = self.ftp_map.get(urlparse(link["value"]).netloc)
                if repo_name == "PRIDE":
                    repos["PRIDE"] = self.id

        if not repos:
            raise ValueError(
                "No supported ProteomeXchange partner repository was found for"
                f" {self.id}. ppx currently supports PRIDE and MassIVE."
            )

        repo_order = ["PRIDE", "MassIVE"]
        for repo in repo_order:
            repo_id = repos.get(repo)
            if repo_id is not None:
                return repo, repo_id

        repo = ", ".join(repos.keys())
        raise ValueError(
            f"{self.id} was found in {repo}, which is not supported by ppx at "
            "this time. ppx currently supports PRIDE and MassIVE."
        )

    def _validate_id(self, identifier):
        """Validate a ProteomeXchange identifier"""
        identifier = str(identifier).upper()
        if not re.match("P[XR]D[0-9]{6}", identifier):
            raise ValueError("Malformed ProteomeXchange identifier.")

        return identifier


def find_project(identifier, local=None, repo=None, fetch=False, timeout=10.0):
    """Find a project in the PRIDE or MassIVE repositories.

    Parameters
    ----------
    identifier : str
        The project identifier.
    local : str or Path-like object, optional
        The directory where ppx will look for and download files from this
        project. The default is :code:`~/.ppx`
    repo : {"pride", "massive"}, optional
        The repository in which to look for the project. If :code:`None`,
        ppx will try to figure it out.
    fetch : bool, optional
        Should ppx check the remote repository for updated metadata?
    timeout : float, optional
        The maximum amount of time to wait for a server response

    Returns
    -------
    :py:class:`~ppx.PrideProject` or :py:class:`~ppx.MassiveProject`
        An object to interact with the project data in the repository.
    """
    identifier = str(identifier).upper()
    if repo is not None:
        repo = str(repo).lower()

    # User-specified:
    kwargs = dict(local=local, fetch=fetch, timeout=timeout)
    if repo == "pride":
        return PrideProject(identifier, **kwargs)

    if repo == "massive":
        return MassiveProject(identifier, **kwargs)

    if repo is not None:
        raise ValueError("Unsupported repository.")

    # Try and figure it out:
    if identifier.startswith("MSV") or identifier.startswith("RMS"):
        return MassiveProject(identifier, **kwargs)

    if re.match("P[XR]D", identifier):
        try:
            return PXDFactory(identifier, **kwargs).find()
        except requests.HTTPError:
            return PrideProject(identifier, **kwargs)

    raise ValueError("Malformed identifier.")
