<template>
    <div>
        <h1>Sign Up :)</h1>

        <form @submit.prevent="submitForm">
            <input type="text" name="username" v-model="username" placeholder="username">
            <input type="email" name="email" v-model="email" placeholder="email">
            <input type="password" name="password" v-model="password" placeholder="password">
            <button type="submit">Sign Up</button>
        </form>
    </div>
</template>

<script>

import axios from 'axios'

export default {
    name: 'SignUp',
    data() {
        return {
            username: '',
            email: '',
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
                .post('/api/v1/users/', formData)
                .then(response => {

                    this.$router.push('/log-in')
                    console.log(response)
                })
                .catch(error => {
                    console.log(error)
                })
        }
    }
}
</script>