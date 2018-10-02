ppx + bioservices
=================

The :code:`bioservices` Python package provides access to a number of
bioinformatics services. In their own words:

    "BioServices is a Python package that provides access to many
    Bioinformatics Web Services (e.g., UniProt) and a framework to easily
    implement Web Service wrappers (based on WSDL/SOAP or REST protocols).

    The primary goal of BioServices is to use Python as a glue language to
    provide a programmatic access to Biological Web Services. By doing so,
    elaboration of new applications that combine several Web Services should
    be fostered."

The :code:`bioservices` provides access to the PRoteomics IDEntifications
(PRIDE) Archive [1]_ API, which incidentally makes :code:`ppx` +
:code:`BioServices` a powerful combination.

A Simple Example
----------------
To illustrate the power of :code:`ppx` + :code:`bioservices`, we'll find all of
the PRIDE datasets related to honey bees with runs from Q-Exactive
instruments, retrieve a list of files associated with each dataset, and set-up
to download a the mass spectrometry data files.

.. note::
    To proceed with this example, the :code:`bioservices` Python package will
    need to be installed. See the :code:`bioservices` package website for
    details on its installation and usage.
    `Link <https://bioservices.readthedocs.io/en/master/>`_

First, we need to import the :code:`ppx` and :code:`bioservices` packages.
The :code:`PRIDE` module in the :code:`bioservices` package will allow us to
find datasets that match out query::

    from ppx import PXDataset
    from bioservices import PRIDE
    import re

    # Find datasets about honey bees (Apis mellifera) that used a Q-Exactive.
    pride = PRIDE()
    datasets = pride.get_project_list(speciesFilter = "Apis mellifera",
                                      instrumentFilter = "q exactive")

Let's see how many datasets we found:

    >>> len(datasets)
    6

Note that there are a number of additional filters for
:code:`get_project_list()` and that it returns several fields about the
dataset. For example, look at the first element of :code:`datasets`:

    >>> print(datasets[0])
    {'accession': 'PXD007824', 'title': 'Apis mellifera,Hemolymph,LC-MSMS',
    'projectDescription': 'We characterized and compared hemolymph proteome of
    Royal Jelly ', 'publicationDate': '2017-11-30', 'submissionType':
    'PARTIAL', 'numAssays': 0, 'species': ['Apis mellifera (Honeybee)'],
    'tissues': ['blood'], 'ptmNames': ['iodoacetamide derivatized residue',
    'monohydroxylated residue'], 'instrumentNames': ['Q Exactive'],
    'projectTags': ['Biological']}

Now we can extract use the :code:`'accession'` keys to create a list
:code:`PXDataset` objects::

    pxdat = []
    for dataset in datasets:
        acc = dataset['accession']
        pxdat.append(PXDataset(acc))

With the `PXDataset` objects made, we can easily list the files to see which
ones we might want to download. In this case, we'll print first 5 from each:

    >>> for dat in pxdat: print(dat.pxfiles()[0:4])
    ['ITB2d2.mzxml', 'ITB2d2.pep.xml', 'ITB2d2.raw', 'ITB2d3.mzxml']
    ['ITB-7DB-1.mgf', 'ITB-7DB-1.raw', 'ITB-7DB-2.mgf', 'ITB-7DB-2.raw']
    ['MS160421-XBH-1.raw', 'MS160421-XBH-10.raw', 'MS160421-XBH-11.raw', 'MS160421-XBH-12.raw']
    ['(F002977).mzid.gz', '(F002977).mzid_(F002977).MGF', '(F002978).mzid.gz', '(F002978).mzid_(F002978).MGF']
    ['Antenna-VSH.mzid', 'Antenna-nonVSH.mzid', 'Antennae-VSH.mgf', 'Antennae-nonVSH.mgf']
    ['Bruker_bee_fly.tar.gz', 'ExpressedORFs.fasta', 'F123695_fly3ET.csv', 'F123696_fly2ET.csv']

We could have alternatively used :code:`bioservices.PRIDE.get_file_list()` to
retrieve a file list. Finally, let's pretend that we want to download all of
the Thermo raw files for each dataset. In this case, we could do::

    rawTest = re.compile(".*\.raw$", re.IGNORECASE)

    for dat in pxdat:
        rawFiles = list(filter(rawTest.search, dat.pxfiles()))
        dirName = dat.id + "_data"
        #dat.pxget(files = rawFiles, dest_dir = dirName)
        print(rawFiles)

.. caution::
    You probably don't actually want to do this since it would download a lot
    of large files. I've commented out the download command so that it instead
    only prints the file names, however you can uncomment and run it if you so
    desire.

Alternatively, we could just download all of the README files (This download
is much smaller)::

    readmeTest = re.compile("^README")

    for dat in pxdat:
        readmeFiles = list(filter(readmeTest.search, dat.pxfiles()))
        dirName = dat.id + "_data"
        dat.pxget(files = readmeFiles, dest_dir = dirName)


.. [1] Vizcaíno JA, et al. *2016 update of the PRIDE database and related
    tools*. Nucleic Acids Res. 2016, 44(D1): D447-D456. doi:10.1093/nar/gkv1145.
