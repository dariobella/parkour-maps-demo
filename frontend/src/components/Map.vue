<template>

  <div class="maproot">
    <SpotInfo v-for="spot in spots"
              :spot="spot"
              :spotSelected="spotSelected"
              @closeSpotInfo="spotSelected = 0"
              @editSpotPics="editSpotPics"
              @discardEdit="discardEdit"
              ref="SpotInfo">
    </SpotInfo>

    <div id="map"></div>
    <button @click="$router.push('add-spots')"
            v-if="isAuthenticated && $router.currentRoute.value.name === 'Home'"
            type="button" id="addBtn"
    >
      <span>+</span>
    </button>


    <div class="modal fade" id="deleteSpotModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-body">
            <div class="modalText">Are you sure you want to delete this spot?</div>
            <div class="modalBtns">
              <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">No</button>
              <button type="button" class="btn btn-danger" data-bs-dismiss="modal" @click="deleteSpot()">Yes</button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editPicsModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-body">
            <div class="editPicsTop">
              <h3>Manage {{ editSpot }} images</h3>
              <button>
                <span class="material-icons" data-bs-dismiss="modal">close</span>
              </button>
            </div>
              <div class="divBtn">
                <button class="btn btn-dark" @click="$refs.addPics.click()">Add Images</button>
                <input type="file" name="addPics" id="addPics" ref="addPics" @change="addPicsChanged" multiple>
              </div>

            <div class="imageList">
              <div v-for="pic in spotPics" class="image">
                <div v-if="!deletePics.includes(pic.id)">
                  <img :src="'http://127.0.0.1:8000' + pic.image" alt="">
                </div>
                <button v-if="!deletePics.includes(pic.id)" @click="deleteSpotPic(pic.id)"> <span class="material-icons">delete</span> </button>
              </div>
              <div v-for="(pic, i) in addPics" :key="i" class="image">
                <div>
                  <img :src="addPicUrl(i)" alt="">
                </div>
                <button @click="deleteAddPic(i)"> <span class="material-icons">delete</span> </button>
              </div>
            </div>
            <div class="divBtn submit"><button @click.prevent="submitEdit" class="btn btn-success" data-bs-dismiss="modal">Submit</button></div>
          </div>
        </div>
      </div>
    </div>


  </div>

</template>


<script>

import { Modal } from 'bootstrap'
import {mapState, mapStores} from 'pinia';

import SpotInfo from "@/components/SpotInfo.vue";
import { useMapStore } from "@/stores/MapStore";
import { useUserStore } from "@/stores/UserStore";

