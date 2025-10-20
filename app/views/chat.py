import streamlit as st
from recommenders.recommendation_engine import (
    recommend_training,
    recommend_team_collabs,
    recommend_leadership,
)

def _summarise_no_llm(emp_id: str) -> str:
    lead = recommend_leadership(emp_id).get("leadership_score", 0.0)
    train = recommend_training(emp_id).get("missing_skills", [])[:3]
    collabs = (recommend_team_collabs(emp_id) or {}).get("recommended_collaborators", [])[:2]
    return "\n".join([
        f"**Summary for {emp_id}**",
        f"- Leadership score: **{lead:.1f}**",
        f"- Focus upskilling on: {', '.join(train) if train else 'no major gaps detected'}",
        f"- Potential mentors: {', '.join([rid for rid, _ in collabs]) if collabs else 'none found'}",
        "Next step: prioritise 1–2 skills above and pair with a mentor for a mini-project.",
    ])

def render_chat_tab(emp_id: str, id_to_profile: dict[str, dict], emb_cache):
    st.caption("Ask about next steps, upskilling focus, or collaboration ideas.")

    if "chat" not in st.session_state:
        st.session_state.chat = []

    q = st.text_input("Your question", placeholder="What should I learn next to move into architecture?")

    if st.button("Ask", use_container_width=True):
        if not q.strip():
            st.info("Type a question first.")
            return

        rec_summary = _summarise_no_llm(emp_id)
        ans = rec_summary + f"\n_Your question:_ {q}"

        st.session_state.chat.append(("you", q))
        st.session_state.chat.append(("pathai", ans))

    for role, text in st.session_state.chat[-8:]:
        if role == "you":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(text)
