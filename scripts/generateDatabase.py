# coding: utf-8 
from sanitize import sanitize
import json
import os
from wikipediaQueryEngine import WikipediaQueryEngine
from utils import hashableDict, hashableDictArbre

"""
This script generate the json database.
"""
PATH_JSON = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'webApp', 'json')
PATH_INCOMPLETE_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'webApp', 'json','incomplete_data')
USE_WIKIPEDIA = False

def load_gps():
    """
    Load the gps from arbreGPS.txt. Return the GPS
    """
    gps = {}
    with open(os.path.join(os.path.dirname(__file__), '../data/arbresGPS.txt'), 'r+') as f:
        for line in f:
            line = line.replace(' ', '')
            id_arbre, latitude, longitude = line.split(',')
            longitude = longitude.rstrip()
            gps['ar'+str(id_arbre)] = (latitude, longitude)
    return gps

sanitized_data, incomplete_data = sanitize()

# those are the tables of our model
arbre = set()
nomBinominal = set()
feuillage = set()
data_without_GPS = []
# we load the gps into the memory
gps = load_gps()


if(USE_WIKIPEDIA):
    w = WikipediaQueryEngine()

# for each sanitized_data, we format to JSON correctly
for line in sanitized_data:
    gps_cordinate = True
    tree_latitude, tree_longitude = 0, 0
    try:
        tree_latitude, tree_longitude = gps[line[1]]
    except:
        # print("Missing gps coordinates for :"+line[1])
        gps_cordinate = False

    # we do not add this data if we don't have the gps informations
    if gps_cordinate:
        # we correct datas with wikipedia, if requested
        if USE_WIKIPEDIA:
            print('{} {} {}'.format(line[2], line[3], line[4]))
            r = w.enrich_data(line[2], line[3], line[4])
            #print(r)

            if r:
                #line[3] = normalize(r['genus'])
                #line[4] = normalize(r['species'])

                #this line is a nested informations
                line[9] = r['info_french']
                line[10] = r['genus_page']
                line[11] = r['species_page']

        new_feuillage = {'typeArbre': line[5]}
        feuillage.add(hashableDict(new_feuillage))

        # the firt letter must be upper
        genre = line[3][0].upper()+line[3][1:]

        new_nomBinominal = {'genre': genre,'espece': line[4], 'nom_vernaculaire':line[2], 'feuillage': line[5],
        'info_francais': hashableDict(line[9]), \
        'genus_page': hashableDict(line[10]), 'species_page': hashableDict(line[11])}

        # we add this data only if it is not here yet
        nomBinominal.add(hashableDict(new_nomBinominal))

        new_arbre = {'id': line[1],'hauteur': line[6], 'diametreTronc': line[7], 'diametreCouronne': line[8],\
        'latitude' : tree_latitude, 'longitude': tree_longitude, 'nomBinominal': genre+" "+line[4]}
        arbre.add(hashableDictArbre(new_arbre))
    else:
        data_without_GPS.append(line)

# now we dump datas into json files
with open(os.path.join(PATH_JSON,'feuillage.json'), 'w') as f:
    # we get the representation of
    feuillage_json = list(feuillage)
    f.write(json.dumps(feuillage_json))

with open(os.path.join(PATH_JSON,'nomBinominal.json'), 'w') as f:
    nomBinominal_json = list(nomBinominal)
    f.write(json.dumps(nomBinominal_json))

with open(os.path.join(PATH_JSON,'arbre.json'), 'w') as f:
    arbre_json = list(arbre)
    f.write(json.dumps(arbre_json))

if os.path.isdir(PATH_INCOMPLETE_DATA) == False:
        os.makedirs(PATH_INCOMPLETE_DATA)

with open(os.path.join(PATH_INCOMPLETE_DATA,'incomplete_data.json'), 'w') as f:
    f.write('Number: {}\n'.format(len(incomplete_data)))
    f.write(json.dumps(incomplete_data))

with open(os.path.join(PATH_INCOMPLETE_DATA,'data_without_GPS.json'), 'w') as f:
    f.write('Number: {}\n'.format(len(data_without_GPS)))
    f.write(json.dumps(data_without_GPS))
