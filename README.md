[![Build Status](https://travis-ci.org/wfondrie/ppx.svg?branch=master)](https://travis-ci.org/wfondrie/ppx) [![Documentation Status](https://readthedocs.org/projects/ppx/badge/?version=latest)](https://ppx.readthedocs.io/en/latest/?badge=latest)  


# ppx: A Python interface to the ProteomeXchange Repository  

## Overview  
The `ppx` package provides a simple means to access the [ProteomeXchange](http://www.proteomexchange.org/) repository from Python. Using ProteomeXchange identifiers, the user can retrieve metadata associated with a project and download project files from [PRIDE](https://www.ebi.ac.uk/pride/archive/).

`ppx` is largely based on the `rpx` R package by Laurent Gatto ([Bioconductor](http://bioconductor.org/packages/release/bioc/html/rpx.html) and [GitHub](https://github.com/lgatto/rpx)).

For full documentation and examples, visit: https://ppx.readthedocs.io

## Installation  
`ppx` is `pip` installable. The `ppx` package is available for Python 3.6+ and only depends on packages in the Python Standard Library.

```
pip3 install ppx
```

## Examples  
First create a PXDataset object using a valid ProteomeXchange identifier:
```Python
dat = PXDataset("PXD000001")
```

We can then extract various data about the ProteomeXchange project from the PXDataset:
```Python
dat.pxref()
# ['Gatto L, Christoforou A. Using R and Bioconductor for proteomics data
# analysis. Biochim Biophys Acta. 2014 1844(1 pt a):42-51']

dat.pxurl()
# 'ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001'

dat.pxtax()
# ['Erwinia carotovora']

dat.pxfiles()
# ['F063721.dat', 'F063721.dat-mztab.txt',
# 'PRIDE_Exp_Complete_Ac_22134.xml.gz', 'PRIDE_Exp_mzData_Ac_22134.xml.gz',
# 'PXD000001_mztab.txt', 'README.txt',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzXML',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML',
# 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw',
# 'erwinia_carotovora.fasta', 'generated']
```

Lastly, we can download files that we're interested in:
```Python
# Download "README.txt" to the "test" directory
dat.pxget(files="README.txt", dest_dir="test")
```
