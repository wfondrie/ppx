ppx: A Python interface to ProteomeXchange
==========================================

.. image:: https://github.com/wfondrie/ppx/workflows/tests/badge.svg?branch=master
   :target: https://github.com/wfondrie/ppx/actions?query=workflow%3Atests

.. image:: https://readthedocs.org/projects/ppx/badge/?version=latest
    :target: https://ppx.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

ppx provides a simple means to access the `ProteomeXchange
<http://www.proteomexchange.org/>`_ [1]_ repository from Python. Using
ProteomeXchange identifiers, the user can retrieve metadata associated with a
project and download project files from the `PRIDE Archive
<https://www.ebi.ac.uk/pride/archive/>`_ [2]_, `MassIVE
<https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp>`_, and other partner
repositories.

Our intent is that ppx would provide an efficient method to reuse
proteomics data from ProteomeXchange, allowing easier access for those
developing proteomics tools and analyses in Python.

Installation
------------
ppx was developed and tested for Python 3.6+, and only requires
packages that are distributed as part of the Python Standard Library. The
release version of ppx can be installed with :code:`pip` (or 
:code:`pip3`)::

    pip install ppx

License
-------
ppx is distributed under the MIT license.

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   Overview <self>
   basicUsage.rst
   API Reference <PXDataset.rst>

.. examples.rst


For R Users
-----------

ppx was inspired by the rpx R package [3]_ written by Laurent Gatto. If you are
an R user and want many of the same functionalities that ppx offers, check it
out on `Bioconductor
<http://bioconductor.org/packages/release/bioc/html/rpx.html>`_. and `GitHub
<https://github.com/lgatto/rpx>`_.


.. [1] Vizcaino J.A. et al. *ProteomeXchange: globally co-ordinated proteomics
    data submission and dissemination*, Nature Biotechnology 2014, 32, 223 – 226,
    doi:10.1038/nbt.2839.

.. [2] Vizcaíno JA, et al. *2016 update of the PRIDE database and related
    tools*. Nucleic Acids Res. 2016, 44(D1): D447-D456. doi:10.1093/nar/gkv1145.

.. [3] Gatto L. *rpx: R Interface to the ProteomeXchange Repository*. 2018,
    R package version 1.16.0, https://github.com/lgatto/rpx.
