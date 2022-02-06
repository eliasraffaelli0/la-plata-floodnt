<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      En este sitio web usted podrá recibir y brindar información relacionada
      <br />
      a inundaciones en la ciudad de La Plata
    </p>
    <h3></h3>
    <dl>
      <dt>Denuncias</dt>
      <dd>
        Apartado que presenta un formulario para el alerta de eventos que puedan
        causar inundaciones
      </dd>
      <dt>Mapa de denuncias</dt>
      <dd>
        Mapa que visualiza los eventos que ya han sido denunciados y confirmados
        por nuestros operadores
      </dd>
      <dt>Zonas inundables</dt>
      <dd>En este mapa se visualizarán las zonas con riesgo de inundación</dd>
      <dt>Recorridos de evacuación y puntos de encuentro</dt>
      <dd>
        En este mapa se visualizarán los recorridos de evacuación y puntos de
        encuentro que se encuentran <br />
        disponibles en caso de una inundación
      </dd>
    </dl>
  </div>
</template>

<script>
export default {
  name: "HelloWorld",
  props: {
    msg: String,
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
