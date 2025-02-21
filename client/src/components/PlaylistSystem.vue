<template>
  <Navbar />
  
  <v-container>
    <h1 class="text-h4 font-weight-bold mb-4">Create a Playlist</h1>
    
    <v-text-field
      v-model="newSong"
      label="Add a song"
      outlined
      dense
      class="mb-2"
    />
    <v-btn color="primary" @click="addSong" :disabled="!newSong">Add</v-btn>
    
    <v-list v-if="playlist.length" class="mt-4">
      <v-list-item v-for="(song, index) in playlist" :key="index" class="d-flex justify-space-between">
        <span>{{ song }}</span>
        <v-btn icon @click="removeSong(index)" style="font-size: 12px; width: 24px; height: 24px;">
          <v-icon color="red">mdi-delete</v-icon>
        </v-btn>
      </v-list-item>
    </v-list>
    
    <p v-else class="mt-4 text-grey">No songs in the playlist yet.</p>
  </v-container>
</template>

<script>
import Navbar from './Navbar.vue';

export default {
  name: 'PlaylistSystem',
  components: {
    Navbar
  },
  data() {
    return {
      newSong: '',
      playlist: []
    };
  },
  methods: {
    addSong() {
      if (this.newSong) {
        this.playlist.push(this.newSong);
        this.newSong = '';
      }
    },
    removeSong(index) {
      this.playlist.splice(index, 1);
    }
  }
};
</script>

<style scoped>
.text-grey {
  color: grey;
}
</style>
