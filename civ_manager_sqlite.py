# civ_manager_supabase.py
import pandas as pd
from client_supabase import supabase  # ton supabase déjà configuré

class CivManager:

    # ----------------------------
    # Civilizations
    # ----------------------------
    def list_civs(self):
        """Retourne la liste des civs (id, nom)"""
        response = supabase.table("civs").select("id, nom").execute()
        if response.data is None:
            return []
        return [(c["id"], c["nom"]) for c in response.data]

    def get_civs(self):
        """Retourne toutes les civilisations (id, nom)"""
        response = supabase.table("civs").select("id, nom").order("nom").execute()
        if response.data is None:
            return []
        return [(row["id"], row["nom"]) for row in response.data]

    def get_civ(self, civ_id):
        """Retourne une civilisation complète"""
        response = supabase.table("civs").select("*").eq("id", civ_id).single().execute()
        if response.data is None:
            return None
        return response.data

    def update_civ(self, civ_id, nom, early, mid, late, very_late, remarque=""):
        supabase.table("civs").update({
            "nom": nom,
            "early": early,
            "mid": mid,
            "late": late,
            "very_late": very_late,
            "remarque": remarque
        }).eq("id", civ_id).execute()

    # ----------------------------
    # Build Orders
    # ----------------------------
    def get_bos(self):
        """Retourne la liste de tous les BO"""
        response = supabase.table("bos").select("id, titre").execute()
        if response.data is None:
            return []
        return [(b["id"], b["titre"]) for b in response.data]

    def insert_bo(self, titre, description):
        supabase.table("bos").insert({"titre": titre, "description": description}).execute()

    def get_bo(self, bo_id):
        response = supabase.table("bos").select("*").eq("id", bo_id).single().execute()
        if response.data is None:
            return None
        return response.data

    def get_civ_bos(self, civ_id):
        """Retourne la liste des BO associés à une civ, triés par ordre"""
        response = supabase.table("civ_bos").select("bo_id, ordre, bos(titre, description)").eq("civ_id", civ_id).execute()
        if response.data is None:
            return []
        result = []
        for r in response.data:
            bo_id = r["bo_id"]
            titre = r["bos"]["titre"]
            desc = r["bos"]["description"]
            ordre = r["ordre"]
            result.append((bo_id, titre, desc, ordre))
        return sorted(result, key=lambda x: x[3])

    def add_bo_to_civ(self, civ_id, bo_id, ordre=None):
        """Associe un BO à une civ, à un ordre donné ou à la fin"""
        # Récupérer l'ordre max si non spécifié
        if ordre is None:
            existing = supabase.table("civ_bos").select("ordre").eq("civ_id", civ_id).order("ordre", desc=True).limit(1).execute()
            ordre = (existing.data[0]["ordre"] if existing.data else 0) + 1

        # Vérifier si déjà associé
        existing = supabase.table("civ_bos").select("*").eq("civ_id", civ_id).eq("bo_id", bo_id).execute()
        if existing.data:
            supabase.table("civ_bos").update({"ordre": ordre}).eq("civ_id", civ_id).eq("bo_id", bo_id).execute()
        else:
            supabase.table("civ_bos").insert({"civ_id": civ_id, "bo_id": bo_id, "ordre": ordre}).execute()

    def remove_bo_from_civ(self, civ_id, bo_id):
        supabase.table("civ_bos").delete().eq("civ_id", civ_id).eq("bo_id", bo_id).execute()

    # ----------------------------
    # DataFrame pour comparateur
    # ----------------------------
    def load_all_as_df(self):
        civs = self.get_civs()
        data = []
        for civ_id, nom in civs:
            civ = self.get_civ(civ_id)
            if civ:
                data.append({
                    "Civ": nom,
                    "Early": civ.get("early", 0),
                    "Mid": civ.get("mid", 0),
                    "Late": civ.get("late", 0),
                    "Very late": civ.get("very_late", 0),
                    "Remarque": civ.get("remarque", "")
                })
        return pd.DataFrame(data)
