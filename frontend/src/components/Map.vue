<template>

  <div class="maproot">
    <SpotInfo v-for="spot in spots" :spot="spot" :spotSelected="spotSelected"></SpotInfo>
    <div id="map" :class="mapClass"></div>
    <button @click="$router.push('add-spots')" type="button" id="addBtn" v-if="isAuthenticated && $router.currentRoute.value.name === 'Home'">
      <span>+</span>
    </button>
  </div>

</template>


<script>

import SpotInfo from "@/components/SpotInfo.vue";
import { mapState } from 'pinia';
import { useMapStore } from "@/stores/MapStore";
import { useUserStore } from "@/stores/UserStore";

export default {
  name: Map,

  components: {
    SpotInfo
  },

  computed: {
    mapClass () {
      return this.$router.currentRoute.value.name === 'Map' ? 'vh-89' : 'vh-94'
    },
    ...mapState(useMapStore, ['spots']),
    ...mapState(useUserStore, ['isAuthenticated'])
  },

  data() {
    return {
      spotSelected: 0,
      map: {},
      iconSize: {},
      searchWindow: {},
    }
  },

  mounted() {
    this.initMap()
  },

  watch: {
    spots() {
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

      var offset = new google.maps.Size(0, 0);
      marker.addListener("click", function () {
        vm.spotSelected = m.id;
        document.getElementById('search').placeholder = 'Search places';
        vm.searchWindow.close();
      });
    },

    loadSpots() {
      var vm = this;
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
  },

}


</script>


<style>

.maproot {
  display: grid;
}

.spotInfo, #map {
  grid-area: 1 / 1;
}

.vh-89 {
  height: 89.4vh;
  text-align: left;
}

.vh-94 {
  height: 94.1vh;
  text-align: left;
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

</style>