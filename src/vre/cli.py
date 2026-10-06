"""Command-line entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .core import enhance_section
from .io import load_mat_section
from .plotting import save_comparison


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Enhance a seismic section with VRE.")
    parser.add_argument("input", type=Path, help="MATLAB .mat input file")
    parser.add_argument(
        "--variable", default="myfilter", help="array name in the MAT file"
    )
    parser.add_argument("--window", type=int, default=80)
    parser.add_argument("--power", type=float, default=3)
    parser.add_argument("--sample-interval", type=float, default=0.002, help="seconds")
    parser.add_argument("--rows", default="0:700", help="Python slice, e.g. 0:700")
    parser.add_argument(
        "--columns", default="149:200", help="Python slice, e.g. 149:200"
    )
    parser.add_argument("--output", type=Path, default=Path("results"))
    parser.add_argument(
        "--overwrite", action="store_true", help="replace existing result files"
    )
    return parser


def _slice(text: str) -> slice:
    fields = text.split(":")
    if len(fields) not in (2, 3):
        raise argparse.ArgumentTypeError("slice must have start:stop[:step] form")
    values = [int(field) if field else None for field in fields]
    return slice(*values)


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not np.isfinite(args.sample_interval) or args.sample_interval <= 0:
        parser.error("--sample-interval must be finite and positive")
    targets = ("vre_result.npz", "before_after.png", "normalized_spectrum.png")
    if not args.overwrite and any((args.output / name).exists() for name in targets):
        parser.error("result files already exist; choose another output or --overwrite")
    data = load_mat_section(
        args.input,
        variable=args.variable,
        rows=_slice(args.rows),
        columns=_slice(args.columns),
    )
    enhanced = enhance_section(data, window=args.window, power=args.power)
    args.output.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        args.output / "vre_result.npz", original=data, enhanced=enhanced
    )
    save_comparison(data, enhanced, args.output, sample_interval=args.sample_interval)
    print(f"Saved enhanced data and figures to {args.output.resolve()}")


if __name__ == "__main__":
    main()
