"""Input helpers for seismic arrays."""

from __future__ import annotations

from pathlib import Path

import numpy as np
from numpy.typing import NDArray
from scipy.io import loadmat


def load_mat_section(
    path: str | Path,
    variable: str = "myfilter",
    rows: slice | None = None,
    columns: slice | None = None,
) -> NDArray[np.float64]:
    """Load a 2-D array from a MATLAB file and optionally select a region."""
    source = Path(path)
    if not source.is_file():
        raise FileNotFoundError(f"input file not found: {source}")
    contents = loadmat(source)
    if variable not in contents:
        available = sorted(key for key in contents if not key.startswith("__"))
        raise KeyError(f"variable {variable!r} not found; available: {available}")
    data = np.asarray(contents[variable], dtype=np.float64)
    if data.ndim != 2:
        raise ValueError(f"{variable!r} must be 2-D, got shape {data.shape}")
    return data[rows or slice(None), columns or slice(None)]
