from __future__ import annotations

import math
from typing import Iterable


def _to_float_list(values: Iterable[float]) -> list[float]:
    return [float(v) for v in values]


def psi(expected: Iterable[float], actual: Iterable[float], bins: int = 10, eps: float = 1e-6) -> float:
    expected_vals = _to_float_list(expected)
    actual_vals = _to_float_list(actual)

    if not expected_vals or not actual_vals:
        return 0.0

    min_v = min(expected_vals)
    max_v = max(expected_vals)
    if min_v == max_v:
        return 0.0

    width = (max_v - min_v) / bins
    edges = [min_v + i * width for i in range(bins + 1)]

    def bucketize(values: list[float]) -> list[int]:
        counts = [0] * bins
        for value in values:
            if value <= edges[0]:
                idx = 0
            elif value >= edges[-1]:
                idx = bins - 1
            else:
                idx = int((value - min_v) / width)
                idx = min(max(idx, 0), bins - 1)
            counts[idx] += 1
        return counts

    exp_counts = bucketize(expected_vals)
    act_counts = bucketize(actual_vals)

    exp_total = sum(exp_counts) or 1
    act_total = sum(act_counts) or 1

    score = 0.0
    for e_count, a_count in zip(exp_counts, act_counts):
        e_pct = max(e_count / exp_total, eps)
        a_pct = max(a_count / act_total, eps)
        score += (a_pct - e_pct) * math.log(a_pct / e_pct)

    return float(score)
