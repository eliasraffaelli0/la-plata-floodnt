import { Map } from '../Map.js';


const flood_zone_geometric_figures = {
    circle: false,
    marker: false,
    polyline: false,

}
window.onload = () => {
    const mapita = new Map({
        selector: 'mapid',
        geometricFigures: flood_zone_geometric_figures
    });

    var pointList = zoneCoordinates.map(coor => new L.LatLng(coor.lat, coor.lng))
    var polygon = new L.Polygon(pointList, {color: zoneColor});
    mapita.addElement(polygon);
    mapita.removeControls();

}
