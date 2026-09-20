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
