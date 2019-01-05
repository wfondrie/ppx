"""
This module contains the PXDataset class and its associated methods,
which are the foundation of the ppx package.
"""
import xml.etree.ElementTree as ET
import urllib.request
import logging
import os
import shutil
import time


def _getnodes(xml, xpath):
    """Retreive the 'value' attribute from a set of XML nodes.

    Parameters
    ----------
    xml : xml.etree.ElementTree.ElementTree
        XML data in the PXDataset.data attribute.

    XPath : str
        An XPath string used to the define the nodes of interest.

    Returns
    -------
    list of str
        A list containing the 'value' attribute for each node found

    """
    return [node.attrib["value"] for node in xml.getroot().findall(xpath)]


def _openurl(url):
    """
    Open a URL using the ppx user-agent. If an URLError is raised,
    such as by a timeout, the request will retry up to 5 times.

    Parameters
    ----------
    url : str
        The URL to open.

    Return
    ------
    Whatever urllib.request.urlopen() would return.
    """
    req = urllib.request.Request(url)
    req.add_header("user-agent", "ppx (https://pypi.org/project/ppx/)")

    # Retries were added after Travic-CI build failures. These seem to
    # have been necessary due to connectivity issues on Travis servers.
    # Retries may not be needed in normal settings.
    max_retry = 5
    retries = 0
    success = False
    while not success:
        retries += 1
        try:
            dat = urllib.request.urlopen(req, timeout=100)
            success = True
        except urllib.error.URLError:
            logging.debug("Attempt %s  download failed...", retries)
            if retries <= max_retry:
                time.sleep(3)
            else:
                raise

    return dat


class PXDataset:
    """Information about a ProteomeXchange dataset.

    Parameters
    ----------
    id : str
        A ProteomeXchange identifier, such as "PXD000001".

    Attributes
    ----------
    return_id : str
        The ProteomeXchange identifier returned by the server. There
        are cases where this may differ from the query identifier.

    query_id : str
        The query ProteomeXchange identifier.

    formatVersion : str
        The XML schema version.

    data : xml.etree.ElementTree.ElementTree
        The parsed XML data returned by the ProteomeXchange server.

    """
    def __init__(self, pxid):
        """Instantiate a PXDataset object."""
        pxid = pxid.upper()
        pxid_conditions = [isinstance(pxid, str),
                           len(pxid) == 9,
                           pxid[0:3] == "PXD" or pxid[0:3] == "PRD",
                           pxid[3:9].isdigit()]

        if not all(pxid_conditions):
            raise Exception("Malformed ProteomeXchange identifier.")

        url = ("http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID="
               + pxid + "&outputMode=XML&test=no")
        logging.debug(url)

        xml = ET.parse(_openurl(url))
        root = xml.getroot()

        self.format_version = root.attrib["formatVersion"]
        self.return_id = root.attrib["id"]
        self.query_id = pxid
        self.data = xml

        if self.return_id != pxid:
            logging.warning("The identifier, %s, was not found. Retrieved "
                            "%s instead.", pxid, self.return_id)

    def pxurl(self):
        """Retrieve the URL for the data files of a PXDataset.

        Some ProteomeXchange submissions have data files that are
        deposited in the PRIDE repository. This method returns the URL
        of the PRIDE FTP site hosting the files for a PXDataset. Note
        that not all ProteomeXchange submissions have corresponding
        depositions in PRIDE.

        Returns
        -------
        str or None
            The URL of the data files. Returns None if no
            FTP location is listed.

        """
        links = _getnodes(self.data, ".//cvParam[@accession='PRIDE:0000411']")
        if not links:
            logging.warning("No FTP URL found for %s.", self.return_id)
            return None

        return links[0]

    def pxtax(self):
        """Retrieve the sample taxonomies listed for a PXDataset.

        Returns
        -------
        list of str or None
            The species or other taxonimies list in a PXDataset
            submission. If not provided, returns None.

        """
        tax = _getnodes(self.data, ".//cvParam[@accession='MS:1001469']")
        if not tax:
            logging.warning("No taxonomies reported for %s.", self.return_id)
            tax = None

        return tax

    def pxref(self):
        """Retrieve references associated with a PXDataset.

        Returns
        -------
        list of str or None
            Both current and pending references are returned. Returns
            None if no references are found.

        """
        curr_ref = _getnodes(self.data,
                             ".//cvParam[@accession='PRIDE:0000400']")
        pend_ref = _getnodes(self.data,
                             ".//cvParam[@accession='PRIDE:0000432']")

        all_ref = curr_ref + pend_ref
        if not all_ref:
            logging.warning("No references reported for %s.", self.return_id)
            return None

        return all_ref

    def pxfiles(self):
        """List files available from the PRIDE FTP URL of a PXDataset.

        Returns
        -------
        list of str or None
            Returns a list of available files. Returns None if there is
            no PRIDE FTP location or no files at the location.

        """
        url = self.pxurl()
        if url is None:
            return None

        lines = _openurl(url + "/").read().decode("UTF-8").splitlines()
        files = [line.split(maxsplit=8)[-1] for line in lines]

        if not files:
            logging.warning("No files were found at %s.", url)
            files = None

        return files

    def pxget(self, files=None, dest_dir=".", force_=False):
        """Download PXDataset files from the PRIDE FTP location.

        By default, pxget() will not download files that have a file
        with a matching name in the destination directory, dest_dir.

        Parameters
        ----------
        files : str, list of str, or None
            Specifies the files to be downloaded. The default, None,
            downloads all files found with PXDataset.pxfiles().

        dest_dir : string
            Specifies the directory to download files into. If the
            directory does not exist, it will be created. The default
            is the current working directory.

        force_ : bool
            When False, files with matching name is dest_dir will not be
            downloaded again. True overides this, overwriting the
            matching file.

        Returns
        -------
        None

        """
        if files is None:
            files = self.pxfiles()
        elif isinstance(files, str):
            files = (files,)

        url = self.pxurl()
        if not os.path.isdir(dest_dir):
            os.makedirs(dest_dir)

        for file in files:
            path = os.path.join(dest_dir, file)

            if os.path.isfile(path) and not force_:
                logging.info("%s exists. Skipping file...", path)
                continue

            logging.info("Downloading %s...", file)

            with _openurl(url + "/" + file) as dat, open(path, 'wb') as fout:
                shutil.copyfileobj(dat, fout)

        logging.info("Done!")
