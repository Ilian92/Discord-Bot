# Bot Discord Par Ilian Igoudjil

## Installation avec un environnement virtuel

### Créer un environnement virtuel avec python3

(Si vous utilisez pip3 par exemple)

```
python3 -m venv venv
```

### Lancer L'environnement virtuel

```
source venv/bin/activate
```

Pour désactiver l'environnement virtuel:

```
deactivate
```

### Installer toutes les dépendances et ajouter celles installées à requirements.txt

```
pip install -r requirements.txt
```

## Installation avec Docker

### Build et création du conteneur (le bot se met en ligne directement)

```
docker compose up -d --build
```

### Accès au terminal du conteneur

```
docker-compose exec discord-bot bash
```

## Commandes utiles

### Lancer le bot

Se placer dans le dossier du projet (et lancer l'environnement virtuel) puis:

```bash
python3 main.py
```
