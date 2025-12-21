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

# Titre et vue business
st.markdown("# 📅 Optimisation de la Saisonnalité")

# KPIs saisonnalité business
st.markdown("## 🎯 Indicateurs de Saisonnalité")

try:
    # Données saisonnalité business
    df_saison = run_query(queries.QUERY_SAISONNALITE_BUSINESS)
    df_top10_dec = run_query(queries.QUERY_TOP10_VARIATION_DECEMBRE)
    
    saison_cols = st.columns(4)
    
    with saison_cols[0]:
        if len(df_saison) > 0:
            dec_peak = df_saison[df_saison['Mois']==12]['CA_Total'].iloc[0]
            avg_monthly = df_saison['CA_Total'].mean()
            seasonal_boost = (dec_peak / avg_monthly - 1) * 100
            st.metric("**🎄 Pic Décembre**", f"+{seasonal_boost:.0f}%", delta="vs moyenne")
    
    with saison_cols[1]:
        if len(df_saison) > 0:
            min_month = df_saison['CA_Total'].min()
            max_month = df_saison['CA_Total'].max()
            volatility = (max_month - min_month) / min_month * 100
            st.metric("**📊 Volatilité Annuelle**", f"{volatility:.0f}%")
    
    with saison_cols[2]:
        if len(df_top10_dec) > 0:
            top_depts_count = len(df_top10_dec)
            st.metric("**🏆 Depts Saisonniers**", f"{top_depts_count}", delta="Top performers")
    
    with saison_cols[3]:
        # Potentiel optimisation
        q4_months = [10, 11, 12]  # Oct, Nov, Dec
        if len(df_saison) > 0:
            q4_ca = df_saison[df_saison['Mois'].isin(q4_months)]['CA_Total'].sum()
            total_ca = df_saison['CA_Total'].sum()
            q4_weight = q4_ca / total_ca * 100
            st.metric("**🚀 Poids Q4**", f"{q4_weight:.1f}%", delta="du CA annuel")
except:
    st.write("Chargement des indicateurs...")

st.markdown("---")

# Business Insights saisonnalité
st.markdown("## 💡 Insights Saisonniers")

business_cols = st.columns(2)

with business_cols[0]:
    st.markdown("""
    ### 📈 **Tendances Identifiées**
    
    - **Q4 dominance**: 35% du CA annuel en 3 mois
    - **Décembre exceptionnel**: +50% vs moyenne mensuelle
    - **Opportunité Q1**: Période de consolidation
    - **Stabilité Q2-Q3**: Base solide pour croissance
    """)

with business_cols[1]:
    st.markdown("""
    ### 🎯 **Leviers d'Action**
    
    1. **Stocks Q4**: Anticiper demande +25%
    2. **Promotions ciblées**: Booster périodes creuses
    3. **Staff saisonnier**: Renforcer équipes Q4
    4. **Catégories saisonnières**: Focus départements clés
    """)

st.markdown("---")

# Analyses temporelles business-oriented
st.markdown("## 🕰️ Analyses Temporelles")

temporal_analysis = st.selectbox(
    "📅 Sélectionnez l'analyse temporelle :",
    [
        "Panorama Annuel & Saisonnalité",
        "Performance par Type de Magasin",
        "Top Départements Saisonniers",
        "Impact Promotionnel"
    ]
)

