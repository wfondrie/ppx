"""See the README for detailed documentation and examples."""

try:
    from importlib.metadata import PackageNotFoundError, version

    try:
        __version__ = version(__name__)
    except PackageNotFoundError:
        pass

except ImportError:
    from pkg_resources import DistributionNotFound, get_distribution

    try:
        __version__ = get_distribution(__name__).version
    except DistributionNotFound:
        pass

from . import massive, pride
from .config import get_data_dir, set_data_dir
from .factory import find_project
from .massive import MassiveProject
from .pride import PrideProject
