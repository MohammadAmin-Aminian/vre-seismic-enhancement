"""Run VRE on a small deterministic synthetic seismic section."""

from pathlib import Path

import numpy as np

from vre import enhance_section
from vre.plotting import save_comparison


def synthetic_section(samples: int = 500, traces: int = 80) -> np.ndarray:
    time = np.linspace(0, 1, samples)[:, None]
    trace = np.linspace(-1, 1, traces)[None, :]
    reflector_1 = np.exp(-((time - (0.35 + 0.03 * trace)) / 0.012) ** 2)
    reflector_2 = -0.7 * np.exp(-((time - (0.68 - 0.05 * trace)) / 0.018) ** 2)
    rng = np.random.default_rng(7)
    return reflector_1 + reflector_2 + 0.08 * rng.standard_normal((samples, traces))


if __name__ == "__main__":
    data = synthetic_section()
    enhanced = enhance_section(data, window=60, power=3)
    output = Path("results/synthetic")
    output.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(output.with_suffix(".npz"), original=data, enhanced=enhanced)
    save_comparison(data, enhanced, output)
    print(f"Saved example results to {output.resolve()}")