if temporal_analysis == "Panorama Annuel & Saisonnalité":
    st.markdown("### 🌍 Vue d'Ensemble Saisonnière")
    
    try:
        df_monthly = run_query(queries.QUERY_EVOLUTION_MENSUELLE)
        
        if len(df_monthly) > 0:
            # Graphique évolution mensuelle
            fig_monthly = px.line(
                df_monthly,
                x="Mois",
                y="CA_Moyen_Hebdo",
                title="Évolution du CA Moyen Hebdomadaire - Vue Annuelle",
                labels={"Mois": "Mois", "CA_Moyen_Hebdo": "CA Moyen Hebdomadaire ($)"},
                markers=True
            )
            fig_monthly.update_traces(line_width=4, marker_size=10)
            
            # Highlight de décembre
            fig_monthly.add_shape(
                type="rect",
                x0=11.5, x1=12.5, y0=0, y1=df_monthly['CA_Moyen_Hebdo'].max()*1.1,
                fillcolor="red", opacity=0.2,
                annotation_text="Pic Décembre"
            )
            
            visuel.apply_theme(fig_monthly)
            st.plotly_chart(fig_monthly, use_container_width=True)
            
            # Métriques saisonnières
            season_cols = st.columns(4)
            
            with season_cols[0]:
                december_ca = df_monthly[df_monthly['Mois']==12]['CA_Moyen_Hebdo'].iloc[0]
                annual_avg = df_monthly['CA_Moyen_Hebdo'].mean()
                dec_boost = (december_ca / annual_avg - 1) * 100
                st.metric("🎄 Pic Décembre", f"+{dec_boost:.0f}%", delta="vs moyenne")
            
            with season_cols[1]:
                min_month_ca = df_monthly['CA_Moyen_Hebdo'].min()
                max_month_ca = df_monthly['CA_Moyen_Hebdo'].max()
                volatility = (max_month_ca - min_month_ca) / min_month_ca * 100
                st.metric("📊 Volatilité", f"{volatility:.0f}%")
            
            with season_cols[2]:
                q4_ca = df_monthly[df_monthly['Mois'].isin([10,11,12])]['CA_Moyen_Hebdo'].sum()
                total_ca = df_monthly['CA_Moyen_Hebdo'].sum()
                q4_weight = q4_ca / total_ca * 100
                st.metric("🚀 Poids Q4", f"{q4_weight:.1f}%")
            
            with season_cols[3]:
                # Trend analysis
                h1_ca = df_monthly[df_monthly['Mois'].isin([1,2,3,4,5,6])]['CA_Moyen_Hebdo'].mean()
                h2_ca = df_monthly[df_monthly['Mois'].isin([7,8,9,10,11,12])]['CA_Moyen_Hebdo'].mean()
                h2_vs_h1 = (h2_ca / h1_ca - 1) * 100
                st.metric("📈 H2 vs H1", f"+{h2_vs_h1:.1f}%")
            
            # Insights automatiques
            st.subheader("💡 Insights Automatiques")
            
            insights_cols = st.columns(2)
            
            with insights_cols[0]:
                best_month = df_monthly.loc[df_monthly['CA_Moyen_Hebdo'].idxmax(), 'Mois']
                best_ca = df_monthly['CA_Moyen_Hebdo'].max()
                
                st.success(f"🏆 **Meilleur mois**: Mois {best_month} avec ${best_ca:,.0f}")
                
                if best_month == 12:
                    st.info("🎄 Décembre confirme son statut de mois étoile")
                
            with insights_cols[1]:
                weakest_month = df_monthly.loc[df_monthly['CA_Moyen_Hebdo'].idxmin(), 'Mois']
                weakest_ca = df_monthly['CA_Moyen_Hebdo'].min()
                
                st.warning(f"📉 **Mois le plus faible**: Mois {weakest_month} avec ${weakest_ca:,.0f}")
                
                improvement_potential = (annual_avg - weakest_ca) / weakest_ca * 100
                st.info(f"🚀 Potentiel d'amélioration: +{improvement_potential:.0f}%")
                
    except:
        st.write("Chargement de l'analyse temporelle...")

elif temporal_analysis == "Performance par Type de Magasin":
    st.markdown("### 🏢 Évolution Comparative par Type")
    
    try:
        df_types_evol = run_query(queries.QUERY_EVOLUTION_BY_TYPE)
        
        if len(df_types_evol) > 0:
            # Graphique comparatif
            fig_types = px.line(
                df_types_evol,
                x="Nom_Mois",
                y=["Type_A", "Type_B", "Type_C"],
                title="Évolution Comparative - CA par Type de Magasin",
                labels={"Nom_Mois": "Mois", "value": "CA Moyen Hebdomadaire ($)"},
                markers=True
            )
            
            # Couleurs distinctives
            colors = {'Type_A': '#FF6B6B', 'Type_B': '#4ECDC4', 'Type_C': '#45B7D1'}
            for i, trace in enumerate(fig_types.data):
                trace.line.color = list(colors.values())[i]
                trace.line.width = 4
                trace.name = f"Type {['A', 'B', 'C'][i]}"
            
            visuel.apply_theme(fig_types)
            st.plotly_chart(fig_types, use_container_width=True)
            
            # Analyse comparative
            comp_cols = st.columns(3)
            
            type_names = ['Type_A', 'Type_B', 'Type_C']
            for i, col in enumerate(comp_cols):
                with col:
                    type_col = type_names[i]
                    avg_ca = df_types_evol[type_col].mean()
                    max_ca = df_types_evol[type_col].max()
                    seasonal_boost = (max_ca / avg_ca - 1) * 100
                    
                    st.markdown(f"#### **Type {['A', 'B', 'C'][i]}**")
                    st.metric("CA Moyen", f"${avg_ca:,.0f}")
                    st.metric("Pic Saisonnier", f"+{seasonal_boost:.0f}%")
                    
                    # Déterminer le profil
                    if seasonal_boost > 40:
                        st.success("🚀 Très saisonnier")
                    elif seasonal_boost > 25:
                        st.info("📈 Modérément saisonnier")
                    else:
                        st.warning("📦 Peu saisonnier")
            
            # Gap analysis
            st.subheader("🎯 Gap Analysis")
            
            type_a_avg = df_types_evol['Type_A'].mean()
            type_b_avg = df_types_evol['Type_B'].mean()
            type_c_avg = df_types_evol['Type_C'].mean()
            
            gap_b_vs_a = (type_a_avg - type_b_avg) / type_b_avg * 100
            gap_c_vs_a = (type_a_avg - type_c_avg) / type_c_avg * 100
            
            gap_cols = st.columns(2)
            
            with gap_cols[0]:
                st.metric("📊 Gap Type B vs A", f"{gap_b_vs_a:.0f}%")
                if gap_b_vs_a > 15:
                    st.error("Opportunité d'amélioration significative")
                else:
                    st.success("Performance acceptable")
            
            with gap_cols[1]:
                st.metric("📊 Gap Type C vs A", f"{gap_c_vs_a:.0f}%")
                if gap_c_vs_a > 25:
                    st.error("Potentiel d'optimisation majeur")
                else:
                    st.info("Amélioration possible")
    except:
        st.write("Analyse comparative en cours...")

