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
        <div class="map col-8 col-sm-4 col-md-3 col-lg-2" v-for="map in maps">
          <router-link :to="'/map/' + map.id" class="position-relative">
            <div class="card mb-4 shadow-sm h-100">
              <div class="card-img-top">
                <img v-if="map.name==='Added by me'" src="../assets/addedByMe.png" alt="">
                <img v-else-if="map.name==='Favourites'" src="../assets/favoruites.png" alt="">
                <img v-else-if="map.icon" :src="`http://127.0.0.1:8000${map.icon}`" alt="">
                <img v-else src="../assets/mapIcon.svg" alt="">
              </div>
              <div class="card-body">
                <div class="mapName">
                  <h5 class="card-title fw-bold align-middle">{{ mapName(map) }}</h5>
                </div>
              </div>
            </div>
            <button v-if="editing" id="deleteMapBtn" data-bs-toggle="modal" data-bs-target="#deleteMapModal" @click.prevent="this.mapToDelete = map.id" class="position-absolute top-0 start-100">
              <span class="material-icons">delete</span>
            </button>
          </router-link>

        </div>
        <div class="map col-6 col-sm-4 col-md-3 col-lg-2">
          <button type="button" class="new-map-btn shadow-sm w-100 h-100" data-bs-toggle="modal" data-bs-target="#newMapModal">
            <div class="card-img-top">
              <span class="material-icons">add_circle</span>
            </div>
            <span class="card-body fw-bold">New Map</span>
          </button>
        </div>
        <div class="modal fade" id="newMapModal" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLabel">New Map</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <form @submit.prevent id="newMapForm">
                  <div>
                    <label for="newMapName">Map name: </label>
                    <input type="text" name="newMapName" id="newMapName" v-model="newMapName">
                  </div>
                  <div>
                    <input @change="newMapIconSelected" type="file" name="newMapIcon" id="newMapIcon" ref="newMapIcon" hidden>
                    <button id="newMapIconBtn" @click.prevent="this.$refs.newMapIcon.click()"> <span class="material-icons">upload</span> Map icon </button>
                    <img class="newMapIconImg" :src="newMapIconUrl" alt="">
                  </div>
                </form>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                <button type="button" class="btn btn-success"  data-bs-dismiss="modal" @click="newMap">Save</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="deleteMapModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-body">
            <div class="modalText">Are you sure you want to delete this map?</div>
            <div class="modalBtns">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="this.mapToDelete = 0">No</button>
              <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="deleteMap()">Yes</button>
            </div>
          </div>
        </div>
      </div>
    </div>
    

    
  </div>
</template>

<script>
import axios from 'axios'
import { mapStores, mapState } from 'pinia';
import { useUserStore } from "@/stores/UserStore";
import { useGlobalStore } from "@/stores/GlobalStore";

export default {
  name: 'Profile',

  computed: {
    profile_picture () {
      if (!this.pictureChanged) {
        return this.myUser.profile_picture ? `http://127.0.0.1:8000${this.myUser.profile_picture}` : '/src/assets/profile-placeholder.png'
      } else {
        return URL.createObjectURL(this.$refs.profile_picture.files[0]);
      }
    },
    newMapIconUrl () {
      if (this.newMapIcon) {
        return URL.createObjectURL(this.newMapIcon);
      } else {
        return ''
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
    ...mapStores(useUserStore, useGlobalStore),
    ...mapState(useUserStore, ['user', 'myUser', 'maps'])
  },

  data () {
    return {
      editing: false,
      pictureChanged: false,
      newMapName: '',
      newMapIcon: null,
      mapToDelete: 0,
    }
  },

  async created () {
    await this.userStore.loadMyMe()
    await this.userStore.loadMyMaps()
  },

  mounted () {
    document.title = 'My Profile | ' + this.globalStore.title
  },

  methods: {
    mapName (map) {
      let n = ''
      if (map) {
        if (map.creator.id === this.user.id) n = map.name
        else if (map.name === 'Added by me') n = `Added by ${map.creator.username}`
        else n = `${map.creator.username}'s ${map.name}`
      }
      return n
    },

    logout () {
      axios.defaults.headers.common["Authorization"] = ""

      localStorage.removeItem("token")
      localStorage.removeItem("username")
      localStorage.removeItem("userId")

      this.userStore.removeToken()
      this.userStore.clearUser()
      this.globalStore.setToast({title: 'Logged out successfully'}, {type: 'success'})
      this.$router.push({name: 'Home'})
    },

    async edit (save = 0) {
      if (!this.editing) {
        this.editing = true
      } else {
        if (save) {
          const userData = new FormData()
          userData.append('social', this.myUser.social)
          userData.append('bio', this.myUser.bio)
          if (typeof this.myUser.profile_picture === 'string') this.myUser.profile_picture = this.myUser.profile_picture.substring('/media/'.length)
          userData.append('profile_picture', this.myUser.profile_picture)

          await this.userStore.updateMyUser(userData, this.myUser.id)
        }

        this.$refs.profile_picture.value = null
        this.pictureChanged = false
        this.editing = false
      }
    },

    profilePictureSelected () {
      this.pictureChanged = true
      if (this.$refs.profile_picture.files[0]) {
       this.myUser.profile_picture = this.$refs.profile_picture.files[0]
      }
    },

    newMap () {
      if (!this.newMapName) {
        this.globalStore.setToast({title: 'Map name is required'}, {type: 'danger'})
      } else if (['Added by me', 'Favourites'].includes(this.newMapName)) {
        this.globalStore.setToast({title: 'Cannot create a map with that name'}, {type: 'danger'})
      } else {
        const formData = new FormData()
        formData.append('name', this.newMapName)
        if (this.newMapIcon) formData.append('icon', this.newMapIcon)

        this.userStore.addMap(formData)
      }
    },

    newMapIconSelected () {
      if (this.$refs.newMapIcon.files[0]) {
        this.newMapIcon = this.$refs.newMapIcon.files[0]
      }
    },

    deleteMap() {
      if (this.mapToDelete) this.userStore.deleteMap(this.mapToDelete)
    }
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

.card-img-top {
  height: 70%;
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

.modal-content {
  margin-bottom: 8rem;
}

#newMapForm {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 0;
}

#newMapForm div {
  display: flex;
  align-items: center;
  padding: 10px 0;
}

#newMapForm input {
  margin: 0;
}

#newMapForm label, #newMapIconBtn {
  margin-right: 10px;
}

#newMapIconBtn {
  display: flex;
  align-items: center;
  height: 100%;
}

#newMapIconBtn span {
  padding-right: 5px;
}

.newMapIconImg {
  height: 5rem;
}

#deleteMapBtn {
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  transform: translateX(-70%) translateY(-30%);
  border-radius: 100%;
  background-color: #dc3545;
  padding: 10px;
  transition: transform .2s ease-in-out;
}

#deleteMapBtn:hover {
  transform: scale(1.2) translateX(-60%) translateY(-25%);
}

</style>