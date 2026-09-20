# VRE — Virtual Resolution Enhancement for Seismic Data

A compact, reproducible Python implementation of **Virtual Resolution Enhancement (VRE)** for seismic data, developed from MATLAB experiments conducted during my master's research in seismic data processing.

VRE is a nonlinear, moving-window seismic enhancement technique introduced by **Rashed and Atef (2020)**. It operates separately on the positive and negative components of each seismic trace, sharpening major reflections while preserving their polarity and peak positions.

This repository preserves the numerical procedure used in my original MATLAB implementation, removes memory-heavy intermediate arrays, and provides a clean Python package and command-line workflow for reproducible experiments.

## Scientific context

**Virtual Resolution Enhancement (VRE)** was introduced by Mohamed A. Rashed and Ali H. Atef as a post-stack enhancement technique for seismic sections.

The method is intended primarily to improve the visualization and interpretability of existing seismic reflections. By applying a nonlinear amplitude transformation within a moving window, VRE sharpens reflection wavelets, reduces their apparent smearing and irregularities, and can increase the apparent temporal resolution and lateral coherence of major reflections.

The underlying idea is simple. After amplitudes within a local window are normalized by their local peak, values between zero and one become progressively smaller when raised to a power greater than one, whereas the normalized peak remains equal to one. After restoring the original amplitude scale, the peak is retained while surrounding lower-amplitude samples are suppressed. The resulting reflection therefore becomes narrower and sharper.

Because seismic traces contain both positive and negative amplitudes, VRE processes the positive and negative components separately before recombining them.

Rashed and Atef tested VRE on several land and marine post-stack seismic sections. Their examples showed sharper and more clearly defined reflections and an increase in the high-frequency portion of the amplitude spectrum following VRE processing.

VRE should nevertheless be interpreted as an **enhancement procedure rather than a method for recovering missing subsurface information**. The original paper explicitly notes that VRE does not reveal hidden features or generate new reflections; instead, it enhances reflections already present in the seismic data.

### Original VRE publication

> Mohamed A. Rashed and Ali H. Atef,  
> **“Virtual resolution enhancement: A new enhancement tool for seismic data.”**  
> *Open Geosciences*, 12(1), 363–375, 2020.  
> DOI: 10.1515/geo-2020-0169

The implementation in this repository is my Python reconstruction and optimization of the VRE experiment used during my master's work. It is **not the original software of Rashed and Atef**.

## Method

Consider a seismic trace \(x\). VRE first separates it into positive and negative components:

```text
x+ = max(x, 0)
x- = min(x, 0)
```

A sliding window is then moved along each trace.

For every window, the positive samples are normalized by the maximum positive amplitude in that window, while the negative samples are normalized by the minimum negative amplitude.

For a power parameter `r > 1`, the transformation is:

```text
positive: y = max(x) * (x / max(x))^r
negative: y = min(x) * (x / min(x))^r
```

The local peak therefore remains unchanged because

```text
1^r = 1
```

while normalized amplitudes smaller than one decrease:

```text
0 < a < 1  →  a^r < a    for r > 1
```

Increasing `r` consequently suppresses samples surrounding a local peak more strongly and produces a sharper wavelet.

Because successive sliding windows overlap, a given sample can receive several VRE estimates. Following the original procedure, estimates from all windows containing that sample are averaged. The processed positive and negative components are then recombined to obtain the enhanced trace.

The procedure is repeated independently for every trace in the seismic section.

## Implementation

The original MATLAB experiment stores the results of individual sliding-window operations in large intermediate arrays before averaging them.

This Python implementation performs the same moving-window transformation without constructing the original `nt × nt × nx` intermediate arrays.

As a result, memory requirements scale primarily with the 2-D seismic section rather than with the square of the number of time samples.

The original experimental settings preserved in this repository are:

```text
window parameter = 80
power            = 3
```

In the original MATLAB indexing, `window = 80` corresponds to an **inclusive span of 81 samples**.

These values reproduce the configuration of the supplied research script; they should not be interpreted as universally optimal VRE parameters.

## Expected effect

VRE primarily changes the **shape of reflection wavelets**.

Samples close to local extrema are retained more strongly than lower-amplitude samples surrounding them. Consequently, reflections generally become narrower and visually sharper.

