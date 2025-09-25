# Streamlit app: Comparateur de civilisations (simplifié)
# Usage:
# 1) Installer dependencies: pip install streamlit pandas matplotlib
# 2) Lancer: streamlit run Comparateur_de_civs_streamlit.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------
# Données d'exemple (à remplacer / étendre)
# ---------------------------
CIV_DATA = {
    'Bourguignons': {'Early':38,'Mid':36,'Late':49,'Very late':50},
    'Gurjaras': {'Early':40,'Mid':47,'Late':45,'Very late':48},
    'Byzantins': {'Early':44,'Mid':41,'Late':48,'Very late':50},
    'Tatars': {'Early':46,'Mid':44,'Late':47,'Very late':50},
    'Vikings': {'Early':46,'Mid':49,'Late':57,'Very late':52},
    'Géorgiens': {'Early':48,'Mid':41,'Late':45,'Very late':50},
    'Malais': {'Early':49,'Mid':56,'Late':55,'Very late':50},
    'Shu': {'Early':52,'Mid':63,'Late':55,'Very late':47},
    'Romains': {'Early':55,'Mid':54,'Late':53,'Very late':55},
    'Bulgare': {'Early':57,'Mid':52,'Late':52,'Very late':52},
    'Wu': {'Early':60,'Mid':65,'Late':53,'Very late':46},
    'Hindustanis': {'Early':48,'Mid':48,'Late':53,'Very late':54},
    'Khitans': {'Early':53,'Mid':55,'Late':52,'Very late':51},
    'Malians': {'Early':48,'Mid':56,'Late':53,'Very late':51},
    'Japanese': {'Early':61,'Mid':54,'Late':49,'Very late':50},
    'Teutons': {'Early':53,'Mid':49,'Late':52,'Very late':51},
    'Huns': {'Early':46,'Mid':49,'Late':52,'Very late':52},
    'Persians': {'Early':58,'Mid':50,'Late':50,'Very late':50},
    'Celts': {'Early':53,'Mid':55,'Late':51,'Very late':49},
    'Ethiopians': {'Early':54,'Mid':59,'Late':51,'Very late':46},
    'Goths': {'Early':60,'Mid':50,'Late':49,'Very late':50},
    'Italians': {'Early':45,'Mid':50,'Late':52,'Very late':51},
    'Spanish': {'Early':47,'Mid':58,'Late':53,'Very late':47},
    'Mongols': {'Early':61,'Mid':53,'Late':48,'Very late':49},
    'Incas': {'Early':52,'Mid':49,'Late':50,'Very late':51},
    'Bohemians': {'Early':40,'Mid':52,'Late':53,'Very late':49},
    'Turks': {'Early':40,'Mid':47,'Late':54,'Very late':49},
    'Franks': {'Early':44,'Mid':48,'Late':51,'Very late':51},
    'Armenians': {'Early':55,'Mid':52,'Late':48,'Very late':50},
    'Sicilians': {'Early':56,'Mid':51,'Late':48,'Very late':49},
    'Magyars': {'Early':52,'Mid':49,'Late':48,'Very late':52},
    'Lithuanians': {'Early':52,'Mid':45,'Late':50,'Very late':51},
    'Bengalis': {'Early':44,'Mid':55,'Late':51,'Very late':48},
    'Dravidians': {'Early':52,'Mid':51,'Late':48,'Very late':51},
    'Slavs': {'Early':44,'Mid':45,'Late':51,'Very late':51},
    'Berbers': {'Early':42,'Mid':46,'Late':49,'Very late':52},
    'Mayans': {'Early':48,'Mid':51,'Late':47,'Very late':50},
    'Cumans': {'Early':49,'Mid':46,'Late':53,'Very late':48},
    'Burmese': {'Early':46,'Mid':54,'Late':48,'Very late':48},
    'Koreans': {'Early':47,'Mid':53,'Late':50,'Very late':47},
    'Aztecs': {'Early':48,'Mid':47,'Late':49,'Very late':49},
    'Khmer': {'Early':48,'Mid':47,'Late':48,'Very late':50},
    'Poles': {'Early':43,'Mid':39,'Late':50,'Very late':51},
    'Portuguese': {'Early':45,'Mid':52,'Late':47,'Very late':49},
    'Wei': {'Early':34,'Mid':41,'Late':53,'Very late':50},
    'Jurchens': {'Early':48,'Mid':53,'Late':46,'Very late':49},
    'Saracens': {'Early':44,'Mid':50,'Late':46,'Very late':50},
    'Vietnamese': {'Early':44,'Mid':44,'Late':47,'Very late':50},
    'Britons': {'Early':47,'Mid':45,'Late':47,'Very late':49},
    'Chinese': {'Early':43,'Mid':45,'Late':48,'Very late':49},
}

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

REMARKS = {
    'Vikings': [
        "Vulnérable aux monks en fin de partie.",
        "Excellente économie maritime, attention aux raids de cavalerie."
    ],
    'Malais': [
        "Stratégies scout rush et tower rush fréquentes.",
        "Montée en âges rapide mais fragile si rushée."
    ],
    'Bourguignons': [
        "Fort en chevalerie, attention aux piquiers et moines."
    ],
}

# ---------------------------
# Fonctions utilitaires
# ---------------------------
def civ_to_series(civ_name):
    data = CIV_DATA.get(civ_name, {'Early':0,'Mid':0,'Late':0,'Very late':0})
    return pd.Series(data)

def make_comparison_df(civ1, civ2):
    s1 = civ_to_series(civ1)
    s2 = civ_to_series(civ2)
    df = pd.DataFrame({'Period':['Early','Mid','Late','Very late'], civ1:s1.values, civ2:s2.values})
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
st.set_page_config(page_title="Comparateur de civilisations", layout='wide')
st.title("⚔️ Comparateur de civilisations")

# Sidebar
st.sidebar.header('Sélection')
all_civs = sorted(list(CIV_DATA.keys()))
civ1 = st.sidebar.selectbox('Civ 1', all_civs, index=all_civs.index('Vikings'))
civ2 = st.sidebar.selectbox('Civ 2', all_civs, index=all_civs.index('Malais'))

st.sidebar.markdown('---')
show_radar = st.sidebar.checkbox('Afficher radar', value=True)
show_line = st.sidebar.checkbox('Afficher graphique en lignes', value=True)

# Graphiques
st.subheader('Graphiques comparatifs')
comp_df = make_comparison_df(civ1, civ2)
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
    for r in REMARKS.get(civ, ['Aucune remarque enregistrée.']):
        col.write('- ' + r)
