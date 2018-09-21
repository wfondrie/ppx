# __init__.py : ppx

"""
See the README for detailed documentation and examples.
"""
name = "ppx"

from .PXDataset import PXDataset

with open(os.path.join("..", "VERSION"), "r") as fh:
    version_num = fh.read().strip()

__version__ = version_num
