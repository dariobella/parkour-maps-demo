<template>

  <nav class="navbar navbar-expand-md navbar-dark bg-dark">
    <div class="container-fluid">
      <div class="collapse navbar-collapse order-md-1 order-3" id="navbarSupportedContent">
        <div v-if="name" class="currentMap">Current map: {{mapName}}</div>
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
import { mapState } from 'pinia';
import { useUserStore } from "@/stores/UserStore";
import { useMapStore } from "@/stores/MapStore";
import { useGlobalStore } from "@/stores/GlobalStore";

export default {
  name: 'Navbar',
  computed: {
    ...mapState(useGlobalStore, ['title']),
    ...mapState(useUserStore, ['user', 'isAuthenticated']),
    ...mapState(useMapStore, ['name', 'creator']),
    mapName () {
      let n = ''
      if (this.creator.id === this.user.id) n = this.name
      else if (this.name === 'Added by me') n = `Added by ${this.creator.username}`
      else n = `${this.creator.username}'s ${this.name}`
      return n
    }
  },
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

