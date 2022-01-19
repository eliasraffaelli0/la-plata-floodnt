<template>
  <div>
    <div>{{ points }}</div>
    <l-map
      ref="mapa"
      @ready="onReady"
      style="height: 700px"
      :zoom="zoom"
      :center="center"
      @click="onClick"
    >
      <!-- El doble for es porque de la api obtenemos una lista de diccionarios y estos diccionarios 
      tienen la cantidad de elementos por página, definida en la aplicación privada, de puntos.-->
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <div v-for="(point, index) in points" :key="`point-${index}`">
        <l-marker :lat-lng="[point.latitude, point.longitude]"></l-marker>
      </div>
      <div v-for="(route, index) in routes" :key="`route-${index}`">
        <l-polyline :lat-lngs="route"></l-polyline>
      </div>
      <!-- <div v-for="(pos, index) in routes" :key="`pos-${index}`">
        <div v-for="(route, index) in pos" :key="`route-${index}`">
          <l-polyline: lat-lngs="[route.latitude, route.longitude]"></l-polyline>
          <l-polyline :lat-lngs="polyline.latlngs" :color="polyline.color"></l-polyline>
        </div>
      </div> -->
    </l-map>
  </div>
</template>


<script >
// import L from "leaflet";
import { LMap, LTileLayer, LMarker, LPolyline } from "@vue-leaflet/vue-leaflet";
import axios from "axios";
export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPolyline,
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
      routes: [],
    };
  },
  methods: {
    onClick(e) {
      if (e.latlng) {
        this.markerLatLng = e.latlng;
      }
      console.log(e);
    },
    async onReady() {
      const pages = await this.fetchPoints(1);
      const pages2 = await this.fetchRoutes(1);
      if (pages > 1) {
        for (let i = 2; i <= pages; i++) {
          this.fetchPoints(i);
        }
      }

      if (pages2 > 1) {
        for (let i = 2; i <= pages; i++) {
          this.fetchRoutes(i);
        }
      }
    },
    async fetchPoints(page) {
      const response = await axios.get(
        //`https://admin-grupo5.proyecto2021.linti.unlp.edu.ar/api/puntos/?page=${page}`
        `http://127.0.0.1:5000/api/puntos/?page=${page}`
      );
      this.points = this.points.concat(response.data.Points);
      // this.points.push(response.data.Points);
      return response.data.pages;
    },

    async fetchRoutes(page) {
      const response = await axios.get(
        //`https://admin-grupo5.proyecto2021.linti.unlp.edu.ar/api/puntos/?page=${page}`
        `http://127.0.0.1:5000/api/recorridos/?page=${page}`
      );
      // let pointList = [];

      //response.data.recorridos.map((coor) => new L.LatLng(coor["coordinates"]["latitude"], coor["coordinates"]["longitude"]))
      //response.data.recorridos.map((coor) => console.log(coor["coordinates"][0]["longitude"]))
      // hacer un doble for each o hay alguna manera mas eficiente/facil
      // debugger;
      response.data.recorridos.forEach((recorrido) => {
        let coordenadas = recorrido.coordinates.map((coor) => [
          parseFloat(coor.latitude),
          parseFloat(coor.longitude),
        ]);
        // let recorridoParseado = {};
        this.routes.push(coordenadas);
      });
      return response.data.pages;
    },
  },
};
</script>
