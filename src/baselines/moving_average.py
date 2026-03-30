from __future__ import annotations

from dataclasses import dataclass
import math

import pandas as pd


@dataclass
class MovingAverageConfig:
    history_window: int = 15
    horizon: int = 5
    initial_capacity: int = 1
    min_capacity: int = 0


def simulate_moving_average_policy(
    frame: pd.DataFrame,
    *,
    demand_column: str = "required_capacity",
    config: MovingAverageConfig | None = None,
) -> pd.DataFrame:
    """Forecast future capacity from a rolling mean of past observed demand."""

    if config is None:
        config = MovingAverageConfig()

    app_frame = frame.sort_values("minute").reset_index(drop=True).copy()
    demand = app_frame[demand_column].astype(float).tolist()

    forecasts: list[float] = []
    capacities: list[int] = []

    for idx in range(len(app_frame)):
        history_end = idx - config.horizon
        history_start = history_end - config.history_window + 1

        if history_end < 0:
            forecast = float(config.initial_capacity)
        else:
            history_start = max(history_start, 0)
            history = demand[history_start : history_end + 1]
            forecast = sum(history) / float(len(history))

        capacity = max(math.ceil(forecast), config.min_capacity)
        forecasts.append(forecast)
        capacities.append(capacity)

    app_frame["forecast_capacity"] = forecasts
    app_frame["provisioned_capacity"] = capacities
    return app_frame
