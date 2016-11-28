$( document ).ready(function() {
    $('.ui.dropdown')
    .dropdown()
    ;

    let binomialtemplate = $('#binomialNameTemplate').html();

    jQuery.each(nomBinomial, function(i, val) {
        let template = $('#mapTemplate').html();
        var rendered = Mustache.render(binomialtemplate, {name: i});
        $( "#binomialName-menu" ).append(rendered);
    });



    var greenIcon = L.icon({
        iconUrl: './static/images/leaf-green.png',
        shadowUrl: './static/images/leaf-shadow.png',

        iconSize: [38, 95], // size of the icon
        shadowSize: [50, 64], // size of the shadow
        iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
        shadowAnchor: [4, 62], // the same for the shadow
        popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
    });

    function searchID() {
        id_arbre = document.getElementById("id_arbre").value.toLowerCase();

        current_arbre = arbre[id_arbre];

        //here we are making the join, if necessary
        if (typeof current_arbre["nomBinomial"] === 'string') {
            current_nomBinomial = nomBinomial[current_arbre["nomBinomial"]];
            current_nomBinomial["feuillage"] = feuillage[current_nomBinomial["feuillage"]];
            current_arbre["nomBinomial"] = current_nomBinomial;
        }

        //document.getElementById("info_arbre").appendChild(document.createElement('pre')).innerHTML = syntaxHighlight(JSON.stringify(current_arbre, null, 2));
        var marker = L.marker([current_arbre['latitude'], current_arbre['longitude']], {
            icon: greenIcon
        }).addTo(mymap);
        var template = $('#mapTemplate').html();
        var rendered = Mustache.render(template, current_arbre);
        console.log(current_arbre)
        marker.bindPopup(rendered).openPopup();
    }

    //now we create the map
    var mymap = L.map('mapid', {
        center: [45.7807286829, 4.85788730701],
        zoom: 15
    });

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'romathonat.23e4b6a0',
        accessToken: 'pk.eyJ1Ijoicm9tYXRob25hdCIsImEiOiJjaXZmM2J4M2cwMDM2Mnpxa253cHVkdHA0In0.FU0Ju6sGpWmlm74TEphPbA'
    }).addTo(mymap);
});
