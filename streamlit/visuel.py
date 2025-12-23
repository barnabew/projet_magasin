"""
visuel.py
Fonctions de visualisation extraites du notebook projet_magasin.ipynb
Toutes les visualisations utilisent Plotly pour l'interactivité
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ===========================
# CONFIGURATION THEME
# ===========================

THEME_CONFIG = {
    "paper_bgcolor": "#1e3c72",
    "plot_bgcolor": "#1e3c72", 
    "font": dict(color="#ffffff", family="Inter"),
    "title": dict(font=dict(color="#ffffff", size=16, family="Inter")),
    "xaxis": dict(
        gridcolor="#2d3142",
        color="#ffffff",
        linecolor="#2d3142"
    ),
    "yaxis": dict(
        gridcolor="#2d3142", 
        color="#ffffff",
        linecolor="#2d3142"
    ),
    "colorway": [
        "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
        "#DDA0DD", "#98D8C8", "#FDCB6E", "#6C5CE7", "#A29BFE"
    ]
}

def apply_theme(fig):
    """Applique le thème sombre retail au graphique Plotly"""
    fig.update_layout(**THEME_CONFIG)
    
    # Configuration supplémentaire pour un look moderne
    fig.update_layout(
        margin=dict(t=50, l=50, r=50, b=50),
        showlegend=True,
        legend=dict(
            bgcolor="rgba(255,255,255,0.1)",
            bordercolor="rgba(255,255,255,0.2)",
            borderwidth=1
        )
    )
    
    # Style pour les axes
    fig.update_xaxes(
        showgrid=True,
        gridwidth=1,
        gridcolor="rgba(255,255,255,0.1)"
    )
    
    fig.update_yaxes(
        showgrid=True,
        gridwidth=1, 
        gridcolor="rgba(255,255,255,0.1)"
    )
    
    return fig

# ===========================
# VISUALISATIONS DU NOTEBOOK
# ===========================

# 1. GRAPHIQUE CORRÉLATION TAILLE-PERFORMANCE
def plot_performance_by_type(df):
    """
    Graphique scatter de corrélation Taille vs Performance par type de magasin
    Avec ligne de tendance et coefficient de corrélation
    
    Args:
        df: DataFrame avec colonnes ['Store', 'Size', 'Type', 'CA_Moyen']
    Returns:
        fig: Figure Plotly
    """
    # Couleurs pour chaque type
    colors = {'A': '#FF6B6B', 'B': '#4ECDC4', 'C': '#45B7D1'}
    
    # Création du scatter plot avec Plotly Express
    fig = px.scatter(
        df,
        x='Size',
        y='CA_Moyen',
        color='Type',
        color_discrete_map=colors,
        title='Corrélation Taille-Performance par Type de Magasin',
        labels={
            'Size': 'Taille (sqft)',
            'CA_Moyen': 'CA Moyen Hebdomadaire ($)',
            'Type': 'Type de Magasin'
        },
        opacity=0.7
    )
    
    # Calcul de la ligne de tendance
    z = np.polyfit(df['Size'], df['CA_Moyen'], 1)
    p = np.poly1d(z)
    
    # Ajout de la ligne de tendance
    x_trend = np.linspace(df['Size'].min(), df['Size'].max(), 100)
    y_trend = p(x_trend)
    
    fig.add_trace(
        go.Scatter(
            x=x_trend,
            y=y_trend,
            mode='lines',
            name='Tendance',
            line=dict(color='white', dash='dash', width=2),
            opacity=0.5
        )
    )
    
    # Calcul de la corrélation
    correlation = df['Size'].corr(df['CA_Moyen'])
    
    # Ajout de l'annotation de corrélation
    fig.add_annotation(
        text=f'Corrélation: {correlation:.3f}',
        xref='paper', yref='paper',
        x=0.05, y=0.95,
        showarrow=False,
        bgcolor='rgba(255, 255, 255, 0.2)',
        bordercolor='rgba(255, 255, 255, 0.3)',
        borderwidth=1,
        font=dict(color='white', size=12)
    )
    
    apply_theme(fig)
    return fig


# 2. HEATMAP PERFORMANCE DÉPARTEMENTS PAR TYPE
def plot_heatmap_by_type(df, store_type='A'):
    """
    Heatmap des performances départementales pour un type de magasin
    
    Args:
        df: DataFrame avec colonnes ['Type', 'Store', 'Dept', 'CA_Total']
        store_type: 'A', 'B', ou 'C'
    Returns:
        fig: Figure Plotly
    """
    # Filtrer les données pour le type spécifié
    type_data = df[df['Type'] == store_type].copy()
    
    if len(type_data) == 0:
        # Retourner une figure vide si pas de données
        fig = go.Figure()
        fig.add_annotation(
            text=f"Aucune donnée pour le type {store_type}",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16, color="white")
        )
        apply_theme(fig)
        return fig
    
    # Pivot pour la heatmap
    pivot_data = type_data.pivot(index='Store', columns='Dept', values='CA_Total')
    pivot_data = pivot_data.fillna(0)
    
    # Création de la heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=pivot_data.columns,
        y=pivot_data.index,
        colorscale='YlOrRd',
        colorbar=dict(title="CA Total ($)")
    ))
    
    fig.update_layout(
        title=f'Type {store_type} - Performance par Département',
        xaxis_title='Département',
        yaxis_title='Magasin'
    )
    
    apply_theme(fig)
    return fig


# 3. GRAPHIQUE TEMPOREL PAR TYPE DE MAGASIN
def plot_evolution_temporelle_types(df):
    """
    Graphique d'évolution du CA hebdomadaire par type de magasin
    
    Args:
        df: DataFrame avec colonnes ['Nom_Mois', 'Type_A', 'Type_B', 'Type_C']
    Returns:
        fig: Figure Plotly
    """
    # Couleurs pour chaque type
    colors = {'A': '#FF6B6B', 'B': '#4ECDC4', 'C': '#45B7D1'}
    
    fig = px.line(
        df, 
        x="Nom_Mois", 
        y=["Type_A", "Type_B", "Type_C"], 
        title="CA Hebdomadaire par Type de Magasin",
        markers=True,
        color_discrete_sequence=[colors['A'], colors['B'], colors['C']],
        labels={
            'Nom_Mois': 'Mois',
            'value': 'CA Moyen Hebdomadaire ($)',
            'variable': 'Type'
        }
    )
    
    # Augmenter l'épaisseur des lignes
    fig.update_traces(line_width=3.5)
    
    # Renommer les légendes
    fig.for_each_trace(lambda t: t.update(name=t.name.replace("Type_", "Type ")))
    
    apply_theme(fig)
    return fig


# 4. GRAPHIQUE TEMPOREL DES TOP DÉPARTEMENTS
def plot_evolution_top_departements(df, top_depts):
    """
    Graphique d'évolution saisonnière des top départements
    
    Args:
        df: DataFrame avec colonnes ['Mois', 'Nom_Mois', 'Dept_X', 'Dept_Y', ...]
        top_depts: Liste des numéros de départements à afficher
    Returns:
        fig: Figure Plotly
    """
    # Colonnes des départements pour le graphique
    dept_columns = [f'Dept_{dept}' for dept in top_depts]
    
    # Palette de couleurs distinctives
    colors_depts = [
        '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7',
        '#DDA0DD', '#98D8C8', '#FDCB6E', '#6C5CE7', '#A29BFE'
    ]
    
    # Création du graphique
    fig = px.line(
        df, 
        x="Nom_Mois", 
        y=dept_columns,
        title="<b>Évolution Saisonnière des Top 10 Départements (Plus forte variation en Décembre - Type A)</b>",
        markers=True,
        color_discrete_sequence=colors_depts,
        labels={
            'Nom_Mois': 'Mois',
            'value': 'CA Moyen Hebdomadaire ($)',
            'variable': 'Département'
        }
    )
    
    # Renommer les légendes pour enlever "Dept_"
    fig.for_each_trace(lambda t: t.update(name=t.name.replace("Dept_", "Dept ")))
    
    apply_theme(fig)
    return fig


# ===========================
# UTILITAIRES
# ===========================

def format_currency(value):
    """Formate une valeur en devise"""
    return f"${value:,.0f}"

def format_percentage(value):
    """Formate une valeur en pourcentage"""
    return f"{value:.1f}%"

def get_color_palette(n_colors):
    """Retourne une palette de couleurs"""
    colors = THEME_CONFIG["colorway"]
    if n_colors <= len(colors):
        return colors[:n_colors]
    else:
        # Répète les couleurs si nécessaire
        return (colors * ((n_colors // len(colors)) + 1))[:n_colors]
