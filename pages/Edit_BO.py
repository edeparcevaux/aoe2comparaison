import streamlit as st
from civ_manager import CivManager

cm = CivManager()

if "edit_bo_id" not in st.session_state:
    st.error("⚠️ Aucun BO sélectionné")
else:
    bo_id = st.session_state["edit_bo_id"]
    bo = cm.get_bo(bo_id)

    if bo is None:
        st.error("❌ BO introuvable")
    else:
        st.title(f"✏️ Modifier BO : {bo['titre']}")

        with st.form("edit_bo_form"):
            new_titre = st.text_input("Titre", bo["titre"])
            new_desc = st.text_area("Description", bo["description"])
            submitted = st.form_submit_button("Enregistrer")

            if submitted:
                cm.update_bo(bo["id"], new_titre, new_desc)
                st.success("✅ BO mis à jour")