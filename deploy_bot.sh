#!/bin/bash

# Mettre à jour les paquets système
sudo apt update && sudo apt upgrade -y

# Installer Git, Python et pip
sudo apt install git python3 python3-pip python3-venv -y

# Cloner le repository GitHub
git clone https://github.com/Ilian92/Discord-Bot.git
cd Discord-Bot

# Créer et activer un environnement virtuel Python
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le bot Discord
python main.py