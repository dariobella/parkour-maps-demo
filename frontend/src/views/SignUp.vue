<template>
    <div class="signup">
        <h1>Sign Up</h1>

        <div class="alert alert-danger" v-if="errors.length">
          <p v-for="error in errors" :key="error">{{ error }}</p>
        </div>

        <form @submit.prevent="submitForm">
            <input type="text" name="username" v-model="username" placeholder="username">
            <input type="email" name="email" v-model="email" placeholder="email">
            <input type="password" name="password" v-model="password" placeholder="password">
            <input type="password" name="confPassword" v-model="confPassword" placeholder="confirm password">
            <button type="submit">Sign Up</button>
        </form>

        <div>Already have an account? <router-link to="/login">Login</router-link></div>
    </div>
</template>

<script>

import axios from 'axios'
import { mapStores } from 'pinia';
import { useUserStore } from "@/stores/UserStore";

export default {
  name: 'SignUp',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confPassword: '',
      lastId: 0,
      errors: []
    }
  },
  computed: {
    ...mapStores(useUserStore)
  },
  mounted() {
    document.title = this.userStore.title + ' | Sign Up'
  },
  methods: {
    submitForm() {
      this.errors = []

      if (this.username === '') this.errors.push('The username is missing')
      else if (this.password === '') this.errors.push('The password is too short')
      else if (this.password !== this.confPassword) this.errors.push('The passwords do not match')

      if (!this.errors.length) {
        const formData = {
          username: this.username,
          email: this.email,
          password: this.password,
        }

        this.userStore.addMyUser(formData)

      }
    }
  }
}
</script>

<style>
.signup {
  margin-top: 10vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.signup form {
  width: 30%;
  min-width: 300px;
  display: flex;
  flex-direction: column;
}

.signup form button {
  align-self: flex-end;
  width: 100px;
}

</style>