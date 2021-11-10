import { MapClass as Map } from '../punto/MarkerClass.js';


const submitHandler = (event, map) => {


    if (!map.marker) {
        event.preventDefault();
        alert('Debes seleccionar una ubicación en el mapa, pelotudito.');
    }
    else {
        latlng = map.marker.getLatLng();
        document.getElementById('lat').setAttribute('value', latlng.lat);
        document.getElementById('lng').setAttribute('value', latlng.lng);
    }
}



window.onload = () => {
    const map = new Map({
        selector: 'mapid',
        addSearch: false
    });
    const form = document.getElementById('create-punto-form');

    form.addEventListener('submit', (event) => submitHandler(event, map));
}