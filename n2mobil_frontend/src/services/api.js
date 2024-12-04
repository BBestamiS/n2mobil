import axios from 'axios'
import { useErrorStore } from '../stores/errorStore'

const API = 'https://jsonplaceholder.typicode.com'

const handleRequest = async (request) => {
  const errorStore = useErrorStore()
  try {
    const response = await request()
    return response
  } catch (error) {
    console.error('API Error:', error.message || 'An error occurred')
    errorStore.setError('Beklenmedik bir hata oluştu. Lütfen tekrar deneyin.')
    throw new Error('Beklenmedik bir hata oluştu. Lütfen tekrar deneyin.')
  }
}

export const fetchUsers = async () => handleRequest(() => axios.get(`${API}/users`))

export const fetchUserDetails = async (id) => handleRequest(() => axios.get(`${API}/users/${id}`))

export const fetchPosts = async (userId) =>
  handleRequest(() => axios.get(`${API}/posts?userId=${userId}`))

export const fetchAlbums = async (userId) =>
  handleRequest(() => axios.get(`${API}/albums?userId=${userId}`))

export const fetchTodos = async (userId) =>
  handleRequest(() => axios.get(`${API}/todos?userId=${userId}`))
