"""Test finding projects"""
import pytest
import ppx

from requests.exceptions import ConnectTimeout, ReadTimeout

PXID = "PXD000001"
MSVID = "MSV000087408"
MSVPXD = "PXD025981"


def test_pride_offline(block_internet, tmp_path):
    """Test pride project offline functionality"""
    with pytest.raises(Exception):
        ppx.find_project(PXID)

    proj = ppx.find_project(PXID, repo="PrIdE")
    assert isinstance(proj, ppx.PrideProject)
    assert proj.local == tmp_path / PXID
    assert not proj.fetch

    proj = ppx.find_project(PXID, local=(tmp_path / "test"), repo="pride")
    assert proj.local == tmp_path / "test"

    proj = ppx.find_project(PXID, fetch=True, repo="pride")
    assert proj.fetch


def test_massive_offline(block_internet, tmp_path):
    """Test massive project offline functionality"""
    ppx.find_project(MSVID)  # Doesn't need internet to resolve
    proj = ppx.find_project(MSVID, repo="mAsSiVe")
    assert isinstance(proj, ppx.MassiveProject)
    assert proj.local == tmp_path / MSVID
    assert not proj.fetch

    proj = ppx.find_project(MSVID, local=(tmp_path / "test"), repo="massive")
    assert proj.local == tmp_path / "test"

    proj = ppx.find_project(MSVID, fetch=True, repo="massive")
    assert proj.fetch


# The following require internet access! --------------------------------------
def test_pride_online():
    """Test pride project resolution"""
    proj = ppx.find_project(PXID, timeout=10)
    assert isinstance(proj, ppx.PrideProject)


def test_massive_project():
    """Test massive project resolution"""
    proj = ppx.find_project(MSVID, timeout=10)
    assert isinstance(proj, ppx.MassiveProject)


def test_massive_project_with_pxd():
    proj = ppx.find_project(MSVPXD, timeout=10)
    assert isinstance(proj, ppx.MassiveProject)
    assert proj.id == MSVID


def test_timeout():
    """Try a value that is too small."""
    with pytest.raises((ConnectTimeout, ReadTimeout)):
        proj = ppx.find_project(PXID, timeout=0.0000000000001)
