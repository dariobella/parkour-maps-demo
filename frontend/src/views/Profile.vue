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
          <img class="pictureProfile w-100" :src="this.profile_picture" alt="">
        </div>
        <div class="infoText col-9">
          <input v-model="myUser.social" type="text" class="social" size="30" disabled >
          <textarea v-model="myUser.bio" type="text" class="bio w-75" disabled></textarea>
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
                <h5 class="card-title fw-bold align-middle">{{ map.name }}</h5>
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
import axios from "axios";

export default {
  name: "Profile",

  computed: {
    profile_picture () {
        return this.myUser.profile_picture ? 'http://127.0.0.1:8000' + this.myUser.profile_picture : '/src/assets/profile-placeholder.png'
    },
  },

  data () {
    return {
      username: '',
      userId: 0,
      myUser: {},
      maps: [],
    }
  },

  created () {
    axios
      .get('/api/profile/' + this.$route.params.id + '/')
      .then(response => {
        this.userId = response.data.id
        this.myUser = response.data.myUser
      })
    .catch(err => {
      console.log(err)
      this.$refs.modalTrigger.click()
    })
  },

  mounted() {
    document.title = this.$store.state.title + ' | Profile'
  },

}


</script>

<style>

@media (min-width: 992px) {
  .upload-profile-picture span {
    font-size: 3rem;
  }
}

.topProfile {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.topProfile button {
  margin-top: 1rem;
  margin-bottom: 1rem;
  margin-right: 1rem;
}

.topProfile .username {
  font-size: x-large;
  font-weight: bold;
  padding-left: 1rem;
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

.infoText .text-editing {
  background-color: #dedede;
  color: #333333;
}

.piCol {
  max-width: 300px!important;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.img-overlay {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
}

.img-overlay:before {
  content: '';
  display: block;
  height: 50%;
}

.upload-profile-picture {
  display: flex;
  --webkit-transform: translate(-50%, -50%);
  transform: translate(-50%, -50%);
  background-color: var(--my-black);
  border-radius: 100%;
  margin-left: 50%;
}

.upload-profile-picture:hover {
  --webkit-transform: scale(1.2) translate(-40%, -40%);
  transform: scale(1.2) translate(-40%, -40%);
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

#alertModal .modal-content {
  background-color: #f8d7da;
  color: #842029;
}

</style>