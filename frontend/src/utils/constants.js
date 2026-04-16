export const APP_NAME = 'ChitraBazar'
export const APP_TAGLINE = 'Online painting gallery & store'

export const ROUTES = {
  HOME: '/',
  SHOP: '/shop',
  PRODUCT: '/products',
  WISHLIST: '/wishlist',
  LOGIN: '/login',
  REGISTER: '/register',
  ADMIN_DASHBOARD: '/admin/dashboard',
  CUSTOMER_HOME: '/customer/home',
}

export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'chitrabazar_access',
  REFRESH_TOKEN: 'chitrabazar_refresh',
  USER: 'chitrabazar_user',
}

export const SORT_OPTIONS = [
  { value: 'latest', label: 'Latest' },
  { value: 'price_low', label: 'Price: Low to High' },
  { value: 'price_high', label: 'Price: High to Low' },
  { value: 'top_rated', label: 'Top Rated' },
]

export const MEDIUM_OPTIONS = [
  { value: '', label: 'All mediums' },
  { value: 'oil', label: 'Oil' },
  { value: 'acrylic', label: 'Acrylic' },
  { value: 'watercolor', label: 'Watercolor' },
  { value: 'mixed', label: 'Mixed Media' },
  { value: 'digital', label: 'Digital Print' },
  { value: 'other', label: 'Other' },
]

export const CATEGORY_ICONS = {
  landscape: '🏔️',
  portrait: '👤',
  abstract: '🎨',
  'still-life': '🌸',
  contemporary: '✨',
}

export const PLACEHOLDER_IMAGE =
  'https://placehold.co/400x500/f5f5f4/78350f?text=ChitraBazar'

export const formatPrice = (price) => {
  const num = Number(price)
  if (Number.isNaN(num)) return price
  return `Rs. ${num.toLocaleString('en-NP')}`
}

export const formatMedium = (medium, mediumDisplay) => {
  if (mediumDisplay) return mediumDisplay
  if (!medium) return ''
  return medium.charAt(0).toUpperCase() + medium.slice(1).replace(/_/g, ' ')
}
