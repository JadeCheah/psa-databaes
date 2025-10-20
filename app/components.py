import streamlit as st

def bullets(items, max_items=5):
    items = (items or [])[:max_items]
    if not items:
        st.info("Looks aligned — consider leadership or soft-skill development.")
        return
    st.markdown("\n".join([f"- {it}" for it in items]))

def mentors_table(recos, top_k=5):
    recos = (recos or [])[:top_k]
    if not recos:
        st.info("No close matches in cache.")
        return
    st.dataframe(
        [{"Rank": i + 1, "Employee ID": rid, "Similarity": round(sim, 3)}
         for i, (rid, sim) in enumerate(recos)],
        hide_index=True,
        use_container_width=True
    )

def employee_header(emp):
    info = emp.get("employment_info", {})
    st.subheader("Current Role")
    st.write(
        f"**{info.get('job_title', '—')}**  \n"
        f"{info.get('department', '—')}  \n"
        f"{info.get('unit', '')}"
    )
