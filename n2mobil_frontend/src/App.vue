<template>
  <div id="app">
    <main class="p-0">
      <ErrorAlert />
      <router-view />
    </main>
  </div>
</template>

<script>
import ErrorAlert from './components/ErrorAlert.vue'

export default {
  name: 'App',
  components: {
    ErrorAlert,
  },
}
</script>
