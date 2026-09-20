import numpy as np
import pytest

from vre import enhance_section


def _literal_reference(data: np.ndarray, window: int, power: float) -> np.ndarray:
    """Direct translation of the original moving-window operations."""
    samples, traces = data.shape
    result = []
    for polarity in (np.where(data >= 0, data, 0.0), np.where(data < 0, data, 0.0)):
        virtual = np.full((samples, samples, traces), np.nan)
        for trace in range(traces):
            for start in range(samples - window):
                virtual[start : start + window + 1, start, trace] = polarity[
                    start : start + window + 1, trace
                ]
        scaled = np.full_like(virtual, np.nan)
        for trace in range(traces):
            for start in range(samples - window):
                column = virtual[:, start, trace]
                scale = np.nanmax(column) if polarity.min() >= 0 else np.nanmin(column)
                if scale != 0:
                    scaled[:, start, trace] = scale * (column / scale) ** power
        result.append(np.nanmean(scaled, axis=1))
    return result[0] + result[1]


def test_matches_literal_matlab_translation():
    data = np.array(
        [[0.2, -0.5], [1.0, -0.1], [-0.4, 0.3], [0.6, -0.8], [-0.2, 0.7]]
    )
    expected = _literal_reference(data, window=2, power=3)
    actual = enhance_section(data, window=2, power=3)
    np.testing.assert_allclose(actual, expected, rtol=1e-14, atol=1e-14)


def test_rejects_invalid_window():
    with pytest.raises(ValueError, match="smaller"):
        enhance_section(np.ones((4, 2)), window=4)


def test_shape_is_preserved():
    rng = np.random.default_rng(4)
    data = rng.standard_normal((20, 3))
    assert enhance_section(data, window=5).shape == data.shape
