import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { selectIsAuthenticated } from '../../redux/auth/authSlice'
import { toggleWishlistItem } from '../../redux/wishlist/wishlistSlice'
import { selectIsInWishlist } from '../../redux/wishlist/wishlistSlice'
import {
  ROUTES,
  resolveMediaUrl,
  formatPrice,
} from '../../utils/constants'
import StarRating from '../common/StarRating'

function ProductCard({ product }) {
  const dispatch = useDispatch()
  const isAuthenticated = useSelector(selectIsAuthenticated)
  const inWishlist = useSelector(selectIsInWishlist(product.id))
  const image = resolveMediaUrl(product.primary_image)

  const handleWishlist = (e) => {
    e.preventDefault()
    if (!isAuthenticated) {
      window.location.href = ROUTES.LOGIN
      return
    }
    dispatch(toggleWishlistItem(product.id))
  }

  return (
    <article className="group flex flex-col overflow-hidden rounded-xl border border-stone-200 bg-white shadow-sm transition hover:border-amber-200 hover:shadow-md">
      <Link
        to={`${ROUTES.PRODUCT}/${product.slug}`}
        className="relative block aspect-[4/5] overflow-hidden bg-stone-100"
      >
        <img
          src={image}
          alt={product.name}
          className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
        />
        {product.is_featured && (
          <span className="absolute left-2 top-2 rounded bg-amber-600 px-2 py-0.5 text-xs font-semibold text-white">
            Featured
          </span>
        )}
        {!product.in_stock && (
          <span className="absolute right-2 top-2 rounded bg-stone-800 px-2 py-0.5 text-xs text-white">
            Sold
          </span>
        )}
      </Link>

      <div className="flex flex-1 flex-col p-4">
        {product.artist_name && (
          <p className="text-xs font-medium text-amber-900">by {product.artist_name}</p>
        )}
        <Link
          to={`${ROUTES.PRODUCT}/${product.slug}`}
          className="mt-1 line-clamp-2 font-medium text-gray-900 hover:text-amber-800"
        >
          {product.name}
        </Link>
        <div className="mt-2">
          <StarRating rating={product.average_rating} />
        </div>
        <p className="mt-2 text-lg font-bold text-gray-900">{formatPrice(product.price)}</p>

        <div className="mt-auto flex gap-2 pt-4">
          <button
            type="button"
            disabled
            title="Checkout coming in next phase"
            className="flex-1 cursor-not-allowed rounded-lg bg-stone-100 py-2 text-sm font-medium text-stone-500"
          >
            Buy now
          </button>
          <button
            type="button"
            onClick={handleWishlist}
            className={`rounded-lg border px-3 py-2 text-sm ${
              inWishlist
                ? 'border-red-200 bg-red-50 text-red-600'
                : 'border-stone-300 text-stone-600 hover:border-amber-500 hover:text-amber-800'
            }`}
            aria-label="Save to wishlist"
          >
            {inWishlist ? '♥' : '♡'}
          </button>
        </div>
      </div>
    </article>
  )
}

export default ProductCard
