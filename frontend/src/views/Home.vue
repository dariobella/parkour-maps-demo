<template>
    <div class="Home">
      <Map />
    </div>
</template>


<script>
import { mapStores } from 'pinia';

import { useMapStore } from "@/stores/MapStore";
import { useGlobalStore } from "@/stores/GlobalStore";
import Map from '@/components/Map.vue'

export default {
  name: 'Home',

  components: {
    Map
  },

  computed: {
    ...mapStores(useMapStore, useGlobalStore)
  },

  beforeMount() {
    this.mapStore.loadSpots()
  },

  mounted() {
    document.title = this.globalStore.title
  },

  methods: {
    toast() {
      this.globalStore.setToast({title: 'Butun'}, {type: 'success'})
    },
  }

}
</script>


<style>

.home {
  background-color: var(--my-black)!important;
}

</style>