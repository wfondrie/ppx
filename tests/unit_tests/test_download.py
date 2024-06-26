"""Test the download functionality of ppx

These tests are in a separate file because they all require internet access.
"""

from ftplib import FTP, error_temp

import pytest

import ppx

from . import utils

PXID = "PXD000001"
MSVID = "MSV000087408"
RMSVID = "RMSV000000253"


def test_no_internet(monkeypatch):
    """Test what happens when connection is blocked"""
    proj = ppx.PrideProject(PXID, timeout=None)
    proj.remote_files()
    fname = "F063721.dat-mztab.txt"

    def retrbinary(*args, **kwargs):
        raise OSError("Mock error")

    monkeypatch.setattr(FTP, "retrbinary", retrbinary)
    with pytest.raises(error_temp):
        proj.download(fname)


def test_pride_download(tmp_path):
    """Test downloading data from PRIDE"""
    proj = ppx.PrideProject(PXID)
    files = proj.local_files()
    assert files == []

    fname = "F063721.dat-mztab.txt"
    txt = proj.download(fname)
    files = proj.local_files()
    local_txt = tmp_path / PXID / fname
    orig_sig = utils.sig(local_txt)
    assert txt == [local_txt]
    assert files[0] == local_txt

    txt = proj.download(fname)  # should do nothing
    assert orig_sig == utils.sig(local_txt)

    txt = proj.download(fname, force_=True)
    new_size, new_mtime = utils.sig(local_txt)
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
    info = [a for a in proj.file_info().splitlines() if a]
    assert len(info) == 13

    proj = ppx.MassiveProject(MSVID, fetch=True)
    proj._api = "blah"
    remote_files = proj.remote_files()
    assert len(remote_files) == 12

    # Keep this to test for HTTPErrors
    proj._api = "https://api.github.com/user"  # A dummy URL...
    proj.remote_files()


@pytest.mark.skip("MassIVE API is currently broken for renalyses.")
def test_massive_reanalysis(tmp_path):
    """Test reanalyses."""
    proj = ppx.MassiveProject(RMSVID, fetch=True)
    remote_files = proj.remote_files("2019-06-03_mnchoi_64a990d7/**/*")
    assert len(remote_files) == 10


def test_massive_download(tmp_path):
    """Test downloading data from massive"""
    proj = ppx.MassiveProject(MSVID)
    files = proj.local_files()
    assert files == []

    fname = "ccms_statistics/statistics.tsv"
    txt = proj.download(fname)
    files = proj.local_files()
    local_txt = tmp_path / MSVID / fname
    orig_sig = utils.sig(local_txt)
    assert txt == [local_txt]
    assert files[0] == local_txt

    txt = proj.download(fname)  # should do nothing
    assert orig_sig == utils.sig(local_txt)

    txt = proj.download(fname, force_=True)
    new_size, new_mtime = utils.sig(local_txt)
    assert orig_sig[0] == new_size
    assert orig_sig[1] != new_mtime

    proj.timeout = 10
    assert proj._parser_state is None


def test_massive_ccms_peak(tmp_path):
    """Test a ccms_peak file."""
    # TODO: Find a smaller file.
    proj = ppx.MassiveProject("MSV000080544")
    files = proj.local_files()
    assert files == []

    fname = "ccms_peak/RAW/01709a_GA9-TUM_second_pool_1_01_01-ETD-1h-R2.mzXML"
    proj.download(fname)
    files = proj.local_files()
    assert len(files) > 0
