"""Test the download functionality of ppx

These tests are in a separate file because they all require internet access.
"""
import filecmp

import pytest
import ppx
from ftplib import FTP, error_temp

PXID = "PXD000001"
MSVID = "MSV000087408"


def test_no_internet(monkeypatch):
    """Test what happens when connection is blocked"""
    proj = ppx.PrideProject(PXID)
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


def sig(f):
    st = f.stat()
    return st.st_size, st.st_mtime
