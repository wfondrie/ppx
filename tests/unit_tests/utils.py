"""Utility functions"""


def sig(fname):
    """Get the size and edit time of file."""
    stats = fname.stat()
    return stats.st_size, stats.st_mtime
