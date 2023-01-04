"""
# jeiss-convert package
"""
from .hdf5 import dat_to_hdf5, hdf5_to_bytes
from .version import version as __version__  # noqa: F401
from .version import version_tuple as __version_info__  # noqa: F401

__all__ = ["dat_to_hdf5", "hdf5_to_bytes"]
