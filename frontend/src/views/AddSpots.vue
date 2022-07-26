<template>

  <div class="addSpots">

    <h1>Add Spots</h1>

    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a href="#" class="nav-link" :class="{'active': current === 1}" @click.prevent="this.current = 1">Add Spot</a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link" :class="{'active': current === 2}" @click.prevent="this.current = 2">Import KML file</a>
      </li>
    </ul>

    <div class="tab-content">
      <div class="tab-spot" v-show="current === 1">

        <div class="alert alert-danger" v-if="spotErrors.length">
          <p v-for="error in spotErrors" :key="error">{{ error }}</p>
        </div>

        <form @submit.prevent="spotSubmitForm">
          <div class="container-fluid">
            <div class="row gy-3">

              <div class="selectLocation col-12">
                <div class="choose">
                  <span>Location:</span> <button @click.prevent="initMapModal()" data-bs-toggle="modal" data-bs-target="#locationModal">Choose from map</button>
                </div>
                <div class="LatLng">
                  <label for="Lat">Lat: </label> <input type="number" name="Lat" id="Lat" v-model="lat" step="0.000001">
                  <label for="Lat">Lng: </label> <input type="number" name="Lat" id="Lng" v-model="lng" step="0.000001">
                </div>
              </div>

              <div class="label col-6"> <label for="name">Name: </label> </div>
              <div class="name col-6"> <input type="text" name="name" id="name" v-model="name"> </div>

              <div class="label col-6"> <label for="type">Type: </label> </div>
              <div class="type col-6">
                <select name="type" id="type" v-model="type">
                  <option value="S">Spot</option>
                  <option value="G">Gym</option>
                  <option value="P">Parkour Park</option>
                  <option value="U">Undercover spot</option>
                </select>
              </div>

              <div class="label col-6"> <label for="description">Description: </label> </div>
              <div class="description col-6"> <textarea name="description" id="description" v-model="description"></textarea> </div>

              <div class="images">
                <input type="file" name="images" id="images" ref="images" @change="imageSelected" multiple>
                <div class="imagesBtn">
                  <button @click.prevent="this.$refs.images.click()"> <span class="material-icons">upload</span> <span> Upload images</span> </button>
                </div>
                <div class="allImages">
                  <div class="imageSelected" v-for="(image, index) in images" :key="index">
                    <div v-if="this.images" class="fileName"> <span class="material-icons">image</span> <span class="text"> {{ image.name }} </span> </div>
                    <div v-else> No file selected </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <button class="btn-success" type="submit">Add spot</button>
        </form>



      </div>

      <div class="tab-kml" v-show="current == 2">

        <div class="alert alert-danger" v-if="kmlErrors.length">
          <p v-for="error in kmlErrors" :key="error">{{ error }}</p>
        </div>

        <form @submit.prevent="kmlSubmitForm" enctype="multipart/form-data">
          <div class="file">
            <input type="file" accept=".kml" name="kmlFile" id="kmlFile" ref="kmlFile" @change="fileSelected">
            <button @click.prevent="this.$refs.kmlFile.click()"> <span class="material-icons">upload</span> <span> Upload file</span> </button>
            <div class="selectedFile">
              <div v-if="this.kmlFile" class="fileName"> <img src="../assets/kmlIcon.png" alt=""> {{ this.kmlFile.name }} </div>
              <div v-else> No file selected </div>
            </div>
          </div>
          <button class="btn-success" type="submit">Add spots</button>
        </form>
      </div>
    </div>


    <div class="modal fade" id="locationModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">

          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Select Location</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="close"></button>
          </div>

          <div class="modal-body">
            <div id="modalMap"></div>
          </div>

          <div class="modal-footer">
            <button type="button" class="btn-dark" data-bs-dismiss="modal">Done</button>
          </div>

        </div>
      </div>
    </div>
  </div>
  
</template>

<script>

