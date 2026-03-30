from __future__ import annotations

import argparse
import itertools
from pathlib import Path
import sys

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.run_risk_calibrated import label_splits
from src.baselines.point_forecast import (
    PointForecastConfig,
    fit_linear_autoregressive_model,
    simulate_point_forecast_policy,
)
from src.calibration.interval_calibration import fit_residual_interval_calibrator
from src.calibration.metrics import attach_interval_metrics, summarize_overall_interval
from src.evaluation.forecast_metrics import attach_forecast_metrics, summarize_overall_forecast
from src.evaluation.scaling_metrics import attach_scaling_metrics, summarize_overall
from src.policy.risk_calibrated_scaling import RiskCalibratedConfig, simulate_risk_calibrated_policy


def _parse_float_list(raw: str) -> list[float]:
    return [float(item.strip()) for item in raw.split(",") if item.strip()]


def main() -> None:
    parser = argparse.ArgumentParser(description="Sweep alpha and policy weights for the risk-calibrated method.")
    parser.add_argument("--input", required=True)
    parser.add_argument("--split", default="test", choices=["train", "val", "test"])
    parser.add_argument("--history-window", type=int, default=30)
    parser.add_argument("--horizon", type=int, default=5)
    parser.add_argument("--initial-capacity", type=int, default=1)
    parser.add_argument("--min-capacity", type=int, default=0)
    parser.add_argument("--alphas", default="0.05,0.10,0.15")
    parser.add_argument("--cost-weights", default="1.0")
    parser.add_argument("--underprovision-weights", default="6.0,8.0,10.0")
    parser.add_argument("--oscillation-weights", default="0.10,0.25,0.50")
    parser.add_argument("--candidate-buffer", type=int, default=5)
    parser.add_argument("--output-csv", default="results/risk_sweep.csv")
    args = parser.parse_args()

    frame = pd.read_csv(args.input)
    frame = label_splits(frame)

    forecast_config = PointForecastConfig(
        history_window=args.history_window,
        horizon=args.horizon,
        initial_capacity=args.initial_capacity,
        min_capacity=args.min_capacity,
    )
    train_frame = frame[frame["split"] == "train"].copy()
    model = fit_linear_autoregressive_model(train_frame, config=forecast_config)

    forecast_frames = []
    for _, app_frame in frame.groupby("app", sort=False):
        forecast_frames.append(
            simulate_point_forecast_policy(
                app_frame,
                model,
                initial_capacity=forecast_config.initial_capacity,
                min_capacity=forecast_config.min_capacity,
            )
        )

    point_forecast_frame = pd.concat(forecast_frames, ignore_index=True)
    point_forecast_frame = attach_forecast_metrics(point_forecast_frame)
    point_forecast_eval = point_forecast_frame[point_forecast_frame["split"] == args.split].copy()
    overall_forecast = summarize_overall_forecast(point_forecast_eval)

    alphas = _parse_float_list(args.alphas)
    cost_weights = _parse_float_list(args.cost_weights)
    under_weights = _parse_float_list(args.underprovision_weights)
    osc_weights = _parse_float_list(args.oscillation_weights)

    rows = []
    calibration_source = point_forecast_frame[point_forecast_frame["split"] == "val"].copy()
    output_csv = Path(args.output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)

    for alpha in alphas:
        calibrator = fit_residual_interval_calibrator(calibration_source, alpha=alpha)

        interval_frames = []
        for _, app_frame in point_forecast_frame.groupby("app", sort=False):
            app_frame = app_frame.copy()
            app_frame["interval_low"] = app_frame["forecast_capacity"].apply(
                lambda prediction: calibrator.interval(float(prediction))[0]
            )
            app_frame["interval_high"] = app_frame["forecast_capacity"].apply(
                lambda prediction: calibrator.interval(float(prediction))[1]
            )
            interval_frames.append(app_frame)

        interval_frame = pd.concat(interval_frames, ignore_index=True)
        interval_frame = attach_interval_metrics(interval_frame)
        interval_eval = interval_frame[interval_frame["split"] == args.split].copy()
        overall_interval = summarize_overall_interval(interval_eval, nominal_coverage=1.0 - alpha)

        for cost_weight, under_weight, osc_weight in itertools.product(
            cost_weights,
            under_weights,
            osc_weights,
        ):
            policy_config = RiskCalibratedConfig(
                initial_capacity=args.initial_capacity,
                min_capacity=args.min_capacity,
                cost_weight=cost_weight,
                underprovision_weight=under_weight,
                oscillation_weight=osc_weight,
                candidate_buffer=args.candidate_buffer,
            )

            decision_frames = []
            for _, app_frame in point_forecast_frame.groupby("app", sort=False):
                simulated = simulate_risk_calibrated_policy(
                    app_frame,
                    calibrator=calibrator,
                    config=policy_config,
                )
                evaluated = attach_scaling_metrics(simulated)
                decision_frames.append(evaluated)

            decisions = pd.concat(decision_frames, ignore_index=True)
            decisions = decisions[decisions["split"] == args.split].copy()
            overall_scaling = summarize_overall(decisions)

            rows.append(
                {
                    "alpha": alpha,
                    "cost_weight": cost_weight,
                    "underprovision_weight": under_weight,
                    "oscillation_weight": osc_weight,
                    "mean_cost": float(overall_scaling["mean_cost"]),
                    "sla_violation_rate": float(overall_scaling["sla_violation_rate"]),
                    "mean_underprovision": float(overall_scaling["mean_underprovision"]),
                    "mean_overprovision": float(overall_scaling["mean_overprovision"]),
                    "mean_oscillation": float(overall_scaling["mean_oscillation"]),
                    "mae": float(overall_forecast["mae"]),
                    "rmse": float(overall_forecast["rmse"]),
                    "empirical_coverage": float(overall_interval["empirical_coverage"]),
                    "calibration_gap": float(overall_interval["calibration_gap"]),
                    "average_interval_width": float(overall_interval["average_interval_width"]),
                }
            )

            sweep = pd.DataFrame(rows).sort_values(
                ["sla_violation_rate", "mean_cost", "mean_oscillation"],
                ascending=[True, True, True],
                ignore_index=True,
            )
            sweep.to_csv(output_csv, index=False)

    sweep = pd.DataFrame(rows).sort_values(
        ["sla_violation_rate", "mean_cost", "mean_oscillation"],
        ascending=[True, True, True],
        ignore_index=True,
    )
    sweep.to_csv(output_csv, index=False)
    print(sweep.to_string(index=False))
    print(f"\nSaved CSV to {output_csv}")


if __name__ == "__main__":
    main()
