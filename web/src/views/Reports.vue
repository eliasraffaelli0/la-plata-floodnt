<template>
  <div class="marco">
    <form @submit.prevent="submitForm">
      <input type="text" hidden v-model="form.latitude" required />
      <input type="text" hidden v-model="form.longitude" required />
      <p>
        <label>Titulo</label> <br />
        <input type="text" name="title" v-model="form.title" required />
      </p>
      <p>
        <label>Categoría</label> <br />
        <select
          id="category"
          class=""
          name="category"
          v-model="form.category"
          required
        >
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
          required
        ></textarea>
      </p>
      <p>
        <label>Teléfono del denunciante</label> <br />
        <input
          type="text"
          name="complainant_telephone"
          v-model="form.complainant_telephone"
          required
        />
      </p>
      <p>
        <label>Email del denunciante</label> <br />
        <input
          type="email"
          name="complainant_email"
          v-model="form.complainant_email"
          required
        />
      </p>
      <p>
        <label>Nombres del denunciante</label> <br />
        <input
          type="text"
          name="complainant_name"
          v-model="form.complainant_name"
          required
        />
      </p>
      <p>
        <label>Apellidos del denunciante</label> <br />
        <input
          type="text"
          name="complainant_last_name"
          v-model="form.complainant_last_name"
          required
        />
      </p>

      <input
        class="btn btn-primary mb-2"
        type="submit"
        value="Crear denuncia"
      />
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

    submitForm() {
      axios
        .post(
          "https://admin-grupo5.proyecto2021.linti.unlp.edu.ar/api/reports/",
          this.form
        )
        .then((res) => {
          if (res.status === 200) {
            this.$router.push({ path: "/" });
          }
          return confirm(`Denuncia creada correctamente`);
        })
        .catch((error) => {
          console.log(error.response.status);
        });
    },
  },
};
</script>