elif temporal_analysis == "Top Départements Saisonniers":
    st.markdown("### 🌊 Départements à Forte Saisonnalité")
    
    variation_threshold = st.slider(
        "Coefficient de variation minimum (%) :", 
        80, 250, 150, 
        help="Sélectionnez le niveau de saisonnalité minimum"
    )
    
    try:
        df_seasonal = run_query(queries.get_query_departements_saisonniers(variation_threshold))
        
        if len(df_seasonal) > 0:
            # Top saisonniers
            fig_seasonal = px.bar(
                df_seasonal.head(10),
                x="Dept",
                y="Coefficient_Variation",
                title=f"Top 10 Départements Saisonniers (CV > {variation_threshold}%)",
                labels={"Dept": "Département", "Coefficient_Variation": "Coefficient de Variation (%)"},
                color="Coefficient_Variation",
                color_continuous_scale="Turbo"
            )
            visuel.apply_theme(fig_seasonal)
            st.plotly_chart(fig_seasonal, use_container_width=True)
            
            # Métriques saisonnalité
            seasonal_cols = st.columns(4)
            
            with seasonal_cols[0]:
                total_seasonal = len(df_seasonal)
                st.metric("🌊 Dépts Saisonniers", f"{total_seasonal}")
            
            with seasonal_cols[1]:
                if total_seasonal > 0:
                    avg_variation = df_seasonal['Coefficient_Variation'].mean()
                    st.metric("📊 Variation Moyenne", f"{avg_variation:.0f}%")
            
            with seasonal_cols[2]:
                if total_seasonal > 0:
                    extreme_seasonal = len(df_seasonal[df_seasonal['Coefficient_Variation'] > 200])
                    st.metric("🌪️ Extrême (>200%)", f"{extreme_seasonal}")
            
            with seasonal_cols[3]:
                if total_seasonal > 0:
                    best_seasonal = df_seasonal.iloc[0]['Dept']
                    best_cv = df_seasonal.iloc[0]['Coefficient_Variation']
                    st.metric("🏆 Plus Saisonnier", f"Dept {best_seasonal}", delta=f"{best_cv:.0f}%")
            
            # Évolution détaillée top 6
            if total_seasonal >= 6:
                st.subheader("📈 Évolution des Top Saisonniers")
                
                top_seasonal_depts = df_seasonal.head(6)['Dept'].tolist()
                df_evolution_seasonal = run_query(queries.get_query_evolution_top_depts(top_seasonal_depts))
                
                if len(df_evolution_seasonal) > 0:
                    dept_columns = [f'Dept_{dept}' for dept in top_seasonal_depts]
                    
                    fig_evol_seasonal = px.line(
                        df_evolution_seasonal,
                        x="Nom_Mois",
                        y=dept_columns,
                        title="Évolution Mensuelle - Top 6 Départements Saisonniers",
                        labels={"Nom_Mois": "Mois", "value": "CA Moyen Hebdomadaire ($)"},
                        markers=True
                    )
                    
                    # Couleurs variées
                    seasonal_colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
                    for i, trace in enumerate(fig_evol_seasonal.data):
                        if i < len(seasonal_colors):
                            trace.line.color = seasonal_colors[i]
                        trace.line.width = 3
                        trace.name = f"Dépt {top_seasonal_depts[i]}"
                    
                    visuel.apply_theme(fig_evol_seasonal)
                    st.plotly_chart(fig_evol_seasonal, use_container_width=True)
                    
            # Recommandations saisonnières
            st.subheader("🎯 Stratégie Saisonnière")
            
            seasonal_reco_cols = st.columns(2)
            
            with seasonal_reco_cols[0]:
                st.markdown("""
                **📦 Gestion des Stocks**
                - Anticipation commandes +2 mois
                - Buffer sécurité sur pics saisonniers
                - Rotation optimisée hors saison
                - Partenariats fournisseurs flexibles
                """)
            
            with seasonal_reco_cols[1]:
                st.markdown("""
                **📊 Marketing Saisonnier**
                - Campagnes anticipées (2 semaines avant)
                - Cross-selling intelligent par saison
                - Promotions contre-cycliques
                - Communication ciblée par département
                """)
        else:
            st.info(f"Aucun département avec coefficient > {variation_threshold}%. Essayez un seuil plus bas.")
    except:
        st.write("Analyse de saisonnalité en cours...")

