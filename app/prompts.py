SYSTEM_PROMPT = (
    "You are PathAI, PSA’s career coach. Be concise (≤6 bullets), kind, and actionable. "
    "Ground advice in the employee profile and recommendation summary. "
    "If information is missing, acknowledge it and suggest realistic next steps. "
    "Never make up company-specific policies."
)

def _skinny_profile(emp: dict) -> dict:
    ei = emp.get("employment_info", {})
    return {
        "id": emp.get("employee_id"),
        "name": emp.get("name", ei.get("full_name", "")),
        "title": ei.get("job_title", ""),
        "department": ei.get("department", ""),
        "skills": [s.get("skill_name") for s in emp.get("skills", [])][:15],
        "competencies": [c.get("name") for c in emp.get("competencies", [])][:10],
    }

def build_messages(emp_profile: dict, user_q: str, rec_summary: str) -> list[dict]:
    context = {
        "employee": _skinny_profile(emp_profile),
        "summary": rec_summary,
    }
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": f"Context:\n{context}"},
        {"role": "user", "content": user_q.strip()},
    ]
