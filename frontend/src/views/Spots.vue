<template>
    <div class="spots">
        <h1>Look at my spots :)</h1>
    </div>

    <ul>
        <div v-for="spots in APIData" :key="spots.id">
            
            <li>#{{spots.id}} - LatLng: { {{spots.lat}}, {{spots.lng}} }, Nome: {{ spots.name }}, Tipo: {{spots.type}} </li>

        </div>
    </ul>
</template>

<script>
import { axiosAPI } from '../axios-api'

export default {
    data() {
        return {
            APIData: []
        }
    },
    created () {
        axiosAPI.get('/api/spots/',)
            .then(response => {
                console.log('Here\'s the data')
                this.APIData = response.data
            })
            .catch(err => {
                console.log(err)
            })
    }
}
</script>