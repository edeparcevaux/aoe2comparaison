import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

class PowerGraph:
    def __init__(self, cm):
        self.cm = cm

    def render(self, civ1_id, civ2_id):
        civ1 = self.cm.get_civ(civ1_id)
        civ2 = self.cm.get_civ(civ2_id)

        df = pd.DataFrame({
            "Phase": ["Early", "Mid", "Late", "Very late"],
            civ1["nom"]: [civ1["early"], civ1["mid"], civ1["late"], civ1["very_late"]],
            civ2["nom"]: [civ2["early"], civ2["mid"], civ2["late"], civ2["very_late"]],
        }).set_index("Phase")

        fig, ax = plt.subplots(figsize=(4, 2.7))
        df.plot(ax=ax, marker="o")
        st.pyplot(fig)
