from core import (
    load_employee_profiles,
    load_embedding_cache,
    search_skills,
    similar_employees,
    gap_analysis,
    leadership_score,
)

def get_emp(profiles, emp_id):
    return next(p for p in profiles if p["employee_id"] == emp_id)

def main():
    print("Loading data…")
    profiles = load_employee_profiles()
    cache = load_embedding_cache()
    print(f"Profiles: {len(profiles)} | Cached embeddings: {len(cache['vectors'])}")

    # 1) Skill search by declared skill keyword
    print("\n[ search_skills('Automation') ]")
    hits = search_skills(profiles, "Automation")
    for p in hits[:5]:
        role = p.get("employment_info", {}).get("job_title", "")
        print("  -", p["employee_id"], role)

    # 2) Similar employees (nearest neighbors in embedding space)
    seed_id = profiles[0]["employee_id"]
    print(f"\n[ similar_employees('{seed_id}', top_k=3) ]")
    sims = similar_employees(seed_id, cache, top_k=3)
    for eid, score in sims:
        print(f"  - {eid} (sim={score:.3f})")

    # 3) Gap analysis: skills in B not in A
    a_id, b_id = profiles[0]["employee_id"], profiles[1]["employee_id"]
    A, B = get_emp(profiles, a_id), get_emp(profiles, b_id)
    print(f"\n[ gap_analysis({a_id} -> {b_id}) ]")
    gaps = gap_analysis(A, B)
    for s in gaps[:10]:
        print("  -", s)
    if len(gaps) > 10:
        print(f"  (+{len(gaps)-10} more)")

    # 4) Simple leadership score
    print(f"\n[ leadership_score({a_id}) ]")
    print("  ->", leadership_score(A))

if __name__ == "__main__":
    main()
