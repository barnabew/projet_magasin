# Projet : Analyse d'une chaîne de magasin

## Contexte

Ce projet vise à extraire des pour orienté une améliorations du chiffre d'affaires pour une châine de magasins. Les données sont issues du data center public, pour cela elles sont annonimisées. L'ojectif de ce projet est de comprendre les facteurs qui permettent d'améliorer en utiliser les differentes données mises à notre disposition.
L’objectif est double :
- Identifier les facteurs qui influencent le plus la décision de résiliation ;
- Développer un modèle de machine learning capable d’anticiper les clients à risque.

Les résultats obtenus doivent permettre d’appuyer les décisions stratégiques en matière d'obtimisation des magasins..

---

## Analyses réalisées

L’étude a été menée en plusieurs étapes. Une analyses rapides à permis de comprendre que les promotions avaient uniqument un impact faibles sur le chiffres d'affaires. 

L’exploration initiale a permis d’identifier que la classification par type, A,B ,et C étaient lié directement à la taille du magasins. De plus on put sortir que les départments étaients vers quoi l'analyses devait se faire.

Les analyses ont donc été faites sur la répartitions des départements dans les différents types de magasins. Cela nous a permis d'extraires les départements disposant des meilleur rendements.

De plus après une pondérations unes analyses temporelle a pu etre faites , ce qui a permis de voir la saisonalités des types de magasins , ainsi que des départements.

---

## Résultats clés

Les analyses ont pu permettre d'extraires des améliorations possibles des magasisns. Avec évidemment des léviers possibles sur la formes des magasins possbiles ainsi que des saisonnabilités.


---

## Organisation du projet

Le notebook [`Projet_churn.ipynb`](https://github.com/barnabew/projet_churn/blob/main/Projet_churn.ipynb) contient toutes les explications détaillées sur le **traitement des données**,  
le **nettoyage**, les **analyses**, ainsi que les **visualisations**.  
Il constitue la base exploratoire du projet, permettant de documenter chaque étape du raisonnement.

Le dossier [`streamlit/`](https://github.com/barnabew/projet_churn/tree/main/streamlit) reprend le même code,  
mais il a été **structuré en plusieurs fichiers** afin de rendre l’application plus **lisible**, **modulaire** et **facile à maintenir**.  
Cette séparation du code permet une meilleure réutilisation et simplifie les futures évolutions du projet.  

---

## Application Streamlit

Une **interface Streamlit** a été développée afin de permettre une utilisation interactive du modèle.  
Elle se compose de plusieurs pages :

1. **Resumé** – résumé des kpis principaux ainsi que des analyses les plus utilises pour permmetrenet une lecture rapide.  
2. **Magasins** – évaluation des résultats obtenus avec les principales métriques (AUC, rappel, précision, F1-score) et visualisation des courbes ROC et Précision–Rappel.  
3. **Départements** – simulation en temps réel de la probabilité de churn à partir des caractéristiques d’un client.

L’application est disponible :  [Accéder à l'application](https://projetmagasin.streamlit.app/).

---

## Résultats et recommandations

L’analyse montre que le chiffres d'affaires dépants du types de magasins. L'analyses montres une répartition par département presques identiques entres les magasisn du type A et C. Cependant les analyses temporelles montrent une divergences des ces deux types en fin d'années. Cela est du a la présences dans les magains du type a de département spécifiques ayant un CA élevé en fin d'années. 

Les différentes analyses permettent également de soulever les problemes de promotions qui ne permettent pas une augmentation du CA conséquentes même si nous avons pas les données des stocks ce qui nous permettré de connaitre leurs utilités a ce niveau la.








