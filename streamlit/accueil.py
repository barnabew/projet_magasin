import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_table, get_connection, run_query
import queries
from styles import get_page_config, get_custom_css, render_navbar, render_kpi_card
import visuel
import textes
import styles

# Configuration de la page
st.set_page_config(**get_page_config())

# Application du CSS personnalisé
st.markdown(get_custom_css(), unsafe_allow_html=True)

# Navbar
render_navbar(st, current_page="resume")

# Titre principal


# Affichage en colonnes
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(render_kpi_card("Différences CA promo", "1.92%"),unsafe_allow_html=True)
    
with col2:
    st.markdown(render_kpi_card("Nombre départements universels (présence 100%)", "62/81"),unsafe_allow_html=True)
    
with col3:
    st.markdown(render_kpi_card("TOP 5 Départements communs A et C", "92,95,90,38"),unsafe_allow_html=True)
    
with col4:
    st.markdown(render_kpi_card("Variation CA décembre type A et B", "23%"),unsafe_allow_html=True)







chart_row1 = st.columns(2, gap="large")

with chart_row1[0]:
    # Corrélation Taille vs Performance
    st.plotly_chart(visuel.plot_performance_by_type(run_query(queries.QUERY_TAILLE_PERF)), use_container_width=True)

with chart_row1[1]:
    # Évolution Temporelle des Types de Magasins
    st.plotly_chart(visuel.plot_evolution_temporelle_types(run_query(queries.QUERY_EVOL_TEMP_TYPE)), use_container_width=True)

chart_row2 = st.columns(2, gap="large")

df_dept_stars = run_query(queries.QUERY_DEPT_STARS)
def_dept_segmentation = run_query(queries.QUERY_CATEGORIE_DEPTS)

with chart_row2[0]:
   st.markdown(styles.render_table_window("Détail des ventes", df_dept_stars[df_dept_stars["Rang"]<=5]),unsafe_allow_html=True)

with chart_row2[1]:
   st.markdown(styles.render_table_window("Segmentation des départements", def_dept_segmentation),unsafe_allow_html=True)


st.title("Recommandations")
st.markdown(textes.recommandations, unsafe_allow_html=True)
