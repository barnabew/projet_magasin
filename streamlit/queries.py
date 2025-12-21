"""
queries.py
Requêtes SQL pour le dashboard Retail Analytics
"""

# ===================
# KPIs PRINCIPAUX
# ===================

QUERY_CA_TOTAL = """
SELECT ROUND(SUM(Weekly_Sales), 2) AS CA_Total
FROM sales;
"""

QUERY_CA_MOYEN = """
SELECT ROUND(AVG(Weekly_Sales), 2) AS CA_Moyen
FROM sales;
"""

QUERY_NB_MAGASINS = """
SELECT COUNT(DISTINCT Store) AS Nb_Magasins
FROM sales;
"""

QUERY_NB_DEPARTEMENTS = """
SELECT COUNT(DISTINCT Dept) AS Nb_Departements
FROM sales;
"""

# Requête KPI globaux complète du notebook
QUERY_KPI_GLOBAUX = """
SELECT 
    ROUND(SUM(Weekly_Sales), 2) AS CA_Total,
    ROUND(AVG(Weekly_Sales), 2) AS CA_Moyen,
    COUNT(*) AS Total_Observations,
    COUNT(DISTINCT Store) AS Nb_Magasins,
    COUNT(DISTINCT Dept) AS Nb_Departements,
    MIN(DATE(Date)) AS Date_Debut,
    MAX(DATE(Date)) AS Date_Fin
FROM sales;
"""

# ===================
# ANALYSES MAGASINS
# ===================

QUERY_TYPES_PERFORMANCE = """
SELECT 
    s.Type,
    COUNT(DISTINCT s.Store) AS Nb_Magasins,
    ROUND(AVG(s.Size), 0) AS Taille_Moyenne,
    ROUND(AVG(sa.Weekly_Sales), 2) AS CA_Moyen
FROM sales sa
JOIN stores s ON sa.Store = s.Store
GROUP BY s.Type
ORDER BY Taille_Moyenne DESC;
"""

QUERY_TYPES_DETAILED = """
SELECT 
    s.Type,
    COUNT(DISTINCT s.Store) AS Nb_Magasins,
    ROUND(AVG(s.Size), 0) AS Taille_Moyenne,
    ROUND(AVG(sa.Weekly_Sales), 2) AS CA_Moyen,
    ROUND(SUM(sa.Weekly_Sales), 2) AS CA_Total
FROM sales sa
JOIN stores s ON sa.Store = s.Store
GROUP BY s.Type
ORDER BY Taille_Moyenne DESC;
"""

QUERY_TAILLE_PERFORMANCE = """
SELECT 
    sa.Store,
    s.Size,
    s.Type,
    ROUND(AVG(sa.Weekly_Sales), 2) AS CA_Moyen
FROM sales sa
JOIN stores s ON sa.Store = s.Store
GROUP BY sa.Store, s.Size, s.Type;
"""

# ===================
# ANALYSES DÉPARTEMENTS
# ===================

QUERY_TOP_DEPARTMENTS = """
SELECT 
    Dept,
    ROUND(SUM(Weekly_Sales), 2) AS CA_Total,
    ROUND(AVG(Weekly_Sales), 2) AS CA_Moyen,
    COUNT(DISTINCT Store) AS Nb_Magasins
FROM sales
GROUP BY Dept
ORDER BY CA_Total DESC;
"""

QUERY_SEGMENTATION_DEPARTEMENTS = """
WITH dept_presence AS (
    SELECT 
        Dept,
        COUNT(DISTINCT Store) as Nb_Magasins,
        ROUND(COUNT(DISTINCT Store) * 100.0 / 
              (SELECT COUNT(DISTINCT Store) FROM sales), 1) AS Taux_Presence,
        ROUND(SUM(Weekly_Sales), 2) AS CA_Total,
        CASE 
            WHEN COUNT(DISTINCT Store) * 100.0 / 
                 (SELECT COUNT(DISTINCT Store) FROM sales) >= 90 THEN 'Universel'
            WHEN COUNT(DISTINCT Store) * 100.0 / 
                 (SELECT COUNT(DISTINCT Store) FROM sales) >= 70 THEN 'Courant' 
            WHEN COUNT(DISTINCT Store) * 100.0 / 
                 (SELECT COUNT(DISTINCT Store) FROM sales) >= 40 THEN 'Sélectif'
            ELSE 'Spécialisé'
        END AS Categorie
    FROM sales
    GROUP BY Dept
)
SELECT 
    Categorie,
    COUNT(*) as Nb_Depts,
    ROUND(AVG(Taux_Presence), 1) as Taux_Moyen,
    ROUND(AVG(CA_Total), 0) as CA_Moyen_Dept
FROM dept_presence
GROUP BY Categorie
ORDER BY CA_Moyen_Dept DESC;
"""

