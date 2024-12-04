import { defineStore } from 'pinia'

export const useErrorStore = defineStore('error', {
  state: () => ({
    errorMessage: null,
  }),
  actions: {
    setError(message) {
      this.errorMessage = message
    },
    clearError() {
      this.errorMessage = null
    },
  },
})
