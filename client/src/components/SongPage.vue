<template>
  <!-- This is a comment -->
  <div class="frame">
      <div class="div">
        <Navbar />
        <!-- This is the Song picture/name -->
        <div class="SongBlock">
          <div class="SongPicture" />

          <div class="SongName">Song Name</div>
        </div>


        <!-- This is the Song Info -->
        <div class="SongInfoBlock">
          <div class="SongInfo">
            <div class="SongInfoText">Song(s): Person 1, Person 2</div>
          </div>

          <div class="SongInfo">
            <div class="SongInfoText">Popularity: XXXXX</div>
          </div>

          <div class="SongInfo">
            <div class="SongInfoText">Score: 8.88</div>
          </div>

          <div class="SongInfo">
            <div class="SongInfoText">Release Date: MM/DD/YYYY</div>
          </div>

          <div class="SongInfo">
            <div class="SongInfoText">Genre</div>
          </div>

          <div class="SongInfo">
            <div class="SongInfoText">Length: XXXX</div>
          </div>

          <div class="SongInfo">
            <div class="SongInfoText">Language: XXXX</div>
          </div>


          <div class="SongInfo">
            <div class="SongInfoText">ETC: XXXX</div>
          </div>
        </div>


        <!-- This is the Song About -->
        <div class="OtherInfoBlcok">
          <div class="about-wrapper">
            <p class="about">
              <span class="text-wrapper-4">&nbsp;&nbsp; </span>

              <span class="SectionTitle">About</span>
            </p>
          </div>

          <div class="div-wrapper-2">
            <p class="p">
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
              enim ad minim veniam, quis nostrud exercitation ullamco laboris
              nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
              reprehenderit in voluptate velit esse cillum dolore eu fugiat
              nulla pariatur. Excepteur sint occaecat cupidatat non proident,
              sunt in culpa qui officia deserunt mollit anim id est laborum.
              Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
              eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut
              enim ad minim veniam, quis nostrud exercitation ullamco laboris
              nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
              reprehenderit in voluptate velit esse cillum dolore eu fugiat
              nulla pariatur. Excepteur sint occaecat cupidatat non proident,
              sunt in culpa qui officia deserunt mollit anim id est laborum.
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

        <!-- This is the Song Discography -->
        <div class="OtherInfoBlcok">
          <div class="div-7">
            <div class="discography">&nbsp;&nbsp; 
              <span class="SectionTitle">Discography</span>
            </div>

            <div class="div-8">
              <div class="sort-by">&nbsp;&nbsp;Sort By</div>

              <div class="div-9">
                <div class="text-wrapper-6">Popularity</div>
              </div>
            </div>
          </div>

        <!-- This is the related songs -->
        <div class="frame-wrapper">
          <SongDisplayElement :elementType="'Song'" :elementScore="7.50" :elementName="'Holder'" />
          <SongDisplayElement />
          <SongDisplayElement />
          <SongDisplayElement />
          <SongDisplayElement />
        </div>
        <div class="frame-wrapper">
          <SongDisplayElement :elementType="'Song'" :elementScore="7.50" :elementName="'Holder'" />
          <SongDisplayElement />
          <SongDisplayElement />
          <SongDisplayElement />
          <SongDisplayElement />
        </div>
        <div class="frame-wrapper">
          <SongDisplayElement :elementType="'Song'" :elementScore="7.50" :elementName="'Holder'" />
          <SongDisplayElement />
          <SongDisplayElement />
          <SongDisplayElement />
          <SongDisplayElement />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import SongDisplayElement from './DisplayElement.vue';

export default {
  name: 'SongPage',
  components: {
    Navbar,
    SongDisplayElement
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
  color:#000000;
  font-family: var(--subtitle-font-family);
  font-size: var(--subtitle-font-size);
  font-style: var(--subtitle-font-style);
  font-weight: var(--subtitle-font-weight);
  letter-spacing: var(--subtitle-letter-spacing);
  line-height: var(--subtitle-line-height);
  text-decoration: underline;
  position: relative;
  align-self:stretch;
  height:40px;
  width:max-content;
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
