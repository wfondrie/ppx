"""
Tests for the ppx package.

There are issues connecting to the PRIDE FTP site from the Travis-CI
Local testing should run still run these tests.
servers, so some tests are marked for skipping.

"""
import os
import logging
import pytest
from ppx import PXDataset


def test_initialization():
    """Tests that a PXDataset can be constructed"""
    test_id = "PXD000001"
    test_dat = PXDataset(test_id)
    assert test_dat.return_id == test_id
    assert test_dat.query_id == test_id


PRD = PXDataset("PXD000001")
MSV = PXDataset("PXD018973")


def test_properties():
    """Checks the basic PXDataset properties"""
    url = "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001"
    ref = ["Gatto L, Christoforou A. Using R and Bioconductor for proteomics "
           "data analysis. Biochim Biophys Acta. 2013 May 18. doi:pii: "
           "S1570-9639(13)00186-6. 10.1016/j.bbapap.2013.04.032"]

    assert PRD.url == url
    assert PRD.references == ref
    assert PRD.taxonomies == ["Erwinia carotovora"]


#@pytest.mark.skip(reason="Travis-CI can't consistently access PRIDE FTP site.")
def test_files():
    """Test that file names are retrieved successfully."""
    files = ["F063721.dat", "F063721.dat-mztab.txt",
             "PRIDE_Exp_Complete_Ac_22134.xml.gz",
             "PRIDE_Exp_mzData_Ac_22134.xml.gz",
             "PXD000001_mztab.txt", "README.txt",
             ("TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_"
              "60min_01-20141210.mzML"),
             ("TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_"
              "60min_01-20141210.mzXML"),
             "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML",
             "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw",
             "erwinia_carotovora.fasta"]

    retrieved_files = PRD.list_files()
    assert retrieved_files == files

    # test a subdirectory too
    dir_file = ['HELA-DIA-DDA-A2.raw']
    assert MSV.list_files(path="raw") == dir_file


def test_directories():
    """Test that listing directories works"""
    dirs = ['ccms_parameters', 'ccms_quant', 'quant_stats', 'raw', 'search']
    assert MSV.list_dirs() == dirs


#@pytest.mark.skip(reason="Travis-CI can't consistently access PRIDE FTP site.")
def test_download(tmpdir, caplog):
    """Tests downloading a PXDataset file from PRIDE"""
    caplog.set_level(logging.INFO)
    dest = os.path.join(tmpdir.strpath, "test")
    download_msg = "Downloading %s..."

    # Verify download works
    PRD.download(files="README.txt", dest_dir=dest)
    file = os.path.join(dest, "README.txt")
    assert os.path.isfile(file) is True
    assert download_msg in caplog.records[0].msg

    # Verify that the force_ argument actually works
    PRD.download(files="README.txt", dest_dir=dest, force_=True)
    assert download_msg in caplog.records[1].msg


#@pytest.mark.skip(reason="Travis-CI can't consistently access PRIDE FTP site.")
def test_file_whitespace():
    """
    Some files contain whitepace, causing pxfiles() in v0.2.0 and
    earlier to break. This test verifies that was fixed.
    """
    ws_dat = PXDataset("PXD002828")
    ws_files = ws_dat.list_files()
    assert ws_files[-2] == "Species MB9.raw"