# Requête complète de segmentation avec CA par magasin du notebook
QUERY_SEGMENTATION_COMPLETE = """
WITH dept_presence AS (
    SELECT 
        Dept,
        COUNT(DISTINCT Store) as Nb_Magasins,
        ROUND(COUNT(DISTINCT Store) * 100.0 / 
              (SELECT COUNT(DISTINCT Store) FROM sales), 1) AS Taux_Presence,
        ROUND(SUM(Weekly_Sales), 2) AS CA_Total,
        ROUND(SUM(Weekly_Sales) / COUNT(DISTINCT Store), 2) AS CA_Moyen_Par_Magasin,
        CASE 
            WHEN COUNT(DISTINCT Store) * 100.0 / 
                 (SELECT COUNT(DISTINCT Store) FROM sales) >= 90 THEN 'Universel'
            WHEN COUNT(DISTINCT Store) * 100.0 / 
                 (SELECT COUNT(DISTINCT Store) FROM sales) >= 70 THEN 'Courant' 
            WHEN COUNT(DISTINCT Store) * 100.0 / 
                 (SELECT COUNT(DISTINCT Store) FROM sales) >= 40 THEN 'Sélectif'
            ELSE 'Spécialisé'
        END AS Categorie
    FROM sales
    GROUP BY Dept
)
SELECT 
    Categorie,
    COUNT(*) as Nb_Depts,
    ROUND(AVG(Taux_Presence), 1) as Taux_Moyen,
    ROUND(AVG(CA_Total), 0) as Moyenne_CA_Total,
    ROUND(AVG(CA_Moyen_Par_Magasin), 0) as Moyenne_CA_Par_Magasin
FROM dept_presence
GROUP BY Categorie
ORDER BY Moyenne_CA_Total DESC;
"""

def get_query_departements_champions(min_presence):
    return f"""
    WITH dept_stats AS (
        SELECT 
            Dept,
            COUNT(DISTINCT Store) as Nb_Magasins,
            ROUND(COUNT(DISTINCT Store) * 100.0 / 
                  (SELECT COUNT(DISTINCT Store) FROM sales), 1) AS Taux_Presence,
            ROUND(SUM(Weekly_Sales), 2) AS CA_Total,
            ROUND(AVG(Weekly_Sales), 2) AS CA_Moyen
        FROM sales
        GROUP BY Dept
        HAVING Taux_Presence >= {min_presence}
    )
    SELECT * FROM dept_stats
    ORDER BY CA_Total DESC;
    """

def get_query_departements_specialises(max_presence):
    return f"""
    WITH dept_stats AS (
        SELECT 
            Dept,
            COUNT(DISTINCT Store) as Nb_Magasins,
            ROUND(COUNT(DISTINCT Store) * 100.0 / 
                  (SELECT COUNT(DISTINCT Store) FROM sales), 1) AS Taux_Presence,
            ROUND(SUM(Weekly_Sales), 2) AS CA_Total,
            ROUND(SUM(Weekly_Sales) / COUNT(DISTINCT Store), 2) AS CA_Moyen_Magasin
        FROM sales
        GROUP BY Dept
        HAVING Taux_Presence <= {max_presence} AND CA_Total > 10000
    )
    SELECT * FROM dept_stats
    ORDER BY CA_Moyen_Magasin DESC;
    """

