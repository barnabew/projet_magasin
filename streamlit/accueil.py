import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_table, get_connection, run_query
import styles
import queries
import visuel

# Configuration de la page
st.set_page_config(**styles.get_page_config())

# Application du CSS personnalisé
st.markdown(styles.get_custom_css(), unsafe_allow_html=True)

# Navbar
styles.render_navbar(st, current_page="resume")

# Objectif du Dashboard
with st.expander("🎯 Comprendre l'Écosystème Retail", expanded=True):
    st.markdown("""
    **Retail Analytics Dashboard** - Tableau de bord stratégique pour optimiser les performances de votre écosystème retail
    
    **🏪 Contexte**: Analyse de 45 magasins répartis en 3 typologies (A, B, C) sur 81 départements
    
    **💼 Objectifs Business**:
    - 📊 **Optimiser l'assortiment** départemental par typologie de magasin
    - 📈 **Identifier les leviers saisonniers** pour maximiser les ventes en fin d'année
    - 🎯 **Développer des stratégies différenciées** selon la taille et le type des magasins
    - 💰 **Améliorer la rentabilité** par une allocation optimale des ressources
    
    **📋 Navigation**:
    - **Magasins**: Typologie et performances par taille
    - **Départements**: Segmentation et stratégies d'assortiment
    - **Temporel**: Saisonnalité et pic de performance
    - **Recommandations**: Actions prioritaires pour les décideurs
    """)

st.markdown("---")

# Insights business en tête
st.markdown("## 📈 Résumé Exécutif")

insights_cols = st.columns(2)

with insights_cols[0]:
    st.markdown("""
    ### 🏆 **Faits Marquants**
    - **Type A**: Grands magasins avec 40% d'augmentation en décembre
    - **Effet taille**: Corrélation forte entre surface et performance (r=0.85+)
    - **Top départements**: 10 départements génèrent 65% du surplus de décembre
    - **Opportunité**: Potentiel d'amélioration estimé à +12% CA annuel
    """)

with insights_cols[1]:
    st.markdown("""
    ### ⚡ **Actions Prioritaires**
    1. **Renforcer** l'assortiment des départements saisonniers dans les Type A
    2. **Standardiser** les meilleures pratiques des Type A vers Type C
    3. **Optimiser** la gestion des stocks pour les pics de décembre
    4. **Développer** les départements spécialisés à fort ROI
    """)

st.markdown("---")

# Récupération des données KPI
ca_total = run_query(queries.QUERY_CA_TOTAL)["CA_Total"][0]
ca_moyen = run_query(queries.QUERY_CA_MOYEN)["CA_Moyen"][0]
nb_magasins = run_query(queries.QUERY_NB_MAGASINS)["Nb_Magasins"][0]
nb_departements = run_query(queries.QUERY_NB_DEPARTEMENTS)["Nb_Departements"][0]

# Affichage des KPI
kpi_cols = st.columns(4, gap="large")

with kpi_cols[0]:
    st.markdown(styles.render_kpi_card("CA Total", f"${ca_total:,.0f}"), unsafe_allow_html=True)

with kpi_cols[1]:
    st.markdown(styles.render_kpi_card("CA Moyen Hebdo", f"${ca_moyen:,.0f}"), unsafe_allow_html=True)

with kpi_cols[2]:
    st.markdown(styles.render_kpi_card("Magasins", f"{nb_magasins}"), unsafe_allow_html=True)

with kpi_cols[3]:
    st.markdown(styles.render_kpi_card("Départements", f"{nb_departements}"), unsafe_allow_html=True)

st.markdown("---")

# Graphiques business orientés décideurs
st.markdown("## 📊 Vue d'Ensemble Business")

chart_row1 = st.columns(2, gap="large")

with chart_row1[0]:
    st.markdown("### 💰 Performance Exécutive par Type")
    # Performance executive avec métriques business
    df_exec_perf = run_query(queries.QUERY_PERFORMANCE_EXECUTIVE)
    
    fig_exec = px.bar(
        df_exec_perf,
        x="Type",
        y="CA_Par_Magasin",
        text="Part_CA_Pct",
        title="CA par Magasin et Part de Marché (%)",
        labels={
            "Type": "Type de Magasin", 
            "CA_Par_Magasin": "CA par Magasin ($)",
            "Part_CA_Pct": "Part (%)"
        },
        color="Type",
        color_discrete_map={'A': '#FF6B6B', 'B': '#4ECDC4', 'C': '#45B7D1'}
    )
    fig_exec.update_traces(texttemplate='%{text}%', textposition='outside')
    visuel.apply_theme(fig_exec)
    st.plotly_chart(fig_exec, use_container_width=True)
    
    # Métriques clés sous le graphique
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Type A - CA/Magasin", f"${df_exec_perf[df_exec_perf['Type']=='A']['CA_Par_Magasin'].iloc[0]:,.0f}")
    with col2:
        st.metric("Type B - CA/Magasin", f"${df_exec_perf[df_exec_perf['Type']=='B']['CA_Par_Magasin'].iloc[0]:,.0f}")
    with col3:
        st.metric("Type C - CA/Magasin", f"${df_exec_perf[df_exec_perf['Type']=='C']['CA_Par_Magasin'].iloc[0]:,.0f}")

