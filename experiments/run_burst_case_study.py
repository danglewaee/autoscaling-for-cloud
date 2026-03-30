from __future__ import annotations

import argparse
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.evaluation.burst_analysis import mark_burst_minutes
from src.plotting.case_study_plots import plot_burst_case_study


REQUIRED_METHODS = ["reactive", "point_forecast", "risk_calibrated"]


def _load_decision_frames(result_dir: Path, split: str) -> dict[str, pd.DataFrame]:
    frames: dict[str, pd.DataFrame] = {}
    for method_name in REQUIRED_METHODS:
        path = result_dir / f"{method_name}_decisions.csv"
        if not path.exists():
            raise FileNotFoundError(f"Missing decision file: {path}")

        frame = pd.read_csv(path)
        if "split" in frame.columns:
            frame = frame[frame["split"] == split].copy()
        if frame.empty:
            raise ValueError(f"No rows available for split '{split}' in {path}")
        frames[method_name] = frame

    return frames


def _select_episode(
    risk_frame: pd.DataFrame,
    *,
    app: str | None,
    rolling_window: int,
    burst_quantile: float,
    burst_multiplier: float,
    min_jump: float,
) -> pd.Series:
    marked = mark_burst_minutes(
        risk_frame,
        rolling_window=rolling_window,
        burst_quantile=burst_quantile,
        burst_multiplier=burst_multiplier,
        min_jump=min_jump,
    )
    episodes = (
        marked[marked["is_burst"] == 1]
        .groupby(["app", "burst_episode_id"], as_index=False)
        .agg(
            start_minute=("minute", "min"),
            end_minute=("minute", "max"),
            steps=("minute", "size"),
            total_underprovision=("underprovision", "sum"),
            max_required=("required_capacity", "max"),
            mean_required=("required_capacity", "mean"),
        )
        .sort_values(
            ["total_underprovision", "max_required", "steps"],
            ascending=[False, False, False],
        )
        .reset_index(drop=True)
    )
    if app is not None:
        episodes = episodes[episodes["app"].astype(str) == str(app)].reset_index(drop=True)

    if episodes.empty:
        raise ValueError("No burst episodes were found with the requested filters.")

    return episodes.iloc[0]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a multi-method burst case-study figure."
    )
    parser.add_argument("--result-dir", default="results")
    parser.add_argument("--output", default="paper/figures/burst_case_study.png")
    parser.add_argument("--split", default="test", choices=["train", "val", "test"])
    parser.add_argument("--app", default=None)
    parser.add_argument("--start-minute", type=int, default=None)
    parser.add_argument("--end-minute", type=int, default=None)
    parser.add_argument("--context-minutes", type=int, default=10)
    parser.add_argument("--rolling-window", type=int, default=30)
    parser.add_argument("--burst-quantile", type=float, default=0.90)
    parser.add_argument("--burst-multiplier", type=float, default=2.0)
    parser.add_argument("--min-jump", type=float, default=1.0)
    args = parser.parse_args()

    result_dir = Path(args.result_dir)
    frames = _load_decision_frames(result_dir, args.split)

    if args.start_minute is not None or args.end_minute is not None:
        if args.app is None or args.start_minute is None or args.end_minute is None:
            raise ValueError(
                "--app, --start-minute, and --end-minute must be provided together."
            )
        selected = pd.Series(
            {
                "app": args.app,
                "start_minute": int(args.start_minute),
                "end_minute": int(args.end_minute),
                "steps": int(args.end_minute - args.start_minute + 1),
                "total_underprovision": float("nan"),
                "max_required": float("nan"),
                "mean_required": float("nan"),
            }
        )
    else:
        selected = _select_episode(
            frames["risk_calibrated"],
            app=args.app,
            rolling_window=args.rolling_window,
            burst_quantile=args.burst_quantile,
            burst_multiplier=args.burst_multiplier,
            min_jump=args.min_jump,
        )

    app_id = str(selected["app"])
    start_minute = int(selected["start_minute"])
    end_minute = int(selected["end_minute"])

    method_frames = {
        method_name: frame[frame["app"].astype(str) == app_id].copy()
        for method_name, frame in frames.items()
    }
    for method_name, frame in method_frames.items():
        if frame.empty:
            raise ValueError(f"No rows found for app '{app_id}' in method '{method_name}'.")

    title = (
        f"Burst case study for app {app_id[:12]}... "
        f"(minutes {start_minute}-{end_minute})"
    )
    output_path = plot_burst_case_study(
        method_frames,
        output_path=args.output,
        burst_start_minute=start_minute,
        burst_end_minute=end_minute,
        context_minutes=args.context_minutes,
        title=title,
    )

    print("Selected episode:")
    print(selected.to_string())
    print(f"\nSaved burst case-study figure to {output_path}")


if __name__ == "__main__":
    main()