import { mapState, mapStores } from 'pinia';
import { useMapStore } from "@/stores/MapStore";
import { useUserStore } from "@/stores/UserStore";
import { addPics } from "@/api";

export default {
  name: 'AddSpots',
  computed: {
    ...mapStores(useMapStore),
    ...mapState(useUserStore, ['title', 'myUser'])
  },
  data() {
    return {
      current: 1,
      map: {},
      iconSize: {},
      marker: {},
      lat: 0,
      lng: 0,
      name: '',
      type: 'S',
      description: '',
      images: [],
      spotId: 0,
      kmlFile : '',
      spotErrors: [],
      kmlErrors: [],
    }
  },
  mounted() {
    document.title = this.title + ' | Add Spots'
  },
  methods: {
    spotSubmitForm() {
      this.spotErrors = []

      if (this.lat === 0 && this.lng  === 0) {
        this.spotErrors.push('The coordinates are missing')
      }
      else if (this.name === '') this.spotErrors.push('The name is missing')

      if (!this.spotErrors.length) {

        const formData = {
          lat: this.lat,
          lng: this.lng,
          name: this.name,
          type: this.type,
          description: this.description,
          adder: this.myUser.id
        }

        this.mapStore.addSpot(formData)
            .then((response) => {
              console.log(response)
              this.spotId = response.data.id
            })
            .then(() => {
              if (this.images.length > 0) {
                const imagesData = new FormData()
                this.images.forEach(image => {
                  imagesData.append('images', image, image.name)
                })
                imagesData.append('spotId', this.spotId)

                addPics(imagesData)
                  .then(response => {
                    console.log(response.data)
                  })
                  .catch(error => {
                    this.spotErrors.push('Something went wrong, please try again')
                    console.log(JSON.stringify(error))
                  })
              }
            })
            .then(() => {
              this.$router.push('/')
            })
            .catch((error) => {
                console.log(error)
            })
      }
    },

    initMapModal() {

      var location = {lat: parseInt(this.lat), lng: parseInt(this.lng)};
      const bounds = {
        north: 85,
        south: -85,
        west: -200,
        east: 200,
      }

      var options = {
        center: location,
        restriction: {
          latLngBounds: bounds,
          strictBounds: false,
        },
        zoom: 4,
        minZoom: 3,
        draggableCursor: 'pointer',
        mapTypeControl: true,
        mapTypeControlOptions: {
          style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
          position: google.maps.ControlPosition.LEFT_BOTTOM,
        },
      }

      this.map = new google.maps.Map(document.getElementById('modalMap'), options)
      this.marker = new google.maps.Marker({
        map: this.map,
        position: location,
      })

      var modalSearch = document.createElement('input')
      modalSearch.id = 'modalSearch'
      modalSearch.type = 'text'
      modalSearch.placeholder = 'Search places'
      this.map.controls[google.maps.ControlPosition.TOP_CENTER].push(modalSearch)
      
      var modalAutocomplete = new google.maps.places.Autocomplete(modalSearch)
      modalAutocomplete.bindTo('bounds', this.map)
      modalAutocomplete.setFields(['place_id', 'name', 'geometry', 'formatted_address'])

      var vm = this
      modalAutocomplete.addListener('place_changed', function() {
        console.log('place changed')
        var place = modalAutocomplete.getPlace();

        if (!place.geometry) {
          modalSearch.placeholder = 'Enter a place'
        } else {
          var bounds = new google.maps.LatLngBounds()

          var position = place.geometry.location
          vm.marker.setPosition(position)
          vm.lat = position.toJSON().lat.toFixed(6)
          vm.lng = position.toJSON().lng.toFixed(6)

          if (place.geometry.viewport) {
            bounds.union(place.geometry.viewport)
          } else {
            bounds.extend(place.geometry.location)
          }
          vm.map.fitBounds(bounds)
        }
      });

      this.map.addListener("click", (mapsMouseEvent) => {
        var position = mapsMouseEvent.latLng
        vm.marker.setPosition(position)

        vm.lat = position.toJSON().lat.toFixed(6)
        vm.lng = position.toJSON().lng.toFixed(6)
      })

    },

    kmlSubmitForm() {
      this.kmlErrors = []

      if (this.kmlFile) {
        const formData = new FormData();
        formData.append('kmlFile', this.kmlFile, this.kmlFile.name)
        
        console.log(formData)
        console.log('Feature TBD')

      } else {
        this.kmlErrors.push('The file is missing')
      }


    },

    imageSelected() {
      for (let i = 0; i < this.$refs.images.files.length; i++) {
        this.images.push(this.$refs.images.files[i])
      }
    },

    fileSelected() {
      this.kmlErrors = []
      this.kmlFile = this.$refs.kmlFile.files[0]

      if (!this.kmlFile) {
        this.kmlErrors.push('The file is missing')
      }
    }
  }
  
}
</script>

