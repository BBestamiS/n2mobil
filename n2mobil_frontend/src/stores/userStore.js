import { defineStore } from 'pinia'
import { fetchUsers } from '../services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    users: [],
  }),
  actions: {
    async loadUsers() {
      const { data } = await fetchUsers()
      this.users = data
    },
  },
})
