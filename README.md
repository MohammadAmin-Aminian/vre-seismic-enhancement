# VRE seismic amplitude enhancement

A compact, reproducible Python implementation of **Virtual Resolution Enhancement (VRE)** for seismic data, based on the method proposed by Rashed and Atef (2020) and implemented during my master's research in seismic data processing.

VRE is a nonlinear, moving-window amplitude transformation designed to sharpen seismic reflection events and improve their apparent temporal resolution while preserving polarity.

This repository preserves the numerical behavior of my original MATLAB implementation, removes memory-heavy intermediate arrays, and provides a cleaner Python implementation with a simple command-line workflow.

## Scientific context

Seismic resolution is limited by the bandwidth and shape of the recorded seismic wavelet. Closely spaced reflections may therefore appear broad or poorly separated, making interpretation more difficult.

**Virtual Resolution Enhancement (VRE)** was introduced by Rashed and Atef (2020) as a post-stack seismic enhancement technique. The method sharpens existing seismic events by modifying amplitudes locally within a moving window.

The basic principle is that amplitudes are normalized relative to a local extreme and then raised to a power greater than one. The largest amplitude in the window is preserved, while smaller surrounding amplitudes are reduced. This produces a narrower and sharper representation of the seismic event.

Positive and negative amplitudes are treated separately so that seismic polarity is retained.

VRE is an **enhancement method**: it sharpens information already present in the seismic section. It should not be interpreted as generating new reflections or recovering geological information that was absent from the original data.

### Original VRE publication

> M. A. Rashed and A. H. Atef,  
> “Virtual resolution enhancement: A new enhancement tool for seismic data,”  
> *Open Geosciences*, 12, 363–375, 2020.  
> DOI: 10.1515/geo-2020-0169

This repository is an independent implementation developed from the VRE experiment used during my master's work. It is not the original software distributed by the authors of the VRE paper.

## Method

For each seismic trace, the input signal is separated into non-negative and negative components.

Within each moving window, the positive amplitudes are normalized by the local positive maximum and the negative amplitudes by the local negative extreme.

The transformation used in the original implementation is:

```text
positive: y = max(x) * (x / max(x))^r
negative: y = min(x) * (x / min(x))^r
where r is the enhancement power.
For r > 1, normalized amplitudes smaller than the local extreme are reduced:
0 < a < 1  ->  a^r < a
while the normalized peak remains unchanged:
1^r = 1
The effect is therefore to suppress amplitudes surrounding a local extreme more strongly than the extreme itself, producing a sharper seismic event.
Because the moving windows overlap, a sample can receive several estimates. The estimates from all windows containing that sample are averaged before the positive and negative components are recombined.
The operation is applied independently to every trace in the seismic section.
Original implementation
The original MATLAB code used during the master's experiment is preserved in:
VRE_3_original.m
The original experimental parameters are:
window = 80
power  = 3
An important MATLAB indexing detail is preserved in the Python version:
window = 80
corresponds to an inclusive interval of 81 samples, because both endpoints are included.
The number and positioning of moving windows are also kept consistent with the original implementation.
Python implementation
The original MATLAB implementation creates large intermediate arrays while storing the result from individual overlapping windows.
The Python implementation computes the same transformation without constructing the original nt × nt × nx intermediate arrays.
This substantially reduces memory requirements while preserving the numerical procedure used in the original experiment.
The implementation therefore focuses on:
- preserving the original VRE calculation;
- reducing unnecessary memory allocation;
- making the algorithm easier to read and reuse;
- providing a reproducible command-line interface;
- preserving the original MATLAB script for reference and validation.
Results
The following figures are results from the VRE experiment performed during my master's work.
Original seismic section
 
The input seismic section before application of VRE.
VRE-enhanced seismic section
 
After application of VRE, reflection events become sharper while the main reflector geometry remains visible.
The enhancement results from suppressing lower-amplitude samples surrounding local extrema relative to the extrema themselves.
VRE does not create new seismic events; it modifies the representation of events already contained in the input section.
Normalized amplitude spectrum
 
The normalized spectral comparison illustrates the change in frequency content produced by the nonlinear VRE transformation.
Sharpening a signal in the time domain naturally modifies its spectrum and can increase the relative contribution of higher frequencies. Similar spectral broadening was reported in the original VRE study.
The spectral difference should therefore be interpreted as a consequence of the nonlinear enhancement rather than as recovery of independently measured frequencies that were absent from the original seismic data.
Installation
Python 3.10 or newer is recommended.
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
On Windows:
.venv\Scripts\activate
python -m pip install -e .
Quick start
Run the self-contained synthetic example:
python examples/synthetic_example.py
Run the original experiment after placing Section_GARCH.mat in data/:
vre data/Section_GARCH.mat \
  --variable myfilter \
  --rows 0:700 \
  --columns 149:200 \
  --window 80 \
  --power 3 \
  --sample-interval 0.002 \
  --output results/original
The command writes the original and enhanced arrays to:
vre_result.npz
and generates the corresponding seismic-section and normalized-spectrum figures.
Repository structure
.
├── src/vre/               Python implementation and command-line interface
├── examples/              Reproducible synthetic example
├── tests/                 Numerical-equivalence and validation tests
├── figures/               Selected results from the master's work
├── data/README.md          Instructions for locally held research data
├── VRE_3_original.m       Original MATLAB research script
├── CITATION.cff           Software citation metadata
└── pyproject.toml          Package metadata and dependencies
Numerical fidelity and corrections
The cleaned implementation deliberately preserves important numerical details of the original MATLAB code.
In particular:
- positive and negative amplitudes are processed separately;
- the same nonlinear power transformation is used;
- overlapping window estimates are averaged;
- window = 80 corresponds to an inclusive span of 81 samples;
- the moving-window behavior follows the original implementation;
- the original power value of 3 is preserved as the default experimental setting.
The plotting code corrects the original frequency-axis construction by deriving the frequency bins from the actual number of samples and sampling interval.
This correction affects only the frequency coordinates used for visualization. It does not modify the VRE-enhanced seismic data.
The horizontal section axis is labelled as trace number because the original dataset/script does not provide physical offset coordinates.
Reproducibility
The original research dataset is not distributed with this repository because redistribution rights have not been established.
A small synthetic example is therefore included so that the VRE implementation can be run without access to the original data:
python examples/synthetic_example.py
Users who have access to the original MATLAB dataset can reproduce the original experiment by placing the data locally in the data/ directory.
The original MATLAB script is retained in the repository so that the Python implementation can be compared against the research code.
Limitations
- VRE is a nonlinear amplitude transformation.
- Results depend on the selected window length and enhancement power.
- Larger powers produce stronger suppression of amplitudes surrounding local extrema.
- The method modifies waveform shape and therefore also modifies the frequency spectrum.
- Spectral broadening should not automatically be interpreted as recovery of new geological information.
- VRE enhances existing seismic events rather than revealing reflections absent from the input data.
- The included experimental figures provide a qualitative demonstration rather than a general validation of performance.
- The original research data are not distributed because redistribution rights have not been established.
Citation
The VRE methodology originates from:
Rashed, M. A., & Atef, A. H. (2020).
Virtual resolution enhancement: A new enhancement tool for seismic data.
Open Geosciences, 12, 363–375.
https://doi.org/10.1515/geo-2020-0169

If you use the software from this repository, please also cite the repository using the metadata provided in CITATION.cff.
License
The software in this repository is available under the MIT License.
The VRE methodology originates from Rashed and Atef (2020). Research data, published articles, figures from third-party publications, and other externally owned materials remain subject to their respective copyright and licensing terms and are not covered by this repository's software license.
```
