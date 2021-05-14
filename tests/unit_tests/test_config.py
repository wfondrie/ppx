"""Test the configuration"""
import os
from pathlib import Path

import pytest
import ppx

PXID = "PXD000001"


def test_reset_dir(monkeypatch):
    """Test resetting the data directory"""
    monkeypatch.delenv("PPX_DATA_DIR")
    ppx.set_data_dir()
    assert ppx.get_data_dir() == Path(Path.home(), ".ppx")

    ppx.PrideProject(PXID)
    assert Path(Path.home(), ".ppx").exists()


def test_change_dir(monkeypatch, tmp_path):
    """Test changing the data dir"""
    test_dir = tmp_path / "test"
    with pytest.raises(FileNotFoundError):
        ppx.set_data_dir(test_dir)

    test_dir.mkdir()
    ppx.set_data_dir(test_dir)
    assert ppx.get_data_dir() == test_dir

    proj = ppx.PrideProject(PXID)
    assert proj.local == test_dir / PXID

    test_dir = tmp_path / "test2"
    monkeypatch.setenv("PPX_DATA_DIR", str(test_dir))
    with pytest.raises(FileNotFoundError):
        ppx.set_data_dir()

    test_dir.mkdir()
    ppx.set_data_dir(test_dir)
    assert ppx.get_data_dir() == test_dir

    proj = ppx.PrideProject(PXID)
    assert proj.local == test_dir / PXID
