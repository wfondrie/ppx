"""Test PRIDE functionality w/o internet access"""
import json
from pathlib import Path

import pytest
import ppx

PXID = "PXD000001"


def test_init(tmp_path):
    """Test initialization"""
    proj = ppx.PrideProject(PXID)
    url = "ftp://ftp.pride.ebi.ac.uk/pride-archive/2012/03/PXD000001"
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

    proj = ppx.PrideProject(PXID, timeout=5)
    assert proj.timeout == 5

    proj.timeout = 10
    assert proj.timeout == 10


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

    title = (
        "TMT spikes -  Using R and Bioconductor for proteomics data analysis"
    )
    assert proj.title == title

    desc = (
        "Expected reporter ion ratios: Erwinia peptides:    1:1:1:1:1:1 "
        "Enolase spike (sp|P00924|ENO1_YEAST):  10:5:2.5:1:2.5:10 BSA spike "
        "(sp|P02769|ALBU_BOVIN):  1:2.5:5:10:5:1 PhosB spike "
        "(sp|P00489|PYGM_RABIT):  2:2:2:2:1:1 Cytochrome C spike "
        "(sp|P62894|CYC_BOVIN): 1:1:1:1:1:2"
    )
    assert proj.description == desc
    assert proj.sample_processing_protocol == "Not available"

    data_prot = (
        "Two extra files have been added post-publication:<br>"
        '<a href="ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/'
        "PXD000001/TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-"
        '20141210.mzML" target="_top">TMT_Erwinia_1uLSike_Top10HCD_isol2_'
        '45stepped_60min_01-20141210.mzML</a><br><a href="ftp://ftp.pride.'
        "ebi.ac.uk/pride/data/archive/2012/03/PXD000001/TMT_Erwinia_1uLSike_"
        'Top10HCD_isol2_45stepped_60min_01-20141210.mzXML" target="_top">'
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzXML"
        "</a>"
    )
    assert proj.data_processing_protocol == data_prot
    assert proj.doi == "10.6019/PXD000001"


def test_remote_files(mock_pride_project_response):
    """Test that listing remote files works"""
    proj = ppx.PrideProject(PXID)
    files = proj.remote_files()
    true_files = [
        "F063721.dat",
        "F063721.dat-mztab.txt",
        "PRIDE_Exp_Complete_Ac_22134.xml.gz",
        "PRIDE_Exp_mzData_Ac_22134.xml.gz",
        "PXD000001_mztab.txt",
        "README.txt",
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML",
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzXML",
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML",
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw",
        "erwinia_carotovora.fasta",
        "generated/PRIDE_Exp_Complete_Ac_22134.pride.mgf.gz",
        "generated/PRIDE_Exp_Complete_Ac_22134.pride.mztab.gz",
    ]

    assert files == true_files

    gzipped = proj.remote_files("*.gz")
    print(gzipped)
    true_gzipped = [
        "PRIDE_Exp_Complete_Ac_22134.xml.gz",
        "PRIDE_Exp_mzData_Ac_22134.xml.gz",
        "generated/PRIDE_Exp_Complete_Ac_22134.pride.mgf.gz",
        "generated/PRIDE_Exp_Complete_Ac_22134.pride.mztab.gz",
    ]
    assert gzipped == true_gzipped

    ms_files = proj.remote_files("*60min_01*")
    true_ms_files = [
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML",
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzXML",
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML",
        "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw",
    ]
    assert ms_files == true_ms_files
    assert proj.remote_files("blah") == []


def test_remote_files(mock_pride_project_response):
    """Test that listing remote directories works"""
    proj = ppx.PrideProject(PXID)
    dirs = proj.remote_dirs()
    assert dirs == ["generated"]


def test_cached_remote_files(tmp_path, mock_pride_project_response):
    """Test that caching remote files works"""
    cached = tmp_path / ".remote_files"

    test_files = ["test1", "test2"]
    with cached.open("w+") as ref:
        ref.write("\n".join(test_files))

    proj = ppx.PrideProject(PXID, local=tmp_path)
    files = proj.remote_files()
    assert files == test_files

    proj.fetch = True
    files = proj.remote_files()
    assert files != test_files


def test_cached_remote_dirs(tmp_path, mock_pride_project_response):
    """Test that caching remote directories works"""
    cached = tmp_path / ".remote_dirs"

    test_dirs = ["test1", "test2"]
    with cached.open("w+") as ref:
        ref.write("\n".join(test_dirs))

    proj = ppx.PrideProject(PXID, local=tmp_path)
    files = proj.remote_dirs()
    assert files == test_dirs

    proj.fetch = True
    files = proj.remote_dirs()
    assert files != test_dirs


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
