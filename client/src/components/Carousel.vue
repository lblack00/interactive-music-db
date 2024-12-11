<!-- This file was written by Jax Hendrickson -->
<template>
  <div class="carousel">
    <div v-for="(item, index) in items" :key="index">
      <img :src="item" alt="Song Image"/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Carousel',
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>

<style scoped>
.carousel {
  display: flex;
  overflow-x: auto;
  gap: 20px;
  padding: 10px 0;
}

.carousel img {
  width: 250px;
  height: 250px;
  object-fit: cover;
  border-radius: 8px;
  transition: transform 0.3s;
}

.carousel img:hover {
  transform: scale(1.05);
}
</style>
