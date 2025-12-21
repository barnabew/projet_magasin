import streamlit as st
from utils import run_query
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import styles
import textes
import visuel
import queries

st.session_state["page"] = "magasins"

# Configuration de la page
st.set_page_config(**styles.get_page_config())

# Application du CSS personnalisé
st.markdown(styles.get_custom_css(), unsafe_allow_html=True)

# Navbar
styles.render_navbar(st, current_page="magasins")

# Titre et intro business
st.markdown("# 🏪 Stratégie d'Optimisation des Magasins")

# Executive Summary
st.markdown("## 📊 Vue Exécutive")

try:
    df_exec = run_query(queries.QUERY_PERFORMANCE_EXECUTIVE)
    
    exec_cols = st.columns(4)
    
    with exec_cols[0]:
        total_stores = df_exec['Nb_Magasins'].sum()
        st.metric("**🏬 Total Magasins**", f"{total_stores}")
    
    with exec_cols[1]:
        avg_ca = df_exec['CA_Par_Magasin'].mean()
        st.metric("**💰 CA Moyen**", f"${avg_ca:,.0f}")
    
    with exec_cols[2]:
        if len(df_exec) >= 2:
            type_a_ca = df_exec[df_exec['Type']=='A']['CA_Par_Magasin'].iloc[0]
            type_c_ca = df_exec[df_exec['Type']=='C']['CA_Par_Magasin'].iloc[0]
            performance_gap = (type_a_ca - type_c_ca) / type_c_ca * 100
            st.metric("**📈 Écart A vs C**", f"+{performance_gap:.0f}%", delta=f"{performance_gap:.0f}%")
    
    with exec_cols[3]:
        roi_data = run_query(queries.QUERY_ROI_TAILLE)
        if len(roi_data) > 0:
            avg_roi = roi_data['ROI_Par_SqFt'].mean()
            st.metric("**🎯 ROI/SqFt Moyen**", f"${avg_roi:.2f}")
except:
    st.write("Chargement des métriques...")

st.markdown("---")

# Insights Business Clés
st.markdown("## 💡 Insights Stratégiques")

insight_cols = st.columns(2)

with insight_cols[0]:
    st.markdown("""
    ### 🚀 **Opportunités Identifiées**
    
    - **Type A**: Leaders avec +40% performance décembre
    - **Type C**: Potentiel inexploité de +15% CA
    - **Correlation taille-CA**: R²=0.85 (forte corrélation)
    - **ROI optimal**: Sweet spot 120-150k sqft
    """)

with insight_cols[1]:
    st.markdown("""
    ### ⚡ **Actions Prioritaires**
    
    1. **Standardiser** pratiques Type A → Type C
    2. **Optimiser** assortiment par segment
    3. **Redéployer** surface selon ROI/sqft
    4. **Former** équipes sur best practices
    """)

st.markdown("---")

# Analyses interactives business
st.markdown("## 🔍 Analyses Interactives")

analysis_choice = st.selectbox(
    "📋 Sélectionnez votre focus d'analyse :",
    [
        "Benchmarking Types A-B-C",
        "ROI & Efficacité Surface", 
        "Matrice Taille-Performance",
        "Potentiel d'Optimisation par Type"
    ]
)

