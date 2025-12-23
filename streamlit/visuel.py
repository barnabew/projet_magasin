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
# GRAPHIQUES SPÉCIALISÉS RETAIL
# ===========================

def plot_performance_by_type(df):
    """Graphique de performance par type de magasin"""
    
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

    """Graphique d'impact des promotions"""
    fig = px.bar(
        df,
        x="Statut_Promo",
        y="CA_Moyen",
        title=title,
        color="CA_Moyen",
        color_continuous_scale="viridis"
    )
    
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
