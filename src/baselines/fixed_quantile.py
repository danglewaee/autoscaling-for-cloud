from __future__ import annotations

from dataclasses import dataclass
import math

import numpy as np
import pandas as pd


@dataclass
class FixedQuantileConfig:
    history_window: int = 30
    horizon: int = 5
    quantile: float = 0.95
    initial_capacity: int = 1
    min_capacity: int = 0
    target_column: str = "required_capacity"


def simulate_fixed_quantile_policy(
    frame: pd.DataFrame,
    *,
    config: FixedQuantileConfig | None = None,
) -> pd.DataFrame:
    """Provision to a fixed historical quantile of past observed demand."""

    if config is None:
        config = FixedQuantileConfig()

    app_frame = frame.sort_values("minute").reset_index(drop=True).copy()
    values = app_frame[config.target_column].to_numpy(dtype=float)

    quantile_forecasts: list[float] = []
    capacities: list[int] = []
    used_fallback: list[int] = []

    for idx in range(len(app_frame)):
        history_end = idx - config.horizon
        history_start = history_end - config.history_window + 1

        if history_end < 0:
            quantile_value = float(config.initial_capacity)
            fallback = 1
        else:
            history_start = max(history_start, 0)
            history = values[history_start : history_end + 1]
            quantile_value = float(np.quantile(history, config.quantile))
            fallback = 0

        capacity = max(math.ceil(max(quantile_value, 0.0)), config.min_capacity)
        quantile_forecasts.append(quantile_value)
        capacities.append(capacity)
        used_fallback.append(fallback)

    app_frame["forecast_capacity"] = quantile_forecasts
    app_frame["provisioned_capacity"] = capacities
    app_frame["forecast_quantile"] = config.quantile
    app_frame["used_fallback_forecast"] = used_fallback
    return app_frame
