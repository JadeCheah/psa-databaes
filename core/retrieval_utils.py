from typing import List, Dict, Any
import numpy as np
from .embedding_utils import load_embedding_cache, cosine_sim

# ---- helpers over the profiles structure ----

def _skills_set(emp: Dict[str, Any]) -> set:
    return {s.get("skill_name","").strip() for s in emp.get("skills", []) if s.get("skill_name")}

def search_skills(profiles: List[Dict[str, Any]], keyword: str) -> List[Dict[str, Any]]:
    """Return employees whose explicit skills contain the keyword (case-insensitive)."""
    k = keyword.lower()
    return [
        p for p in profiles
        if any(k in (s.get("skill_name","").lower()) for s in p.get("skills", []))
    ]

def similar_employees(emp_id: str, cache: Dict[str, Any], top_k: int = 5):
    """Rank other employees by cosine similarity of cached embeddings."""
    vecs = cache["vectors"]
    if emp_id not in vecs:
        raise KeyError(f"Employee id {emp_id} not in embedding cache.")
    q = vecs[emp_id]
    sims = []
    for other_id, v in vecs.items():
        if other_id == emp_id: continue
        sims.append((other_id, cosine_sim(q, v)))
    sims.sort(key=lambda x: x[1], reverse=True)
    return sims[:top_k]

def gap_analysis(emp_a: Dict[str, Any], emp_b: Dict[str, Any]) -> List[str]:
    """Skills in B that A does not have (simple set diff)."""
    a = _skills_set(emp_a)
    b = _skills_set(emp_b)
    return sorted(list(b - a))
