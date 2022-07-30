import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from '@/App.vue'
import router from '@/router'
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css'

const pinia = createPinia()
axios.defaults.baseURL = 'http://127.0.0.1:8000'

createApp(App).use(pinia).use(router, axios).mount('#app')

import 'bootstrap/dist/js/bootstrap.js'

