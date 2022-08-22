import { defineStore } from 'pinia'

export const useGlobalStore = defineStore("global", {

  state: () => ({
    title: 'Parkour Maps',
    toast: {
      content: {
        title: '',
        description: '',
      },
      options: {
        timeout: 4000,
        hideProgressBar: true,
        showIcon: true,
        position: 'bottom-right',
        type: 'info',
        transition: 'slide',
      }
    },

  }),

  getters: {},

  actions: {

    setToast(c, o = {}) {
      this.toast = {
        content: {
          ...this.toast.content,
          ...c,
        },
        options: {
          ...this.toast.options,
          ...o,
        }
      }
    },

  }

})

