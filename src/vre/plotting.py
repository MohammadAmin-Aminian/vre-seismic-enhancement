"""Small plotting helpers used by the command-line interface."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import ArrayLike


def save_comparison(
    original: ArrayLike,
    enhanced: ArrayLike,
    output: str | Path,
    sample_interval: float = 0.002,
) -> None:
    """Save section and normalized-spectrum comparisons."""
    original = np.asarray(original)
    enhanced = np.asarray(enhanced)
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)

    limit = np.nanpercentile(np.abs(original), 99)
    extent = [1, original.shape[1], original.shape[0] * sample_interval * 1000, 0]
    fig, axes = plt.subplots(1, 2, figsize=(11, 6), constrained_layout=True)
    for axis, values, title in zip(axes, [original, enhanced], ["Before", "After"]):
        image = axis.imshow(
            values,
            cmap="gray",
            aspect="auto",
            extent=extent,
            vmin=-limit,
            vmax=limit,
        )
        axis.set(title=title, xlabel="Trace number", ylabel="Two-way time (ms)")
        fig.colorbar(image, ax=axis, shrink=0.8)
    fig.savefig(output / "before_after.png", dpi=180)
    plt.close(fig)

    frequencies = np.fft.rfftfreq(original.shape[0], d=sample_interval)
    # MATLAB's nanmean can leave isolated NaNs when one polarity is absent in
    # every overlapping window. Treat those missing contributions as zero for
    # display so a single sample cannot invalidate an entire trace spectrum.
    original_for_fft = np.nan_to_num(original)
    enhanced_for_fft = np.nan_to_num(enhanced)
    original_spectrum = np.max(np.abs(np.fft.rfft(original_for_fft, axis=0)), axis=1)
    enhanced_spectrum = np.max(np.abs(np.fft.rfft(enhanced_for_fft, axis=0)), axis=1)
    original_spectrum /= original_spectrum.max()
    enhanced_spectrum /= enhanced_spectrum.max()
    fig, axis = plt.subplots(figsize=(8, 4.5), constrained_layout=True)
    axis.plot(frequencies, original_spectrum, color="black", label="Data")
    axis.plot(frequencies, enhanced_spectrum, color="red", label="VRE")
    axis.set(xlabel="Frequency (Hz)", ylabel="Normalized amplitude", xlim=(0, frequencies[-1]))
    axis.legend()
    fig.savefig(output / "normalized_spectrum.png", dpi=180)
    plt.close(fig)
