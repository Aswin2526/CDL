import api from './api'

export const registerUser = (payload) => api.post('/users/register/', payload)

export const loginUser = (payload) => api.post('/users/login/', payload)

export const logoutUser = () => api.post('/users/logout/')

export const refreshToken = (refresh) =>
  api.post('/users/token/refresh/', { refresh })

export const fetchProfile = () => api.get('/users/profile/')

export const updateProfile = (payload) => api.patch('/users/profile/', payload)

export const uploadProfileImage = (file) => {
  const formData = new FormData()
  formData.append('profile_image', file)
  return api.post('/users/profile/image/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}
