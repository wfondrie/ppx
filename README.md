<img src="static/ppx_light.svg" width=300>

# A Python interface to proteomics data repositories

[![tests](https://github.com/wfondrie/ppx/workflows/tests/badge.svg?branch=master)](https://github.com/wfondrie/ppx/actions?query=workflow%3Atests)[![Documentation Status](https://readthedocs.org/projects/ppx/badge/?version=latest)](https://ppx.readthedocs.io/en/latest/?badge=latest)  

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
dependencies are easily installed with `pip`:

```
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


## Examples
First, find a project using its ProteomeXchange or MassIVE identifier:

``` Python
>>> import ppx

>>> proj = ppx.find_project("PXD000001")
```

We can then view the files associated with the project in the repository
(PRIDE in this case):

``` Python
>>> remote_files = proj.remote_files()
>>> print(remote_files)
# ['F063721.dat', 'F063721.dat-mztab.txt',
# 'PRIDE_Exp_Complete_Ac_22134.xml.gz', 'PRIDE_Exp_mzData_Ac_22134.xml.gz',
# 'PXD000001_mztab.txt', 'README.txt',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzXML',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw',
# 'erwinia_carotovora.fasta']
```

We can also [glob](https://en.wikipedia.org/wiki/Glob_(programming)) for
specific types of files:

``` Python
>>> mzml_files = proj.remote_files("*.mzML")
>>> print(mzml_files)
# ['TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML']
```

Then we can download one or more files to the projects local data directory:

``` Python
>>> downloaded = proj.download("README.txt")
>>> print(downloaded)
# [PosixPath('/Users/wfondrie/.ppx/PXD000001/README.txt')]
```

Once we've downloaded files, ppx no longer needs an internet connection to
retrieve a project's local data. However, you will need to specify the 
repository in which the project data resides. If we start a new Python
session, we can find our previous file easily:

``` Python
>>> import ppx

>>> proj = ppx.find_project("PXD000001", repo="PRIDE")
>>> local_files = proj.local_files()
>>> print(local_files)
# [PosixPath('/Users/wfondrie/.ppx/PXD000001/README.txt')]
```

## If you are an R user...

ppx was inpsired the rpx R package by Laurent Gatto. Check it out on
[Bioconductor](http://bioconductor.org/packages/release/bioc/html/rpx.html) and
[GitHub](https://github.com/lgatto/rpx).
