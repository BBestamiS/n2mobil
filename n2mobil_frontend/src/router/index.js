import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '../views/HomePage.vue'
import TodosView from '../views/Todos.vue'
import { useSidebarStore } from '../stores/sidebarStore'
import PostsView from '../views/PostsView.vue'
import AlbumsView from '../views/AlbumsView.vue'
import AlbumPhotosView from '../views/AlbumPhotosView.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomePage,
  },
  {
    path: '/todos',
    name: 'Todos',
    component: TodosView,
  },
  {
    path: '/posts',
    name: 'Posts',
    component: PostsView,
  },
  {
    path: '/albums',
    name: 'AlbumsView',
    component: AlbumsView,
  },
  {
    path: '/albums/:albumId',
    name: 'AlbumPhotosView',
    component: AlbumPhotosView,
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const sidebarStore = useSidebarStore()

  if (to.path === '/') {
    sidebarStore.resetSidebar()
  }

  next()
})

export default router