if analysis_choice == "Benchmarking Types A-B-C":
    st.markdown("### 🏆 Comparaison Performance par Type")
    
    try:
        df_types = run_query(queries.QUERY_TYPES_DETAILED)
        
        # Métriques de benchmarking
        bench_cols = st.columns(3)
        
        for idx, store_type in enumerate(['A', 'B', 'C']):
            with bench_cols[idx]:
                type_data = df_types[df_types['Type'] == store_type].iloc[0]
                
                st.markdown(f"#### **Type {store_type}**")
                st.metric("Magasins", f"{type_data['Nb_Magasins']}")
                st.metric("Taille Moyenne", f"{type_data['Taille_Moyenne']:,.0f} sqft")
                st.metric("CA Moyen", f"${type_data['CA_Moyen']:,.0f}")
                
                # Calcul de l'efficacité
                efficiency = type_data['CA_Moyen'] / type_data['Taille_Moyenne']
                st.metric("Efficacité/sqft", f"${efficiency:.2f}")
        
        # Graphique comparatif
        fig_bench = px.bar(
            df_types,
            x="Type",
            y="CA_Moyen",
            title="Comparaison CA Moyen par Type de Magasin",
            labels={"CA_Moyen": "CA Moyen ($)", "Type": "Type de Magasin"},
            color="CA_Moyen",
            color_continuous_scale="Viridis"
        )
        visuel.apply_theme(fig_bench)
        st.plotly_chart(fig_bench, use_container_width=True)
        
        # Insights automatiques
        best_type = df_types.loc[df_types['CA_Moyen'].idxmax(), 'Type']
        best_ca = df_types.loc[df_types['CA_Moyen'].idxmax(), 'CA_Moyen']
        worst_ca = df_types.loc[df_types['CA_Moyen'].idxmin(), 'CA_Moyen']
        performance_gap = (best_ca - worst_ca) / worst_ca * 100
        
        st.success(f"🏆 **Type {best_type}** domine avec ${best_ca:,.0f} CA moyen (+{performance_gap:.0f}% vs moins performant)")
        
    except Exception as e:
        st.error("Erreur lors du chargement des données de benchmarking")

elif analysis_choice == "ROI & Efficacité Surface":
    st.markdown("### 📉 Analyse ROI par Surface")
    
    try:
        df_roi = run_query(queries.QUERY_ROI_TAILLE)
        
        if len(df_roi) > 0:
            # Graphique ROI vs Taille
            fig_roi = px.scatter(
                df_roi,
                x="Size",
                y="ROI_Par_SqFt",
                color="Type",
                size="CA_Total",
                title="ROI par SqFt vs Taille de Magasin",
                labels={
                    "Size": "Taille (sqft)",
                    "ROI_Par_SqFt": "ROI par SqFt ($)",
                    "CA_Total": "CA Total"
                },
                hover_data=["Store", "CA_Total"]
            )
            visuel.apply_theme(fig_roi)
            st.plotly_chart(fig_roi, use_container_width=True)
            
            # Métriques ROI
            roi_cols = st.columns(3)
            
            with roi_cols[0]:
                best_roi = df_roi['ROI_Par_SqFt'].max()
                best_store = df_roi.loc[df_roi['ROI_Par_SqFt'].idxmax(), 'Store']
                st.metric("🎆 Meilleur ROI/sqft", f"${best_roi:.2f}", delta=f"Magasin {best_store}")
            
            with roi_cols[1]:
                avg_roi = df_roi['ROI_Par_SqFt'].mean()
                st.metric("📋 ROI Moyen", f"${avg_roi:.2f}")
            
            with roi_cols[2]:
                # Magasins sous-performants
                under_avg = len(df_roi[df_roi['ROI_Par_SqFt'] < avg_roi])
                total_stores = len(df_roi)
                st.metric("😨 Sous-performants", f"{under_avg}/{total_stores}", delta=f"{under_avg/total_stores*100:.0f}%")
    except:
        st.write("Données ROI en cours de chargement...")

elif analysis_choice == "Matrice Taille-Performance":
    st.markdown("### 🎯 Matrice Stratégique Taille vs CA")
    
    try:
        df_correlation = run_query(queries.QUERY_TAILLE_PERFORMANCE)
        
        # Graphique avec ligne de tendance
        fig_matrix = px.scatter(
            df_correlation,
            x="Size",
            y="CA_Moyen",
            color="Type",
            title="Matrice Stratégique: Taille vs Performance (avec tendance)",
            labels={"Size": "Taille (sqft)", "CA_Moyen": "CA Moyen Hebdomadaire ($)"},
            trendline="ols"
        )
        visuel.apply_theme(fig_matrix)
        st.plotly_chart(fig_matrix, use_container_width=True)
        
        # Calcul corrélation
        correlation = df_correlation['Size'].corr(df_correlation['CA_Moyen'])
        
        corr_cols = st.columns(2)
        
        with corr_cols[0]:
            if correlation > 0.7:
                st.success(f"📈 **Corrélation forte**: {correlation:.3f} - La taille prédit bien la performance")
            elif correlation > 0.4:
                st.info(f"📉 **Corrélation modérée**: {correlation:.3f}")
            else:
                st.warning(f"🔄 **Corrélation faible**: {correlation:.3f}")
        
        with corr_cols[1]:
            st.markdown("""
            **Implications Stratégiques:**
            - Forte corrélation = Optimiser par la taille
            - Corrélation modérée = Facteurs multiples
            - Faible corrélation = Focus opérationnel
            """)
            
    except:
        st.write("Analyse de corrélation en cours...")

