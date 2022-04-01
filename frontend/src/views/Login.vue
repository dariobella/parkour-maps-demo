<template>
    <div>
        <h1>Login :)</h1>

        <form @submit.prevent="submitForm">
            <input type="text" name="username" v-model="username" placeholder="username">
            <input type="password" name="password" v-model="password" placeholder="password">
            <button type="submit">Login</button>
        </form>
    </div>
</template>

<script>

import axios from 'axios'

export default {
    name: 'Login',
    data() {
        return {
            username: '',
            password: '',
        }
    },
    methods: {
        submitForm(e) {
            const formData = {
                username: this.username,
                email: this.email,
                password: this.password,
            }

            axios
                .post('/api/v1/token/login', formData)
                .then(response => {
                    console.log(response)

                    const token = response.data.auth_token
                    this.$store.commit('setToken', token)

                    axios.defaults.headers.common['Authorization'] = "Token " + token

                    localStorage.setItem('token', token);
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>