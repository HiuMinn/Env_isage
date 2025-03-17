#!/bin/bash

# Créer l’environnement conda
conda env create -f environment.yml

# Activer l’environnement
conda activate env_isage

# Afficher la liste des paquets installés
conda list
