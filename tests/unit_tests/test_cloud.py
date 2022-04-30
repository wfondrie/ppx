"""Test using cloud locations"""
from cloudpathlib import CloudPath
import ppx

from . import utils

MSVID = "MSV000087408"


def test_local_arg(cloud_bucket):
    """Test downloading data from massive to a cloudpath"""
    proj = ppx.MassiveProject(MSVID)

    # Google Cloud
    bucket = "s3://ppx-test-bucket/ppx"
    proj = ppx.MassiveProject(MSVID, local=bucket)
    assert isinstance(proj.local, CloudPath)
    files = proj.local_files()
    assert files == []

    fname = "ccms_statistics/statistics.tsv"
    txt = proj.download(fname)
    orig_sig = utils.sig(txt[0])
    files = proj.local_files()
    local_txt = CloudPath(bucket) / fname
    assert txt == [local_txt]
    assert files[0] == local_txt

    txt = proj.download(fname)  # should do nothing
    assert orig_sig == utils.sig(local_txt)

    txt = proj.download(fname, force_=True)
    new_size, new_mtime = utils.sig(local_txt)
    assert orig_sig[0] == new_size
    assert orig_sig[1] != new_mtime


def test_data_dir(cloud_bucket):
    """Test that setting the ppx data directory works."""
    bucket = "s3://ppx-test-bucket/ppx"
    ppx.set_data_dir(bucket)

    proj = ppx.MassiveProject(MSVID)
    assert isinstance(proj.local, CloudPath)
    files = proj.local_files()
    assert files == []

    fname = "ccms_statistics/statistics.tsv"
    txt = proj.download(fname)
    files = proj.local_files()
    local_txt = CloudPath(bucket) / MSVID / fname
    assert txt == [local_txt]
    assert files[0] == local_txt
