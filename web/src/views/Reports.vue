<template>
  <div>
    <form v-on:submit.prevent="submitForm">
      <input type="text" hidden v-model="form.latitude" />
      <input type="text" hidden v-model="form.longitude" />
      <p>
        <label>Titulo</label> <br />
        <input type="text" name="title" v-model="form.title" />
      </p>
      <p>
        <label>Categoría</label> <br />
        <select id="category" class="" name="category" v-model="form.category">
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
        <label>Descripción</label> <br />
        <textarea
          name="description"
          id="description"
          placeholder="Descripción"
          cols="50"
          rows="5"
          v-model="form.description"
        ></textarea>
      </p>
      <p>
        <label>Teléfono del denunciante</label> <br />
        <input
          type="text"
          name="complainant_telephone"
          v-model="form.complainant_telephone"
        />
      </p>
      <p>
        <label>Email del denunciante</label> <br />
        <input
          type="text"
          name="complainant_email"
          v-model="form.complainant_email"
        />
      </p>
      <p>
        <label>Nombres del denunciante</label> <br />
        <input
          type="text"
          name="complainant_name"
          v-model="form.complainant_name"
        />
      </p>
      <p>
        <label>Apellidos del denunciante</label> <br />
        <input
          type="text"
          name="complainant_last_name"
          v-model="form.complainant_last_name"
        />
      </p>
      <p>
        <button>Crear denuncia</button>
        <input type="submit" value="Crear denuncia" />
      </p>
    </form>
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

    return {
      url: "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
      zoom: 13,
      center: [initialLat, initialLng],
      markerLatLng: {},
      form: {
        title: "",
        category: "",
        complainant_email: "",
        complainant_telephone: "",
        complainant_name: "",
        complainant_last_name: "",
        description: "",
        latitude: "",
        longitude: "",
      },
    };
  },
  methods: {
    onClick(e) {
      if (e.latlng) {
        this.markerLatLng = e.latlng;
        this.form.latitude = e.latlng.lat;
        this.form.longitude = e.latlng.lng;
        console.log(e.latlng);
      }
    },
  },
  submitForm() {
    debugger;
    axios.post("http://127.0.0.1:5000/api/reports/", this.form).then((res) => {
      return confirm(`Denuncia creada ${res.status}`);
    });
  },
};
// form.addEventListener('submit', (event) => submitHandler(event, mapita));
//     const form = document.querySelector('#kk');

// const submitHandler = (event, mapita) => {

//     if (!mapita.hasValidMarker()) {
//         event.preventDefault();
//         alert('Debes dibujar una zona válida en el mapa.\nPara que sea válida debe contener al menos 3 puntos');
//     }
//     else {

//         const coordinates = document.querySelector('#coordinates');
//         const coorr = mapita.drawnlayers[0].getLatLngs().flat().map(coordinate => {
//             return { lat: coordinate.lat, lng: coordinate.lng }
//         });
//         coordinates.setAttribute('value', JSON.stringify(coorr));
//     }
// }
</script>
