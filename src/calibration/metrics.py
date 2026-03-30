from __future__ import annotations

import pandas as pd


def attach_interval_metrics(
    frame: pd.DataFrame,
    *,
    target_column: str = "required_capacity",
    lower_column: str = "interval_low",
    upper_column: str = "interval_high",
) -> pd.DataFrame:
    evaluated = frame.copy()
    evaluated["interval_width"] = evaluated[upper_column] - evaluated[lower_column]
    evaluated["covered"] = (
        (evaluated[target_column] >= evaluated[lower_column])
        & (evaluated[target_column] <= evaluated[upper_column])
    ).astype(int)
    return evaluated


def summarize_interval_metrics(
    frame: pd.DataFrame,
    *,
    nominal_coverage: float,
    app_column: str = "app",
) -> pd.DataFrame:
    summary = (
        frame.groupby(app_column, as_index=False)
        .agg(
            forecast_steps=("minute", "size"),
            empirical_coverage=("covered", "mean"),
            average_interval_width=("interval_width", "mean"),
        )
        .sort_values("empirical_coverage", ascending=True, ignore_index=True)
    )
    summary["calibration_gap"] = (
        summary["empirical_coverage"] - nominal_coverage
    ).abs()
    return summary


def summarize_overall_interval(frame: pd.DataFrame, *, nominal_coverage: float) -> pd.Series:
    empirical_coverage = float(frame["covered"].mean())
    return pd.Series(
        {
            "forecast_steps": int(len(frame)),
            "nominal_coverage": float(nominal_coverage),
            "empirical_coverage": empirical_coverage,
            "calibration_gap": abs(empirical_coverage - nominal_coverage),
            "average_interval_width": float(frame["interval_width"].mean()),
        }
    )
