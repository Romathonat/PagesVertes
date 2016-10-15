from sanitize import sanitize
import json


sanitized_datas = sanitize()

#those are the tables of our model
#python dict are hashable, very good to gain perfs
arbre = {}
nomBinomial = {}
feuillage = {}

#we load the gps into the memory
gps = {}
with open('./data/arbresGPS.txt', 'r+') as f:
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
        feuillage.setdefault(line[5], new_feuillage)

        new_nomBinomial = {'genre': line[3] ,'espece': line[4], 'nomFrancais':line[2], 'feuillage': line[5]}
        #we add this data only if it not here yet
        nomBinomial.setdefault(line[3]+" "+line[4], new_nomBinomial)

        new_arbre = {'id': line[1],'hauteur': line[6], 'diametreTronc': line[7], 'diametreCouronne': line[8],\
        'latitude' : tree_latitude, 'longitude': tree_longitude, 'nomBinomial': line[3]+" "+line[4]}
        arbre[line[1]] = new_arbre


#now we dump datas into json files
with open('./data/json/feuillage.json', 'w') as f:
    json.dump(feuillage, f)

with open('./data/json/nomBinomial.json', 'w') as f:
    json.dump(nomBinomial, f)

with open('./data/json/arbre.json', 'w') as f:
    json.dump(arbre, f)
