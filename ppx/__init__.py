# __init__.py : ppx
"""
See the README for detailed documentation and examples.
"""
import os.path

name = "ppx"

with open(os.path.join(__file__, "..", "VERSION"), "r") as fh:
    version_num = fh.read().strip()

__version__ = version_num

from .PXDataset import PXDataset