This nonlinear sharpening also modifies the frequency content of the section. Rashed and Atef reported amplification of the higher-frequency portions of the amplitude spectra in their examples and interpreted the associated spectral broadening as an indication of increased temporal resolution.

The effect should not be interpreted as recovery of frequencies or geological information that were absent from the original data. VRE enhances existing seismic events rather than creating new subsurface information.

## Results

The supplied experimental figures from my master's work show the seismic section before and after application of the VRE procedure.

The processed section exhibits sharper local reflection amplitudes while retaining the principal reflector geometry. The corresponding normalized spectral comparison illustrates the spectral changes introduced by the nonlinear sharpening operation.

These figures should be interpreted as demonstrations of the algorithm on the available experimental data rather than as proof of general performance.

A more rigorous quantitative evaluation would require a dataset with a known reference together with defined metrics for quantities such as temporal resolution, amplitude fidelity, event continuity, and signal-to-noise ratio.

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

The command writes the original and enhanced arrays to:

```text
vre_result.npz
```

and generates before/after seismic-section figures together with a normalized spectral comparison.

## Repository structure

```text
.
├── src/vre/               Python implementation and command-line interface
├── examples/              Reproducible synthetic example
├── tests/                 Numerical-equivalence and validation tests
├── figures/               Selected results from the master's work
├── data/README.md          Instructions for locally held research data
├── VRE_3_original.m       Original MATLAB research script
├── CITATION.cff           Software and article citation metadata
└── pyproject.toml          Package metadata and dependencies
```

## Numerical fidelity and corrections

The Python implementation deliberately preserves important details of the original MATLAB experiment.

In particular:

- `window = 80` corresponds to 81 samples because both MATLAB window endpoints are included.
- The number and positioning of sliding windows follow the indexing behavior of the original script.
- Positive and negative amplitudes are processed independently.
- Overlapping window estimates are averaged before the two polarity components are recombined.
- The original power parameter is preserved.

The plotting implementation corrects the frequency-axis construction used in the research script by deriving frequency bins directly from the actual number of samples and the specified sampling interval.

This correction affects only the coordinates used for spectral visualization; it does **not** alter the VRE-enhanced seismic data.

The horizontal section axis is labelled as **trace number** because physical offset coordinates are not provided by the original script.

## Relationship to the published method

This repository implements the core VRE procedure described by Rashed and Atef (2020):

1. separate positive and negative seismic amplitudes;
2. apply a sliding window along each trace;
3. normalize samples using the local positive maximum or negative minimum;
4. raise the normalized amplitudes to a user-defined power;
5. restore the local amplitude scale;
6. average estimates from overlapping windows;
7. recombine the positive and negative components.

The repository should therefore be considered an **independent Python implementation and optimization of the published VRE concept**, based on the MATLAB implementation used in my master's research.

It is not an official implementation supplied by the authors of the original VRE paper.

## Limitations

- VRE is a nonlinear seismic enhancement operation. The output depends on the selected window length, sliding behavior, and exponent.
- Increasing the exponent produces stronger wavelet sharpening and therefore stronger modification of the original waveform.
- Spectral broadening after VRE is partly a consequence of sharpening seismic wavelets and should not automatically be interpreted as recovery of independently measured high-frequency geological information.
- VRE does not reveal reflections or geological structures that are absent from the original seismic data.
- Interpretation of enhanced sections should therefore always consider the corresponding original data.
- The figures included here demonstrate the behavior of the method but do not establish its general performance on arbitrary seismic datasets.
- The original research dataset is excluded because redistribution rights have not been established.

## Citation

If you use the VRE methodology, please cite the publication that introduced the method:

> Rashed, M. A., & Atef, A. H. (2020).  
> **Virtual resolution enhancement: A new enhancement tool for seismic data.**  
> *Open Geosciences, 12*(1), 363–375.  
> DOI: 10.1515/geo-2020-0169

If you use the software implementation from this repository, please also cite the repository using the metadata provided in `CITATION.cff`.

## License

The software in this repository is available under the MIT License.

The VRE methodology originates from the work of Rashed and Atef (2020). Research datasets, published figures, articles, and other third-party materials remain subject to their respective copyright and licensing terms and are not covered by this repository's software license.
