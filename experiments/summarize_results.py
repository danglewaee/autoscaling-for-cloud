from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd


BASELINE_ORDER = [
    "reactive",
    "moving_average",
    "point_forecast",
    "fixed_quantile",
    "risk_calibrated",
]


def _baseline_name_from_path(path: Path) -> str:
    name = path.stem
    if name.endswith("_decisions"):
        return name[: -len("_decisions")]
    return name


def _format_float(value: float | int | str | None) -> str:
    if value is None or (isinstance(value, float) and np.isnan(value)):
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, (int, np.integer)):
        return str(int(value))
    return f"{float(value):.6f}"


def summarize_decisions_file(
    path: Path,
    *,
    nominal_coverage: float = 0.90,
) -> dict[str, float | str]:
    frame = pd.read_csv(path)
    row: dict[str, float | str] = {
        "baseline": _baseline_name_from_path(path),
        "steps": int(len(frame)),
    }

    if "cost" in frame.columns:
        row["mean_cost"] = float(frame["cost"].mean())
        row["total_cost"] = float(frame["cost"].sum())
    if "sla_violation" in frame.columns:
        row["sla_violation_rate"] = float(frame["sla_violation"].mean())
    if "underprovision" in frame.columns:
        row["mean_underprovision"] = float(frame["underprovision"].mean())
        row["total_underprovision"] = float(frame["underprovision"].sum())
    if "overprovision" in frame.columns:
        row["mean_overprovision"] = float(frame["overprovision"].mean())
    if "oscillation" in frame.columns:
        row["mean_oscillation"] = float(frame["oscillation"].mean())
        row["total_oscillation"] = float(frame["oscillation"].sum())

    if "forecast_error" in frame.columns:
        row["mae"] = float(frame["abs_error"].mean())
        row["rmse"] = float(np.sqrt(frame["squared_error"].mean()))
        row["mean_forecast_error"] = float(frame["forecast_error"].mean())

    if "pinball_loss" in frame.columns:
        row["pinball_loss"] = float(frame["pinball_loss"].mean())
    if "forecast_quantile" in frame.columns:
        row["forecast_quantile"] = float(frame["forecast_quantile"].iloc[0])

    if "covered" in frame.columns:
        empirical_coverage = float(frame["covered"].mean())
        row["nominal_coverage"] = float(nominal_coverage)
        row["empirical_coverage"] = empirical_coverage
        row["calibration_gap"] = abs(empirical_coverage - nominal_coverage)
    if "interval_width" in frame.columns:
        row["average_interval_width"] = float(frame["interval_width"].mean())

    return row


def discover_decision_files(result_dir: Path) -> list[Path]:
    files = sorted(result_dir.glob("*_decisions.csv"))

    def sort_key(path: Path) -> tuple[int, str]:
        baseline = _baseline_name_from_path(path)
        try:
            index = BASELINE_ORDER.index(baseline)
        except ValueError:
            index = len(BASELINE_ORDER)
        return index, baseline

    return sorted(files, key=sort_key)


def build_markdown_table(frame: pd.DataFrame, columns: Iterable[str]) -> str:
    columns = [column for column in columns if column in frame.columns]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"

    rows = [header, separator]
    for record in frame[columns].to_dict(orient="records"):
        row = "| " + " | ".join(_format_float(record[column]) for column in columns) + " |"
        rows.append(row)

    return "\n".join(rows) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Aggregate per-step decisions into one baseline comparison table."
    )
    parser.add_argument(
        "--result-dir",
        default="results",
        help="Directory containing *_decisions.csv files.",
    )
    parser.add_argument(
        "--output-csv",
        default=None,
        help="Optional output CSV path. Defaults to <result-dir>/baseline_comparison.csv.",
    )
    parser.add_argument(
        "--output-md",
        default=None,
        help="Optional output markdown path. Defaults to <result-dir>/baseline_comparison.md.",
    )
    parser.add_argument(
        "--nominal-coverage",
        type=float,
        default=0.90,
        help="Nominal coverage used for interval-based methods.",
    )
    args = parser.parse_args()

    result_dir = Path(args.result_dir)
    decision_files = discover_decision_files(result_dir)
    if not decision_files:
        raise ValueError(f"No *_decisions.csv files found in {result_dir}")

    rows = [
        summarize_decisions_file(path, nominal_coverage=args.nominal_coverage)
        for path in decision_files
    ]
    comparison = pd.DataFrame(rows)

    preferred_columns = [
        "baseline",
        "steps",
        "mean_cost",
        "sla_violation_rate",
        "mean_underprovision",
        "mean_overprovision",
        "mean_oscillation",
        "mae",
        "rmse",
        "pinball_loss",
        "empirical_coverage",
        "calibration_gap",
    ]
    ordered_columns = [
        column for column in preferred_columns if column in comparison.columns
    ] + [
        column
        for column in comparison.columns
        if column not in preferred_columns
    ]
    comparison = comparison[ordered_columns]

    output_csv = (
        Path(args.output_csv)
        if args.output_csv is not None
        else result_dir / "baseline_comparison.csv"
    )
    output_md = (
        Path(args.output_md)
        if args.output_md is not None
        else result_dir / "baseline_comparison.md"
    )
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)

    comparison.to_csv(output_csv, index=False)
    markdown = build_markdown_table(comparison, ordered_columns)
    output_md.write_text(markdown, encoding="utf-8")

    print(comparison.to_string(index=False))
    print(f"\nSaved CSV to {output_csv}")
    print(f"Saved Markdown to {output_md}")


if __name__ == "__main__":
    main()
