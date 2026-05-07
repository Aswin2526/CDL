import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { loadWishlist } from '../../redux/wishlist/wishlistSlice'
import ProductGrid from '../../components/products/ProductGrid'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import EmptyState from '../../components/common/EmptyState'
import { ROUTES } from '../../utils/constants'

function WishlistPage() {
  const dispatch = useDispatch()
  const { items, loading, error } = useSelector((state) => state.wishlist)
  const products = items.map((item) => item.product).filter(Boolean)

  useEffect(() => {
    dispatch(loadWishlist())
  }, [dispatch])

  return (
    <div className="mx-auto max-w-7xl px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 md:text-3xl">Saved artworks</h1>
      <p className="mt-1 text-gray-500">Paintings you want to revisit or purchase later</p>

      {error && (
        <p className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
          {typeof error === 'string' ? error : error.detail || 'Could not load wishlist.'}
        </p>
      )}

      {loading && <LoadingSpinner />}
      {!loading && products.length === 0 && (
        <div className="mt-8">
          <EmptyState
            title="No saved artworks yet"
            message="Browse the gallery and tap the heart to save paintings you love."
            action={
              <Link
                to={ROUTES.SHOP}
                className="inline-block rounded-lg bg-amber-700 px-6 py-2 text-white hover:bg-amber-800"
              >
                Browse gallery
              </Link>
            }
          />
        </div>
      )}
      {!loading && products.length > 0 && (
        <div className="mt-8">
          <ProductGrid products={products} />
        </div>
      )}
    </div>
  )
}

export default WishlistPage
