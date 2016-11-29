//this file will use the json files to generate a specific data structure to make the join with good performances

var arbre;
var feuillage;
var nomBinominal;


$.ajax({
    url: 'json/arbre.json',
    async: false,
    dataType: 'json',
    success: function (json) {
        arbre = json;
    }
});

$.ajax({
    url: 'json/feuillage.json',
    async: false,
    dataType: 'json',
    success: function (json) {
        feuillage = json;
    }
});

$.ajax({
    url: 'json/nomBinominal.json',
    async: false,
    dataType: 'json',
    success: function (json) {
        nomBinominal = json;
    }
});


var arbreTampon = {};

for(var i=0; i<arbre.length; i++){
    arbreTampon[arbre[i].id] = arbre[i];
}

arbre = arbreTampon;

var nomBinominalTampon = {};

for(var i=0; i<nomBinominal.length; i++){
    var genreEspece = nomBinominal[i].genre+" "+nomBinominal[i].espece;
    nomBinominalTampon[genreEspece] = nomBinominal[i];
}

nomBinominal = nomBinominalTampon;

var feuillageTampon = {};

for(var i=0; i<feuillage.length; i++){
    feuillageTampon[feuillage[i].typeArbre] = feuillage[i];
}

feuillage = feuillageTampon;
