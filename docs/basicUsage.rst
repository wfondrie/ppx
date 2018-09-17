Basic Usage
===========

The :code:`ppx` package defines a single class, the :code:`PXDataset`. When
provided with a ProteomeXchange identifier---such as "PXD000001"---the
constructor retrieves the metadata for the dataset from ProteomeXchange. The
methods for the :code:`PXDataset` class are used to access specific
information about the dataset or download files associated with it.

To begin, first import the package::

    >>> from ppx import PXDataset

Then we can create a :code:`PXDataset` object for a ProteomeXchange dataset::

    >>> dat = PXDataset("PXD000001")
    >>> print(dat.id)
    PXD000001

We can then use the :code:`PXDataset` methods to access information about the
dataset. Bibliographic information can be accessed with the :code:`pxref()`
method:

    >>> dat.pxref()
    ['Gatto L, Christoforou A. Using R and Bioconductor for proteomics data
    analysis. Biochim Biophys Acta. 2014 1844(1 pt a):42-51']

The species used to generate the dataset can be accessed with the
:code:`pxtax()` method:

    >>> dat.pxtax()
    ['Erwinia carotovora']

The FTP URL where the data files can be downloaded can be accessed with the
:code:`pxurl()` method. Note that not all datasets have this available::

    # The FTP link is available
    >>> dat.pxurl()
    'ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001'

    # The FTP link is not available. This also results in a warning.
    >>> print(PXDataset("PXD010937").pxurl())
    None

If there is an FTP URL for the dataset, a list of the available files can be
retrieved with the :code:`pxfiles()` method:

    >>> dat.pxfiles()
    ['F063721.dat', 'F063721.dat-mztab.txt',
    'PRIDE_Exp_Complete_Ac_22134.xml.gz', 'PRIDE_Exp_mzData_Ac_22134.xml.gz',
    'PXD000001_mztab.txt', 'README.txt',
    'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML',
    'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzXML',
    'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML',
    'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw',
    'erwinia_carotovora.fasta', 'generated']

Finally, we can use the :code:`pxget()` method to download all or some of the
files available at the FTP URL:

    >>> dat.pxget(files = "README.txt", destDir = "test")
    Downloading README.txt...
    Done!

For more information about the :code:`PXDataset` class or any of its methods,
see the :ref:`API Reference <PXDataset-API>`.
