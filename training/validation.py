from __future__ import annotations


def should_promote_model(f1_score_value: float, threshold: float) -> bool:
    return f1_score_value >= threshold
