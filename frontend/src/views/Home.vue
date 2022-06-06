<template>
    <div class="Home">
      <Map :spots="spots"/>
    </div>
</template>


<script>
import Map from '../components/Map.vue'
import axios from "axios";

export default {
  name: 'Home',

  components: {
    Map
  },

  data () {
    return {
      spots: [],
    }
  },

  created () {
    axios
      .get('/api/spots/',)
      .then(response => {
        console.log('API data retrieved')
        this.spots = response.data
      })
    .catch(err => {
        console.log(err)
    })
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