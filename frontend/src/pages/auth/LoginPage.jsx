import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import {
  clearError,
  getDashboardRoute,
  login,
  selectAuth,
  selectIsAuthenticated,
} from '../../redux/auth/authSlice'
import { APP_NAME, ROUTES } from '../../utils/constants'

function LoginPage() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { loading, error, user } = useSelector(selectAuth)
  const isAuthenticated = useSelector(selectIsAuthenticated)

  const [form, setForm] = useState({ email: '', password: '' })

  useEffect(() => {
    dispatch(clearError())
  }, [dispatch])

  useEffect(() => {
    if (isAuthenticated && user) {
      navigate(getDashboardRoute(user.role), { replace: true })
    }
  }, [isAuthenticated, user, navigate])

  const handleChange = (e) => {
    setForm((prev) => ({ ...prev, [e.target.name]: e.target.value }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    const result = await dispatch(login(form))
    if (login.fulfilled.match(result)) {
      navigate(getDashboardRoute(result.payload.user.role), { replace: true })
    }
  }

  const errorMessage =
    error?.detail ||
    error?.non_field_errors?.[0] ||
    (typeof error === 'object' ? Object.values(error).flat()[0] : null)

  return (
    <div className="mx-auto flex min-h-[70vh] max-w-md flex-col justify-center px-4 py-12">
      <div className="rounded-xl border border-gray-200 bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-bold text-gray-900">Sign in</h1>
        <p className="mt-1 text-sm text-gray-500">
          Welcome back to {APP_NAME}
        </p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label htmlFor="email" className="mb-1 block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              value={form.email}
              onChange={handleChange}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-amber-500 focus:outline-none focus:ring-1 focus:ring-amber-500"
            />
          </div>
          <div>
            <label htmlFor="password" className="mb-1 block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              value={form.password}
              onChange={handleChange}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-amber-500 focus:outline-none focus:ring-1 focus:ring-amber-500"
            />
          </div>

          {errorMessage && (
            <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
              {String(errorMessage)}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-amber-600 py-2.5 font-medium text-white hover:bg-amber-700 disabled:opacity-60"
          >
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          No account?{' '}
          <Link to={ROUTES.REGISTER} className="font-medium text-amber-700 hover:underline">
            Register
          </Link>
        </p>
      </div>
    </div>
  )
}

export default LoginPage