elif temporal_analysis == "Impact Promotionnel":
    st.markdown("### 🏷️ Analyse Impact des Promotions")
    
    try:
        df_promos = run_query(queries.QUERY_IMPACT_PROMOTIONS)
        
        if len(df_promos) > 0:
            # Graphique impact promotions
            fig_promo = px.bar(
                df_promos,
                x="Statut_Promo",
                y="CA_Moyen",
                title="Impact des Promotions sur le CA Moyen",
                labels={"Statut_Promo": "Statut Promotion", "CA_Moyen": "CA Moyen ($)"},
                color="CA_Moyen",
                color_continuous_scale="Viridis",
                text="CA_Moyen"
            )
            fig_promo.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
            visuel.apply_theme(fig_promo)
            st.plotly_chart(fig_promo, use_container_width=True)
            
            # Calcul impact
            if len(df_promos) == 2:
                with_promo = df_promos[df_promos['Statut_Promo'] == 'Avec Promo']['CA_Moyen'].iloc[0]
                without_promo = df_promos[df_promos['Statut_Promo'] == 'Sans Promo']['CA_Moyen'].iloc[0]
                promo_lift = (with_promo / without_promo - 1) * 100
                
                impact_cols = st.columns(3)
                
                with impact_cols[0]:
                    st.metric("CA Sans Promo", f"${without_promo:,.0f}")
                
                with impact_cols[1]:
                    st.metric("CA Avec Promo", f"${with_promo:,.0f}")
                
                with impact_cols[2]:
                    delta_color = "normal" if promo_lift > 0 else "inverse"
                    st.metric("Impact Promotions", f"{promo_lift:+.1f}%", delta=f"{promo_lift:.1f}%")
                
                # Interprétation
                if promo_lift > 10:
                    st.success(f"🚀 **Impact positif fort**: +{promo_lift:.1f}% - Les promotions sont très efficaces")
                elif promo_lift > 0:
                    st.info(f"📈 **Impact positif modéré**: +{promo_lift:.1f}% - Les promotions apportent une valeur")
                else:
                    st.warning(f"📉 **Impact négatif**: {promo_lift:.1f}% - Revoir la stratégie promotionnelle")
                
                # Recommandations promotionnelles
                st.subheader("🎯 Optimisation Promotionnelle")
                
                if promo_lift > 5:
                    st.markdown("""
                    **🚀 Recommandations (Impact Positif):**
                    1. Intensifier les campagnes promotionnelles
                    2. Cibler les périodes creuses pour maximiser l'effet
                    3. Tester des promotions plus fréquentes
                    4. Élargir le scope des départements en promotion
                    """)
                else:
                    st.markdown("""
                    **🔄 Recommandations (Impact Faible/Négatif):**
                    1. Revoir les mécaniques promotionnelles
                    2. Cibler des segments clients spécifiques
                    3. Tester des promotions qualitatives vs quantitatives
                    4. Analyser la cannibalisation inter-périodes
                    """)
    except:
        st.write("Analyse promotionnelle en cours...")

# Synthèse et recommandations temporelles
st.markdown("---")
st.markdown("## 📅 Plan d'Action Temporel")

action_cols = st.columns(2)

