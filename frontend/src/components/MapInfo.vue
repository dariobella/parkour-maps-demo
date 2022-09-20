<template>
<div class="mapInfo show" v-if="show">
  <div class="mapInfoTop">
    <input type="text" class="mapName" placeholder="Map name"
           :size="map.name ? map.name.length : 15"
           v-model="map.name"
           :class="editing ? 'text_editing' : 'text_disabled'"
           :disabled="!editing">
    <div class="controlBtns">
      <button v-if="map.creator.id === user.id" id="editMapBtn" @click="editMap()">
        <span class="material-icons" :class="{ save : editing }"> {{ editing ? 'save' : 'edit' }} </span>
      </button>
      <button id="hideInfoBtn" @click="hideMapInfo()">
        <span class="material-icons">{{ editing ? 'close' : 'arrow_left' }}</span>
      </button>
    </div>
  </div>
  <div>
    <div class="mapCreator">
      <span>created by <router-link :to="`/profile/${map.creator.id}`"> {{map.creator.username}} </router-link> </span>
    </div>
    <div class="mapDescription">
      <textarea v-show="editing" v-model="map.description"
          @keydown="resizeTextArea"
          style="overflow: hidden; resize: none"
          ref="mapDescTextArea" placeholder="Map description">
      </textarea>
      <div v-show="!editing" ref="mapDescText"> {{ map.description }} </div>
    </div>
  </div>
  <div class="spotList">
    <div class="spotItem" v-for="spot in spots" @click.prevent="selectSpot(spot.id, spot.lat, spot.lng)">
      <div>
        <img :src="spotIcon(spot.type)">
        <span>{{spot.name}}</span>
      </div>
      <div>
        <button id="deleteSpotFromMapBtn" @click.prevent="e => deleteSpotFromMap(e, spot.id)">
          <span class="material-icons">close</span>
        </button>
      </div>
    </div>
  </div>
</div>
<div class="mapInfo hide" v-else>
  <button id="showMapInfoBtn" @click="showMapInfo">
    <span class="material-icons">arrow_right</span>
  </button>
</div>
</template>

<script>


import {mapState, mapStores} from "pinia";
import { useMapStore } from "@/stores/MapStore";
import {useUserStore} from "@/stores/UserStore";

export default {
  name: "MapInfo",

  props: {
    map: Object
  },

  computed: {
    ...mapStores(useMapStore, useUserStore),
    ...mapState(useMapStore, ['spots']),
    ...mapState(useUserStore, ['user', 'myUser']),
  },

  data () {
    return {
      show: true,
      editing: false,
    }
  },

  methods: {
    spotIcon(type) {
      if (type === 'U') return "https://i.ibb.co/LZQWkQB/bluePin.png"
      else if (type === 'P') return "https://i.ibb.co/VBtTnMG/orange-Pin.png"
      else if (type === 'G') return "https://i.ibb.co/cXdG8Dv/purple-Pin.png"
      else return "https://i.ibb.co/CWLrJK6/redPin.png"
    },

    showMapInfo() {
      this.show = true
    },

    hideMapInfo() {
      if (this.editing) {
        this.editing = false
        this.mapStore.loadMap(this.id)
      } else {
        this.show = false
      }
    },

    selectSpot(spotId, lat, lng) {
      this.$emit('selectSpot', spotId, lat, lng)
    },

    deleteSpotFromMap(e, spotId) {
      this.userStore.deleteSpotFromMap(spotId, this.map.id)

      e.cancelBubble = true;
      if (e.stopPropagation) e.stopPropagation();
    },

    async editMap () {
      if (!this.editing) {
        if (this.map.description) this.$refs.mapDescTextArea.style.height = this.$refs.mapDescText.scrollHeight + 10 + 'px'
        this.editing = true
      } else {
        const mapData = new FormData()
        mapData.append('name', this.map.name)
        console.log(this.map.description)
        mapData.append('description', this.map.description)

        await this.mapStore.updateMap(this.myUser.id, mapData)
        this.editing = false
        this.mapStore.loadMap(this.$route.params.id)
      }
    },

    resizeTextArea () {
      this.$refs.mapDescTextArea.style.height = '1px'
      this.$refs.mapDescTextArea.style.height = this.$refs.mapDescTextArea.scrollHeight + 'px'
    },
  }
}
</script>

<style scoped>

.mapInfo {
  z-index: 1;
}

.mapInfo.show {
  width: 22%;
  background-color: #f8f8f8;
  box-shadow: 3px 0 3px 2px rgba(0, 0, 0, 0.1), 0 0 0 2px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  text-align: left;
}

.mapInfo.hide {
  text-align: left;
  height: min-content;
  width: min-content;
}

.mapInfo.hide button {
  background-color: #f8f8f8;
  color: var(--my-black);
  box-shadow: 3px 0 3px 2px rgba(0, 0, 0, 0.1), 0 0 0 2px rgba(0, 0, 0, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  /*border-top: 1px solid var(--my-black);*/
  /*border-right: 1px solid var(--my-black);*/
  /*border-bottom: 1px solid var(--my-black);*/
  border-radius: 0 5px 5px 0;
  margin-top: 20px;
  margin-left: -20px;
  padding: 10px 2px 10px 20px;
}

.mapInfo.hide button:hover {
  transform: translateX(5px);
}

.mapInfoTop {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-inline: 10px;
  margin-top: 20px;
}

.controlBtns {
  display: flex;
  align-items: center;
}

.controlBtns button {
  color: var(--my-black);
  background-color: transparent;
  border: none;
  padding: 0 0 0 5px;
  display: flex;
  align-items: center;
}

#closeInfoBtn {
  font-size: 2rem;
}

#editMapBtn .save {
  color: #198754;
}

input.text_disabled {
  background-color: #f8f8f8;
  resize: none;
}

.mapName {
  font-size: 1.5rem;
  font-weight: bold;
  border: none;
  color: var(--my-black);
}

.mapCreator {
  padding-left: 16px;
}

.mapDescription {
  padding: 16px;
}

.spotList {
  display: flex;
  flex-direction: column;
}

.spotItem {
  padding-inline: 10px;
  padding-bottom: 10px;
  display: flex;
  justify-content: space-between;
}

.spotItem:hover {
  cursor: pointer;
}

.spotItem img {
  height: 1.8rem;
  width: auto;
  padding-right: 10px;
}

#deleteSpotFromMapBtn {
  color: var(--my-black);
  background-color: transparent;
  border: none;
  padding: 0 0 0 5px;
  display: flex;
  align-items: center;
}

</style>