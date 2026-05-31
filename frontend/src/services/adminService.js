import api from './api'

export const fetchAdminDashboard = () => api.get('/analytics/admin/dashboard/')

/** Default dev admin — must match backend seed_admin command */
export const DEFAULT_ADMIN_CREDENTIALS = {
  email: 'admin@chitrabazar.com',
  password: 'ChitraAdmin@2024',
}
