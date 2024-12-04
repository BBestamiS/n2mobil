<template>
  <div v-if="selectedUser" class="flex h-screen p-0">
    <SidebarHP
      class="bg-gray-100 flex-shrink-0 h-full transition-all duration-300"
      :class="['md:w-64']"
    />
    <div class="flex-1 overflow-y-auto p-6">
      <div class="max-w-6xl mx-auto">
        <div class="flex items-center mb-24 mt-4">
          <button @click="goHome" class="flex items-center gap-2 font-medium text-2xl">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="36"
              height="36"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            >
              <path d="M12 8l-4 4l4 4" />
              <path d="M16 12h-8" />
              <path d="M12 3c7.2 0 9 1.8 9 9s-1.8 9 -9 9s-9 -1.8 -9 -9s1.8 -9 9 -9z" />
            </svg>
            Go Home
          </button>
        </div>

        <ul class="space-y-6">
          <li
            v-for="post in posts"
            :key="post.id"
            class="p-6 border-b border-[#D8D9DD] cursor-pointer"
            @click="showPostDetails(post)"
          >
            <h2 class="text-xl font-medium mb-4">{{ post.title }}</h2>
            <p class="text-base text-gray-700 mb-4 text-[#5C6672]">{{ post.body }}</p>
            <div class="flex w-full justify-end">
              <button class="flex items-center gap-2 mt-4">
                <p class="font-thin text-base mr-4">See More</p>
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  width="24"
                  height="24"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="#4F359B"
                  stroke-width="2"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                >
                  <path d="M12 16l4 -4l-4 -4" />
                  <path d="M8 12h8" />
                  <path d="M12 3c7.2 0 9 1.8 9 9s-1.8 9 -9 9s-9 -1.8 -9 -9s1.8 -9 9 -9z" />
                </svg>
              </button>
            </div>
          </li>
        </ul>
      </div>
    </div>

    <div
      v-if="selectedPost"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center"
    >
      <div class="bg-white rounded-3xl shadow-lg max-w-5xl w-full p-8 flex max-h-[550px]">
        <div class="flex-1 pr-4 overflow-y-auto">
          <h2 class="text-xl font-medium mb-4">{{ selectedPost.title }}</h2>
          <p class="text-[#5C6672] font-thin">{{ selectedPost.body }}</p>
        </div>

        <div class="flex-1 flex-col">
          <div class="flex justify-end w-full h-[5%] mb-4">
            <button @click="closePostDetails">
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
                <path d="M10 10l4 4m0 -4l-4 4"></path>
                <path d="M12 3c7.2 0 9 1.8 9 9s-1.8 9 -9 9s-9 -1.8 -9 -9s1.8 -9 9 -9z"></path>
              </svg>
            </button>
          </div>
          <div class="flex-1 pl-4 h-[93%] border-l overflow-y-auto">
            <h3 class="text-xl font-medium mb-4">Comments</h3>
            <div v-if="isCommentsLoading" class="flex justify-center items-center">
              <div
                class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-purple-600"
              ></div>
              <span class="ml-2 text-gray-600">Loading comments...</span>
            </div>
            <ul v-else class="space-y-4">
              <li
                v-for="comment in comments"
                :key="comment.id"
                class="flex gap-4 mb-4 items-center"
              >
                <img
                  :src="`https://i.pravatar.cc/50?u=${comment.email}`"
                  alt="User Avatar"
                  class="w-12 h-12 rounded-full object-cover"
                />
                <div>
                  <h4 class="font-bold text-gray-800">{{ comment.name }}</h4>
                  <p class="text-[#5C6672] text-sm font-thin">{{ comment.body }}</p>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="flex items-center justify-center h-screen">
    <p class="text-xl text-gray-500">
      Kullanıcı bilgisi bulunamadı. Ana sayfaya yönlendiriliyorsunuz...
    </p>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useSidebarStore } from '../stores/sidebarStore'
import SidebarHP from '../components/SidebarHP.vue'

export default {
  name: 'PostsView',
  components: { SidebarHP },
  setup() {
    const sidebarStore = useSidebarStore()
    const posts = ref([])
    const selectedPost = ref(null)
    const comments = ref([])
    const isCommentsLoading = ref(false)

    const fetchPosts = async (userId) => {
      const response = await fetch(`https://jsonplaceholder.typicode.com/posts?userId=${userId}`)
      const data = await response.json()
      posts.value = data

      localStorage.setItem('posts', JSON.stringify(data))
    }

    const showPostDetails = async (post) => {
      selectedPost.value = post
      isCommentsLoading.value = true

      try {
        const response = await fetch(
          `https://jsonplaceholder.typicode.com/comments?postId=${post.id}`,
        )
        comments.value = await response.json()
      } catch (error) {
        console.error('Error fetching comments:', error)
      } finally {
        isCommentsLoading.value = false
      }
    }

    const closePostDetails = () => {
      selectedPost.value = null
      comments.value = []
    }

    const goHome = () => {
      window.location.href = '/'
    }

    onMounted(() => {
      if (sidebarStore.selectedUser) {
        const savedPosts = JSON.parse(localStorage.getItem('posts'))
        if (savedPosts && savedPosts.length) {
          posts.value = savedPosts
        } else {
          fetchPosts(sidebarStore.selectedUser.id)
        }
      } else {
        console.warn('Kullanıcı bilgisi bulunamadı. Ana sayfaya yönlendiriliyor...')
        window.location.href = '/'
      }
    })

    return {
      posts,
      selectedPost,
      comments,
      isCommentsLoading,
      selectedUser: sidebarStore.selectedUser,
      showPostDetails,
      closePostDetails,
      goHome,
    }
  },
}
</script>
