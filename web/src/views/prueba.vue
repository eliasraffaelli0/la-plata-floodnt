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
      <div v-for="(pos, index) in points" :key="`pos-${index}`">
        <div v-for="(point, index) in pos" :key="`point-${index}`">
          <l-marker :lat-lng="[point.latitude, point.longitude]"></l-marker>
        </div>
      </div>
    </l-map>
  </div>
</template>


<script >
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
import axios from "axios";
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
  //   getLocation() {

  //     if (navigator.geolocation) {
  //         navigator.geolocation.getCurrentPosition(showPosition);
  //     } else {
  //         x.innerHTML = "Geolocation is not supported by this browser.";
  //     }
  //     },

  // showPosition(position) {
  //     x.innerHTML = "Latitude: " + position.coords.latitude +
  //     "<br>Longitude: " + position.coords.longitude;
  //     },
  methods: {
    onClick(e) {
      if (e.latlng) {
        this.markerLatLng = e.latlng;
      }
      console.log(e);
    },
    async onReady() {
      const pages = await this.fetchPoints(1);

      if (pages > 1) {
        for (let i = 2; i <= pages; i++) {
          this.fetchPoints(i);
        }
      }
    },
    async fetchPoints(page) {
      const response = await axios.get(
        `http://127.0.0.1:5000/api/puntos/?page=${page}`
      );
      this.points.push(response.data.Points);
      return response.data.pages;
    },
  },
};
</script>