QUERY_DEPT_BY_TYPE = """
SELECT 
    s.Type,
    sa.Dept,
    ROUND(SUM(sa.Weekly_Sales), 2) AS CA_Total,
    ROUND(AVG(sa.Weekly_Sales), 2) AS CA_Moyen,
    COUNT(DISTINCT sa.Store) AS Nb_Magasins,
    RANK() OVER (PARTITION BY s.Type ORDER BY SUM(sa.Weekly_Sales) DESC) as Rang
FROM sales sa
JOIN stores s ON sa.Store = s.Store
GROUP BY s.Type, sa.Dept
ORDER BY s.Type, CA_Total DESC;
"""

def get_query_perf_by_type(store_type):
    return f"""
    SELECT 
        sa.Dept,
        ROUND(SUM(sa.Weekly_Sales), 2) AS CA_Total,
        ROUND(AVG(sa.Weekly_Sales), 2) AS CA_Moyen,
        COUNT(DISTINCT sa.Store) AS Nb_Magasins
    FROM sales sa
    JOIN stores s ON sa.Store = s.Store
    WHERE s.Type = '{store_type}'
    GROUP BY sa.Dept
    ORDER BY CA_Moyen DESC;
    """

# ===================
# ANALYSES TEMPORELLES
# ===================

QUERY_EVOLUTION_MENSUELLE = """
SELECT 
    CAST(strftime('%m', Date) as INTEGER) as Mois,
    ROUND(SUM(Weekly_Sales), 2) as CA_Total_Mensuel,
    ROUND(SUM(Weekly_Sales) / COUNT(*), 2) as CA_Moyen_Hebdo
FROM sales
GROUP BY strftime('%m', Date)
ORDER BY Mois;
"""

QUERY_EVOLUTION_BY_TYPE = """
WITH type_monthly AS (
    SELECT 
        s.Type,
        CAST(strftime('%m', sa.Date) as INTEGER) as Mois,
        ROUND(SUM(sa.Weekly_Sales) / COUNT(*), 2) as CA_Moyen_Hebdo,
        CASE CAST(strftime('%m', sa.Date) as INTEGER)
            WHEN 1 THEN 'Jan' WHEN 2 THEN 'Fév' WHEN 3 THEN 'Mar'
            WHEN 4 THEN 'Avr' WHEN 5 THEN 'Mai' WHEN 6 THEN 'Jun'
            WHEN 7 THEN 'Jul' WHEN 8 THEN 'Aoû' WHEN 9 THEN 'Sep'
            WHEN 10 THEN 'Oct' WHEN 11 THEN 'Nov' WHEN 12 THEN 'Déc'
        END as Nom_Mois
    FROM sales sa
    JOIN stores s ON sa.Store = s.Store
    GROUP BY s.Type, strftime('%m', sa.Date)
)
SELECT 
    Mois,
    Nom_Mois,
    SUM(CASE WHEN Type = 'A' THEN CA_Moyen_Hebdo END) as Type_A,
    SUM(CASE WHEN Type = 'B' THEN CA_Moyen_Hebdo END) as Type_B,
    SUM(CASE WHEN Type = 'C' THEN CA_Moyen_Hebdo END) as Type_C
FROM type_monthly
GROUP BY Mois, Nom_Mois
ORDER BY Mois;
"""

# Requête du notebook avec noms de mois complets
QUERY_EVOLUTION_BY_TYPE_COMPLET = """
WITH type_monthly AS (
    SELECT 
        s.Type,
        CAST(strftime('%m', sa.Date) as INTEGER) as Mois,
        ROUND(SUM(sa.Weekly_Sales) / COUNT(*), 2) as CA_Moyen_Hebdo,
        CASE CAST(strftime('%m', sa.Date) as INTEGER)
            WHEN 1 THEN 'Janvier' WHEN 2 THEN 'Février' WHEN 3 THEN 'Mars'
            WHEN 4 THEN 'Avril' WHEN 5 THEN 'Mai' WHEN 6 THEN 'Juin'
            WHEN 7 THEN 'Juillet' WHEN 8 THEN 'Août' WHEN 9 THEN 'Septembre'
            WHEN 10 THEN 'Octobre' WHEN 11 THEN 'Novembre' WHEN 12 THEN 'Décembre'
        END as Nom_Mois
    FROM sales sa
    JOIN stores s ON sa.Store = s.Store
    GROUP BY s.Type, strftime('%m', sa.Date)
)
SELECT 
    Nom_Mois,
    SUM(CASE WHEN Type = 'A' THEN CA_Moyen_Hebdo END) as Type_A,
    SUM(CASE WHEN Type = 'B' THEN CA_Moyen_Hebdo END) as Type_B,
    SUM(CASE WHEN Type = 'C' THEN CA_Moyen_Hebdo END) as Type_C
FROM type_monthly
GROUP BY Mois
ORDER BY Mois;
"""

