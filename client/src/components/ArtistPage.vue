<template>
  <Navbar />
  <!-- This is a comment -->
  <div className="frame">
      <div className="div">
        <!-- This is the artist picture/name -->
        <div className="div-2">
          <div className="artistPicture" />

          <div className="text-wrapper-2">Artist Name</div>
        </div>


        <!-- This is the artist Info -->
        <div className="ArtistInfo">
          <div className="div-wrapper">
            <div className="ArtistInfoText">Aliases: Name 1, Name 2</div>
          </div>

          <div className="div-wrapper">
            <div className="ArtistInfoText">Popularity: XXXXX</div>
          </div>

          <div className="div-wrapper">
            <div className="ArtistInfoText">Score: 8.88</div>
          </div>

          <div className="div-wrapper">
            <div className="ArtistInfoText">Date of Birth: MM/DD/YYYY</div>
          </div>

          <div className="div-wrapper">
            <div className="ArtistInfoText">Birth Country: United Kingdom</div>
          </div>

          <div className="div-wrapper">
            <div className="ArtistInfoText">
              <span className="span">Member of: </span>

              <span className="text-wrapper-3">Group 1</span>

              <span className="span">, </span>

              <span className="text-wrapper-3">Group 2</span>
            </div>
          </div>

          <div className="div-wrapper">
            <div className="ArtistInfoText">ETC: XXXX</div>
          </div>
        </div>


        <!-- This is the artist About -->
        <div className="div-5">
          <div className="about-wrapper">
            <p className="about">
              <span className="text-wrapper-4">&nbsp;&nbsp; </span>

              <span className="SectionTitle">About</span>
            </p>
          </div>

          <div className="div-wrapper-2">
            <p className="p">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
              enim ad minim veniam, quis nostrud exercitation ullamco laboris
              nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
              reprehenderit in voluptate velit esse cillum dolore eu fugiat
              nulla pariatur. Excepteur sint occaecat cupidatat non proident,
              sunt in culpa qui officia deserunt mollit anim id est laborum.
            </p>
          </div>
        </div>

        <!-- This is the artist Discography -->
        <div className="div-5">
          <div className="div-7">
            <div className="discography">&nbsp;&nbsp; Discography</div>

            <div className="div-8">
              <div className="sort-by">&nbsp;&nbsp;Sort By</div>

              <div className="div-9">
                <Size48 className="chevron-down" />
                <div className="text-wrapper-6">Popularity</div>
              </div>
            </div>
          </div>

          <!-- This is the songs Discography -->
          <div className="frame-wrapper">
            <div className="displayElement">
              <div className="ElementInfo">
                <div className="ElementScore">8.88 </div>div>

                <div className="ElementName" />
              </div>

              <div className="ElementPicture" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<script>
import Navbar from './Navbar.vue';

export default {
  name: 'ArtistPage',
  components: {
    Navbar
  },
};
</script>

<style scoped>
.frame {
  background-color: #ffffff;
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
}

.frame .div {
  background-color: #ffffff;
  height: 1080px;
  position: relative;
  width: 1920px;
}

.frame .div-2 {
  background-color: #eaeaea;
  height: 528px;
  left: 46px;
  position: absolute;
  top: 126px;
  width: 470px;
}

.frame .artistPicture {
  background-color: #dd2424;
  height: 440px;
  left: 15px;
  position: absolute;
  top: 16px;
  width: 440px;
}

.frame .text-wrapper-2 {
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

.frame .ArtistInfo {
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

.frame .div-wrapper {
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

.frame .div-5 {
  align-items: flex-start;
  background-color: #e9e9e9;
  display: flex;
  flex-direction: column;
  gap: 8px;
  left: 545px;
  padding: 9px 12px;
  position: relative;
  margin-bottom: 30px;
  top: 125px;
  width: 1200px;
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
  font-family: var(--subtitle-font-family);
  font-size: var(--subtitle-font-size);
  font-style: var(--subtitle-font-style);
  font-weight: var(--subtitle-font-weight);
  letter-spacing: var(--subtitle-letter-spacing);
  line-height: var(--subtitle-line-height);
  text-decoration: underline;
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
}

.frame .p {
  color: #000000;
  font-family: var(--body-base-font-family);
  font-size: var(--body-base-font-size);
  font-style: var(--body-base-font-style);
  font-weight: var(--body-base-font-weight);
  height: 118px;
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

.frame .chevron-down {
  height: 32px !important;
  left: 200px !important;
  position: absolute !important;
  top: 0 !important;
  width: 23px !important;
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
  display: flex;
  flex: 0 0 auto;
  gap: 10px;
  margin-right: -24.00px;
  padding: 10px;
  position: relative;
  width: 1323px;
}

.frame .displayElement {
  height: 245px;
  position: relative;
  width: 215px;
}

.frame .ElementInfo {
  height: 30px;
  left: 0;
  overflow: hidden;
  position: absolute;
  top: 215px;
  width: 215px;
}

.frame .ElementScore {
  background-color: #ffffff;
  border: 1px solid;
  border-color: #000000;
  height: 30px;
  left: 160px;
  position: absolute;
  top: 0;
  width: 55px;
  
}

.frame .ElementName {
  background-color: #ffffff;
  border: 1px solid;
  border-color: #000000;
  height: 30px;
  left: 0;
  position: absolute;
  top: 0;
  width: 160px;
}

.frame .ElementPicture {
  background-color: #e91d1d;
  border: 1px solid;
  border-color: #000000;
  height: 215px;
  left: 0;
  position: absolute;
  top: 0;
  width: 215px;
}
</style>
