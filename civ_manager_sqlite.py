import sqlite3
import pandas as pd

DB_FILE = "aoe2.db"

class CivManager:
    def __init__(self, db_file=DB_FILE):
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
        self._create_table()

    def _create_table(self):
        c = self.conn.cursor()
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
        self.conn.commit()

    def list_civs(self):
        c = self.conn.cursor()
        c.execute("SELECT nom FROM civs ORDER BY nom")
        return [row[0] for row in c.fetchall()]

    def get_civ(self, nom):
        c = self.conn.cursor()
        c.execute("SELECT nom, early, mid, late, very_late, remarque FROM civs WHERE nom=?", (nom,))
        row = c.fetchone()
        if row:
            return {
                "nom": row[0],
                "early": row[1],
                "mid": row[2],
                "late": row[3],
                "very_late": row[4],
                "remarque": row[5] or ""
            }
        return None

    def save_civ(self, civ_data):
        """Ajoute ou met à jour une civ"""
        c = self.conn.cursor()
        c.execute("""
                  INSERT INTO civs (nom, early, mid, late, very_late, remarque)
                  VALUES (:nom, :early, :mid, :late, :very_late, :remarque)
                      ON CONFLICT(nom) DO UPDATE SET
                      early=excluded.early,
                                              mid=excluded.mid,
                                              late=excluded.late,
                                              very_late=excluded.very_late,
                                              remarque=excluded.remarque
                  """, civ_data)
        self.conn.commit()

    def load_all_as_df(self):
        df = pd.read_sql_query("SELECT * FROM civs", self.conn)
        return df
