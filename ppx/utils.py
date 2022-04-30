"""Utility Functions"""
from pathlib import Path

import requests
from cloudpathlib import CloudPath
from cloudpathlib.exceptions import CloudPathNotImplementedError


def listify(obj):
    """Turn an object into a list, but don't split strings"""
    try:
        assert not isinstance(obj, str)
        iter(obj)
    except (AssertionError, TypeError):
        obj = [obj]

    return list(obj)


def test_url(url):
    """Test if a URL exists.

    Parameters
    ----------
    url : str
        The URL to test.

    Returns
    -------
    str
        The input URL.
    """
    http_url = url.replace("ftp://", "http://")
    if http_url[-1] != "/":
        http_url += "/"

    res = requests.head(http_url)
    if res.status_code != 200:
        raise requests.HTTPError(f"Unable to connect to URL: {url}")

    return url


def glob(path, pattern=None):
    """A function to glob.

    Parameters
    ----------
    path : Path or CloudPath
        The path to search.
    pattern : str, optional
        The glob pattern.

    Returns
    -------
    list of Path or CloudPath
        The sorted list of files.
    """
    pattern = "**/[!.]*" if pattern is None else pattern
    return sorted(path.glob(pattern))
