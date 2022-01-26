<template>
  <div>
    <div>{{ markerLatLng }}</div>
    <form action="">
      <input type="text" hidden value="{{markerLatLng}}" />
      <p>
        <label for="">Titulo</label> <br />
        <input type="text" name="title" />
      </p>
      <p>
        <label>Categoría</label> <br />
        <select id="category" class="" name="category">
          <option value="cat1">Categoría 1</option>
          <option value="cat2">Categoría 2</option>
          <option value="cat3">Categoría 3</option>
          <option value="cat4">Categoría 4</option>
        </select>
      </p>
      <l-map
        ref="mapa"
        @ready="onReady"
        style="height: 700px"
        :zoom="zoom"
        :center="center"
        @click="onClick"
      >
        <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
        <l-marker :lat-lng="markerLatLng"></l-marker>
      </l-map>
      <p>
        <label for="">Descripción</label> <br />
        <textarea
          name="description"
          id="description"
          placeholder="Descripción"
          cols="50"
          rows="5"
        ></textarea>
      </p>
      <p>
        <label for="">Teléfono del denunciante</label> <br />
        <input type="text" name="complainant_telephone" />
      </p>
      <p>
        <label for="">Email del denunciante</label> <br />
        <input type="text" name="complainant_email" />
      </p>
      <p>
        <label for="">Nombres del denunciante</label> <br />
        <input type="text" name="complainant_name" />
      </p>
      <p>
        <label for="">Apellidos del denunciante</label> <br />
        <input type="text" name="complainant_last_name" />
      </p>
      <p>
        <input
          class="btn btn-outline-dark btn-sm"
          type="submit"
          value="Crear denuncia"
        />
      </p>
    </form>
  </div>
</template>


<script >
import { LMap, LTileLayer, LMarker } from "@vue-leaflet/vue-leaflet";
// import axios from "axios";
export default {
  components: {
    LMap,
    LTileLayer,
    LMarker,
  },
  data() {
    let initialLat = -34.9187;
    let initialLng = -57.956;

    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      zoom: 13,
      center: [initialLat, initialLng],
      markerLatLng: [],
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
  },
};
</script>
