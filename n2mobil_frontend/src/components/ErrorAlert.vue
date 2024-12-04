<template>
  <div
    v-if="errorMessage"
    class="fixed top-4 left-1/2 transform -translate-x-1/2 bg-red-500 text-white px-6 py-3 rounded-md shadow-lg z-50"
  >
    <div class="flex justify-between items-center">
      <span>{{ errorMessage }}</span>
      <button @click="clearError" class="ml-4 bg-white text-red-500 px-2 py-1 rounded">
        Kapat
      </button>
    </div>
  </div>
</template>

<script>
import { useErrorStore } from '../stores/errorStore'

export default {
  name: 'ErrorAlert',
  setup() {
    const errorStore = useErrorStore()

    return {
      errorMessage: errorStore.errorMessage,
      clearError: errorStore.clearError,
    }
  },
}
</script>
