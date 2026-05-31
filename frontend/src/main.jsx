import { StrictMode, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import { Provider, useDispatch, useSelector } from 'react-redux'
import './index.css'
import { router } from './routes/router.jsx'
import { store } from './redux/store/index.js'
import {
  initializeAuth,
  selectIsAuthenticated,
  selectIsCustomer,
} from './redux/auth/authSlice'
import { loadCart, resetCart } from './redux/cart/cartSlice'
import { loadWishlist, resetWishlist } from './redux/wishlist/wishlistSlice'
function AuthBootstrap({ children }) {
  const dispatch = useDispatch()
  const isAuthenticated = useSelector(selectIsAuthenticated)
  const isCustomer = useSelector(selectIsCustomer)

  useEffect(() => {
    dispatch(initializeAuth())
  }, [dispatch])

  useEffect(() => {
    if (isAuthenticated && isCustomer) {
      dispatch(loadCart())
      dispatch(loadWishlist())
    } else {
      dispatch(resetCart())
      dispatch(resetWishlist())
    }
  }, [dispatch, isAuthenticated, isCustomer])

  return children
}

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Provider store={store}>
      <AuthBootstrap>
        <RouterProvider router={router} />
      </AuthBootstrap>
    </Provider>
  </StrictMode>,
)
