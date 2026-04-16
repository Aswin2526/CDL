import { useSelector } from 'react-redux'
import { selectAuth } from '../../redux/auth/authSlice'

function AdminDashboard() {
  const { user } = useSelector(selectAuth)

  return (
    <section className="mx-auto max-w-7xl px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900">Admin Dashboard</h1>
      <p className="mt-2 text-gray-600">
        Welcome, {user?.full_name}. Manage the store catalog, collectors, and orders.
      </p>
      <div className="mt-8 rounded-xl border border-amber-200 bg-amber-50 p-6">
        <p className="text-sm text-amber-900">
          ChitraBazar admin is active. Manage paintings and store settings in Django admin;
          orders expand in upcoming phases.
        </p>
      </div>
    </section>
  )
}

export default AdminDashboard
