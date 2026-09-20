"""Core variable-range enhancement algorithm.

The implementation follows the numerical operations in the original MATLAB
script while avoiding its large three-dimensional intermediate arrays.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray


def _enhance_polarity(
    data: NDArray[np.float64], window: int, power: float, *, positive: bool
) -> NDArray[np.float64]:
    """Enhance one polarity and average all overlapping moving windows."""
    samples, traces = data.shape
    accumulator = np.zeros_like(data)
    counts = np.zeros_like(data, dtype=np.int64)

    # MATLAB uses 1:nt-window and includes both endpoints of each window,
    # producing nt-window windows containing window+1 samples each.
    for start in range(samples - window):
        stop = start + window + 1
        segment = data[start:stop]
        scale = np.max(segment, axis=0) if positive else np.min(segment, axis=0)
        valid_trace = scale != 0
        if not np.any(valid_trace):
            continue

        transformed = np.full_like(segment, np.nan)
        transformed[:, valid_trace] = scale[valid_trace] * (
            segment[:, valid_trace] / scale[valid_trace]
        ) ** power
        finite = np.isfinite(transformed)
        accumulator[start:stop] += np.where(finite, transformed, 0.0)
        counts[start:stop] += finite

    return np.divide(
        accumulator,
        counts,
        out=np.full_like(accumulator, np.nan),
        where=counts > 0,
    )


def enhance_section(
    data: ArrayLike, window: int = 80, power: float = 3
) -> NDArray[np.float64]:
    """Apply variable-range enhancement to a 2-D seismic section.

    Parameters
    ----------
    data:
        Two-dimensional array with samples along rows and traces along columns.
    window:
        MATLAB-compatible window parameter. Each moving window contains
        ``window + 1`` samples.
    power:
        Exponent controlling enhancement strength. The original experiment
        used ``3``.

    Returns
    -------
    numpy.ndarray
        Enhanced section with the same shape as the input.

    Notes
    -----
    Positive and negative amplitudes are processed independently. Within each
    moving window, amplitudes are normalized by the local positive maximum or
    negative minimum, raised to ``power``, rescaled, and averaged across all
    overlapping windows.
    """
    section = np.asarray(data, dtype=np.float64)
    if section.ndim != 2:
        raise ValueError("data must be a 2-D array of samples by traces")
    if not np.all(np.isfinite(section)):
        raise ValueError("data must contain only finite values")
    if not isinstance(window, (int, np.integer)) or window < 1:
        raise ValueError("window must be a positive integer")
    if window >= section.shape[0]:
        raise ValueError("window must be smaller than the number of samples")
    if power <= 0:
        raise ValueError("power must be positive")

    positive = np.where(section >= 0, section, 0.0)
    negative = np.where(section < 0, section, 0.0)
    return _enhance_polarity(positive, window, power, positive=True) + _enhance_polarity(
        negative, window, power, positive=False
    )
