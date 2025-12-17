import pandas as pd
import streamlit as st
import os
import pandasql as psql

# Obtenir le répertoire du fichier utils.py
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# Chemins vers les fichiers CSV nettoyés dans le dossier data
CSV_PATHS = {
    "sales": os.path.join(CURRENT_DIR, "data", "sales_clean.csv"),
    "stores": os.path.join(CURRENT_DIR, "data", "stores_clean.csv"),
    "features": os.path.join(CURRENT_DIR, "data", "features_clean.csv")
}


@st.cache_resource  # Cache persistant pour toute la session
def load_csv_data():
    """Charge tous les fichiers CSV nettoyés depuis le dossier data."""
    data = {}
    missing_files = []
    
    for table_name, file_path in CSV_PATHS.items():
        if os.path.exists(file_path):
            data[table_name] = pd.read_csv(file_path)
        else:
            missing_files.append(f"{table_name}: {file_path}")
    
    if missing_files:
        for missing in missing_files:
            st.error(f"❌ Fichier introuvable: {missing}")
        st.error(f"Répertoire courant: {os.getcwd()}")
        st.error(f"Chemin utils.py: {CURRENT_DIR}")
        return None
    
    return data


def run_query(query):
    """Exécute une requête SQL sur les DataFrames pandas."""
    data = load_csv_data()
    
    if data is None:
        st.error("Impossible de charger les données CSV !")
        return pd.DataFrame()
    
    # Met les DataFrames à disposition pour la requête SQL
    sales = data['sales']
    stores = data['stores']  
    features = data['features']
    
    # Exécute la requête avec pandasql
    result = psql.sqldf(query, locals())
    return result


def load_table(table_name):
    """Charge une table complète."""
    data = load_csv_data()
    
    if data is None:
        st.error("Impossible de charger les données CSV !")
        return pd.DataFrame()
        
    if table_name not in data:
        st.error(f"Table '{table_name}' introuvable !")
        return pd.DataFrame()
        
    return data[table_name]


def get_connection():
    """Fonction de compatibilité - ne fait rien avec les CSV."""
    return None
