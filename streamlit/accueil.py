import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_table, get_connection, run_query
from queries import QUERY_KPI_GLOBAUX
from styles import get_page_config, get_custom_css, render_navbar, apply_theme
import visuel

# Configuration de la page
st.set_page_config(styles.get_page_config())

# Application du CSS personnalisé
st.markdown(styles.get_custom_css(), unsafe_allow_html=True)

# Navbar
styles.render_navbar(st, current_page="resume")

# Titre principal
st.markdown("---")


st.markdown(textes.Accueil_Intro)

st.markdown("---")
st.markdown("### KPI Globaux")

kpi_df = pd.read_sql(QUERY_KPI_GLOBAUX, get_db_connection())
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





st.markdown("---")
st.markdown("### Analyses Visuelles")




chart_row1 = st.columns(2, gap="large")

with chart_row1[0]:
    # Corrélation Délai vs Satisfaction
    st.plotly_chart(visuel.plot_performance_by_type(), use_container_width=True)

with chart_row1[1]:
    # Corrélation Délai vs Satisfaction
    st.plotly_chart(visuel.plot_performance_by_type(), use_container_width=True)

chart_row2 = st.columns(2, gap="large")

with chart_row2[0]:
    # Corrélation Délai vs Satisfaction
    st.plotly_chart(visuel.plot_performance_by_type(), use_container_width=True)

with chart_row2[1]:
    # Corrélation Délai vs Satisfaction
    st.plotly_chart(visuel.plot_performance_by_type(), use_container_width=True)




st.markdown("---")
st.markdown("### Recommandations")


