import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { selectAuth } from '../../redux/auth/authSlice'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import {
  DEFAULT_ADMIN_CREDENTIALS,
  fetchAdminDashboard,
} from '../../services/adminService'
import { ROUTES, formatPrice } from '../../utils/constants'

const DJANGO_ADMIN_URL = 'http://127.0.0.1:8000/admin/'

function StatCard({ label, value, hint }) {
  return (
    <div className="rounded-xl border border-stone-200 bg-white p-5 shadow-sm">
      <p className="text-sm font-medium text-gray-500">{label}</p>
      <p className="mt-1 text-2xl font-bold text-gray-900">{value}</p>
      {hint && <p className="mt-1 text-xs text-gray-400">{hint}</p>}
    </div>
  )
}

function AdminDashboard() {
  const { user } = useSelector(selectAuth)
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    let active = true
    setLoading(true)
    fetchAdminDashboard()
      .then(({ data }) => {
        if (active) {
          setStats(data)
          setError('')
        }
      })
      .catch((err) => {
        if (active) {
          setStats(null)
          setError(
            err.response?.data?.detail || 'Could not load dashboard stats.',
          )
        }
      })
      .finally(() => {
        if (active) setLoading(false)
      })
    return () => {
      active = false
    }
  }, [])

  const totals = stats?.totals

  return (
    <section className="mx-auto max-w-7xl px-4 py-10">
      <div className="flex flex-wrap items-start justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
          <p className="mt-1 text-gray-600">
            Welcome, {user?.full_name}. Overview of ChitraBazar gallery and collectors.
          </p>
        </div>
        <div className="flex flex-wrap gap-2">
          <Link
            to={ROUTES.SHOP}
            className="rounded-lg border border-stone-300 px-4 py-2 text-sm font-medium text-gray-700 hover:border-amber-500 hover:text-amber-800"
          >
            View gallery
          </Link>
          <a
            href={DJANGO_ADMIN_URL}
            target="_blank"
            rel="noreferrer"
            className="rounded-lg bg-amber-600 px-4 py-2 text-sm font-medium text-white hover:bg-amber-700"
          >
            Django admin
          </a>
        </div>
      </div>

      <div className="mt-8 rounded-xl border border-amber-200 bg-amber-50 p-5">
        <h2 className="text-sm font-semibold uppercase tracking-wide text-amber-900">
          Admin login (ready-made)
        </h2>
        <p className="mt-2 text-sm text-amber-950">
          Use these credentials on the{' '}
          <Link to={ROUTES.LOGIN} className="font-medium underline hover:text-amber-800">
            login page
          </Link>
          :
        </p>
        <dl className="mt-3 grid gap-2 text-sm sm:grid-cols-2">
          <div>
            <dt className="font-medium text-amber-900">Email</dt>
            <dd className="font-mono text-gray-900">{DEFAULT_ADMIN_CREDENTIALS.email}</dd>
          </div>
          <div>
            <dt className="font-medium text-amber-900">Password</dt>
            <dd className="font-mono text-gray-900">{DEFAULT_ADMIN_CREDENTIALS.password}</dd>
          </div>
        </dl>
        <p className="mt-3 text-xs text-amber-800">
          Create or reset this account with{' '}
          <code className="rounded bg-white/80 px-1">python manage.py seed_admin</code>
        </p>
      </div>

      {loading && (
        <div className="mt-10">
          <LoadingSpinner label="Loading dashboard…" />
        </div>
      )}

      {error && !loading && (
        <p className="mt-8 rounded-lg bg-red-50 px-4 py-3 text-sm text-red-700">{error}</p>
      )}

      {totals && !loading && (
        <>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard label="Active paintings" value={totals.products_active} />
            <StatCard label="Registered collectors" value={totals.customers} />
            <StatCard
              label="Open carts"
              value={totals.active_carts}
              hint={`${totals.cart_line_items} line items`}
            />
            <StatCard
              label="Wishlist saves"
              value={totals.wishlist_items}
              hint={`${totals.reviews} reviews`}
            />
          </div>

          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard label="Categories" value={totals.categories} />
            <StatCard label="Featured" value={totals.featured_products} />
            <StatCard label="Sold out" value={totals.sold_out} />
            <StatCard
              label="Cart subtotal (all users)"
              value={formatPrice(stats.cart_value?.subtotal)}
            />
          </div>

          <div className="mt-10 grid gap-8 lg:grid-cols-2">
            <div className="rounded-xl border border-stone-200 bg-white p-5 shadow-sm">
              <h2 className="text-lg font-semibold text-gray-900">Paintings by category</h2>
              <ul className="mt-4 space-y-2">
                {stats.categories?.map((cat) => (
                  <li
                    key={cat.slug}
                    className="flex items-center justify-between text-sm text-gray-700"
                  >
                    <span>{cat.name}</span>
                    <span className="font-medium text-gray-900">{cat.product_count}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="rounded-xl border border-stone-200 bg-white p-5 shadow-sm">
              <h2 className="text-lg font-semibold text-gray-900">Low stock</h2>
              {stats.low_stock?.length === 0 ? (
                <p className="mt-4 text-sm text-gray-500">All active items have stock above 2.</p>
              ) : (
                <ul className="mt-4 space-y-2">
                  {stats.low_stock.map((p) => (
                    <li key={p.id} className="flex justify-between text-sm">
                      <Link
                        to={`${ROUTES.PRODUCT}/${p.slug}`}
                        className="text-amber-800 hover:underline"
                      >
                        {p.name}
                      </Link>
                      <span className="text-gray-600">Stock: {p.stock}</span>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>

          <div className="mt-10 rounded-xl border border-stone-200 bg-white p-5 shadow-sm">
            <h2 className="text-lg font-semibold text-gray-900">Recently updated</h2>
            <div className="mt-4 overflow-x-auto">
              <table className="w-full min-w-[520px] text-left text-sm">
                <thead>
                  <tr className="border-b border-stone-200 text-gray-500">
                    <th className="pb-2 pr-4 font-medium">Painting</th>
                    <th className="pb-2 pr-4 font-medium">Artist</th>
                    <th className="pb-2 pr-4 font-medium">Category</th>
                    <th className="pb-2 pr-4 font-medium">Price</th>
                    <th className="pb-2 font-medium">Stock</th>
                  </tr>
                </thead>
                <tbody>
                  {stats.recent_products?.map((p) => (
                    <tr key={p.id} className="border-b border-stone-100 last:border-0">
                      <td className="py-2 pr-4">
                        <Link
                          to={`${ROUTES.PRODUCT}/${p.slug}`}
                          className="font-medium text-amber-800 hover:underline"
                        >
                          {p.name}
                        </Link>
                        {p.is_featured && (
                          <span className="ml-2 text-xs text-amber-600">Featured</span>
                        )}
                      </td>
                      <td className="py-2 pr-4 text-gray-700">{p.artist_name || '—'}</td>
                      <td className="py-2 pr-4 text-gray-700">{p.category__name}</td>
                      <td className="py-2 pr-4 text-gray-900">{formatPrice(p.price)}</td>
                      <td className="py-2 text-gray-700">{p.stock}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </section>
  )
}

export default AdminDashboard
