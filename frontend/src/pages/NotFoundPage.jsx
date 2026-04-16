import { Link } from 'react-router-dom'

function NotFoundPage() {
  return (
    <section className="mx-auto max-w-7xl px-4 py-24 text-center">
      <h1 className="text-6xl font-bold text-gray-300">404</h1>
      <p className="mt-4 text-xl text-gray-600">Page not found</p>
      <Link
        to="/"
        className="mt-6 inline-block rounded-lg bg-amber-600 px-6 py-2 text-white hover:bg-amber-700"
      >
        Back to Home
      </Link>
    </section>
  )
}

export default NotFoundPage
