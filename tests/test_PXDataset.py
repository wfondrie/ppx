import pytest
import os
import re
from ppx import PXDataset

def test_PXDataset_initialization():
    testID = "PXD000001"
    dat = PXDataset(testID)
    assert dat.return_id == testID
    assert dat.query_id == testID

dat = PXDataset("PXD000001")

def test_simple_methods():
    url = "ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001"
    assert dat.pxurl() == url

    ref = [("Gatto L, Christoforou A. Using R and Bioconductor for proteomics "
            "data analysis. Biochim Biophys Acta. 2014 1844(1 pt a):42-51")]
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

def test_download(tmpdir, capsys):
    dest = os.path.join(tmpdir.strpath, "test")

    # Verify download works
    dat.pxget(files="README.txt", dest_dir=dest)
    file = os.path.join(dest, "README.txt")
    assert os.path.isfile(file) is True
    #assert capsys.readouterr().out == "Downloading README.txt...\nDone!\n"

    # Verify that the file isn't downloaded again if it is already present
    dat.pxget(files="README.txt", dest_dir=dest)
    expected = file + " exists. Skipping file...\nDone!\n"
    #assert capsys.readouterr().out == expected

    # Verify that the force_ argument actually works
    dat.pxget(files="README.txt", dest_dir=dest, force_=True)
    #assert capsys.readouterr().out == "Downloading README.txt...\nDone!\n"