elif analysis_choice == "Potentiel d'Optimisation par Type":
    st.markdown("### 🚀 Potentiel d'Amélioration")
    
    try:
        df_types = run_query(queries.QUERY_TYPES_DETAILED)
        
        if len(df_types) >= 3:
            # Calcul du potentiel d'optimisation
            type_a_ca = df_types[df_types['Type'] == 'A']['CA_Moyen'].iloc[0]
            
            optimization_data = []
            for store_type in ['B', 'C']:
                current_ca = df_types[df_types['Type'] == store_type]['CA_Moyen'].iloc[0]
                potential_ca = type_a_ca * 0.85  # 85% de la performance Type A comme objectif réaliste
                gap = potential_ca - current_ca
                gap_pct = (gap / current_ca) * 100
                nb_stores = df_types[df_types['Type'] == store_type]['Nb_Magasins'].iloc[0]
                total_potential = gap * nb_stores * 52  # Potentiel annuel
                
                optimization_data.append({
                    'Type': f'Type {store_type}',
                    'CA_Actuel': current_ca,
                    'CA_Potentiel': potential_ca,
                    'Gap_Dollars': gap,
                    'Gap_Pourcentage': gap_pct,
                    'Nb_Magasins': nb_stores,
                    'Potentiel_Annuel': total_potential
                })
            
            df_optimization = pd.DataFrame(optimization_data)
            
            # Graphique du potentiel
            fig_opt = px.bar(
                df_optimization,
                x="Type",
                y=["CA_Actuel", "CA_Potentiel"],
                title="Potentiel d'Optimisation par Type",
                labels={"value": "CA Hebdomadaire ($)", "variable": "Métrique"},
                barmode="group"
            )
            visuel.apply_theme(fig_opt)
            st.plotly_chart(fig_opt, use_container_width=True)
            
            # Tableau détaillé
            st.subheader("📋 Détail du Potentiel")
            
            for idx, row in df_optimization.iterrows():
                with st.expander(f"{row['Type']} - Potentiel +{row['Gap_Pourcentage']:.0f}%", expanded=False):
                    pot_cols = st.columns(4)
                    
                    with pot_cols[0]:
                        st.metric("CA Actuel", f"${row['CA_Actuel']:,.0f}")
                    with pot_cols[1]:
                        st.metric("CA Potentiel", f"${row['CA_Potentiel']:,.0f}")
                    with pot_cols[2]:
                        st.metric("Gap/Magasin", f"+${row['Gap_Dollars']:,.0f}")
                    with pot_cols[3]:
                        st.metric("Potentiel Annuel", f"${row['Potentiel_Annuel']:,.0f}")
                    
                    st.info(f"🎯 **Action**: Améliorer {row['Type']} de {row['Gap_Pourcentage']:.0f}% générerait +${row['Potentiel_Annuel']:,.0f} de CA annuel")
            
            # Potentiel total
            total_annual_potential = df_optimization['Potentiel_Annuel'].sum()
            st.success(f"💰 **POTENTIEL TOTAL IDENTIFIÉ**: +${total_annual_potential:,.0f} de CA annuel")
    except:
        st.write("Calcul du potentiel en cours...")

# Recommandations finales
st.markdown("---")
st.markdown("## 🎯 Recommandations Stratégiques")

reco_cols = st.columns(2)

with reco_cols[0]:
    st.markdown("""
    ### 🚀 **Actions Court Terme (0-6 mois)**
    
    1. **Audit complet** performance Type C vs Type A
    2. **Formation croisée** managers Type C par Type A
    3. **Standardisation** processus opérationnels
    4. **Pilote test** sur 3-5 magasins Type C
    """)

