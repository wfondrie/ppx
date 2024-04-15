#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import subprocess
import sys

sys.path.insert(0, os.path.abspath(".."))

try:
    import numpydoc
except ModuleNotFoundError:
    subprocess.run(["pip", "install", "numpydoc"], check=True)

# -- Project information -----------------------------------------------------

project = "ppx"
copyright = "2020, William E Fondrie"
author = "William E Fondrie"

import ppx

# The short X.Y version
version = str(ppx.__version__)
# The full version, including alpha/beta/rc tags
release = version


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = "1.0"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named "sphinx.ext.*") or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
    "numpydoc",
    "sphinxarg.ext",
    "recommonmark",
]

autosummary_generate = True
autodoc_default_options = {
    "members": True,
    "inherited-members": True,
    "member-order": "bysource",
}

numpydoc_show_class_members = True
numpydoc_show_inherited_class_members = True
numpydoc_attributes_as_param_list = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = [".rst", ".md"]
source_suffix = [".rst", ".md"]

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_theme_options = {
    "style_nav_header_background": "#343131",
    "logo_only": True,
}
html_css_files = ["custom.css"]
html_logo = "_static/ppx_dark.png"

# Output file base name for HTML help builder.
htmlhelp_basename = "ppxdoc"
