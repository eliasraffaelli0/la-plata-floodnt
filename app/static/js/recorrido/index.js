import { ZoneMap } from '../ZoneMap.js';

const submitHandler = (event, mapita) => {
    event.preventDefault();

    if (!mapita.hasValidZone()) {
        alert('Debes dibujar una zona en el mapa.');
    }
    else {
        const name = document.querySelector('#name').value;
        const address = document.querySelector('#address').value;
        // const coordinates = map.drawnlayers[0].getLatLngs().flat().map(coordinate => {
        //     return { lat: coordinate.lat, lng: coordinate.lng }
        // });
        const lat = mapita.drawnlayers[0]._latlng.lat
        const lng = mapita.drawnlayers[0]._latlng.lng
        const state = document.querySelector('#state').value;
        const telephone = document.querySelector('#telephone').value;
        const email = document.querySelector('#email').value;

        const formData = new FormData();
        formData.append('name', name);
        formData.append('address', address);
        // formData.append('coordinates', JSON.stringify(coordinates));
        formData.append('latitude', lat);
        formData.append('longitude', lng);
        formData.append('state', state);
        formData.append('telephone', telephone);
        formData.append('email', email);

        // fetch('/puntos_de_encuentro/nuevo', {
        //     method: 'POST',
        //     body: formData
        // })
        $.ajax({
            type: "POST",
            url: '/puntos_de_encuentro/nuevo',
            data: formData,
            processData: false,
            //contentType: "application/json"
        });
    }
}

const recorrido_geometric_figures = {
    circle: false,
    marker: false,
    rectangle: false,
    polygon: false,

}

window.onload = () => {
    const mapita = new ZoneMap({
        selector: 'mapid',
        addSearch: false,
        geometricFigures: recorrido_geometric_figures
    });
    const form = document.querySelector('#create-recorrido-form');

    form.addEventListener('submit', (event) => submitHandler(event, mapita));
}