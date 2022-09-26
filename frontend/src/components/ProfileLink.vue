<template>
  <router-link :to="`/profile/${id}`" class="profileLink">
    <img :src="profilePictureURL">{{ username }}
  </router-link>
</template>

<script>
import {mapStores} from "pinia";
import {useUserStore} from "@/stores/UserStore";

export default {
  name: "ProfileLink",

  props: {
    id: Number,
    username: String,
  },

  computed: {
    profilePictureURL() {
      return this.profilePicture ? `http://127.0.0.1:8000${this.profilePicture}` : '/src/assets/profile-placeholder.png'
    },
    ...mapStores(useUserStore),
  },

  data () {
    return {
      profilePicture: '',
    }
  },

  mounted() {
    if (this.id) this.getProfilePicture()
  },

  beforeUpdate() {
    this.getProfilePicture()
  },

  methods: {
    getProfilePicture() {
      this.userStore.getProfilePicture(this.id)
        .then((response) => {
          console.log(response)
          this.profilePicture = response.data.profilePicture
        })
        .catch((error) => {
          console.log(error)
        })
    }
  }
}
</script>

<style scoped>

.profileLink {
  text-decoration: none;
  color: var(--my-black);
}

.profileLink img {
  border-radius: 100%;
  height: 1.5rem;
  aspect-ratio: 1;
  margin-inline: 5px;
}

</style>