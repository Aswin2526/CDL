import { Navigate, Outlet } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { ROUTES } from '../../utils/constants'
import { selectAuth, selectIsAuthenticated } from '../../redux/auth/authSlice'

function ProtectedRoute({ allowedRoles }) {
  const isAuthenticated = useSelector(selectIsAuthenticated)
  const { user } = useSelector(selectAuth)

  if (!isAuthenticated) {
    return <Navigate to={ROUTES.LOGIN} replace />
  }

  if (allowedRoles && !allowedRoles.includes(user?.role)) {
    return <Navigate to={ROUTES.HOME} replace />
  }

  return <Outlet />
}

export default ProtectedRoute
