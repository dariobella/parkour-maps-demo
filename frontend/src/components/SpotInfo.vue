<template>
  <div class="spotInfo" v-if="spot.id === spotSelected">
    <div class="spotInfo-name">
      <div class="nameInput">
        <input v-model="spot.name" type="text" class="spotName" :class="editing ? 'text_editing' : 'text_disabled' " :size="spot.name.length" placeholder="Spot name" :disabled="!editing" >
        <button v-if="userStore.isAuthenticated" @click="toggleFavourite" class="favouriteBtn">
          <span class="material-icons">{{ favourite }}</span>
        </button>
        <div class="dropdown" v-if="userStore.isAuthenticated">
          <button @click="dropdownToggle" class="addSpotToMapBtn">
            <span class="material-icons">add_box</span>
          </button>
          <div class="dropdown-content" tabindex="-1" @blur="this.$refs.addSpotToMapDropdown.classList.remove('show')" ref="addSpotToMapDropdown">
            <div @click="addSpotToMap(map)"
                 v-for="map in maps" v-show="map.creator.id === user.id && !(['Added by me', 'Favourites'].includes(map.name))"
            >
              {{ map.name }} <span :class="!map.spots.includes(spot.id) ? 'transparent' : ''" class="material-icons">check</span>
            </div>
          </div>
        </div>
      </div>
      <div class="controlBtns">
        <button v-if="editing" id="deleteSpotBtn" data-bs-toggle="modal" data-bs-target="#deleteSpotModal">
          <span class="material-icons">delete</span>
        </button>
        <button v-if="spot.adder.id === myUser.id" id="editSpotBtn" @click="edit()">
          <span class="material-icons" :class="{ save : editing }"> {{ editing ? 'save' : 'edit' }} </span>
        </button>
        <button id="closeInfoBtn" @click="closeSpotInfo()">
          <span class="material-icons">close</span>
        </button>
      </div>
    </div>



    <div class="spotInfo-top">

      <div class="spotTypeIf">
        <select v-if="editing" name="type" class="spotType" :class="spot.type" v-model="spot.type" >
          <option value="S">Spot</option>
          <option value="G">Gym</option>
          <option value="P">Parkour Park</option>
          <option value="U">Undercover spot</option>
        </select>
        <div v-else>
          <div v-if="spot.type === 'S'" class="spotType" style="background-color: #E65100">
            <p>Spot</p>
          </div>
          <div v-else-if="spot.type === 'U'" class="spotType" style="background-color: #4169E1FF">
            <p>Undercover Spot</p>
          </div>
          <div v-else-if="spot.type === 'P'" class="spotType" style="background-color: #FF8C00FF">
            <p>Parkour Park</p>
          </div>
          <div v-else-if="spot.type === 'G'" class="spotType" style="background-color: #800080FF">
            <p>Gym</p>
          </div>
        </div>
      </div>

      <div class="adder">Added by <ProfileLink :id="spot.adder.user.id" :username="spot.adder.user.username"></ProfileLink> </div>
    </div>

    <div class="spotPicsContainer">
      <div id="picsCarousel" class="carousel slide" data-bs-interval="false">
        <div class="carousel-indicators">
          <button v-for="(pic, i) in pics"
                  class="carousel-indicator" type="button"
                  :data-bs-slide-to="i"
                  data-bs-target="#picsCarousel"
                  :class="{ active : i === 0 }"
                  :aria-current="i === 0 ? 'true' : ''" :aria-label="'Slide ' + i">
          </button>
        </div>
        <div class="carousel-inner" @click="showPics">
          <div v-for="(pic, i) in pics" class="carousel-item" :class="{ active: i === 0 }">
            <img :src="'http://127.0.0.1:8000' + pic.image" class="d-block w-100" alt="">
          </div>
        </div>
        <div class="carouselControls" v-if="pics.length > 1">
          <button class="carousel-control-prev" type="button" data-bs-target="#picsCarousel" data-bs-slide="prev">
            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Previous</span>
          </button>
          <button class="carousel-control-next" type="button" data-bs-target="#picsCarousel" data-bs-slide="next">
            <span class="carousel-control-next-icon" aria-hidden="true"></span>
            <span class="visually-hidden">Next</span>
          </button>
        </div>
      </div>
      <div v-if="editing && pics.length > 0" class="img-overlay">
        <button class="manageSpotPics" @click="editPics">
          Manage Images
        </button>
      </div>
      <button v-else-if="editing" class="addSpotPics" @click="editPics">
        Add Images
      </button>
    </div>


    <div class="spotDesc">
      <textarea v-show="editing" v-model="spot.description"
                @keydown="resizeDescTextArea"
                style="overflow: hidden; resize: none"
                ref="descTextArea" class="w-100" placeholder="Spot description">
      </textarea>
      <div v-show="!editing" ref="descText"> {{ spot.description }} </div>
      <a :href="'https://www.google.com/maps/search/?api=1&query=' + spot.lat + ',' + spot.lng" target="_blank">Open in Google Maps</a>
    </div>

  </div>
