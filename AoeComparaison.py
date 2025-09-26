import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from civ_manager_sqlite import CivManager

cm = CivManager()

# ---------------------------
# Sidebar: choix mode
# ---------------------------
mode = st.sidebar.radio("Mode", ["Comparateur de civs", "Édition de civ"])

if mode == "Comparateur de civs":
    st.title("⚔️ Comparateur de civilisations")

    civs = cm.list_civs()
    civ1 = st.selectbox("Choisir la première civilisation", civs)
    civ2 = st.selectbox("Choisir la seconde civilisation", civs)

    df = cm.load_all_as_df()
    comp_df = df[df["Civ"].isin([civ1, civ2])].set_index("Civ")[["Early", "Mid", "Late", "Very late"]]
    comp_df = comp_df.astype(int)
    comp_df = comp_df.fillna(0).astype(int)

    st.subheader("Graphique comparatif")
    fig, ax = plt.subplots()
    comp_df.T.plot(kind="line", marker="o", ax=ax)
    ax.set_ylabel("Score")
    st.pyplot(fig)

    st.markdown("---")
    st.subheader("Remarques & Build Orders")
    for civ in [civ1, civ2]:
        data = cm.get_civ(civ)
        st.markdown(f"### {civ}")
        st.write("- " + data.get("remarque","Aucune remarque enregistrée."))
        bo_id = data.get("bo_id")
        if bo_id:
            bo = cm.get_bo(bo_id)
            if bo:
                with st.expander(f"Voir Build Order: {bo[1]}"):
                    st.markdown(bo[3])

elif mode == "Édition de civ":
    st.title("🛠️ Édition d'une civilisation")
    civs = cm.list_civs()
    civ_name = st.selectbox("Choisir une civilisation", civs)

    civ = cm.get_civ(civ_name)
    if civ is None:
        st.warning("Civilisation non trouvée.")
    else:
        st.subheader(f"Édition: {civ_name}")
        cols = st.columns(4)
        early = cols[0].number_input("Early", value=civ["early"], step=1)
        mid = cols[1].number_input("Mid", value=civ["mid"], step=1)
        late = cols[2].number_input("Late", value=civ["late"], step=1)
        very_late = cols[3].number_input("Very late", value=civ["very_late"], step=1)

        remarque = st.text_area("Remarque", value=civ.get("remarque",""))

        bos = cm.list_bos()
        bo_dict = {f"{b[1]} ({b[0]})": b[0] for b in bos}
        bo_choice = st.selectbox("Build Order associé (facultatif)", ["Aucun"] + list(bo_dict.keys()))
        bo_id = bo_dict.get(bo_choice, None) if bo_choice != "Aucun" else None

        if st.button("Sauvegarder"):
            cm.update_civ(civ_name, early, mid, late, very_late, remarque, bo_id)
            st.success("Civilisation mise à jour.")
