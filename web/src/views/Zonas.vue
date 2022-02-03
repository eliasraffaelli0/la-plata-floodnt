<template>
  <div>
    <l-map
      ref="mapa"
      @ready="onReady"
      style="height: 700px"
      :zoom="zoom"
      :center="center"
    >
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <div v-for="(zone, index) in zones" :key="`zone-${index}`">
        <l-polygon
          :lat-lngs="zone.coordinates"
          :color="zone.color"
          :fillColor="zone.color"
          :fill="true"
          :weight="3"
          :opacity="1.0"
          v-if="zone.state != 0"
        ></l-polygon>
      </div>
    </l-map>
    <table>
      <tr>
        <th>Zonas inundables</th>
      </tr>
      <div v-for="(zone, index) in zones" :key="`zone-${index}`">
        <tr>
          <!-- Se crean los links a las diferentes rutas dinamicas de las zonas específicas -->
          <router-link
            class="linkardo"
            :to="`/zonaEspecifica/${zone.id}`"
            v-if="zone.state != 0"
          >
            {{ zone.name }}
          </router-link>
          <br />
        </tr>
      </div>
    </table>
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
      points: [],
      zones: [],
    };
  },
  methods: {
    async onReady() {
      const pages = await this.fetchZones(1);

      if (pages > 1) {
        for (let i = 2; i <= pages; i++) {
          this.fetchZones(i);
        }
      }
    },

    async fetchZones(page) {
      const response = await axios.get(
        //`https://admin-grupo5.proyecto2021.linti.unlp.edu.ar/api/puntos/?page=${page}`
        `http://127.0.0.1:5000/api/zonas/?page=${page}`
      );
      response.data.zonas.forEach((zona) => {
        let coordenadas = zona.coordinates.map((coor) => [
          parseFloat(coor.latitude),
          parseFloat(coor.longitude),
        ]);
        let zonaParseada = {
          name: zona.name,
          coordinates: coordenadas,
          color: zona.color,
          zone_code: zona.zone_code,
          state: zona.state,
          id: zona.id,
        };
        this.zones = this.zones.concat(zonaParseada);
      });
      return response.data.pages;
    },
  },
};
</script>

<style >
.linkardo {
  text-decoration: none;
}
</style>