</template>

<script>
import {mapState, mapStores} from 'pinia';

import { spotPics } from "@/api";
import { useUserStore } from "@/stores/UserStore";
import { useMapStore } from "@/stores/MapStore";
import { useGlobalStore } from "@/stores/GlobalStore";
import ProfileLink from "./ProfileLink.vue";

export default {
  name: 'SpotInfo',
  components: {ProfileLink},
  props: {
    spot: Object,
    spotSelected: Number,
  },

  computed: {
    favourite () {
      return this.maps[1]?.spots.includes(this.spot.id) ? 'star' : 'star_border'
    },
    ...mapState(useUserStore, ['user','myUser', 'maps']),
    ...mapStores(useUserStore, useMapStore, useGlobalStore),
  },

  data () {
    return {
      pics: [],
      editing: false,
      descTextHeight: 0,
      dropdownClicked: false,
    }
  },

  watch: {
    spotSelected: function(v) {
      if (v === this.spot.id) {
        this.loadPics()
      }
    }
  },

  methods: {
    async edit () {
      if (!this.editing) {
        if (this.spot.description) this.$refs.descTextArea.style.height = this.$refs.descText.scrollHeight + 10 + 'px'
        this.editing = true
      } else {
        const spotData = new FormData()
        spotData.append('name', this.spot.name)
        spotData.append('type', this.spot.type)
        spotData.append('description', this.spot.description)

        await this.mapStore.updateSpot(spotData, this.spot.id)
        this.editing = false
        if (this.$router.currentRoute.value.name === 'Home') this.mapStore.loadSpots()
        else if (this.$router.currentRoute.value.name === 'Map') this.mapStore.loadMap(this.$route.params.id)
      }
    },

    resizeDescTextArea () {
      this.$refs.descTextArea.style.height = '1px'
      this.$refs.descTextArea.style.height = this.$refs.descTextArea.scrollHeight + 'px'
    },

    closeSpotInfo() {
      if (this.editing) {
        if (this.$router.currentRoute.value.name === 'Home') this.mapStore.loadSpots()
        else if (this.$router.currentRoute.value.name === 'Map') this.mapStore.loadMap(this.$route.params.id)
        this.$emit('discardEdit')
      } else {
        this.$emit('closeSpotInfo')
      }
      this.editing = false
    },

    showPics() {
      console.log(this.spot.name)
      console.log(this.pics)
      this.$emit('showSpotPics', this.spot.name, this.pics)
    },

    editPics() {
      this.$emit('editSpotPics', this.spot.id, this.spot.name, this.pics)
    },

    loadPics() {
      spotPics(this.spot.id)
      .then((response) => {
        this.pics = response.data
      })
      .catch((error) => {
        console.log(error)
      })
    },

    toggleFavourite() {
      this.userStore.toggleFavourite(this.spot.id)
    },

    dropdownToggle () {
      this.$refs.addSpotToMapDropdown.classList.toggle('show')
      this.$refs.addSpotToMapDropdown.focus()
    },

    addSpotToMap(map) {
      if (map.spots.includes(this.spot.id)) {
        this.globalStore.setToast({title: `${this.spot.name} is already in this map`}, {type: 'info'})
      } else {
        this.userStore.addSpotToMap(this.spot.id, map.id)
      }
      this.$refs.addSpotToMapDropdown.classList.remove('show')
    },
  }
}
</script>