<style>

.pac-container { z-index: 10000 !important; }

.addSpots {
  margin: 3rem;
  min-width: 290px;
}

.addSpots h1, .addSpots button {
  margin: 1em;
}
.addSpots .LatLng label {
  padding-inline: 0.5rem;
}

.addSpots .label {
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.addSpots .name, .addSpots .type, .addSpots .description {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}

.addSpots .name input, .addSpots .description textarea {
  width: 100%;
  max-width: 300px;
}

.addSpots .container-fluid input, .addSpots .container-fluid select {
  margin: 0;
}

.addSpots input[type=number] {
  width: 6rem;
}

.addSpots form {
  margin: 0;
  display: flex;
  flex-direction: column;
}

.addSpots .nav-item {
  width: 50%;
}

.addSpots .tab-content {
  border: 1px solid #dee2e6;
  border-top: none;
  padding: 2em;
}

.addSpots button[type=submit] {
  align-self: flex-end;
}

.addSpots .selectLocation {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  justify-content: center;
}

.addSpots .file, .addSpots .images {
  display: flex;
  justify-content: center;
}

.addSpots .file button, .addSpots .images button {
  display: flex;
  align-items: center;
}

.addSpots .file button .material-icons, .addSpots .images button .material-icons {
  margin-right: 10px;
}

.addSpots .file input[type=file], .addSpots .images input[type=file] {
  display: none;
}

.addSpots .file .selectedFile, .addSpots .images .imageSelected {
  display: flex;
  align-items: center;
}

.addSpots .images .allImages {
  display: flex;
  flex-wrap: wrap;
}

.addSpots .file .selectedFile div {
  padding: 10px;
  padding-inline: 15px;
  border: none;
  background-color: #dcdcdc;
  color: #333333;
  border-radius: 5px;
}

.addSpots .file .selectedFile .fileName {
  padding: 10px;
  padding-inline: 15px;
  border: none;
  background-color: #dcdcdc;
  color: #333333;
  border-radius: 5px;
}

.addSpots .images .imageSelected .fileName {
  display: flex;
  align-items: center;
  padding: 10px;
  padding-inline: 15px;
  margin: 10px;
  border: none;
  background-color: #dcdcdc;
  color: #333333;
  border-radius: 5px;
}

.addSpots .images .imageSelected .fileName .text {
  padding-inline: 10px;
}

.addSpots .file .selectedFile img {
  width: 2rem;
  margin-right: 5px;
}

.addSpots .modal-footer button {
  border-radius: 10px;
}

.addSpots .modal-body {
  height: 60vh;
}

#modalMap {
  height: 100%;
}

#modalSearch {
  background-color: white;
  box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.16), 0 0 0 1px rgba(0, 0, 0, 0.08);
  font-size: 1rem;
  border-radius: 3px;
  border: 0;
  margin-top: 10px;
  width: 70%;
  max-width: 400px;
  height: 40px;
  text-overflow: ellipsis;
  padding: 0 1em;
}

@media (max-width: 400px) {
  #modalSearch {
    left: 20px!important;
  }
}

</style>