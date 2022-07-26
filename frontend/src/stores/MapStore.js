import {defineStore} from 'pinia'
import * as Api from '@/api'

export const useMapStore = defineStore("map", {

  state: () => ({
    name: '',
    spots: [],
    //toast: {},
  }),

  getters: {},

  actions: {

    loadMyMaps(id) {
      return Api.fetchMyMaps(id)
        .then((response) => {
          this.myMaps = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    },

    addSpot(spot) {
      return Api.addSpot(spot)
        .then(() => {
          this.loadSpots()
        })
        .catch((error) => {
          console.log(error)
        })
    },

    loadSpots() {
      return Api.fetchSpots()
        .then((response) => {
          this.spots = response.data
        })
        .catch((error) => {
          console.log(error)
        })
    },

    loadMap(id) {
      return Api.loadMap(id)
        .then((response) => {
          this.name = response.data.name
          this.spots = response.data.spots
        })
        .catch((error) => {
          console.log(error)
        })
    },

  }

})

