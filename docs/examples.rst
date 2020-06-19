.. I've removed this for now, because it appears the PRIDE module in bioservices
   is broken :(

ppx + BioServices
=================

The `BioServices <https://bioservices.readthedocs.io>`_ Python package provides
access to a number of bioinformatics services. In their own words:

    "BioServices is a Python package that provides access to many
    Bioinformatics Web Services (e.g., UniProt) and a framework to easily
    implement Web Service wrappers (based on WSDL/SOAP or REST protocols).

    The primary goal of BioServices is to use Python as a glue language to
    provide a programmatic access to Biological Web Services. By doing so,
    elaboration of new applications that combine several Web Services should
    be fostered."

BioServices provides access to the PRoteomics IDEntifications (PRIDE) Archive
[1]_ API, which incidentally makes ppx + BioServices a powerful combination.

A Simple Example
----------------

To illustrate the power of ppx + BioServices, we'll find all of the PRIDE
datasets related to honey bees (*Apis mellifera*) with runs from Q-Exactive
instruments, retrieve a list of files associated with each dataset, and setup to
download all of the mass spectrometry data files.

.. note::
    To proceed with this example, the BioServices Python package will
    need to be installed. See the BioServices package website for
    details on its installation and usage.
    `Link <https://bioservices.readthedocs.io/en/master/>`_

First, we need to import the ppx and BioServices packages. The
:code:`PRIDE` module in the BioServices package will allow us to find
datasets that match out query:

.. 
    >>> import re
    >>> import ppx
    >>> from bioservices import PRIDE

Next, we retrieve a list of ProteomeXchange identifiers for:

.. 
    >>> # Find datasets about honey bees (Apis mellifera) that used a Q-Exactive.
    >>> pride = PRIDE()
    >>> datasets = pride.get_project_list(speciesFilter="Apis mellifera",
    ...                                   instrumentFilter="q exactive")

Let's see how many datasets we found:

..
    >>> len(datasets)
    6

Note that there are a number of additional filters for
:code:`get_project_list()` and that it returns several fields about the
dataset. For example, look at the first element of :code:`datasets`:

.. 
    >>> print(datasets[0])
    {'accession': 'PXD007824', 'title': 'Apis mellifera,Hemolymph,LC-MSMS', 'projectDescription': 'We characterized and compared hemolymph proteome of Royal Jelly ', 'publicationDate': '2017-11-30', 'submissionType': 'PARTIAL', 'numAssays': 0, 'species': ['Apis mellifera (Honeybee)'], 'tissues': ['blood'], 'ptmNames': ['iodoacetamide derivatized residue', 'monohydroxylated residue'], 'instrumentNames': ['Q Exactive'], 'projectTags': ['Biological']}

Now we can extract use the :code:`"accession"` keys to create a list
:code:`PXDataset` objects:

..
    >>> pxdat = [ppx.PXDataset(d["accession"]) for d in datasets]

With the `PXDataset` objects created, we can easily list the files to see which
ones we might want to download. In this case, we'll print first 5 from each:

..
    >>> [print(d.list_files()[:4]) for d in pxdat]
    ['ITB2d2.mzxml', 'ITB2d2.pep.xml', 'ITB2d2.raw', 'ITB2d3.mzxml']
    ['ITB-7DB-1.mgf', 'ITB-7DB-1.raw', 'ITB-7DB-2.mgf', 'ITB-7DB-2.raw']
    ['MS160421-XBH-1.raw', 'MS160421-XBH-10.raw', 'MS160421-XBH-11.raw', 'MS160421-XBH-12.raw']
    ['(F002977).mzid.gz', '(F002977).mzid_(F002977).MGF', '(F002978).mzid.gz', '(F002978).mzid_(F002978).MGF']
    ['Antenna-VSH.mzid', 'Antenna-nonVSH.mzid', 'Antennae-VSH.mgf', 'Antennae-nonVSH.mgf']
    ['Bruker_bee_fly.tar.gz', 'ExpressedORFs.fasta', 'F123695_fly3ET.csv', 'F123696_fly2ET.csv']

Note that we also could have used :code:`bioservices.PRIDE.get_file_list()` to
retrieve a file list. Either way, we'll download all of the Thermo \*.raw files for
each dataset. In this case, we could do:

..
    >>> for dat in pxdat:
    ...     raw_files = [f for f in dat.list_files() if f.endswith(".raw")
    ...     dir_name = dat.id + "_data"
    ...     #dat.download(files=raw_files, dest_dir=dir_name)
    ...     print(raw_files)

.. caution::
    You probably don't actually want to do this since it would download a lot
    of large files. I've commented out the download command so that it instead
    only prints the file names, however you can uncomment and run it if you so
    desire.

Alternatively, we could just download all of the README files (This download
is much smaller):

.. 
    >>> for dat in pxdat:
    ...     readme_files = [f for f in dat.list_files() if f.endswith(".raw")]
    ...     dir_name = dat.id + "_data"
    ...     downloaded = dat.download(files=readme_files, dest_dir=dir_name)
    ...     print(downloaded)


.. [1] Vizcaíno JA, et al. *2016 update of the PRIDE database and related
    tools*. Nucleic Acids Res. 2016, 44(D1): D447-D456. doi:10.1093/nar/gkv1145.
