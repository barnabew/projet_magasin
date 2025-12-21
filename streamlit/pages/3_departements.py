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

try:
    # Données des départements opportunités
    df_opport = run_query(queries.QUERY_DEPARTEMENTS_OPPORTUNITE)
    df_top10 = run_query(queries.QUERY_TOP10_VARIATION_DECEMBRE)
    
    perf_cols = st.columns(4)
    
    with perf_cols[0]:
        st.metric("**🏆 Départements Actifs**", "81")
    
    with perf_cols[1]:
        if len(df_opport) > 0:
            total_potential = df_opport['Potentiel_CA_Supplementaire'].sum()
            st.metric("**💎 Potentiel Total**", f"${total_potential:,.0f}", delta="Identifié")
    
    with perf_cols[2]:
        if len(df_top10) > 0:
            dec_boost = df_top10['Variation_Pourcentage'].mean()
            st.metric("**🎄 Boost Décembre**", f"+{dec_boost:.0f}%", delta="Top 10")
    
    with perf_cols[3]:
        # Champions départementaux
        df_champions = run_query(queries.get_query_departements_champions(50))
        if len(df_champions) > 0:
            champions_count = len(df_champions)
            st.metric("**⭐ Départements Champions**", f"{champions_count}", delta="+50% présence")
except:
    st.write("Chargement des métriques...")

st.markdown("---")

# Vue stratégique
st.markdown("## 🎯 Vision Stratégique des Départements")

# Analyses par priorité business
analysis_focus = st.selectbox(
    "🎯 Sélectionnez votre focus stratégique :",
    [
        "Top Opportunités Départementales",
        "Champions & Best Performers", 
        "Potentiel Saisonnier Décembre",
        "Analyse Comparative par Type Magasin"
    ]
)

if analysis_focus == "Top Opportunités Départementales":
    st.markdown("### 💎 Top Opportunités d'Amélioration")
    
    try:
        df_opportunities = run_query(queries.QUERY_DEPARTEMENTS_OPPORTUNITE)
        
        if len(df_opportunities) > 0:
            # Top 10 des opportunités
            top_opport = df_opportunities.head(10)
            
            # Graphique des opportunités
            fig_opport = px.bar(
                top_opport,
                x="Dept",
                y="Potentiel_CA_Supplementaire",
                text="Pct_Amelioration",
                title="Top 10 Départements à Fort Potentiel",
                labels={
                    "Dept": "Département",
                    "Potentiel_CA_Supplementaire": "Potentiel CA Supplémentaire ($)"
                },
                color="Pct_Amelioration",
                color_continuous_scale="Viridis"
            )
            fig_opport.update_traces(texttemplate='%{text:.0f}%', textposition='outside')
            visuel.apply_theme(fig_opport)
            st.plotly_chart(fig_opport, use_container_width=True)
            
            # Métriques d'opportunités
            opp_cols = st.columns(4)
            
            with opp_cols[0]:
                total_potential = top_opport['Potentiel_CA_Supplementaire'].sum()
                st.metric("💰 Potentiel Top 10", f"${total_potential:,.0f}")
            
            with opp_cols[1]:
                avg_improvement = top_opport['Pct_Amelioration'].mean()
                st.metric("📈 Amélioration Moyenne", f"+{avg_improvement:.0f}%")
            
            with opp_cols[2]:
                best_dept = top_opport.iloc[0]['Dept']
                best_potential = top_opport.iloc[0]['Potentiel_CA_Supplementaire']
                st.metric("🏆 Meilleure Opportunité", f"Dept {best_dept}", delta=f"${best_potential:,.0f}")
            
            with opp_cols[3]:
                high_impact = len(top_opport[top_opport['Pct_Amelioration'] > 20])
                st.metric("🚀 Impact Élevé (+20%)", f"{high_impact} dépts")
            
            # Détail des top 3
            st.subheader("🎆 Top 3 Priorités Immédiates")
            
            for i in range(min(3, len(top_opport))):
                dept = top_opport.iloc[i]
                with st.expander(f"🎯 Département {dept['Dept']} - Potentiel +{dept['Pct_Amelioration']:.0f}%", expanded=i==0):
                    detail_cols = st.columns(3)
                    
                    with detail_cols[0]:
                        st.metric("CA Actuel", f"${dept['CA_Actuel']:,.0f}")
                        st.metric("CA Potentiel", f"${dept['CA_Potentiel']:,.0f}")
                    
                    with detail_cols[1]:
                        st.metric("Gain Possible", f"${dept['Potentiel_CA_Supplementaire']:,.0f}")
                        st.metric("% Amélioration", f"+{dept['Pct_Amelioration']:.1f}%")
                    
                    with detail_cols[2]:
                        st.markdown("""
                        **Actions Recommandées:**
                        1. Audit assortiment vs leaders
                        2. Formation équipes spécialisées  
                        3. Optimisation merchandising
                        4. Campagne marketing ciblée
                        """)
    except:
        st.write("Chargement des opportunités...")

