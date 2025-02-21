<template>
  <Navbar />
  
  <v-container v-if="Object.keys(groupedAlbums).length">
    <h1 class="text-h4 font-weight-bold mb-4">Upcoming Album Releases</h1>
    
    <div v-for="(albums, date) in groupedAlbums" :key="date" class="mb-4">
      <h2 class="text-h5 font-weight-bold">{{ formatDate(date) }}</h2>
      <ul>
        <li v-for="(album, index) in albums" :key="index" class="d-flex align-center">
          <strong>{{ album.title }}</strong> by {{ album.artist }} ({{ album.countdown }})
          <v-btn icon class="ml-2" @click="notifyUser(album)" style="font-size: 12px; width: 24px; height: 24px;">
            <v-icon small>mdi-bell-ring-outline</v-icon>
          </v-btn>
        </li>
      </ul>
    </div>
  </v-container>
  
  <div v-else class="loading">Loading...</div>
</template>

<script>
import Navbar from './Navbar.vue';

export default {
  name: 'Countdown',
  components: {
    Navbar
  },
  data() {
    return {
      albums: [
        { title: 'Album One', artist: 'Artist A', release_date: '2025-03-01' },
        { title: 'Album Two', artist: 'Artist B', release_date: '2025-04-15' },
        { title: 'Album Three', artist: 'Artist C', release_date: '2025-04-15' },
        { title: 'Album Four', artist: 'Artist D', release_date: '2025-05-20' }
      ].map(album => ({
        ...album,
        countdown: this.calculateCountdown(album.release_date)
      }))
    };
  },
  computed: {
    groupedAlbums() {
      return this.albums.reduce((acc, album) => {
        (acc[album.release_date] = acc[album.release_date] || []).push(album);
        return acc;
      }, {});
    }
  },
  methods: {
    calculateCountdown(releaseDate) {
      const releaseTime = new Date(releaseDate) - new Date();
      if (releaseTime <= 0) return 'Released!';
      const days = Math.floor(releaseTime / (1000 * 60 * 60 * 24));
      return `${days} days remaining`;
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString();
    },
    notifyUser(album) {
      alert(`You will be notified about the release of ${album.title} by ${album.artist}!`);
    }
  }
};
</script>

<style scoped>
.loading {
  text-align: center;
  font-size: 1.2rem;
  margin-top: 20px;
}
</style>
