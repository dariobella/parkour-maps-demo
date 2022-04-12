import { createRouter, createWebHistory } from 'vue-router'

import store from '../store'

import Login from '../views/Login.vue'
import SignUp from '../views/SignUp.vue'
import Spots from '../views/Spots.vue'
import Home from '../views/Home.vue'
import Profile from '../views/Profile.vue'
import AddSpots from '../views/AddSpots.vue'

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
    path: '/spots',
    name: 'Spots',
    component: Spots
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      requireLogin: true
    }
  },
  {
    path: '/add-spots',
    name: 'AddSpots',
    component: AddSpots,
    meta: {
      requireLogin: true
    }
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
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
