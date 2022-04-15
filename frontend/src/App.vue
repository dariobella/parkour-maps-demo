<template>
  <div class="app">
    <Navbar></Navbar>
    <router-view/>
  </div>
</template>



<script>
import axios from 'axios'
import Navbar from './components/Navbar.vue'

export default {
  name: 'App',
  components: {
    Navbar
  },
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
  
    if (token) {
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
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

p {
  margin: 0rem!important;
}

#app {
  font-family: 'Nunito', sans-serif;
  text-align: center;
}

input[type=text], input[type=password], input[type=email], input[type=number], select, textarea {
  padding: 6px;
  border: none;
  background-color: #dcdcdc;
  color: #333333;
  border-radius: 5px;
}

form {
  margin: 20px;
}

form input, form select {
  margin-bottom: 20px;
}

form button {
  font-family: 'Nunito', sans-serif;
  background-color: black;
  border: 1px solid black;
  color: white;
  padding: 10px;
  padding-left: 20px; padding-right: 20px;
  font-size: 1rem;
  transition: transform .2s ease-in-out;
  border-radius: 10px;
}

button {
  background-color: #aaa;
  color: white;
  border: 1px solid #aaa;
  font-family: 'Nunito', sans-serif;
  padding: 10px;
  transition: transform .2s ease-in-out;
}

button:hover {
  cursor: pointer;
  transform: scale(1.1);
}
</style>
