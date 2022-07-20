import { createRouter, createWebHistory } from 'vue-router'

import store from '../store'

import Login from '../views/Login.vue'
import SignUp from '../views/SignUp.vue'
import Home from '../views/Home.vue'
import Profile from '../views/Profile.vue'
import AddSpots from '../views/AddSpots.vue'
import MapView from '../views/MapView.vue';
import MyProfile from "../views/MyProfile.vue";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/sign-up',
    name: 'SignUp',
    component: SignUp
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/my-profile',
    name: 'MyProfile',
    component: MyProfile,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/map/:id',
    name: 'Map',
    component: MapView,
  },
  {
    path: '/add-spots',
    name: 'AddSpots',
    component: AddSpots,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/profile/:id',
    name: 'Profile',
    component: Profile,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  if (to.matched.some(record => record.meta.requireLogin) && !store.state.isAuthenticated) {
    next({ name: 'Login', query: { to: to.path } });
  } else {
    next()
  }
})

export default router
