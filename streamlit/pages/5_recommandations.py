import streamlit as st
import pandas as pd
import plotly.express as px
from utils import run_query
import styles
import queries
import visuel
import textes

# Configuration de la page
st.set_page_config(**styles.get_page_config())

# Application du CSS personnalisé
st.markdown(styles.get_custom_css(), unsafe_allow_html=True)

# Navbar
styles.render_navbar(st, current_page="recommandations")

st.markdown("# 🚀 Plan d'Action Stratégique")

# Section Executive Summary
st.markdown("## 📋 Résumé Exécutif")

summary_cols = st.columns(3)

with summary_cols[0]:
    st.markdown("""
    ### 💰 **Impact Financier**
    - **Potentiel identifié**: +12-15% CA annuel
    - **ROI estimé**: 250-300% sur 18 mois
    - **Investissement requis**: Réallocation stocks + formation
    """)

with summary_cols[1]:
    st.markdown("""
    ### ⏱️ **Timeline**
    - **Q1**: Optimisation stocks décembre
    - **Q2-Q3**: Standardisation processus
    - **Q4+**: Expansion départements
    """)

with summary_cols[2]:
    st.markdown("""
    ### 🎯 **KPIs de Suivi**
    - CA/magasin par type
    - Pénétration départements clés
    - ROI/sqft par catégorie
    """)

st.markdown("---")

# Actions par priorité avec données
st.markdown("## 🏆 Actions Prioritaires (Data-Driven)")

