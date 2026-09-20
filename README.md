# VRE seismic amplitude enhancement

A compact, reproducible Python implementation of the variable-range enhancement (VRE) experiment developed during my master's research in seismic data processing.

VRE applies a nonlinear, moving-window amplitude transform separately to positive and negative samples. Its purpose is to emphasize locally coherent reflection amplitudes in a seismic section while retaining polarity. This repository preserves the numerical procedure in the original MATLAB script, removes memory-heavy intermediate arrays, and provides a command-line workflow for repeatable experiments.

![Before and after seismic sections](figures/before_after.jpg)

## Scientific context

Ground roll is coherent, high-amplitude, low-frequency surface-wave energy that can mask reflection events in seismic records. Conventional attenuation methods, including frequency and frequency-wavenumber filters, can suppress ground roll but may also remove useful reflection energy when their spectral or apparent-velocity content overlaps.

The related published research by Aminian and Riahi uses GARCH-derived conditional standard deviation and clustering to identify useful energy within conventionally attenuated noise and return selected signal components to the filtered data. It reports tests on synthetic and experimental seismic data, including stacked and 3-D cases.

The VRE code in this repository is an amplitude-enhancement experiment associated with that broader research context. It does **not** implement the paper's GARCH estimation or K-means workflow. Keeping this distinction clear makes the code and the scientific claims auditable.

Related publication:

> M. A. Aminian and M. A. Riahi, “Enhanced data fidelity after ground roll attenuation using conditional standard deviation clustering obtained from the GARCH model,” *Exploration Geophysics*, 54(3), 271–287, 2023. [https://doi.org/10.1080/08123985.2022.2135430](https://doi.org/10.1080/08123985.2022.2135430)

## Method

For every trace, the input is split into non-negative and negative components. Within each overlapping window, each component is normalized using its local extreme amplitude, raised to a configurable power, and rescaled:

```text
positive: y = max(x) * (x / max(x))^r
negative: y = min(x) * (x / min(x))^r
```

The estimates from all windows containing a sample are averaged, then the positive and negative results are recombined. The original settings are a window parameter of `80` (an inclusive span of 81 samples) and a power of `3`.

The Python implementation produces the same transform without constructing the original `nt × nt × nx` arrays. Memory use therefore scales with the 2-D section instead of the square of the sample count.

## Results

The supplied experimental figures show stronger local amplitudes after VRE while retaining the main reflector geometry. The normalized spectral comparison also shows close agreement over most of the recorded band, with changes concentrated at selected peaks. These plots are qualitative evidence; a final scientific assessment should also report a defined amplitude-fidelity or signal-to-noise metric on a dataset with a trusted reference.

![Original and VRE frequency spectra](figures/frequency_spectra.jpg)

![Normalized spectral comparison](figures/normalized_spectrum.jpg)

## Installation

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
```

## Quick start

Run the self-contained synthetic example:

```bash
python examples/synthetic_example.py
```

Run the original experiment after placing `Section_GARCH.mat` in `data/`:

```bash
vre data/Section_GARCH.mat \
  --variable myfilter \
  --rows 0:700 \
  --columns 149:200 \
  --window 80 \
  --power 3 \
  --sample-interval 0.002 \
  --output results/original
```

The command writes the original and enhanced arrays to `vre_result.npz`, plus before/after and normalized-spectrum figures.

## Repository structure

```text
.
├── src/vre/               Python implementation and command-line interface
├── examples/              Reproducible synthetic example
├── tests/                 Numerical-equivalence and validation tests
├── figures/               Selected results from the master's work
├── data/README.md          Instructions for locally held research data
├── VRE_3_original.m       Original MATLAB research script
├── CITATION.cff            Software and article citation metadata
└── pyproject.toml          Package metadata and dependencies
```

## Numerical fidelity and corrections

The moving-window transform deliberately preserves two details of the MATLAB code: `window = 80` means 81 samples because both endpoints are included, and the number of window starts is `nt - window`.

The plotting code corrects the original frequency-axis construction by deriving bins from the actual sample count and sampling interval. This affects plot coordinates, not the enhanced data. It also labels the horizontal section axis as trace number because the provided script does not include offset coordinates.

## Limitations

- VRE is nonlinear; changing the window or exponent changes amplitudes and must be justified for each dataset.
- The included figures do not by themselves establish general performance or causal recovery of lost signal.
- The research data are excluded because redistribution rights have not been established.
- The GARCH and clustering method described in the article is outside this implementation.

## License

The code is available under the MIT License. Research data and published article content are governed by their respective owners and are not covered by this repository's software license.
