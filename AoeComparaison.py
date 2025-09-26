import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import os

# ---------------------------
# Config
# ---------------------------
DATA_FILE = "civs.json"

STRATEGIES = {
    'Vikings': [
        {'name':'Infantry Boom','tag':'infantry_boom','description':'Boom eco and mass infantry (infantry/cavalry transition).','bo_exists':True},
        {'name':'Drush Into Feudal','tag':'drush_feudal','description':'Early drush pressure followed by feudal aggression.','bo_exists':False}
    ],
    'Malais': [
        {'name':'Scout Rush','tag':'scout_rush','description':'Fast scouts with aggressive raiding.','bo_exists':True},
        {'name':'Tower Rush','tag':'tower_rush','description':'Cheesy tower rush (map dependent).','bo_exists':True}
    ],
    'Bourguignons': [
        {'name':'Knight Led Push','tag':'knight_push','description':'Exploit strong knights and upgrades.','bo_exists':True}
    ],
}

BUILD_ORDERS = {
    'infantry_boom': """
# Build Order: Infantry Boom (Vikings)
- 6 on sheep
- 3 on wood
- Click up at 27-28 villagers
- Mass farms + blacksmith upgrades
""",
    'drush_feudal': """
# Build Order: Drush -> Feudal
- 3 on sheep
- 4 on wood
- 2 on boar
- Create 2 militia ~6-7 mins
""",
    'scout_rush': """
# Build Order: Scout Rush (Malais)
- 6 on sheep
- 4 on wood
- 3 on berries
- Build stable at Feudal ~10:30
""",
    'tower_rush': """
# Build Order: Tower Rush (Malais)
- Early wood heavy
- Forward towers with villagers
""",
    'knight_push': """
# Build Order: Knight Push (Bourguignons)
- Standard scout/eco
- Click up Castle ~28-30 vills
- Mass knights + husbandry
"""
}

# ---------------------------
# Fonctions utilitaires
# ---------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def make_comparison_df(data, civ1, civ2):
    s1 = pd.Series(data[civ1]["scores"])
    s2 = pd.Series(data[civ2]["scores"])
    df = pd.DataFrame({'Period':s1.index, civ1:s1.values, civ2:s2.values})
    df.set_index('Period', inplace=True)
    return df

def radar_plot(df, civ1, civ2):
    labels = df.index.tolist()
    stats1 = df[civ1].values
    stats2 = df[civ2].values
    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()
    stats1 = np.concatenate((stats1, [stats1[0]]))
    stats2 = np.concatenate((stats2, [stats2[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig = plt.figure(figsize=(6,6))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats1, marker='o', label=civ1)
    ax.fill(angles, stats1, alpha=0.1)
    ax.plot(angles, stats2, marker='o', label=civ2)
    ax.fill(angles, stats2, alpha=0.1)
    ax.set_thetagrids(angles[:-1]*180/np.pi, labels)
    ax.set_title(f"Comparaison: {civ1} vs {civ2}")
    ax.legend(loc='upper right')
    ax.set_ylim(0, max(df.max().max(), 10))
    return fig

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Civilisations AoE2", layout="wide")
st.title("⚔️ Civilisations AoE2")

mode = st.sidebar.radio("Choisir un mode :", ["Comparateur", "Édition"])

data = load_data()
all_civs = sorted(data.keys())

# ---------------------------
# Mode Comparateur
# ---------------------------
if mode == "Comparateur":
    st.subheader("Comparateur de civilisations")
    civ1 = st.selectbox("Civilisation 1", all_civs, index=0)
    civ2 = st.selectbox("Civilisation 2", all_civs, index=1)

    comp_df = make_comparison_df(data, civ1, civ2)

    show_line = st.checkbox('Afficher graphique en lignes', value=True)
    show_radar = st.checkbox('Afficher radar', value=True)

    if show_line:
        fig_line, ax = plt.subplots()
        comp_df.plot(kind='line', marker='o', ax=ax)
        ax.set_ylabel('Score')
        ax.set_xticks(range(len(comp_df.index)))
        ax.set_xticklabels(comp_df.index)
        st.pyplot(fig_line)
    if show_radar:
        fig_rad = radar_plot(comp_df, civ1, civ2)
        st.pyplot(fig_rad)

    st.markdown('---')

    # Stratégies & BO
    st.subheader('Stratégies connues & Build Orders')
    left, right = st.columns(2)

    for civ, col in zip([civ1, civ2], [left, right]):
        col.markdown(f'### {civ}')
        strategies = STRATEGIES.get(civ, [])
        if not strategies:
            col.info("Aucune stratégie renseignée pour cette civ.")
        for strat in strategies:
            cols = col.columns([6,1])
            cols[0].markdown(f"**{strat['name']}**  \n*{strat['description']}*")
            if strat.get('bo_exists'):
                if cols[1].button('Voir BO', key=f"{civ}_{strat['tag']}"):
                    bo_text = BUILD_ORDERS.get(strat['tag'], 'Build order introuvable.')
                    col.markdown(f"#### Build Order — {strat['name']}")
                    col.code(bo_text)

    st.markdown('---')

    # Remarques
    st.subheader('Remarques & conseils')
    cols = st.columns(2)
    for civ, col in zip([civ1, civ2], cols):
        col.markdown(f'**{civ}**')
        for r in data[civ].get("remarks", ["Aucune remarque enregistrée."]):
            col.write('- ' + r)

# ---------------------------
# Mode Édition
# ---------------------------
elif mode == "Édition":
    st.subheader("Édition de civilisation")
    civ = st.selectbox("Choisir une civilisation", all_civs)
    civ_data = data[civ]

    st.write("### Scores")
    scores = civ_data["scores"]
    df = pd.DataFrame([scores])
    new_scores = st.data_editor(df, num_rows="fixed")
    civ_data["scores"] = dict(new_scores.iloc[0])

    st.write("### Remarques")
    new_remarks = []
    for i, remark in enumerate(civ_data.get("remarks", [])):
        new_remark = st.text_input(f"Remarque {i+1}", value=remark)
        new_remarks.append(new_remark)
    add_new = st.text_input("Ajouter une remarque")
    if add_new:
        new_remarks.append(add_new)
    civ_data["remarks"] = new_remarks

    if st.button("💾 Sauvegarder"):
        data[civ] = civ_data
        save_data(data)
        st.success(f"{civ} mis à jour !")
