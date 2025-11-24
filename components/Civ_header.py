import streamlit as st

def civ_header(civ):
    st.title(f"Civilisation : {civ['nom']}")
    st.write(civ.get("description", ""))