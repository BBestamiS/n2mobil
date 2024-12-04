<template>
  <div>
    <button
      class="fixed top-6 right-6 z-50 p-2 bg-[#4F359B] text-white rounded-md md:hidden"
      @click="toggleSidebar"
    >
      Menu
    </button>

    <div
      :class="[
        'bg-gray-100 h-screen flex flex-col justify-between fixed top-0 left-0 z-40 transition-transform duration-300',
        isSidebarOpen ? 'translate-x-0' : '-translate-x-full',
        'md:relative md:translate-x-0 md:w-64',
      ]"
    >
      <div>
        <div v-if="selectedUser" class="p-4 text-center border-b border-[#D8D9DD]">
          <img
            :src="selectedUser.avatar"
            alt="User Avatar"
            class="rounded-full mx-auto mb-2 h-16 object-cover"
          />
          <h2 class="text-lg font-bold">{{ selectedUser.name }}</h2>
          <p class="text-sm text-gray-600 underline">{{ selectedUser.email }}</p>
        </div>
        <nav>
          <ul class="space-y-2">
            <li
              v-for="tab in tabs"
              :key="tab.name"
              class="relative flex items-center gap-2 p-2 mt-4 bg-[#FFFFFF] text-gray-700 hover:bg-gray-200"
            >
              <div
                v-if="isActive(tab.name)"
                class="absolute left-0 top-0 h-full w-2 bg-[#4F359B] rounded-r-lg"
              ></div>
              <router-link
                :to="tab.route"
                class="flex items-center gap-2 w-full"
                @click="setActiveTab(tab.name)"
              >
                <div
                  :class="
                    isActive(tab.name) ? 'flex text-[#4F359B] font-semibold' : 'text-gray-700 flex '
                  "
                >
                  <svg
                    v-if="tab.icon === 'user-icon'"
                    class="mr-2 ml-4"
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
                    <path d="M9 7m-4 0a4 4 0 1 0 8 0a4 4 0 1 0 -8 0"></path>
                    <path d="M3 21v-2a4 4 0 0 1 4 -4h4a4 4 0 0 1 4 4v2"></path>
                  </svg>
                  <svg
                    v-else-if="tab.icon === 'todos-icon'"
                    class="mr-2 ml-4"
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M9 5h-2a2 2 0 0 0 -2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2 -2v-12a2 2 0 0 0 -2 -2h-2"
                    />
                    <path
                      d="M9 3m0 2a2 2 0 0 1 2 -2h2a2 2 0 0 1 2 2v0a2 2 0 0 1 -2 2h-2a2 2 0 0 1 -2 -2z"
                    />
                    <path d="M9 14h.01" />
                    <path d="M9 17h.01" />
                    <path d="M12 16l1 1l3 -3" />
                  </svg>
                  <svg
                    v-else-if="tab.icon === 'posts-icon'"
                    class="mr-2 ml-4"
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path
                      d="M6 4h11a2 2 0 0 1 2 2v12a2 2 0 0 1 -2 2h-11a1 1 0 0 1 -1 -1v-14a1 1 0 0 1 1 -1m3 0v18"
                    />
                    <path d="M13 8l2 0" />
                    <path d="M13 12l2 0" />
                    >
                    <path d="M4 4h16v16H4z"></path>
                  </svg>
                  <svg
                    v-else-if="tab.icon === 'albums-icon'"
                    class="mr-2 ml-4"
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                  >
                    <path d="M15 8h.01" />
                    <path d="M11.5 21h-5.5a3 3 0 0 1 -3 -3v-12a3 3 0 0 1 3 -3h12a3 3 0 0 1 3 3v5" />
                    <path d="M3 16l5 -5c.928 -.893 2.072 -.893 3 0l1.5 1.5" />
                    <path
                      d="M18 22l3.35 -3.284a2.143 2.143 0 0 0 .005 -3.071a2.242 2.242 0 0 0 -3.129 -.006l-.224 .22l-.223 -.22a2.242 2.242 0 0 0 -3.128 -.006a2.143 2.143 0 0 0 -.006 3.071l3.355 3.296z"
                    />
                  </svg>
                  {{ tab.name }}
                </div>
              </router-link>
            </li>
          </ul>
        </nav>
      </div>

      <div class="p-4 text-center">
        <img :src="logo" alt="Logo" class="mx-auto w-max" />
      </div>
    </div>

    <div
      v-if="isSidebarOpen"
      class="fixed inset-0 bg-black bg-opacity-50 z-30 md:hidden"
      @click="toggleSidebar"
    ></div>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue'
import { useSidebarStore } from '../stores/sidebarStore'
import logo from '../assets/logo.png'

export default {
  name: 'SidebarHP',
  setup() {
    const sidebarStore = useSidebarStore()
    const isSidebarOpen = ref(false)

    const tabs = computed(() => {
      if (!sidebarStore.selectedUser) {
        return [
          {
            name: 'Users',
            route: '/',
            icon: 'user-icon',
          },
        ]
      }
      return [
        {
          name: 'Todos',
          route: '/todos',
          icon: 'todos-icon',
        },
        {
          name: 'Posts',
          route: '/posts',
          icon: 'posts-icon',
        },
        {
          name: 'Albums',
          route: '/albums',
          icon: 'albums-icon',
        },
      ]
    })

    const setActiveTab = (tab) => {
      sidebarStore.setActiveTab(tab)
      isSidebarOpen.value = false
    }

    const isActive = (tab) => sidebarStore.activeTab === tab

    const toggleSidebar = () => {
      isSidebarOpen.value = !isSidebarOpen.value
    }

    onMounted(() => {
      if (!sidebarStore.selectedUser && sidebarStore.activeTab !== 'Users') {
        window.location.href = '/'
      }
    })

    return {
      tabs,
      setActiveTab,
      isActive,
      toggleSidebar,
      isSidebarOpen,
      logo,
      selectedUser: sidebarStore.selectedUser,
    }
  },
}
</script>
