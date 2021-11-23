"""Test the command line interface"""
import subprocess
from pathlib import Path

import pytest

PXID = "PXD000001"
MSVID = "MSV000087408"


# pytest.mark.skip(reason="PRIDE conneciton instability")
def test_pride(tmp_path):
    """Test the CLI for pride"""
    out_dir = tmp_path / PXID
    cmd = ["ppx", "-l", str(out_dir), "-t", "10", PXID, "*.txt"]
    subprocess.run(cmd, check=True)
    print(list(out_dir.iterdir()))


def test_massive(tmp_path):
    """Test the CLI for massive"""
    out_dir = tmp_path / MSVID
    cmd = ["ppx", "-l", str(out_dir), MSVID, "*/statistics.tsv"]
    subprocess.run(cmd, check=True)
    assert (out_dir / "ccms_statistics" / "statistics.tsv").exists()


def test_version(tmp_path):
    """Test ppx version"""
    subprocess.run(["ppx", "--version"], check=True)
