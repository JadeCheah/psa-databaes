import streamlit as st

from recommenders.recommendation_engine import (
    recommend_training,
    recommend_team_collabs,
    recommend_leadership,
)
from core.retrieval_utils import similar_employees, gap_analysis
from app.components import bullets, mentors_table, employee_header

def render_career_tab(emp_id: str, profiles: list[dict], id_to_profile: dict[str, dict], emb_cache):
    emp = id_to_profile[emp_id]

    left, right = st.columns([1, 2], vertical_alignment="top")
    with left:
        employee_header(emp)

    with right:
        if st.button("Get Suggestions", type="primary", use_container_width=True):
            with st.spinner("Generating suggestions..."):
                # 1) leadership
                lead = recommend_leadership(emp_id)  # {'leadership_score': float}
                score = float(lead.get("leadership_score", 0.0))

                # 2) training / missing skills
                train = recommend_training(emp_id)   # {'missing_skills': [...]}
                missing = (train or {}).get("missing_skills") or []

                # 3) collaborators
                recos = []
                try:
                    if emb_cache:
                        collab = recommend_team_collabs(emp_id) or {}
                        recos = collab.get("recommended_collaborators") or []
                except Exception:
                    recos = []

            # ---- render results (with guardrails) ----
            st.metric("Leadership Score", f"{score:.1f}")

            st.write("**Upskilling / Missing skills (max 5):**")
            bullets(missing, max_items=5)

            st.write("**Suggested collaborators / mentors (Top 5):**")
            mentors_table(recos, top_k=5)

    # -------- Exploratory tools --------
    st.divider()
    st.subheader("Explore Similarity & Gaps")

    c1, c2 = st.columns(2)
    with c1:
        k = st.slider("Top-K similar employees", 1, 10, 5)
        if st.button("Find Similar", use_container_width=True, key="btn_sim"):
            if not emb_cache:
                st.info("Similarity requires the embedding cache. Run `python scripts/build_cache.py`.")
            else:
                with st.spinner("Finding similar employees…"):
                    sims = similar_employees(emp_id, emb_cache, top_k=k)  # list[(id, score)]
                mentors_table(sims, top_k=k)

    with c2:
        # a second selectbox to compare with
        other_options = [p["employee_id"] for p in profiles if p["employee_id"] != emp_id]
        other_id = st.selectbox("Compare gaps against", other_options, index=0 if other_options else None)
        if st.button("Run Gap Analysis", use_container_width=True, key="btn_gap"):
            if not other_id:
                st.info("Pick another employee to compare.")
            else:
                with st.spinner("Computing skill gaps…"):
                    a = id_to_profile[emp_id]
                    b = id_to_profile[other_id]
                    gaps = gap_analysis(a, b)  # skills in B that A lacks
                st.write("**Skills to develop (max 8):**")
                bullets(gaps, max_items=8)
