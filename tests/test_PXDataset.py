import pytest
import os
import re
import logging
from ppx import PXDataset

def test_PXDataset_initialization():
    testID = "PXD000001"
    dat = PXDataset(testID)
    assert dat.return_id == testID
    assert dat.query_id == testID

dat = PXDataset("PXD000001")

def test_simple_methods():
    url = "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001"
    ref = [("Gatto L, Christoforou A. Using R and Bioconductor for proteomics "
            "data analysis. Biochim Biophys Acta. 2014 1844(1 pt a):42-51")]
    assert dat.pxurl() == url
    assert dat.pxref() == ref
    assert dat.pxtax() == ["Erwinia carotovora"]

def test_files():
    files = ["F063721.dat", "F063721.dat-mztab.txt",
             "PRIDE_Exp_Complete_Ac_22134.xml.gz",
             "PRIDE_Exp_mzData_Ac_22134.xml.gz",
             "PXD000001_mztab.txt", "README.txt",
             "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML",
             "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzXML",
             "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML",
             "TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw",
             "erwinia_carotovora.fasta", "generated"]
    assert dat.pxfiles() == files

def test_download(tmpdir, caplog):
    caplog.set_level(logging.INFO)
    dest = os.path.join(tmpdir.strpath, "test")
    download_msg = "Downloading README.txt"
    skip_msg = "exists. Skipping file..."

    # Verify download works
    dat.pxget(files="README.txt", dest_dir=dest)
    file = os.path.join(dest, "README.txt")
    assert os.path.isfile(file) is True
    assert download_msg in caplog.records[0].msg

    # Verify that the file isn't downloaded again if it is already present
    dat.pxget(files="README.txt", dest_dir=dest)
    assert skip_msg in caplog.records[2].msg

    # Verify that the force_ argument actually works
    dat.pxget(files="README.txt", dest_dir=dest, force_=True)
    assert download_msg in caplog.records[4].msg
