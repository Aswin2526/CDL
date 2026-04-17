import { Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { getDashboardRoute, selectIsAuthenticated, selectAuth } from '../../redux/auth/authSlice'

/**
 * Wrap login/register pages — redirect authenticated users to their dashboard.
 */
function GuestRoute({ children }) {
  const isAuthenticated = useSelector(selectIsAuthenticated)
  const { user } = useSelector(selectAuth)

  if (isAuthenticated && user?.role) {
    return <Navigate to={getDashboardRoute(user.role)} replace />
  }

  return children
}

export default GuestRoute
