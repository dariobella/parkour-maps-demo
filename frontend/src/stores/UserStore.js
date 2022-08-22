import {defineStore} from 'pinia'
import axios from 'axios'

import * as Api from '@/api'
import { useGlobalStore } from "./GlobalStore";

export const useUserStore = defineStore("user", {

  state: () => ({
    user: {},
    myUser: {},
    token: '',
    isAuthenticated: false,
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
        })
        .catch((error) => {
          console.log(error)
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
      await this.loadMe()
      return Api.fetchMyUser(this.user.id)
        .then((response) => {
          this.myUser = response.data.user[1]
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
          this.loadMyMe()
        })
        .catch((error) => {
          console.log(error)
        })
    },
  },

})
