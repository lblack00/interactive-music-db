<template>
  <Navbar />
  <div>
    <h1>Welcome to the New Page</h1>
    <p>This is your newly created webpage!</p>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';

export default {
  name: "ArtistPage",
  components: {
    Navbar
  },
};
</script>

<style scoped>
h1 {
  color: blue;
}
</style>