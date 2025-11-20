import streamlit as st
from civ_manager import CivManager

from components.SelectCiv import SelectCiv
from components.SelectMap import SelectMap
from components.PowerGraph import PowerGraph
from components.WinrateBox import WinrateBox
from components.CommentaireBox import CommentaireBox

cm = CivManager()

st.title("🆚 Match-up 1v1")

# ---------------------
# 1. Sélection Civ / Carte
# ---------------------
col1, col2, col3 = st.columns(3)

with col1:
    civ1 = SelectCiv(cm, "civ1").render("Civilisation 1")

with col2:
    civ2 = SelectCiv(cm, "civ2").render("Civilisation 2")

with col3:
    carte = SelectMap(cm, "map").render("Carte")

st.markdown("---")

# ---------------------
# 2. Graphique de puissance
# ---------------------
st.subheader("📈 Comparaison des forces par phase de jeu")
PowerGraph(cm).render(civ1[0], civ2[0])

st.markdown("---")

# ---------------------
# 3. Winrate
# ---------------------
st.subheader("🎯 Probabilité de victoire")
WinrateBox().render(civ1[1], civ2[1])

st.markdown("---")

# ---------------------
# 4. Commentaires
# ---------------------
col1, col2 = st.columns(2)

with col1:
    com_civ1 = CommentaireBox(f"💬 Commentaire {civ1[1]}").render("com_civ1")

with col2:
    com_civ2 = CommentaireBox(f"💬 Commentaire {civ2[1]}").render("com_civ2")

st.markdown("---")

com_map = CommentaireBox(f"🗺️ Commentaire de la carte {carte['nom']}").render("com_map")

st.markdown("---")

com_matchup = CommentaireBox("⚔️ Commentaire global du match-up").render("com_matchup")
