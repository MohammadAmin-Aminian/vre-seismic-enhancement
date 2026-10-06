# Changelog

## 0.1.2

- Validate CLI sample interval before reading or writing files.
- Refuse existing result files unless `--overwrite` is specified.
- Add MAT-to-NPZ/PNG integration tests and development guidance.

## 0.1.1

- Treat absent positive or negative polarity as a zero contribution, eliminating
  NaNs for zero, constant and locally single-polarity sections.
- Require finite positive powers and plotting sample intervals.
- Handle zero spectra without division by zero.
- Add regression tests for these cases and automated GitHub checks.

The original MATLAB script remains available for provenance; its missing-polarity
NaN behavior is intentionally corrected rather than reproduced.
