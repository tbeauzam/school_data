# [Python] Schools Scrapper

Ce projet est un exercice ayant pour but de s'entraîner au scrapping et à la mise en forme de données.
Voici le sujet :
```
L'objectif de ce tests est de regrouper deux sources de données différentes
et de les modéliser dans un format propre à ce que les données résultantes
soient directement incorporées dans une base de données.


La première source de données {Insee} est la liste géolocalisée des
établissements d'enseignement du premier et second degrés

  https://www.data.gouv.fr/fr/datasets/adresse-et-geolocalisation-des-etablissements-denseignement-du-premier-et-second-degres/


La seconde source de données {Créteil} est la liste des établissements
du second degré de l'académie de Créteil

  http://www.ia94.ac-creteil.fr/infogen/etablissements/lycees.htm


Nous cherchons en premier lieu à enrichir {Insee} des numéros de téléphone
contenus dans {Créteil}, puis de modéliser en plusieurs collections/tables
les données résultantes.


Trois tâches sont demandées pour cet exercice :


 1/ La collecte, le formatage et la normalisation des données,

 2/ La fusion des données,

 3/ La modélisation des données.
 

Les données résultantes sont susceptibles d'être utilisées en totalité ou partiellement.


Fichiers attendus :

 - Code de collecte/formatage/normalisation/fusion;

 - Fichiers contenant les données résultantes;

 - Tout fichier jugé nécessaire pour la reprise sur erreur, le débuggage,
 etc. ou encore la bonne compréhension du résultat final;

 - Documentation de description de la méthode employée.


Mis à part ce dernier fichier, les fichiers attendus seront au
format JSON et encodés en UTF-8.
```
### Informations et usage

Pour lancer le script dans un terminal :
```
python main.py
```

- le script nécessite le module "requests" installé et a été fait en python 2.7.12.
- le script va tenter de télécharger un fichier csv d'environ 20 Mo à partir de la première source de données ([Source 1](https://www.data.gouv.fr/fr/datasets/adresse-et-geolocalisation-des-etablissements-denseignement-du-premier-et-second-degres/)), nécessaire pour la solution de l'exercice. Si le script est éxécuté plusieurs fois et que le fichier est déjà présent à la racine du projet, le script va passer directement à l'étape suivante.
- le script va scrapper la seconde source de données (page recensant tous les lycées du Val-de-Marne : [Source 2](http://www.ia94.ac-creteil.fr/infogen/etablissements/lycees.htm)) pour récupérer les numéros de téléphone de ces établissements, et les fusionner avec les établissements correspondants venant de la première source de données (qui contient beaucoup d'informations, mais pas les numéros de téléphone)
- à l'issue de l'éxécution du script, deux fichiers seront générés :
  - `all_schools.json` : liste de toutes les écoles de France au format json (~ 65.000 entrées)
  - `schools_with_phone` : liste des lycées du Val-de-Marne possédant un numéro de téléphone au format json (~ 40 entrées)
  
##### Liste des champs issus du .csv de la première source de données :
```
    Code établissement
    Appellation officielle
    Dénomination principale',
    Patronyme uai
    Secteur Public/Privé
    Adresse
    Lieu dit
    Boite postale
    Code postal
    Localite d'acheminement
    Commune
    Coordonnee X
    Coordonnee Y
    EPSG
    Latitude
    Longitude
    Qualité d'appariement
    Localisation
    Code nature
    Nature
    Code état établissement
    Etat établissement
    Code département
    Code région
    Code académie
    Code commune
    Département
    Région
    Académie
    Position
```
On ajoute à cela un champ `Téléphone` au cours de l'éxécution du script.

##### Exemple d'objet json généré par le script :
```
{
    "info":{
        "etat_etablissement":"OUVERT",
        "nature":"LYCEE POLYVALENT",
        "telephone":"01 45 13 26 80",
        "secteur_public_prive":"Public",
        "code_academie":"24",
        "code_etat_etablissement":"1",
        "appellation_officielle":"Lycée polyvalent Gutenberg",
        "denomination_principale":"LYCEE POLYVALENT",
        "academie":"Créteil",
        "code_nature":"306",
        "patronyme_uai":"JOHANNES GUTENBERG"
    },
    "localisation":{
        "departement":"Val-de-Marne",
        "commune":"Créteil",
        "localite_d_acheminement":"CRETEIL",
        "adresse":"16 rue DE SAUSSURE",
        "code_commune":"94028",
        "localisation":"Numéro de rue",
        "boite_postale":"",
        "qualite_d_appariement":"Parfaite",
        "code_postal":"94000",
        "code_region":"11",
        "region":"Ile-de-France",
        "code_departement":"94",
        "lieu_dit":""
    },
    "donnees_geo":{
        "coordonnee_y":"6852312.7",
        "coordonnee_x":"661133.4",
        "epsg":"EPSG:2154",
        "longitude":"2.4711703520991506",
        "latitude":"48.76974261722545",
        "position":"48.7697426172, 2.4711703521"
    },
    "code_etablissement":"0941930M"
}

```
