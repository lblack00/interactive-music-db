<template>
  <div class="displayElementFrame">
    <div class="ElementPicture" :style="{ backgroundImage: 'url(' + (elementPicture || defaultPicture) + ')' }"></div>
    <div class="ElementScore">{{ formattedScore }}</div>

    <div class="ElementName"><a :href="'/' + elementType + '/' + elementName">{{ elementName }}</a></div>

    
  </div>
</template>

<script>


export default {
  name: 'SongDisplayElement',
  // When passing in values, surrond them with parentheses (ie. :elementName="'Holder'" :elementScore="7.56")
  props: {
    // Declare the variables that will be passed from parent component
    elementType: {
      type: String,
      default: 'song', // default to 'song' if not specified
      validator(value) {
        // Only allow 'artist' or 'song'
        return ['artist', 'song'].includes(value);
      }
    },
    elementPicture: {
      type: String,
      default: ''
    },
    elementScore: {
      type: Number,
      default: 8.88
    },
    elementName: {
      type: String,
      default: 'Element Name'
    }
  },

  computed: {
    // Compute the default image based on the elementType
    defaultPicture() {
      return this.elementType === 'artist'
        ? '/images/UnknownPerson.png'  // Default image for artist
        : '/images/UnknownSong.png';  // Default image for song
    },
    formattedScore() {
      // Format the number to two decimal places
      return this.elementScore.toFixed(2);
    }
  }
};
</script>

<style scoped>
.displayElementFrame {
  height: 245px;
  position: relative;
  width: 215px;
  margin: 0px 5px 0px 5px;
}

.ElementInfo {
  height: 30px;
  left: 0;
  overflow: hidden;
  position: absolute;
  top: 215px;
  width: 215px;
}

.ElementScore {
  background-color: #ffffff;
  border: 1px solid;
  border-color: #000000;
  height: 30px;
  left: 160px;
  position: absolute;
  top: 185px;
  width: 55px;
  color: #000000;
  font-family: var(--single-line-body-base-font-family);
  font-size: 20px;
  font-style: var(--single-line-body-base-font-style);
  font-weight: bold;
  letter-spacing: var(--single-line-body-base-letter-spacing);
  text-align: center;
}

.ElementName {
  background-color: #ffffff;
  border: 1px solid;
  border-color: #000000;
  height: 30px;
  left: 0;
  position: absolute;
  top: 215px;
  width: 215px;
  color: #000000;
  font-family: var(--single-line-body-base-font-family);
  font-size: 20px;
  font-style: var(--single-line-body-base-font-style);
  letter-spacing: var(--single-line-body-base-letter-spacing);
  text-align: center;
}

.ElementPicture {
  background-color: #e91d1d;
  border: 1px solid;
  border-color: #000000;
  height: 215px;
  left: 0;
  position: absolute;
  top: 0;
  width: 215px;
  background-size: cover;
  background-position: center;
}


</style>