export default {
  name: Map,

  components: {
    SpotInfo
  },

  computed: {
    ...mapState(useMapStore, ['spots']),
    ...mapState(useUserStore, ['isAuthenticated']),
    ...mapStores(useMapStore),
  },

  data() {
    return {
      spotSelected: 0,
      map: {},
      markers: [],
      iconSize: {},
      searchWindow: {},
      editSpotId: 0,
      editSpot: '',
      spotPics: [],
      deletePics: [],
      addPics: [],
    }
  },

  mounted() {
    this.markers = []
    this.initMap()
  },

  watch: {
    spots: function () {
      this.loadSpots()
    }
  },


  methods: {

    initMap() {
      this.iconSize = new google.maps.Size(20, 30); // (width, height)
      const krk = {lat:50.0646501, lng:19.9449799};
      const bounds = {
        north: 85,
        south: -85,
        west: -200,
        east: 200,
      }

      var options = {
        zoom: 12,
        center: krk,
        restriction: {
          latLngBounds: bounds,
          strictBounds: false,
        },
        minZoom: 3,
        mapTypeControl: true,
        mapTypeControlOptions: {
          style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
          position: google.maps.ControlPosition.LEFT_BOTTOM,
        },
      };

      this.map = new google.maps.Map(document.getElementById('map'), options);

      var search = document.createElement('input')
      search.id = 'search'
      search.type = 'text'
      search.placeholder = 'Search places'
      this.map.controls[google.maps.ControlPosition.TOP_CENTER].push(search);

      var addBtn = document.getElementById('addBtn')
      this.map.controls[google.maps.ControlPosition.BOTTOM_CENTER].push(addBtn);

      var autocomplete = new google.maps.places.Autocomplete(search);
      autocomplete.bindTo('bounds', this.map);
      autocomplete.setFields(['place_id', 'name', 'geometry', 'formatted_address']);

      var searchMarker = new google.maps.Marker({
        map: this.map,
      });
      this.searchWindow = new google.maps.InfoWindow();

      var vm = this;
      autocomplete.addListener('place_changed', function() {

        var place = autocomplete.getPlace();

        if (!place.geometry) {
          search.placeholder = 'Enter a place';
          searchMarker.setPosition();
          vm.searchWindow.close();
        } else {
          var bounds = new google.maps.LatLngBounds();

          var placeInfo = "<b>" + place.name + "</b> <br>" + place.formatted_address + '<br> <br> <a href="https://www.google.com/maps/search/?api=1&query='+ place.geometry.location.lat() +'%2C'+ place.geometry.location.lng() + '&query_place_id=' + place.place_id + '" target="_blank" >Visualizza su Google Maps</a>';


          searchMarker.setPosition(place.geometry.location);
          vm.searchWindow.setContent(placeInfo);
          vm.searchWindow.setOptions({maxWidth: 200});
          vm.searchWindow.open({
            anchor: searchMarker,
            map: vm.map,
          });

          searchMarker.addListener('click', function() {
            vm.searchWindow.open({
              anchor: searchMarker,
              map: vm.map,
            });
          });

          // adatto la mappa visibile alla posizione del risultato della ricerca
          if (place.geometry.viewport) {
            bounds.union(place.geometry.viewport);
          } else {
            bounds.extend(place.geometry.location);
          }
          vm.map.fitBounds(bounds);
        }
      });

    },

    addMarker(m) {
      var marker = new google.maps.Marker({
        position: m.position,
        map: this.map,
      });

      
      if (m.icon) {
        var icon = {
          url: m.icon,
          scaledSize: this.iconSize,
        }
        marker.setIcon(icon);
      }

      var vm = this

      marker.addListener("click", function () {
        vm.spotSelected = m.id;
        document.getElementById('search').placeholder = 'Search places';
        vm.searchWindow.close();
      });

      this.markers.push(marker)
    },

    clearMarkers() {
      this.markers.forEach((marker) => {
        marker.setVisible(false);
      })
      this.markers = []
    },

    loadSpots() {
      this.clearMarkers()
      let vm = this;
      for (var spot of JSON.parse(JSON.stringify(vm.spots))) {
        var i = ""
        if (spot.type === 'U') i = "https://i.ibb.co/LZQWkQB/bluePin.png"
        else if (spot.type === 'P') i = "https://i.ibb.co/VBtTnMG/orange-Pin.png"
        else if (spot.type === 'G') i = "https://i.ibb.co/cXdG8Dv/purple-Pin.png"
        else i = "https://i.ibb.co/CWLrJK6/redPin.png"
        vm.addMarker({
          id: spot.id,
          position: {lat: spot.lat, lng: spot.lng},
          icon: i,
        });
      }
    },

    async deleteSpot() {
      await this.mapStore.deleteSpot(this.spotSelected)
      this.spotSelected = 0;
      if (this.$router.currentRoute.value.name === 'Home') this.mapStore.loadSpots()
      else if (this.$router.currentRoute.value.name === 'Map') this.mapStore.loadMap(this.$route.params.id)
    },


    editSpotPics(id, spot, pics) {
      this.editSpotId = id
      this.editSpot = spot
      this.spotPics = pics
      const modal = new Modal('#editPicsModal')
      modal.toggle()
    },

    addPicsChanged() {
      for (let i = 0; i < this.$refs.addPics.files.length; i++) {
        this.addPics.push(this.$refs.addPics.files[i])
      }
    },

    addPicUrl(i) {
      return URL.createObjectURL(this.addPics[i])
    },

    deleteSpotPic(id) {
      this.deletePics.push(id)
    },

    deleteAddPic(i) {
      this.addPics.splice(i, 1)
    },

    discardEdit() {
      this.editSpot = ''
      this.deletePics = []
      this.addPics = []
    },

    async submitEdit() {
      const editData = new FormData()
      if (this.deletePics.length > 0) {
        this.deletePics.forEach(id => {
          editData.append('deletePics', id)
        })
      }

      if (this.addPics.length > 0) {
        this.addPics.forEach(image => {
          editData.append('addPics', image, image.name)
        })
      }

      let e = 0
      for (const v of editData.entries()) {
        e++
      }

      if (e > 0) {
        await this.mapStore.updateSpotPics(this.editSpotId, editData)

        this.deletePics = []
        this.addPics = []
        this.$refs.SpotInfo.forEach((s) => {
          if (s.editing) {
            s.loadPics()
          }
        })

      }
    },
  },

}


</script>


<style>

#map {
  height: 94.1vh;
  text-align: left;
}

.maproot {
  display: grid;
}

.spotInfo, #map {
  grid-area: 1 / 1;
}

#search {
  background-color: white;
  box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.16), 0 0 0 1px rgba(0, 0, 0, 0.08);
  font-size: 1rem;
  border-radius: 3px;
  border: 0;
  margin-top: 10px;
  margin-left: 30px;
  width: 70%;
  max-width: 400px;
  height: 40px;
  text-overflow: ellipsis;
  padding: 0 1em;
}

@media (max-width: 400px) {
  #search {
    left: 20px!important;
  }
}

#addBtn {
  background-color: var(--my-black);
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 4rem; height: 4rem;
  border-radius: 100%;
  margin-bottom: 50px;
  transition: transform .2s ease-in-out;
}

#addBtn:hover {
  transform: scale(1.2);
}

#addBtn span {
  font-size: 3rem;
  font-family: 'Nunito', sans-serif;
}

.spotInfo {
  z-index: 1;
  width: 30%;
}

.modal-body {
  background-color: #f8f8f8;
  border-radius: 10px;
}

.modalText {
  padding: 20px;
}

.modalBtns {
  display: flex;
  justify-content: end;
}

.modalBtns .btn-danger {
  margin-left: 10px;
}

#editPicsModal .modal-body {
  display: flex;
  flex-direction: column;
}
.editPicsTop {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.editPicsTop button, .imageList button {
  background-color: transparent;
  border: none;
  padding: 0;
}
#editPicsModal button span {
  color: var(--my-black);
  padding: 5px;
}
.divBtn {
  display: flex;
  margin: 10px 0;
}
.divBtn.submit {
  margin: 10px 0 0;
  justify-content: flex-end;
}
.image {
  display: flex;
  align-items: center;
}
#editPicsModal .image button span {
  color: red;
  font-size: 2rem;
  padding: 5px;
}
.image div {
  flex-grow: 1;
  padding: 10px 0;
}
.image div img {
  width: 100%;
  height: auto;
}
#addPics {
  display: none;
}

</style>