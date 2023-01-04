import typing as tp
from pathlib import Path

import h5py

from .utils import group_to_bytes, split_channels


def dat_to_hdf5(
    dat_path: Path,
    container_path: Path,
    group_name: tp.Optional[str] = None,
    ds_kwargs: tp.Optional[dict[str, tp.Any]] = None,
):
    """Convert a dat file to an HDF5 file.

    Parameters
    ----------
    dat_path : Path
        Path to .dat file.
    container_path : Path
        Path to HDF5 file (may exist)
    group_name : tp.Optional[str], optional
        Name of group inside HDF5 (must not exist).
        By default None (use the root group).
    ds_kwargs : tp.Optional[dict[str, tp.Any]], optional
        Keyword arguments passed to h5py.Group.create_dataset.
        By default None (no extra arguments).
    """
    meta, channel_names, data = split_channels(dat_path)

    if ds_kwargs is None:
        ds_kwargs = dict()

    if not group_name:
        group_name = "/"

    with h5py.File(container_path, "a") as h5:
        if group_name == "/":
            g = h5
        else:
            g = h5.create_group(group_name)

        g.attrs.update(meta)

        for idx, ds in enumerate(channel_names):
            g.create_dataset(ds, data=data[idx], **ds_kwargs)


def hdf5_to_bytes(hdf5_path, hdf5_group=None) -> bytes:
    """Convert an HDF5 group into the contents of a .dat file.

    This should only be used to check that the contents of a .dat
    file can be round-tripped; NOT to create new .dat files.

    Parameters
    ----------
    hdf5_path : Path
        Path to existing HDF5 container.
    hdf5_group : str, optional
        Name of internal HDF5 group, by default None (root)

    Returns
    -------
    bytes
        Contents of a .dat file with the same data as the HDF5 file.
    """
    if not hdf5_group:
        hdf5_group = "/"

    with h5py.File(hdf5_path) as h5:
        g = h5[hdf5_group]
        b = group_to_bytes(g)
    return b
