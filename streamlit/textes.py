"""
textes.py
Textes extraits du notebook projet_magasin.ipynb
Organisés par rubrique avec intro/conclusion
"""
magasins_intro = """
### Points clés – Analyse des magasins
- Les promotions ont un impact marginal sur le CA moyen (+1,9 %)
- La taille du magasin est fortement corrélée au chiffre d’affaires (corrélation ≈ 0,8)
- Les magasins peuvent être segmentés efficacement par taille (Types A, B, C)
"""

magasins_promotions = """
**Insight clé :**  
Les promotions ont un impact limité sur le chiffre d’affaires moyen (+1,9 %).

**Conclusion :**  
En l’absence de données sur les marges et les stocks, les promotions ne peuvent pas être considérées comme un levier principal de croissance du CA dans cette analyse.
"""

magasins_taille_performance = """
**Insight clé :**  
La variable « Type » correspond principalement à la taille des magasins.

- Type A : grands magasins  
- Type B : magasins de taille moyenne  
- Type C : petits magasins  

La taille explique une grande partie des écarts de performance observés.
"""

departements_intro = """
### Points clés – Analyse des départements
- Les départements ayant le plus fort CA varient selon le type de magasin.
- Les magasins de type A et C partagent des départements performants quasi similaires, tandis que le type B diffère.
- Certains départements sont performants quel que soit le type de magasin, suggérant des « départements universels ».
"""



departements_top5 = """
**Insight clé :**  
Les magasins de type A et C partagent un top 5 de départements très similaire, tandis que le type B présente une composition légèrement différente.

Certains départements apparaissent systématiquement parmi les plus performants, quel que soit le type de magasin, suggérant l’existence de départements « universels ».
"""


departements_heatmaps = """
**Insight clé :**  
Les magasins de type A et C présentent des schémas de performance départementale similaires, tandis que le type B diffère notablement.
"""

departements_segmentation = """
**Insight clé :**
Les départements universels, ainsi que les département spécialisés sont les départements les plus performants en moyenne.
Cela suggère que cibler ces départements pourrait être une stratégie efficace pour maximiser le chiffre d’affaires.
"""


temporel_intro = """
### Points clés – Analyse Temporelle
- Les tendances temporelles diffèrent selon le type de magasin.
- La hausse des ventes pour les magasins du type A en fin d’année est principalement portée par un nombre limité de départements.
- Sur le top 10 des départements des magasins de type A, une saisonnalité marquée est observée en novembre et décembre.
"""

temporel_type = """
**Insight clé :**  
Les tendances temporelles diffèrent selon le type de magasin.

Les magasins de type A et B enregistrent une hausse marquée du chiffre d’affaires en fin d’année, tandis que les magasins de type C présentent une performance stable sur l’ensemble de l’année.
"""


temporel_decembre_a = """
**Insight clé :**  
La hausse observée en fin d’année n’est pas généralisée à tous les départements.

Elle est principalement portée par un nombre limité de départements, regroupés dans le top 10.
"""




temporel_dept_a = """
**Insight clé :**  
Les départements qui varient le plus en décembres varient également en novembre.
"""



recommandations = """
- **Promotions** : Ne pas se focaliser sur les promotions comme levier principal de croissance du chiffre d’affaires, étant donné leur impact limité.
- **Segmentation des Magasins** : Utiliser la taille des magasins pour segmenter et adapter les stratégies commerciales.
- **Départements performants** : Cibler les départements universels et spécialisés pour maximiser le chiffre d’affaires.
- **Stratégies Temporelles** : Adapter les stratégies de vente en fonction des tendances temporelles spécifiques à chaque type de magasin.
"""