with chart_row1[1]:
    st.markdown("### 📈 Saisonnalité Business")
    # Analyse saisonnière avec indicateurs business
    df_saison = run_query(queries.QUERY_SAISONNALITE_BUSINESS)
    
    fig_saison = px.bar(
        df_saison,
        x="Nom_Mois",
        y="CA_Total",
        color="Pct_Vs_Moyenne",
        title="Performance Mensuelle vs Moyenne",
        labels={
            "Nom_Mois": "Mois",
            "CA_Total": "Chiffre d'Affaires ($)",
            "Pct_Vs_Moyenne": "% vs Moyenne"
        },
        text="Performance",
        color_continuous_scale="RdYlGn"
    )
    fig_saison.update_traces(textposition='outside')
    visuel.apply_theme(fig_saison)
    st.plotly_chart(fig_saison, use_container_width=True)
    
    # Insight décembre
    decembre_pct = df_saison[df_saison['Nom_Mois']=='Décembre']['Pct_Vs_Moyenne'].iloc[0]
    st.success(f"🎯 **Pic de décembre**: +{decembre_pct}% vs moyenne annuelle")

chart_row2 = st.columns(2, gap="large")

with chart_row2[0]:
    st.markdown("### 🎯 Top Opportunités Départements")
    # Top opportunités business
    df_opport = run_query(queries.QUERY_DEPARTEMENTS_OPPORTUNITE)
    
    if len(df_opport) > 0:
        fig_opport = px.scatter(
            df_opport.head(8),
            x="Taux_Penetration",
            y="Potentiel_CA_Supplementaire",
            size="CA_Actuel",
            hover_data=["Dept", "Pct_Amelioration"],
            title="Potentiel vs Pénétration Actuelle",
            labels={
                "Taux_Penetration": "Taux de Pénétration (%)",
                "Potentiel_CA_Supplementaire": "Potentiel CA Supplémentaire ($)"
            }
        )
        visuel.apply_theme(fig_opport)
        st.plotly_chart(fig_opport, use_container_width=True)
        
        # Top 3 opportunités
        st.markdown("**🏆 Top 3 Opportunités**:")
        for i in range(min(3, len(df_opport))):
            dept = df_opport.iloc[i]
            st.write(f"• **Dept {dept['Dept']}**: +${dept['Potentiel_CA_Supplementaire']:,.0f} (+{dept['Pct_Amelioration']}%)")
    else:
        st.info("Aucune opportunité majeure identifiée selon les critères actuels")

with chart_row2[1]:
    st.markdown("### ⚖️ ROI par Taille de Magasin")
    # ROI par taille
    df_roi = run_query(queries.QUERY_ROI_TAILLE)
    
    fig_roi = px.bar(
        df_roi,
        x="Categorie_Taille",
        y="ROI_Moyen_Par_1000_Sqft",
        title="Rentabilité par 1000 sqft selon la Taille",
        labels={
            "Categorie_Taille": "Catégorie de Taille",
            "ROI_Moyen_Par_1000_Sqft": "ROI par 1000 sqft ($)"
        },
        text="ROI_Moyen_Par_1000_Sqft",
        color="ROI_Moyen_Par_1000_Sqft",
        color_continuous_scale="Viridis"
    )
    fig_roi.update_traces(texttemplate='$%{text}', textposition='outside')
    visuel.apply_theme(fig_roi)
    st.plotly_chart(fig_roi, use_container_width=True)
    
    # Insight ROI
    best_roi = df_roi.loc[df_roi['ROI_Moyen_Par_1000_Sqft'].idxmax()]
    st.info(f"💡 **Meilleur ROI**: {best_roi['Categorie_Taille']} magasins (${best_roi['ROI_Moyen_Par_1000_Sqft']}/1000 sqft)")

st.markdown("---")

# Section recommandations business
st.markdown("## 🚀 Recommandations Stratégiques")

rec_cols = st.columns(3)

with rec_cols[0]:
    st.markdown("""
    ### 📊 **Court Terme (0-6 mois)**
    - Optimiser les stocks des départements TOP 10 pour décembre
    - Renforcer marketing fin d'année pour magasins Type A
    - Ajuster assortiment Type B selon modèle Type A
    - Former équipes sur départements à fort potentiel
    """)

with rec_cols[1]:
    st.markdown("""
    ### 🎯 **Moyen Terme (6-18 mois)**
    - Déployer départements high-performers dans Type C
    - Standardiser processus Type A vers autres types
    - Développer programme fidélité saisonnalité
    - Optimiser allocation espace par ROI/sqft
    """)

with rec_cols[2]:
    st.markdown("""
    ### 🏗️ **Long Terme (18+ mois)**
    - Étudier extension magasins Type C performants
    - Repositionner départements sous-performants
    - Développer nouveaux concepts Type A+
    - Implémenter IA pour optimisation continue
    """)

with chart_row2[0]:
    # Top départements par CA
    df_top_depts = run_query(queries.QUERY_TOP_DEPARTMENTS)
    
    fig_top_depts = px.bar(
        df_top_depts.head(10),
        x="CA_Total",
        y="Dept",
        orientation="h",
        title="Top 10 Départements par CA Total",
        labels={"CA_Total": "Chiffre d'affaires ($)", "Dept": "Département"}
    )
    visuel.apply_theme(fig_top_depts)
    st.plotly_chart(fig_top_depts, use_container_width=True)

with chart_row2[1]:
    # Évolution temporelle globale
    df_evolution = run_query(queries.QUERY_EVOLUTION_MENSUELLE)
    
    fig_evolution = px.line(
        df_evolution,
        x="Mois",
        y="CA_Total_Mensuel",
        title="Évolution du CA Mensuel",
        labels={"Mois": "Mois", "CA_Total_Mensuel": "CA Total Mensuel ($)"},
        markers=True
    )
    visuel.apply_theme(fig_evolution)
    st.plotly_chart(fig_evolution, use_container_width=True)
