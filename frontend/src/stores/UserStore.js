import {defineStore} from 'pinia'
import axios from 'axios'

import * as Api from '@/api'
import { useGlobalStore } from "./GlobalStore";
import { useMapStore } from "./MapStore";

export const useUserStore = defineStore("user", {

  state: () => ({
    user: {},
    myUser: {},
    maps: [],
    token: '',
    isAuthenticated: false,
    addSpotPosition: {}
  }),

  getters: {},

  actions: {

    initializeStore() {
      if ( localStorage.getItem('token') ) {
        this.token = localStorage.getItem('token')
        this.isAuthenticated = true
      } else {
        this.removeToken()
      }
    },

    removeToken() {
      this.token = ''
      this.isAuthenticated = false
    },

    async addUser(user) {
      await Api.addUser(user)
        .then((response) => {
          this.user = response.data
          global.setToast()
        })
        .catch((error) => {
          console.log(error)
        })
    },

    async addMyUser(user) {
      await this.addUser(user)
      return Api.addMyUser({id: this.user.id})
        .then((response) => {
          this.myUser = response.data
          const global = useGlobalStore()
          global.setToast({title: 'Signed up successfully'}, {type: 'success'})
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          global.setToast({title: 'Error while signing up'}, {type: 'danger'})
        })
    },

    login(user) {
      return Api.login(user)
        .then((response) => {
          let token = response.data.auth_token
          console.log('Token: ' + token)
          this.token = token
          this.isAuthenticated = true
          localStorage.setItem("token", token)
          axios.defaults.headers.common['Authorization'] = "Token " + token
          this.loadMyMe()
          const global = useGlobalStore()
          global.setToast({title: 'Logged in successfully'}, {type: 'success'})
        })
        .catch(error => {
          const global = useGlobalStore()
          //console.log(error)
          if (error.response) {
            let e = ''
            for (const property in error.response.data) {
              if (property === 'non_field_errors') {
                e = 'Unable to login with provided credentials'
              } else {
                e = `${property} field is missing`
              }
            }

            global.setToast({title: e}, {type: 'danger'})

            console.log(error.response.data)
          } else if (error.message) {
            global.setToast({title: error.message}, {type: 'danger'})
          }
        })
    },

    async loadMe() {
      await Api.fetchMe()
        .then((response) => {
          this.user = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    },

    async loadMyMe() {
      if (Object.keys(this.user).length === 0) {
        await this.loadMe()
      }
      return Api.fetchMyUser(this.user.id)
        .then((response) => {
          this.myUser = response.data.myuser
          this.loadMyMaps()
        })
        .catch((error) => {
          console.log(error)
        })
    },

    updateMyUser(user, id) {
      return Api.updateMyUser(user, id)
        .then(() => {
          this.loadMyMe()
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          global.setToast({title: 'Error while trying to update profile'}, {type: 'danger'})
        })
    },

    clearUser() {
      this.user = {}
      this.myUser = {}
    },

    toggleFavourite(spot) {
      const user = new FormData()
      user.append('user', this.myUser.id)
      return Api.toggleFavourite(spot, user)
        .then(() => {
          this.loadMyMaps()
          const map = useMapStore()
          if (map.name === 'Favourites') {
            map.loadMap(map.id)
          }
        })
        .catch((error) => {
          console.log(error)
        })
    },

    loadMyMaps() {
      return Api.fetchMaps(this.myUser.id)
        .then((response) => {
          this.maps = response.data
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          global.setToast({title: 'Error while trying to load maps'}, {type: 'danger'})
        })
    },

    addMap(map) {
      return Api.addMap(map, this.myUser.id)
        .then((response) => {
          console.log(response)
          const global = useGlobalStore()
          global.setToast({title: 'Map added successfully'}, {type: 'success'})
          this.loadMyMaps()
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          global.setToast({title: 'Error while trying to add map'}, {type: 'danger'})
        })
    },

    deleteMap(map) {
      return Api.deleteMap(this.myUser.id, map)
        .then((response) => {
          console.log(response)
          const global = useGlobalStore()
          global.setToast({title: 'Map deleted successfully'}, {type: 'success'})
          this.loadMyMaps()
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          global.setToast({title: 'Error while trying to delete map'}, {type: 'danger'})
        })
    },
  },

})
