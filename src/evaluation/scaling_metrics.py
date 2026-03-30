from __future__ import annotations

import pandas as pd


def attach_scaling_metrics(
    frame: pd.DataFrame,
    *,
    demand_column: str = "required_capacity",
    capacity_column: str = "provisioned_capacity",
) -> pd.DataFrame:
    evaluated = frame.copy()
    evaluated["cost"] = evaluated[capacity_column]
    evaluated["underprovision"] = (
        evaluated[demand_column] - evaluated[capacity_column]
    ).clip(lower=0)
    evaluated["overprovision"] = (
        evaluated[capacity_column] - evaluated[demand_column]
    ).clip(lower=0)
    evaluated["sla_violation"] = (
        evaluated[demand_column] > evaluated[capacity_column]
    ).astype(int)
    evaluated["oscillation"] = evaluated[capacity_column].diff().abs().fillna(0)
    return evaluated


def summarize_scaling_metrics(
    frame: pd.DataFrame,
    *,
    app_column: str = "app",
) -> pd.DataFrame:
    summary = (
        frame.groupby(app_column, as_index=False)
        .agg(
            steps=("minute", "size"),
            mean_cost=("cost", "mean"),
            total_cost=("cost", "sum"),
            sla_violation_rate=("sla_violation", "mean"),
            mean_underprovision=("underprovision", "mean"),
            total_underprovision=("underprovision", "sum"),
            mean_overprovision=("overprovision", "mean"),
            total_oscillation=("oscillation", "sum"),
            mean_oscillation=("oscillation", "mean"),
        )
        .sort_values("sla_violation_rate", ascending=False, ignore_index=True)
    )
    return summary


def summarize_overall(frame: pd.DataFrame) -> pd.Series:
    return pd.Series(
        {
            "steps": int(len(frame)),
            "mean_cost": float(frame["cost"].mean()),
            "total_cost": float(frame["cost"].sum()),
            "sla_violation_rate": float(frame["sla_violation"].mean()),
            "mean_underprovision": float(frame["underprovision"].mean()),
            "total_underprovision": float(frame["underprovision"].sum()),
            "mean_overprovision": float(frame["overprovision"].mean()),
            "total_oscillation": float(frame["oscillation"].sum()),
            "mean_oscillation": float(frame["oscillation"].mean()),
        }
    )
