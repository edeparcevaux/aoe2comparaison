import streamlit as st

class SelectMap:
    def __init__(self, cm, key):
        self.cm = cm
        self.key = key

    def render(self, label="Carte"):
        maps = self.cm.get_all_maps()
        return st.selectbox(label, maps, format_func=lambda x: x["nom"], key=self.key)
