# Data

Research data are not distributed in this repository. The published article states that data are available from the corresponding author on request.

To reproduce the original VRE experiment, place `Section_GARCH.mat` in this directory. The expected variable is `myfilter`; the default command selects MATLAB rows `1:700` and columns `150:200`.

```bash
vre data/Section_GARCH.mat
```

Do not commit datasets unless you have permission to redistribute them.
