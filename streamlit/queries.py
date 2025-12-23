"""
queries.py
Requêtes SQL extraites du notebook projet_magasin.ipynb
"""

# ===========================================
# 1. KPI GLOBAUX
# ===========================================
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

# ===========================================
# 2. IMPACT DES PROMOTIONS
# ===========================================
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

# ===========================================
# 3. VALIDATION TYPOLOGIE ABC (TYPES DE MAGASINS)
# ===========================================
QUERY_TYPES_VALIDATION = """
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

# ===========================================
# 4. DÉPARTEMENTS STARS PAR TYPE DE MAGASIN
# ===========================================
QUERY_DEPT_STARS = """
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

# ===========================================
# 5. CATÉGORIES DE DÉPARTEMENTS SELON PRÉSENCE ET PERFORMANCE
# ===========================================
QUERY_CATEGORIE_DEPTS = """
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





# ===========================================
# 6. ÉVOLUTION TEMPORELLE PAR TYPE DE MAGASIN
# ===========================================
QUERY_EVOL_TEMP_TYPE ="""
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



# ===========================================
# 7. VARIATION DÉCEMBRE VS MOYENNE ANNUELLE (TYPE A) - SOMMES
# ===========================================
QUERY_VARIATION_DECEMBRE_SOMMES = """
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

# ===========================================
# 8. TOP 10 DÉPARTEMENTS AVEC PLUS FORTE VARIATION DÉCEMBRE (DÉTAIL)
# ===========================================
QUERY_TOP10_DETAIL = """
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

# ===========================================
# 9. TAILLE VS PERFORMANCE (GRAPHIQUE CORRÉLATION)
# ===========================================
QUERY_TAILLE_PERF = """
SELECT 
    sa.Store,
    s.Size,
    s.Type,
    ROUND(AVG(sa.Weekly_Sales), 2) AS CA_Moyen
FROM sales sa
JOIN stores s ON sa.Store = s.Store
GROUP BY sa.Store, s.Size, s.Type;
"""

# ===========================================
# 10. HEATMAP DATA (PERFORMANCE DÉPARTEMENTS PAR TYPE)
# ===========================================
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

# ===========================================
# 11. GET TOP 10 DÉPARTEMENTS (POUR GRAPHIQUE TEMPOREL)
# ===========================================
QUERY_GET_TOP10 = """
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

# ===========================================
# 12. FONCTION: ÉVOLUTION TEMPORELLE TOP DÉPARTEMENTS (DYNAMIQUE)
# ===========================================
def get_query_top_depts_temporel(top_depts):
    """
    Génère une requête pour l'évolution temporelle d'une liste de départements
    Args: top_depts (list): Liste des numéros de départements
    """
    dept_str = ','.join(map(str, top_depts))
    dept_cases = ',\n    '.join([f"SUM(CASE WHEN Dept = {dept} THEN CA_Moyen_Hebdo END) as Dept_{dept}" for dept in top_depts])
    
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
    {dept_cases}
FROM dept_monthly
GROUP BY Mois, Nom_Mois
ORDER BY Mois;
"""
