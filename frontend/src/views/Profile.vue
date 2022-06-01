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
          <div class="social"> @{{ myUser.social }} </div>
          <div class="bio"> {{ myUser.bio }} </div>
        </div>
      </div>
    </div>


    <div class="maps container-fluid">
      <div class="row gy-4">
        <div class="map col-6 col-sm-4 col-md-3 col-lg-2" v-for="map in maps">
          <div class="card h-100">
            <img v-if="map.name==='Added by me'" class="card-img-top" src="../assets/addedByMe.png" alt="">
            <img v-else-if="map.name==='Favourites'" class="card-img-top" src="../assets/favoruites.png" alt="">
            <img v-else class="card-img-top" src="../assets/mapIcon.svg" alt="">
            <div class="card-body">
              <h5 class="card-title fw-bold">{{ map.name }}</h5>
            </div>
          </div>
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
        console.log('myUserId: ' + this.myUser.id)
      })
      .then(() => {
        axios
        .get('/api/myMaps/' + this.myUser.id)
        .then(response => {
          this.maps = response.data
          console.log(this.maps)
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
    document.title = this.$store.state.title + ' | Profile'
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

.map img {
  padding: 15%
}

</style>