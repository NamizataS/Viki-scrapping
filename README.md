# Projet Viki scrapping

Ce projet a pour but de scrapper le site web "www.viki.com", d'envoyer les informations obtenues lors du scrapping dans une base MongoDB et de récupérer des informations afin de réaliser de la data visualization

## Docker
Afin de pouvoir utiliser au mieux notre projet il faut installer Docker.

### Installation des librairies
Il faut tout d'abord exécuter la commande `pip install -r requirements.txt`qui liste toutes les librairies nécessaires à la bonne exécution de ce projet. 

### Création de l'image
Il faut tout d'abord utiliser la commande `docker build -t image_drio  .` pour crée l'image utilisée dans le projet.

### Création du conteneur
Pour ensuite créer le conteneur, c'est-à-dire l'instance dans laquelle on va travailler à partir de l'image créée, on utilise la commande:
```
docker run -it --name conteneur_drio -v `pwd`:/home/dev/code/ image_drio
````

### Docker compose
Pour instancier la base MongoDB ainsi que d'autres outils nécessaires, un fichier docker-compose est disponible. Il suffit de lancer la commande `docker-compose up -d` dans le terminal

### Lancer le programme

#### Scraper les données
Lors de la première utilisation il est obligé de lancer le Scraper. Pour cela il suffit d'exécuter le script Python `scraping.py`

#### Lancer l'application
Pour pouvoir lancer le programme, il y a juste à executer le script Python: `app.py` et ensuite se rendre à l'adresse indiquée par le terminal

## Contributors
* [SANGARE Namizata](https://github.com/NamizataS)
* [STROCK Rebecca](https://github.com/StrockBecca)
