from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class ReactivePolicyConfig:
    initial_capacity: int = 1
    min_capacity: int = 0
    scale_up_delay: int = 1
    scale_down_delay: int = 1
    downscale_stabilization: int = 5


def simulate_reactive_policy(
    frame: pd.DataFrame,
    *,
    demand_column: str = "required_capacity",
    config: ReactivePolicyConfig | None = None,
) -> pd.DataFrame:
    """Simulate a simple delayed reactive autoscaler on one app trace."""

    if config is None:
        config = ReactivePolicyConfig()

    app_frame = frame.sort_values("minute").reset_index(drop=True).copy()
    demand = app_frame[demand_column].astype(int).tolist()

    capacities: list[int] = []
    current_capacity = max(config.initial_capacity, config.min_capacity)
    last_scale_minute: int | None = None

    for idx in range(len(app_frame)):
        if idx >= config.scale_up_delay:
            delayed_up_demand = demand[idx - config.scale_up_delay]
        else:
            delayed_up_demand = current_capacity

        if idx >= config.scale_down_delay:
            delayed_down_demand = demand[idx - config.scale_down_delay]
        else:
            delayed_down_demand = current_capacity

        desired_up = max(int(delayed_up_demand), config.min_capacity)
        desired_down = max(int(delayed_down_demand), config.min_capacity)

        if desired_up > current_capacity:
            current_capacity = desired_up
            last_scale_minute = idx
        elif desired_down < current_capacity:
            stable_enough = (
                last_scale_minute is None
                or idx - last_scale_minute >= config.downscale_stabilization
            )
            if stable_enough:
                current_capacity = desired_down
                last_scale_minute = idx

        capacities.append(current_capacity)

    app_frame["provisioned_capacity"] = capacities
    return app_frame
