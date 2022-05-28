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
    document.title = this.$store.state.title
  },

}
</script>


<style scoped>

.home {
  background-color: var(--my-black)!important;
}

</style>