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
      <div v-for="(report, index) in reports" :key="`report-${index}`">
        <l-marker :lat-lng="[report.latitude, report.longitude]">
          <l-popup>
            {{ report.title }}<br />
            {{ report.state }}
          </l-popup>
        </l-marker>
      </div>
    </l-map>
  </div>
</template>


<script >
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import axios from "axios";
export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
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
      reports: [],
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
      const pages = await this.fetchReports(1);
      if (pages > 1) {
        for (let i = 2; i <= pages; i++) {
          this.fetchReports(i);
        }
      }
    },
    async fetchReports(page) {
      const response = await axios.get(
        //`https://admin-grupo5.proyecto2021.linti.unlp.edu.ar/api/puntos/?page=${page}`
        `http://127.0.0.1:5000/api/reports/?page=${page}`
      );
      this.reports = this.reports.concat(response.data.Reports);
      return response.data.pages;
    },
  },
};
</script>