<style scoped>

.spotInfo {
  z-index: 1;
  width: 30%;
  background-color: #f8f8f8;
  box-shadow: 3px 0 3px 2px rgba(0, 0, 0, 0.1), 0 0 0 2px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
}

.spotInfo-name {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-inline: 10px;
  margin-top: 20px;
}

.spotInfo-name .nameInput {
  display: flex;
  align-items: center;
}

.spotInfo-name .nameInput button {
  display: flex;
  align-items: center;
  background-color: transparent;
  border: none;
  padding: 0 5px 0 0;
}

.favouriteBtn {
  color: var(--bs-yellow);
}

.addSpotToMapBtn {
  color: var(--my-black);
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f1f1f1;
  min-width: 100%;
  box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
  z-index: 3;
  border: 1px solid rgba(0, 0, 0, 0.2);
  border-radius: 5px;
  padding: 5px 0;
}

.dropdown-content div {
  text-align: left;
  display: flex;
  align-items: center;
  justify-content: space-between;
  white-space: nowrap;
  padding: 5px 10px;
}

.dropdown-content span {
  color: var(--my-black);
  padding-left: 10px;
}

.dropdown-content span.transparent {
  color: transparent;
}

.show {
  display: flex;
  flex-direction: column;
  justify-content: left;
}

.dropdown-content div:hover {
  background-color: #ddd;
  cursor: pointer;
}

.spotInfo-name .nameInput button span {
  font-size: 2.2rem;
}

.controlBtns button {
  color: var(--my-black);
  background-color: transparent;
  border: none;
  padding: 0 0 0 5px;
}

#deleteSpotBtn {
  color: #dc3545;
}

#editSpotBtn .save {
  color: #198754;
}

.spotName {
  font-size: 1.2rem;
  font-weight: bold;
}

input.text_disabled {
  background-color: #f8f8f8;
  resize: none;
}

.spotInfo-top {
  align-self: flex-start;
  display: flex;
  align-items: center;
}

.adder:hover {
  cursor: pointer;
}

.spotType {
  margin: 10px;
  padding: 5px;
  padding-inline: 20px;
  background-color: var(--my-black);
  color: white;
  border-radius: 10px;
}

select.spotType {
  background-color: #dcdcdc;
  color: var(--my-black);
}

.spotDesc {
  padding: 10px;
  text-align: left;
  white-space: break-spaces;
}

.spotDesc textarea, .spotDesc div {
  margin-bottom: 20px;
}

.carousel-inner > .carousel-item > img{
  min-height : 300px;
  max-height : 300px;
  width : 100%;
}

.spotPicsContainer {
  position: relative;
  display: flex;
}

#picsCarousel .carousel-inner {
  cursor: pointer;
}

.img-overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}
.img-overlay:before {
    content: '';
    display: block;
    height: 50%;
}
.manageSpotPics {
  border: none;
  padding: 0.375rem 0.75rem;
  font-size: 1.1rem;
  border-radius: 0.25rem;
  display: flex;
  --webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  background-color: var(--my-black);
  margin-left: 50%;
}
.manageSpotPics:hover {
  --webkit-transform: scale(1.2) translate(-40%, -40%);
  transform: scale(1.2) translate(-40%, -40%);
}
.addSpotPics {
  margin-left: 10px;
  border: none;
  padding: 0.375rem 0.75rem;
  font-size: 1.1rem;
  border-radius: 0.25rem;
  background-color: var(--my-black);
}

</style>