import api from './api'

export const fetchAdminDashboard = () => api.get('/analytics/admin/dashboard/')
