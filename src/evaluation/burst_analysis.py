from __future__ import annotations

import numpy as np
import pandas as pd


def mark_burst_minutes(
    frame: pd.DataFrame,
    *,
    demand_column: str = "required_capacity",
    rolling_window: int = 30,
    burst_quantile: float = 0.90,
    burst_multiplier: float = 2.0,
    min_jump: float = 1.0,
) -> pd.DataFrame:
    marked = []

    for app, app_frame in frame.groupby("app", sort=False):
        ordered = app_frame.sort_values("minute").reset_index(drop=True).copy()
        demand = ordered[demand_column].astype(float)
        rolling_baseline = (
            demand.shift(1)
            .rolling(rolling_window, min_periods=max(5, rolling_window // 4))
            .mean()
            .fillna(0.0)
        )
        app_quantile = float(demand.quantile(burst_quantile))
        app_threshold = max(app_quantile, 1.0)

        ordered["rolling_baseline"] = rolling_baseline
        ordered["is_burst"] = (
            (demand >= app_threshold)
            & (demand >= rolling_baseline * burst_multiplier)
            & ((demand - rolling_baseline) >= min_jump)
        ).astype(int)

        burst_start = (ordered["is_burst"] == 1) & (
            ordered["is_burst"].shift(1, fill_value=0) == 0
        )
        ordered["burst_episode_start"] = burst_start.astype(int)
        ordered["burst_episode_id"] = np.where(
            ordered["is_burst"] == 1,
            burst_start.cumsum(),
            0,
        )
        marked.append(ordered)

    return pd.concat(marked, ignore_index=True)


def summarize_burst_subset(frame: pd.DataFrame) -> pd.Series:
    burst = frame[frame["is_burst"] == 1].copy()
    if burst.empty:
        return pd.Series(
            {
                "burst_steps": 0,
                "burst_fraction": 0.0,
                "burst_episodes": 0,
                "mean_cost": np.nan,
                "sla_violation_rate": np.nan,
                "mean_underprovision": np.nan,
                "mean_overprovision": np.nan,
                "mean_oscillation": np.nan,
            }
        )

    return pd.Series(
        {
            "burst_steps": int(len(burst)),
            "burst_fraction": float(len(burst) / len(frame)),
            "burst_episodes": int(burst["burst_episode_start"].sum()),
            "mean_cost": float(burst["cost"].mean()) if "cost" in burst.columns else np.nan,
            "sla_violation_rate": float(burst["sla_violation"].mean())
            if "sla_violation" in burst.columns
            else np.nan,
            "mean_underprovision": float(burst["underprovision"].mean())
            if "underprovision" in burst.columns
            else np.nan,
            "mean_overprovision": float(burst["overprovision"].mean())
            if "overprovision" in burst.columns
            else np.nan,
            "mean_oscillation": float(burst["oscillation"].mean())
            if "oscillation" in burst.columns
            else np.nan,
        }
    )
