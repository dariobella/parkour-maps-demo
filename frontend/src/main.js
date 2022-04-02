import { createApp } from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css'

createApp(App).use(router, axios, store).mount('#app')

import 'bootstrap/dist/js/bootstrap.js'

