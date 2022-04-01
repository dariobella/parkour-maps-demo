<script>

import { axiosAPI } from '../axios-api'

export default {
  name: Map,

  data() {
    return {
      APIData: [],
      map: {},
      iconSize: {},
      infoWindow: {},
      searchWindow: {}
    }
  },


  created () {
    axiosAPI.get('/api/spots/',)
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

    initMap: function() {
      this.iconSize = new google.maps.Size(20, 30); // (width, height)
      const lonato = {lat:45.4609, lng:10.4845};

      var options = {zoom: 12, center: lonato};
      this.map = new google.maps.Map(document.getElementById('map'), options);


      this.infoWindow = new google.maps.InfoWindow();

      var search = document.createElement('input');
      search.id = 'search';
      search.type = 'text';
      search.placeholder = 'Search places';
      this.map.controls[google.maps.ControlPosition.TOP_CENTER].push(search);
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
          document.getElementById('search').placeholder = 'Enter a place';
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

    addMarker: function(m) {
      var marker = new google.maps.Marker({
        position: m.position,
        map: this.map,
      });

      if (m.icon) {
        marker.setIcon(m.icon);
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

    loadSpots: function() {
      var vm = this;
      for (var spot of JSON.parse(JSON.stringify(vm.APIData))) {
        vm.addMarker({
          position: {lat: spot.lat, lng: spot.lng},
          info: "<b>" + spot.name + "</b> <br>" + spot.type + '<br> <br> <a href="https://www.google.com/maps/search/?api=1&query='+ spot.lat +'%2C'+ spot.lng + '" target="_blank" >Visualizza su Google Maps</a>',
          //icon: '../assets/redPin.png'
        });
      }
    },
  },

}


</script>


<template>

  <div id="map"></div>

</template>


<style>


#search {
  background-color: white;
  box-shadow: 0 2px 2px 0 rgba(0, 0, 0, 0.16), 0 0 0 1px rgba(0, 0, 0, 0.08);
  font-size: 1rem;
  border-radius: 3px;
  border: 0;
  margin-top: 10px;
  width: 400px;
  height: 40px;
  text-overflow: ellipsis;
  padding: 0 1em;
}

</style>