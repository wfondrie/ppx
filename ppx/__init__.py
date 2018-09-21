# __init__.py : ppx
"""
See the README for detailed documentation and examples.
"""
import os.path

name = "ppx"

root = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(root, "..", "VERSION"), "r") as fh:
    version_num = fh.read().strip()

__version__ = version_num

from .PXDataset import PXDataset
