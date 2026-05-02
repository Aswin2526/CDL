import api from './api'

export const fetchCart = () => api.get('/carts/')

export const addToCart = (productId, quantity = 1) =>
  api.post('/carts/add/', { product_id: productId, quantity })

export const updateCartQuantity = (productId, quantity) =>
  api.patch(`/carts/items/${productId}/`, { quantity })

export const removeFromCart = (productId) => api.delete(`/carts/items/${productId}/`)

export const clearCart = () => api.delete('/carts/clear/')
