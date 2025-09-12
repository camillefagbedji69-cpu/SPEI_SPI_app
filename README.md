# Dashboard SPI & SPEI – Analyse climatique interactive

📊 **Description**
Ce projet est un **dashboard interactif Streamlit** permettant de calculer et visualiser les indices hydriques **SPI (Standardized Precipitation Index)** et **SPEI (Standardized Precipitation-Evapotranspiration Index)** à partir de données climatiques quotidiennes.
Il est conçu pour l’analyse de sécheresse et d’humidité sur des séries temporelles locales.

---

## Fonctionnalités

* Upload d’un fichier CSV contenant :

  * Pluviométrie
  * Température minimale et maximale
  * Radiation solaire
* Imputation automatique des valeurs aberrantes par la **médiane des valeurs positives**.
* Calcul de l’**évapotranspiration** selon la méthode de Hargreaves.
* Calcul des indices **SPEI30 et SPI30** sur une fenêtre glissante de 30 jours.
* Graphique interactif avec **Plotly** :
  
  * Courbes SPI et SPEI
  * Lignes de référence pour sécheresse/humidité
  * Zoom, hover et légende dynamique

## Exemple d’usage

* Analyse de la sécheresse dans une commune sur plusieurs années.
* Suivi hydrique pour la planification agricole.
* Prévention et gestion des risques liés aux déficits hydriques.

## URL de l'application 
https://speispiapp-uiycpejdavnvsb7rmqfzd8.streamlit.app/

👨‍💻 Auteur

**Camille Boris FAGBEDJI**
Master en Sciences Agronomiques – Université de Parakou (Bénin)
Spécialisation en **ingénierie des eaux et sols, télédétection et modélisation écohydrologique**.
