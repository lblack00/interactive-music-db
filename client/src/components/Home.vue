<template>
  <Navbar />
  <div class="container mt-5">
    <h2>Welcome to the Homepage!</h2>
    <p>We are glad to have you here. Start exploring our website!</p>
    <!-- Add more content here as needed -->
  </div>
</template>

<script>
import Navbar from './Navbar.vue';

export default {
  name: 'Homepage',
  components: {
    Navbar
  },
};
</script>

<style scoped>
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #ecf0f1;
  color: #333;
  line-height: 1.6;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.container {
  background-color: #ffffff;
  padding: 40px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  width: 100%;
  box-sizing: border-box;
  text-align: center;
}

h2 {
  font-size: 2rem;
  color: #1abc9c;
  margin-bottom: 20px;
}

p {
  font-size: 1.2rem;
  color: #34495e;
  margin-bottom: 20px;
}

@media (max-width: 768px) {
  .container {
    padding: 20px;
  }

  h2 {
    font-size: 1.5rem;
  }

  p {
    font-size: 1rem;
  }
}

.mt-3 {
  margin-top: 20px;
}
</style>
