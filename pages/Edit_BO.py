import streamlit as st
from civ_manager import CivManager
from supabase import create_client, Client

# --- Initialisation ---
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase = create_client(url, key)
cm = CivManager(supabase)

# --- Récupération du BO en cours ---
bo_id = st.session_state.get("edit_bo_id")
if not bo_id:
    st.error("Aucun Build Order sélectionné.")
    st.stop()

bo = cm.get_bo(bo_id)
st.title(f"🛠️ Édition du BO : {bo['titre']}")

# --- Édition des infos générales ---
with st.form("edit_bo_form"):
    titre = st.text_input("Titre", value=bo["titre"])
    description = st.text_area("Description", value=bo["description"])
    submitted = st.form_submit_button("💾 Enregistrer les infos")
    if submitted:
        cm.update_bo(bo_id, titre, description)
        st.success("✅ Informations mises à jour")

st.divider()

# --- Gestion des étapes ---
st.subheader("📋 Étapes du Build Order")

steps = cm.get_bo_steps(bo_id)
for step in steps:
    with st.expander(f"🔹 Étape {step['ordre']} — {step['note'][:40]}"):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            age = st.text_input("Age", value=step["age"], key=f"age_{step['id']}")
        with col2:
            vils = st.text_input("Vils", value=step["vils"], key=f"vils_{step['id']}")
        with col3:
            task = st.text_input("Task", value=step["task"], key=f"task_{step['id']}")
        with col4:
            note = st.text_area("Note", value=step["note"], key=f"note_{step['id']}")
        with col5:
            ordre = st.number_input("Ordre", value=step["ordre"], key=f"ordre_{step['id']}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("💾 Sauvegarder", key=f"save_{step['id']}"):
                cm.update_bo_step(step["id"], age, vils, task, note, ordre)
                st.rerun()
        with c2:
            if st.button("🗑️ Supprimer", key=f"delete_{step['id']}"):
                cm.delete_bo_step(step["id"])
                st.rerun()

# --- Ajout d'une nouvelle étape ---
with st.expander("➕ Ajouter une étape"):
    with st.form("add_step_form"):
        age = st.text_input("Âge")
        vils = st.text_input("Villageois")
        task = st.text_input("Tâche")
        note = st.text_area("Note")
        ordre = st.number_input("Ordre", min_value=1, step=1)
        submitted = st.form_submit_button("Ajouter")
        if submitted:
            cm.insert_bo_step(bo_id, age, vils, task, note, ordre)
            st.success("✅ Étape ajoutée")
            st.rerun()