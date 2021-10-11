"""Test the download functionality of ppx

These tests are in a separate file because they all require internet access.
"""
import filecmp
from ftplib import FTP, error_temp

import pytest
import ppx
import requests

PXID = "PXD000001"
MSVID = "MSV000087408"


def test_no_internet(monkeypatch):
    """Test what happens when connection is blocked"""
    proj = ppx.PrideProject(PXID, timeout=None)
    remote_files = proj.remote_files()
    fname = "F063721.dat-mztab.txt"

    def retrbinary(*args, **kwargs):
        raise OSError("Mock error")

    monkeypatch.setattr(FTP, "retrbinary", retrbinary)
    with pytest.raises(error_temp):
        txt = proj.download(fname)


def test_pride_download(tmp_path):
    """Test downloading data from PRIDE"""
    proj = ppx.PrideProject(PXID)
    files = proj.local_files()
    assert files == []

    fname = "F063721.dat-mztab.txt"
    txt = proj.download(fname)
    files = proj.local_files()
    local_txt = tmp_path / PXID / fname
    orig_sig = sig(local_txt)
    assert txt == [local_txt]
    assert files[0] == local_txt

    txt = proj.download(fname)  # should do nothing
    assert orig_sig == sig(local_txt)

    txt = proj.download(fname, force_=True)
    new_size, new_mtime = sig(local_txt)
    assert orig_sig[0] == new_size
    assert orig_sig[1] != new_mtime

    proj.timeout = 10
    assert proj._parser_state is None


def test_massive_api(tmp_path):
    """Test that the MassIVE API call is working"""
    proj = ppx.MassiveProject(MSVID, fetch=True)
    proj._url = None
    remote_files = proj.remote_files()
    assert len(remote_files) == 12

    remote_files = proj.remote_files("*.mzTab")
    assert len(remote_files) == 1

    proj.fetch = False
    info = [l for l in proj.file_info().splitlines() if l]
    print(info)
    assert len(info) == 13

    proj = ppx.MassiveProject(MSVID, fetch=True)
    proj._api = "blah"
    remote_files = proj.remote_files()
    assert len(remote_files) == 12

    proj._api = "https://api.github.com/user"  # A dummy URL...
    proj.remote_files()


def test_massive_download(tmp_path):
    """Test downloading data from massive"""
    proj = ppx.MassiveProject(MSVID)
    files = proj.local_files()
    assert files == []

    fname = "ccms_statistics/statistics.tsv"
    txt = proj.download(fname)
    files = proj.local_files()
    local_txt = tmp_path / MSVID / fname
    orig_sig = sig(local_txt)
    assert txt == [local_txt]
    assert files[0] == local_txt

    txt = proj.download(fname)  # should do nothing
    assert orig_sig == sig(local_txt)

    txt = proj.download(fname, force_=True)
    new_size, new_mtime = sig(local_txt)
    assert orig_sig[0] == new_size
    assert orig_sig[1] != new_mtime

    proj.timeout = 10
    assert proj._parser_state is None


def sig(f):
    st = f.stat()
    return st.st_size, st.st_mtime
