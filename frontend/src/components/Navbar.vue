<template>

  <nav class="navbar navbar-expand-md navbar-dark bg-dark">
    <div class="container-fluid">
      <div class="collapse navbar-collapse order-md-1 order-3" id="navbarSupportedContent">
        <div v-if="isAuthenticated && ['Home', 'Map'].includes($router.currentRoute.value.name)" class="selectMap dropdown">
          <button type="button" class="btn btn-light dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" v-if="$router.currentRoute.value.name === 'Home'"> Home </button>
          <button type="button" class="btn btn-light dropdown-toggle" data-bs-toggle="dropdown" aria-expanded="false" v-else> {{ mapName({name, creator}) }} </button>
          <ul class="dropdown-menu">
            <li> <router-link class="dropdown-item" to="/">Home</router-link> </li>
            <li> <router-link class="dropdown-item" :to="`/map/${map.id}`" v-for="map in maps">{{ mapName(map) }}</router-link> </li>
          </ul>
        </div>
      </div>
      <router-link class="navbar-brand order-1" to="/"> {{ title }} </router-link>
      <button class="navbar-toggler order-2" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse order-md-3 order-4" id="navbarSupportedContent">
        <ul class="navbar-nav ms-auto">
          <template v-if="isAuthenticated">
            <li class="nav-item">
              <router-link class="nav-link" :class="{'active': $router.currentRoute.value.name === 'MyProfile'}" to="/my-profile">Profile</router-link>
            </li>
          </template>
          
          <template v-else>
            <li class="nav-item">
              <router-link class="nav-link" :class="{'active': $router.currentRoute.value.name === 'Login'}" to="/login">Login</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" :class="{'active': $router.currentRoute.value.name === 'SignUp'}" to="/sign-up">Sign Up</router-link>
            </li>
          </template>
        </ul>
      </div>
    </div>
  </nav>

</template>

<script>
import { mapState, mapStores } from 'pinia';
import { useUserStore } from "@/stores/UserStore";
import { useMapStore } from "@/stores/MapStore";
import { useGlobalStore } from "@/stores/GlobalStore";

export default {
  name: 'Navbar',
  computed: {
    ...mapState(useGlobalStore, ['title']),
    ...mapState(useUserStore, ['user', 'isAuthenticated', 'maps']),
    ...mapState(useMapStore, ['name', 'creator']),
    ...mapStores(useMapStore),
  },

  data() {
    return {

    }
  },

  methods: {
    mapName (map) {
      let n = ''
      if (map) {
        if (map.creator.id === this.user.id) n = map.name
        else if (map.name === 'Added by me') n = `Added by ${map.creator.username}`
        else n = `${map.creator.username}'s ${map.name}`
      }
      return n
    },
  }
}

</script>

<style scoped>

@media (min-width: 768px) {
  .navbar-expand-md .navbar-collapse {
    width: 100%;
  }
}

.logo-link {
    color: white;
    text-decoration: none;
}

.currentMap {
  background-color: white;
  border-radius: 5px;
  padding: 5px 10px;
}

</style>

