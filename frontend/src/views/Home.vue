<template>
    <div class="Home">
      <Map />
    </div>
</template>


<script>
import Map from '../components/Map.vue'

export default {
  name: 'Home',

  components: {
    Map
  },

  mounted() {
    document.title = 'PKSPOTMAP'
  },

}
</script>


<style scoped>

#map {
  width: 100%;
  height: 94vh;
}

</style>