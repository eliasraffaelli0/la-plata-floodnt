<template>
  <div class="home marco fondo">
    <img id="logo" alt="Vue logo" src="../assets/LogoLP.png" />
    <HelloWorld msg="Bienvenidos a La Plata Floodn't" />
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: "Home",
  components: {
    HelloWorld,
  },
};
</script>
