# Pages Vertes

Ce projet a pour but le nettoyage de données sur les arbres de Lyon, et la production d'une application permettant l'exploration et la recherche de ces arbres. 

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
Pour ne pas utiliser la correction de wikipedia (et générer la base de donnée très rapidement), il suffit de changer la constante USE_WIKIPEDIA au début du fichier comme ceci:

```python
USE_WIKIPEDIA = False
```

## Fichier JSON
Les fichiers json situés dans webApp/json correspondent à notre base de données. Le fichier incomplete_data.json correspond à l'ensemble des données qui ont été éliminées lors du traitement à cause d'un manque d'informations, et data_without_GPS correspond à l'ensemble des données qui n'ont pas de coordonnées GPS (et qui ne sont pas dans incomplete_data.json)


