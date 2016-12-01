class SearchMap {
    constructor(divId) {
        this.treeMapTemplate = $('#mapMarkerTemplate').html();

        this.searchMap = L.map(divId, {
            center: [45.7807286829, 4.85788730701],
            zoom: 15,
            maxZoom: 18
        });

        this.markers = L.markerClusterGroup(); //markerClusterGroup layer object containing the markers
        this.searchMap.addLayer(this.markers);

        this.markersIndex = {}; //Index that allows finding a marker with tree id

        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
            attribution: 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://mapbox.com">Mapbox</a>',
            maxZoom: 18,
            id: 'romathonat.23e4b6a0',
            accessToken: 'pk.eyJ1Ijoicm9tYXRob25hdCIsImEiOiJjaXZmM2J4M2cwMDM2Mnpxa253cHVkdHA0In0.FU0Ju6sGpWmlm74TEphPbA'
        }).addTo(this.searchMap);

        this.greenIcon = L.icon({
            iconUrl: './static/images/leaf-green.png',
            shadowUrl: './static/images/leaf-shadow.png',
            iconSize: [38, 95], // size of the icon
            shadowSize: [50, 64], // size of the shadow
            iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
            shadowAnchor: [4, 62], // the same for the shadow
            popupAnchor: [-3, -76] // point from which the popup should open relative to the iconAnchor
        });

        this.currentOpenedMarker = {};
    }


    setMarker(currentTree){
        let marker = L.marker([currentTree.latitude, currentTree.longitude], {
            icon: this.greenIcon
        });
        let renderedTemplate = Mustache.render(this.treeMapTemplate, currentTree);
        marker.bindPopup(renderedTemplate);
        this.markers.addLayer(marker);
        this.markersIndex[currentTree.id] = marker;
    }

    setViewToMarker(tree) {
        this.searchMap.setView(new L.LatLng(tree.latitude, tree.longitude), 16);
    }

    highlightMarker(tree){
        let renderedTemplate = Mustache.render(this.treeMapTemplate, tree);
        let marker = this.markersIndex[tree.id];
        let cluster = this.markers.getVisibleParent(marker);
        cluster.bindPopup(marker._popup._content).openPopup();
        this.currentOpenedMarker = cluster;
    }

    unhighlightMarker(tree){
        this.currentOpenedMarker.closePopup();
    }

    clearMap(){
        this.markers.clearLayers();
        this.markersIndex = {}
    }
}
