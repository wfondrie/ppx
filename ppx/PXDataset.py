# PXDataset.py : ppx

import xml.etree.ElementTree as ET
from urllib.request import urlopen
from warnings import warn
from os.path import join, isfile, isdir
from os import makedirs
import shutil


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

    return(links)


def _vprint(x, v):
    """Print x if v is true."""
    if v:
        print(x)


class PXDataset:
    """Information about a ProteomeXchange dataset.

    Parameters
    ----------
    id : str
        A ProteomeXchange identifier, such as "PXD000001".

    Attributes
    ----------
    id : str
        The ProteomeXchange identifier returned by the server. There
        are cases where this may differ from the query identifier.

    formatVersion : str
        The XML schema version.

    data : xml.etree.ElementTree.ElementTree
        The parsed XML data returned by the ProteomeXchange server.

    """

    def __init__(self, id):
        """Instantiate a PXDataset object."""
        url = ("http://proteomecentral.proteomexchange.org/cgi/GetDataset?ID="
               + id + "&outputMode=XML&test=no")

        xml = ET.parse(urlopen(url))
        root = xml.getroot()

        self.formatVersion = root.attrib["formatVersion"]
        self.id = root.attrib["id"]
        self.data = xml

        if self.id != id:
            warn("The identifier, " + id + ", was not found. Retrieved "
                 + self.id + " instead.")

    def pxurl(cls):
        """Retrieve the URL for the data files of a PXDataset.

        Some ProteomeXchange submissions have data files that are
        deposited in the PRIDE repository. This method returns the URL
        of the PRIDE FTP site hosting the files for a PXDataset. Note
        that not all ProteomeXchange submissions have corresponding
        depositions in PRIDE.

        Parameters
        ----------
        None

        Returns
        -------
        str or None
            The URL of the data files. Returns None if no
            FTP location is listed.

        """
        links = _getNodes(cls.data, ".//cvParam[@accession='PRIDE:0000411']")
        if len(links) == 0:
            warn("No FTP URL found for " + cls.id + ".")
            return(None)

        return(links[0])

    def pxtax(cls):
        """Retrieve the sample taxonomies listed for a PXDataset.

        Parameters
        ----------
        None

        Returns
        -------
        list of str or None
            The species or other taxonimies list in a PXDataset
            submission. If not provided, returns None.

        """
        tax = _getNodes(cls.data, ".//cvParam[@accession='MS:1001469']")
        if len(tax) == 0:
            warn("No taxonomies reported for " + cls.id + ".")
            return(None)

        return(tax)

    def pxref(cls):
        """Retrieve references associated with a PXDataset.

        Parameters
        ----------
        None

        Returns
        -------
        list of str or None
            Both current and pending references are returned. Returns
            None if no references are found.

        """
        currRef = _getNodes(cls.data,
                            ".//cvParam[@accession='PRIDE:0000400']")
        pendRef = _getNodes(cls.data,
                            ".//cvParam[@accession='PRIDE:0000432']")

        allRef = currRef + pendRef
        if len(allRef) == 0:
            warn("No references reported for " + cls.id + ".")
            return(None)

        return(allRef)

    def pxfiles(cls):
        """List files available from the PRIDE FTP URL of a PXDataset.

        Parameters
        ----------
        None

        Returns
        -------
        list of str or None
            Returns a list of available files. Returns None if there is
            no PRIDE FTP location or no files at the location.

        """
        url = cls.pxurl()
        if url is None:
            return(None)

        lines = urlopen(url + "/").read().decode("UTF-8").splitlines()

        files = []
        for line in lines:
            files.append(line.split()[-1])
        return(files)

        if len(file) == 0:
            warn("No files were found at " + url + ".")
            return(None)

    def pxget(cls, files=None, destDir=".",
              force_=False, verbose=True):
        """Download PXDataset files from the PRIDE FTP location.

        By default, pxget() will not download files that have a file
        with a matching name in the destination directory, destDir.

        Parameters
        ----------
        files : str, list of str, or None
            Specifies the files to be downloaded. The default, None,
            downloads all files found with PXDataset.pxfiles().

        destDir : string
            Specifies the directory to download files into. If the
            directory does not exist, it will be created. The default
            is the current working directory.

        force_ : bool
            When False, files with matching name is destDir will not be
            downloaded again. True overides this, overwriting the
            matching file.

        verbose : bool
            Controls whether messages about download progress are
            printed.

        Returns
        -------
        None

        """
        if files is None:
            files = cls.pxfiles()
        elif isinstance(files, str):
            files = (files,)

        url = cls.pxurl()
        if not isdir(destDir):
            makedirs(destDir)

        for file in files:
            path = join(destDir, file)

            if isfile(path) and not force_:
                _vprint(path + " exists. Skipping file...", verbose)
                continue

            _vprint("Downloading " + file + "...", verbose)

            with urlopen(url + "/" + file) as dat, open(path, 'wb') as fout:
                shutil.copyfileobj(dat, fout)

        _vprint("Done!", verbose)
