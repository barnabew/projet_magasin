import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_table, get_connection, run_query
import queries
from styles import get_page_config, get_custom_css, render_navbar
import visuel

# Configuration de la page
st.set_page_config(**get_page_config())

# Application du CSS personnalisé
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Navbar
render_navbar(st, current_page="resume")

# Titre principal
st.markdown("---")


st.markdown("textes.Accueil_Intro")

st.markdown("---")
st.markdown("### KPI Globaux")

kpi_df = run_query(queries.QUERY_KPI_GLOBAUX)

# Affichage en colonnes
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 CA Total", f"${kpi_df['CA_Total'][0]/1_000_000:.2f}M")
    
with col2:
    st.metric("🏪 Magasins", kpi_df['Nb_Magasins'][0])
    
with col3:
    st.metric("📦 Départements", kpi_df['Nb_Departements'][0])
    
with col4:
    st.metric("📅 Période", f"{kpi_df['Date_Debut'][0][:4]} - {kpi_df['Date_Fin'][0][:4]}")





st.markdown("---")
st.markdown("### Analyses Visuelles")




chart_row1 = st.columns(2, gap="large")

with chart_row1[0]:
    # Corrélation Taille vs Performance
    st.plotly_chart(visuel.plot_performance_by_type(run_query(queries.QUERY_TAILLE_PERF)), width=True)

with chart_row1[1]:
    # Heatmap du CA par Type de departement pour le Type de magasin A
    st.plotly_chart(visuel.plot_heatmap_by_type(run_query(queries.QUERY_HEATMAP_DATA), store_type='A'), width=True)

chart_row2 = st.columns(2, gap="large")

with chart_row2[0]:
    # Évolution Temporelle des Types de Magasins
    st.plotly_chart(visuel.plot_evolution_temporelle_types(run_query(queries.QUERY_EVOL_TEMP_TYPE)), width=True)

with chart_row2[1]:
    # Évolution des Top Départements
    top_depts_df = run_query(queries.QUERY_GET_TOP10) 
    top_depts = top_depts_df['Dept'].tolist() 
    query_temporal = queries.get_query_top_depts_temporel(top_depts)  
    dept_temporal_df = run_query(query_temporal) 
    st.plotly_chart(visuel.plot_evolution_top_departements(dept_temporal_df, top_depts), width=True) 



st.markdown("---")
st.markdown("### Recommandations")


