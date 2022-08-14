<template>
  <div class="profile">
    <div class="topProfile container-fluid">
      <div class="username">
        {{ user.username }}
      </div>
      <div class="btns">
        <button v-if="editing" @click="edit(0)" type="button" class="btn btn-secondary">Cancel</button>
        <button @click="edit(1)" type="button" class="btn" :class="editBtnClass">{{ editBtn }}</button>
        <button @click="logout()" type="button" class="btn btn-danger">Logout</button>
      </div>
    </div>

    <div class="infoProfile container-fluid">
      <div class="row">
        <div class="piCol col-3 col-md-2">
          <img class="pictureProfile w-100" :src="this.profile_picture" alt="">
          <input @change="profilePictureSelected" type="file" accept="image" ref="profile_picture" hidden>
          <div v-if="editing" class="img-overlay">
            <button class="upload-profile-picture" @click.prevent="this.$refs.profile_picture.click()">
              <span class="material-icons">{{ upload_icon }}</span>
            </button>
          </div>
        </div>
        <div class="infoText col-9">
          <input v-model="myUser.social" type="text" class="social" :class="text_editing" size="30" placeholder="Click edit to add your social handle" :disabled="!editing" >
          <textarea v-model="myUser.bio" type="text" class="bio w-75" :class="text_editing" placeholder="Click edit to add your bio" :disabled="!editing"></textarea>
        </div>
      </div>
    </div>


    <div class="maps container-fluid">
      <div class="row gy-4">
        <div class="map col-6 col-sm-4 col-md-3 col-lg-2" v-for="map in myUser.maps">
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
        <div class="map col-6 col-sm-4 col-md-3 col-lg-2">
          <button class="new-map-btn shadow-sm w-100 h-100">
            <div class="card-img-top">
              <span class="material-icons">add_circle</span>
            </div>
            <span class="card-body fw-bold">New Map</span>
          </button>
        </div>
      </div>
    </div>
    

    
  </div>
</template>

<script>
import axios from 'axios'
import { mapStores, mapState } from 'pinia';
import { useUserStore } from "@/stores/UserStore";

export default {
  name: 'Profile',

  computed: {
    profile_picture () {
      if (!this.pictureChanged) {
        return this.myUser.profile_picture ? 'http://127.0.0.1:8000' + this.myUser.profile_picture : '/src/assets/profile-placeholder.png'
      } else {
        return URL.createObjectURL(this.$refs.profile_picture.files[0]);
      }
    },
    upload_icon () {
      return this.pictureChanged ? 'download_done' : 'file_upload'
    },
    text_editing () {
      return this.editing ? 'text-editing' : ''
    },
    editBtn () {
      return this.editing ? 'Save' : 'Edit'
    },
    editBtnClass () {
      return this.editing ? 'btn-success' : 'btn-secondary'
    },
    ...mapStores(useUserStore),
    ...mapState(useUserStore, ['user', 'myUser', 'title'])
  },

  data () {
    return {
      editing: false,
      pictureChanged: false,
    }
  },

  created () {
    this.userStore.loadMyMe()
  },

  mounted () {
    document.title = this.title + ' | Profile'
  },

  methods: {
    logout () {
      axios.defaults.headers.common["Authorization"] = ""

      localStorage.removeItem("token")
      localStorage.removeItem("username")
      localStorage.removeItem("userId")

      this.userStore.removeToken()
      this.userStore.clearUser()
      this.$router.push({name: 'Home'})
    },

    edit (save = 0) {
      if (!this.editing) {
        this.editing = true
      } else {
        if (save) {
          const userData = new FormData()
          userData.append('social', this.myUser.social)
          userData.append('bio', this.myUser.bio)
          if (typeof this.myUser.profile_picture === 'string') this.myUser.profile_picture = this.myUser.profile_picture.substring('/media/'.length)
          userData.append('profile_picture', this.myUser.profile_picture)

          this.userStore.updateMyUser(userData, this.myUser.id)
        } else {
          this.userStore.loadMyMe()
        }
        this.editing = false
      }
    },

    profilePictureSelected () {
      this.pictureChanged = true;
      if (this.$refs.profile_picture.files[0]) {
       this.myUser.profile_picture = this.$refs.profile_picture.files[0]
      }
    }
  }
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

.new-map-btn {
  background-color: #bbb;
  border: 1px solid rgba(0, 0, 0, 0.125);
  border-radius: 0.25rem;
  padding-top: 6rem;
  padding-bottom: 6rem;
}

.new-map-btn:hover {
  transform: none!important;
}

.new-map-btn .material-icons {
  font-size: 4rem;
}

</style>