def get_query_departements_saisonniers(seuil_variation):
    return f"""
    WITH dept_monthly AS (
        SELECT 
            Dept,
            CAST(strftime('%m', Date) as INTEGER) as Mois,
            SUM(Weekly_Sales) / COUNT(*) as CA_Moyen_Hebdo,
            COUNT(*) as Nb_Semaines
        FROM sales
        GROUP BY Dept, strftime('%m', Date)
    ),
    dept_stats AS (
        SELECT 
            Dept,
            AVG(CA_Moyen_Hebdo) as CA_Moyen_Global,
            MAX(CA_Moyen_Hebdo) as CA_Max,
            MIN(CA_Moyen_Hebdo) as CA_Min,
            SUM(Nb_Semaines) as Total_Semaines,
            COUNT(DISTINCT Mois) as Mois_Actifs
        FROM dept_monthly
        GROUP BY Dept
        HAVING Total_Semaines >= 40 AND ABS(CA_Moyen_Global) > 2000
    )
    SELECT 
        ds.Dept,
        ROUND(ds.CA_Moyen_Global, 0) as CA_Moyen_Global,
        ROUND(ds.CA_Max, 0) as Pic_CA,
        ROUND(ds.CA_Min, 0) as Creux_CA,
        ROUND(ABS(ds.CA_Max - ds.CA_Min) / ABS(ds.CA_Moyen_Global) * 100, 1) as Coefficient_Variation
    FROM dept_stats ds
    WHERE ABS(ds.CA_Max - ds.CA_Min) / ABS(ds.CA_Moyen_Global) * 100 >= {seuil_variation}
    ORDER BY Coefficient_Variation DESC;
    """

def get_query_evolution_top_depts(dept_list):
    dept_str = ','.join(map(str, dept_list))
    dept_cases = '\n'.join([f"    SUM(CASE WHEN Dept = {dept} THEN CA_Moyen_Hebdo END) as Dept_{dept}," for dept in dept_list])
    
    return f"""
    WITH dept_monthly AS (
        SELECT 
            Dept,
            CAST(strftime('%m', Date) as INTEGER) as Mois,
            ROUND(SUM(Weekly_Sales) / COUNT(*), 2) as CA_Moyen_Hebdo,
            CASE CAST(strftime('%m', Date) as INTEGER)
                WHEN 1 THEN 'Jan' WHEN 2 THEN 'Fév' WHEN 3 THEN 'Mar'
                WHEN 4 THEN 'Avr' WHEN 5 THEN 'Mai' WHEN 6 THEN 'Jun'
                WHEN 7 THEN 'Jul' WHEN 8 THEN 'Aoû' WHEN 9 THEN 'Sep'
                WHEN 10 THEN 'Oct' WHEN 11 THEN 'Nov' WHEN 12 THEN 'Déc'
            END as Nom_Mois
        FROM sales
        WHERE Dept IN ({dept_str})
        GROUP BY Dept, strftime('%m', Date)
    )
    SELECT 
        Mois,
        Nom_Mois,
{dept_cases.rstrip(',')}
    FROM dept_monthly
    GROUP BY Mois, Nom_Mois
    ORDER BY Mois;
    """

# ===================
# ANALYSES SAISONNIÈRES SPÉCIALISÉES
# ===================

