from typing import Dict, List, Any
from core.retrieval_utils import (
    gap_analysis,
    similar_employees,
)
from core.data_loader import load_employee_profiles
from core.embedding_utils import load_embedding_cache
from core.scoring_utils import leadership_score

def recommend_training(emp_id: str, target_role_id: str | None = None) -> Dict[str, Any]:
    """
    Suggests upskilling or training areas for the given employee.
    Uses gap_analysis() to find what skills they lack compared to a target role.
    """
    try:
        profiles = load_employee_profiles()
        emp_profile = next(p for p in profiles if p["employee_id"] == emp_id)
        # For now, just pick the first other employee as "target"
        target_profile = next(p for p in profiles if p["employee_id"] != emp_id)
        gaps = gap_analysis(emp_profile, target_profile)
        return {
            "employee_id": emp_id,
            "target_id": target_profile["employee_id"],
            "missing_skills": gaps[:5],
        }
    except Exception as e:
        return {"employee_id": emp_id, "error": str(e)}


def recommend_team_collabs(emp_id: str, top_k: int = 5) -> Dict[str, Any]:
    """
    Finds potential collaborators or mentors.
    Uses cached embeddings + cosine similarity.
    """
    try:
        cache = load_embedding_cache()
        similar = similar_employees(emp_id, cache, top_k=top_k)
        return {
            "employee_id": emp_id,
            "recommended_collaborators": similar,
        }
    except Exception as e:
        return {"employee": emp_id, "error": str(e)}


def recommend_leadership(emp_id: str) -> Dict[str, Any]:
    """
    Compute leadership score based on competencies and weights.
    """
    try:
        profiles = load_employee_profiles()
        emp_profile = next(p for p in profiles if p.get("employee_id") == emp_id)
        score = leadership_score(emp_profile)
        return {
            "employee_id": emp_id,
            "leadership_score": round(score, 2)
        }
    except Exception as e:
        return {"employee_id": emp_id, "error": str(e)}


if __name__ == "__main__":
    print(recommend_training("EMP-20003"))
    print(recommend_team_collabs("EMP-20003"))
    print(recommend_leadership("EMP-20003"))