<template>
<div class="mapInfo" v-if="show">
  <div class="mapInfoTop">
    <input class="mapName" v-model="name" :class="editing ? 'text_editing' : 'text_disabled'" placeholder="Map name" :disabled="!editing"> <!-- :size="name.length" -->
    <div class="controlBtns">
      <button v-if="creator.id === user.id" id="editMapBtn" @click="editMap()">
        <span class="material-icons" :class="{ save : editing }"> {{ editing ? 'save' : 'edit' }} </span>
      </button>
      <button id="closeInfoBtn" @click="closeMapInfo()">
        <span class="material-icons">{{ editing ? 'close' : 'arrow_left' }}</span>
      </button>
    </div>
  </div>
  <div class="spotList">
    <div class="spotItem" v-for="spot in spots">
      <div>
        <img :src="spotIcon(spot.type)">
        <span>{{spot.name}}</span>
      </div>
      <div>
        <button id="deleteSpotFromMapBtn">
          <span class="material-icons">close</span>
        </button>
      </div>
    </div>
  </div>
</div>
</template>

<script>


import {mapState, mapStores} from "pinia";
import { useMapStore } from "@/stores/MapStore";
import {useUserStore} from "@/stores/UserStore";

export default {
  name: "MapInfo",

  computed: {
    ...mapStores(useMapStore),
    ...mapState(useMapStore, ['id', 'name', 'spots', 'creator']),
    ...mapState(useUserStore, ['user']),
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

    closeMapInfo() {
      if (this.editing) {
        this.editing = false
        this.mapStore.loadMap(this.id)
      } else {
        this.show = false
      }
    },
  }
}
</script>

<style scoped>

.mapInfo {
  background-color: #f8f8f8;
  box-shadow: 3px 0 3px 2px rgba(0, 0, 0, 0.1), 0 0 0 2px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
  text-align: left;
}

.mapInfoTop {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-inline: 10px;
  margin: 20px 0;
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