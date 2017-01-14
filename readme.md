# Pages Vertes

Ce projet a pour but le nettoyage de données sur les arbres de Lyon, et la production d'une application permettant l'exploration et la recherche de ces arbres.

## Requis
Python (>=3)

## Installer les dépendances Python
Pour faire fonctionner le projet, il est nécessaire d'installer quelques dépendances python. Pour cela, il est nécessaire d'avoir pip. Si celui-ci n'est pas présent sur le système, faites:
```bash
./scripts/installPip.sh
```

Puis, pour installer les dépendances python, faites:
```bash
./script/installDependencies.sh
```
## Générer la base de données depuis le fichier .xls
```bash
python scripts/generateDatabase.py
```
Pour ne pas enrichir les données avec wikipedia (et générer la base de donnée très rapidement), il suffit de changer la constante USE_WIKIPEDIA au début du fichier comme ceci:

```python
USE_WIKIPEDIA = False
```

## Fichier JSON
Les fichiers json situés dans webApp/json correspondent à notre base de données. Le fichier incomplete_data.json correspond à l'ensemble des données qui ont été éliminées lors du traitement à cause d'un manque d'informations, et data_without_GPS correspond à l'ensemble des données qui n'ont pas de coordonnées GPS (et qui ne sont pas dans incomplete_data.json)


## Convertir les json en script sql
Le script de conversion convertit les fichiers json valides se situant dans webApp/json et produit le script sql correspondant dans data/sql. Si des fichiers json sont non valides, ils ne seront pas considérés, il faudra les modifier afin qu'ils puissent être convertis. Dans le mécanisme de conversion, les originaux ne sont pas modifiés.
Pour effectuer la conversion, faites :
```bash
python scripts/json2sqlConverter.py
```
