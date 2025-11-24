import streamlit as st

def civ_stats_section(civ, mode):
    st.subheader(f"Statistiques {mode}")
    st.write(civ.get("stats", {}).get(mode, "Pas de données"))