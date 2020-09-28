"""
This module contains the PXDataset class and its associated methods,
which are the foundation of the ppx package.
"""
import xml.etree.ElementTree as ET
import logging

from .utils import getnodes, openurl, list_files, list_dirs, download


class PXDataset:
    """Retrieve information about a ProteomeXchange project.

    Parameters
    ----------
    pxid : str
        A ProteomeXchange identifier, such as "PXD000001".

    Attributes
    ----------
    name : str
    description : str
    taxonomies : list of str
    references : list of str
    url : str
    return_id : str
    query_id : str
    data : xml.etree.ElementTree.ElementTree
    """
    def __init__(self, pxid):
        """Instantiate a PXDataset object."""

        if not isinstance(pxid, str):
            raise TypeError("'pxid' must be a string (str).")

        pxid = pxid.upper()
        pxid_conditions = [len(pxid) == 9,
                           pxid[0:3] == "PXD" or pxid[0:3] == "PRD",
                           pxid[3:9].isdigit()]

        if not all(pxid_conditions):
            raise ValueError("Malformed ProteomeXchange identifier.")

        url = (f"http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID="
               f"{pxid}&outputMode=XML&test=no")

        logging.debug("ProteomeXchange URL is %s", url)

        xml = ET.parse(openurl(url))
        root = xml.getroot()

        self._format_version = root.attrib["formatVersion"]
        self._return_id = root.attrib["id"]
        self._query_id = pxid
        self._data = xml

        if self._return_id != pxid:
            logging.warning("The identifier, %s, was not found. Retrieved "
                            "%s instead.", pxid, self._return_id)

    @property
    def return_id(self):
        """
        The ProteomeXchange identifier returned by the server. There
        are cases where this may differ from the query identifier.
        """
        return self._return_id

    @property
    def query_id(self):
        """The queried ProteomeXchange identifier."""
        return self._query_id

    @property
    def data(self):
        """The parsed XML data returned by the ProteomeXchange server."""
        return self._data

    @property
    def url(self):
        """The URL of the FTP server associated with the project."""
        links = getnodes(self.data,
                         ".//cvParam[@name='Dataset FTP location']")

        if not links:
            raise ValueError(f"No FTP URL found for {self.return_id}.")

        link = links[0]

        # This fixes an annoying bug caused by PRIDE URL changes.
        # See https://github.com/lgatto/rpx/issues/5 for details.
        if (link.startswith("ftp://ftp.pride.ebi")
                and "pride/data/archive" not in link):
            link = link.replace("ebi.ac.uk/", "ebi.ac.uk/pride/data/archive/")

        return link

    @property
    def taxonomies(self):
        """The species and other taxonomies provided for the project."""
        tax = getnodes(self.data, ".//cvParam[@accession='MS:1001469']")
        if not tax:
            logging.warning("No taxonomies reported for %s.", self.return_id)
            tax = None

        return tax

    @property
    def references(self):
        """Bibliographic information for the project."""
        curr_ref = getnodes(self.data,
                            ".//cvParam[@accession='PRIDE:0000400']")
        pend_ref = getnodes(self.data,
                            ".//cvParam[@accession='PRIDE:0000432']")

        all_ref = curr_ref + pend_ref
        if not all_ref:
            logging.warning("No references reported for %s.", self.return_id)
            all_ref = None

        return all_ref

    @property
    def description(self):
        """A description of the project."""
        desc = self.data.getroot().find(".//Description")
        if desc is None:
            return None

        return desc.text

    @property
    def name(self):
        """The name of the project."""
        name = self.data.getroot().find(".//RepositoryRecord")
        if name is None:
            return None

        return name.attrib["name"]

    def list_dirs(self, path=None):
        """
        List available directories on the FTP server.

        Parameters
        ----------
        path : str or list of str, optional
            The subdirectory on the FTP server to look in. A list
            will be concatenated into a single URL.

        Returns
        -------
        list of str
             The directories available on the FTP server.
        """
        return list_dirs(self.url, path)

    def list_files(self, path=None):
        """
        List available files on the FTP server.

        Parameters
        ----------
        path : str or list of str, optional
            The subdirectory on the FTP server to look in. A list
            will be concatenated into a single URL.

        Returns
        -------
        list of str
            The available files on the FTP server.
        """
        return list_files(self.url, path)

    def download(self, files=None, dest_dir=None, force_=False):
        """
        Download PXDataset files from the PRIDE FTP location.

        By default, it will not download files that have a file
        with a matching name in the destination directory, `dest_dir`.

        Parameters
        ----------
        files : str or tuple of str, optional
            Specifies the files to be downloaded. The default, None,
            downloads all files found with PXDataset.list_files().
        dest_dir : str, optional
            Specifies the directory to download files into. If the
            directory does not exist, it will be created. The default
            is the current working directory.
        force_ : bool, optional
            When False, files with matching name is dest_dir will not be
            downloaded again. True overides this, overwriting the
            matching file.

        Returns
        -------
        list of str
            A list of the downloaded files.
        """
        return download(self.url, files, dest_dir, force_)

    # Depricated methods:
    def pxref(self):
        """Deprecated"""
        logging.warning("'PXDataset.pxref()' is deprecated. Use "
                        "'PXDataset.references' instead.")
        return self.references

    def pxurl(self):
        """Deprecated"""
        logging.warning("'PXDataset.pxurl()' is deprecated. Use "
                        "'PXDataset.url' instead.")
        return self.url

    def pxtax(self):
        """Deprecated"""
        logging.warning("'PXDataset.pxtax()' is deprecated. Use "
                        "'PXDataset.taxonomies' instead.")
        return self.references

    def pxfiles(self):
        """Deprecated"""
        logging.warning("'PXDataset.pxfiles()' is deprecated. Use "
                        "'PXDataset.list_files()' instead.")
        return self.list_files()

    def pxget(self, files, dest_dir="."):
        """Deprecated"""
        logging.warning("'PXDataset.pxget()' is deprecated. Use "
                        "'PXDataset.download()' instead.")
        _ = self.download(files, dest_dir)
