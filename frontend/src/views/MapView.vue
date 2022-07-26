<template>

  <div class="mapView">
    <div class="currentMap">
      <div class="currentMapLabel">Current map: {{ name }} </div>
    </div>
    <Map />
    <button type="button" class="btn" data-bs-toggle="modal" data-bs-target="#alertModal" id="modalTrigger" ref="modalTrigger" hidden></button>
    <div class="modal fade" id="alertModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="alertModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header"></div>
          <div class="modal-body">
            <p>The map you are looking for doesn't exist</p>
          </div>
          <div class="modal-footer">
            <router-link to="/myProfile"> <button type="button" data-bs-dismiss="modal" class="btn btn-secondary">Close</button> </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>

</template>

<script>

import Map from '@/components/Map.vue'
import { mapStores, mapState } from 'pinia';
import { useMapStore } from "@/stores/MapStore";
import { useUserStore } from "@/stores/UserStore";

export default {
  name: 'MapView',

  components: {
    Map
  },

  computed: {
    ...mapStores(useMapStore),
    ...mapState(useMapStore, ['name']),
    ...mapState(useUserStore, ['title'])
  },

  created () {
    this.mapStore.loadMap(this.$route.params.id)
  },

  mounted() {
    document.title = this.title + ' | Map'
  },

}
</script>

<style scoped>

#alertModal .modal-content {
  background-color: #f8d7da;
  color: #842029;
}

.currentMap {
  background-color: var(--my-black);
  display: flex;
}

.currentMapLabel {
  background-color: white;
  padding: 5px;
  padding-inline: 10px;
  border-radius: 5px;
  margin: 5px;
}

</style>