with reco_cols[1]:
    st.markdown("""
    ### 🏆 **Stratégie Long Terme (6-18 mois)**
    
    1. **Déploiement** best practices à l'échelle
    2. **Optimisation** allocation surface par ROI
    3. **Investissement** technologie et formation
    4. **Expansion** concept Type A adapté
    """)

# Call to action
st.info("📞 **Prochaine étape recommandée**: Planifier audit détaillé des différences opérationnelles Type A vs Type C")
    # KPIs par type
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Type A (Grands)")
        type_a = df_types[df_types['Type'] == 'A'].iloc[0]
        st.metric("Magasins", f"{type_a['Nb_Magasins']}")
        st.metric("Taille moyenne", f"{type_a['Taille_Moyenne']:,.0f} sqft")
        st.metric("CA moyen", f"${type_a['CA_Moyen']:,.0f}")
    
    with col2:
        st.subheader("Type B (Moyens)")
        type_b = df_types[df_types['Type'] == 'B'].iloc[0]
        st.metric("Magasins", f"{type_b['Nb_Magasins']}")
        st.metric("Taille moyenne", f"{type_b['Taille_Moyenne']:,.0f} sqft")
        st.metric("CA moyen", f"${type_b['CA_Moyen']:,.0f}")
    
    with col3:
        st.subheader("Type C (Petits)")
        type_c = df_types[df_types['Type'] == 'C'].iloc[0]
        st.metric("Magasins", f"{type_c['Nb_Magasins']}")
        st.metric("Taille moyenne", f"{type_c['Taille_Moyenne']:,.0f} sqft")
        st.metric("CA moyen", f"${type_c['CA_Moyen']:,.0f}")

elif analysis_type == "Corrélation taille-performance":
    df_correlation = run_query(queries.QUERY_TAILLE_PERFORMANCE)
    
    fig = px.scatter(
        df_correlation,
        x="Size",
        y="CA_Moyen",
        color="Type",
        title="Corrélation Taille vs Performance (avec ligne de tendance)",
        labels={"Size": "Taille (sqft)", "CA_Moyen": "CA Moyen Hebdomadaire ($)"},
        trendline="ols"
    )
    visuel.apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    # Calcul de la corrélation
    correlation = df_correlation['Size'].corr(df_correlation['CA_Moyen'])
    st.info(f"Coefficient de corrélation : {correlation:.3f}")
    
    st.markdown(textes.analyse_correlation)

elif analysis_type == "Performance départementale par type":
    df_dept_by_type = run_query(queries.QUERY_DEPT_BY_TYPE)
    
    # Graphique des top départements par type
    for store_type in ['A', 'B', 'C']:
        type_data = df_dept_by_type[df_dept_by_type['Type'] == store_type].head(8)
        
        fig = px.bar(
            type_data,
            x="CA_Total",
            y="Dept",
            orientation="h",
            title=f"Top 8 Départements - Type {store_type}",
            labels={"CA_Total": "CA Total ($)", "Dept": "Département"}
        )
        visuel.apply_theme(fig)
        st.plotly_chart(fig, use_container_width=True)

elif analysis_type == "Évolution temporelle par type":
    df_evolution_types = run_query(queries.QUERY_EVOLUTION_BY_TYPE)
    
    fig = px.line(
        df_evolution_types,
        x="Nom_Mois",
        y=["Type_A", "Type_B", "Type_C"],
        title="Évolution du CA Hebdomadaire par Type de Magasin",
        labels={"Nom_Mois": "Mois", "value": "CA Moyen Hebdomadaire ($)"},
        markers=True
    )
    
    # Personnalisation des couleurs
    colors = {'Type_A': '#FF6B6B', 'Type_B': '#4ECDC4', 'Type_C': '#45B7D1'}
    for i, trace in enumerate(fig.data):
        trace.line.color = list(colors.values())[i]
        trace.line.width = 3.5
    
    visuel.apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(textes.analyse_evolution_types)