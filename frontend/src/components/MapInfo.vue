<template>
<div class="mapInfo" v-if="show">
  <input v-model="name" disabled>
  <div class="spotList">
    <div class="spotItem" v-for="spot in spots">{{spot.name}}</div>
  </div>
</div>
</template>

<script>


import {mapState, mapStores} from "pinia";
import { useMapStore } from "@/stores/MapStore";

export default {
  name: "MapInfo",

  computed: {
    ...mapStores(useMapStore),
    ...mapState(useMapStore, ['name', 'spots']),
  },

  data () {
    return {
      show: true,
    }
  },
}
</script>

<style scoped>

.mapInfo {
  background-color: #f8f8f8;
  box-shadow: 3px 0 3px 2px rgba(0, 0, 0, 0.1), 0 0 0 2px rgba(0, 0, 0, 0.08);
  display: flex;
  flex-direction: column;
}

</style>