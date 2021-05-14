Python API
==========

Using ppx typically starts with calling the :py:func:`ppx.find_project()`
function. This function returns either a :py:class:`~ppx.PrideProject` or
:py:class:`~ppx.MassiveProject` object, depending on the repository in
where the project resides (PRIDE or MassIVE, respectively). These project
objects have methods to find and download files of interest.

.. toctree::
   :maxdepth: 1
   :hidden:
   :titlesonly:

   Overview <self>
   functions.rst
   pride.rst
   massive.rst

.. currentmodule:: ppx
.. autosummary::
   :nosignatures:

   find_project
   get_data_dir
   set_data_dir
   pride.list_projects
   massive.list_projects
   PrideProject
   MassiveProject
