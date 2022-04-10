<template>
  <div class="profile">
    <h1>My Profile</h1>

    <button @click="logout()" type="button" class="btn btn-danger">Logout</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Profile',
  methods: {
    logout() {
      axios.defaults.headers.common["Authorization"] = ""

      localStorage.removeItem("token")
      localStorage.removeItem("username")
      localStorage.removeItem("userId")

      this.$store.commit('removeToken')

      this.$router.push('/')
    }
  }
}
</script>