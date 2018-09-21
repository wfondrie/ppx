# __init__.py : ppx
"""
See the README for detailed documentation and examples.
"""
name = "ppx"

with open("VERSION", "r") as fh:
    version_num = fh.read().strip()

__version__ = version_num

from .PXDataset import PXDataset
