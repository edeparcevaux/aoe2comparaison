import pandas as pd
from client_supabase import supabase
import streamlit as st

class CivManager:

    # ----------------------------
    # Civilizations
    # ----------------------------
    @staticmethod
    @st.cache_data(ttl=600)
    def list_civs():
        """Retourne la liste des civs (id, nom)"""
        response = supabase.table("civs").select("id, nom").execute()
        if response.data is None:
            return []
        return [(c["id"], c["nom"]) for c in response.data]

    @staticmethod
    @st.cache_data(ttl=600)
    def get_civs():
        """Retourne toutes les civilisations (id, nom)"""
        response = supabase.table("civs").select("id, nom").order("nom").execute()
        if response.data is None:
            return []
        return [(row["id"], row["nom"]) for row in response.data]

    @staticmethod
    @st.cache_data(ttl=600)
    def get_civ(civ_id):
        """Retourne une civilisation complète"""
        response = supabase.table("civs").select("*").eq("id", civ_id).single().execute()
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
    @staticmethod
    @st.cache_data(ttl=600)
    def get_bos():
        """Retourne la liste de tous les BO"""
        response = supabase.table("bos").select("id, titre").execute()
        if response.data is None:
            return []
        return [(b["id"], b["titre"]) for b in response.data]

    def insert_bo(self, titre, description):
        supabase.table("bos").insert({"titre": titre, "description": description}).execute()

    @staticmethod
    @st.cache_data(ttl=600)
    def get_bo(bo_id):
        response = supabase.table("bos").select("*").eq("id", bo_id).single().execute()
        if response.data is None:
            return None
        return response.data

    @staticmethod
    @st.cache_data(ttl=600)
    def get_civ_bos(civ_id):
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
        if ordre is None:
            existing = supabase.table("civ_bos").select("ordre").eq("civ_id", civ_id).order("ordre", desc=True).limit(1).execute()
            ordre = (existing.data[0]["ordre"] if existing.data else 0) + 1

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
    @staticmethod
    @st.cache_data(ttl=600)
    def load_all_as_df():
        civs = CivManager.get_civs()
        data = []
        for civ_id, nom in civs:
            civ = CivManager.get_civ(civ_id)
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

    def update_bo(self, bo_id, titre, description):
        """Met à jour un build order existant"""
        supabase.table("bos").update({
            "titre": titre,
            "description": description
        }).eq("id", bo_id).execute()

    # --- Gestion des Cartes ---
    def get_all_maps(self):
        response = supabase.table("maps").select("*").execute()
        return response.data

    def get_map(self, map_id):
        response = supabase.table("maps").select("*").eq("id", map_id).single().execute()
        return response.data

    def update_map(self, map_id, remarque):
        supabase.table("maps").update({
            "remarque": remarque
        }).eq("id", map_id).execute()

    # --- Liens entre BO / Civ / Carte ---
    def get_bos_for_civ(self, civ_id):
        response = supabase.table("bos_civs").select("bo_id, bos(*)").eq("civ_id", civ_id).execute()
        return [r["bos"] for r in response.data]

    def get_bos_for_map(self, map_id):
        response = supabase.table("bos_maps").select("bo_id, bos(*)").eq("map_id", map_id).execute()
        return [r["bos"] for r in response.data]

    def get_civs_for_map(self, map_id):
        response = supabase.table("civs_maps").select("civ_id, civs(*), remarque").eq("map_id", map_id).execute()
        return response.data

    def update_civ_map_remarque(self, civ_id, map_id, remarque):
        supabase.table("civs_maps").update({
            "remarque": remarque
        }).eq("civ_id", civ_id).eq("map_id", map_id).execute()