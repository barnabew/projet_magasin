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

st.markdown("textes.departements_intro" , unsafe_allow_html=True)

st.markdown("---")

# Top 5 des départements par type de magasin
st.markdown("### 🏆 Top 5 des Départements par Type de Magasin")


df_dept_stars = run_query(queries.QUERY_DEPT_STARS)
    
st.markdown(
    render_table_card(df_dept_stars),
    unsafe_allow_html=True
)
    
    



st.markdown("---")

# Heatmaps des performances par type
st.markdown("## 🔥 Heatmaps Performance Départementale")
st.markdown("*Visualisation de la performance (CA Total) de chaque département par magasin et par type*")

try:
    # Récupération des données pour les heatmaps
    df_heatmap = run_query(queries.QUERY_HEATMAP_DATA)
    
    if not df_heatmap.empty:
        # Création de 3 colonnes pour les heatmaps
        col_heat_a, col_heat_b, col_heat_c = st.columns(3)
        
        with col_heat_a:
            st.markdown("### 🏪 Type A (Grands)")
            fig_heatmap_a = visuel.plot_heatmap_by_type(df_heatmap, store_type='A')
            st.plotly_chart(fig_heatmap_a, use_container_width=True)
        
        with col_heat_b:
            st.markdown("### 🏬 Type B (Moyens)")
            fig_heatmap_b = visuel.plot_heatmap_by_type(df_heatmap, store_type='B')
            st.plotly_chart(fig_heatmap_b, use_container_width=True)
        
        with col_heat_c:
            st.markdown("### 🏫 Type C (Petits)")
            fig_heatmap_c = visuel.plot_heatmap_by_type(df_heatmap, store_type='C')
            st.plotly_chart(fig_heatmap_c, use_container_width=True)
        
        # Légende explicative
        st.markdown("---")
        st.markdown("""
        **📖 Interprétation des Heatmaps :**
        - **Axe X** : Numéros des départements
        - **Axe Y** : Numéros des magasins  
        - **Couleur** : Intensité du CA Total (plus rouge = plus performant)
        - **Zones vides** : Départements non présents dans le magasin
        """)
    
    else:
        st.error("Aucune donnée disponible pour les heatmaps")

except Exception as e:
    st.error(f"Erreur lors du chargement des heatmaps: {str(e)}")

st.markdown("---")



