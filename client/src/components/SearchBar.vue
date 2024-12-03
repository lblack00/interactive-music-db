<template>
  <div class="search-bar-container">
    <!-- Search Bar -->
    <input 
      class="search-bar" 
      type="text" 
      v-model="searchQuery" 
      placeholder="Search music/artists" 
    />

    <!-- Filters Section -->
    <div class="filters">
      <div class="filter-item">
        <img src="@/assets/song-icon.png" alt="Songs">
        Songs
      </div>
      <div class="filter-item">
        <img src="@/assets/artist-icon.png" alt="Artists">
        Artists
      </div>
      <div class="filter-item">
        <img src="@/assets/playlist-icon.png" alt="Playlists">
        Playlists
      </div>
      <div class="filter-item">
        <img src="@/assets/keyword-icon.png" alt="Keywords">
        Keywords
      </div>
      <div class="filter-item" @click="toggleDropdown">
        <img src="@/assets/search-icon.png" alt="Advanced Search">
        Advanced Search
        <i class="fas fa-chevron-down" style="margin-left: 5px;"></i>
        <div v-if="dropdownOpen" class="dropdown-menu">
          <div class="dropdown-item">Option 1</div>
          <div class="dropdown-item">Option 2</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      dropdownOpen: false,
    };
  },
  methods: {
    toggleDropdown() {
      this.dropdownOpen = !this.dropdownOpen;
    },
  },
};
</script>

<style scoped>
.search-bar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.search-bar {
  width: 80%;
  padding: 10px;
  font-size: 18px;
  border-radius: 5px;
}

.filters {
  display: flex;
  gap: 20px;
  align-items: center;
}

.filter-item {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.filter-item img {
  width: 20px;
  margin-right: 8px;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  background-color: white;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  width: 200px;
}

.dropdown-item {
  padding: 10px;
  cursor: pointer;
}

.dropdown-item:hover {
  background-color: #f1f1f1;
}
</style>
