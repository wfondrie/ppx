Basic Usage
===========

The ppx package centers around a single class, the :code:`PXDataset`. When
provided with a ProteomeXchange identifier---such as "PXD000001"---the
constructor retrieves the metadata for the dataset from ProteomeXchange. The
attributes, properties, and methods a :code:`PXDataset` instance allows us to
access specific information about the dataset or download the files associated
with it.

To begin, we first import the package:

    >>> import ppx

Then we create a :code:`PXDataset` object for a ProteomeXchange dataset:

    >>> dat = ppx.PXDataset("PXD000001")
    >>> dat.return_id
    'PXD000001'

We can then use the :code:`PXDataset` attributes, properties, and methods to
access information about the dataset. Bibliographic information is accessed with
the :code:`references` property:

    >>> dat.references
    ['Gatto L, Christoforou A. Using R and Bioconductor for proteomics data analysis. Biochim Biophys Acta. 2013 May 18. doi:pii: S1570-9639(13)00186-6. 10.1016/j.bbapap.2013.04.032']

The species used to generate the dataset is accessed with the :code:`taxonomies`
property:

    >>> dat.taxonomies
    ['Erwinia carotovora']

The URL for the FTP server where the data files can be downloaded is accessed
with the :code:`url` property. Note that not all datasets have this available:

    >>> dat.url
    'ftp://ftp.pride.ebi.ac.uk/pride/data/archive/2012/03/PXD000001'

If there a :code:`PXDataset` does have an FTP URL, we can retrieve a list of the
available files in the root directory with the :code:`list_files()` method:

    >>> dat.list_files()
    ['F063721.dat', 'F063721.dat-mztab.txt', 'PRIDE_Exp_Complete_Ac_22134.xml.gz', 'PRIDE_Exp_mzData_Ac_22134.xml.gz', 'PXD000001_mztab.txt', 'README.txt', 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzML', 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01-20141210.mzXML', 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.mzXML', 'TMT_Erwinia_1uLSike_Top10HCD_isol2_45stepped_60min_01.raw', 'erwinia_carotovora.fasta']

In some repositories, such as MassIVE, the FTP server has the project files
organized into directories. We can list the available directories using the
:code:`list_dirs()` method:

   >>> msv = ppx.PXDataset("PXD018973")
   >>> msv.list_dirs()
   ['ccms_parameters', 'ccms_quant', 'quant_stats', 'raw', 'search']

We can then list the files in one of these subdirectories:

    >>> msv.list_files(path="raw")
    ['HELA-DIA-DDA-A2.raw']


Finally, we can use the :code:`download()` method to download all or some of the
files available on the FTP server.

    >>> dat.download(files="README.txt", dest_dir="test")
    ['test/README.txt']

.. note::
   If we want updates on download progress, we can change the level for
   reporting using the :code:`logging` package:

       >>> import logging
       >>> logging.getLogger().setLevel(logging.INFO)


For more information about the :code:`PXDataset` class or any of its methods,
see the :ref:`API Reference <PXDataset-API>`.
