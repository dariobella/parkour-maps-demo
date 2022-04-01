<template>
  <div class="app">
    <Navbar></Navbar>
    <router-view/>
  </div>
</template>



<script>
import Navbar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    Navbar
  },
}
</script>




<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700&display=swap');

html, body {
  margin: 0;
  padding: 0;
  background-color: #f8f8f8!important;
  font-family: 'Nunito', sans-serif;
}

#app {
  font-family: 'Nunito', sans-serif;
}
</style>
