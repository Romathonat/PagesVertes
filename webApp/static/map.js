    class SearchMap {
    constructor(divId) {
        this.treeMapTemplate = $('#mapMarkerTemplate').html();

        this.maxZoom = 22;
        this.defaultZoom = 15;
        this.defaultLatitude = 45.7807286829;
        this.defaultLongitude = 4.85788730701;

        this.searchMap = L.map(divId, {
            center: [this.defaultLatitude, this.defaultLongitude],
            zoom: this.defaultZoom,
            maxZoom: this.maxZoom
        });

        this.clusterViewLayer = L.markerClusterGroup(); //markerClusterGroup layer object containing the markers
        this.standardViewLayer = L.featureGroup();
        this.searchMap.addLayer(this.clusterViewLayer);

        this.markersIndex = {}; //Index that allows finding a marker with tree id

        L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png?', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
            maxZoom: this.maxZoom
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

        //make the layers accessible in the custom button onClick event
        var clusterViewLayer = this.clusterViewLayer;
        var standardViewLayer = this.standardViewLayer;

        this.clusteringToggleButton = L.easyButton({
            states: [{
                    stateName: 'clusterView',
                    icon:      '<i class="tree icon"></i>',
                    title:     'Switch to standard view',
                    onClick: function(btn, map) {
                        clusterViewLayer.remove();
                        map.addLayer(standardViewLayer);
                        btn.state('standardView');
                    }
                }, {
                    stateName: 'standardView',
                    icon:      '<i class="block layout icon"></i>',
                    title:     'Switch to cluster view',
                    onClick: function(btn, map) {
                        standardViewLayer.remove();
                        map.addLayer(clusterViewLayer);
                        btn.state('clusterView');
                    }
            }]
        });

        this.clusteringToggleButton.addTo( this.searchMap );
    }


    setMarker(currentTree){
        let marker = L.marker([currentTree.latitude, currentTree.longitude], {
            icon: this.greenIcon
        });
        let renderedTemplate = Mustache.render(this.treeMapTemplate, currentTree);
        marker.bindPopup(renderedTemplate);
        this.clusterViewLayer.addLayer(marker);
        this.standardViewLayer.addLayer(marker);
        this.markersIndex[currentTree.id] = marker;
        marker.on("click", function() {
            updateTreeDetails(currentTree);
        });
    }

    resetView(){
        this.searchMap.setView(new L.LatLng(this.defaultLatitude, this.defaultLongitude), this.defaultZoom);
    }

    setViewToMarker(tree) {
        this.searchMap.setView(new L.LatLng(tree.latitude, tree.longitude), 16);
    }

    highlightMarker(tree){
        let marker = this.markersIndex[tree.id];
        if (this.clusteringToggleButton._currentState.stateName === "clusterView") {
            let cluster = this.clusterViewLayer.getVisibleParent(marker);
            cluster.bindPopup(marker._popup._content).openPopup();
            this.currentOpenedMarker = cluster;
        }
        else {
            marker.openPopup();
            this.currentOpenedMarker = marker;
        }

    }

    unhighlightMarker(tree){
        this.currentOpenedMarker.closePopup();
    }

    clearMap(){
        this.clusterViewLayer.clearLayers();
        this.standardViewLayer.clearLayers();
        this.markersIndex = {};
    }
}
