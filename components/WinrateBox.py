import streamlit as st

class WinrateBox:
    def render(self, civ1, civ2):
        # Placeholder → calcul réel plus tard
        fake_winrate = 50

        st.markdown(f"""
        <div style='background:#222;padding:15px;border-radius:10px;text-align:center;'>
            <h3 style='margin:0;'>Probabilité de victoire</h3>
            <p style='font-size:32px;margin:5px 0;'>{fake_winrate}%</p>
        </div>
        """, unsafe_allow_html=True)
