<template>
  <div>
    <p>Click the button to get your coordinates.</p>
    <!-- 
    <button onclick="getLocation()">Try It</button>

    <p id="demo"></p> -->
    <button @click="locatorButtonPressed">hola</button>
    <l-map
      ref="mapa"
      @ready="onReady"
      style="height: 700px"
      :zoom="zoom"
      :center="center"
      @click="onClick"
    >
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <!-- <l-marker :lat-lng="markerLatLng"></l-marker> -->
    </l-map>
  </div>
</template>

<script>
import { LMap, LTileLayer } from "@vue-leaflet/vue-leaflet";
// LMarker
export default {
  components: {
    LMap,
    LTileLayer,
    // LMarker,
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
      zoom: 14,
      center: [initialLat, initialLng],
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
    locatorButtonPressed() {
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
          (position) => {
            this.data;
            console.log(position.coords.latitude);
            console.log(position.coords.longitude);
          },
          (error) => {
            console.log(error.message);
          }
        );
      } else {
        console.log("your browser kk");
      }
    },
    // onReady() {
    //   this.$refs.mapa.locate();
    // },
  },
};
</script>

