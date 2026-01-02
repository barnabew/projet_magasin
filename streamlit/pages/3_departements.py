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

# Titre business-oriented
st.markdown("# 🛍️ Optimisation Départementale & Assortiment")

# KPIs Business des départements
st.markdown("## 📈 Performance Départementale")

# Top 5 des départements par type de magasin
st.markdown("### 🏆 Top 5 des Départements par Type de Magasin")

try:
    # Récupération des données
    df_dept_stars = run_query(queries.QUERY_DEPT_STARS)
    
    # Filtrer sur le top 5 par type
    df_top5 = df_dept_stars[df_dept_stars['Rang'] <= 5].copy()
    
    if not df_top5.empty:
        # Création du tableau croisé
        tableau_data = []
        
        for rang in range(1, 6):  # Rangs 1 à 5
            row = {"🏆 Rang": rang}
            
            # Pour chaque type de magasin
            for type_magasin in ['A', 'B', 'C']:
                dept_info = df_top5[(df_top5['Type'] == type_magasin) & (df_top5['Rang'] == rang)]
                
                if not dept_info.empty:
                    dept_num = int(dept_info.iloc[0]['Dept'])
                    ca_moyen = int(dept_info.iloc[0]['CA_Moyen'])
                    row[f"🏪 Type {type_magasin}"] = f"Dept {dept_num} (${ca_moyen:,})"
                else:
                    row[f"🏪 Type {type_magasin}"] = "-"
            
            tableau_data.append(row)
        
        # Affichage du tableau
        df_tableau = pd.DataFrame(tableau_data)
        
        st.dataframe(
            df_tableau,
            column_config={
                "🏆 Rang": st.column_config.NumberColumn("🏆 Rang", width="small"),
                "🏪 Type A": st.column_config.TextColumn("🏪 Type A (Grands)", width="medium"),
                "🏪 Type B": st.column_config.TextColumn("🏬 Type B (Moyens)", width="medium"),
                "🏪 Type C": st.column_config.TextColumn("🏫 Type C (Petits)", width="medium")
            },
            use_container_width=True,
            hide_index=True
        )
        
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



