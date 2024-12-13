<!-- This file was written by Matthew Stenvold -->
<template>
  <div class="frame" v-if="data">
    <div class="div">
      <Navbar />
      <!-- New rating header section -->
      <div class="rating-header">
        <h1 class="artist-title">{{ data.artist?.[0]?.name }}</h1>
        <RatingSystem 
          itemType="artist"
          :itemId="$route.params.artist_id"
        />
      </div>

      <!-- Artist block (remove rating from here) -->
      <div class="ArtistBlock">
        <div class="artistPicture" :style="{ backgroundImage: `url(${getArtistImage()})` }"></div>
        <div class="ArtistName">{{ data.artist?.[0]?.name }}</div>
      </div>

      <!-- Artist Info -->
      <div class="ArtistInfoBlock">
        <div class="ArtistInfo">
          <div class="ArtistInfoText">Aliases: {{ data.aliases?.join(', ') || 'None' }}</div>
        </div>

        <div class="ArtistInfo">
          <div class="ArtistInfoText">Popularity: {{ ArtistPop }}</div>
        </div>

        <div class="ArtistInfo">
          <div class="ArtistInfoText">Score: {{ ArtistScore.toFixed(2) }}</div>
        </div>

        <div class="ArtistInfo">
          <div class="ArtistInfoText">Date of Birth: {{ ArtistBD }}</div>
        </div>

        <div class="ArtistInfo">
          <div class="ArtistInfoText">Birth Country: {{ ArtistBC }}</div>
        </div>

        <div class="ArtistInfo">
          <div class="ArtistInfoText">
            Member of: 
            <a href="/band1">Band 1</a>,
            <a href="/band2">Band 2</a>
          </div>
        </div>

        <div class="ArtistInfo">
          <div class="ArtistInfoText">ETC: XXXX</div>
        </div>
      </div>

      <div class="right-column">
        <!-- About section -->
        <div class="OtherInfoBlcok">
          <div class="SectionTitle">About</div>
          <div class="div-wrapper-2">
            <p class="p">{{ data.artist?.[0]?.profile || 'No profile available' }}</p>
          </div>
        </div>

        <!-- Discography section -->
        <div class="OtherInfoBlcok" v-if="data.discography">
          <div class="SectionTitle">
            Discography
            <div class="div-8">
              <div class="sort-by">Sort By</div>
              <div class="div-9">
                <div class="text-wrapper-6">Popularity</div>
              </div>
            </div>
          </div>

          <!-- Songs Discography -->
          <template v-if="data.discography && data.discography.length">
            <div class="frame-wrapper" v-for="chunk in discographyChunks" :key="chunk.start">
              <div v-for="n in 5" :key="n">
                <SongDisplayElement 
                  v-if="data.discography[chunk.start + n - 1]"
                  :elementName="data.discography[chunk.start + n - 1].title" 
                  :elementID="data.discography[chunk.start + n - 1].master_id" 
                />
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="loading">Loading...</div>
</template>

<script>
import axios from 'axios';
import Navbar from './Navbar.vue';
import RatingSystem from './RatingSystem.vue';
import SongDisplayElement from './DisplayElement.vue';

