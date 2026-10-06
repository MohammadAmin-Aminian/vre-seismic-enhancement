import numpy as np
import pytest
from vre.plotting import save_comparison


def test_zero_spectrum_and_figures(tmp_path):
    with np.errstate(divide="raise", invalid="raise"):
        save_comparison(np.zeros((10, 2)), np.zeros((10, 2)), tmp_path)
    assert (tmp_path / "normalized_spectrum.png").is_file()
    assert (tmp_path / "before_after.png").is_file()


@pytest.mark.parametrize("interval", [0, -1, np.nan, np.inf])
def test_invalid_sampling_interval(tmp_path, interval):
    with pytest.raises(ValueError, match="sample_interval"):
        save_comparison(np.ones((10, 2)), np.ones((10, 2)), tmp_path, interval)