elif analysis_focus == "Champions & Best Performers":
    st.markdown("### 🏆 Départements Champions")
    
    presence_threshold = st.slider("Seuil minimum de présence (%) :", 30, 100, 60)
    
    try:
        df_champions = run_query(queries.get_query_departements_champions(presence_threshold))
        
        if len(df_champions) > 0:
            # Graphique des champions
            fig_champ = px.bar(
                df_champions.head(15),
                x="CA_Total",
                y="Dept",
                orientation="h",
                title=f"Top 15 Départements Champions (>{presence_threshold}% présence)",
                labels={"CA_Total": "CA Total ($)", "Dept": "Département"},
                color="CA_Total",
                color_continuous_scale="Blues"
            )
            visuel.apply_theme(fig_champ)
            st.plotly_chart(fig_champ, use_container_width=True)
            
            # Statistiques champions
            champ_cols = st.columns(4)
            
            with champ_cols[0]:
                total_champions = len(df_champions)
                st.metric("🏆 Champions Identifiés", f"{total_champions}")
            
            with champ_cols[1]:
                total_ca_champions = df_champions['CA_Total'].sum()
                st.metric("💰 CA Champions", f"${total_ca_champions:,.0f}")
            
            with champ_cols[2]:
                avg_presence = df_champions['Taux_Presence'].mean()
                st.metric("🎯 Présence Moyenne", f"{avg_presence:.0f}%")
            
            with champ_cols[3]:
                universal_champs = len(df_champions[df_champions['Taux_Presence'] >= 90])
                st.metric("🌍 Universels (>90%)", f"{universal_champs}")
    except:
        st.write("Analyse des champions en cours...")

elif analysis_focus == "Potentiel Saisonnier Décembre":
    st.markdown("### 🎄 Analyse du Pic de Décembre")
    
    try:
        df_december = run_query(queries.QUERY_TOP10_VARIATION_DECEMBRE)
        
        if len(df_december) > 0:
            # Graphique du top 10 décembre
            fig_dec = px.bar(
                df_december,
                x="Departement",
                y="Variation_Pourcentage",
                title="Top 10 Départements - Variation Décembre",
                labels={"Departement": "Département", "Variation_Pourcentage": "Variation (%)"},
                color="CA_Decembre",
                color_continuous_scale="Reds"
            )
            visuel.apply_theme(fig_dec)
            st.plotly_chart(fig_dec, use_container_width=True)
            
            # Métriques saisonnières
            dec_cols = st.columns(4)
            
            with dec_cols[0]:
                avg_boost = df_december['Variation_Pourcentage'].mean()
                st.metric("📈 Boost Moyen", f"+{avg_boost:.0f}%")
            
            with dec_cols[1]:
                best_dept = df_december.iloc[0]['Departement']
                best_boost = df_december.iloc[0]['Variation_Pourcentage']
                st.metric("🏆 Champion Décembre", f"Dept {best_dept}", delta=f"+{best_boost:.0f}%")
            
            with dec_cols[2]:
                total_dec_ca = df_december['CA_Decembre'].sum()
                total_avg_ca = df_december['CA_Moyen_Annuel'].sum()
                overall_boost = (total_dec_ca / total_avg_ca - 1) * 100
                st.metric("🎄 Boost Global Top 10", f"+{overall_boost:.0f}%")
            
            with dec_cols[3]:
                high_performers = len(df_december[df_december['Variation_Pourcentage'] > 50])
                st.metric("🚀 Super Performers (+50%)", f"{high_performers}")
            
            # Plan d'action décembre
            st.subheader("🎯 Plan d'Action Décembre")
            
            action_cols = st.columns(2)
            
            with action_cols[0]:
                st.markdown("""
                **📦 Préparation Stocks (Nov-Déc)**
                - Augmenter stocks top 10 de +40%
                - Commandes anticipées dès octobre
                - Buffer de sécurité sur best performers
                - Monitoring quotidien ruptures
                """)
            
            with action_cols[1]:
                st.markdown("""
                **📊 Activation Marketing**
                - Campagnes ciblées par département
                - Promotions croisées intelligentes
                - Merchandising premium décembre
                - Formation équipes vente spécialisée
                """)
    except:
        st.write("Analyse saisonnière en cours...")

