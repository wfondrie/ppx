.. ppx documentation master file, created by
   sphinx-quickstart on Tue Sep  4 15:33:48 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

The ppx Package
===============
A Python interface to the ProteomeXchange Repository
----------------------------------------------------

.. image:: https://travis-ci.org/wfondrie/ppx.svg?branch=master
   :target: https://travis-ci.org/wfondrie/ppx

.. image:: https://readthedocs.org/projects/ppx/badge/?version=latest
    :target: https://ppx.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status



The :code:`ppx` package provides a simple means to access the ProteomeXchange
[1]_ repository from Python. Using ProteomeXchange identifiers, the user can
retrieve metadata associated with a project and download project files from
the PRIDE Archive [2]_ .

:code:`ppx` is a heavily based on the :code:`rpx` R package by Laurent Gatto
[3]_. My intent is that :code:`ppx` would provide an efficient method to reuse
proteomics data from ProteomeXchange, allowing easier access for those
developing proteomics tools and analyses in Python.

Installation
------------
:code:`ppx` was developed and tested for Python 3.5+, and only requires
packages that are dirstributed as part of the Python Standard Library. The
release version of :code:`ppx` can be installed with :code:`pip` (or
:code:`pip3`)::

    pip install ppx

Alternatively, the development version of :code:`ppx` can be installed from
GitHub::

    pip install git+git://github.com/wfondrie/ppx.git

License
-------
:code:`ppx` is distributed under the MIT license.

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   self
   basicUsage.rst
   examples.rst

.. toctree::
   :maxdepth: 1
   :caption: API Reference

   PXDataset.rst

.. [1] Vizcaino J.A. et al. *ProteomeXchange: globally co-ordinated proteomics
    data submission and dissemination*, Nature Biotechnology 2014, 32, 223 – 226,
    doi:10.1038/nbt.2839.

.. [2] Vizcaíno JA, et al. *2016 update of the PRIDE database and related
    tools*. Nucleic Acids Res. 2016, 44(D1): D447-D456. doi:10.1093/nar/gkv1145.

.. [3] Gatto L. *rpx: R Interface to the ProteomeXchange Repository*. 2018,
    R package version 1.16.0, https://github.com/lgatto/rpx.
