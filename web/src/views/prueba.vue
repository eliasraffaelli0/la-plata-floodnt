<template>
<div>
    <p>Click the button to get your coordinates.</p>
<!-- 
    <button onclick="getLocation()">Try It</button>

    <p id="demo"></p> -->
    <button @click="locatorButtonPressed">hola</button>
  <l-map ref="mapa" @ready="onReady" style="height: 700px" :zoom="zoom" :center="center" @click="onClick">
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
      var x,y;
        navigator.geolocation.getCurrentPosition(function(position){
            console.log(position);
            
        }
        );
        console.log(x);
        console.log(y);
        return {
        url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
        zoom: 14,
        
        }

      
  },
  computed:{

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
        onClick(e){
        if(e.latlng){
            this.markerLatLng = e.latlng;
        }
        console.log(e);
    },
    locatorButtonPressed(){
        if (navigator.geolocation){
            navigator.geolocation.getCurrentPosition(position => {
                console.log(position.coords.latitude);
                console.log(position.coords.longitude);
            },
            error => {
                console.log(error.message);
            }
            );
        } else {
            console.log("your browser kk");
        }
    },
    onReady(){
        debugger;
        this.$refs.mapa.locate()
    }

  }
    
}
    



</script>

