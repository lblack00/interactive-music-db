<template>
  <div class="frame">
    <div class="div">
      <Navbar />

      <div class="welcome-message">
        Welcome to the Interactive Music Database! Explore what's trending, or use the filters to search for your favorite songs, artists, or playlists!
      </div>

      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          class="search-bar" 
          placeholder="Search..." 
        />
        <div v-if="searchQuery" class="search-results">
          <div class="result-item">Predictions/results here...</div>
          <div class="result-item">Predictions/results here...</div>
          <div class="result-item">Predictions/results here...</div>
        </div>
        <div class="dropdown-container">
          <select v-model="filterOption" class="filter-dropdown">
            <option value="Artists">Artists</option>
            <option value="Songs">Songs</option>
            <option value="Playlists">Playlists</option>
            <option value="Advanced Search">Advanced Search</option>
          </select>
          <select v-model="genreOption" class="filter-dropdown">
            <option value="Genres" disabled>Genres</option>
            <option value="-">-</option>
            <option value="Pop">Pop</option>
            <option value="Rock">Rock</option>
            <option value="Hip-hop">Hip-hop</option>
            <option value="Jazz">Jazz</option>
          </select>
        </div>
      </div>

      <div class="carousel-container">
        <div class="carousel-section">
          <h3 class="carousel-title">Featured Songs</h3>
          <div class="carousel">
            <img v-for="(item, index) in featuredSongs" :key="index" :src="item" />
            <button class="carousel-nav left" @click="prevSlide('featured')">
              &lt;
            </button>
            <button class="carousel-nav right" @click="nextSlide('featured')">
              &gt;
            </button>
          </div>
        </div>

        <div class="carousel-section">
          <h3 class="carousel-title">Popular Artists</h3>
          <div class="carousel">
            <img v-for="(item, index) in popularArtists" :key="index" :src="item" />
            <button class="carousel-nav left" @click="prevSlide('popular')">
              &lt;
            </button>
            <button class="carousel-nav right" @click="nextSlide('popular')">
              &gt;
            </button>
          </div>
        </div>

        <div class="carousel-section">
          <h3 class="carousel-title">Trending Now</h3>
          <div class="carousel">
            <img v-for="(item, index) in trendingNow" :key="index" :src="item" />
            <button class="carousel-nav left" @click="prevSlide('trending')">
              &lt;
            </button>
            <button class="carousel-nav right" @click="nextSlide('trending')">
              &gt;
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';

export default {
  name: 'Home',
  components: {
    Navbar,
  },
  data() {
    return {
      searchQuery: '',
      filterOption: 'Artists',
      genreOption: '-',

      featuredSongs: [
        '/images/UnknownSong.png', 
        '/images/UnknownSong.png', 
        '/images/UnknownSong.png',
        '/images/UnknownSong.png',
        '/images/UnknownSong.png'
      ],
      popularArtists: [
        '/images/UnknownPerson.png', 
        '/images/UnknownPerson.png', 
        '/images/UnknownPerson.png',
        '/images/UnknownPerson.png',
        '/images/UnknownPerson.png'
      ],
      trendingNow: [
        '/images/UnknownSong.png', 
        '/images/UnknownSong.png', 
        '/images/UnknownSong.png',
        '/images/UnknownSong.png',
        '/images/UnknownSong.png'
      ],
      currentIndex: {
        featured: 0,
        popular: 0,
        trending: 0,
      }
    };
  },
  methods: {
    prevSlide(carousel) {
      if (this.currentIndex[carousel] > 0) {
        this.currentIndex[carousel]--;
      } else {
        this.currentIndex[carousel] = this[`${carousel}Songs`].length - 1;
      }
    },
    nextSlide(carousel) {
      if (this.currentIndex[carousel] < this[`${carousel}Songs`].length - 1) {
        this.currentIndex[carousel]++;
      } else {
        this.currentIndex[carousel] = 0;
      }
    }
  },
};
</script>

<style scoped>
.frame {
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  height: auto;
}

.frame .div {
  background-color: #ffffff;
  height: auto;
  position: relative;
  width: 100%;
  max-width: 1900px;
}

.welcome-message {
  font-size: 18px;
  color: #333;
  text-align: center;
  margin: 20px 0;
  font-weight: bold;
  max-width: 90%;
  line-height: 1.5;
}

.search-container {
  margin: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.search-bar {
  padding: 10px;
  font-size: 16px;
  width: 50%;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-results {
  width: 50%;
  background-color: #f0f0f0;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  max-height: 150px;
  overflow-y: auto;
  border: 1px solid #ccc;
}

.result-item {
  padding: 5px;
  font-size: 14px;
  color: #333;
  transition: all 0.3s;
}

.result-item:hover {
  background-color: #ddd;
  text-decoration: underline;
  cursor: pointer;
}

.dropdown-container {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.filter-dropdown {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.carousel-container {
  width: 80%; 
  max-width: 1200px; 
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0 auto; 
}

.carousel-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  margin-bottom: 30px;
  width: 100%;
}

.carousel-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.carousel {
  display: flex;
  overflow-x: auto;
  gap: 20px;
  padding: 10px 0;
  width: 100%;
  position: relative;
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

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: green;
  color: white;
  border: none;
  font-size: 30px;
  padding: 10px;
  cursor: pointer;
  border-radius: 50%;
}

.carousel-nav.left {
  left: 10px;
}

.carousel-nav.right {
  right: 10px;
}

.carousel-nav:hover {
  background-color: darkgreen;
}
</style>
