<template>
  <Navbar />
  
  <v-alert v-if="error" type="error" class="ma-4">
    {{ error }}
  </v-alert>

  <v-container>
    <h1 class="text-h4 font-weight-bold mb-4">Upcoming Album Releases</h1>
    
    <div v-if="loading" class="d-flex justify-center align-center" style="height: 400px;">
      <v-progress-circular
        indeterminate
        color="primary"
        size="64"
      ></v-progress-circular>
    </div>

    <div v-else>
      <div v-if="Object.keys(groupedAlbums).length > 0">
        <div v-for="(albums, date) in groupedAlbums" :key="date" class="mb-6">
          <h2 class="text-h5 font-weight-bold mb-3">
            {{ formatDate(date) }}
            <span class="text-subtitle-1 font-weight-regular">
              ({{ calculateCountdown(date) }})
            </span>
          </h2>
          
          <v-row>
            <v-col v-for="album in albums" 
                   :key="album.id" 
                   cols="12" sm="6" md="4">
              <v-card>
                <v-img
                  :src="album.cover_url || 'default-album-cover.jpg'"
                  height="200"
                  cover
                  class="bg-grey-lighten-2"
                />
                
                <v-card-title>{{ album.title }}</v-card-title>
                <v-card-subtitle>{{ album.artist }}</v-card-subtitle>
                
                <v-card-actions>
                  <v-btn
                    prepend-icon="mdi-bell-ring-outline"
                    variant="text"
                    @click="notifyUser(album)"
                  >
                    Notify Me
                  </v-btn>
                  <v-spacer></v-spacer>
                  <v-btn
                    icon="mdi-heart-outline"
                    variant="text"
                    @click="toggleFavorite(album)"
                  ></v-btn>
                </v-card-actions>
              </v-card>
            </v-col>
          </v-row>
        </div>
      </div>
      
      <div v-else class="text-center pa-4">
        <v-icon size="64" class="mb-4">mdi-album</v-icon>
        <div class="text-h6">No upcoming releases found</div>
      </div>
    </div>
  </v-container>
</template>

<script>
import Navbar from './Navbar.vue';
import axios from 'axios';

export default {
  name: 'Countdown',
  components: {
    Navbar
  },
  data() {
    return {
      albums: [],
      loading: true,
      error: null
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
    async fetchReleases() {
      console.log('Starting fetch...');
      try {
        const response = await axios.get('http://localhost:5001/upcoming-releases');
        console.log('Response received:', response.data);
        this.albums = response.data.releases || [];
      } catch (error) {
        console.error('Error fetching releases:', error);
        this.error = 'Failed to load upcoming releases';
      } finally {
        console.log('Setting loading to false');
        this.loading = false;
      }
    },
    calculateCountdown(releaseDate) {
      const now = new Date();
      const release = new Date(releaseDate);
      const diffTime = release - now;
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      
      if (diffDays < 0) return 'Released';
      if (diffDays === 0) return 'Releasing today!';
      if (diffDays === 1) return 'Releasing tomorrow!';
      return `${diffDays} days remaining`;
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString(undefined, {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    notifyUser(album) {
      alert(`You will be notified when "${album.title}" by ${album.artist} is released!`);
    },
    toggleFavorite(album) {
      console.log('Toggle favorite for:', album.title);
    }
  },
  async created() {
    console.log('Component created');
    await this.fetchReleases();
  }
};
</script>

<style scoped>
.v-card {
  transition: transform 0.2s;
}

.v-card:hover {
  transform: translateY(-4px);
}
</style>
