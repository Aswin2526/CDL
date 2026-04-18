
import api from './api'

export const fetchProducts = (params = {}) => api.get('/products/', { params })

export const fetchProductDetail = (slug) => api.get(`/products/${slug}/`)

export const fetchCategories = () => api.get('/products/categories/')

export const fetchCategoryProducts = (slug, params = {}) =>
  api.get(`/products/categories/${slug}/products/`, { params })

export const fetchFeaturedProducts = () => api.get('/products/featured/')

export const fetchLatestProducts = () => api.get('/products/latest/')

export const fetchTopRatedProducts = () => api.get('/products/top-rated/')

export const fetchProductReviews = (productId) =>
  api.get(`/reviews/product/${productId}/`)

export const addProductReview = (productId, payload) =>
  api.post(`/reviews/product/${productId}/add/`, payload)

export const fetchWishlist = () => api.get('/customers/wishlist/')

export const toggleWishlist = (productId) =>
  api.post('/customers/wishlist/toggle/', { product_id: productId })

export const removeFromWishlist = (productId) =>
  api.delete(`/customers/wishlist/${productId}/`)
