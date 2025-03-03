# Kiss AI (_Keep It Simple Stupid AI_)

Le nom "Kiss AI" s'inspire du principe KISS ("Keep It Simple, Stupid"), qui préconise la simplicité dans la conception pour améliorer l'efficacité et l'utilisabilité.
Ce principe est largement reconnu dans le développement logiciel et la conception de systèmes.

_Le principe KISS stipule que la plupart des systèmes fonctionnent mieux lorsqu'ils sont conçus de manière simple, évitant ainsi des conceptions inutiles et complexes._

Kiss AI vise à démocratiser l'accès à l'intelligence artificielle en fournissant des outils simples, efficaces et accessibles. En adhérant au principe KISS, nous nous engageons à développer des solutions qui répondent aux besoins actuels tout en restant conviviales et performantes.​

Kiss AI reconnaît les préoccupations environnementales liées à l'utilisation de technologies d'IA gourmandes en ressources. En privilégiant des modèles légers et des algorithmes optimisés, nous visons à réduire l'empreinte carbone associée au déploiement de solutions d'IA. Cette approche permet de concilier innovation technologique et responsabilité écologique.

## Installation

Prérequis : Python

1. Cloner le dépôt :

```bash
$ git clone https://github.com/charlesen/kiss-ai.git
$ cd kiss-ai
```

2. Virtual python :

```bash
$ python -m venv .venv
$ source .venv/bin/activate
```

3. Installation des dépendances

```bash
$ pip install -r requirements.txt
```

4. Fichier de configuration

Créez un fichier `.env.local` pour y stocker vos informations sensibles, notamment la Master Key essentielle pour interagir avec l'API.

```bash
# .env.local
debug=True

# API
master_key=votre_master_key # Lancez la commande suivante pour générer une nouvelle clé ==> openssl rand -hex 16
openai_api_key=cle_open_ai
openai_model=gpt-4o-mini
```

5. Lancement de l'application

```bash
$ uvicorn app.main:app --reload
```

L'application sera accessible à l'adresse : http://127.0.0.1:8000.

Une fois le serveur en marche, vous pouvez accéder à la documentation interactive de l'API à l'adresse : http://127.0.0.1:8000/docs.

Cette interface, générée automatiquement par FastAPI, vous permettra de tester les différents endpoints de l'application (Vous devrez indiquer la master key dans chacune des requetes).

## Fonctionnalités clés (_en constante évolution_)

- Synthèse vocale : Conversion de texte en parole de haute qualité, avec des options pour personnaliser la langue et la voix, en utilisant des bibliothèques comme pyttsx3 et gTTS.​

- Classification de texte : Catégorisation efficace de textes en différentes classes, facilitation de l'organisation et l'analyse de données textuelles.​

- Génération de texte : création de contenu textuel basé sur des modèles pré-entraînés, permettant d'automatiser la rédaction et la génération de contenu.​

- _d'autres fonctionnalités à venir_

## Contribution au projet

Nous encourageons vivement les contributions de la communauté pour enrichir Kiss AI en :​

- Proposant des améliorations de fonctionnalités existantes pour accroître l'efficacité et la convivialité.​

- Développant de nouveaux outils et modules répondant aux besoins émergents de la communauté IA.​

- Identifiant et corrigeant des bugs pour assurer la fiabilité et la stabilité de la bibliothèque.​

## Comment Contribuer

Option 1

- Créez une branche : développez vos modifications sur une branche distincte nommée de manière descriptive.​
- Soumettez une Pull Request : proposez vos modifications pour examen et intégration dans la branche principale.

Option 2

- Fork le dépôt en clonant le dépôt principal de Kiss AI sur votre compte GitHub.​
