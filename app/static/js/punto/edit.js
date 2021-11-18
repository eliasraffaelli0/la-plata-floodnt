import { Map } from '../Map.js';

const submitHandler = (event, mapita) => {


    if (!mapita.hasValidMarker()) {
        event.preventDefault();
        alert('Debes dibujar una zona en el mapa.');
    }
    else {

        const coordinates = document.querySelector('#coordinates');
        const lat = mapita.drawnlayers[0]._latlng
        coordinates.setAttribute('value', JSON.stringify(lat));
    }
}

const punto_geometric_figures = {
    circle: false,
    polyline: false,
    rectangle: false,
    polygon: false,

}
window.onload = () => {
    const mapita = new Map({
        selector: 'mapid',
        addSearch: false,
        geometricFigures: punto_geometric_figures
    });
    // var marker = L.marker([-34.9187, -57.956].addTo(mapita))
    //     marker = L.marker([50.84673, 4.35247]).addTo(map);
    //     const initialLat = -34.9187
    // const initialLng = -57.956
    // marker = L.marker([-34.9187, -57.956])
    // this.map.addLayer(marker)
    const form = document.querySelector('#create-punto-form');
    const latitude = document.querySelector('#latitude').getAttribute("data-latitude");
    const longitude = document.querySelector('#longitude').getAttribute("data-longitude");

    var marker = L.marker([parseFloat(latitude), parseFloat(longitude)]);
    // mapita.map.addLayer(marker);
    mapita.agregarCosa(marker);

    form.addEventListener('submit', (event) => submitHandler(event, mapita));
}
