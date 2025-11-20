import streamlit as st

class Card:
    def __init__(self, icon, title, page_path):
        self.icon = icon
        self.title = title
        self.page_path = page_path

    def render(self):
        # Style global injecté une seule fois
        if "card_style_loaded" not in st.session_state:
            st.session_state["card_style_loaded"] = True
            st.markdown("""
            <style>
            .card {
                border: 1px solid #444;
                border-radius: 12px;
                padding: 20px;
                background-color: #1f1f1f;
                text-align: center;
                transition: 0.2s ease;
            }
            .card:hover {
                background-color: #333333;
                transform: scale(1.03);
            }
            .card-icon {
                font-size: 42px;
            }
            .card-title {
                font-size: 20px;
                margin-top: 10px;
                font-weight: 600;
            }
            </style>
            """, unsafe_allow_html=True)

        # Contenu de la carte
        with st.container():
            if st.button(f"{self.icon} {self.title}", use_container_width=True):
                st.switch_page(self.page_path)
