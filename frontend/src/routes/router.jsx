import { createBrowserRouter } from 'react-router-dom'
import MainLayout from '../layouts/MainLayout'
import ProtectedRoute from '../components/common/ProtectedRoute'
import GuestRoute from '../components/common/GuestRoute'
import HomePage from '../pages/HomePage'
import NotFoundPage from '../pages/NotFoundPage'
import LoginPage from '../pages/auth/LoginPage'
import RegisterPage from '../pages/auth/RegisterPage'
import AdminDashboard from '../pages/dashboard/AdminDashboard'
import CustomerHome from '../pages/dashboard/CustomerHome'
import ShopPage from '../pages/customer/ShopPage'
import ProductDetailPage from '../pages/customer/ProductDetailPage'
import WishlistPage from '../pages/customer/WishlistPage'
import CartPage from '../pages/customer/CartPage'

export const router = createBrowserRouter([
  {
    path: '/',
    element: <MainLayout />,
    children: [
      { index: true, element: <HomePage /> },
      { path: 'shop', element: <ShopPage /> },
      { path: 'products/:slug', element: <ProductDetailPage /> },
      {
        path: 'login',
        element: (
          <GuestRoute>
            <LoginPage />
          </GuestRoute>
        ),
      },
      {
        path: 'register',
        element: (
          <GuestRoute>
            <RegisterPage />
          </GuestRoute>
        ),
      },
      {
        element: <ProtectedRoute />,
        children: [
          { path: 'wishlist', element: <WishlistPage /> },
          { path: 'cart', element: <CartPage /> },
        ],
      },
      {
        element: <ProtectedRoute allowedRoles={['admin']} />,
        children: [{ path: 'admin/dashboard', element: <AdminDashboard /> }],
      },
      {
        element: <ProtectedRoute allowedRoles={['customer']} />,
        children: [{ path: 'customer/home', element: <CustomerHome /> }],
      },
      { path: '*', element: <NotFoundPage /> },
    ],
  },
])
