import axios from 'axios'
import { STORAGE_KEYS } from '../utils/constants'

/**
 * Central Axios client for ChitraBazar API with JWT support.
 */
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Attach access token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN)
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Refresh access token on 401
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    if (error.response?.status !== 401 || original._retry) {
      return Promise.reject(error)
    }

    const refresh = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN)
    if (!refresh) {
      return Promise.reject(error)
    }

    original._retry = true
    try {
      const { data } = await axios.post(
        `${import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'}/users/token/refresh/`,
        { refresh },
      )
      localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, data.access)
      original.headers.Authorization = `Bearer ${data.access}`
      return api(original)
    } catch (refreshError) {
      localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
      localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
      localStorage.removeItem(STORAGE_KEYS.USER)
      return Promise.reject(refreshError)
    }
  },
)

export default api
