import sqlite3

# Nom du fichier SQLite (on garde "aoe2.db" pour cohérence)
DB_FILE = "aoe2.db"

# Connexion
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Création de la table civs
c.execute("""
          CREATE TABLE IF NOT EXISTS civs (
                                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                                              nom TEXT UNIQUE NOT NULL,
                                              early INTEGER NOT NULL,
                                              mid INTEGER NOT NULL,
                                              late INTEGER NOT NULL,
                                              very_late INTEGER NOT NULL,
                                              remarque TEXT
          )
          """)

# Données de toutes les civs (extrait de ton JSON CIV_DATA + REMARKS)
civs = [
    {"nom": "Bourguignons", "early": 38, "mid": 36, "late": 49, "very_late": 50,
     "remarque": "Fort en chevalerie, attention aux piquiers et moines."},
    {"nom": "Gurjaras", "early": 40, "mid": 47, "late": 45, "very_late": 48, "remarque": ""},
    {"nom": "Byzantins", "early": 44, "mid": 41, "late": 48, "very_late": 50, "remarque": ""},
    {"nom": "Tatars", "early": 46, "mid": 44, "late": 47, "very_late": 50, "remarque": ""},
    {"nom": "Vikings", "early": 46, "mid": 49, "late": 57, "very_late": 52,
     "remarque": "Vulnérable aux monks en fin de partie. Excellente économie maritime."},
    {"nom": "Géorgiens", "early": 48, "mid": 41, "late": 45, "very_late": 50, "remarque": ""},
    {"nom": "Malais", "early": 49, "mid": 56, "late": 55, "very_late": 50,
     "remarque": "Stratégies scout rush et tower rush fréquentes."},
    {"nom": "Shu", "early": 52, "mid": 63, "late": 55, "very_late": 47, "remarque": ""},
    {"nom": "Romains", "early": 55, "mid": 54, "late": 53, "very_late": 55, "remarque": ""},
    {"nom": "Wu", "early": 60, "mid": 65, "late": 53, "very_late": 46, "remarque": ""},
    {"nom": "Hindustanis", "early": 48, "mid": 48, "late": 53, "very_late": 54, "remarque": ""},
    {"nom": "Khitans", "early": 53, "mid": 55, "late": 52, "very_late": 51, "remarque": ""},
    {"nom": "Malians", "early": 48, "mid": 56, "late": 53, "very_late": 51, "remarque": ""},
    {"nom": "Japanese", "early": 61, "mid": 54, "late": 49, "very_late": 50, "remarque": ""},
    {"nom": "Teutons", "early": 53, "mid": 49, "late": 52, "very_late": 51, "remarque": ""},
    {"nom": "Huns", "early": 46, "mid": 49, "late": 52, "very_late": 52, "remarque": ""},
    {"nom": "Persians", "early": 58, "mid": 50, "late": 50, "very_late": 50, "remarque": ""},
    {"nom": "Celts", "early": 53, "mid": 55, "late": 51, "very_late": 49, "remarque": ""},
    {"nom": "Ethiopians", "early": 54, "mid": 59, "late": 51, "very_late": 46, "remarque": ""},
    {"nom": "Goths", "early": 60, "mid": 50, "late": 49, "very_late": 50, "remarque": ""},
    {"nom": "Italians", "early": 45, "mid": 50, "late": 52, "very_late": 51, "remarque": ""},
    {"nom": "Spanish", "early": 47, "mid": 58, "late": 53, "very_late": 47, "remarque": ""},
    {"nom": "Mongols", "early": 61, "mid": 53, "late": 48, "very_late": 49, "remarque": ""},
    {"nom": "Incas", "early": 52, "mid": 49, "late": 50, "very_late": 51, "remarque": ""},
    {"nom": "Bohemians", "early": 40, "mid": 52, "late": 53, "very_late": 49, "remarque": ""},
    {"nom": "Turks", "early": 40, "mid": 47, "late": 54, "very_late": 49, "remarque": ""},
    {"nom": "Franks", "early": 44, "mid": 48, "late": 51, "very_late": 51, "remarque": ""},
    {"nom": "Armenians", "early": 55, "mid": 52, "late": 48, "very_late": 50, "remarque": ""},
    {"nom": "Sicilians", "early": 56, "mid": 51, "late": 48, "very_late": 49, "remarque": ""},
    {"nom": "Magyars", "early": 52, "mid": 49, "late": 48, "very_late": 52, "remarque": ""},
    {"nom": "Lithuanians", "early": 52, "mid": 45, "late": 50, "very_late": 51, "remarque": ""},
    {"nom": "Bengalis", "early": 44, "mid": 55, "late": 51, "very_late": 48, "remarque": ""},
    {"nom": "Dravidians", "early": 52, "mid": 51, "late": 48, "very_late": 51, "remarque": ""},
    {"nom": "Slavs", "early": 44, "mid": 45, "late": 51, "very_late": 51, "remarque": ""},
    {"nom": "Berbers", "early": 42, "mid": 46, "late": 49, "very_late": 52, "remarque": ""},
    {"nom": "Mayans", "early": 48, "mid": 51, "late": 47, "very_late": 50, "remarque": ""},
    {"nom": "Cumans", "early": 49, "mid": 46, "late": 53, "very_late": 48, "remarque": ""},
    {"nom": "Burmese", "early": 46, "mid": 54, "late": 48, "very_late": 48, "remarque": ""},
    {"nom": "Koreans", "early": 47, "mid": 53, "late": 50, "very_late": 47, "remarque": ""},
    {"nom": "Aztecs", "early": 48, "mid": 47, "late": 49, "very_late": 49, "remarque": ""},
    {"nom": "Khmer", "early": 48, "mid": 47, "late": 48, "very_late": 50, "remarque": ""},
    {"nom": "Poles", "early": 43, "mid": 39, "late": 50, "very_late": 51, "remarque": ""},
    {"nom": "Portuguese", "early": 45, "mid": 52, "late": 47, "very_late": 49, "remarque": ""},
    {"nom": "Wei", "early": 34, "mid": 41, "late": 53, "very_late": 50, "remarque": ""},
    {"nom": "Jurchens", "early": 48, "mid": 53, "late": 46, "very_late": 49, "remarque": ""},
    {"nom": "Saracens", "early": 44, "mid": 50, "late": 46, "very_late": 50, "remarque": ""},
    {"nom": "Vietnamese", "early": 44, "mid": 44, "late": 47, "very_late": 50, "remarque": ""},
    {"nom": "Britons", "early": 47, "mid": 45, "late": 47, "very_late": 49, "remarque": ""},
    {"nom": "Chinese", "early": 43, "mid": 45, "late": 48, "very_late": 49, "remarque": ""},
]

# Insertion
for civ in civs:
    c.execute("""
              INSERT OR IGNORE INTO civs (nom, early, mid, late, very_late, remarque)
    VALUES (:nom, :early, :mid, :late, :very_late, :remarque)
              """, civ)

conn.commit()
conn.close()
print(f"✅ BDD '{DB_FILE}' créée et peuplée avec {len(civs)} civilisations.")
