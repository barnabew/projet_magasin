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

st.markdown("### 1. Performance par Type de Magasin")

st.markdown("testé")
visuel.plot_performance_by_type(run_query(queries.QUERY_TAILLE_PERFORMANCE))