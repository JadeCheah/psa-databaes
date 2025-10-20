import streamlit as st
from recommenders.recommendation_engine import (
    recommend_training,
    recommend_team_collabs,
    recommend_leadership,
)
from services.llm_client import call_llm

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
    
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "You are PathAI, a concise internal career coach. "
                    "Give practical next steps, concrete courses/skills, and collaboration ideas."
                ),
            }
        ]

    q = st.text_input("Your question", placeholder="What should I learn next to move into architecture?")

    if st.button("Ask", use_container_width=True):
        if not q.strip():
            st.info("Type a question first.")
            return

        # Build per-turn context
        rec_summary = _summarise_no_llm(emp_id)
        profile = id_to_profile.get(emp_id, {})
        name = profile.get("name", emp_id)
        context_msg = {
            "role": "system",
            "content": f"Employee context for {name} (id={emp_id}):\n{rec_summary}"
        }

        # history + context + new user question
        messages = st.session_state.messages + [context_msg, {"role": "user", "content": q}]

        try:
            reply = call_llm(messages)
        except Exception as e:
            st.error(f"LLM error: {e}")
            return

        st.session_state.chat.append(("you", q))
        st.session_state.chat.append(("pathai", reply))

        # persist logical LLM history (don’t persist the per-turn context)
        st.session_state.messages.extend([
            {"role": "user", "content": q},
            {"role": "assistant", "content": reply},
        ])

    # --- RENDER CHAT HISTORY ---

    # group messages into exchanges: [("you", q), ("pathai", reply)]
    exchanges = []
    i = 0
    chat = st.session_state.chat
    while i < len(chat):
        if i + 1 < len(chat) and chat[i][0] == "you" and chat[i+1][0] == "pathai":
            exchanges.append(chat[i:i+2])
            i += 2
        else:
            exchanges.append([chat[i]])
            i += 1
    
    # show the last N exchanges, newest first
    N = 5  # tweak how many exchanges to show
    recent = list(reversed(exchanges[-N:]))

    if recent:
        st.caption("Most recent (top)")

    for idx, ex in enumerate(recent):
        if idx > 0:
            st.divider()  # horizontal line between exchanges
        for role, text in ex:
            if role == "you":
                st.markdown(f"**You:** {text}")
            else:
                st.markdown(text)

