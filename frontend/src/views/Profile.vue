<template>
  <div class="profile">
    <div class="topProfile container-fluid">
      <div class="username">
        {{ username }}
      </div>
      <button @click="logout()" type="button" class="btn btn-danger">Logout</button>
    </div>

    <div class="infoProfile container-fluid">
      <div class="row">
        <div class="piCol col-3">
          <img class="pictureProfile" src="../assets/profile-placeholder.png" alt="Profile Picture">
        </div>
        <div class="infoText col-9">
          <div class="social"> @darjo.pk </div>
          <div class="bio">This is my bio</div>
        </div>
      </div>
    </div>


    <div class="maps container-fluid">
      <div class="row">
        <div class="map col-sm-6 col-md-4 col-lg-3" v-for="map in maps">
          <img src="../assets/mapIcon.svg" alt="">
          <div class="mapName"> {{ map.name }} </div>
        </div>
      </div>
    </div>
    

    
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Profile',
  data() {
    return {
      username: '',
      userId: 0,
      myUser: {},
      maps: [],
    }
  },
  created() {
    axios
    .get('/api/v1/users/me')
    .then(response => {
      this.username = response.data.username
      this.userId = response.data.id
    })
    .then(() => {
      axios
      .get('/api/myProfile/' + this.userId)
      .then(response => {
        this.myUser = response.data
        console.log('myUser: ' + this.myUser)
      })
      .then(() => {
        axios
        .get('/api/myMaps/' + this.myUser.id)
        .then(response => {
          this.maps = response.data
        })
        .catch(err => {
          console.log(err)
        })
      })
      .catch(err => {
        console.log(err)
      })
    })
    .catch(err => {
      console.log(err)
    })
  },
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

.topProfile {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.topProfile button {
  margin: 20px;
}

.topProfile .username {
  font-size: x-large;
  font-weight: bold;
  padding-left: 20px;
}

.pictureProfile {
  width: 90%;
}

.infoText {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.infoText div {
  padding: 10px;
}

.piCol {
  max-width: 300px!important;
}

.maps {
  padding: 30px;
}

.map {
  background-color: #dcdcdc;
  border-radius: 20px;
  padding: 20px;
  margin: 20px;
}

.map img {
  width: 50%;
  margin-bottom: 20px;
}

</style>