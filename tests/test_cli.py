"""Exercise the public CLI with a real MAT file and numerical/figure outputs."""

import numpy as np
import pytest
from scipy.io import savemat
from vre.cli import main
from vre.core import enhance_section


def test_mat_to_results_and_explicit_overwrite(tmp_path):
    data = np.random.default_rng(7).normal(size=(40, 6))
    source = tmp_path / "section.mat"
    output = tmp_path / "results"
    savemat(source, {"myfilter": data})
    args = [
        str(source),
        "--rows",
        ":",
        "--columns",
        ":",
        "--window",
        "8",
        "--output",
        str(output),
    ]
    main(args)
    with np.load(output / "vre_result.npz", allow_pickle=False) as result:
        np.testing.assert_array_equal(result["original"], data)
        np.testing.assert_allclose(result["enhanced"], enhance_section(data, window=8))
    for name in ["before_after.png", "normalized_spectrum.png"]:
        assert (output / name).read_bytes().startswith(b"\x89PNG\r\n\x1a\n")
    before = {p.name: p.read_bytes() for p in output.iterdir()}
    with pytest.raises(SystemExit):
        main(args)
    assert before == {p.name: p.read_bytes() for p in output.iterdir()}
    main(args + ["--overwrite"])


@pytest.mark.parametrize("interval", ["0", "-1", "nan", "inf"])
def test_invalid_interval_creates_no_results(tmp_path, interval):
    output = tmp_path / "results"
    with pytest.raises(SystemExit):
        main(
            [
                str(tmp_path / "missing.mat"),
                "--output",
                str(output),
                "--sample-interval",
                interval,
            ]
        )
    assert not output.exists()
