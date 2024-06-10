# Surveillance des Rapports YesWeHack - README

## Introduction

Ce projet est conçu pour surveiller le nombre de rapports hunter soumis sur les programmes publics de la plateforme de bug bounty YesWeHack. L'application utilise l'API publique de YesWeHack pour récupérer les programmes publics et leurs rapports soumis à intervalles réguliers, transmet les données dans un système de queue, puis les consomme pour les stocker dans une base de données.

## Fonctionnalités

- **Crawling de l'API YesWeHack** : Récupère le nom des programmes publics et le nombre de rapports soumis à intervalles réguliers.
- **Kafka** : Transmet les données collectées dans un topic kafka pour traitement.
- **Consommation et stockage des données** : Consomme les données de la queue et les stocke dans une base de données postgreSQL.
- **Scalabilité** : La partie consommant les données de la queue est conçue pour être scalable.

## Prérequis

- Docker
- Docker Compose

## Installation

1. Clonez le dépôt GitHub :

   ```bash
   git clone https://github.com/jblezoray/ywh
   cd ywh
   ```

2. Lancez l'application avec Docker Compose :
   ```bash
   docker compose up --build
   ```
