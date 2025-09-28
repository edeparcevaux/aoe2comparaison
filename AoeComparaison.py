import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from civ_manager_sqlite import CivManager

cm = CivManager()

# ---------------------------
# Sidebar: choix mode
# ---------------------------
mode = st.sidebar.radio("Mode", ["Comparateur de civs", "Édition de civ", "BO"])


# ---------------------------
# Mode Comparateur
# ---------------------------
if mode == "Comparateur de civs":
    st.title("⚔️ Comparateur de civilisations")

    civs = cm.list_civs()  # [(id, nom), ...]
    civ1 = st.sidebar.selectbox(
        "Civ 1",
        civs,
        format_func=lambda x: x[1],
        index=[c[1] for c in civs].index("Vikings")
    )
    civ2 = st.sidebar.selectbox(
        "Civ 2",
        civs,
        format_func=lambda x: x[1],
        index=[c[1] for c in civs].index("Malais")
    )

    # DataFrame avec scores
    df = cm.load_all_as_df()
    comp_df = df[df["Civ"].isin([civ1[1], civ2[1]])].set_index("Civ")[["Early", "Mid", "Late", "Very late"]]
    comp_df = comp_df.fillna(0).astype(int)

    with st.expander("📊 Graphique comparatif"):
        col1, col2 = st.columns([2,1])
        with col1:
            st.subheader("Graphique comparatif")
            fig, ax = plt.subplots(figsize=(4,2.5))
            comp_df.T.plot(kind="line", marker="o", ax=ax)
            ax.set_ylabel("Score")
            st.pyplot(fig)
        with col2:
            st.info("📊 Comparaison simplifiée")

    # --- Remarques & BO
    st.markdown("---")
    st.subheader("Remarques & Build Orders")

    cols = st.columns(2)  # 2 colonnes côte à côte

    for i, (civ_id, civ_name) in enumerate([civ1, civ2]):
        with cols[i]:
            st.markdown(f"### {civ_name}")

            # Remarque
            data = cm.get_civ(civ_id)
            st.write("**Remarques :**")
            st.write(data.get("remarque", "Aucune remarque enregistrée."))

            st.write("---")
            # BO
            st.write("**Build Orders :**")
            civ_bos = cm.get_civ_bos(civ_id)
            if civ_bos:
                for bo_id, titre, desc, ordre in civ_bos:
                    with st.expander(f"BO {ordre}: {titre}"):
                        st.markdown(desc)
            else:
                st.info("Aucun BO associé.")

# ---------------------------
# Mode Édition de civ
# ---------------------------
elif mode == "Édition de civ":
    st.title("🛠️ Édition d'une civilisation")
    civs = cm.list_civs()  # [(id, nom), ...]
    if not civs:
        st.warning("Aucune civilisation en base.")
    else:
        civ_selection = st.selectbox("Choisir une civilisation", civs, format_func=lambda x: x[1])
        civ_id, civ_name = civ_selection

        civ = cm.get_civ(civ_id)
        if civ is None:
            st.warning("Civilisation non trouvée.")
        else:
            st.subheader(f"Édition: {civ['nom']}")
            cols = st.columns(4)
            early = cols[0].number_input("Early", value=civ["early"], step=1)
            mid = cols[1].number_input("Mid", value=civ["mid"], step=1)
            late = cols[2].number_input("Late", value=civ["late"], step=1)
            very_late = cols[3].number_input("Very late", value=civ["very_late"], step=1)

            remarque = st.text_area("Remarque", value=civ.get("remarque", ""))

            # --- Gestion des BO associés ---
            st.subheader("📜 Build Orders associés")
            civ_bos = cm.get_civ_bos(civ_id)
            if not civ_bos:
                st.info("Aucun BO associé.")
            else:
                for bo_id, titre, desc, ordre in civ_bos:
                    col1, col2, col3 = st.columns([3, 1, 1])
                    col1.markdown(f"**{titre}**  — ordre {ordre}")
                    # Up / Down / Remove — protéger par try/except
                    if col2.button("⬆️", key=f"up_{bo_id}"):
                        try:
                            cm.add_bo_to_civ(civ_id, bo_id, ordre-1)
                            st.success("Ordre mis à jour")
                        except Exception as e:
                            st.error(f"Erreur: {e}")
                        st.rerun()
                    if col2.button("⬇️", key=f"down_{bo_id}"):
                        try:
                            cm.add_bo_to_civ(civ_id, bo_id, ordre+1)
                            st.success("Ordre mis à jour")
                        except Exception as e:
                            st.error(f"Erreur: {e}")
                        st.rerun()
                    if col3.button("❌", key=f"remove_{bo_id}"):
                        try:
                            cm.remove_bo_from_civ(civ_id, bo_id)
                            st.success("Association supprimée")
                        except Exception as e:
                            st.error(f"Erreur: {e}")
                        st.rerun()

            # --- Ajout d'un nouveau BO (via form pour éviter doubles clics) ---
            st.subheader("➕ Associer un nouveau BO")
            all_bos = cm.get_bos()  # [(id, titre), ...]
            used_ids = [b[0] for b in civ_bos]
            available_bos = [b for b in all_bos if b[0] not in used_ids]

            if available_bos:
                bo_map = {f"{b[1]} (id={b[0]})": b[0] for b in available_bos}
                with st.form("assoc_bo_form"):
                    choice = st.selectbox("Sélectionner un BO", ["Aucun"] + list(bo_map.keys()))
                    submit_assoc = st.form_submit_button("Associer ce BO")
                    if submit_assoc:
                        if choice != "Aucun":
                            bo_id_to_link = bo_map[choice]
                            try:
                                cm.add_bo_to_civ(civ_id, bo_id_to_link, ordre=None)
                                st.success("BO associé à la civilisation ✅")
                            except Exception as e:
                                st.error(f"Erreur lors de l'association: {e}")
                            st.rerun()
            else:
                st.info("Tous les BO sont déjà associés à cette civ.")

            # --- Sauvegarde des infos de la civ ---
            if st.button("💾 Sauvegarder infos civ"):
                try:
                    cm.update_civ(civ_id, civ_name, early, mid, late, very_late, remarque)
                    st.success("Civilisation mise à jour ✅")
                except Exception as e:
                    st.error(f"Erreur de sauvegarde: {e}")

# ---------------------------
# Mode BO
# ---------------------------
elif mode == "BO":
    st.title("📜 Liste des Build Orders")

    bos = cm.get_bos()
    for bo_id, titre in bos:
        if st.button(f"✏️ {titre}", key=f"edit_{bo_id}"):
            st.session_state["edit_bo_id"] = bo_id
            st.switch_page("pages/Edit_BO.py")  # page suivante

    with st.expander("➕ Créer un nouveau BO"):
        with st.form("new_bo_form"):
            titre = st.text_input("Titre")
            description = st.text_area("Description")
            submitted = st.form_submit_button("Créer")
            if submitted and titre.strip():
                cm.insert_bo(titre, description)
                st.success("✅ BO créé avec succès")
                st.rerun()
