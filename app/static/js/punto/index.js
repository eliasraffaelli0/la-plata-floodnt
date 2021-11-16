import { Map } from '../Map.js';

const submitHandler = (event, mapita) => {


    if (!mapita.hasValidMarker()) {
        event.preventDefault();
        alert('Debes dibujar una zona en el mapa.');
    }
    else {

        const coordinates = document.querySelector('#coordinates');
        const lat = mapita.drawnlayers[0]._latlng
        debbuger
        coordinates.setAttribute('value', JSON.stringify(lat));
    }
}

const punto_geometric_figures = {
    circle: false,
    polyline: false,
    rectangle: false,
    polygon: false,

}
const kk = () => {
    const mapita = new Map({
        selector: 'mapid',
        addSearch: false,
        geometricFigures: punto_geometric_figures
    });
    const form = document.querySelector('#create-punto-form');

    form.addEventListener('submit', (event) => submitHandler(event, mapita));
}
window.onload = kk