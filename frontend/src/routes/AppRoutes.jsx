import { Routes, Route } from 'react-router-dom'
import MainLayout from '../layouts/MainLayout'
import ProtectedRoute from '../components/common/ProtectedRoute'
import HomePage from '../pages/HomePage'
import NotFoundPage from '../pages/NotFoundPage'
import LoginPage from '../pages/auth/LoginPage'
import RegisterPage from '../pages/auth/RegisterPage'
import AdminDashboard from '../pages/dashboard/AdminDashboard'
import CustomerHome from '../pages/dashboard/CustomerHome'
import ShopPage from '../pages/customer/ShopPage'
import ProductDetailPage from '../pages/customer/ProductDetailPage'
import WishlistPage from '../pages/customer/WishlistPage'

function AppRoutes() {
  return (
    <Routes>
      <Route element={<MainLayout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/shop" element={<ShopPage />} />
        <Route path="/products/:slug" element={<ProductDetailPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />

        <Route element={<ProtectedRoute />}>
          <Route path="/wishlist" element={<WishlistPage />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
        </Route>

        <Route element={<ProtectedRoute allowedRoles={['customer']} />}>
          <Route path="/customer/home" element={<CustomerHome />} />
        </Route>

        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}

export default AppRoutes
