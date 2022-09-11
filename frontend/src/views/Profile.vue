<template>
  <div class="profile">
    <div class="topProfile container-fluid">
      <div class="username">
        {{ username }}
      </div>
    </div>

    <div class="infoProfile container-fluid">
      <div class="row">
        <div class="piCol col-3 col-md-2">
          <img class="pictureProfile w-100" :src="profile_picture" alt="">
        </div>
        <div class="infoText col-9">
          <input v-model="profile.social" type="text" class="social" size="30" disabled >
          <textarea v-model="profile.bio" type="text" class="bio w-75" disabled></textarea>
        </div>
      </div>
    </div>


    <div class="maps container-fluid">
      <div class="row gy-4">
        <div class="map col-6 col-sm-4 col-md-3 col-lg-2" v-for="map in maps">
          <router-link :to="'/map/' + map.id">
            <div class="card mb-4 shadow-sm h-100">
              <div class="card-img-top">
                <img v-if="map.name==='Added by me'" src="../assets/addedByMe.png" alt="">
                <img v-else-if="map.name==='Favourites'" src="../assets/favoruites.png" alt="">
                <img v-else src="../assets/mapIcon.svg" alt="">
              </div>
              <div class="card-body">
                <h5 class="card-title fw-bold align-middle">{{ mapName(map) }}</h5>
              </div>
            </div>
          </router-link>

        </div>
      </div>
    </div>



  </div>
  <button type="button" class="btn" data-bs-toggle="modal" data-bs-target="#alertModal" id="modalTrigger" ref="modalTrigger" hidden></button>
    <div class="modal fade" id="alertModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="alertModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header"></div>
          <div class="modal-body">
            <p>The user you are looking for doesn't exist</p>
          </div>
          <div class="modal-footer">
            <router-link to="/"> <button type="button" data-bs-dismiss="modal" class="btn btn-secondary">Close</button> </router-link>
          </div>
        </div>
      </div>
    </div>
</template>

<script>
import { mapState, mapStores } from 'pinia';

import { fetchMyUser, fetchMaps } from "@/api";
import { useUserStore } from "@/stores/UserStore";
import { useGlobalStore } from "@/stores/GlobalStore";

export default {
  name: "Profile",

  computed: {
    computedTitle () {
      return `${this.username}'s Profile | ${this.title}`
    },
    profile_picture () {
        return this.profile.profile_picture ? 'http://127.0.0.1:8000' + this.profile.profile_picture : '/src/assets/profile-placeholder.png'
    },
    ...mapStores(useUserStore, useGlobalStore),
    ...mapState(useUserStore, ['user', 'isAuthenticated']),
    ...mapState(useGlobalStore, ['title'])
  },

  data () {
    return {
      username: '',
      profile: {},
      maps: [],
    }
  },

  watch: {
    userId: function(id) {
      console.log({'isAuth': this.isAuthenticated, 'param': this.$route.params.id})

    }
  },

  async created () {

    await fetchMyUser(this.$route.params.id)
        .then(response => {
          this.username = response.data.user.username
          this.profile = response.data.myuser
          document.title = `${this.username}'s profile | ${this.title}`

        })
        .catch(err => {
          console.log(err)
          this.$refs.modalTrigger.click()
        })

    fetchMaps(this.profile.id)
        .then(response => {
          console.log(response)
          this.maps = response.data
        })
        .catch(error => {
          console.log(error)
        })

  },

  mounted() {
    if (this.isAuthenticated && parseInt(this.$route.params.id) === this.user.id) {
        this.$router.push({name: 'MyProfile'})
    }
  },

  methods: {
    mapName (map) {
      let n = ''
      if (map) {
        if (map.creator.id === parseInt(this.$route.params.id)) n = map.name
        else if (map.name === 'Added by me') n = `Added by ${map.creator.username}`
        else n = `${map.creator.username}'s ${map.name}`
      }
      return n
    },
  }

}


</script>

<style scoped>

@media (min-width: 992px) {
  .upload-profile-picture span {
    font-size: 3rem;
  }
}

.topProfile {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-left: 30px;
}

.infoProfile {
  padding-left: 30px;
}

.topProfile button {
  margin-top: 1rem;
  margin-bottom: 1rem;
  margin-right: 1rem;
}

.topProfile .username {
  font-size: x-large;
  font-weight: bold;
  margin: 1em 0;
}

.pictureProfile {
  width: 100%;
  height: auto;
}

.infoText {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.infoText input, .infoText textarea {
  background-color: #f8f8f8;
  margin-bottom: 10px;
  padding: 10px;
}

.infoText textarea {
  resize: none;
}

.piCol {
  max-width: 300px!important;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.maps {
  padding: 30px;
}

.map {
  transition: transform .2s ease-in-out;
}

.map:hover {
  transform: scale(1.1);
}

.map a {
  color: black;
  text-decoration: none;
  transition: transform .2s ease-in-out;
}

.map a:hover {
  color: black;
}

.map img {
  width: 100%;
  height: auto;
  padding: 20px;
}

.card-body {
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-body {
  background-color: transparent;
}

#alertModal .modal-content {
  background-color: #f8d7da;
  color: #842029;
}

</style>