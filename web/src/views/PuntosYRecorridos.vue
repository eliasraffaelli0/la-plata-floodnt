<template>
  <div>
    <l-map
      ref="mapa"
      @ready="onReady"
      style="height: 700px"
      :zoom="zoom"
      :center="center"
      @click="onClick"
    >
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <div v-for="(punto, index) in points" :key="`punto-${index}`">
        <l-marker :lat-lng="[punto.latitude, punto.longitude]"></l-marker>
      </div>
    </l-map>
  </div>
</template>


<script >
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
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
    };
  },
  methods: {
    onClick(e) {
      if (e.latlng) {
        this.markerLatLng = e.latlng;
      }
      console.log(e);
    },
    onReady() {
      const axios = require("axios");
      axios.get("http://127.0.0.1:5000/api/puntos/").then((res) => {
        this.points = res.data.Points;
        console.log(res);
      });
    },
  },
};
</script>
