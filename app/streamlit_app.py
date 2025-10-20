import streamlit as st

from core.data_loader import load_employee_profiles
from core.embedding_utils import load_embedding_cache

from app.views.career import render_career_tab
from app.views.chat import render_chat_tab

# ---------- page setup ----------
st.set_page_config(page_title="PathAI – PSA Career Assistant", layout="wide")
st.title("PathAI – PSA Career Assistant")

# ---------- cached data loaders ----------
@st.cache_data(show_spinner=False)
def _profiles():
    return load_employee_profiles()

@st.cache_resource(show_spinner=False)
def _try_load_cache():
    try:
        return load_embedding_cache() 
    except Exception:
        return None

profiles = _profiles()
emb_cache = _try_load_cache()

if not profiles:
    st.error("No profiles found. Check `data/Employee_Profiles.json`.")
    st.stop()

id_to_profile = {p["employee_id"]: p for p in profiles}
labels = [
    f'{p["employee_id"]} — {p.get("employment_info", {}).get("job_title", "")}'
    for p in profiles
]
label_to_id = {lbl: p["employee_id"] for lbl, p in zip(labels, profiles)}

if emb_cache is None:
    st.warning(
        "⚠️ Embedding cache not found. Similarity/mentorship features will be limited.\n\n"
        "Build it once with:\n`python scripts/build_cache.py`"
    )

st.caption("Choose an employee to analyse")
sel = st.selectbox("Select employee", labels, index=0 if labels else None)
emp_id = label_to_id.get(sel)

tab1, tab2 = st.tabs(["🧭 Career Recommender", "💬 Chat with PathAI"])
with tab1:
    render_career_tab(emp_id=emp_id, profiles=profiles, id_to_profile=id_to_profile, emb_cache=emb_cache)

with tab2:
    render_chat_tab(emp_id=emp_id, id_to_profile=id_to_profile, emb_cache=emb_cache)
