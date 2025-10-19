from typing import Dict, Any, List

_DEFAULT_WEIGHTS = {
    # tweak as needed
    "Stakeholder & Partnership Management": 2.0,
    "Change & Transformation Management":   2.0,
    "Leadership Development":               3.0,
}

def leadership_score(emp: Dict[str, Any], weights: Dict[str, float] = None) -> float:
    """Very simple rule-based score on competencies (0-100 scaling)."""
    if weights is None:
        weights = _DEFAULT_WEIGHTS
    score = 0.0
    for c in emp.get("competencies", []):
        score += weights.get(c.get("name",""), 1.0)
    # Normalize to a 0–100-ish scale (heuristic)
    return min(100.0, score * 5.0)