# Analyse des variations décembre vs année (du notebook)
QUERY_VARIATION_DECEMBRE_TYPE_A = """
WITH dept_stats AS (
    SELECT 
        sa.Dept,
        ROUND(SUM(CASE WHEN CAST(strftime('%m', sa.Date) as INTEGER) = 12 THEN sa.Weekly_Sales ELSE 0 END) / 
              NULLIF(COUNT(CASE WHEN CAST(strftime('%m', sa.Date) as INTEGER) = 12 THEN 1 END), 0), 2) as CA_Moyen_Hebdo_Decembre,
        ROUND(SUM(sa.Weekly_Sales) / COUNT(*), 2) as CA_Moyen_Hebdo_Annee
    FROM sales sa
    JOIN stores s ON sa.Store = s.Store
    WHERE s.Type = 'A'
    GROUP BY sa.Dept
),
ranked_stats AS (
    SELECT 
        Dept,
        ROUND(CA_Moyen_Hebdo_Decembre - CA_Moyen_Hebdo_Annee, 2) as Difference_Decembre_Annee,
        ROW_NUMBER() OVER (ORDER BY (CA_Moyen_Hebdo_Decembre - CA_Moyen_Hebdo_Annee) DESC) as rang_desc,
        ROW_NUMBER() OVER (ORDER BY (CA_Moyen_Hebdo_Decembre - CA_Moyen_Hebdo_Annee) ASC) as rang_asc
    FROM dept_stats
    WHERE CA_Moyen_Hebdo_Annee IS NOT NULL
)
SELECT 
    'TOP 10' as Groupe,
    ROUND(SUM(Difference_Decembre_Annee), 2) as Somme_Differences,
    COUNT(*) as Nb_Departements
FROM ranked_stats
WHERE rang_desc <= 10

UNION ALL

SELECT 
    'TOP 20' as Groupe,
    ROUND(SUM(Difference_Decembre_Annee), 2) as Somme_Differences,
    COUNT(*) as Nb_Departements
FROM ranked_stats
WHERE rang_desc <= 20

UNION ALL

SELECT 
    'Negatif' as Groupe,
    ROUND(SUM(Difference_Decembre_Annee), 2) as Somme_Differences,
    COUNT(*) as Nb_Departements
FROM ranked_stats
WHERE Difference_Decembre_Annee < 0

UNION ALL

SELECT 
    'Le reste' as Groupe,
    ROUND(SUM(Difference_Decembre_Annee), 2) as Somme_Differences,
    COUNT(*) as Nb_Departements
FROM ranked_stats
WHERE Difference_Decembre_Annee > 0 AND rang_desc > 20;
"""

# Top 10 des départements avec plus forte variation décembre (du notebook)
QUERY_TOP10_VARIATION_DECEMBRE = """
WITH dept_stats AS (
    SELECT 
        sa.Dept,
        ROUND(SUM(CASE WHEN CAST(strftime('%m', sa.Date) as INTEGER) = 12 THEN sa.Weekly_Sales ELSE 0 END) / 
              NULLIF(COUNT(CASE WHEN CAST(strftime('%m', sa.Date) as INTEGER) = 12 THEN 1 END), 0), 2) as CA_Moyen_Hebdo_Decembre,
        ROUND(SUM(sa.Weekly_Sales) / COUNT(*), 2) as CA_Moyen_Hebdo_Annee
    FROM sales sa
    JOIN stores s ON sa.Store = s.Store
    WHERE s.Type = 'A'
    GROUP BY sa.Dept
),
ranked_stats AS (
    SELECT 
        Dept,
        CA_Moyen_Hebdo_Decembre,
        CA_Moyen_Hebdo_Annee,
        ROW_NUMBER() OVER (ORDER BY (CA_Moyen_Hebdo_Decembre - CA_Moyen_Hebdo_Annee) DESC) as rang_desc
    FROM dept_stats
    WHERE CA_Moyen_Hebdo_Annee IS NOT NULL
)
SELECT 
    Dept as Departement
FROM ranked_stats
WHERE rang_desc <= 10
ORDER BY rang_desc;
"""

# Récupération dynamique du top 10 pour graphiques
QUERY_GET_TOP10_DEPTS = """
WITH dept_stats AS (
    SELECT 
        sa.Dept,
        ROUND(SUM(CASE WHEN CAST(strftime('%m', sa.Date) as INTEGER) = 12 THEN sa.Weekly_Sales ELSE 0 END) / 
              NULLIF(COUNT(CASE WHEN CAST(strftime('%m', sa.Date) as INTEGER) = 12 THEN 1 END), 0), 2) as CA_Moyen_Hebdo_Decembre,
        ROUND(SUM(sa.Weekly_Sales) / COUNT(*), 2) as CA_Moyen_Hebdo_Annee
    FROM sales sa
    JOIN stores s ON sa.Store = s.Store
    WHERE s.Type = 'A'
    GROUP BY sa.Dept
),
ranked_stats AS (
    SELECT 
        Dept,
        ROW_NUMBER() OVER (ORDER BY (CA_Moyen_Hebdo_Decembre - CA_Moyen_Hebdo_Annee) DESC) as rang_desc
    FROM dept_stats
    WHERE CA_Moyen_Hebdo_Annee IS NOT NULL
)
SELECT Dept
FROM ranked_stats
WHERE rang_desc <= 10
ORDER BY rang_desc;
"""

