# __init__.py : ppx
import os.path

"""
See the README for detailed documentation and examples.
"""
name = "ppx"

with open(os.path.join("..", "VERSION"), "r") as fh:
    version_num = fh.read().strip()

__version__ = version_num

from .PXDataset import PXDataset
