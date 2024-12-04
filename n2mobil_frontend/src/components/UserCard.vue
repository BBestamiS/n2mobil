<template>
  <div class="max-w-6xl mx-auto p-4 bg-gray-50 rounded-lg">
    <h1 class="text-2xl font-medium mb-4">All Users</h1>
    <div class="grid grid-cols-1 md:grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
      <div
        v-for="user in users"
        :key="user.id"
        class="bg-white border border-gray-200 rounded-lg p-6 transition-shadow duration-300 hover:shadow-xl cursor-pointer"
        @click="selectUser(user)"
      >
        <div class="flex items-center mb-4">
          <img
            :src="`https://i.pravatar.cc/150?img=${user.id}`"
            alt="User Avatar"
            class="w-20 h-20 rounded-full object-cover"
          />
          <div class="ml-4">
            <h2 class="text-xl font-medium text-lg">{{ user.name }}</h2>
            <p class="text-gray-600 font-extralight text-sm text-[#5C6672]">{{ user.email }}</p>
            <p class="text-gray-600 font-extralight text-sm text-[#5C6672]">{{ user.phone }}</p>
          </div>
        </div>
        <div class="space-y-4">
          <div class="flex flex-col">
            <div class="flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                width="24"
                height="24"
                stroke-width="2"
              >
                <path d="M15 11a3 3 0 1 0 -3.973 2.839"></path>
                <path
                  d="M11.76 21.47a1.991 1.991 0 0 1 -1.173 -.57l-4.244 -4.243a8 8 0 1 1 13.657 -5.588"
                ></path>
                <path
                  d="M18 22l3.35 -3.284a2.143 2.143 0 0 0 .005 -3.071a2.242 2.242 0 0 0 -3.129 -.006l-.224 .22l-.223 -.22a2.242 2.242 0 0 0 -3.128 -.006a2.143 2.143 0 0 0 -.006 3.071l3.355 3.296z"
                ></path>
              </svg>
              <h3 class="font-medium text-sm ml-2">Location</h3>
            </div>
            <div>
              <p class="text-gray-600 font-extralight text-sm text-[#5C6672]">
                {{ user.address.street }}, {{ user.address.suite }},<br />
                {{ user.address.city }} / {{ user.address.zipcode }}
              </p>
            </div>
          </div>
          <div class="flex flex-col">
            <div class="flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                width="24"
                height="24"
                stroke-width="2"
              >
                <path d="M3 21l18 0"></path>
                <path d="M5 21v-14l8 -4v18"></path>
                <path d="M19 21v-10l-6 -4"></path>
                <path d="M9 9l0 .01"></path>
                <path d="M9 12l0 .01"></path>
                <path d="M9 15l0 .01"></path>
                <path d="M9 18l0 .01"></path>
              </svg>

              <h3 class="font-medium text-sm ml-2">Company</h3>
            </div>
            <div>
              <p class="text-gray-600 text-sm text-[#5C6672]">{{ user.company.name }}</p>
              <p class="text-gray-600 text-sm text-[#5C6672]">{{ user.company.catchPhrase }}</p>
            </div>
          </div>
          <div class="flex flex-col">
            <div class="flex items-center">
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 30 24"
                fill="none"
                stroke="currentColor"
                stroke-linecap="round"
                stroke-linejoin="round"
                width="24"
                height="24"
                stroke-width="2"
              >
                <path d="M20.94 13.045a9 9 0 1 0 -8.953 7.955"></path>
                <path d="M3.6 9h16.8"></path>
                <path d="M3.6 15h9.4"></path>
                <path d="M11.5 3a17 17 0 0 0 0 18"></path>
                <path d="M12.5 3a16.991 16.991 0 0 1 2.529 10.294"></path>
                <path d="M16 22l5 -5"></path>
                <path d="M21 21.5v-4.5h-4.5"></path>
              </svg>

              <h3 class="font-medium text-sm ml-2">Website</h3>
            </div>
            <div>
              <p class="text-gray-600 text-sm text-[#5C6672]">
                <a :href="'http://' + user.website" target="_blank" class="text-sm">
                  {{ user.website }}
                </a>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useSidebarStore } from '../stores/sidebarStore' // Pinia
import { useRouter } from 'vue-router'

export default {
  props: {
    users: {
      type: Array,
      required: true,
    },
  },
  setup() {
    const sidebarStore = useSidebarStore()
    const router = useRouter()

    const selectUser = (user) => {
      const selectedUser = {
        ...user,
        avatar: `https://i.pravatar.cc/150?img=${user.id}`,
      }

      // Seçilen kullanıcıyı Pinia Store'a yaz
      sidebarStore.setSelectedUser(selectedUser)

      // Seçilen kullanıcıyı Local Storage'a kaydet
      localStorage.setItem('selectedUser', JSON.stringify(selectedUser))

      sidebarStore.setActiveTab('Todos')
      router.push('/todos')
    }

    return {
      selectUser,
    }
  },
}
</script>
