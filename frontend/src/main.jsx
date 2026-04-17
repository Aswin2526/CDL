import { StrictMode, useEffect } from 'react'
import { createRoot } from 'react-dom/client'
import { RouterProvider } from 'react-router-dom'
import { Provider, useDispatch } from 'react-redux'
import './index.css'
import { router } from './routes/router.jsx'
import { store } from './redux/store/index.js'
import { initializeAuth } from './redux/auth/authSlice'

function AuthBootstrap({ children }) {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(initializeAuth())
  }, [dispatch])

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
