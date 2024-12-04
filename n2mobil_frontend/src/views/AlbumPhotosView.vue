<template>
  <div class="flex h-screen p-0">
    <SidebarHP
      class="bg-gray-100 flex-shrink-0 h-full transition-all duration-300"
      :class="['md:w-64']"
    />
    <div class="flex-1 overflow-y-auto p-6">
      <div class="max-w-6xl mx-auto">
        <div class="flex items-center mb-24 mt-4">
          <button @click="goAlbums" class="flex items-center gap-2 font-medium text-2xl">
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
            Go Albums
          </button>
        </div>
        <ul class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          <li v-for="photo in photos" :key="photo.id" class="p-4">
            <img :src="photo.thumbnailUrl" :alt="photo.title" class="h-auto mb-2" />
            <p class="text-gray-700 text-sm truncate">{{ photo.title }}</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import SidebarHP from '../components/SidebarHP.vue'

export default {
  name: 'AlbumPhotosView',
  components: { SidebarHP },
  setup() {
    const router = useRouter()
    const album = ref({})
    const photos = ref([])
    const isLoading = ref(true)

    // https://jsonplaceholder.typicode.com/photos end-point'i içerisinde bulunan fotoğraf url'leri çalışmadığı için alternatif api kullanılmıştır.
    const staticPhotos = [
      {
        id: 1,
        thumbnailUrl: 'https://picsum.photos/id/1011/200/200',
      },
      {
        id: 2,
        thumbnailUrl: 'https://picsum.photos/id/1022/200/200',
      },
      {
        id: 3,
        thumbnailUrl: 'https://picsum.photos/id/1033/200/200',
      },
      {
        id: 4,
        thumbnailUrl: 'https://picsum.photos/id/1044/200/200',
      },
    ]

    const fetchAlbum = () => {
      const storedAlbum = JSON.parse(localStorage.getItem('selectedAlbum'))
      if (storedAlbum) {
        album.value = storedAlbum
        photos.value = staticPhotos
        isLoading.value = false
      } else {
        console.warn('Albüm bilgisi bulunamadı. Albüm listesine yönlendiriliyor...')
        goAlbums()
      }
    }

    const goAlbums = () => {
      router.push('/albums')
    }

    onMounted(fetchAlbum)

    return {
      album,
      photos,
      isLoading,
      goAlbums,
    }
  },
}
</script>
