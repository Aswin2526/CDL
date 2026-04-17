import { useEffect, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import {
  clearError,
  getDashboardRoute,
  register as registerAccount,
  selectAuth,
  selectIsAuthenticated,
} from '../../redux/auth/authSlice'
import { ROUTES } from '../../utils/constants'

function RegisterPage() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const { loading, error, user } = useSelector(selectAuth)
  const isAuthenticated = useSelector(selectIsAuthenticated)

  const [form, setForm] = useState({
    full_name: '',
    email: '',
    password: '',
    phone_number: '',
    address: '',
  })

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
    const result = await dispatch(registerAccount(form))
    if (registerAccount.fulfilled.match(result)) {
      navigate(getDashboardRoute(result.payload.user.role), { replace: true })
    }
  }

  const errorMessage =
    error?.detail ||
    (error && typeof error === 'object'
      ? Object.entries(error)
          .map(([k, v]) => `${k}: ${Array.isArray(v) ? v[0] : v}`)
          .join(' ')
      : null)

  return (
    <div className="mx-auto max-w-lg px-4 py-12">
      <div className="rounded-xl border border-gray-200 bg-white p-8 shadow-sm">
        <h1 className="text-2xl font-bold text-gray-900">Create account</h1>
        <p className="mt-1 text-sm text-gray-500">
          Join as a collector to save artworks and leave reviews
        </p>

        <form onSubmit={handleSubmit} className="mt-6 space-y-4">
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Full name
            </label>
            <input
              name="full_name"
              required
              value={form.full_name}
              onChange={handleChange}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-amber-500 focus:outline-none focus:ring-1 focus:ring-amber-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              name="email"
              type="email"
              required
              value={form.email}
              onChange={handleChange}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-amber-500 focus:outline-none focus:ring-1 focus:ring-amber-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Password
            </label>
            <input
              name="password"
              type="password"
              required
              minLength={8}
              value={form.password}
              onChange={handleChange}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-amber-500 focus:outline-none focus:ring-1 focus:ring-amber-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Phone (optional)
            </label>
            <input
              name="phone_number"
              value={form.phone_number}
              onChange={handleChange}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-amber-500 focus:outline-none focus:ring-1 focus:ring-amber-500"
            />
          </div>
          <div>
            <label className="mb-1 block text-sm font-medium text-gray-700">
              Shipping address (optional)
            </label>
            <textarea
              name="address"
              rows={2}
              value={form.address}
              onChange={handleChange}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 focus:border-amber-500 focus:outline-none focus:ring-1 focus:ring-amber-500"
            />
          </div>

          {errorMessage && (
            <p className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
              {errorMessage}
            </p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-lg bg-amber-600 py-2.5 font-medium text-white hover:bg-amber-700 disabled:opacity-60"
          >
            {loading ? 'Creating account...' : 'Register'}
          </button>
        </form>

        <p className="mt-6 text-center text-sm text-gray-600">
          Already have an account?{' '}
          <Link to={ROUTES.LOGIN} className="font-medium text-amber-700 hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  )
}

export default RegisterPage
