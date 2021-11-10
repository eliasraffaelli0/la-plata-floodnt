const initialLat = -34.9187
const initialLng = -57.956
const mapLayerUrl = 'https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png'

export class MapClass {
    constructor({ selector, addSearch }) {

        this.initializeMap(selector);
        if (addSearch) {
            this.addSearchControl();
        }
        this.map.addEventListener('click', (e) => {
            this.addMarker(e.latlng)
        });
    }



    initializeMap(selector) {
        this.map = L.map(selector).setView([initialLat, initialLng], 13);
        L.tileLayer(mapLayerUrl).addTo(this.map);

    };

    addMarker({ lat, lng }) {
        if (this.marker) {
            this.marker.remove();
        };
        this.marker = L.marker([lat, lng]).addTo(this.map);
    };

    addSearchControl() {
        L.control.scale().addTo(this.map);
        let searchControl = new L.esri.Controls.Geosearch().addTo(this.map);

        let results = new L.LayerGroup().addTo(this.map);

        searchControl.on('results', (data) => {
            results.clearLayers();

            if (data.results.length > 0) {
                this.addMarker(data.results[0].latlng);
            };
        });
    }
}

