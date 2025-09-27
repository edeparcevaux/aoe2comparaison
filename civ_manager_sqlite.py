import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("aoe2.db")

class CivManager:
    def __init__(self, db_path=DB_PATH):
        # check_same_thread=False pour usage dans Streamlit
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        c.execute("""
                  CREATE TABLE IF NOT EXISTS bos (
                                                     id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                     titre TEXT NOT NULL,
                                                     description TEXT
                  )
                  """)
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
        c.execute("""
                  CREATE TABLE IF NOT EXISTS civs_bos (
                                                          civ_id INTEGER NOT NULL,
                                                          bo_id INTEGER NOT NULL,
                                                          ordre INTEGER DEFAULT 0,
                                                          PRIMARY KEY (civ_id, bo_id),
                      FOREIGN KEY (civ_id) REFERENCES civs(id) ON DELETE CASCADE,
                      FOREIGN KEY (bo_id) REFERENCES bos(id) ON DELETE CASCADE
                      )
                  """)
        self.conn.commit()

    # ----------------------------
    # Build Orders
    # ----------------------------
    def get_bos(self):
        c = self.conn.cursor()
        c.execute("SELECT id, titre FROM bos ORDER BY titre")
        return c.fetchall()

    def insert_bo(self, titre, description):
        c = self.conn.cursor()
        c.execute("INSERT INTO bos (titre, description) VALUES (?, ?)", (titre, description))
        self.conn.commit()
        return c.lastrowid

    def get_bo(self, bo_id):
        c = self.conn.cursor()
        c.execute("SELECT id, titre, description FROM bos WHERE id=?", (bo_id,))
        return c.fetchone()

    def update_bo(self, bo_id, titre, description):
        c = self.conn.cursor()
        c.execute("UPDATE bos SET titre=?, description=? WHERE id=?", (titre, description, bo_id))
        self.conn.commit()

    # ----------------------------
    # Civilisations
    # ----------------------------
    def add_civ(self, nom, early, mid, late, very_late, remarque=""):
        c = self.conn.cursor()
        c.execute("""
            INSERT OR REPLACE INTO civs (nom, early, mid, late, very_late, remarque)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (nom, early, mid, late, very_late, remarque))
        self.conn.commit()
        return c.lastrowid

    def update_civ(self, civ_id, nom, early, mid, late, very_late, remarque=""):
        c = self.conn.cursor()
        c.execute("""
                  UPDATE civs
                  SET nom=?, early=?, mid=?, late=?, very_late=?, remarque=?
                  WHERE id=?
                  """, (nom, early, mid, late, very_late, remarque, civ_id))
        self.conn.commit()

    def get_civ(self, civ_id):
        c = self.conn.cursor()
        c.execute("SELECT id, nom, early, mid, late, very_late, remarque FROM civs WHERE id=?", (civ_id,))
        row = c.fetchone()
        if row:
            keys = ["id", "nom", "early", "mid", "late", "very_late", "remarque"]
            return dict(zip(keys, row))
        return None

    def list_civs(self):
        c = self.conn.cursor()
        c.execute("SELECT id, nom FROM civs ORDER BY nom")
        return c.fetchall()

    def load_all_as_df(self):
        c = self.conn.cursor()
        c.execute("""SELECT nom AS Civ, early AS Early, mid AS Mid, late AS Late,
                            very_late AS 'Very late', remarque
                     FROM civs ORDER BY nom""")
        rows = c.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in c.description])
        return df

    # ----------------------------
    # Associations civ <-> BO
    # ----------------------------
    def add_bo_to_civ(self, civ_id, bo_id, ordre=None):
        """
        Ajoute l'association civ <-> bo.
        Si ordre is None => place à la fin (max+1).
        Si association existe déjà, met à jour l'ordre.
        """
        c = self.conn.cursor()
        # check civ and bo exist
        c.execute("SELECT 1 FROM civs WHERE id=?", (civ_id,))
        if c.fetchone() is None:
            raise ValueError("Civ id introuvable")
        c.execute("SELECT 1 FROM bos WHERE id=?", (bo_id,))
        if c.fetchone() is None:
            raise ValueError("BO id introuvable")

        if ordre is None:
            c.execute("SELECT COALESCE(MAX(ordre), 0) FROM civs_bos WHERE civ_id=?", (civ_id,))
            ordre = (c.fetchone()[0] or 0) + 1

        # Insert or update ordre
        c.execute("INSERT OR IGNORE INTO civs_bos (civ_id, bo_id, ordre) VALUES (?, ?, ?)", (civ_id, bo_id, ordre))
        c.execute("UPDATE civs_bos SET ordre=? WHERE civ_id=? AND bo_id=?", (ordre, civ_id, bo_id))
        self.conn.commit()

        # normalize orders
        self._reorder_civ_bos(civ_id)

    def remove_bo_from_civ(self, civ_id, bo_id):
        c = self.conn.cursor()
        c.execute("DELETE FROM civs_bos WHERE civ_id=? AND bo_id=?", (civ_id, bo_id))
        self.conn.commit()
        # normalize orders
        self._reorder_civ_bos(civ_id)

    def get_civ_bos(self, civ_id):
        c = self.conn.cursor()
        c.execute("""
                  SELECT b.id, b.titre, b.description, cb.ordre
                  FROM civs_bos cb
                           JOIN bos b ON b.id = cb.bo_id
                  WHERE cb.civ_id=?
                  ORDER BY cb.ordre ASC
                  """, (civ_id,))
        return c.fetchall()

    def _reorder_civ_bos(self, civ_id):
        """Réattribue des ordres contigus (1..n) pour une civ"""
        c = self.conn.cursor()
        c.execute("SELECT bo_id FROM civs_bos WHERE civ_id=? ORDER BY ordre, bo_id", (civ_id,))
        rows = c.fetchall()
        for idx, (bo_id,) in enumerate(rows, start=1):
            c.execute("UPDATE civs_bos SET ordre=? WHERE civ_id=? AND bo_id=?", (idx, civ_id, bo_id))
        self.conn.commit()
