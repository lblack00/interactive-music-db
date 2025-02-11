<!-- This file was written by Matthew Stenvold -->
<template>
  <Navbar />

  <v-container v-if="data">
    <v-row>
      <v-col cols="12" md="3">
        <v-card class="pa-4 d-flex flex-column align-center">
          <v-img
            src="/images/UnknownPerson.png"
            width="200"
            height="200"
            contain
          />
          <p class="mt-2">Born: December 13, 1989</p>
          <p>Genre: Pop, Country</p>
          <p>Aliases: {{ data.aliases?.join(', ') || 'None' }}</p>
        </v-card>
      </v-col>

      <v-col cols="12" md="9">
        <h1 class="text-h4 font-weight-bold">{{ data.artist?.[0]?.name }}</h1>
        <RatingSystem 
          itemType="artist"
          :itemId="$route.params.artist_id"
        />

        <p class="mt-4">{{ data.artist?.[0]?.profile || 'No profile available' }}</p>
      </v-col>
    </v-row>

    <div v-if="data.discography && data.discography.length">
      <h2 class="text-h5 mt-6">Discography</h2>

      <v-row class="align-center mb-4">
        <v-col cols="12" md="4">
          <v-select
            v-model="sortBy"
            :items="['Popularity', 'Release Date']"
            label="Sort By"
            outlined
            dense
          />
        </v-col>
      </v-row>

      <v-row>
        <v-col
          v-for="(release, index) in data.discography"
          :key="index"
          cols="4"
          sm="4"
          md="3"
        >
          <v-card class="pa-2" outlined>
            <v-img src="/images/UnknownSong.png" height="120" contain />
            <v-card-title>
              <router-link :key="i" :to="`/master/${release.master_id}`">{{ release.title }}</router-link>
            </v-card-title>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </v-container>
  <div v-else class="loading">Loading...</div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
import RatingSystem from './RatingSystem.vue';

export default {
  name: 'ArtistPage',
  components: {
    Navbar,
    RatingSystem
  },
  data() {
    return {
      data: {
        artist: [],
        discography: [],
        aliases: []
      },
      loading: true
    };
  },
  methods: {
    getArtistImage() {
      console.log('Artist data in getArtistImage:', this.data); // Debug log
      console.log('Artist images:', this.data.artist?.[0]?.images); // Debug log
      const artistImage = this.data.artist?.[0]?.images?.[0]?.uri;
      console.log('Selected image URL:', artistImage); // Debug log
      return artistImage || '/images/UnknownPerson.png';
    },
    
    async getArtist() {
      try {
        console.log('Fetching artist with ID:', this.$route.params.artist_id); // Debug log
        const response = await axios.get('http://localhost:5001/artist', {
          params: { artist_id: this.$route.params.artist_id }
        });
        console.log('Raw API response:', response.data); // Debug log
        this.data = response.data.payload;
        this.loading = false;
        console.log('Processed artist data:', this.data); // Debug log
      } catch (error) {
        console.error('Error fetching artist:', error);
        console.log('Error details:', error.response?.data); // Debug log
        this.loading = false;
      }
    }
  },
  created() {
    this.getArtist();
  }
};
</script>

<style scoped>

.v-card-title {
  font-size: 0.9rem;
  font-weight: bold;
}

</style>