export default {
  name: 'ArtistPage',
  components: {
    Navbar,
    RatingSystem,
    SongDisplayElement
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
  props: {
    ArtistName: String,
    ArtistPop: {
      type: Number,
      default: 0
    },
    ArtistScore: {
      type: Number,
      default: 5.00
    },
    ArtistBD: {
      type: String,
      default: 'MM/DD/YYYY'
    },
    ArtistBC: {
      type: String,
      default: 'Unknown'
    }
  },
  computed: {
    discographyChunks() {
      return [
        { start: 0 },
        { start: 5 },
        { start: 10 }
      ];
    }
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
.frame {
  background-color: #ffffff;
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
  height: auto;
}

.frame .left-column {
  width: 40%;
  display: flex;
  flex-direction: column;
  gap: 20px; /* Space between the blocks */
}

.frame .right-column {
  width: 55%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}


.frame .div {
  background-color: #ffffff;
  height: auto;
  position: relative;
  width: 1900px;
}

.frame .ArtistBlock {
  background-color: #eaeaea;
  height: 528px;
  left: 46px;
  position: absolute;
  top: 246px;
  width: 470px;
}

.frame .artistPicture {
  background-color: #dd2424;
  height: 440px;
  left: 15px;
  position: absolute;
  top: 16px;
  width: 440px;
  background-size: cover;
  background-position: center;
}

.frame .ArtistName {
  color: #030303;
  font-family: var(--subtitle-font-family);
  font-size: var(--subtitle-font-size);
  font-style: var(--subtitle-font-style);
  font-weight: var(--subtitle-font-weight);
  left: 0;
  letter-spacing: var(--subtitle-letter-spacing);
  line-height: var(--subtitle-line-height);
  position: absolute;
  text-align: center;
  top: 471px;
  width: 470px;
}

.frame .ArtistInfoBlock {
  align-items: flex-start;
  background-color: #eaeaea;
  display: flex;
  flex-direction: column;
  gap: 11px;
  left: 45px;
  padding: 6px 8px;
  position: absolute;
  top: 684px;
  width: 471px;
}

.frame .ArtistInfo {
  align-items: center;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  gap: 10px;
  justify-content: center;
  padding: 7px 8px;
  position: relative;
  width: 100%;
}

.frame .ArtistInfoText{
  color: #000000;
  font-family: var(--single-line-body-base-font-family);
  font-size: var(--single-line-body-base-font-size);
  font-style: var(--single-line-body-base-font-style);
  font-weight: var(--single-line-body-base-font-weight);
  letter-spacing: var(--single-line-body-base-letter-spacing);
  line-height: var(--single-line-body-base-line-height);
  margin-top: -1.00px;
  position: relative;
  width: 432px;
}

.frame .span {
  color: #000000;
  font-family: var(--single-line-body-base-font-family);
  font-size: var(--single-line-body-base-font-size);
  font-style: var(--single-line-body-base-font-style);
  font-weight: var(--single-line-body-base-font-weight);
  letter-spacing: var(--single-line-body-base-letter-spacing);
  line-height: var(--single-line-body-base-line-height);
}

.frame .text-wrapper-3 {
  font-family: var(--single-line-body-base-font-family);
  font-size: var(--single-line-body-base-font-size);
  font-style: var(--single-line-body-base-font-style);
  font-weight: var(--single-line-body-base-font-weight);
  letter-spacing: var(--single-line-body-base-letter-spacing);
  line-height: var(--single-line-body-base-line-height);
  text-decoration: underline;
}

.frame .OtherInfoBlcok {
  align-items: flex-start;
  background-color: #e9e9e9;
  display: flex;
  flex-direction: column;
  gap: 8px;
  left: 545px;
  padding: 9px 12px;
  position: relative;
  margin-bottom: 30px;
  margin-right: 1000px;
  top: 125px;
  width: 1300px;
  height: auto;
}

.frame .about-wrapper {
  align-self: stretch;
  height: 40px;
  position: relative;
  width: 100%;
}

.frame .about {
  color: #000000;
  font-family: var(--subtitle-font-family);
  font-size: var(--subtitle-font-size);
  font-style: var(--subtitle-font-style);
  font-weight: var(--subtitle-font-weight);
  left: 20;
  letter-spacing: var(--subtitle-letter-spacing);
  line-height: var(--subtitle-line-height);
  position: absolute;
  top: -2px;
  width: 1299px;
}

.frame .text-wrapper-4 {
  color: #000000;
  font-family: var(--subtitle-font-family);
  font-size: var(--subtitle-font-size);
  font-style: var(--subtitle-font-style);
  font-weight: var(--subtitle-font-weight);
  letter-spacing: var(--subtitle-letter-spacing);
  line-height: var(--subtitle-line-height);
}

.frame .SectionTitle {
  color: #000000;
  font-family: var(--subtitle-font-family);
  font-size: var(--subtitle-font-size);
  font-style: var(--subtitle-font-style);
  font-weight: var(--subtitle-font-weight);
  letter-spacing: var(--subtitle-letter-spacing);
  line-height: var(--subtitle-line-height);
  text-decoration: underline;
  margin-left: 20px;
  width:95%;
  display: grid;
  grid-template-columns: auto 1fr;
}

.frame .div-wrapper-2 {
  align-items: center;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  gap: 10px;
  justify-content: center;
  padding: 2px 5px;
  position: relative;
  width: 100%;
  height: auto;
}

.frame .p {
  color: #000000;
  font-family: var(--body-base-font-family);
  font-size: var(--body-base-font-size);
  font-style: var(--body-base-font-style);
  font-weight: var(--body-base-font-weight);
  height: auto;
  letter-spacing: var(--body-base-letter-spacing);
  line-height: var(--body-base-line-height);
  margin-left: -0.50px;
  margin-right: -0.50px;
  margin-top: -1.00px;
  position: relative;
  width: 1290px;
}

.frame .div-7 {
  align-items: flex-start;
  align-self: stretch;
  display: flex;
  flex: 0 0 auto;
  gap: 7px;
  position: relative;
  width: 100%;
}

.frame .discography {
  color: #000000;
  font-family: var(--subtitle-font-family);
  font-size: var(--subtitle-font-size);
  font-style: var(--subtitle-font-style);
  font-weight: var(--subtitle-font-weight);
  height: 63px;
  letter-spacing: var(--subtitle-letter-spacing);
  line-height: var(--subtitle-line-height);
  margin-top: -1.00px;
  position: relative;
  width: 1037px;
}

.frame .div-8 {
  margin-left: auto;
  align-items: flex-start;
  display: flex;
  flex-direction: column;
  gap: 5px;
  position: relative;
  width: 229px;
}

.frame .sort-by {
  align-self: stretch;
  color: #000000;
  font-family: var(--m3-headline-small-font-family);
  font-size: var(--m3-headline-small-font-size);
  font-style: var(--m3-headline-small-font-style);
  font-weight: var(--m3-headline-small-font-weight);
  height: 26px;
  letter-spacing: var(--m3-headline-small-letter-spacing);
  line-height: var(--m3-headline-small-line-height);
  margin-top: -1.00px;
  position: relative;
  white-space: nowrap;
}

.frame .div-9 {
  align-self: stretch;
  background-color: #f0f0f0;
  border-radius: 5px;
  height: 32px;
  overflow: hidden;
  position: relative;
  width: 100%;
}

.frame .text-wrapper-6 {
  color: #7d7d7d;
  font-family: var(--m3-label-medium-prominent-font-family);
  font-size: var(--m3-label-medium-prominent-font-size);
  font-style: var(--m3-label-medium-prominent-font-style);
  font-weight: var(--m3-label-medium-prominent-font-weight);
  height: 14px;
  left: 22px;
  letter-spacing: var(--m3-label-medium-prominent-letter-spacing);
  line-height: var(--m3-label-medium-prominent-line-height);
  position: absolute;
  top: 8px;
  white-space: nowrap;
  width: 106px;
}

.frame .frame-wrapper {
  align-items: flex-start;
  align-self: center;
  display: flex;
  flex: 0 0 auto;
  gap: 10px;
  margin-right: -24.00px;
  padding: 10px;
  position: relative;
  width: 1200px;
}

.rating-header {
  position: relative;
  width: 100%;
  padding: 20px 0;
  background: linear-gradient(to bottom, #f8f8f8, #ffffff);
  border-bottom: 1px solid #eaeaea;
  margin-top: 60px;
  text-align: center;
}

.artist-title {
  font-size: 2.5rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 15px;
}

</style>
