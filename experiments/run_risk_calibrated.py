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
from src.calibration.interval_calibration import fit_residual_interval_calibrator
from src.calibration.interval_calibration import fit_grouped_residual_interval_calibrators
from src.calibration.metrics import (
    attach_interval_metrics,
    summarize_interval_metrics,
    summarize_overall_interval,
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
from src.policy.risk_calibrated_scaling import (
    RiskCalibratedConfig,
    simulate_risk_calibrated_policy,
)


def label_splits(frame: pd.DataFrame) -> pd.DataFrame:
    labeled = frame.copy()
    train_cut, val_cut = split_minutes(frame)
    labeled["split"] = "train"
    labeled.loc[labeled["minute"] >= train_cut, "split"] = "val"
    labeled.loc[labeled["minute"] >= val_cut, "split"] = "test"
    return labeled


def run_risk_calibrated_baseline(
    frame: pd.DataFrame,
    *,
    forecast_config: PointForecastConfig,
    policy_config: RiskCalibratedConfig,
    alpha: float,
    calibration_scope: str = "global",
    min_calibration_samples: int = 200,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, pd.Series]:
    train_frame = frame[frame["split"] == "train"].copy()
    model = fit_linear_autoregressive_model(train_frame, config=forecast_config)

    point_forecast_frames = []
    for _, app_frame in frame.groupby("app", sort=False):
        simulated = simulate_point_forecast_policy(
            app_frame,
            model,
            initial_capacity=forecast_config.initial_capacity,
            min_capacity=forecast_config.min_capacity,
        )
        point_forecast_frames.append(simulated)

    point_forecast_frame = pd.concat(point_forecast_frames, ignore_index=True)
    calibration_source = point_forecast_frame[point_forecast_frame["split"] == "val"].copy()
    if calibration_scope == "app":
        app_calibrators, global_calibrator = fit_grouped_residual_interval_calibrators(
            calibration_source,
            alpha=alpha,
            min_samples=min_calibration_samples,
        )
    else:
        app_calibrators = {}
        global_calibrator = fit_residual_interval_calibrator(
            calibration_source,
            alpha=alpha,
        )

    decisions = []
    for app, app_frame in point_forecast_frame.groupby("app", sort=False):
        calibrator = app_calibrators.get(str(app), global_calibrator)
        simulated = simulate_risk_calibrated_policy(
            app_frame,
            calibrator=calibrator,
            config=policy_config,
        )
        simulated["calibration_scope_used"] = (
            "app" if str(app) in app_calibrators else "global"
        )
        evaluated = attach_scaling_metrics(simulated)
        evaluated = attach_forecast_metrics(evaluated)
        evaluated = attach_interval_metrics(evaluated)
        decisions.append(evaluated)

    decisions_frame = pd.concat(decisions, ignore_index=True)
    nominal_coverage = 1.0 - alpha
    per_app_scaling = summarize_scaling_metrics(decisions_frame)
    per_app_forecast = summarize_forecast_metrics(decisions_frame)
    per_app_interval = summarize_interval_metrics(
        decisions_frame,
        nominal_coverage=nominal_coverage,
    )
    overall_scaling = summarize_overall(decisions_frame)
    overall_forecast = summarize_overall_forecast(decisions_frame)
    overall_interval = summarize_overall_interval(
        decisions_frame,
        nominal_coverage=nominal_coverage,
    )
    return (
        decisions_frame,
        per_app_scaling,
        per_app_forecast,
        per_app_interval,
        overall_scaling,
        overall_forecast,
        overall_interval,
    )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the calibration-aware risk-sensitive autoscaling policy."
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
    parser.add_argument("--alpha", type=float, default=0.10)
    parser.add_argument(
        "--calibration-scope",
        default="global",
        choices=["global", "app"],
        help="Whether calibration residuals are pooled globally or fitted per app.",
    )
    parser.add_argument(
        "--min-calibration-samples",
        type=int,
        default=200,
        help="Minimum validation residuals required for app-specific calibration.",
    )
    parser.add_argument("--initial-capacity", type=int, default=1)
    parser.add_argument("--min-capacity", type=int, default=0)
    parser.add_argument("--cost-weight", type=float, default=1.0)
    parser.add_argument("--underprovision-weight", type=float, default=8.0)
    parser.add_argument("--oscillation-weight", type=float, default=0.25)
    parser.add_argument("--candidate-buffer", type=int, default=5)
    parser.add_argument("--tail-risk-weight", type=float, default=0.0)
    parser.add_argument("--tail-alpha", type=float, default=0.99)
    parser.add_argument("--reactive-guard-lookback", type=int, default=0)
    parser.add_argument("--reactive-guard-factor", type=float, default=1.0)
    parser.add_argument("--reactive-guard-buffer", type=int, default=0)
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    frame = label_splits(frame)

    forecast_config = PointForecastConfig(
        history_window=args.history_window,
        horizon=args.horizon,
        initial_capacity=args.initial_capacity,
        min_capacity=args.min_capacity,
    )
    policy_config = RiskCalibratedConfig(
        initial_capacity=args.initial_capacity,
        min_capacity=args.min_capacity,
        cost_weight=args.cost_weight,
        underprovision_weight=args.underprovision_weight,
        oscillation_weight=args.oscillation_weight,
        candidate_buffer=args.candidate_buffer,
        tail_risk_weight=args.tail_risk_weight,
        tail_alpha=args.tail_alpha,
        reactive_guard_lookback=args.reactive_guard_lookback,
        reactive_guard_factor=args.reactive_guard_factor,
        reactive_guard_buffer=args.reactive_guard_buffer,
    )
    (
        decisions_frame,
        per_app_scaling,
        per_app_forecast,
        per_app_interval,
        overall_scaling,
        overall_forecast,
        overall_interval,
    ) = run_risk_calibrated_baseline(
        frame,
        forecast_config=forecast_config,
        policy_config=policy_config,
        alpha=args.alpha,
        calibration_scope=args.calibration_scope,
        min_calibration_samples=args.min_calibration_samples,
    )

    if args.split != "all":
        decisions_frame = decisions_frame[decisions_frame["split"] == args.split].copy()
        per_app_scaling = summarize_scaling_metrics(decisions_frame)
        per_app_forecast = summarize_forecast_metrics(decisions_frame)
        per_app_interval = summarize_interval_metrics(
            decisions_frame,
            nominal_coverage=1.0 - args.alpha,
        )
        overall_scaling = summarize_overall(decisions_frame)
        overall_forecast = summarize_overall_forecast(decisions_frame)
        overall_interval = summarize_overall_interval(
            decisions_frame,
            nominal_coverage=1.0 - args.alpha,
        )

    summary = per_app_scaling.merge(per_app_forecast, on="app", how="left")
    summary = summary.merge(per_app_interval, on=["app", "forecast_steps"], how="left")

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
    print("\nOverall interval summary:")
    print(overall_interval.to_string())
    print(f"\nSaved per-app summary to {summary_out}")
    print(f"Saved decisions to {decisions_out}")


if __name__ == "__main__":
    main()
