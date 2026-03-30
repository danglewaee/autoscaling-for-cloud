from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.baselines.point_forecast import (
    PointForecastConfig,
    fit_linear_autoregressive_model,
    simulate_point_forecast_policy,
)
from src.data.make_windows import split_minutes
from src.evaluation.forecast_metrics import (
    attach_forecast_metrics,
    summarize_forecast_metrics,
    summarize_overall_forecast,
)
from src.evaluation.scaling_metrics import (
    attach_scaling_metrics,
    summarize_overall,
    summarize_scaling_metrics,
)


def label_splits(frame: pd.DataFrame) -> pd.DataFrame:
    labeled = frame.copy()
    train_cut, val_cut = split_minutes(frame)
    labeled["split"] = "train"
    labeled.loc[labeled["minute"] >= train_cut, "split"] = "val"
    labeled.loc[labeled["minute"] >= val_cut, "split"] = "test"
    return labeled


def run_point_forecast_baseline(
    frame: pd.DataFrame,
    *,
    config: PointForecastConfig,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    train_frame = frame[frame["split"] == "train"].copy()
    model = fit_linear_autoregressive_model(train_frame, config=config)

    decisions = []
    for _, app_frame in frame.groupby("app", sort=False):
        simulated = simulate_point_forecast_policy(
            app_frame,
            model,
            initial_capacity=config.initial_capacity,
            min_capacity=config.min_capacity,
        )
        evaluated = attach_scaling_metrics(simulated)
        evaluated = attach_forecast_metrics(evaluated)
        decisions.append(evaluated)

    decisions_frame = pd.concat(decisions, ignore_index=True)
    per_app_scaling = summarize_scaling_metrics(decisions_frame)
    per_app_forecast = summarize_forecast_metrics(decisions_frame)
    overall_scaling = summarize_overall(decisions_frame)
    overall_forecast = summarize_overall_forecast(decisions_frame)
    return (
        decisions_frame,
        per_app_scaling,
        per_app_forecast,
        overall_scaling,
        overall_forecast,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the autoregressive point-forecast autoscaling baseline."
    )
    parser.add_argument("--input", required=True, help="Processed minute-level CSV.")
    parser.add_argument("--summary-out", required=True, help="Where to save per-app summary.")
    parser.add_argument("--decisions-out", required=True, help="Where to save step-level decisions.")
    parser.add_argument(
        "--split",
        default="test",
        choices=["all", "train", "val", "test"],
        help="Which time split to evaluate.",
    )
    parser.add_argument("--history-window", type=int, default=30)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--initial-capacity", type=int, default=1)
    parser.add_argument("--min-capacity", type=int, default=0)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    frame = label_splits(frame)

    config = PointForecastConfig(
        history_window=args.history_window,
        horizon=args.horizon,
        initial_capacity=args.initial_capacity,
        min_capacity=args.min_capacity,
    )
    (
        decisions_frame,
        per_app_scaling,
        per_app_forecast,
        overall_scaling,
        overall_forecast,
    ) = run_point_forecast_baseline(frame, config=config)

    if args.split != "all":
        decisions_frame = decisions_frame[decisions_frame["split"] == args.split].copy()
        per_app_scaling = summarize_scaling_metrics(decisions_frame)
        per_app_forecast = summarize_forecast_metrics(decisions_frame)
        overall_scaling = summarize_overall(decisions_frame)
        overall_forecast = summarize_overall_forecast(decisions_frame)

    summary = per_app_scaling.merge(per_app_forecast, on="app", how="left")

    summary_out = Path(args.summary_out)
    decisions_out = Path(args.decisions_out)
    summary_out.parent.mkdir(parents=True, exist_ok=True)
    decisions_out.parent.mkdir(parents=True, exist_ok=True)

    summary.to_csv(summary_out, index=False)
    decisions_frame.to_csv(decisions_out, index=False)

    print("Overall scaling summary:")
    print(overall_scaling.to_string())
    print("\nOverall forecast summary:")
    print(overall_forecast.to_string())
    print(f"\nSaved per-app summary to {summary_out}")
    print(f"Saved decisions to {decisions_out}")


if __name__ == "__main__":
    main()
