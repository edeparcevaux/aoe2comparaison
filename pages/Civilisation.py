from components.Tabs import civ_tabs
from components.Civ_header import civ_header
from components.Civ_stats import civ_stats_section

CIV_DATA = {
    "nom": "Vikings",
    "description": "Civ orientée infanterie et économie.",
    "stats": {
        "1v1": "Forte early, faible late.",
        "2v2": "Eco très solide.",
        "3v3": "Bon pocket.",
        "4v4": "Très bon boom.",
    },
}

civ_header(CIV_DATA)

tab_1v1, tab_2v2, tab_3v3, tab_4v4 = civ_tabs()

with tab_1v1:
    civ_stats_section(CIV_DATA, "1v1")

with tab_2v2:
    civ_stats_section(CIV_DATA, "2v2")

with tab_3v3:
    civ_stats_section(CIV_DATA, "3v3")

with tab_4v4:
    civ_stats_section(CIV_DATA, "4v4")