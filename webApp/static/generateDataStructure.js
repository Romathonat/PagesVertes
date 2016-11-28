//this file will use the json files to generate a specific data structure to make the join with good performances

var arbre;
var feuillage;
var nomBinomial;


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
    url: 'json/nomBinomial.json',
    async: false,
    dataType: 'json',
    success: function (json) {
        nomBinomial = json;
    }
});


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
