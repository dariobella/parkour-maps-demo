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
        <form @submit.prevent="spotSubmitForm">
          <div class="selectLocation">
            <div class="choose">
              <span>Location:</span> <button @click="selectLocation()">Choose from map</button>
            </div>
            <div class="LatLng">
              <label for="Lat">Lat:</label> <input type="number" name="Lat" id="Lat">
              <label for="Lat">Lng:</label> <input type="number" name="Lat" id="Lng">
            </div>
            
          </div>

          <div class="name">
            <label for="name">Name:</label> <input type="text" name="name" id="name">
          </div>
        
          <button class="btn-success" type="submit">Add spots</button>
        </form>
      </div>

      <div class="tab-kml" v-show="current == 2">
        <form @submit.prevent="kmlSubmitForm">
        
          <button class="btn-success" type="submit">Add spots</button>
        </form>
      </div>
    </div>
  </div>
  
</template>

<script>
export default {
  name: 'AddSpots',
  data() {
    return {
      current: 1,
    }
  },
  mounted() {
    document.title = 'PK SPOT MAP | Add Spots'
  },
  methods: {
    spotSubmitForm() {
      console.log('spot submit form')
    },
    kmlSubmitForm() {
      console.log('kml submit form')
    },    
    selectLocation() {
      console.log('select location')
    }
  }
  
}
</script>

<style>

.addSpots {
  margin: 3em;
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

</style>