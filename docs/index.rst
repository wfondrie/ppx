.. image:: https://img.shields.io/conda/vn/bioconda/ppx?color=green
   :target: http://bioconda.github.io/recipes/ppx/README.html
   :alt: bioconda

.. image:: https://img.shields.io/pypi/v/ppx?color=green
   :target: https://pypi.org/project/ppx/
   :alt: PyPI

.. image:: https://github.com/wfondrie/ppx/workflows/tests/badge.svg?branch=master
   :target: https://github.com/wfondrie/ppx/actions?query=workflow%3Atests

.. image:: https://readthedocs.org/projects/ppx/badge/?version=latest
    :target: https://ppx.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

A Python interface to proteomics data repositories
==================================================

ppx provides simple, programmatic access means to access proteomics data that
are publicly available in `ProteomeXchange <http://www.proteomexchange.org/>`_
[1]_ partner repositories. ppx allows users to easily find and download files
associated with projects in `PRIDE <https://www.ebi.ac.uk/pride/archive/>`_
[2]_ and `MassIVE <https://massive.ucsd.edu/ProteoSAFe/static/massive.jsp>`_
[3]_.

Our intent is that ppx would provide an efficient method to reuse
proteomics data that has been deposited in public repositories, thereby
promoting reproducible research practices and enabling tool developers.

Installation
------------

ppx requires Python 3.6+ and depends upon the `requests
<https://docs.python-requests.org/en/master/>`_ and `tqdm
<https://tqdm.github.io/>`_ Python packages. ppx and any missing dependencies
can be installed with :code:`pip`: or :code:`conda`.

Install with :code:`conda`::

    conda install -c bioconda ppx

Or install with :code:`pip`::

    pip install ppx


License
-------
ppx is distributed under the MIT license.

.. toctree::
   :hidden:
   :maxdepth: 1

   Overview <self>
   Basic Usage <usage.rst>
   Python API <api/index.rst>
   Command Line Interface <cli.rst>
   Contributing <CONTRIBUTING.md>
   Code of Conduct <CODE_OF_CONDUCT.md>
   Changelog <CHANGELOG.md>


For R Users
-----------

ppx was inspired by the rpx R package [4]_ written by Laurent Gatto. If you are
an R user and want many of the same functionalities that ppx offers, check it
out on `Bioconductor
<http://bioconductor.org/packages/release/bioc/html/rpx.html>` and `GitHub
<https://github.com/lgatto/rpx>`_.


.. [1] Vizcaino J.A. et al. *ProteomeXchange: globally co-ordinated proteomics
    data submission and dissemination*, Nature Biotechnology 2014, 32, 223 – 226,
    doi:10.1038/nbt.2839.

.. [2] Vizcaíno JA, et al. *2016 update of the PRIDE database and related
    tools*. Nucleic Acids Res. 2016, 44(D1): D447-D456. doi:10.1093/nar/gkv1145.

.. [3] Wang M, et al. Assembling the Community-Scale Discoverable Human
       Proteome. Cell Syst. 2018 Oct 24;7(4):412-421.e5. doi:
       10.1016/j.cels.2018.08.004.

.. [4] Gatto L. *rpx: R Interface to the ProteomeXchange Repository*. 2018,
    R package version 1.16.0, https://github.com/lgatto/rpx.
