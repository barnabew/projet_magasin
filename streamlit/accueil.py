import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_table, get_connection, run_query
from utils import get_db_connection
from queries import QUERY_KPI_GLOBAUX
from styles import apply_custom_css

# Configuration de la page
st.set_page_config(styles.get_page_config())

# Application du CSS personnalisé
st.markdown(styles.get_custom_css(), unsafe_allow_html=True)

# Navbar
styles.render_navbar(st, current_page="resume")

# Titre principal
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    ### 📊 Le Défi Business
    
    Une chaîne de **retail** avec **45 magasins** répartis en 3 types (A, B, C) 
    et **81 départements** cherche à optimiser ses assortiments et maximiser ses ventes.
    
    **Comment transformer les données en décisions stratégiques ?**
    """)

with col2:
    st.info("""
    **📍 Méthodologie**
    - SQL pour requêtes
    - Python pour analyse
    - Plotly pour visualisation
    - Approche : Question → Analyse → Réponse
    """)


st.markdown("---")  

st.markdown("### ❓ Les 3 Questions Clés")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 🏪 Question 1
    **Nos magasins sont-ils bien segmentés ?**
    
    Validation de la typologie A/B/C et corrélation taille-performance.
    
    [→ Voir l'analyse](#)
    """)

with col2:
    st.markdown("""
    #### 🛍️ Question 2
    **Quels départements privilégier ?**
    
    Identification des départements stratégiques par type de magasin.
    
    [→ Voir l'analyse](#)
    """)

with col3:
    st.markdown("""
    #### 📅 Question 3
    **Comment exploiter la saisonnalité ?**
    
    Patterns temporels et opportunités saisonnières.
    
    [→ Voir l'analyse](#)
    """)    

st.markdown("---")
st.markdown("### 📊 KPI Globaux")

# Requête
conn = get_db_connection()
kpi_df = pd.read_sql(QUERY_KPI_GLOBAUX, conn)
conn.close()

# Extraction des valeurs
ca_total = kpi_df['CA_Total'][0]
nb_magasins = kpi_df['Nb_Magasins'][0]
nb_depts = kpi_df['Nb_Departements'][0]
date_debut = kpi_df['Date_Debut'][0]
date_fin = kpi_df['Date_Fin'][0]

# Affichage en colonnes
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 CA Total", f"${ca_total/1_000_000:.2f}M")
    
with col2:
    st.metric("🏪 Magasins", nb_magasins)
    
with col3:
    st.metric("📦 Départements", nb_depts)
    
with col4:
    st.metric("📅 Période", f"{date_debut[:4]} - {date_fin[:4]}")