from __future__ import annotations

import numpy as np


def expected_underprovision(demand_samples: np.ndarray, capacity: int) -> float:
    return float(np.maximum(demand_samples - capacity, 0.0).mean())


def decision_objective(
    capacity: int,
    *,
    demand_samples: np.ndarray,
    previous_capacity: int,
    cost_weight: float,
    underprovision_weight: float,
    oscillation_weight: float,
) -> float:
    return (
        cost_weight * float(capacity)
        + underprovision_weight * expected_underprovision(demand_samples, capacity)
        + oscillation_weight * abs(float(capacity) - float(previous_capacity))
    )


def choose_capacity(
    demand_samples: np.ndarray,
    *,
    previous_capacity: int,
    min_capacity: int = 0,
    cost_weight: float = 1.0,
    underprovision_weight: float = 8.0,
    oscillation_weight: float = 0.25,
    candidate_buffer: int = 5,
) -> tuple[int, float]:
    max_sample = int(np.ceil(float(demand_samples.max()))) if len(demand_samples) else 0
    max_candidate = max(max_sample + candidate_buffer, previous_capacity + candidate_buffer, min_capacity)

    best_capacity = min_capacity
    best_score = float("inf")

    for capacity in range(min_capacity, max_candidate + 1):
        score = decision_objective(
            capacity,
            demand_samples=demand_samples,
            previous_capacity=previous_capacity,
            cost_weight=cost_weight,
            underprovision_weight=underprovision_weight,
            oscillation_weight=oscillation_weight,
        )
        if score < best_score:
            best_score = score
            best_capacity = capacity

    return best_capacity, best_score
