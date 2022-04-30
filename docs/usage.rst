Using ppx
=========

Configuration
-------------

By default, ppx will download project files in the :code:`.ppx` directory under
the current user's home directory (:code:`~/.ppx` on Linux and MacOS). There
are several ways to specify different data directories:

1. Change the ppx data directory for all future Python sessions by setting the
   :code:`PPX_DATA_DIR` environment variable to your preferred directory.

2. Change the ppx data directory for a Python session using the
   :py:func:`ppx.set_data_dir()` function.

3. Specify a data directory for a project using the :code:`local` argument:

    >>> import ppx
    >>> proj = ppx.find_project("PXD000001", local="my/data/dir")

Why does ppx set a default data directory? We found that this makes it easier
to reuse the same proteomics data files in multiple tasks that we're working
on.

As of ppx v1.3.0, cloud paths can also be used as the data directory. This
allows you to stream downloaded files to AWS S3, Google Cloud Storage, or Azure
Blob Storage. To use a cloud storage provider, simply set the data directory to
a cloud URI, such as :code:`s3://my-data-bucket/ppx` using any of the methods
above. Please note that you'll also need to setup credentials for your cloud
provider---see the `CloudPathLib documentation
<https://cloudpathlib.drivendata.org/v0.6/authentication/>`_ for details.

Examples
--------

To begin, we first import the ppx package:

    >>> import ppx

We can now find a project using its ProteomeXchange or MassIVE identifier. Note
that ppx currently only supports projects hosted on PRIDE and MassIVE. For this
example, we'll use a project from PRIDE:

    >>> proj = ppx.find_project("PXD000001")

Here, :code:`proj` is a is :py:class:`~ppx.PrideProject` object with
methods that let us explore the available files and download files that we
select. Let's retrieve a list of all of the files associated with this project
on PRIDE:

    >>> remote_files = proj.remote_files()
    >>> print(remote_files)
    ['F063721.dat', 'F063721.dat-mztab.txt', 'PRIDE_Exp_Complete_Ac_22134.xml.gz', 'PRIDE_Exp_mzData_Ac_22134.xml.gz', 'PXD000001_mztab.txt', 'README.txt', 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML', 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzXML', 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML', 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw', 'erwinia_carotovora.fasta', 'generated/PRIDE_Exp_Complete_Ac_22134.pride.mgf.gz', 'generated/PRIDE_Exp_Complete_Ac_22134.pride.mztab.gz']


Alternatively, we can `glob
<https://en.wikipedia.org/wiki/Glob_(programming)>`_ for specific files of
interest:

    >>> mzml_files = proj.remote_files("*.mzML")
    >>> print(mzml_files)
    ['TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML']

Once we've determined what file we desire to download, we can download
them to our local data directory. In this case, that is `~/.ppx/PXD000001`:

    >>> downloaded = proj.download("F063721.dat-mztab.txt")
    >>> print(downloaded)
    [PosixPath('/Users/wfondrie/.ppx/PXD000001/F063721.dat-mztab.txt')]


Once we've downloaded files, ppx no longer needs an internet connection to
retrieve a project's local data. However, you will need to specify the
repository in which the project data resides. If we start a new Python
session, we can find our previous files easily:

    >>> import ppx
    >>> proj = ppx.find_project("PXD000001", repo="PRIDE")
    >>> local_files = proj.local_files()
    >>> print(local_files)
    [PosixPath('/Users/wfondrie/.ppx/PXD000001/F063721.dat-mztab.txt')]

For more details about the available methods for a project, see our Python API
documentation for the :py:class:`~ppx.PrideProject` and
:py:class:`~ppx.MassiveProject` classes.

Using Cloud Storage
+++++++++++++++++++

We use `CloudPathlib <https://cloudpathlib.drivendata.org/stable/>`_ to power
support for AWS S3, Google Cloud Storage, and Azure Blob Storage. To use a
cloud storage provider, create the bucket for ppx to use and set it as the ppx
data directory.

For example using AWS S3, we can save the files of a project to an S3 bucket:

    >>> proj = ppx.find_project("PXD000001", local="s3://my-bucket/PXD000001")
    >>> proj.download("README.txt")
    [S3Path('s3://my-bucket/PXD000001/README.txt')]

CloudPathLib then provides methods to download files from S3 when you need them:

    >>> readme_on_s3 = proj.local_files("README.txt")[0]
    >>> readme_on_s3.download_to("README.txt")
    PosixPath(README.txt)
