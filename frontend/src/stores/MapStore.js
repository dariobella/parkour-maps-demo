import {defineStore} from 'pinia'
import * as Api from '@/api'
import {addPics} from "../api";

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

    addSpot(formData) {
      return Api.addSpot(formData[0])
        .then((response) => {
          console.log(response)
          if (formData.length > 1) {
            formData[1].append('spotId', response.data.id)
            Api.addPics(formData[1])
              .then((response) => {
                console.log(response)
                this.loadSpots()
              })
              .catch((error) => {
                console.log(error)
              })
          } else {
            this.loadSpots()
          }
        })
        .catch((error) => {
          console.log(error)
        })
    },

    updateSpot(spot, id) {
      return Api.updateSpot(spot, id)
        .then(() => {
          //
        })
        .catch((error) => {
          console.log(error)
        })
    },

    updateSpotPics(id, data) {
      return Api.updateSpotPics(id, data)
        .then(() => {
          //
        })
        .catch((error) => {
          console.log(error)
        })
    },

    deleteSpot(id) {
      return Api.deleteSpot(id)
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

