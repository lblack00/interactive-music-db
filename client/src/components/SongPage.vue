<template>
  <div class="frame" v-if="data">
    <div class="div">
      <Navbar />
      <!-- Song picture/name -->
      <div class="SongBlock">
        <div class="SongPicture" :style="{ backgroundImage: 'url(' + (SongPicture) + ')' }"></div>
        <div class="SongName">{{ data.master?.[0]?.title || 'Unknown Song' }}</div>
        <RatingSystem 
          itemType="master"
          :itemId="$route.params.master_id"
        />
      </div>

      <!-- Song Info -->
      <div class="SongInfoBlock">
        <div class="SongInfo">
          <div class="SongInfoText">
            Artists: 
            <router-link 
              v-if="data.artist?.[0]" 
              :to="`/artist/${data.artist[0].artist_id}`"
            >
              {{ data.artist[0].artist_name }}
            </router-link>
          </div>
        </div>

        <div class="SongInfo">
          <div class="SongInfoText">Popularity: {{ SongPop }}</div>
        </div>

        <div class="SongInfo">
          <div class="SongInfoText">Score: {{ SongScore.toFixed(2) }}</div>
        </div>

        <div class="SongInfo">
          <div class="SongInfoText">Release Date: {{ data.master?.[0]?.year || 'Unknown' }}</div>
        </div>

        <div class="SongInfo">
          <div class="SongInfoText">
            Genre(s): {{ data.genre?.map(g => g.genre).join(', ') || 'Unknown' }}
          </div>
        </div>

        <div class="SongInfo">
          <div class="SongInfoText">Length: {{ SongLength }}</div>
        </div>

        <div class="SongInfo">
          <div class="SongInfoText">Language: {{ Language }}</div>
        </div>
      </div>

      <!-- About section -->
      <div class="OtherInfoBlcok">
        <div class="SectionTitle">About</div>
        <div class="div-wrapper-2">
          <p class="p">{{ data.master?.[0]?.notes || 'No description available.' }}</p>
        </div>
      </div>

      <!-- Lyrics section -->
      <div class="OtherInfoBlcok">
        <div class="SectionTitle">Lyrics</div>
        <div class="div-wrapper-2">
          <p class="p">{{ data.lyrics || 'No lyrics available.' }}</p>
        </div>
      </div>

      <!-- Related Songs -->
      <div class="OtherInfoBlcok" v-if="data.related">
        <div class="SectionTitle">
          Related Songs
          <div class="div-8">
            <div class="sort-by">Sort By</div>
            <div class="div-9">
              <div class="text-wrapper-6">Popularity</div>
            </div>
          </div>
        </div>

        <!-- Songs Display -->
        <div class="frame-wrapper">
          <template v-if="data.related && data.related.length">
            <SongDisplayElement 
              v-for="(song, index) in data.related.slice(0, 5)" 
              :key="index"
              :elementType="'master'"
              :elementScore="song.score || 0"
              :elementName="song.title"
              :elementID="song.master_id"
            />
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
import SongDisplayElement from './DisplayElement.vue';
import RatingSystem from './RatingSystem.vue';

export default {
  name: 'SongPage',
  components: {
    Navbar,
    SongDisplayElement,
    RatingSystem
  },
  data() {
    return {
      data: {
        master: [],
        artist: [],
        genre: [],
        related: [],
        lyrics: null
      },
      loading: true
    };
  },
  props: {
    SongName: String,
    SongPicture: {
      type: String,
      default: '/images/UnknownSong.png'
    },
    SongPop: {
      type: Number,
      default: 0
    },
    SongScore: {
      type: Number,
      default: 5.00
    },
    SongLength: {
      type: String,
      default: 'Unknown'
    },
    Language: {
      type: String,
      default: 'Unknown'
    }
  },
  methods: {
    async getSong() {
      try {
        const response = await axios.get('http://localhost:5001/master', {
          params: { master_id: this.$route.params.master_id }
        });
        this.data = response.data.payload;
        this.loading = false;
      } catch (error) {
        console.error('Error fetching song:', error);
        this.loading = false;
      }
    }
  },
  created() {
    this.getSong();
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

.frame .div {
  background-color: #ffffff;
  height: auto;
  position: relative;
  width: 1900px;
}

.frame .SongBlock {
  background-color: #eaeaea;
  height: 528px;
  left: 46px;
  position: absolute;
  top: 126px;
  width: 470px;
}

.frame .SongPicture {
  background-color: #dd2424;
  height: 440px;
  left: 15px;
  position: absolute;
  top: 16px;
  width: 440px;
  background-size: cover;
  background-position: center;
}

.frame .SongName {
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

.frame .SongInfoBlock {
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

.frame .SongInfo {
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

.frame .SongInfoText{
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


</style>
