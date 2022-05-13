<template>
  <div class="profile">

    <div class="topProfile row">
      <div class="left col-sm"></div>
      <div class="center col-sm"> <span> My Profile </span></div>
      <div class="right col-sm"><button @click="logout()" type="button" class="btn btn-danger">Logout</button></div>
    </div>

    <div class="maps">
      <div class="map">

      </div>
    </div>
    

    
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Profile',
  mounted() {
    document.title = 'PK SPOT MAP | Profile'
  },
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

<style>

.topProfile div {
  padding: 20px;
}

.topProfile .right {
  display: flex;
  justify-content: flex-end;
  align-items: center;
}

</style>