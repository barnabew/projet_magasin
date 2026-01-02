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

# Top 5 des départements par type de magasin
st.markdown("### 🏆 Top 5 des Départements par Type de Magasin")

try:
    # Récupération des données
    df_dept_stars = run_query(queries.QUERY_DEPT_STARS)
    
    # Filtrer sur le top 5 par type
    df_top5 = df_dept_stars[df_dept_stars['Rang'] <= 5].copy()
    
    if not df_top5.empty:
        # Affichage en cartes KPI par rang
        for rang in range(1, 6):  # Rangs 1 à 5
            st.markdown(f"### 🏆 **Rang {rang}**")
            
            # Création de 3 colonnes pour chaque type
            col_a, col_b, col_c = st.columns(3)
            
            # Type A
            with col_a:
                dept_info_a = df_top5[(df_top5['Type'] == 'A') & (df_top5['Rang'] == rang)]
                if not dept_info_a.empty:
                    dept_num = int(dept_info_a.iloc[0]['Dept'])
                    ca_moyen = int(dept_info_a.iloc[0]['CA_Moyen'])
                    nb_magasins = int(dept_info_a.iloc[0]['Nb_Magasins'])
                    
                    st.markdown(
                        styles.render_kpi_card(
                            "🏪 Type A (Grands)", 
                            f"Dept {dept_num}<br>${ca_moyen:,} moy.<br>({nb_magasins} magasins)"
                        ), 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        styles.render_kpi_card("🏪 Type A", "Aucune donnée"), 
                        unsafe_allow_html=True
                    )
            
            # Type B  
            with col_b:
                dept_info_b = df_top5[(df_top5['Type'] == 'B') & (df_top5['Rang'] == rang)]
                if not dept_info_b.empty:
                    dept_num = int(dept_info_b.iloc[0]['Dept'])
                    ca_moyen = int(dept_info_b.iloc[0]['CA_Moyen'])
                    nb_magasins = int(dept_info_b.iloc[0]['Nb_Magasins'])
                    
                    st.markdown(
                        styles.render_kpi_card(
                            "🏬 Type B (Moyens)", 
                            f"Dept {dept_num}<br>${ca_moyen:,} moy.<br>({nb_magasins} magasins)"
                        ), 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        styles.render_kpi_card("🏬 Type B", "Aucune donnée"), 
                        unsafe_allow_html=True
                    )
            
            # Type C
            with col_c:
                dept_info_c = df_top5[(df_top5['Type'] == 'C') & (df_top5['Rang'] == rang)]
                if not dept_info_c.empty:
                    dept_num = int(dept_info_c.iloc[0]['Dept'])
                    ca_moyen = int(dept_info_c.iloc[0]['CA_Moyen'])
                    nb_magasins = int(dept_info_c.iloc[0]['Nb_Magasins'])
                    
                    st.markdown(
                        styles.render_kpi_card(
                            "🏫 Type C (Petits)", 
                            f"Dept {dept_num}<br>${ca_moyen:,} moy.<br>({nb_magasins} magasins)"
                        ), 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        styles.render_kpi_card("🏫 Type C", "Aucune donnée"), 
                        unsafe_allow_html=True
                    )
            
            # Espacement entre les rangs
            if rang < 5:
                st.markdown("<br>", unsafe_allow_html=True)
        
        # Analyse comparative
        st.markdown("### 📊 Analyse Comparative")
        
        # Départements communs dans le top 5
        depts_type_a = set(df_top5[df_top5['Type'] == 'A']['Dept'].tolist())
        depts_type_b = set(df_top5[df_top5['Type'] == 'B']['Dept'].tolist())
        depts_type_c = set(df_top5[df_top5['Type'] == 'C']['Dept'].tolist())
        
        depts_communs_ac = depts_type_a.intersection(depts_type_c)
        depts_communs_abc = depts_type_a.intersection(depts_type_b).intersection(depts_type_c)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔄 Départements communs A & C:**")
            if depts_communs_ac:
                st.write(f"📦 Depts: {', '.join(map(str, sorted(depts_communs_ac)))}")
            else:
                st.write("Aucun département commun")
        
        with col2:
            st.markdown("**🎯 Départements communs A, B & C:**")
            if depts_communs_abc:
                st.write(f"📦 Depts: {', '.join(map(str, sorted(depts_communs_abc)))}")
            else:
                st.write("Aucun département commun aux 3 types")
    
    else:
        st.error("Aucune donnée disponible pour les départements")

except Exception as e:
    st.error(f"Erreur lors du chargement des données: {str(e)}")




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



