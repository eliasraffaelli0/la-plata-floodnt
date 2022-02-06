const initialLat = -34.9187
const initialLng = -57.956
const mapLayerUrl = 'https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png'

export class Map {
    #drawnItems;
    #geometricFigures;

    constructor({ selector, geometricFigures }) {
        this.#drawnItems = new L.FeatureGroup();
        this.#geometricFigures = geometricFigures;
        this.#initializeMap(selector, this.#geometricFigures);

        this.map.on(L.Draw.Event.CREATED, (e) => {
            this.#eventHandler(e, this.map, this.#drawnItems, this.editControls, this.createControls)
        });

        this.map.on('draw:deleted', () => {
            this.#deleteHandler(this.map, this.editControls, this.createControls)
        });

    }


    #initializeMap(selector) {
        this.map = L.map(selector).setView([initialLat, initialLng], 13);
        L.tileLayer(mapLayerUrl).addTo(this.map);

        this.map.addLayer(this.#drawnItems);

        this.map.addControl(this.createControls);


    }


    #eventHandler(e, map, drawnItems, editControls, createControls) {
        const existingZones = Object.values(drawnItems._layers);

        if (existingZones.length == 0) {
            const type = e.layerType;
            const layer = e.layer;


            drawnItems.addLayer(layer);
            editControls.addTo(map);
            createControls.remove();
        }
    };

    //Esta función se agregó para poder editar los distintos elementos de la aplicación 
    //ya que al traerlos de la base de datos la instancia del mapa no los reconocía como
    //elementos dibujados en la variable drawnItems, por ende, fallaban las validaciones
    //lo que hace simplemente es agregar el elemento a la variable, eliminar los controles de 
    //creación y agregar los de edición

    addElement(element) {
        this.#drawnItems.addLayer(element);
        this.createControls.remove();
        this.editControls.addTo(this.map);

    }

    
    removeControls(){
        this.createControls.remove();
        this.editControls.remove();
    }

    // Si no se elimina el punto, no se eliminan los controles ya que si no se hace esta validación
    // pueden eliminarse los controles y para borrar el punto habría que refrescar la pagina
    #deleteHandler(map, editControls, createControls) {
        if (!this.hasValidZone()) {

            createControls.addTo(map);
            editControls.remove();

        }
    }


    hasValidMarker() {
        return this.drawnlayers.length === 1;
    }
    hasValidZone() {
        return this.drawnlayers.length === 1 && this.drawnlayers[0].getLatLngs().length >= 3;
    }

    get drawnlayers() {
        return Object.values(this.#drawnItems._layers);
    }

    get editControls() {
        return this.editControlsToolbar ||= new L.Control.Draw({
            draw: false,
            edit: {
                featureGroup: this.#drawnItems
            }

        });
    }

    get createControls() {
        return this.createControlsToolbar ||= new L.Control.Draw({
            draw: this.#geometricFigures
        });
    }
}


