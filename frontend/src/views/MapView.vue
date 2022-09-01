<template>

  <div class="mapView">
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
import { useGlobalStore } from "@/stores/GlobalStore";

export default {
  name: 'MapView',

  components: {
    Map
  },

  computed: {
    ...mapStores(useMapStore, useGlobalStore),
    ...mapState(useMapStore, ['name']),
  },

  created () {
    this.mapStore.loadMap(this.$route.params.id)
  },

  mounted() {
    document.title = 'Map | ' + this.globalStore.title
  },

}
</script>

<style scoped>

#alertModal .modal-content {
  background-color: #f8d7da;
  color: #842029;
}

</style>