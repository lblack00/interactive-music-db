<!-- This file was written by Jax Hendrickson -->
<template>
  <div class="frame">
    <div class="div">
      <Navbar />

      <div class="welcome-message">
        Welcome to the Interactive Music Database! Explore what's trending, or use the filters to search for your favorite songs, artists, or playlists!
      </div>

      <div class="search-container">
        <form @submit.prevent="performSearch" class="search-form">
          <div class="search-input-container">
            <input 
              type="text" 
              v-model="searchQuery" 
              class="search-bar" 
              placeholder="Search..." 
              @input="getPreviewResults"
            />
            <button type="submit" class="search-button">Search</button>
          </div>
          
          <!-- Preview Results Dropdown -->
          <div v-if="searchQuery && (isSearching || previewResults.length)" class="search-preview">
            <div v-if="isSearching" class="preview-item">
              Searching, wait just a second...
            </div>
            <template v-else>
              <div 
                v-for="(result, index) in previewResults.slice(0, 3)" 
                :key="index" 
                class="preview-item"
                @click="handlePreviewClick(result)"
              >
                <template v-if="filterOption === 'Artists'">
                  {{ result.name }}
                </template>
                <template v-else-if="filterOption === 'Releases'">
                  {{ result.title }} ({{ result.year }}) - {{ result.artists }}
                </template>
                <template v-else-if="filterOption === 'Tracks'">
                  {{ result.title }} - {{ result.release_title }}
                </template>
              </div>
              <div class="preview-footer" @click.prevent="performSearch">
                See all results...
              </div>
            </template>
          </div>
        </form>

        <div class="dropdown-container">
          <select v-model="filterOption" class="filter-dropdown">
            <option value="Artists">Artists</option>
            <option value="Releases">Releases</option>
            <option value="Tracks">Tracks</option>
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
            <router-link 
              v-for="(item, index) in featuredSongs" 
              :key="index" 
              :to="item.link"
              class="carousel-link"
            >
              <img :src="item.image" />
            </router-link>
          </div>
        </div>

        <div class="carousel-section">
          <h3 class="carousel-title">Popular Artists</h3>
          <div class="carousel">
            <router-link 
              v-for="(item, index) in popularArtists" 
              :key="index" 
              :to="item.link"
              class="carousel-link"
            >
              <img :src="item.image" />
            </router-link>
          </div>
        </div>

        <div class="carousel-section">
          <h3 class="carousel-title">Trending Now</h3>
          <div class="carousel">
            <router-link 
              v-for="(item, index) in trendingNow" 
              :key="index" 
              :to="item.link"
              class="carousel-link"
            >
              <img :src="item.image" />
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import axios from 'axios';

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
      previewResults: [],
      searchTimeout: null,
      isSearching: false,

      //i think it would be really intersting if the carousel looked more like a stack of cards on it's side; 
      //so it could look like flipping through vinyls or albums in a store.

      featuredSongs: [
        { image: '/images/UnknownSong.png', link: '/master/763819' },  // Ed Sheeran - A Team
        { image: '/images/UnknownSong.png', link: '/master/483665' },  // Taylor Swift - We Are Never...
        { image: '/images/UnknownSong.png', link: '/master/74524' },   // Linkin Park - Papercut
        { image: '/images/UnknownSong.png', link: '/master/267064' },  // Metallica - Evil Never Dies
        { image: '/images/UnknownSong.png', link: '/master/1293228' }, // Frank Ocean - Chanel
        { image: '/images/UnknownSong.png', link: '/master/763819' },  // Repeat Ed Sheeran
        { image: '/images/UnknownSong.png', link: '/master/483665' }   // Repeat Taylor Swift
      ],
      popularArtists: [
        { image: '/images/UnknownPerson.png', link: '/artist/1124645' },  // Taylor Swift
        { image: '/images/UnknownPerson.png', link: '/artist/18839' },    // Metallica
        { image: '/images/UnknownPerson.png', link: '/artist/40029' },    // Linkin Park
        { image: '/images/UnknownPerson.png', link: '/artist/2184482' },  // Ed Sheeran
        { image: '/images/UnknownPerson.png', link: '/artist/2013868' },  // Frank Ocean
        { image: '/images/UnknownPerson.png', link: '/artist/1124645' },  // Repeat Taylor Swift
        { image: '/images/UnknownPerson.png', link: '/artist/18839' }     // Repeat Metallica
      ],
      trendingNow: [
        { image: '/images/UnknownSong.png', link: '/master/876374' },    // Blank Space
        { image: '/images/UnknownSong.png', link: '/master/308202' },    // Master of Puppets
        { image: '/images/UnknownSong.png', link: '/master/1503117' },   // Blackout
        { image: '/images/UnknownSong.png', link: '/master/1547600' },   // I Don't Care
        { image: '/images/UnknownSong.png', link: '/master/1046042' },   // Blonde
        { image: '/images/UnknownSong.png', link: '/master/876374' },    // Repeat Blank Space
        { image: '/images/UnknownSong.png', link: '/master/308202' }     // Repeat Master of Puppets
      ],
      currentIndex: {
        featured: 0,
        popular: 0,
        trending: 0
      }
    };
  },
  methods: {
    prevSlide(carousel) {
      const items = carousel === 'popular' ? this.popularArtists : 
                    carousel === 'featured' ? this.featuredSongs : 
                    this.trendingNow;
      
      const currentPosition = this.currentIndex[carousel];
      const itemWidth = 270; // Width of item (250px) + gap (20px)
      const containerWidth = document.querySelector('.carousel').offsetWidth;
      const maxScroll = items.length * itemWidth - containerWidth;
      
      let newPosition = currentPosition + itemWidth;
      if (newPosition > maxScroll) {
        newPosition = 0; // Loop to start
      }
      
      this.currentIndex[carousel] = newPosition;
      const carouselElement = document.querySelector(`.carousel-section:nth-child(${carousel === 'featured' ? 1 : carousel === 'popular' ? 2 : 3}) .carousel`);
      carouselElement.scrollTo({
        left: newPosition,
        behavior: 'smooth'
      });
    },

    nextSlide(carousel) {
      const items = carousel === 'popular' ? this.popularArtists : 
                    carousel === 'featured' ? this.featuredSongs : 
                    this.trendingNow;
      
      const currentPosition = this.currentIndex[carousel];
      const itemWidth = 270; // Width of item (250px) + gap (20px)
      const containerWidth = document.querySelector('.carousel').offsetWidth;
      const maxScroll = items.length * itemWidth - containerWidth;
      
      let newPosition = currentPosition - itemWidth;
      if (newPosition < 0) {
        newPosition = maxScroll; // Loop to end
      }
      
      this.currentIndex[carousel] = newPosition;
      const carouselElement = document.querySelector(`.carousel-section:nth-child(${carousel === 'featured' ? 1 : carousel === 'popular' ? 2 : 3}) .carousel`);
      carouselElement.scrollTo({
        left: newPosition,
        behavior: 'smooth'
      });
    },
    async getPreviewResults() {
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout);
      }

      if (!this.searchQuery.trim()) {
        this.previewResults = [];
        this.isSearching = false;
        return;
      }

      this.isSearching = true;

      this.searchTimeout = setTimeout(async () => {
        try {
          const response = await axios.post('http://localhost:5001/search', {
            query: this.searchQuery,
            filterOption: this.filterOption,
            genreOption: this.genreOption
          });

          if (response.status === 200) {
            this.previewResults = response.data.results;
          }
        } catch (error) {
          console.error('Error fetching preview results:', error);
        } finally {
          this.isSearching = false;
        }
      }, 300);
    },

    handlePreviewClick(result) {
      // Navigate to the appropriate page based on result type
      if (this.filterOption === 'Artists') {
        this.$router.push(`/artist/${result.id}`);
      } else if (this.filterOption === 'Releases') {
        this.$router.push(`/master/${result.id}`);
      } else if (this.filterOption === 'Tracks') {
        this.$router.push(`/release/${result.release_id}`);
      }
    },

    performSearch() {
      console.log('Performing search...', this.searchQuery); // Debug log
      if (this.searchQuery.trim()) {
        this.$router.push({
          name: 'SearchResults',  // Matches the name in router
          params: {
            query: this.searchQuery
          },
          query: {
            filterOption: this.filterOption,
            genreOption: this.genreOption
          }
        });
      }
    }
  },
};
</script>