elif analysis_focus == "Analyse Comparative par Type Magasin":
    st.markdown("### 🏢 Performance Départementale par Type")
    
    store_type = st.selectbox("Choisissez le type de magasin :", ["A", "B", "C"])
    
    try:
        df_type_perf = run_query(queries.get_query_perf_by_type(store_type))
        
        if len(df_type_perf) > 0:
            # Performance par type
            fig_type = px.bar(
                df_type_perf.head(12),
                x="Dept",
                y="CA_Moyen",
                title=f"Top 12 Départements - Magasins Type {store_type}",
                labels={"Dept": "Département", "CA_Moyen": "CA Moyen ($)"},
                color="CA_Moyen",
                color_continuous_scale="Plasma"
            )
            visuel.apply_theme(fig_type)
            st.plotly_chart(fig_type, use_container_width=True)
            
            # Comparaison avec autres types
            compare_cols = st.columns(3)
            
            for i, comp_type in enumerate(['A', 'B', 'C']):
                with compare_cols[i]:
                    if comp_type == store_type:
                        st.success(f"🎯 **Type {comp_type}** (Sélectionné)")
                        top_dept_ca = df_type_perf.iloc[0]['CA_Moyen']
                        st.metric("Top Département", f"${top_dept_ca:,.0f}")
                    else:
                        st.info(f"Type {comp_type} (Comparaison)")
                        # Ici on pourrait ajouter une comparaison avec les autres types
    except:
        st.write(f"Analyse Type {store_type} en cours...")

# Recommandations départementales
st.markdown("---")
st.markdown("## 🎯 Recommandations Départementales")

reco_dept_cols = st.columns(2)

with reco_dept_cols[0]:
    st.markdown("""
    ### 🚀 **Priorités Court Terme**
    
    1. **Focus Top 10 Opportunités**: Investir sur potentiel identifié
    2. **Préparation Décembre**: Stocks et marketing départements saisonniers
    3. **Standardisation**: Déployer champions dans sous-performants
    4. **Formation**: Équipes spécialisées par catégorie
    """)

with reco_dept_cols[1]:
    st.markdown("""
    ### 🏆 **Stratégie Long Terme**
    
    1. **Expansion Champions**: Deployer universellement top performers
    2. **Innovation**: Nouveaux départements à fort potentiel
    3. **Spécialisation**: Créer expertises métier uniques
    4. **Data-Driven**: Pilotage par analytics avancées
    """)
        x="CA_Total",
        y="Dept",
        orientation="h",
        title="Top 15 Départements Champions (CA Total)",
        labels={"CA_Total": "Chiffre d'affaires total ($)", "Dept": "Département"}
    )
    visuel.apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

# Section 3: Départements spécialisés
with st.expander("Départements Spécialisés – Niches Rentables", expanded=False):
    st.markdown(textes.analyse_specialises)
    
    max_presence = st.slider("Seuil maximum de présence (%) :", 10, 50, 30, key="slider_specialises")
    
    df_specialises = run_query(queries.get_query_departements_specialises(max_presence))

    fig = px.scatter(
        df_specialises,
        x="Taux_Presence",
        y="CA_Moyen_Magasin",
        size="CA_Total",
        hover_data=["Dept", "Nb_Magasins"],
        title="Départements Spécialisés : Exclusivité vs Performance",
        labels={
            "Taux_Presence": "Taux de présence (%)",
            "CA_Moyen_Magasin": "CA moyen par magasin ($)"
        }
    )
    visuel.apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)

# Section 4: Performance par type de magasin
with st.expander("Performance Départementale par Type de Magasin", expanded=False):
    st.markdown(textes.analyse_perf_par_type)
    
    type_selected = st.selectbox("Choisissez un type de magasin :", ["A", "B", "C"])
    
    df_perf_type = run_query(queries.get_query_perf_by_type(type_selected))

    fig = px.bar(
        df_perf_type.head(10),
        x="Dept",
        y="CA_Moyen",
        title=f"Top 10 Départements - Magasins Type {type_selected}",
        labels={"Dept": "Département", "CA_Moyen": "CA Moyen ($)"}
    )
    visuel.apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)