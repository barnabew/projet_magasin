import pandas as pd
import streamlit as st
import os
import pandasql as psql

# Chemins vers les fichiers CSV nettoyés dans le dossier data
CSV_PATHS = {
    "sales": "data/sales_clean.csv",
    "stores": "data/stores_clean.csv",
    "features": "data/features_clean.csv"
}


@st.cache_data(ttl=3600)  # Cache pendant 1 heure
def load_csv_data():
    """Charge tous les fichiers CSV nettoyés depuis le dossier data."""
    data = {}
    for table_name, file_path in CSV_PATHS.items():
        if os.path.exists(file_path):
            data[table_name] = pd.read_csv(file_path)
        else:
            st.error(f"Fichier {file_path} introuvable !")
            return None
    
    return data


@st.cache_data(ttl=3600)  # Cache pendant 1 heure
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


@st.cache_data(ttl=3600)  # Cache pendant 1 heure
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
