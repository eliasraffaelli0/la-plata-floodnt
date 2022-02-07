<template>
  <div>
    <l-map
      class="marco"
      ref="mapa"
      @ready="onReady"
      style="height: 700px"
      :zoom="zoom"
      :center="center"
      @click="onClick"
    >
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <div v-for="(point, index) in points" :key="`point-${index}`">
        <l-marker
          :lat-lng="[point.latitude, point.longitude]"
          v-if="point.state != 0"
        >
          <l-popup>
            {{ point.name }}<br />
            Dirección: {{ point.address }} <br />
            Teléfono: {{ point.telephone }} <br />
            Mail: {{ point.email }}
          </l-popup>
        </l-marker>
      </div>
      <div v-for="(route, index) in routes" :key="`route-${index}`">
        <l-polyline
          :lat-lngs="route.coordinates"
          v-if="route.state != 0"
        ></l-polyline>
      </div>
    </l-map>
    <h2>Puntos de encuentro</h2>
    <div class="table-responsive">
      <table class="table table-striped table-border table-sm table-hover">
        <thead>
          <tr class="table-light">
            <th>Nombre</th>
            <th>Direccion</th>
            <th>Teléfono</th>
            <th>Mail</th>
          </tr>
        </thead>
        <tbody>
          <tr
            class="table-info"
            v-for="(point, index) in points"
            :key="`point-${index}`"
          >
            <td class="table-info">{{ point.name }}</td>
            <td class="table-info">{{ point.address }}</td>
            <td class="table-info">{{ point.telephone }}</td>
            <td class="table-info">{{ point.email }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <h2>Recorridos de evacuación</h2>
    <div class="table-responsive">
      <table class="table table-striped table-border table-sm table-hover">
        <thead>
          <tr class="table-light">
            <th>nombre</th>
            <th>descripcion</th>
          </tr>
        </thead>
        <tbody>
          <tr
            class="table-info"
            v-for="(route, index) in routes"
            :key="`route-${index}`"
          >
            <td class="table-info">
              {{ route.name }}
            </td>
            <td class="table-info">{{ route.description }} <br /></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script >
import {
  LMap,
  LTileLayer,
  LMarker,
  LPolyline,
  LPopup,
} from "@vue-leaflet/vue-leaflet";
import axios from "axios";
export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
    LPolyline,
    LPopup,
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
        `https://admin-grupo5.proyecto2021.linti.unlp.edu.ar/api/puntos/?page=${page}`
        // `http://127.0.0.1:5000/api/puntos/?page=${page}`
      );
      this.points = this.points.concat(response.data.Points);
      return response.data.pages;
    },

    async fetchRoutes(page) {
      const response = await axios.get(
        `https://admin-grupo5.proyecto2021.linti.unlp.edu.ar/api/puntos/?page=${page}`
        // `http://127.0.0.1:5000/api/recorridos/?page=${page}`
      );
      response.data.recorridos.forEach((recorrido) => {
        let coordenadas = recorrido.coordinates.map((coor) => [
          parseFloat(coor.latitude),
          parseFloat(coor.longitude),
        ]);
        let recorridoParseado = {
          name: recorrido.name,
          description: recorrido.description,
          coordinates: coordenadas,
          state: recorrido.state,
        };
        this.routes = this.routes.concat(recorridoParseado);
      });
      return response.data.pages;
    },
  },
};
</script>