# ===================
# VISUALISATIONS
# ===================

# Requête pour les heatmaps (du notebook)
QUERY_HEATMAP_DATA = """
SELECT 
    s.Type,
    sa.Store,
    sa.Dept,
    ROUND(SUM(sa.Weekly_Sales), 2) AS CA_Total
FROM sales sa
JOIN stores s ON sa.Store = s.Store
GROUP BY s.Type, sa.Store, sa.Dept;
"""

# ===================
# PROMOTIONS
# ===================

QUERY_IMPACT_PROMOTIONS = """
SELECT 
    CASE 
        WHEN (COALESCE(f.MarkDown1, 0) + COALESCE(f.MarkDown2, 0) + 
              COALESCE(f.MarkDown3, 0) + COALESCE(f.MarkDown4, 0) + 
              COALESCE(f.MarkDown5, 0)) > 0 THEN 'Avec Promo'
        ELSE 'Sans Promo'
    END AS Statut_Promo,
    COUNT(*) as Nb_Observations,
    ROUND(AVG(sa.Weekly_Sales), 2) AS CA_Moyen
FROM features f
JOIN sales sa ON f.Store = sa.Store AND f.Date = sa.Date
GROUP BY Statut_Promo;
"""

# ===================
# ANALYSES BUSINESS DÉCIDEURS
# ===================

# Performance comparative détaillée par type
QUERY_PERFORMANCE_EXECUTIVE = """
WITH type_performance AS (
    SELECT 
        s.Type,
        COUNT(DISTINCT s.Store) AS Nb_Magasins,
        ROUND(AVG(s.Size), 0) AS Taille_Moyenne,
        ROUND(SUM(sa.Weekly_Sales), 0) AS CA_Total,
        ROUND(AVG(sa.Weekly_Sales), 0) AS CA_Moyen_Hebdo,
        ROUND(SUM(sa.Weekly_Sales) / COUNT(DISTINCT s.Store), 0) AS CA_Par_Magasin,
        ROUND(SUM(sa.Weekly_Sales) / SUM(s.Size) * 1000, 2) AS CA_Par_1000_Sqft
    FROM sales sa
    JOIN stores s ON sa.Store = s.Store
    GROUP BY s.Type
)
SELECT 
    Type,
    Nb_Magasins,
    Taille_Moyenne,
    CA_Total,
    CA_Moyen_Hebdo,
    CA_Par_Magasin,
    CA_Par_1000_Sqft,
    ROUND(CA_Total * 100.0 / (SELECT SUM(CA_Total) FROM type_performance), 1) AS Part_CA_Pct
FROM type_performance
ORDER BY CA_Total DESC;
"""

# Top départements avec potentiel d'amélioration
QUERY_DEPARTEMENTS_OPPORTUNITE = """
WITH dept_analysis AS (
    SELECT 
        sa.Dept,
        COUNT(DISTINCT sa.Store) as Nb_Magasins_Actuels,
        (SELECT COUNT(DISTINCT Store) FROM sales) as Total_Magasins,
        ROUND(SUM(sa.Weekly_Sales), 0) AS CA_Actuel,
        ROUND(AVG(sa.Weekly_Sales), 0) AS CA_Moyen,
        ROUND(COUNT(DISTINCT sa.Store) * 100.0 / 
              (SELECT COUNT(DISTINCT Store) FROM sales), 1) AS Taux_Penetration
    FROM sales sa
    GROUP BY sa.Dept
),
potential_calc AS (
    SELECT 
        *,
        CASE 
            WHEN Taux_Penetration < 80 AND CA_Moyen > 15000 THEN 
                ROUND((Total_Magasins - Nb_Magasins_Actuels) * CA_Moyen * 0.7, 0)
            ELSE 0
        END AS Potentiel_CA_Supplementaire
    FROM dept_analysis
)
SELECT 
    Dept,
    Nb_Magasins_Actuels,
    Taux_Penetration,
    CA_Actuel,
    CA_Moyen,
    Potentiel_CA_Supplementaire,
    ROUND(Potentiel_CA_Supplementaire * 100.0 / CA_Actuel, 1) AS Pct_Amelioration
FROM potential_calc
WHERE Potentiel_CA_Supplementaire > 0
ORDER BY Potentiel_CA_Supplementaire DESC
LIMIT 10;
"""

