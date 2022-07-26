<template>
    <div class="login">
      
      <h1>Login</h1>

      <div class="alert alert-danger" v-if="errors.length">
        <p v-for="error in errors" :key="error">{{ error }}</p>
      </div>

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
import { mapStores } from 'pinia';
import { useUserStore } from "@/stores/UserStore";

export default {
    name: 'Login',
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    computed: {
      ...mapStores(useUserStore)
    },
    mounted() {
      document.title = this.userStore.title + ' | Login'
    },
    methods: {
      async submitForm() {
        this.errors = []
        axios.defaults.headers.common["Authorization"] = ""
        localStorage.removeItem("token")

        const formData = {
          username: this.username,
          password: this.password,
        }

        await this.userStore.login(formData)

        if (this.userStore.isAuthenticated) this.$router.push({name: 'Home'})

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