# Action 1: Optimisation saisonnière
with st.expander("🥇 **PRIORITÉ 1**: Maximiser le Pic de Décembre", expanded=True):
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        **🎯 Objectif**: Augmenter de +25% les ventes de décembre sur les départements identifiés
        
        **📊 Constats**:
        - 10 départements génèrent 65% du surplus de décembre
        - Type A: +40% performance en décembre vs année
        - Potentiel inexploité sur Types B et C
        
        **⚡ Actions Immédiates**:
        1. **Stocks renforcés** sur départements TOP 10 pour novembre-décembre
        2. **Formation équipes** sur techniques de vente spécialisées
        3. **Campagnes marketing** ciblées par type de magasin
        4. **Merchandising** optimisé pour départements saisonniers
        """)
    
    with col2:
        # Mini-graphique des top départements
        try:
            top_depts = run_query(queries.QUERY_TOP10_VARIATION_DECEMBRE)
            if len(top_depts) > 0:
                st.markdown("**🔥 Départements Prioritaires**")
                for i in range(min(5, len(top_depts))):
                    st.write(f"• **Dept {top_depts.iloc[i]['Departement']}**")
        except:
            st.write("Données en cours de chargement...")

# Action 2: Standardisation Type A → C
with st.expander("🥈 **PRIORITÉ 2**: Dupliquer le Succès Type A vers Type C", expanded=False):
    
    st.markdown("""
    **🎯 Objectif**: Améliorer performance Type C de +15% en adoptant meilleures pratiques Type A
    
    **📈 Analyse Comparative**:
    """)
    
    # Comparaison Type A vs C
    try:
        perf_data = run_query(queries.QUERY_PERFORMANCE_EXECUTIVE)
        if len(perf_data) >= 2:
            type_a_ca = perf_data[perf_data['Type']=='A']['CA_Par_Magasin'].iloc[0]
            type_c_ca = perf_data[perf_data['Type']=='C']['CA_Par_Magasin'].iloc[0]
            gap_pct = round((type_a_ca - type_c_ca) / type_c_ca * 100, 1)
            
            comp_cols = st.columns(3)
            with comp_cols[0]:
                st.metric("Type A - CA/Magasin", f"${type_a_ca:,.0f}")
            with comp_cols[1]:
                st.metric("Type C - CA/Magasin", f"${type_c_ca:,.0f}")
            with comp_cols[2]:
                st.metric("Écart Performance", f"+{gap_pct}%", delta=f"{gap_pct}%")
    except:
        st.write("Calcul en cours...")
    
    st.markdown("""
    **🛠️ Plan d'Action**:
    1. **Audit assortiment** Type A vs Type C par département
    2. **Formations croisées** équipes Type C par managers Type A
    3. **Déploiement progressif** top départements Type A dans Type C
    4. **Suivi mensuel** amélioration performance
    """)

# Action 3: Expansion départements opportunité
with st.expander("🥉 **PRIORITÉ 3**: Exploiter les Opportunités Départementales", expanded=False):
    
    st.markdown("**💎 Départements à Fort Potentiel**")
    
    try:
        opport_data = run_query(queries.QUERY_DEPARTEMENTS_OPPORTUNITE)
        if len(opport_data) > 0:
            
            # Graphique potentiel
            fig_pot = px.bar(
                opport_data.head(5),
                x="Dept",
                y="Potentiel_CA_Supplementaire",
                text="Pct_Amelioration",
                title="Top 5 Opportunités par Département",
                labels={
                    "Dept": "Département",
                    "Potentiel_CA_Supplementaire": "Potentiel CA ($)",
                    "Pct_Amelioration": "% Amélioration"
                }
            )
            fig_pot.update_traces(texttemplate='%{text}%', textposition='outside')
            visuel.apply_theme(fig_pot)
            st.plotly_chart(fig_pot, use_container_width=True)
            
            total_potentiel = opport_data['Potentiel_CA_Supplementaire'].sum()
            st.success(f"💰 **Potentiel Total**: +${total_potentiel:,.0f} CA annuel")
    except:
        st.write("Analyse des opportunités en cours...")

# Section Timeline et Budget
st.markdown("---")
st.markdown("## 📅 Timeline d'Implémentation")

timeline_cols = st.columns(4)

with timeline_cols[0]:
    st.markdown("""
    ### **Q1 2025**
    - ✅ Audit départements
    - ✅ Formation équipes
    - ✅ Ajustement stocks
    
    **Budget**: €50K
    """)

with timeline_cols[1]:
    st.markdown("""
    ### **Q2 2025**
    - 🔄 Tests Type A→C
    - 🔄 Campagnes ciblées
    - 🔄 Suivi KPIs
    
    **Budget**: €75K
    """)

with timeline_cols[2]:
    st.markdown("""
    ### **Q3 2025**
    - 📈 Déploiement général
    - 📈 Expansion départements
    - 📈 Optimisation continue
    
    **Budget**: €100K
    """)

with timeline_cols[3]:
    st.markdown("""
    ### **Q4 2025+**
    - 🚀 Mesure ROI
    - 🚀 Ajustements fine
    - 🚀 Nouveaux concepts
    
    **ROI**: +€500K
    """)

# KPIs de suivi
st.markdown("---")
st.markdown("## 📊 Tableau de Bord de Suivi")

kpi_suivi_cols = st.columns(2)

with kpi_suivi_cols[0]:
    st.markdown("""
    ### 🎯 **KPIs Principaux**
    
    | Indicateur | Baseline | Objectif | Délai |
    |------------|----------|----------|-------|
    | CA Décembre vs Moyenne | +35% | +50% | Q4 2025 |
    | Pénétration Dept TOP 10 | 75% | 90% | Q3 2025 |
    | ROI Type C vs Type A | -25% | -15% | Q4 2025 |
    | CA/sqft Global | Actuel | +12% | Q4 2025 |
    """)

with kpi_suivi_cols[1]:
    st.markdown("""
    ### 🚨 **Alertes & Seuils**
    
    - 🔴 **Alerte Rouge**: ROI < -5% objectif
    - 🟠 **Alerte Orange**: Progression < 50% objectif
    - 🟢 **Vert**: Objectifs atteints ou dépassés
    
    **Fréquence Reporting**: Mensuel
    
    **Responsables**: 
    - Direction Générale (stratégie)
    - Directeurs Magasins (exécution)
    - Équipe Data (suivi)
    """)

# Section ressources nécessaires
st.markdown("---")
st.markdown("## 🛠️ Ressources & Prérequis")

ressources_cols = st.columns(3)

with ressources_cols[0]:
    st.markdown("""
    ### 👥 **Équipe Projet**
    - 1 Chef de Projet (0.5 ETP)
    - 3 Directeurs Magasins
    - 1 Data Analyst (0.3 ETP)
    - Support IT (ponctuel)
    """)

with ressources_cols[1]:
    st.markdown("""
    ### 💻 **Outils & Systèmes**
    - Tableau de bord BI
    - Système de gestion stocks
    - CRM pour campagnes
    - Outils de formation
    """)

with ressources_cols[2]:
    st.markdown("""
    ### 📈 **Formations**
    - Merchandising avancé
    - Analyse de performance
    - Gestion saisonnalité
    - Leadership changement
    """)

st.markdown("---")

# Call to action final
st.markdown("## 🎯 Prochaines Étapes")

st.success("""
🚀 **ACTION IMMÉDIATE RECOMMANDÉE**:

1. **Validation Direction** de ce plan d'action (Semaine 1)
2. **Constitution équipe projet** (Semaine 2) 
3. **Lancement Phase 1** - Audit départements (Semaine 3-4)
4. **Première mesure impact** (Mois 2)

💡 **Contact recommandé**: Planifier réunion de validation avec Direction Générale dans les 48h
""")

# Footer
st.markdown("---")
st.markdown("*📊 Dashboard généré automatiquement à partir des données retail • Dernière mise à jour: Décembre 2024*")

    st.success(textes.reco_conclusion)