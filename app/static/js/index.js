import { ZoneMap } from '../js/ZoneMap.js';

const submitHandler = (event, map) => {
    event.preventDefault();

    if (!map.hasValidZone()) {
        alert('Debes dibujar una zona en el mapa.');
    }
    else {
        const name = document.querySelector('#name').value;
        const coordinates = map.drawnlayers[0].getLatLngs().flat().map(coordinate => {
            return { lat: coordinate.lat, lng: coordinate.lng }
        });

        const formData = new FormData();
        formData.append('name', name);
        formData.append('address', address);
        formData.append('coordinates', JSON.stringify(coordinates));
        formData.append('state', state);
        formData.append('telephone', telephone);
        formData.append('email', email);


        fetch('/puntos_de_encuentro/nuevo', {
            method: 'POST',
            body: formData
        })
    }
}

const punto_geometric_figures = {
    circle: false,
    polyline: false,
    rectangle: false,
    polygon: false,

}

window.onload = () => {
    const map = new ZoneMap({
        selector: 'mapid',
        addSearch: false,
        geometricFigures: punto_geometric_figures
    });
    const form = document.querySelector('#create-punto-form');

    form.addEventListener('submit', (event) => submitHandler(event, map));
}