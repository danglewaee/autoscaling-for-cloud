from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.burst_analysis import mark_burst_minutes, summarize_burst_subset


BASELINE_ORDER = [
    "reactive",
    "moving_average",
    "point_forecast",
    "fixed_quantile",
    "risk_calibrated",
]


def _baseline_name(path: Path) -> str:
    return path.stem.replace("_decisions", "")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate baselines on burst-only windows.")
    parser.add_argument("--result-dir", default="results")
    parser.add_argument("--split", default="test", choices=["train", "val", "test"])
    parser.add_argument("--rolling-window", type=int, default=30)
    parser.add_argument("--burst-quantile", type=float, default=0.90)
    parser.add_argument("--burst-multiplier", type=float, default=2.0)
    parser.add_argument("--min-jump", type=float, default=1.0)
    parser.add_argument("--output-csv", default=None)
    parser.add_argument("--output-md", default=None)
    args = parser.parse_args()

    result_dir = Path(args.result_dir)
    decision_files = []
    for baseline in BASELINE_ORDER:
        path = result_dir / f"{baseline}_decisions.csv"
        if path.exists():
            decision_files.append(path)

    if not decision_files:
        raise ValueError(f"No decision files found in {result_dir}")

    rows = []
    for path in decision_files:
        frame = pd.read_csv(path)
        if "split" in frame.columns:
            frame = frame[frame["split"] == args.split].copy()

        marked = mark_burst_minutes(
            frame,
            rolling_window=args.rolling_window,
            burst_quantile=args.burst_quantile,
            burst_multiplier=args.burst_multiplier,
            min_jump=args.min_jump,
        )
        summary = summarize_burst_subset(marked).to_dict()
        summary["baseline"] = _baseline_name(path)
        rows.append(summary)

    comparison = pd.DataFrame(rows)
    ordered = ["baseline", "burst_steps", "burst_fraction", "burst_episodes", "mean_cost", "sla_violation_rate", "mean_underprovision", "mean_overprovision", "mean_oscillation"]
    comparison = comparison[ordered]

    output_csv = Path(args.output_csv) if args.output_csv else result_dir / "burst_comparison.csv"
    output_md = Path(args.output_md) if args.output_md else result_dir / "burst_comparison.md"
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    comparison.to_csv(output_csv, index=False)

    md_lines = [
        "| " + " | ".join(ordered) + " |",
        "| " + " | ".join(["---"] * len(ordered)) + " |",
    ]
    for record in comparison.to_dict(orient="records"):
        values = []
        for column in ordered:
            value = record[column]
            if isinstance(value, str):
                values.append(value)
            elif pd.isna(value):
                values.append("")
            elif isinstance(value, (int,)) or (isinstance(value, float) and value.is_integer() and column.endswith(("steps", "episodes"))):
                values.append(str(int(value)))
            else:
                values.append(f"{float(value):.6f}")
        md_lines.append("| " + " | ".join(values) + " |")

    output_md.write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(comparison.to_string(index=False))
    print(f"\nSaved CSV to {output_csv}")
    print(f"Saved Markdown to {output_md}")


if __name__ == "__main__":
    main()
