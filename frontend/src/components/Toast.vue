<template>
  <button ref="toastRef" @click="toast" hidden></button>
</template>

<script setup>
import { ref } from "vue";
import { createToast } from 'mosha-vue-toastify';

import 'mosha-vue-toastify/dist/style.css';
import { useGlobalStore } from "@/stores/GlobalStore";

const store = useGlobalStore()
const toastRef = ref()

store.$subscribe((mutation, state) => {
  if (mutation.events.key === 'toast') {
    toastRef.value.click()
  }
})

function toast () {
  createToast(store.toast.content, store.toast.options)
}
</script>

<style>

.mosha__toast__content__text {
  font-family: 'Nunito', sans-serif;
}

</style>