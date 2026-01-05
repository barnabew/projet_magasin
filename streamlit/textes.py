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
- Objectif : analyser la performance des départements et leur contribution au chiffre d’affaires.
- Méthodologie : agrégation par département, comparaison par type de magasin et visualisations (top, heatmaps).
- À retenir : certains départements sont systématiquement performants et méritent une attention prioritaire.
"""



departements_top5 = """
**Insight clé :**  
Les magasins de type A et C partagent un top 5 de départements très similaire, tandis que le type B présente une composition légèrement différente.

Certains départements apparaissent systématiquement parmi les plus performants, quel que soit le type de magasin, suggérant l’existence de départements « universels ».
"""


departements_heatmaps = """
**Insight clé :**  
Les départements les plus performants varient fortement selon le type de magasin.

La taille du magasin influence directement les départements qui génèrent le plus de chiffre d’affaires.
"""


temporel_intro = """
### Points clés – Analyse Temporelle
- Objectif : identifier les tendances et effets saisonniers sur les ventes (mensualités, pics de fin d'année).
- Méthodologie : comparaison du mois de décembre vs moyenne annuelle, évolutions par type et par département.
- À retenir : une saisonnalité marquée en fin d'année pour certains départements, à intégrer dans la gestion des stocks et stratégies commerciales.
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
Le top 10 des départements des magasins de type A connaît une augmentation significative des ventes en novembre et décembre.

Cette saisonnalité forte doit être prise en compte dans la gestion des stocks et les stratégies commerciales.
"""



recommandations = """



Etudes des stocks pour voir l'utilités des promotions car elles n'ont pas d'impact sur le CA moyen.

Préviligier les département universels qui génerent la grandes majorités du CA
Les magasins du type A et C devraient se concentrer sur les départements performants communs, tandis que les magasins de type B pourraient adapter leur offre en fonction des départements spécifiques qui performent bien pour eux.
Travailler sur les performances des magasins A et B en fin d'années.
Travailler sur les départements performants en fin d'années pour maximiser les ventes durant cette période cruciale.

"""