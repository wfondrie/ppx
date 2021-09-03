"""Test MassIVE functionality w/o internet access"""
import shutil
from pathlib import Path

import pytest
import ppx

MSVID = "MSV000087408"


def test_init(tmp_path):
    """Test initialization"""
    proj = ppx.MassiveProject(MSVID)
    url = "ftp://massive.ucsd.edu/MSV000087408"
    assert proj.id == MSVID
    assert proj.url == url
    assert proj.local == tmp_path / "MSV000087408"
    assert not proj.fetch

    with pytest.raises(ValueError):
        ppx.MassiveProject("MSV;MaLiCiOuScOdE!")

    with pytest.raises(ValueError):
        ppx.MassiveProject("PXD0000087408")

    with pytest.raises(ValueError):
        ppx.MassiveProject("MSV1")

    proj = ppx.MassiveProject(MSVID, local=(tmp_path / "test"))
    assert proj.local == tmp_path / "test"

    proj = ppx.MassiveProject(MSVID, fetch=True)
    assert proj.fetch

    proj = ppx.MassiveProject(MSVID, timeout=2)
    assert proj.timeout == 2

    proj.timeout = 10
    assert proj.timeout == 10


def test_env(monkeypatch, tmp_path):
    """Test that the environment variable is respected"""
    data_dir = tmp_path / "envpath"
    data_dir.mkdir()
    monkeypatch.setenv("PPX_DATA_DIR", str(data_dir))
    ppx.set_data_dir()

    proj = ppx.MassiveProject(MSVID)
    out_path = Path(data_dir, MSVID)
    assert proj.local == out_path


def test_metadata(tmp_path):
    """Test that parsing the metadata works"""
    metadata_path = tmp_path / MSVID / "ccms_parameters"
    metadata_path.mkdir(parents=True)

    metadata_file = metadata_path / "params.xml"
    shutil.copyfile("tests/data/params.xml", metadata_file)
    proj = ppx.MassiveProject(MSVID)
    meta = proj.metadata
    assert isinstance(meta, dict)
    assert proj.title == "RajKumar-PolZeta-P19-078_MayoClinic"

    desc = (
        "Silver stained bands were submitted for mass spec analysis.  "
        "Investigators are interested in the protein polzeta.  "
    )
    assert proj.description == desc
