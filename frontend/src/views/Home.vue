<template>
    <div class="Home">
      <Map />
    </div>
</template>


<script>
import { mapState, mapStores } from 'pinia';
import { useUserStore } from "@/stores/UserStore";
import { useMapStore } from "@/stores/MapStore";
import Map from '@/components/Map.vue'

export default {
  name: 'Home',

  components: {
    Map
  },

  computed: {
    ...mapState(useUserStore, ['title']),
    ...mapStores(useMapStore)
  },

  beforeMount() {
    this.mapStore.loadSpots()
  },

  mounted() {
    document.title = this.title
  },

}
</script>


<style>

.home {
  background-color: var(--my-black)!important;
}

</style>