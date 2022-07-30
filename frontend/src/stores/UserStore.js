import {defineStore} from 'pinia'
import axios from 'axios'
import * as Api from '@/api'
import {updateMyUser} from "../api";

export const useUserStore = defineStore("user", {

  state: () => ({
    user: {},
    myUser: {},
    token: '',
    isAuthenticated: false,
    title: 'Parkour Maps',
    //toast: {},
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
        })
        .catch(error => {
          console.log(error)
/*          if (error.response) {
            const e = []
            for (const property in error.response.data) {
              e.push(`${error.response.data[property][0]}`)
            }
            this.errors.push(e[0])

            console.log(JSON.stringify(error.response.data))
          } else if (error.message) {
            this.errors.push('Something went wrong, please try again')

            console.log(JSON.stringify(error))
          }*/
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
          this.myUser = response.data
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
    }
  }

})