<style scoped>

.frame {
  background: linear-gradient(to bottom, #ffffff, #f0f0f0);
  min-height: 100vh;
  padding: 20px 0;
  position: relative;
  overflow: hidden; 
}

.frame::before,
.frame::after {
  content: '';
  position: fixed;
  top: 0;
  bottom: 0;
  width: 300px; 
  background-image: url('/images/music_texture.jpg'); 
  background-size: cover;
  background-repeat: no-repeat;
  z-index: 1000;
  opacity: 1;
}

.frame::before {
  left: 0;
}

.frame::after {
  right: 0;
}


.carousel-nav {
  display: none;
}


.carousel {
  display: flex;
  overflow-x: auto;
  padding: 20px 0;
  width: 100%;
  position: relative;
  scroll-behavior: smooth;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.carousel-link {
  position: relative;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transition: all 0.3s ease;
  transform: perspective(800px);
  margin-right: -50px; 
  margin-left: 0;
  z-index: 1; 
}

.carousel-link:hover {
  transform: perspective(800px) rotateY(20deg) translateY(-10px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
  z-index: 2; 
}


.carousel img {
  width: 250px;
  height: 250px;
  object-fit: cover;
  border-radius: 12px;
  border: 4px solid white; 
}


.carousel-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  box-shadow: inset -10px 0 10px -10px rgba(0, 0, 0, 0.5);
  pointer-events: none;
  border-radius: 12px;
}


.carousel-section {
  padding: 30px 60px; 
}


.frame .div {
  padding: 0 40px;
}

.welcome-message {
  font-size: 24px;
  color: #1a1a1a;
  text-align: center;
  margin: 40px auto;
  max-width: 800px;
  line-height: 1.6;
  padding: 20px;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.search-container {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  margin: 20px auto 40px;
  max-width: 800px;
}

.search-form {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
  position: relative;
  max-width: 800px;
}

.search-bar {
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  padding: 15px;
  font-size: 18px;
  width: 100%;
  max-width: 600px;
  transition: all 0.3s ease;
  margin-right: 10px;
}

.search-bar:focus {
  border-color: green;
  box-shadow: 0 0 0 3px rgba(0, 128, 0, 0.1);
  outline: none;
}

.search-button {
  background: green;
  color: white;
  padding: 15px 30px;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.search-button:hover {
  background: darkgreen;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 128, 0, 0.2);
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
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 16px;
  background: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-dropdown:hover {
  border-color: green;
}

.filter-dropdown:focus {
  outline: none;
  border-color: green;
  box-shadow: 0 0 0 3px rgba(0, 128, 0, 0.1);
}

.carousel-container {
  width: 80%; 
  margin: 0 auto 30x;
  background: rgba(255, 255, 255, 0.8);
  padding: 10px 20px;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
}

.carousel-section {
  background: white;
  padding: 30px 60px;
  border-radius: 15px;
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 40px;
  transition: transform 0.3s ease;
  position: relative;
  width: 100%;
}

.carousel-section:hover {
  transform: translateY(-5px);
}

.carousel-title {
  font-size: 28px;
  color: #2c3e50;
  margin-bottom: 25px;
  position: relative;
  padding-bottom: 10px;
}

.carousel-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background: green;
  border-radius: 2px;
}

.carousel-items {
  display: flex;
  transition: transform 0.5s ease;
}

.carousel-item {
  flex: 0 0 100%;
  padding: 0 10px;
  cursor: pointer;
}

.carousel-item img {
  width: 250px;
  height: 250px;
  object-fit: cover;
  border-radius: 12px;
  transition: transform 0.5s ease;
}

.carousel-item:hover img {
  transform: scale(1.05);
}

.carousel-item-info {
  text-align: center;
  margin-top: 10px;
  padding: 0 10px;
}

.carousel-item-info .title,
.carousel-item-info .name {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.carousel-item-info .artist {
  color: #666;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: green;
  color: white;
  border: none;
  font-size: 24px;
  padding: 10px;
  cursor: pointer;
  border-radius: 50%;
  z-index: 10;
  transition: background-color 0.3s, transform 0.3s;
}

.carousel-nav.left {
  left: 10px;
}

.carousel-nav.right {
  right: 10px;
}

.carousel-nav:hover {
  background-color: darkgreen;
  transform: scale(1.1) translateY(-50%);
}

.search-input-container {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
}

.search-preview {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 1px solid #ccc;
  border-top: none;
  border-radius: 0 0 4px 4px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  width: 100%;
}

.preview-item {
  padding: 12px 15px;
  cursor: pointer;
  transition: background-color 0.2s;
  color: #333;
  font-size: 14px;
  font-weight: 500;
}

.preview-item:hover {
  background-color: #f0f0f0;
}

.preview-footer {
  padding: 10px 15px;
  text-align: center;
  color: #444;
  font-size: 14px;
  font-weight: 500;
  border-top: 1px solid #eee;
  cursor: pointer;
}

.preview-footer:hover {
  background-color: #f0f0f0;
  color: #222;
}

.search-form {
  position: relative;
  width: 100%;
}

.carousel-items {
  display: flex;
  transition: transform 0.5s ease;
}

.carousel-item {
  flex: 0 0 100%;
  padding: 0 10px;
  cursor: pointer;
}

.carousel-item img {
  width: 250px;
  height: 250px;
  object-fit: cover;
  border-radius: 12px;
  transition: transform 0.5s ease;
}

.carousel-item:hover img {
  transform: scale(1.05);
}

.carousel-item-info {
  text-align: center;
  margin-top: 10px;
  padding: 0 10px;
}

.carousel-item-info .title,
.carousel-item-info .name {
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.carousel-item-info .artist {
  color: #666;
}

.carousel-nav {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: green;
  color: white;
  border: none;
  font-size: 30px;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 50%;
  z-index: 1;
  transition: background-color 0.3s;
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

.carousel-link::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(to top, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0) 50%);
  border-radius: 12px;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.carousel-link:hover::after {
  opacity: 1;
}


.carousel-link::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  box-shadow: inset -10px 0 10px -10px rgba(0, 0, 0, 0.5);
  pointer-events: none;
  border-radius: 12px;
}


.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  background-color: green;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); 
  z-index: 2000;
  padding: 15px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e0e0e0; 
}


.navbar-content {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}


.carousel-container {
  width: 80%; 
  max-width: 1000px;
  margin: 60px auto 0;
  padding: 20px 0;
}

.search-container {
  width: 60%; 
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.welcome-message {
  width: 60%; 
  max-width: 800px;
  margin: 40px auto;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
</style>
