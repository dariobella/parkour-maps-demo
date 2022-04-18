<script>

import axios from 'axios'
import App from '../App.vue'

export default {
  components: { App },
  name: Map,

  data() {
    return {
      APIData: [],
      map: {},
      iconSize: {},
      infoWindow: {},
      searchWindow: {},
    }
  },


  created () {
    axios
      .get('/api/spots/',)
      .then(response => {
        console.log('API data retrieved')
        this.APIData = response.data
      })
      .then(load => {
        this.loadSpots()
      })
    .catch(err => {
        console.log(err)
    })
  },


  mounted() {

    this.initMap()

  },


  methods: {

    initMap() {
      this.iconSize = new google.maps.Size(20, 30); // (width, height)
      const lonato = {lat:45.4609, lng:10.4845};

      var options = {
        zoom: 12, 
        center: lonato, 
        minZoom: 3,
        mapTypeControl: true,
        mapTypeControlOptions: {
          style: google.maps.MapTypeControlStyle.HORIZONTAL_BAR,
          position: google.maps.ControlPosition.LEFT_BOTTOM,
        },
      };

      this.map = new google.maps.Map(document.getElementById('map'), options);
      this.infoWindow = new google.maps.InfoWindow();

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
          vm.infoWindow.close();

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
        vm.infoWindow.setContent(m.info);
        vm.infoWindow.setOptions({maxWidth: m.maxWidth, pixelOffset: offset});
        vm.infoWindow.open({
          anchor: marker,
          map: vm.map,
        });
        document.getElementById('search').placeholder = 'Enter a place';
        vm.searchWindow.close();
      });
    },

    loadSpots() {
      var vm = this;
      for (var spot of JSON.parse(JSON.stringify(vm.APIData))) {
        vm.addMarker({
          position: {lat: spot.lat, lng: spot.lng},
          info: "<b>" + spot.name + "</b> <br>" + spot.type + "<br> <br>" + spot.description + "<br>" + ' <br> <a href="https://www.google.com/maps/search/?api=1&query='+ spot.lat +'%2C'+ spot.lng + '" target="_blank" >Visualizza su Google Maps</a>',
          icon: "https://i.ibb.co/ZddWhrd/redPin.png",
          maxWidth: 250,
        });
      }
    },
  },

}


</script>


<template>

  <div class="maproot">
    <div id="map"></div>
    <button @click="$router.push('add-spots')" type="button" id="addBtn" v-if="$store.state.isAuthenticated">
      <span>+</span>
    </button>
  </div>
  
</template>


<style>

#map {
  height: 94vh;
  text-align: left;
}

#search {
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
  #search {
    left: 20px!important;
  }
}

#addBtn {
  background-color: #212529;
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

</style>