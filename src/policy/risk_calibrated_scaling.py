from __future__ import annotations

from dataclasses import dataclass
import math

import pandas as pd

from src.calibration.interval_calibration import ResidualIntervalCalibrator
from src.policy.decision_objective import choose_capacity


@dataclass
class RiskCalibratedConfig:
    initial_capacity: int = 1
    min_capacity: int = 0
    cost_weight: float = 1.0
    underprovision_weight: float = 8.0
    oscillation_weight: float = 0.25
    candidate_buffer: int = 5
    tail_risk_weight: float = 0.0
    tail_alpha: float = 0.99
    reactive_guard_lookback: int = 0
    reactive_guard_factor: float = 1.0
    reactive_guard_buffer: int = 0


def simulate_risk_calibrated_policy(
    frame: pd.DataFrame,
    *,
    calibrator: ResidualIntervalCalibrator,
    config: RiskCalibratedConfig | None = None,
    prediction_column: str = "forecast_capacity",
) -> pd.DataFrame:
    if config is None:
        config = RiskCalibratedConfig()

    app_frame = frame.sort_values("minute").reset_index(drop=True).copy()

    previous_capacity = max(config.initial_capacity, config.min_capacity)
    capacities: list[int] = []
    objectives: list[float] = []
    interval_low: list[float] = []
    interval_high: list[float] = []
    reactive_guard_capacity: list[int] = []
    guard_activated: list[int] = []

    for row_idx, row in enumerate(app_frame.itertuples(index=False)):
        prediction = float(getattr(row, prediction_column))
        samples = calibrator.sample_demand(prediction)
        low, high = calibrator.interval(prediction)
        chosen_capacity, objective_value = choose_capacity(
            samples,
            previous_capacity=previous_capacity,
            min_capacity=config.min_capacity,
            cost_weight=config.cost_weight,
            underprovision_weight=config.underprovision_weight,
            oscillation_weight=config.oscillation_weight,
            candidate_buffer=config.candidate_buffer,
            tail_risk_weight=config.tail_risk_weight,
            tail_alpha=config.tail_alpha,
        )
        base_capacity = chosen_capacity

        guard_capacity = config.min_capacity
        if config.reactive_guard_lookback > 0 and row_idx > 0:
            history_start = max(0, row_idx - config.reactive_guard_lookback)
            recent_observed = float(
                app_frame.iloc[history_start:row_idx]["required_capacity"].max()
            )
            guard_capacity = max(
                config.min_capacity,
                int(
                    math.ceil(
                        recent_observed * config.reactive_guard_factor
                        + config.reactive_guard_buffer
                    )
                ),
            )
            chosen_capacity = max(chosen_capacity, guard_capacity)

        capacities.append(chosen_capacity)
        objectives.append(objective_value)
        interval_low.append(low)
        interval_high.append(high)
        reactive_guard_capacity.append(guard_capacity)
        guard_activated.append(int(guard_capacity > base_capacity))
        previous_capacity = chosen_capacity

    app_frame["interval_low"] = interval_low
    app_frame["interval_high"] = interval_high
    app_frame["provisioned_capacity"] = capacities
    app_frame["decision_objective"] = objectives
    app_frame["reactive_guard_capacity"] = reactive_guard_capacity
    app_frame["guard_activated"] = guard_activated
    return app_frame
