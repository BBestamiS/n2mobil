<template>
  <div class="flex h-screen p-0">
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

        <ul class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <li
            v-for="album in albums"
            :key="album.id"
            class="bg-white rounded-lg shadow p-4 border cursor-pointer hover:shadow-lg"
            @click="viewAlbumPhotos(album)"
          >
            <div class="grid grid-cols-2 mb-4">
              <img
                v-for="photo in previewPhotos"
                :key="photo.id"
                :src="photo.thumbnailUrl"
                :alt="photo.title"
                class="w-full h-full object-cover"
              />
            </div>
            <p class="text-gray-700 text-sm truncate font-thin">{{ album.title }}</p>
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
  name: 'AlbumsView',
  components: { SidebarHP },
  setup() {
    const router = useRouter()
    const albums = ref([])
    const previewPhotos = ref([])
    const isLoading = ref(true)

    // https://jsonplaceholder.typicode.com/photos end-point'i içerisinde bulunan fotoğraf url'leri çalışmadığı için alternatif api kullanılmıştır.
    const staticPhotos = [
      {
        id: 1,
        title: 'Sample Photo 1',
        thumbnailUrl: 'https://picsum.photos/id/1011/200/200',
      },
      {
        id: 2,
        title: 'Sample Photo 2',
        thumbnailUrl: 'https://picsum.photos/id/1022/200/200',
      },
      {
        id: 3,
        title: 'Sample Photo 3',
        thumbnailUrl: 'https://picsum.photos/id/1033/200/200',
      },
      {
        id: 4,
        title: 'Sample Photo 4',
        thumbnailUrl: 'https://picsum.photos/id/1044/200/200',
      },
    ]

    const fetchAlbums = async () => {
      try {
        const albumResponse = await fetch('https://jsonplaceholder.typicode.com/albums?userId=1')
        const albumData = await albumResponse.json()
        albums.value = albumData.map((album) => ({
          ...album,
          photos: staticPhotos,
        }))

        previewPhotos.value = staticPhotos
      } catch (error) {
        console.error('Albüm verisi yüklenirken hata oluştu:', error)
      } finally {
        isLoading.value = false
      }
    }

    const viewAlbumPhotos = (album) => {
      localStorage.setItem('selectedAlbum', JSON.stringify(album))
      router.push(`/albums/${album.id}`)
    }

    const goHome = () => {
      router.push('/')
    }

    onMounted(fetchAlbums)

    return {
      albums,
      previewPhotos,
      isLoading,
      viewAlbumPhotos,
      goHome,
    }
  },
}
</script>
