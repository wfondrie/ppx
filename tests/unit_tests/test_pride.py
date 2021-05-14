"""Test PRIDE functionality w/o internet access"""
import json
from pathlib import Path

import pytest
import ppx

PXID = "PXD000001"


def test_init(tmp_path):
    """Test initialization"""
    proj = ppx.PrideProject(PXID)
    url = "https://www.ebi.ac.uk/pride/ws/archive/v2/projects/PXD000001"
    assert proj.id == PXID
    assert proj.url == url
    assert proj.local == tmp_path / "PXD000001"
    assert not proj.fetch

    with pytest.raises(ValueError):
        ppx.PrideProject("PXD;MaLiCiOuScOdE!")

    with pytest.raises(ValueError):
        ppx.PrideProject("MSV000001")

    with pytest.raises(ValueError):
        ppx.PrideProject("PXD1")

    proj = ppx.PrideProject(PXID, local=tmp_path / "test")
    assert proj.local == tmp_path / "test"

    proj = ppx.PrideProject(PXID, fetch=True)
    assert proj.fetch


def test_env(monkeypatch, tmp_path):
    """Test that the environment variable works"""
    data_dir = tmp_path / "envpath"
    data_dir.mkdir()
    monkeypatch.setenv("PPX_DATA_DIR", str(data_dir))
    ppx.set_data_dir()

    proj = ppx.PrideProject(PXID)
    out_path = Path(data_dir, PXID)
    assert proj.local == out_path


def test_metadata(mock_pride_project_response):
    """Test that getting the metadata works"""
    proj = ppx.PrideProject(PXID)
    assert not (proj.local / ".pride-metadata").exists()

    meta = proj.metadata
    assert (proj.local / ".pride-metadata").exists()

    with Path("tests/data/pride_project_response.json").open() as ref:
        true_meta = json.load(ref)

    assert meta == true_meta


def test_remote_files(mock_pride_files_response):
    """Test that listing remote files works"""
    proj = ppx.PrideProject(PXID)
    files = proj.remote_files()
    true_files = [
        "erwinia_carotovora.fasta",
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw",
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML",
        "PRIDE_Exp_Complete_Ac_22134.xml.gz",
        "PRIDE_Exp_Complete_Ac_22134.pride.mztab.gz",
        "PRIDE_Exp_Complete_Ac_22134.pride.mgf.gz",
        "F063721.dat-mztab.txt",
        "F063721.dat",
    ]
    assert files == true_files

    gzipped = proj.remote_files("*.gz")
    true_gzipped = [
        "PRIDE_Exp_Complete_Ac_22134.xml.gz",
        "PRIDE_Exp_Complete_Ac_22134.pride.mztab.gz",
        "PRIDE_Exp_Complete_Ac_22134.pride.mgf.gz",
    ]
    assert gzipped == true_gzipped

    ms_files = proj.remote_files("*60min_01*")
    true_ms_files = [
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw",
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML",
    ]
    assert ms_files == true_ms_files
    assert proj.remote_files("blah") == []


def test_local_files(local_files, tmp_path):
    """Test that finding local files works"""
    proj = ppx.PrideProject(PXID, local=tmp_path)
    res = proj.local_files(), proj.local_dirs()
    assert res == local_files

    res = proj.local_files("**/*.mzML")
    assert res == [f for f in local_files[0] if str(f).endswith("mzML")]

    res = proj.local_files("*.mzML")
    assert res == [tmp_path / "test_file.mzML"]

    res = proj.local_dirs("*0")
    assert res == [tmp_path / "test_dir0"]
