import streamlit as st
from components.Card import Card

st.set_page_config(page_title="AOE2 Coach", page_icon="🏰", layout="wide")

st.title("🏰 AOE2 Coach – Tableau de bord")
st.write("Choisis une catégorie pour commencer :")

col1, col2, col3, col4 = st.columns(4)

with col1:
    Card("🆚", "Match-up", "pages/MatchUp.py").render()

with col2:
    Card("🏛️", "Civilisations", "pages/Civilisations.py").render()

with col3:
    Card("🗺️", "Cartes", "pages/Cartes.py").render()

with col4:
    Card("💬", "Remarques", "pages/Remarques.py").render()
