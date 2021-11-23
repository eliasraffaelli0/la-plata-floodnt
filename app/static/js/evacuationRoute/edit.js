import { Map } from '../Map.js';

const submitHandler = (event, mapita) => {


    if (!mapita.hasValidZone()) {
        event.preventDefault();
        alert('Debes dibujar una zona válida en el mapa.\nPara que sea válida debe contener al menos 3 puntos');
    }
    else {

        const coordinates = document.querySelector('#coordinates');
        const coorr = mapita.drawnlayers[0].getLatLngs().flat().map(coordinate => {
            return { lat: coordinate.lat, lng: coordinate.lng }
        });
        coordinates.setAttribute('value', JSON.stringify(coorr));
    }
}

const evacuationRoute_geometric_figures = {
    circle: false,
    marker: false,
    rectangle: false,
    polygon: false,

}
window.onload = () => {
    const mapita = new Map({
        selector: 'mapid',
        addSearch: false,
        geometricFigures: evacuationRoute_geometric_figures
    });
    const form = document.querySelector('#create-evacuationRoute-form');
    coordinates = document.querySelector('#coordinates').getAttribute("data-coordinates");


    form.addEventListener('submit', (event) => submitHandler(event, mapita));
}
