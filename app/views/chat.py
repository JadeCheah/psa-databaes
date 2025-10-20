import hashlib
import streamlit as st
from recommenders.recommendation_engine import (
    recommend_training,
    recommend_team_collabs,
    recommend_leadership,
)
from app.prompts import build_messages
from app.services.llm_client import call_llm, llm_is_configured

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
    if "last_fp" not in st.session_state:
        st.session_state.last_fp = None

    use_llm = st.toggle("Use LLM (Azure OpenAI)", value=True,
                        help="Turn off for deterministic summary only.")
    # mode badge
    st.write(("🧠 **LLM mode**" if (use_llm and llm_is_configured()) else "🧮 **Deterministic mode**"))

    # Use a form to avoid duplicate submits on rerun
    with st.form("chat_form", clear_on_submit=False):
        q = st.text_input("Your question", placeholder="What should I learn next to move into architecture?")
        submitted = st.form_submit_button("Ask", use_container_width=True)

    if submitted:
        if not q.strip():
            st.info("Type a question first.")
            return

        # dedupe: fingerprint = employee + question + mode
        fp_src = f"{emp_id}|{q.strip()}|{'llm' if (use_llm and llm_is_configured()) else 'det'}"
        fp = hashlib.sha256(fp_src.encode()).hexdigest()
        if fp == st.session_state.last_fp:
            # same submission already processed on the previous rerun
            return
        st.session_state.last_fp = fp

        # default deterministic answer
        rec_summary = _summarise_no_llm(emp_id)
        answer = rec_summary + f"\n_Your question:_ {q}"

        # try LLM if enabled & configured
        if use_llm and llm_is_configured():
            emp = id_to_profile[emp_id]
            msgs = build_messages(emp_profile=emp, user_q=q, rec_summary=rec_summary)
            with st.spinner("PathAI is thinking…"):
                try:
                    answer = call_llm(messages=msgs)
                except Exception as e:
                    st.error(f"LLM call failed, showing deterministic summary: {e}")

        st.session_state.chat.append(("you", q))
        st.session_state.chat.append(("pathai", answer))

    # render last few turns
    for role, text in st.session_state.chat[-8:]:
        if role == "you":
            st.markdown(f"**You:** {text}")
        else:
            st.markdown(text)
