import streamlit as st
import matplotlib.pyplot as plt
from civ_manager_sqlite import CivManager
import pandas as pd

cm = CivManager()

st.title("⚔️ Gestion & Comparaison des civilisations")

# Choix de la page
page = st.sidebar.selectbox("Page", ["Comparateur", "Édition"])

if page == "Comparateur":
    civs = cm.list_civs()
    civ1 = st.selectbox("Choisir la première civilisation", civs, index=0 if civs else None)
    civ2 = st.selectbox("Choisir la seconde civilisation", civs, index=1 if len(civs) > 1 else None)

    if civ1 and civ2:
        df = cm.load_all_as_df()
        comp_df = df[df["nom"].isin([civ1, civ2])].set_index("nom")[["early","mid","late","very_late"]]

        st.subheader("📊 Graphique comparatif")
        fig, ax = plt.subplots()
        comp_df.T.plot(kind="line", marker="o", ax=ax)
        ax.set_ylabel("Score")
        ax.set_xlabel("Phase du jeu")
        ax.set_title(f"Comparaison : {civ1} vs {civ2}")
        st.pyplot(fig)

        st.subheader("📋 Détails")
        for civ in [civ1, civ2]:
            civ_data = cm.get_civ(civ)
            if civ_data:
                st.markdown(f"### {civ_data['nom']}")
                st.table({
                    "Early":[civ_data["early"]],
                    "Mid":[civ_data["mid"]],
                    "Late":[civ_data["late"]],
                    "Very late":[civ_data["very_late"]],
                })
                if civ_data["remarque"]:
                    st.info(f"💡 Remarque : {civ_data['remarque']}")

elif page == "Édition":
    civs = cm.list_civs()
    civ_selected = st.selectbox("Choisir une civilisation à éditer", civs)
    civ_data = cm.get_civ(civ_selected)

    if civ_data:
        st.subheader(f"Édition : {civ_data['nom']}")

        # Édition des scores
        col1, col2, col3, col4 = st.columns(4)
        early = col1.number_input("Early", value=civ_data["early"], min_value=0, max_value=100)
        mid = col2.number_input("Mid", value=civ_data["mid"], min_value=0, max_value=100)
        late = col3.number_input("Late", value=civ_data["late"], min_value=0, max_value=100)
        very_late = col4.number_input("Very late", value=civ_data["very_late"], min_value=0, max_value=100)

        # Édition des remarques
        remarque = st.text_area("Remarques", value=civ_data["remarque"])

        if st.button("💾 Sauvegarder"):
            cm.save_civ({
                "nom": civ_selected,
                "early": early,
                "mid": mid,
                "late": late,
                "very_late": very_late,
                "remarque": remarque
            })
            st.success(f"Civilisation {civ_selected} sauvegardée !")
