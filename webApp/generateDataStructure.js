//this file will use the json file to generate a specific data structure to make the join with good performances

var arbreTampon = {};

for(var i=0; i<arbre.length; i++){
    arbreTampon[arbre[i].id] = arbre[i];
}

arbre = arbreTampon;

var nomBinomialTampon = {};

for(var i=0; i<nomBinomial.length; i++){
    var genreEspece = nomBinomial[i].genre+" "+nomBinomial[i].espece;
    nomBinomialTampon[genreEspece] = nomBinomial[i];
}

nomBinomial = nomBinomialTampon;

var feuillageTampon = {};

for(var i=0; i<feuillage.length; i++){
    feuillageTampon[feuillage[i].typeArbre] = feuillage[i];
}

feuillage = feuillageTampon;
