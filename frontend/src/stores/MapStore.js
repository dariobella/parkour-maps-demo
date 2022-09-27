import {defineStore} from 'pinia'
import * as Api from '@/api'
import {useGlobalStore} from "./GlobalStore";

export const useMapStore = defineStore("map", {

  state: () => ({
    id : 0,
    name: '',
    description: '',
    spots: [],
    creator: {},
  }),

  getters: {},

  actions: {

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
                  const global = useGlobalStore()
                  global.setToast({title: 'Spot addded successfully'}, {type: 'success'})
              })
              .catch((error) => {
                console.log(error)
              })
          } else {
            this.loadSpots()
            const global = useGlobalStore()
            global.setToast({title: 'Spot addded successfully'}, {type: 'success'})
          }
        })
        .catch((error) => {
          const global = useGlobalStore()
          let e = error.response.data.name[0] ?? 'Error while trying to add spot'
          global.setToast({title: e}, {type: 'danger'})
        })
    },

    updateSpot(spot, id) {
      return Api.updateSpot(spot, id)
        .then(() => {
          //
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          let e = error.response.data.name[0] ?? 'Error while trying to update spot'
          global.setToast({title: e}, {type: 'danger'})
        })
    },

    updateSpotPics(id, data) {
      return Api.updateSpotPics(id, data)
        .then(() => {
          //
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          global.setToast({title: 'Error while trying to updated images'}, {type: 'danger'})
        })
    },

    deleteSpot(id) {
      return Api.deleteSpot(id)
        .then(() => {
          this.loadSpots()
          const global = useGlobalStore()
          global.setToast({title: 'Spot deleted successfully'}, {type: 'success'})
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          global.setToast({title: 'Error while trying to delete spot'}, {type: 'danger'})
        })
    },

    loadSpots() {
      return Api.fetchSpots()
        .then((response) => {
          this.name = ""
          this.description = ""
          this.spots = response.data
          this.creator = {}
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          global.setToast({title: 'Error while trying to load spots'}, {type: 'danger'})
        })
    },

    loadMap(id) {
      return Api.loadMap(id)
        .then((response) => {
          this.id = response.data.id
          this.name = response.data.name
          this.description = response.data.description
          this.spots = response.data.spots
          this.creator = response.data.creator
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          global.setToast({title: 'Error while trying to load map'}, {type: 'danger'})
        })
    },

    updateMap(idUser, map) {
      return Api.updateMap(idUser, this.id, map)
        .then((response) => {
          this.loadMap(this.id)
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          global.setToast({title: 'Error while trying to update map'}, {type: 'danger'})
        })
    },

    deleteSpotFromMap(userId, spot, map) {
      return Api.deleteSpotFromMap(userId, spot, map)
        .then((response) => {
          const global = useGlobalStore()
          global.setToast({title: 'Spot deleted from map successfully'}, {type: 'success'})
          this.loadMap(map)
        })
        .catch((error) => {
          console.log(error)
          const global = useGlobalStore()
          global.setToast({title: error.message}, {type: 'danger'})
        })
    },

  }

})

