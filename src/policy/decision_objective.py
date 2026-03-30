from __future__ import annotations

import numpy as np


def expected_underprovision(demand_samples: np.ndarray, capacity: int) -> float:
    return float(np.maximum(demand_samples - capacity, 0.0).mean())


def expected_tail_underprovision(
    demand_samples: np.ndarray,
    capacity: int,
    *,
    tail_alpha: float = 0.99,
) -> float:
    if len(demand_samples) == 0:
        return 0.0

    threshold = float(np.quantile(demand_samples, tail_alpha))
    tail_samples = demand_samples[demand_samples >= threshold]
    if len(tail_samples) == 0:
        tail_samples = demand_samples

    return float(np.maximum(tail_samples - capacity, 0.0).mean())


def decision_objective(
    capacity: int,
    *,
    demand_samples: np.ndarray,
    previous_capacity: int,
    cost_weight: float,
    underprovision_weight: float,
    oscillation_weight: float,
    tail_risk_weight: float = 0.0,
    tail_alpha: float = 0.99,
) -> float:
    score = (
        cost_weight * float(capacity)
        + underprovision_weight * expected_underprovision(demand_samples, capacity)
        + oscillation_weight * abs(float(capacity) - float(previous_capacity))
    )
    if tail_risk_weight > 0.0:
        score += tail_risk_weight * expected_tail_underprovision(
            demand_samples,
            capacity,
            tail_alpha=tail_alpha,
        )

    return score


def choose_capacity(
    demand_samples: np.ndarray,
    *,
    previous_capacity: int,
    min_capacity: int = 0,
    cost_weight: float = 1.0,
    underprovision_weight: float = 8.0,
    oscillation_weight: float = 0.25,
    candidate_buffer: int = 5,
    tail_risk_weight: float = 0.0,
    tail_alpha: float = 0.99,
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
            tail_risk_weight=tail_risk_weight,
            tail_alpha=tail_alpha,
        )
        if score < best_score:
            best_score = score
            best_capacity = capacity

    return best_capacity, best_score
