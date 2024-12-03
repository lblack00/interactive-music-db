<template>
  <nav class="navbar">
    <div class="navbar-title">Interactive Music Database</div>
    <div v-if="loggedIn">
      <ul class="navbar-links">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/artistPage">Feeling Lucky</router-link></li>
        <li @click="logout"><router-link>Log Out</router-link></li>
      </ul>
    </div>
    <div v-else>
      <ul class="navbar-links">
        <li><router-link to="/">Home</router-link></li>
        <li><router-link to="/artistPage">Feeling Lucky</router-link></li>
        <li><router-link to="/signup">Sign Up</router-link></li>
        <li><router-link to="/login">Log In</router-link></li>
      </ul>
    </div>
  </nav>
</template>

<script>
import axios from 'axios';

axios.defaults.withCredentials = true;

export default {
  name: 'Navbar',
  data() {
    return {
      loggedIn: false,
      user: null
    };
  },
  methods: {
    async checkSession() {
      try {
        const response = await axios.get('http://localhost:5001/check-session');
        this.loggedIn = response.data.logged_in;
        this.user = response.data.user || null;
      } catch (error) {
        console.error('Error checking user session:', error);
      }
    },
    async logout() {
      try {
        await axios.post('http://localhost:5001/logout');
        this.loggedIn = false;
        this.user = null;
        this.$forceUpdate();
        alert("Log out successful!");
      } catch (error) {
        console.error('Error logging out:', error);
      }
    },
  },
  mounted() {
    this.checkSession();
  },
  beforeRouteEnter(to, from, next) {
    next(vm => {
      vm.$forceUpdate();
    })
  }
}
</script>

<style scoped>
.navbar {
  background-color: #1abc9c;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.navbar-title {
  font-size: 1.3rem;
  color: #ffffff;
  font-weight: bold;
}

.navbar-links {
  list-style-type: none;
  display: flex;
  gap: 1.5rem;
  margin: 0;
  padding: 0;
}

.navbar-links li {
  display: inline;
}

.navbar-links a {
  color: #ffffff;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.navbar-links a:hover {
  color: #ffffff;
  background-color: #16a085;
}
</style>