# Analyse de la corrélation taille-performance pour insights décideurs
QUERY_ROI_TAILLE = """
WITH size_buckets AS (
    SELECT 
        sa.Store,
        s.Type,
        s.Size,
        CASE 
            WHEN s.Size < 100000 THEN 'Petit'
            WHEN s.Size < 150000 THEN 'Moyen'
            ELSE 'Grand'
        END AS Categorie_Taille,
        ROUND(AVG(sa.Weekly_Sales), 0) AS CA_Moyen,
        ROUND(AVG(sa.Weekly_Sales) / s.Size * 1000, 2) AS ROI_Par_1000_Sqft
    FROM sales sa
    JOIN stores s ON sa.Store = s.Store
    GROUP BY sa.Store, s.Type, s.Size
)
SELECT 
    Categorie_Taille,
    COUNT(*) AS Nb_Magasins,
    ROUND(AVG(Size), 0) AS Taille_Moyenne,
    ROUND(AVG(CA_Moyen), 0) AS CA_Moyen,
    ROUND(AVG(ROI_Par_1000_Sqft), 2) AS ROI_Moyen_Par_1000_Sqft,
    ROUND(MIN(ROI_Par_1000_Sqft), 2) AS ROI_Min,
    ROUND(MAX(ROI_Par_1000_Sqft), 2) AS ROI_Max
FROM size_buckets
GROUP BY Categorie_Taille
ORDER BY Taille_Moyenne DESC;
"""

# Analyse saisonnière business-friendly
QUERY_SAISONNALITE_BUSINESS = """
WITH monthly_performance AS (
    SELECT 
        CAST(strftime('%m', Date) as INTEGER) as Mois,
        CASE CAST(strftime('%m', Date) as INTEGER)
            WHEN 1 THEN 'Janvier' WHEN 2 THEN 'Février' WHEN 3 THEN 'Mars'
            WHEN 4 THEN 'Avril' WHEN 5 THEN 'Mai' WHEN 6 THEN 'Juin'
            WHEN 7 THEN 'Juillet' WHEN 8 THEN 'Août' WHEN 9 THEN 'Septembre'
            WHEN 10 THEN 'Octobre' WHEN 11 THEN 'Novembre' WHEN 12 THEN 'Décembre'
        END as Nom_Mois,
        ROUND(SUM(Weekly_Sales), 0) as CA_Total,
        COUNT(*) as Nb_Semaines
    FROM sales
    GROUP BY strftime('%m', Date)
),
avg_calc AS (
    SELECT AVG(CA_Total) as CA_Moyen_Mensuel FROM monthly_performance
)
SELECT 
    mp.Nom_Mois,
    mp.CA_Total,
    ROUND(mp.CA_Total - ac.CA_Moyen_Mensuel, 0) AS Ecart_Moyenne,
    ROUND((mp.CA_Total - ac.CA_Moyen_Mensuel) * 100.0 / ac.CA_Moyen_Mensuel, 1) AS Pct_Vs_Moyenne,
    CASE 
        WHEN mp.CA_Total > ac.CA_Moyen_Mensuel * 1.15 THEN '🔥 Très Fort'
        WHEN mp.CA_Total > ac.CA_Moyen_Mensuel * 1.05 THEN '📈 Fort'
        WHEN mp.CA_Total > ac.CA_Moyen_Mensuel * 0.95 THEN '➖ Moyen'
        ELSE '📉 Faible'
    END AS Performance
FROM monthly_performance mp, avg_calc ac
ORDER BY mp.Mois;
"""
