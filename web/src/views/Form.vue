<template>
<div>
  <l-map style="height: 700px" :zoom="zoom" :center="center" @click="onClick">
    <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
    <l-marker :lat-lng="markerLatLng"></l-marker>
  </l-map>
</div>
</template>

<script>
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data() {
    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      zoom: 14,
      center: [-34.9187,-57.956],
      markerLatLng: [],
    };
  },
  methods: {
    onClick(e){
      if(e.latlng){
        this.markerLatLng = e.latlng;
      }
      console.log(e);
  }
}
}
</script>
