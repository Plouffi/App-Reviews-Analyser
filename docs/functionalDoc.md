# Documentation fonctionnelle

<aside>
📌 App Review Analyser (ARA)

![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled.png)

</aside>

# Sommaire

## I. Objectif de l’application

L’application est un outil permettant de scrapper et analyser les avis des utilisateurs sur un large portefeuille d’applications disponibles sur l’application Google Play store.

![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%201.png)

L’application propose de modifier plusieurs variables permettant d’analyser les avis laissés par les utilisateurs sur une app choisie dans le Google Play store. Il est possible d’obtenir 3 types d’analyses différentes : 

- La distribution des notes données à l’appli par les utilisateurs, sur une période choisie,
- Les notes moyennes des utilisateurs sur une période allant de la date de mise en service de l’application jusqu’ aujourd’hui. Plusieurs moyennes sont calculées (moyennes des notes cumulatives, moyennes des utilisateurs ayant rendus une note, et enfin la moyenne des notes sur toute la période de vie de l’application)
- Enfin, les nuages de mots. Les nuages de mots permettent de rendre compte des principaux mots clés utilisés par les utilisateurs pour définir et noter leur expérience avec l’application

Cette application peut être utilisée par des développeurs afin de rendre compte de l’intérêt et des remarques générales des utilisateurs finaux. 
Elle peut être également utilisée par les utilisateurs finaux eux même afin d’avoir le retour d’expérience des utilisateurs ayant déjà installé et tester l’application.

---

## II. Accès à l’application

L’application est accessible directement sur internet via le lien : ………….  (GitHub page —> [démo](https://plouffi.github.io/App-Reviews-Analyser/)). Aucune connexion n’est exigée. 

---

## III. Fonctionnement de l’application

### a. Changer de langue

- Voir
    - Cliquez sur le bouton des langages et sélectionnez la langue désirée afin de poursuivre dans l’utilisation de ARA
    
    ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%202.png)
    

### b. Changer l’apparence de l’application

- Voir
    - Cliquez sur le bouton composé d’une lune et des étoiles pour passer au mode jour (fond blanc)
    
    ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%203.png)
    
    - Cliquez sur le bouton sous la forme d’un soleil pour passer au mode nuit (fond noir)
    
    ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%204.png)
    

---

### c. Scrapper

- Etape 1
    - Allez sur l’onglet “Scrapper” (=page d’accueil par défaut)
    - Rentrez le nom de l’application à scrapper dans la barre de recherche
    
    ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%205.png)
    
    - Cliquez sur l’application à scrapper dans les “Search Results”. Vous serez redirigez vers la page suivante.
- Etape 2
    - Cliquez sur “Extraction des données”
    
    ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%206.png)
    
- Etape 3
    - Le temps d’extraction des données, certains avis laissés par les utilisateurs défileront comme sur l’interface ci-dessous
    
    ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%207.png)
    
    - Une fois l’application scrappée, ARA vous redirige directement vers l’onglet “Analyseur”

### d. Analyser

> Les notes des utilisateurs vont de 1 étoile pour la pire note à 5 étoiles pour la meilleure note
> 
- Etape 1
    - Aller sur l’onglet “Analyser” puis sélectionner une applications parmi celles affichées dans le menu ou rentrer le nom de l’application à analyser dans la barre de recherche
        
        ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%208.png)
        
- Etape 2
    - Une fois l’application choisie, ARA vous permettra de renseigner et modifier plusieurs variables  afin d’obtenir 3 différentes analyses.
        
        ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%209.png)
        
- Etape 3
    - La “*Distribution des notes*” permet de définir une date et d’obtenir un bar chart recensant les différentes notes sur deux périodes distinctes : avant et après la date définie
    
    ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%2010.png)
    
- Etape 4
    - L’analyse des moyennes permet de calculer le nombre moyen d’utilisateurs, la moyenne générale et la moyenne cumulée sur une période défini
    
    ![—— : Moyenne des notes sur toute la période de vie de l’application
    —— : Moyenne des notes cumulatives
    —— : Moyenne des utilisateurs ayant rendus une note](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%2011.png)
    
    —— : Moyenne des notes sur toute la période de vie de l’application
    —— : Moyenne des notes cumulatives
    —— : Moyenne des utilisateurs ayant rendus une note
    
    > La variation du Delta permet de définir la fenêtre de temps en jour sur laquelle on calcule les moyennes cumulatives. Pour modifier le Delta, faire bouger le curseur de gauche à droite
    > 

### e. Créer des nuages de mots

- Etape 1
    - Sélectionnez le Alpha en faisant bouger le curseur de gauche à droite. Le Alpha permet de réduire le bruit dans la donnée. Plus le Alpha est élevé, moins il y a de bruit. Réduire le bruit permet de facilité l’apprentissage de la relation que l’on cherche à prédire.
    - Sélectionnez le nToken. Cela permet choisir le nombre de mot à faire apparaitre dans le nuage de mot. Choisir 1 nToken fera apparaitre 1 mot; 2 nToken —> 2 mots, et ainsi de suite. Les mots qui apparaissent sont collés dans la phrase rédigée par l’utilisateur. Ce qui peut donner des nuages de mots avec “very good and” par exemple. 
    NB : nToken doit être strictement supérieur à 07
    
    ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%2012.png)
    
- Etape 2
    - Le paramètre langue affiche un menu déroulant. Sélectionner la langue afin d’afficher les nuages de mot dans la langue désirée
    
    ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%2013.png)
    
- Etape 3
    - Avant d’utiliser le curseur “Note”, définissez la première période et la deuxième période à analyser afin d’avoir une comparaison des avis. Le but ici est de pouvoir comparer les commentaires des utilisateurs d’une période définie à une autre.
    
    ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%2014.png)
    
- Etape 4
    - Enfin, sélectionnez la note donnée à l’application donnée par les utilisateurs. Pour sélectionner une note précise, il suffit de faire bouger le curseur de gauche à droite. 0 étant l’ensemble des avis confondus (notes de 1 à 5 étoiles mélangées).
    
    ![Untitled](https://github.com/Plouffi/App-Reviews-Analyser/blob/masterdocs/img/Untitled%2015.png)
    

---

## IV. Bugs et incidents

En cas de bugs ou d’incidents, envoyez un mail spécifique à l’adresse suivante : plouffi.github@gmail.com