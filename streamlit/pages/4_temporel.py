import streamlit as st
import pandas as pd
import plotly.express as px
from utils import run_query
import styles
import textes
import visuel
import queries

# Configuration de la page
st.set_page_config(**styles.get_page_config())

# Application du CSS personnalisé
st.markdown(styles.get_custom_css(), unsafe_allow_html=True)

# Navbar
styles.render_navbar(st, current_page="temporel")

st.markdown("---") 

st.markdown(textes.temporel_intro , unsafe_allow_html=True)

st.markdown("---")

st.markdown("## Analyse Temporelle par type")

st.plotly_chart(visuel.plot_evolution_temporelle_types(run_query(queries.QUERY_EVOL_TEMP_TYPE)), use_container_width=True)

st.markdown(textes.temporel_type , unsafe_allow_html=True)


st.markdown("---")

st.markdown("## Analyse Temporelle décembre - autres mois pour les magasins de type A")


sommes = run_query(queries.QUERY_VARIATION_DECEMBRE_SOMMES)
sommes_group = sommes.groupby(by=["Groupe"]).sum().sort_values(by=["Nb_Departements"], ascending=True)

st.markdown(styles.render_table_window("Départements", sommes_group.reset_index()),unsafe_allow_html=True)


st.markdown("---")

st.markdown("## Analyse Temporelle departements de type A")

top_depts_df = run_query(queries.QUERY_GET_TOP10) 
top_depts = top_depts_df['Dept'].tolist() 
query_temporal = queries.get_query_top_depts_temporel(top_depts)  
dept_temporal_df = run_query(query_temporal) 
st.plotly_chart(visuel.plot_evolution_top_departements(dept_temporal_df, top_depts), use_container_width=True)

st.markdown(textes.temporel_dept_a , unsafe_allow_html=True)



