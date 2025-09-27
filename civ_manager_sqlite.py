import sqlite3
from pathlib import Path
import pandas as pd

DB_PATH = Path("aoe2.db")

class CivManager:
    def __init__(self, db_path=DB_PATH):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        c = self.conn.cursor()
        # Build orders
        c.execute("""
                  CREATE TABLE IF NOT EXISTS build_orders (
                                                              id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                              nom TEXT NOT NULL,
                                                              description TEXT,
                                                              contenu TEXT
                  )
                  """)
        # Civilisations
        c.execute("""
                  CREATE TABLE IF NOT EXISTS civs (
                                                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                      nom TEXT UNIQUE NOT NULL,
                                                      early INTEGER NOT NULL,
                                                      mid INTEGER NOT NULL,
                                                      late INTEGER NOT NULL,
                                                      very_late INTEGER NOT NULL,
                                                      remarque TEXT,
                                                      bo_id INTEGER,
                                                      FOREIGN KEY(bo_id) REFERENCES build_orders(id)
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
        ) """)

        c.execute("""
                  CREATE TABLE IF NOT EXISTS bos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
        titre TEXT NOT NULL,
        description TEXT
        ) """)

        c.execute("""

        CREATE TABLE IF NOT EXISTS civs_bos (
            civ_id INTEGER NOT NULL,
        bo_id INTEGER NOT NULL,
        PRIMARY KEY (civ_id, bo_id),
        FOREIGN KEY (civ_id) REFERENCES civs(id),
        FOREIGN KEY (bo_id) REFERENCES bos(id)
        ) """)

        self.conn.commit()

    # ----------------------------
    # Build Orders
    # ----------------------------
    def add_bo(self, nom, description="", contenu=""):
        c = self.conn.cursor()
        c.execute("INSERT INTO build_orders (nom, description, contenu) VALUES (?, ?, ?)",
                  (nom, description, contenu))
        self.conn.commit()
        return c.lastrowid

    def list_bos(self):
        c = self.conn.cursor()
        c.execute("SELECT id, nom, description FROM build_orders")
        return c.fetchall()

    def get_bo(self, bo_id):
        c = self.conn.cursor()
        c.execute("SELECT id, nom, description, contenu FROM build_orders WHERE id=?", (bo_id,))
        return c.fetchone()

    # ----------------------------
    # Civilisations
    # ----------------------------
    def add_civ(self, nom, early, mid, late, very_late, remarque="", bo_id=None):
        c = self.conn.cursor()
        c.execute("""
        INSERT OR REPLACE INTO civs (nom, early, mid, late, very_late, remarque, bo_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (nom, early, mid, late, very_late, remarque, bo_id))
        self.conn.commit()

    def update_civ(self, nom, early, mid, late, very_late, remarque="", bo_id=None):
        c = self.conn.cursor()
        c.execute("""
                  UPDATE civs
                  SET early=?, mid=?, late=?, very_late=?, remarque=?, bo_id=?
                  WHERE nom=?
                  """, (early, mid, late, very_late, remarque, bo_id, nom))
        self.conn.commit()

    def get_civ(self, nom):
        c = self.conn.cursor()
        c.execute("SELECT * FROM civs WHERE nom=?", (nom,))
        row = c.fetchone()
        if row:
            keys = [desc[0] for desc in c.description]
            return dict(zip(keys, row))
        return None

    def list_civs(self):
        c = self.conn.cursor()
        c.execute("SELECT nom FROM civs ORDER BY nom")
        return [r[0] for r in c.fetchall()]

    def load_all_as_df(self):
        c = self.conn.cursor()
        c.execute("SELECT nom AS Civ, early AS Early, mid AS Mid, late AS Late, very_late AS 'Very late', remarque, bo_id FROM civs ORDER BY nom")
        rows = c.fetchall()
        df = pd.DataFrame(rows, columns=[desc[0] for desc in c.description])
        return df

    def get_civs(self):
        c = self.conn.cursor()
        c.execute("SELECT id, nom FROM civs ORDER BY nom")
        civs = c.fetchall()

        return civs

    def get_bos_for_civ(self,civ_id):
        c = self.conn.cursor()
        c.execute("""
                  SELECT bos.id, bos.titre, bos.description
                  FROM bos
                           JOIN civs_bos ON bos.id = civs_bos.bo_id
                  WHERE civs_bos.civ_id=?
                  """, (civ_id,))
        bos = c.fetchall()

        return bos

    def insert_bo(self, titre, description):
        c = self.conn.cursor()
        c.execute("INSERT INTO bos (titre, description) VALUES (?, ?)", (titre, description))
        bo_id = c.lastrowid
        return bo_id

    def link_bo_to_civ(self,civ_id, bo_id):
        c = self.conn.cursor()
        c.execute("INSERT OR IGNORE INTO civs_bos (civ_id, bo_id) VALUES (?, ?)", (civ_id, bo_id))
