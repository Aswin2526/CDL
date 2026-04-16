import { Link } from 'react-router-dom'
import { useSelector } from 'react-redux'
import { selectAuth } from '../../redux/auth/authSlice'
import { ROUTES } from '../../utils/constants'

function CustomerHome() {
  const { user } = useSelector(selectAuth)

  return (
    <section className="mx-auto max-w-7xl px-4 py-12">
      <h1 className="text-3xl font-bold text-gray-900">My Collection</h1>
      <p className="mt-2 text-gray-600">
        Welcome, {user?.full_name}. Browse the gallery and save pieces you love.
      </p>
      <div className="mt-8 rounded-xl border border-stone-200 bg-white p-6 shadow-sm">
        <p className="text-gray-600">
          Your collector profile is ready. Checkout and order tracking arrive in the
          next project phase.
        </p>
        <Link
          to={ROUTES.SHOP}
          className="mt-4 inline-block rounded-lg bg-amber-700 px-5 py-2 text-sm font-medium text-white hover:bg-amber-800"
        >
          Browse gallery
        </Link>
      </div>
    </section>
  )
}

export default CustomerHome
