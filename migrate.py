import sqlite3

# Nom du fichier SQLite
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

# Données initiales (10 civs)
civs = [
    {"nom":"Bourguignons","early":38,"mid":36,"late":49,"very_late":50,"remarque":"Fort en chevalerie, attention aux piquiers et moines."},
    {"nom":"Gurjaras","early":40,"mid":47,"late":45,"very_late":48,"remarque":""},
    {"nom":"Byzantins","early":44,"mid":41,"late":48,"very_late":50,"remarque":""},
    {"nom":"Tatars","early":46,"mid":44,"late":47,"very_late":50,"remarque":""},
    {"nom":"Vikings","early":46,"mid":49,"late":57,"very_late":52,"remarque":"Vulnérable aux monks en fin de partie. Excellente économie maritime."},
    {"nom":"Géorgiens","early":48,"mid":41,"late":45,"very_late":50,"remarque":""},
    {"nom":"Malais","early":49,"mid":56,"late":55,"very_late":50,"remarque":"Stratégies scout rush et tower rush fréquentes."},
    {"nom":"Shu","early":52,"mid":63,"late":55,"very_late":47,"remarque":""},
    {"nom":"Romains","early":55,"mid":54,"late":53,"very_late":55,"remarque":""},
    {"nom":"Wu","early":60,"mid":65,"late":53,"very_late":46,"remarque":""},
]

# Insertion des données
for civ in civs:
    c.execute("""
              INSERT OR IGNORE INTO civs (nom, early, mid, late, very_late, remarque)
    VALUES (:nom, :early, :mid, :late, :very_late, :remarque)
              """, civ)

conn.commit()
conn.close()
print(f"✅ BDD '{DB_FILE}' créée et peuplée avec {len(civs)} civilisations.")