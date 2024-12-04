import { defineStore } from 'pinia'

export const useSidebarStore = defineStore('sidebar', {
  state: () => ({
    selectedUser: JSON.parse(localStorage.getItem('selectedUser')) || null,
    activeTab: localStorage.getItem('activeTab') || 'Users',
  }),
  actions: {
    setActiveTab(tab) {
      this.activeTab = tab
      localStorage.setItem('activeTab', tab)
    },
    selectUser(user) {
      this.selectedUser = user
      localStorage.setItem('selectedUser', JSON.stringify(user))
    },
    setSelectedUser(user) {
      this.selectedUser = user
      localStorage.setItem('selectedUser', JSON.stringify(user))
    },
    clearUser() {
      this.selectedUser = null
      localStorage.removeItem('selectedUser')
      this.activeTab = 'Users'
      localStorage.setItem('activeTab', 'Users')
    },
    resetSidebar() {
      this.clearUser()
    },
  },
})
