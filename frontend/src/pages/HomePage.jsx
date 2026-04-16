import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import SearchBar from '../components/filters/SearchBar'
import ProductGrid from '../components/products/ProductGrid'
import LoadingSpinner from '../components/common/LoadingSpinner'
import { loadHomeData } from '../redux/product/productSlice'
import { loadWishlist } from '../redux/wishlist/wishlistSlice'
import { selectIsAuthenticated } from '../redux/auth/authSlice'
import { APP_NAME, APP_TAGLINE, ROUTES, CATEGORY_ICONS } from '../utils/constants'

function HomePage() {
  const dispatch = useDispatch()
  const isAuthenticated = useSelector(selectIsAuthenticated)
  const { featured, latest, topRated, categories, homeLoading } = useSelector(
    (state) => state.products,
  )

  useEffect(() => {
    dispatch(loadHomeData())
    if (isAuthenticated) dispatch(loadWishlist())
  }, [dispatch, isAuthenticated])

  return (
    <div>
      <section className="bg-gradient-to-br from-stone-900 via-amber-950 to-stone-800 text-white">
        <div className="mx-auto max-w-7xl px-4 py-16 md:py-24">
          <div className="max-w-2xl">
            <p className="text-sm font-medium uppercase tracking-widest text-amber-200/90">
              {APP_TAGLINE}
            </p>
            <h1 className="mt-3 text-3xl font-bold tracking-tight md:text-5xl">
              Discover original paintings
            </h1>
            <p className="mt-4 text-lg text-stone-200">
              {APP_NAME} is your single destination for original paintings.
              Browse landscapes, portraits, abstracts, and contemporary works — each
              piece sold with authenticity guaranteed.
            </p>
            <div className="mt-8 flex flex-wrap gap-3">
              <Link
                to={ROUTES.SHOP}
                className="rounded-lg bg-amber-500 px-6 py-3 font-semibold text-stone-900 shadow hover:bg-amber-400"
              >
                Browse gallery
              </Link>
              <Link
                to={ROUTES.REGISTER}
                className="rounded-lg border-2 border-amber-200/60 px-6 py-3 font-semibold text-white hover:bg-white/10"
              >
                Join as collector
              </Link>
            </div>
          </div>
          <div className="mt-10 max-w-xl">
            <SearchBar className="shadow-lg" />
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-12">
        <h2 className="text-xl font-bold text-gray-900 md:text-2xl">Browse by style</h2>
        {homeLoading ? (
          <LoadingSpinner />
        ) : (
          <div className="mt-6 grid grid-cols-2 gap-3 sm:grid-cols-3 md:grid-cols-5">
            {categories.map((cat) => (
              <Link
                key={cat.id}
                to={`${ROUTES.SHOP}?category=${cat.slug}`}
                className="rounded-xl border border-stone-200 bg-white p-4 text-center shadow-sm transition hover:border-amber-300 hover:shadow-md"
              >
                <span className="text-2xl">{CATEGORY_ICONS[cat.slug] || '🖼️'}</span>
                <p className="mt-2 font-medium text-gray-900">{cat.name}</p>
                <p className="text-xs text-gray-500">{cat.product_count ?? 0} works</p>
              </Link>
            ))}
          </div>
        )}
      </section>

      <section className="bg-stone-50 py-12">
        <div className="mx-auto max-w-7xl px-4">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold text-gray-900 md:text-2xl">Featured artworks</h2>
            <Link to={ROUTES.SHOP} className="text-sm font-medium text-amber-800 hover:underline">
              View all
            </Link>
          </div>
          {homeLoading ? (
            <LoadingSpinner />
          ) : (
            <div className="mt-6">
              <ProductGrid products={featured} />
            </div>
          )}
        </div>
      </section>

      <section className="mx-auto max-w-7xl px-4 py-12">
        <div className="flex items-center justify-between">
          <h2 className="text-xl font-bold text-gray-900 md:text-2xl">New arrivals</h2>
          <Link
            to={`${ROUTES.SHOP}?sort=latest`}
            className="text-sm font-medium text-amber-800 hover:underline"
          >
            See more
          </Link>
        </div>
        {homeLoading ? (
          <LoadingSpinner />
        ) : (
          <div className="mt-6">
            <ProductGrid products={latest} />
          </div>
        )}
      </section>

      {topRated?.length > 0 && (
        <section className="bg-stone-50 py-12">
          <div className="mx-auto max-w-7xl px-4">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-gray-900 md:text-2xl">Collector favorites</h2>
              <Link
                to={`${ROUTES.SHOP}?sort=top_rated`}
                className="text-sm font-medium text-amber-800 hover:underline"
              >
                See more
              </Link>
            </div>
            <div className="mt-6">
              <ProductGrid products={topRated} />
            </div>
          </div>
        </section>
      )}

      <section className="border-t border-stone-200 bg-white py-12">
        <div className="mx-auto max-w-7xl px-4 text-center">
          <h2 className="text-2xl font-bold text-gray-900">Start your collection today</h2>
          <p className="mt-2 text-gray-600">
            Curated original paintings, secure checkout, and insured delivery.
          </p>
          <Link
            to={ROUTES.SHOP}
            className="mt-6 inline-block rounded-lg bg-amber-700 px-8 py-3 font-semibold text-white hover:bg-amber-800"
          >
            Explore the gallery
          </Link>
        </div>
      </section>
    </div>
  )
}

export default HomePage
