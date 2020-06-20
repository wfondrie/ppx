# __init__.py : ppx
"""
See the README for detailed documentation and examples.
"""
import pkg_resources
from .PXDataset import PXDataset

try:
    __version__ = pkg_resources.get_distribution("ppx").version
except pkg_resources.DistributionNotFound:
    __version__ = "unknown"
