# Projet NSI
### Un moteur de blog en Python avec Flask
## Comment le démarrer
#### - Dans le dossier du projet, créer un venv Python avec la commande suivante:
``python3 -m venv venv``
#### - Ensuite, activer le venv (commande à refaire à chaque fois que vous relancez votre cmd/terminal):
sur macOS et Linux:
`` . venv/bin/activate``

ou sur Windows:
``venv\Scripts\activate``

#### - Installer les dépendances:
``pip install -r requirements.txt``

#### - Copier le fichier .env.example, le renommer en .env et compléter les infos de votre base de données MySQL

#### - Importer le fichier db-schema.sql dans votre base de données

#### - Et lancer le projet avec ``./run.sh``
