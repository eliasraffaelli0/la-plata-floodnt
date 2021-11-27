import { Map } from '../Map.js';

const submitHandler = (event, mapita) => {


    if (!mapita.hasValidMarker()) {
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

const flood_zone_geometric_figures = {
    circle: false,
    marker: false,
    polyline: false,

}
window.onload = () => {
    const mapita = new Map({
        selector: 'mapid',
        addSearch: false,
        geometricFigures: flood_zone_geometric_figures
    });
    const form = document.querySelector('#create-evacuationRoute-form');

    var pointList = zoneCoordinates.map(coor => new L.LatLng(coor.lat, coor.lng))
    var polygon = new L.Polygon(pointList, {color: zoneColor});
    mapita.addElement(polygon);

    form.addEventListener('submit', (event) => submitHandler(event, mapita));
}
