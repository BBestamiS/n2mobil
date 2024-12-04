<template>
  <div class="container mx-auto p-4">
    <div v-if="user" class="bg-white shadow-lg rounded-lg p-6">
      <h1 class="text-2xl font-bold mb-4">{{ user.name }} Detayları</h1>
      <p class="mb-4">{{ user.email }}</p>

      <div class="tabs">
        <button
          @click="activeTab = 'posts'"
          :class="{ 'bg-blue-500': activeTab === 'posts' }"
          class="p-2 rounded"
        >
          Paylaşımlar
        </button>
        <button
          @click="activeTab = 'albums'"
          :class="{ 'bg-blue-500': activeTab === 'albums' }"
          class="p-2 rounded"
        >
          Albümler
        </button>
        <button
          @click="activeTab = 'todos'"
          :class="{ 'bg-blue-500': activeTab === 'todos' }"
          class="p-2 rounded"
        >
          Görevler
        </button>
      </div>

      <div v-if="activeTab === 'posts'">
        <h2 class="text-xl font-semibold">Paylaşımlar</h2>
        <div v-for="post in posts" :key="post.id" class="mb-4">
          <h3 class="font-bold">{{ post.title }}</h3>
          <p>{{ post.body }}</p>
        </div>
      </div>

      <div v-if="activeTab === 'albums'">
        <h2 class="text-xl font-semibold">Albümler</h2>
        <div v-for="album in albums" :key="album.id" class="mb-4">
          <h3 class="font-bold">{{ album.title }}</h3>
        </div>
      </div>

      <div v-if="activeTab === 'todos'">
        <h2 class="text-xl font-semibold">Görevler</h2>
        <div v-for="todo in todos" :key="todo.id" class="mb-4">
          <p>{{ todo.title }} - {{ todo.completed ? 'Tamamlandı' : 'Tamamlanmadı' }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { fetchUserDetails, fetchPosts, fetchAlbums, fetchTodos } from '../services/api'

export default {
  name: 'UserDetail',
  setup() {
    const route = useRoute()
    const user = ref(null)
    const posts = ref([])
    const albums = ref([])
    const todos = ref([])
    const activeTab = ref('posts')

    onMounted(async () => {
      const userId = route.params.id
      const { data: userData } = await fetchUserDetails(userId)
      user.value = userData

      const { data: postData } = await fetchPosts(userId)
      posts.value = postData

      const { data: albumData } = await fetchAlbums(userId)
      albums.value = albumData

      const { data: todoData } = await fetchTodos(userId)
      todos.value = todoData
    })

    return {
      user,
      posts,
      albums,
      todos,
      activeTab,
    }
  },
}
</script>

<style scoped>
.tabs button {
  margin-right: 8px;
}
</style>
