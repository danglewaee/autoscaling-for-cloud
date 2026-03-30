from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.plotting.case_study_plots import plot_capacity_case_study


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a case-study capacity plot.")
    parser.add_argument("--input", required=True, help="Processed or decisions CSV.")
    parser.add_argument("--output", required=True, help="Path to output PNG.")
    parser.add_argument("--app", default=None, help="Optional app id filter.")
    parser.add_argument("--split", default=None, choices=["train", "val", "test"], help="Optional split filter.")
    parser.add_argument("--max-points", type=int, default=300)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)

    if args.app is None:
        args.app = str(frame["app"].iloc[0])

    app_frame = frame[frame["app"].astype(str) == str(args.app)].copy()
    if args.split is not None and "split" in app_frame.columns:
        app_frame = app_frame[app_frame["split"] == args.split].copy()

    if app_frame.empty:
        raise ValueError("No rows matched the requested app/split selection.")

    output_path = plot_capacity_case_study(
        app_frame,
        output_path=args.output,
        title=f"App {args.app}",
        max_points=args.max_points,
    )
    print(f"Saved plot to {output_path}")


if __name__ == "__main__":
    main()
