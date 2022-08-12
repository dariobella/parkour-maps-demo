<template>
  <div class="spotInfo" v-if="spot.id === spotSelected">
    <div class="spotInfo-name">
      <input v-model="spot.name" type="text" class="spotName" :class="editing ? 'text_editing' : 'text_disabled' " :size="spot.name.length" placeholder="Spot name" :disabled="!editing" >
      <div class="controlBtns">
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


      <div class="adder">Added by {{ spot.adder.user.username }}</div>
    </div>

    <div id="picsCarousel" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-indicators">
        <button v-for="(pic, i) in pics" class="carousel-indicator" type="button" :data-bs-slide-to="i" data-bs-target="#picsCarousel" :class="{ active : i === 0 }" :aria-current="i === 0 ? 'true' : ''" :aria-label="'Slide ' + i"></button>
      </div>
      <div class="carousel-inner">
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

    <div class="spotDesc">
      <textarea v-show="editing" v-model="spot.description"
                @keydown="resizeDescTextArea"
                style="overflow: hidden; resize: none"
                ref="descTextArea" class="w-100" placeholder="Spot description">
      </textarea>
      <div v-show="!editing" ref="descText"> {{ spot.description }} </div>
      <a :href="'https://www.google.com/maps/search/?api=1&query=' + spot.lat + ',' + spot.lng" target="_blank">See in Google Maps</a>
    </div>

  </div>
</template>

<script>
import { spotPics } from "@/api";
import {mapState, mapStores} from 'pinia';
import { useUserStore } from "@/stores/UserStore";
import {useMapStore} from "../stores/MapStore";

export default {
  name: 'SpotInfo',

  props: {
    spot: Object,
    spotSelected: Number,
  },

  computed: {
    ...mapState(useUserStore, ['myUser']),
    ...mapStores(useMapStore)
  },

  data () {
    return {
      pics: [],
      editing: false,
      descTextHeight: 0
    }
  },

  mounted() {

    spotPics(this.spot.id)
      .then((response) => {
        this.pics = response.data
      })
      .catch((error) => {
        console.log(error)
      })
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

        //for (let e of spotData.entries()) console.log(e)

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
      this.editing = false
      this.$emit('closeSpotInfo')
    },
  }
}
</script>

<style scoped>

.spotInfo {
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

#closeInfoBtn,  #editSpotBtn {
  color: var(--my-black);
  background-color: #f8f8f8;
  border: none;
  padding: 0 0 0 5px;
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

</style>