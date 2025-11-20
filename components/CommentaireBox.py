import streamlit as st

class CommentaireBox:
    def __init__(self, title):
        self.title = title

    def render(self, key):
        st.subheader(self.title)
        return st.text_area("", key=key)
