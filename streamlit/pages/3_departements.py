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

