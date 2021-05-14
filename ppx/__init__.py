"""See the README for detailed documentation and examples."""
try:
    from importlib.metadata import version, PackageNotFoundError

    try:
        __version__ = version(__name__)
    except PackageNotFoundError:
        pass

except ImportError:
    from pkg_resources import get_distribution, DistributionNotFound

    try:
        __version__ = get_distribution(__name__).version
    except DistributionNotFound:
        pass

from . import pride
from . import massive
from .factory import find_project
from .pride import PrideProject
from .massive import MassiveProject
from .config import get_data_dir, set_data_dir
