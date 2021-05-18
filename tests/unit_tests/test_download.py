"""Test the download functionality of ppx

These tests are in a separate file because they all require internet access.
"""
import pytest
import ppx

PXID = "PXD000001"
MSVID = "MSV000087408"


# @pytest.mark.skip(reason="Seem to have problems with PRIDE connections :/")
def test_pride_download(tmp_path):
    """Test downloading data from PRIDE"""
    proj = ppx.PrideProject(PXID)
    files = proj.local_files()
    assert files == []

    fname = "F063721.dat-mztab.txt"
    txt = proj.download(fname)
    files = proj.local_files()
    local_txt = tmp_path / PXID / fname
    assert txt == [local_txt]
    assert files[0] == local_txt


def test_massive_download(tmp_path):
    """Test downloading data from massive"""
    proj = ppx.MassiveProject(MSVID)
    files = proj.local_files()
    assert files == []

    fname = "ccms_statistics/statistics.tsv"
    txt = proj.download(fname)
    files = proj.local_files()
    local_txt = tmp_path / MSVID / fname
    assert txt == [local_txt]
    assert files[0] == local_txt
