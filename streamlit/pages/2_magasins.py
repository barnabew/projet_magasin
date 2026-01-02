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

st.markdown("---")

st.markdown(textes.magasins_intro , unsafe_allow_html=True)

st.markdown("---")

st.markdown("### Impact des promotions sur la performance des magasins")


promo = run_query(queries.QUERY_PROMO_IMPACT)
avec_promo = round(promo["CA_Moyen"][0])
sans_promo  = round(promo["CA_Moyen"][1])
pourcentage_diff = round(((promo["CA_Moyen"][0] - promo["CA_Moyen"][1]) / promo["CA_Moyen"][1]) * 100, 2)

col1, col2, col3= st.columns(3)

with col1:
    st.markdown(styles.render_kpi_card("CA Avec Promo", f"${avec_promo}€"),unsafe_allow_html=True)
    
with col2:
    st.markdown(styles.render_kpi_card("CA Sans Promo", f"{sans_promo}€"),unsafe_allow_html=True)
    
with col3:
    st.markdown(styles.render_kpi_card("Pourcentage Différence", f"{pourcentage_diff}%"),unsafe_allow_html=True)

st.markdown(textes.magasins_promotions, unsafe_allow_html=True)


st.markdown("---")


st.markdown("### Corrélation entre la taille des magasins et leur performance")


st.plotly_chart(visuel.plot_performance_by_type(run_query(queries.QUERY_TAILLE_PERF)), use_container_width=True)


st.markdown(textes.magasins_taille_performance, unsafe_allow_html=True)
