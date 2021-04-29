"""
Utility Functions
"""
import os
import shutil
import urllib.request
import logging
import time


def list_dirs(url, path=None):
    """
    List available directories on the FTP server.

    Parameters
    ----------
    url : str
        The URL of the FTP server.
    path : str or list of str, optional
        The subdirectory on the FTP server to look in. A list
        will be concatenated into a single URL.

    Returns
    -------
    list of str
         The directories available on the FTP server.
    """
    if isinstance(path, str):
        path = [path]

    if path is not None:
        url = "/".join([url] + path)

    _, dirs = parse_ftp(url)
    if not dirs:
        logging.warning("No directories were found at %s.", url)
        dirs = None

    return dirs


def list_files(url, path=None):
    """
    List available files on the FTP server.

    Parameters
    ----------
    url : str
        The URL of the FTP server.
    path : str or list of str, optional
        The subdirectory on the FTP server to look in. A list
        will be concatenated into a single URL.

    Returns
    -------
    list of str
        The available files on the FTP server.
    """
    if isinstance(path, str):
        path = [path]

    if path is not None:
        url = "/".join([url] + path)

    files, _ = parse_ftp(url)
    if not files:
        logging.warning("No files were found at %s.", url)
        files = None

    return files


def download(url, files=None, dest_dir=None, force_=False):
    """
    Download files from the FTP location.

    By default, it will not download files that have a file
    with a matching name in the destination directory, `dest_dir`.

    Parameters
    ----------
    url : str
        The URL of the FTQ server.
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
    if files is None:
        files = list_files(url)
    elif isinstance(files, str):
        files = [files]

    if dest_dir is not None:
        out_files = [os.path.join(dest_dir, os.path.split(f)[-1])
                     for f in files]
    else:
        out_files = files

    all_exist = all([os.path.isfile(f) for f in out_files])

    if all_exist and not force_:
        return out_files

    os.makedirs(dest_dir, exist_ok=True)
    for in_file, out_file in zip(files, out_files):
        if os.path.isfile(out_file) and not force_:
            continue

        logging.info("Downloading %s...", in_file)

        with openurl(f"{url}/{in_file}") as dat, \
                open(out_file, "wb") as fout:
            shutil.copyfileobj(dat, fout)

    return out_files


def listify(obj):
    """Turn an object into a list, but don't split strings"""
    try:
        assert not isinstance(obj, str)
        iter(obj)
    except (AssertionError, TypeError):
        obj = [obj]

    return list(obj)



def parse_ftp(url):
    """
    Parse the FTP server response.

    Parameters
    ----------
    url : str
        The url of the FTP server.

    Returns
    -------
    files : list of str
    directories : list of str
    """
    if not url.endswith("/"):
        url += "/"

    lines = openurl(url).read().decode("UTF-8").splitlines()
    files = []
    dirs = []
    for line in lines:
        line = line.split(maxsplit=8)
        if line[0].startswith("d"):
            dirs.append(line[-1])
        else:
            files.append(line[-1])

    return files, dirs


def getnodes(xml, xpath):
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


def openurl(url):
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
            if retries <= (max_retry - 1):
                time.sleep(3)
            else:
                raise

    return dat
