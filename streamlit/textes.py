"""
textes.py
Textes extraits du notebook projet_magasin.ipynb
Organisés par rubrique avec intro/conclusion
"""
magasins_intro = """

L'analyses commences par un travail sur les magasins en génreral, afin de comprendre les facteurs influençant leur performance. 
Nous examinons l'impact des promotions sur le chiffre d'affaires des magasins, ainsi que la corrélation entre la taille des magasins et leur performance.
Nous avons pu remarquer que la base de données avait déja mis en place une données types dans les magasins, nous allons montrer a quoi elle correspond pour pouvoir ensuite travailler dessus dans la suites de l'analyses.
"""

magasins_promotions = """
Nous remarquons que les periodes de promotions ont un impact très faibles sur le chiffre d'affaires moyen des magasins. 
En effet un impact de seulement 2% ne permet pas de déclarer que les promotions est un facteur clée du CA. 
Cependant nous n'avons pas les données des stocks et des marges, il est donc possible que les promotions aient un impact plus important sur ces deux facteurs. 
Nous allons donc arreté l'analyses des promotions ici et nous concentrer sur d'autres facteurs.
"""

magasins_taille_performance = """
Nous voulions savoir que voulait dire la donnée "Type" dans la table des magasins. 
Après analyses, nous avons pu remarquer que cette donnée correspondait plus à la taille des magasin qu'à leurs CA, même si les deux sont liés.
En effet, gràce au Grpahiques, nous pouvons dire queles magasins de type A sont les magasins de grandes tailles, le magasins de type B sont les magasins de taille moyennes, et que les magaisns de types C sont les magaisns de peties tailles.
Nous allons maintenant voir si les differences de CA entre les types de magasins sont due a leurs tailles ou a d'autres facteurs.
Pour cela nous allons commencer par regarder les magasisns sont l'angles des départements.
"""