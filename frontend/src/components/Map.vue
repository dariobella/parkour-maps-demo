<template>

  <div class="maproot">
    <SpotInfo v-for="spot in spots"
              :spot="spot"
              :spotSelected="spotSelected"
              @closeSpotInfo="spotSelected = 0"
              @showSpotPics="showSpotPics"
              @editSpotPics="editSpotPics"
              @discardEdit="discardEdit"
              ref="SpotInfo">
    </SpotInfo>

    <MapInfo v-if="$router.currentRoute.value.name === 'Map'" v-show="spotSelected === 0"
             @selectSpot="selectSpot">
    </MapInfo>

    <div id="map"></div>
    <button @click="this.$router.push({name: 'AddSpots'})"
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

    <div class="modal fade" id="showPicsModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">{{ modalSpot }} images</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div id="showPicsCarousel" class="carousel slide" data-bs-interval="false">
              <div class="carousel-indicators">
                <button v-for="(pic, i) in spotPics"
                        class="carousel-indicator" type="button"
                        :data-bs-slide-to="i"
                        data-bs-target="#showPicsCarousel"
                        :class="{ active : i === 0 }"
                        :aria-current="i === 0 ? 'true' : ''" :aria-label="'Slide ' + i">
                </button>
              </div>
              <div class="carousel-inner">
                <div v-for="(pic, i) in spotPics" class="carousel-item" :class="{ active: i === 0 }">
                  <img :src="'http://127.0.0.1:8000' + pic.image" class="d-block w-100" alt="">
                </div>
              </div>
              <div class="carouselControls" v-if="spotPics.length > 1">
                <button class="carousel-control-prev" type="button" data-bs-target="#showPicsCarousel" data-bs-slide="prev">
                  <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                  <span class="visually-hidden">Previous</span>
                </button>
                <button class="carousel-control-next" type="button" data-bs-target="#showPicsCarousel" data-bs-slide="next">
                  <span class="carousel-control-next-icon" aria-hidden="true"></span>
                  <span class="visually-hidden">Next</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="editPicsModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header bg-dark text-white">
            <h5 class="modal-title">Manage {{ modalSpot }} images</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
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

import { useMapStore } from "@/stores/MapStore";
import { useUserStore } from "@/stores/UserStore";
import SpotInfo from "./SpotInfo.vue";
import MapInfo from "./MapInfo.vue";

export default {
  name: Map,

  components: {
    MapInfo,
    SpotInfo
  },

  computed: {
    ...mapState(useMapStore, ['id', 'name', 'description', 'creator', 'spots']),
    ...mapState(useUserStore, ['isAuthenticated']),
    ...mapStores(useMapStore, useUserStore),
  },

  data() {
    return {
      spotSelected: 0,
      map: {},
      markers: [],
      iconSize: {},
      searchWindow: {},
      editSpotId: 0,
      modalSpot: '',
      spotPics: [],
      deletePics: [],
      addPics: [],
    }
  },

  mounted() {
    this.clearMarkers()
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

      if (this.$router.currentRoute.value.name === 'Home') options.draggableCursor = 'pointer'

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

      if (this.$router.currentRoute.value.name === 'Home') {
        let addSpotMarker = new google.maps.Marker({
          map: this.map
        })

        this.map.addListener("click", (mapsMouseEvent) => {
          addSpotMarker.setVisible(true)
          let position = mapsMouseEvent.latLng
          addSpotMarker.setPosition(position)
          this.userStore.addSpotPosition.lat = position.toJSON().lat.toFixed(6)
          this.userStore.addSpotPosition.lng = position.toJSON().lng.toFixed(6)
        })

        addSpotMarker.addListener('click', () => {
          addSpotMarker.setVisible(false)
          addSpotMarker.setPosition(null)
          this.userStore.addSpotPosition = {}
        })
      }

      autocomplete.addListener('place_changed', () => {

        var place = autocomplete.getPlace();

        if (!place.geometry) {
          search.placeholder = 'Enter a place';
          searchMarker.setPosition();
          this.searchWindow.close();
        } else {
          var bounds = new google.maps.LatLngBounds();

          var placeInfo = "<b>" + place.name + "</b> <br>" + place.formatted_address + '<br> <br> <a href="https://www.google.com/maps/search/?api=1&query='+ place.geometry.location.lat() +'%2C'+ place.geometry.location.lng() + '&query_place_id=' + place.place_id + '" target="_blank" >Visualizza su Google Maps</a>';


          searchMarker.setPosition(place.geometry.location);
          this.searchWindow.setContent(placeInfo);
          this.searchWindow.setOptions({maxWidth: 200});
          this.searchWindow.open({
            anchor: searchMarker,
            map: this.map,
          });

          searchMarker.addListener('click', () => {
            this.searchWindow.open({
              anchor: searchMarker,
              map: this.map,
            });
          });

          // adatto la mappa visibile alla posizione del risultato della ricerca
          if (place.geometry.viewport) {
            bounds.union(place.geometry.viewport);
          } else {
            bounds.extend(place.geometry.location);
          }
          this.map.fitBounds(bounds);
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

      marker.addListener("click", () => {
        this.spotSelected = m.id;
        document.getElementById('search').placeholder = 'Search places';
        this.searchWindow.close();
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
      for (var spot of JSON.parse(JSON.stringify(this.spots))) {
        var i = ""
        if (spot.type === 'U') i = "https://i.ibb.co/LZQWkQB/bluePin.png"
        else if (spot.type === 'P') i = "https://i.ibb.co/VBtTnMG/orange-Pin.png"
        else if (spot.type === 'G') i = "https://i.ibb.co/cXdG8Dv/purple-Pin.png"
        else i = "https://i.ibb.co/CWLrJK6/redPin.png"
        this.addMarker({
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

    showSpotPics(spot, pics) {
      this.modalSpot = spot
      this.spotPics = pics
      const modal = new Modal('#showPicsModal')
      modal.toggle()
    },

    editSpotPics(id, spot, pics) {
      this.editSpotId = id
      this.modalSpot = spot
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
      this.modalSpot = ''
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

    selectSpot(id, lat, lng) {
      this.spotSelected = id
      this.map.setCenter({lat, lng})
      this.map.setZoom(17)
    }
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

.spotInfo, .mapInfo, #map {
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
  margin-bottom: 5px;
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