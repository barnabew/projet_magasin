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

departements_intro = """
Nous allons donc maintenant nous concentrer sur la disposition des magasins, et plus particulièrement sur les départements.
L'objectif est de comprendre comment la répartition des départements dans les magasins influence leur performance.
"""


departements_top5 = """
Nous pouvons remarquer que les magasins des types A et C ont leurs top 5 des départment quasiment identiques.
Tandis que les magasins de type B ont un top 5 des départements légèrement différent.
Malheuresement, les dépoartements ne sont pas nommés, nous ne pouvons donc pas savoir de quels départements il s'agit.
Cependant, nous pouvons remarquer que certains départements sont systématiquement dans le top 5 des magasins, quel que soit leur type.
Cela suggère que ces départements sont particulièrement performants et attirent les clients, indépendamment de la taille du magasin.
"""

departements_heatmaps = """
Nous commencons par analyser les heatmaps de performance départementale pour chaque type de magasin.
Cela nous permet de visualiser si les départements performants sont les mêmes selon la taille des magasins.
Nous faisons cela par type de magains, car nous avons remarquer que la taille des magasins avait un impact important sur leur performance.
Nous remarquons que les départements performants varient significativement entre les types de magasins.
Cela suggère que la taille du magasin influence les départements qui réussissent le mieux.
Nous allons donc maintenant regarder le top 5 des départements par type de magasin pour confirmer cette hypothèse.
"""

temporel_intro = """
Nous allons maitenaznt analyser les données sous l'angle temporels.
L'objectif est de comprendre comment les performances des magasins et des départements évoluent au fil du temps.
"""


temporel_type = """
Nous remarquons que les tendances temporelles varient differerament selon le type de magasin.
En effet alors que nous avions remarquer que les types A et C disposer de département similaires, nous remarquons que leurs tendances temporelles sont différentes.
Alors que les magasins de type A et B connaisent un CA plus fort en fin d'années , les magasins du type C ont un CA constant tout au long de l'année.
Nous allons maintenant nous concentrer sur les départements des magasins de type A pour voir si des tendances similaires sont observables au niveau départemental.
Nous voulons savoir si cela est du a un effet saisonnier ou si certains départements performent mieux à certaines périodes de l'année.
"""

temporel_decembre_a = """
Nous voulons donc savoir si cela estr du a une augmentation d'un petit nombres de départments ou si tous les départements connaissent cette tendance.
Or on remarquer que le top Top 10 des départments connait une grosse augmentatyions comparer au autres.
Nous pouvons donc dit que cela est du à ses départments.
"""



temporel_dept_a = """
Nous avons ici la réprensentations de la performance temporelle de ce top 10 des départements dans les magasins de type A.
Nous pouvons donc bien voir cette montée en décembre.
Cela suggère que certains départements, probablement liés aux fêtes de fin d'année (comme les jouets, les décorations, etc.), connaissent une augmentation significative des ventes en novembre(black friday)/ décembre(noël).
Cette tendance saisonnière est importante à prendre en compte pour la gestion des stocks et les stratégies de marketing.
Cependant nous ne pouvons pas en dire plus car nous n'avons pas les noms des départements.
"""
