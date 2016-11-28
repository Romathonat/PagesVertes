var treeMapTemplate
var searchMap;
var greenIcon = L.icon({
    iconUrl: './static/images/leaf-green.png',
    shadowUrl: './static/images/leaf-shadow.png',
    iconSize: [38, 95], // size of the icon
    shadowSize: [50, 64], // size of the shadow
    iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
    shadowAnchor: [4, 62], // the same for the shadow
    popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
});
var markers = []


function setMarker(currentTree){
    var marker = L.marker([currentTree['latitude'], currentTree['longitude']], {
        icon: greenIcon
    }).addTo(searchMap);
    var renderedTemplate = Mustache.render(treeMapTemplate, currentTree);
    marker.bindPopup(renderedTemplate).openPopup();
    markers.push(marker)
}

function clearMap(){
    markers=[]
}

$( document ).ready(function() {
    treeMapTemplate = $('#mapTemplate').html();

    searchMap = L.map('mapId', {
        center: [45.7807286829, 4.85788730701],
        zoom: 15
    });

    L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
        attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
        maxZoom: 18,
        id: 'romathonat.23e4b6a0',
        accessToken: 'pk.eyJ1Ijoicm9tYXRob25hdCIsImEiOiJjaXZmM2J4M2cwMDM2Mnpxa253cHVkdHA0In0.FU0Ju6sGpWmlm74TEphPbA'
    }).addTo(searchMap);
});
