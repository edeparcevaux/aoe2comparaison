import streamlit as st

class SelectCiv:
    def __init__(self, cm, key):
        self.cm = cm
        self.key = key

    def render(self, label="Civilisation"):
        civs = self.cm.list_civs()  # [(id,nom)]
        return st.selectbox(label, civs, format_func=lambda x: x[1], key=self.key)
