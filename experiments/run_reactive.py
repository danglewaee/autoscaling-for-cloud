from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.baselines.reactive import ReactivePolicyConfig, simulate_reactive_policy
from src.data.make_windows import split_minutes
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


def run_reactive_baseline(
    frame: pd.DataFrame,
    *,
    config: ReactivePolicyConfig,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series]:
    decisions = []

    for _, app_frame in frame.groupby("app", sort=False):
        simulated = simulate_reactive_policy(app_frame, config=config)
        evaluated = attach_scaling_metrics(simulated)
        decisions.append(evaluated)

    decisions_frame = pd.concat(decisions, ignore_index=True)
    per_app = summarize_scaling_metrics(decisions_frame)
    overall = summarize_overall(decisions_frame)
    return decisions_frame, per_app, overall


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the reactive autoscaling baseline.")
    parser.add_argument("--input", required=True, help="Processed minute-level CSV.")
    parser.add_argument("--summary-out", required=True, help="Where to save per-app summary.")
    parser.add_argument("--decisions-out", required=True, help="Where to save step-level decisions.")
    parser.add_argument(
        "--split",
        default="test",
        choices=["all", "train", "val", "test"],
        help="Which time split to evaluate.",
    )
    parser.add_argument("--initial-capacity", type=int, default=1)
    parser.add_argument("--min-capacity", type=int, default=0)
    parser.add_argument("--scale-up-delay", type=int, default=1)
    parser.add_argument("--scale-down-delay", type=int, default=1)
    parser.add_argument("--downscale-stabilization", type=int, default=5)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    frame = select_split(frame, args.split)

    config = ReactivePolicyConfig(
        initial_capacity=args.initial_capacity,
        min_capacity=args.min_capacity,
        scale_up_delay=args.scale_up_delay,
        scale_down_delay=args.scale_down_delay,
        downscale_stabilization=args.downscale_stabilization,
    )
    frame = label_splits(frame)
    decisions_frame, _, _ = run_reactive_baseline(frame, config=config)

    if args.split != "all":
        decisions_frame = decisions_frame[decisions_frame["split"] == args.split].copy()

    per_app = summarize_scaling_metrics(decisions_frame)
    overall = summarize_overall(decisions_frame)

    summary_out = Path(args.summary_out)
    decisions_out = Path(args.decisions_out)
    summary_out.parent.mkdir(parents=True, exist_ok=True)
    decisions_out.parent.mkdir(parents=True, exist_ok=True)

    per_app.to_csv(summary_out, index=False)
    decisions_frame.to_csv(decisions_out, index=False)

    print("Overall summary:")
    print(overall.to_string())
    print(f"\nSaved per-app summary to {summary_out}")
    print(f"Saved decisions to {decisions_out}")


if __name__ == "__main__":
    main()
