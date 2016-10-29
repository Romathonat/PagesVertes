from sanitize import sanitize
import json
import os
from utils import hashableDict

sanitized_datas, incomplete_data = sanitize(False)

#those are the tables of our model
#python dict are hashable, very good to gain perfs
arbre = set()
nomBinomial = set()
feuillage = set()

#we load the gps into the memory
gps = {}
with open(os.path.join(os.path.dirname(__file__),'../data/arbresGPS.txt'), 'r+') as f:
    for line in f:
        line = line.replace(' ', '')
        id_arbre, latitude, longitude = line.split(',')
        longitude = longitude.rstrip()
        gps['ar'+str(id_arbre)] = (latitude, longitude)

for line in sanitized_datas:
    gps_cordinate = True
    tree_latitude, tree_longitude = 0,0
    try:
        tree_latitude, tree_longitude = gps[line[1]]
    except:
        #print("Missing gps coordinates for :"+line[1])
        gps_cordinate = False

    #we do not add this data if we don't have the gps informations
    if gps_cordinate:
        new_feuillage = {'typeArbre': line[5]}
        feuillage.add(hashableDict(new_feuillage))

        #the firt letter must be upper
        genre = line[3][0].upper()+line[3][1:]

        new_nomBinomial = {'genre': genre,'espece': line[4], 'nomFrancais':line[2], 'feuillage': line[5],
        'info_francais': line[9], 'url': line[10], 'description': line[11], 'nom_francais_suggere': line[12]}

        #we add this data only if it is not here yet
        nomBinomial.add(hashableDict(new_nomBinomial))

        new_arbre = {'id': line[1],'hauteur': line[6], 'diametreTronc': line[7], 'diametreCouronne': line[8],\
        'latitude' : tree_latitude, 'longitude': tree_longitude, 'nomBinomial': genre+" "+line[4]}
        arbre.add(hashableDict(new_arbre))


#now we dump datas into json files
with open(os.path.join(os.path.dirname(__file__), '../data/json/feuillage.json'), 'w') as f:
    #we get the representation of
    feuillage_json = repr(feuillage)[1:-1]
    feuillage_string = 'var feuillage = [{}];'.format(feuillage_json)
    f.write(feuillage_string)

with open(os.path.join(os.path.dirname(__file__),'../data/json/nomBinomial.json'), 'w') as f:
    nomBinomial_json = repr(nomBinomial)[1:-1]
    nomBinomial_string = 'var nomBinomial = [{}];'.format(nomBinomial_json)
    f.write(nomBinomial_string)

with open(os.path.join(os.path.dirname(__file__),'../data/json/arbre.json'), 'w') as f:
    arbre_json = repr(arbre)[1:-1]
    arbre_string = 'var arbre = [{}];'.format(arbre_json)
    f.write(arbre_string)
