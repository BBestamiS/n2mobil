<template>
  <div class="flex h-screen p-0">
    <SidebarHP
      class="bg-gray-100 flex-shrink-0 h-full transition-all duration-300"
      :class="['md:w-64']"
    />
    <div class="flex-1 overflow-y-auto p-4 mb-6">
      <UserCard
        :users="users"
        :locationLogo="locationLogo"
        :companyLogo="companyLogo"
        :websiteLogo="websiteLogo"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { fetchUsers } from '../services/api'
import SidebarHP from '../components/SidebarHP.vue'
import UserCard from '../components/UserCard.vue'
import { useSidebarStore } from '../stores/sidebarStore'

export default {
  name: 'HomePage',
  components: { SidebarHP, UserCard },
  setup() {
    const users = ref([])
    const sidebarStore = useSidebarStore()

    onMounted(async () => {
      if (!sidebarStore.selectedUser) {
        sidebarStore.clearUser()
      }
      const { data } = await fetchUsers()
      users.value = data.map((user) => ({
        ...user,
        avatar: `https://i.pravatar.cc/150?img=${user.id}`,
      }))
    })

    return {
      users,
    }
  },
}
</script>
