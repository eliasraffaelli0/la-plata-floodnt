<template>
  <div>
    <l-map
      class="marco"
      ref="mapa"
      @ready="onReady"
      style="height: 700px"
      :zoom="zoom"
      :center="center"
    >
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-polygon
        :lat-lngs="zone.coordinates"
        :color="zone.color"
        :fillColor="zone.color"
        :fill="true"
        :weight="3"
        :opacity="1.0"
      ></l-polygon>
    </l-map>
    <div class="table-responsive">
      <table class="table table-striped table-border table-sm table-hover">
        <thead>
          <tr class="table-light">
            <th>Nombre</th>
            <th>Código</th>
          </tr>
        </thead>
        <tbody>
          <tr class="table-info">
            <td class="table-info">{{ zone.name }}</td>
            <td class="table-info">{{ zone.zone_code }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script >
import { LMap, LTileLayer, LPolygon } from "@vue-leaflet/vue-leaflet";
import axios from "axios";
export default {
  components: {
    LMap,
    LTileLayer,
    LPolygon,
  },
  data() {
    let initialLat = -34.9187;
    let initialLng = -57.956;

    navigator.geolocation.getCurrentPosition((position) => {
      initialLat = position.coords.latitude;
      initialLng = position.coords.longitude;
    });
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      zoom: 13,
      center: [initialLat, initialLng],
      zone: {},
    };
  },
  methods: {
    async onReady() {
      await this.fetchZone(this.$route.params.id);
    },
    // this.$route.params.id con esto se accede al parametro dinámico que se envía por la ruta,
    // en nuestro caso es el id, que se utiliza para obtener la zona desde la API
    async fetchZone() {
      const response = await axios.get(
        //`https://admin-grupo5.proyecto2021.linti.unlp.edu.ar/api/puntos/?id=${id}`
        `http://127.0.0.1:5000/api/zonas/id/?id=${this.$route.params.id}`
      );
      let coordenadasParseadas = response.data.coordinates.map((coor) => [
        parseFloat(coor.latitude),
        parseFloat(coor.longitude),
      ]);
      let zonaParseada = {
        name: response.data.name,
        coordinates: coordenadasParseadas,
        color: response.data.color,
        zone_code: response.data.zone_code,
        state: response.data.state,
        id: response.data.id,
      };
      this.zone = zonaParseada;
      //   this.zone.push(zonaParseada);
    },
  },
};
</script>
