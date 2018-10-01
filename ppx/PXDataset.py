# PXDataset.py : ppx
# TODO: List comprehensions
# TODO: PX ID error checking.

import xml.etree.ElementTree as ET
import urllib.request
import logging
import os
import shutil
import time


def _getNodes(xml, XPath):
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
    root = xml.getroot()
    nodes = root.findall(XPath)

    links = []
    for node in nodes:
        links.append(node.attrib["value"])

    return links

def _openurl(url):
    """
    Open a URL using the ppx user-agent

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

    max_retry = 5
    retries = 0
    success = False
    while not success:
        retries += 1
        try:
            dat = urllib.request.urlopen(req, timeout = 50)
            success = True
        except urllib.error.URLError:
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

    def __init__(self, id):
        """Instantiate a PXDataset object."""
        url = ("http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID="
               + id + "&outputMode=XML&test=no")
        logging.debug(url)

        xml = ET.parse(_openurl(url))
        root = xml.getroot()

        self.formatVersion = root.attrib["formatVersion"]
        self.return_id = root.attrib["id"]
        self.query_id = id
        self.data = xml

        if self.return_id != id:
            logging.warning("The identifier, "
                            + id
                            + ", was not found. Retrieved "
                            + self.return_id
                            + " instead.")

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
        links = _getNodes(self.data, ".//cvParam[@accession='PRIDE:0000411']")
        if len(links) == 0:
            logging.warning("No FTP URL found for " + self.return_id + ".")
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
        tax = _getNodes(self.data, ".//cvParam[@accession='MS:1001469']")
        if len(tax) == 0:
            logging.warning("No taxonomies reported for "
                            + self.return_id
                            + ".")
            return None
        else:
            return tax

    def pxref(self):
        """Retrieve references associated with a PXDataset.

        Returns
        -------
        list of str or None
            Both current and pending references are returned. Returns
            None if no references are found.

        """
        curr_ref = _getNodes(self.data,
                             ".//cvParam[@accession='PRIDE:0000400']")
        pend_ref = _getNodes(self.data,
                             ".//cvParam[@accession='PRIDE:0000432']")

        all_ref = curr_ref + pend_ref
        if len(all_ref) == 0:
            logging.warning("No references reported for "
                            + self.return_id
                            + ".")
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

        files = []
        for line in lines:
            files.append(line.split()[-1])

        if len(files) == 0:
            logging.warning("No files were found at " + url + ".")
            return None
        else:
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
                logging.info(path + " exists. Skipping file...")
                continue

            logging.info("Downloading " + file + "...")

            with _openurl(url + "/" + file) as dat, open(path, 'wb') as fout:
                shutil.copyfileobj(dat, fout)

        logging.info("Done!")
