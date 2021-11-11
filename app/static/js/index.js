import { ZoneMap } from './ZoneMap.js';

const submitHandler = (event, mapita) => {


    if (!mapita.hasValidZone()) {
        event.preventDefault();
        alert('Debes dibujar una zona en el mapa.');
    }
    else {

        const coordinates = document.querySelector('#latitude');
        const lat = mapita.drawnlayers[0]._latlng
        coordinates.setAttribute('value', JSON.stringify(lat));



        // const name = document.querySelector('#name').value;
        // const address = document.querySelector('#address').value;
        // // const coordinates = mapita.drawnlayers[0].getLatLngs().flat().mapita(coordinate => {
        // //     return { lat: coordinate.lat, lng: coordinate.lng }
        // // });
        // const lat = mapita.drawnlayers[0]._latlng.lat
        // const lng = mapita.drawnlayers[0]._latlng.lng
        // const state = document.querySelector('#state').value;
        // const telephone = document.querySelector('#telephone').value;
        // const email = document.querySelector('#email').value;

        // const formData = new FormData();
        // const requestBody = {
        //     name: name,
        //     address: address,
        //     latitude: lat,
        //     longitude: lng,
        //     state: state,
        //     telephone: telephone,
        //     email: email
        // }
        // // formData.append('name', name);
        // // formData.append('address', address);
        // // formData.append('coordinates', JSON.stringify(coordinates));
        // // formData.append('latitude', lat);
        // // formData.append('longitude', lng);
        // // formData.append('state', state);
        // // formData.append('telephone', telephone);
        // // formData.append('email', email);

        // // fetch('/puntos_de_encuentro/nuevo', {
        // //     method: 'POST',
        // //     headers: {
        // //         'Accept': 'application/json',
        // //         'Content-Type': 'application/json'
        // //     },
        // //     body: JSON.stringify(requestBody)
        // // })
        // console.log(requestBody);
        // $.ajax({
        //     method: "POST",
        //     url: '/puntos_de_encuentro/nuevo',
        //     headers: {
        //         'Accept': 'application/json',
        //         'Content-Type': 'application/json'
        //     },
        //     data: JSON.stringify(requestBody),
        //     success: function (data, textStatus, jqXHR) {
        //         window.location.href = '/puntos_de_encuentro?puntoCreado=true'
        //     },
        //     error: function (jqXHR, textStatus, errorThrown) {
        //         debugger
        //         }
        //     });
    }
}

const punto_geometric_figures = {
    circle: false,
    polyline: false,
    rectangle: false,
    polygon: false,

}
const kk = () => {
    const mapita = new ZoneMap({
        selector: 'mapid',
        addSearch: false,
        geometricFigures: punto_geometric_figures
    });
    const form = document.querySelector('#create-punto-form');

    form.addEventListener('submit', (event) => submitHandler(event, mapita));
}
window.onload = kk