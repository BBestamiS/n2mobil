<template>
  <div class="container mx-auto">
    <h1 class="text-2xl font-bold mb-4">Kullanıcı Listesi</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <div
        v-for="user in users"
        :key="user.id"
        class="p-4 border rounded-lg shadow hover:bg-gray-100 cursor-pointer"
        @click="goToUserDetails(user.id)"
      >
        <h2 class="text-xl font-semibold">{{ user.name }}</h2>
        <p>{{ user.email }}</p>
        <p>{{ user.address.city }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      users: [],
    }
  },
  methods: {
    async fetchUsers() {
      const response = await axios.get('https://jsonplaceholder.typicode.com/users')
      this.users = response.data
    },
    goToUserDetails(id) {
      this.$router.push(`/user/${id}`)
    },
  },
  mounted() {
    this.fetchUsers()
  },
}
</script>
