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

        <ul class="space-y-4">
          <li v-for="todo in todos" :key="todo.id" class="flex items-center gap-4 p-4 rounded-lg">
            <input
              type="checkbox"
              :checked="todo.completed"
              class="w-5 h-5 text-purple-600 accent-[#4F359B] border-gray-300 rounded focus:ring-purple-500"
              @change="updateTodo(todo)"
            />
            <p :class="{ 'line-through text-gray-500': todo.completed }" class="text-gray-700">
              {{ todo.title }}
            </p>
          </li>
        </ul>
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
  name: 'TodosView',
  components: { SidebarHP },
  setup() {
    const sidebarStore = useSidebarStore()
    const todos = ref([])

    const fetchTodos = async (userId) => {
      const response = await fetch(`https://jsonplaceholder.typicode.com/todos?userId=${userId}`)
      todos.value = await response.json()

      const savedTodos = JSON.parse(localStorage.getItem('todos')) || []
      todos.value.forEach((todo) => {
        const savedTodo = savedTodos.find((t) => t.id === todo.id)
        if (savedTodo) {
          todo.completed = savedTodo.completed
        }
      })
    }

    const updateTodo = async (todo) => {
      const response = await fetch(`https://jsonplaceholder.typicode.com/todos/${todo.id}`, {
        method: 'PUT',
        body: JSON.stringify({
          ...todo,
          completed: !todo.completed,
        }),
        headers: {
          'Content-type': 'application/json; charset=UTF-8',
        },
      })

      const updatedTodo = await response.json()

      todo.completed = updatedTodo.completed

      const savedTodos = JSON.parse(localStorage.getItem('todos')) || []
      const updatedTodos = savedTodos.filter((t) => t.id !== todo.id)
      updatedTodos.push(updatedTodo)
      localStorage.setItem('todos', JSON.stringify(updatedTodos))
    }

    const goHome = () => {
      window.location.href = '/'
    }

    onMounted(() => {
      if (sidebarStore.selectedUser) {
        fetchTodos(sidebarStore.selectedUser.id)
      } else {
        window.location.href = '/'
      }
    })

    return {
      todos,
      selectedUser: sidebarStore.selectedUser,
      updateTodo,
      goHome,
    }
  },
}
</script>
