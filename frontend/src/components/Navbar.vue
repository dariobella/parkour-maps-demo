<template>

  <nav class="navbar navbar-expand-md navbar-dark bg-dark">
    <div class="container-fluid">
      <div class="collapse navbar-collapse order-md-1 order-3" id="navbarSupportedContent">
        <div v-if="['Home', 'Map'].includes($router.currentRoute.value.name)" class="selectMap dropdown">
          <button class="dropBtn" :class="isAuthenticated ? 'hoverable' : ''" v-if="$router.currentRoute.value.name === 'Home'"> Home </button>
          <button class="dropBtn" :class="isAuthenticated ? 'hoverable' : ''" v-else> {{ mapName({name, creator}) }} </button>
          <div v-if="isAuthenticated" class="dropdown-content">
            <router-link class="dropdown-item" to="/">Home</router-link>
            <router-link v-for="map in maps" class="dropdown-item" :to="`/map/${map.id}`">{{ mapName(map) }}</router-link>
          </div>
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
    ...mapState(useMapStore, ['id', 'name', 'creator']),
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

.dropBtn {
  background-color: #f8f8f8;
  color: var(--my-black);
  border: none;
  border-radius: 5px;
  padding: 8px 10px;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  min-width: 100%;
  background-color: #f1f1f1;
  box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
  z-index: 3;
}

.dropdown-content a {
  color: var(--my-black);
  text-align: left;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {background-color: #ddd;}

.dropdown:hover .dropdown-content {display: block;}

.dropdown:hover .dropBtn {
  transform: none;
  cursor: default;
}

.dropdown:hover .dropBtn.hoverable {
  background-color: #e1e1e1;
  border-radius: 5px 5px 0 0;
  cursor: pointer;
}

.dropdown-item.router-link-active {
  display: none;
}

</style>

