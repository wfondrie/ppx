<img src="static/ppx_light.svg" width=300>

# A Python interface to proteomics data repositories

[![conda](https://img.shields.io/conda/vn/bioconda/ppx?color=green)](http://bioconda.github.io/recipes/ppx/README.html)
[![PyPI](https://img.shields.io/pypi/v/ppx?color=green)](https://pypi.org/project/ppx/)
[![tests](https://github.com/wfondrie/ppx/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/wfondrie/ppx/actions/workflows/tests.yml)
[![Documentation Status](https://readthedocs.org/projects/ppx/badge/?version=latest)](https://ppx.readthedocs.io/en/latest/?badge=latest)

https://github.com/wfondrie/ppx/workflows/tests/badge.svg?branch=master

## Overview
ppx provides a simple, programmatic means to access proteomics data that are
publicly available in [ProteomeXchange](http://www.proteomexchange.org) partner
repositories. ppx allows users to easily find and download files associated
with projects in [PRIDE](https://www.ebi.ac.uk/pride/archive/) and
[MassIVE](https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp). In doing so,
ppx promotes the reproducible analysis of proteomics data.

For full documentation and examples, visit: https://ppx.readthedocs.io

## Installation
ppx requires Python 3.6+ and depends upon the
[requests](https://docs.python-requests.org/en/master/) and
[tqdm](https://tqdm.github.io/) Python packages. ppx and any missing
dependencies are easily installed with `pip` or with `conda` through the
[bioconda](https://bioconda.github.io/index.html) channel.

Install with `conda`:

``` shell
conda install -c bioconda ppx
```

Or install with `pip`:

```shell
pip3 install ppx
```

## Configuration

By default, ppx will download project files in the `.ppx` directory under the
current user's home directory (`~/.ppx` on Linux and MacOS). There are several
ways to specify different data directories:

1. Change the ppx data directory for all future Python sessions by setting the
`PPX_DATA_DIR` environment variable to your preferred directory.

2. Change the ppx data directory for a Python session using the
`ppx.set_data_dir()` function.

3. Specify a data directory for a project using the `local` argument:

``` Python
>>> import ppx

>>> proj = ppx.find_project("PXD000001", local="my/data/dir")
```

Why does ppx set a default data directory? We found that this makes it easier
to reuse the same proteomics data files in multiple tasks that we're working
on.

As of ppx v1.3.0, cloud paths can also be used as the data directory. This
allows you to stream downloaded files to AWS S3, Google Cloud Storage, or Azure
Blob Storage. To use a cloud storage provider, simply set the data directory to
a cloud URI, such as :code:`s3://my-data-bucket/ppx` using any of the methods
above. Please note that you'll also need to setup credentials for your cloud
provider---see the `CloudPathLib documentation
<https://cloudpathlib.drivendata.org/v0.6/authentication/>_` for details.

## Examples
First, find a project using its ProteomeXchange or MassIVE identifier:

``` Python
>>> import ppx

>>> proj = ppx.find_project("PXD000001")
```

We can then view the files associated with the project in the repository
(PRIDE in this case):

``` Python
>>> proj.remote_files()
#['F063721.dat',
# 'F063721.dat-mztab.txt',
# 'PRIDE_Exp_Complete_Ac_22134.xml.gz',
# 'PRIDE_Exp_mzData_Ac_22134.xml.gz',
# 'PXD000001_mztab.txt',
# 'README.txt',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzXML',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw',
# 'erwinia_carotovora.fasta',
# 'generated/PRIDE_Exp_Complete_Ac_22134.pride.mgf.gz',
# 'generated/PRIDE_Exp_Complete_Ac_22134.pride.mztab.gz']
```

We can also [glob](https://en.wikipedia.org/wiki/Glob_(programming)) for
specific types of files:

``` Python
>>> proj.remote_files("*.mzML")
# ['TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML']
```

Then we can download one or more files to the projects local data directory:

``` Python
>>> proj.download("README.txt")
# [PosixPath('/Users/wfondrie/.ppx/PXD000001/README.txt')]
```

Once we've downloaded files, ppx no longer needs an internet connection to
retrieve a project's local data. However, you will need to specify the
repository in which the project data resides. If we start a new Python
session, we can find our previous file easily:

``` Python
>>> import ppx

>>> proj = ppx.find_project("PXD000001", repo="PRIDE")
>>> proj.local_files()
# [PosixPath('/Users/wfondrie/.ppx/PXD000001/README.txt')]
```

### Downloading to cloud storage backend

We use [CloudPathlib](https://cloudpathlib.drivendata.org/stable/) to power
support for AWS S3, Google Cloud Storage, and Azure Blob Storage. To use a
cloud storage provider, create the bucket for ppx to use and set it as the ppx data
directory.


For example using AWS S3, we can save the files of a project to an S3 bucket:
``` python
>>> proj = ppx.find_project("PXD000001", local="s3://my-bucket/PXD000001")
>>> proj.download("README.txt")
# [S3Path('s3://my-bucket/PXD000001/README.txt')]
```

CloudPathLib then provides methods to download files from S3 when you need them:

``` Python
>>> readme_on_s3 = proj.local_files("README.txt")[0]
>>> readme_on_s3.download_to("README.txt")
# [PosixPath(README.txt)]
```

## If you are an R user...

ppx was inspired the rpx R package by Laurent Gatto. Check it out on
[Bioconductor](http://bioconductor.org/packages/release/bioc/html/rpx.html) and
[GitHub](https://github.com/lgatto/rpx).
