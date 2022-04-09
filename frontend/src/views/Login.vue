<template>
    <div class="login">
      
      <h1>Login</h1>

      <form @submit.prevent="submitForm">
          <input type="text" name="username" v-model="username" placeholder="username">
          <input type="password" name="password" v-model="password" placeholder="password">
          <button type="submit">Login</button>
      </form>

      <div>New here? <router-link to="/sign-up">Sign up</router-link></div>
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
            errors: []
        }
    },
    mounted() {
      document.title = 'PKSPOTMAP | Login'
    },
    methods: {
      async submitForm() {
        axios.defaults.headers.common["Authorization"] = ""

        localStorage.removeItem("token")

        const formData = {
          username: this.username,
          password: this.password,
        }

        await axios
          .post('/api/v1/token/login', formData)
          .then(response => {
              const token = response.data.auth_token
              this.$store.commit('setToken', token)

              axios.defaults.headers.common['Authorization'] = "Token " + token

              localStorage.setItem('token', token)

              this.$router.push('/')
          })
          .catch(error => {
            if (error.response) {
              for (const property in error.response.data) {
                this.errors.push(`${property}: ${error.response.data[property]}`)
              }

              console.log(JSON.stringify(error.response.data))
            } else if (error.message) {
              this.errors.push('Something went wrong, please try again')
            
              console.log(JSON.stringify(error))
            }
          })
      }
    }
}
</script>

<style>

.login {
  margin-top: 10vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.login form {
  width: 30%;
  min-width: 300px;
  display: flex;
  flex-direction: column;
}

.login form button {
  align-self: flex-end;
  width: 100px;
}

</style>