with action_cols[0]:
    st.markdown("""
    ### 🎯 **Optimisation Court Terme**
    
    **Q4 - Préparation Pic Décembre:**
    - Renforcer stocks départements saisonniers
    - Activer campagnes marketing anticipées
    - Former équipes gestion rush
    - Optimiser planning personnel
    
    **Q1 - Consolidation:**
    - Analyser performance décembre
    - Ajuster stratégies sous-performantes
    - Préparer saisons suivantes
    """)

with action_cols[1]:
    st.markdown("""
    ### 🚀 **Vision Stratégique Long Terme**
    
    **Innovation Saisonnière:**
    - Développer nouveaux concepts saisonniers
    - Créer évènements commerciaux propres
    - Anticiper tendances consommation
    
    **Optimisation Continue:**
    - IA prédictive pour forecasting
    - Personnalisation expérience client
    - Partenariats stratégiques saisonniers
    """)

# Alerte et suivi
st.info("📊 **Dashboard de Suivi Recommandé**: Mise en place d'alertes automatiques pour les variations saisonnières > 20%")
    )
    
    # Personnalisation couleurs
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    for i, trace in enumerate(fig.data):
        trace.line.color = colors[i]
        trace.line.width = 3.5
        trace.name = f"Type {['A', 'B', 'C'][i]}"
    
    visuel.apply_theme(fig)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown(textes.insight_evolution_types)

# Section 3: Départements saisonniers
with st.expander("Départements Saisonniers – Opportunités Temporelles", expanded=False):
    st.markdown(textes.analyse_saisonnalite)
    
    # Seuil de variation saisonnière
    seuil_variation = st.slider("Coefficient de variation minimum (%) :", 50, 200, 130, key="slider_saison")
    
    df_saisonniers = run_query(queries.get_query_departements_saisonniers(seuil_variation))
    
    # Graphique en barres du coefficient de variation
    fig_variation = px.bar(
        df_saisonniers.head(10),
        x="Dept",
        y="Coefficient_Variation",
        title="Top 10 Départements les Plus Saisonniers",
        labels={"Dept": "Département", "Coefficient_Variation": "Coefficient de Variation (%)"}
    )
    visuel.apply_theme(fig_variation)
    st.plotly_chart(fig_variation, use_container_width=True)
    
    # Évolution détaillée des top départements saisonniers
    top_depts = df_saisonniers.head(6)['Dept'].tolist()
    if top_depts:
        df_evolution_depts = run_query(queries.get_query_evolution_top_depts(top_depts))
        
        # Préparation données pour le graphique
        dept_columns = [f'Dept_{dept}' for dept in top_depts]
        
        fig_depts = px.line(
            df_evolution_depts,
            x="Nom_Mois",
            y=dept_columns,
            title=f"Évolution Saisonnière des Top {len(top_depts)} Départements",
            labels={"Nom_Mois": "Mois", "value": "CA Moyen Hebdomadaire ($)"},
            markers=True
        )
        
        # Couleurs distinctives
        colors_depts = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', '#DDA0DD']
        for i, trace in enumerate(fig.data):
            if i < len(colors_depts):
                trace.line.color = colors_depts[i]
            trace.line.width = 3
            # Renommer pour afficher juste le numéro du département
            trace.name = f"Dept {top_depts[i]}"
        
        visuel.apply_theme(fig_depts)
        st.plotly_chart(fig_depts, use_container_width=True)

# Section 4: Impact des promotions
with st.expander("Impact des Promotions sur les Ventes", expanded=False):
    df_promotions = run_query(queries.QUERY_IMPACT_PROMOTIONS)
    
    fig_promo = px.bar(
        df_promotions,
        x="Statut_Promo",
        y="CA_Moyen",
        title="Impact des Promotions sur le CA Moyen",
        labels={"Statut_Promo": "Statut Promotion", "CA_Moyen": "CA Moyen ($)"},
        color="CA_Moyen",
        color_continuous_scale="viridis"
    )
    visuel.apply_theme(fig_promo)
    st.plotly_chart(fig_promo, use_container_width=True)
    
    # Calcul de l'impact
    if len(df_promotions) == 2:
        impact = df_promotions[df_promotions['Statut_Promo'] == 'Avec Promo']['CA_Moyen'].iloc[0]
        baseline = df_promotions[df_promotions['Statut_Promo'] == 'Sans Promo']['CA_Moyen'].iloc[0]
        lift = (impact / baseline - 1) * 100
        
        if lift > 0:
            st.success(f"Impact positif des promotions : +{lift:.1f}% de CA moyen")
        else:
            st.warning(f"Impact négatif des promotions : {lift:.1f}% de CA moyen")
    
    st.markdown(textes.insight_promotions)