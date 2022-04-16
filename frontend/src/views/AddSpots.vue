<template>

  <div class="addSpots">

    <h1>Add Spots</h1>

    <ul class="nav nav-tabs">
      <li class="nav-item">
        <a href="#" class="nav-link" :class="{'active': current == 1}" @click.prevent="this.current = 1">Add Spot</a>
      </li>
      <li class="nav-item">
        <a href="#" class="nav-link" :class="{'active': current == 2}" @click.prevent="this.current = 2">Import KML file</a>
      </li>
    </ul>

    <div class="tab-content">
      <div class="tab-spot" v-show="current == 1">

        <div class="alert alert-danger" v-if="errors.length">
          <p v-for="error in errors" :key="error">{{ error }}</p>
        </div>

        <form @submit.prevent="spotSubmitForm">
          <div class="selectLocation">
            <div class="choose">
              <span>Location:</span> <button @click.prevent="initMapModal()" data-bs-toggle="modal" data-bs-target="#locationModal">Choose from map</button>
            </div>
            <div class="LatLng">
              <label for="Lat">Lat:</label> <input type="number" name="Lat" id="Lat" v-model="lat" step="0.000001">
              <label for="Lat">Lng:</label> <input type="number" name="Lat" id="Lng" v-model="lng" step="0.000001">
            </div>
            
          </div>

          <div class="name">
            <label for="name">Name:</label> <input type="text" name="name" id="name" v-model="name">
          </div>

          <div class="type">
            <label for="type">Type:</label>
            <select name="type" id="type" v-model="type">
              <option value="spot">Spot</option>
              <option value="gym">Gym</option>
              <option value="park">Parkour Park</option>
              <option value="undercover">Undercover spot</option>
            </select>
          </div>

          <div class="description">
            <label for="description">Description:</label>
            <textarea name="description" id="description" v-model="description"></textarea>
          </div>
        
          <button class="btn-success" type="submit">Add spots</button>
        </form>



      </div>

      <div class="tab-kml" v-show="current == 2">
        <form @submit.prevent="kmlSubmitForm" enctype="multipart/form-data">
          <div class="file">
            <label for="kmlFile">Upload file</label>
            <input type="file" accept=".kml" name="kmlFile" id="kmlFile" ref="kmlFile" @change="fileSelected">
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

import axios from 'axios'

export default {
  name: 'AddSpots',
  data() {
    return {
      current: 1,
      map: {},
      iconSize: {},
      marker: {},
      lat: 0,
      lng: 0,
      name: '',
      type: '',
      description: '',
      kmlFile : {},
      errors: []
    }
  },
  mounted() {
    document.title = 'PK SPOT MAP | Add Spots'
  },
  methods: {
    spotSubmitForm() {
      this.errors = []

      if (this.lat === 0 && this.lng  === 0) {
        this.errors.push('The coordinates are missing')
      }
      else if (this.name === '') this.errors.push('The name is missing')

      if (!this.errors.length) {
        const formData = {
          lat: this.lat,
          lng: this.lng,
          name: this.name,
          type: this.type,
          description: this.description,
        }

        axios
        .post('/api/addSpot/', formData)
        .then(response => {
          this.$router.push('/')
          console.log(response)
        })
        .catch(error => {
          this.errors.push('Something went wrong, please try again')
          console.log(JSON.stringify(error))
        })

      }
    },

    initMapModal() {
      var location = {lat:45.4609, lng:10.4845};
      var options = {
        center: location,
        zoom: 12,
        minZoom: 3,
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
      
      var autocomplete = new google.maps.places.Autocomplete(modalSearch)
      autocomplete.bindTo('bounds', this.map)
      autocomplete.setFields(['place_id', 'name', 'geometry', 'formatted_address'])

      var vm = this
      autocomplete.addListener('place_changed', function() {

        var place = autocomplete.getPlace();

        if (!place.geometry) {
          modalSearch.placeholder = 'Enter a place'
        } else {
          var bounds = new google.maps.LatLngBounds()

          vm.marker.setPosition(place.geometry.location)

          // adatto la mappa visibile alla posizione del risultato della ricerca
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
      const tj = require("@tmcw/togeojson")
      const fs = require("fs")
      const DOMParser = require("xmldom").DOMParser
      const kml = new DOMParser().parseFromString(fs.readFileSync(this.kmlFile, "utf8"))

      const converted = tj.kml(kml)
      console.log(converted)
    },

    fileSelected() {
      this.kmlFile = this.$refs.kmlFile.files[0]
      console.log(this.kmlFile)
    }
  }
  
}
</script>

<style>

.addSpots {
  margin: 3rem;
  min-width: 290px;
}

.addSpots h1, .addSpots button {
  margin: 1em;
}

.addSpots label {
  margin-left: 1em;
  margin-right: 0.5em;
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
  align-items: baseline;
  justify-content: center;
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