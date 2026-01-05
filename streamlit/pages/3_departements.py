import streamlit as st
import pandas as pd
import plotly.express as px
from utils import run_query
import styles
import visuel
import queries
import textes

# Configuration de la page
st.set_page_config(**styles.get_page_config())

# Application du CSS personnalisé
st.markdown(styles.get_custom_css(), unsafe_allow_html=True)

# Navbar
styles.render_navbar(st, current_page="departements")

st.markdown("---")

st.markdown(textes.departements_intro , unsafe_allow_html=True)

st.markdown("---")

st.markdown("## Heatmaps Performance Départementale")

df_heatmap = run_query(queries.QUERY_HEATMAP_DATA)


col_heat_a, col_heat_b, col_heat_c = st.columns(3)

with col_heat_a:
    fig_heatmap_a = visuel.plot_heatmap_by_type(df_heatmap, store_type='A')
    st.plotly_chart(fig_heatmap_a, use_container_width=True)

with col_heat_b:
    fig_heatmap_b = visuel.plot_heatmap_by_type(df_heatmap, store_type='B')
    st.plotly_chart(fig_heatmap_b, use_container_width=True)

with col_heat_c:
    fig_heatmap_c = visuel.plot_heatmap_by_type(df_heatmap, store_type='C')
    st.plotly_chart(fig_heatmap_c, use_container_width=True)



st.markdown(textes.departements_heatmaps, unsafe_allow_html=True)

st.markdown("---")


st.markdown("### Top 5 des Départements par Type de Magasin")


df_dept_stars = run_query(queries.QUERY_DEPT_STARS)
    
st.markdown(styles.render_table_window("Détail des ventes", df_dept_stars[df_dept_stars["Rang"]<=5]),unsafe_allow_html=True)


st.markdown(textes.departements_top5, unsafe_allow_html=True)
