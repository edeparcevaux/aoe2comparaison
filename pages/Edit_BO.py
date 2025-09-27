import streamlit as st
import sqlite3
from civ_manager_sqlite import CivManager



cm = CivManager()

if "edit_bo_id" not in st.session_state:
    st.error("⚠️ Aucun BO sélectionné")
else:
    bo_id = st.session_state["edit_bo_id"]
    titre, description = cm.get_bo(bo_id)

    st.title(f"✏️ Modifier BO : {titre}")
    with st.form("edit_bo_form"):
        new_titre = st.text_input("Titre", titre)
        new_desc = st.text_area("Description", description)
        submitted = st.form_submit_button("Enregistrer")
        if submitted:
            cm.update_bo(bo_id, new_titre, new_desc)
            st.success("✅ BO mis à jour")