import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { selectIsAuthenticated } from '../../redux/auth/authSlice'
import { toggleWishlistItem, selectIsInWishlist } from '../../redux/wishlist/wishlistSlice'
import { addCartItem, selectIsInCart } from '../../redux/cart/cartSlice'
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
  const inCart = useSelector(selectIsInCart(product.id))
  const adding = useSelector((state) => state.cart.adding)
  const image = resolveMediaUrl(product.primary_image)

  const handleWishlist = (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (!isAuthenticated) {
      window.location.href = ROUTES.LOGIN
      return
    }
    dispatch(toggleWishlistItem(product.id))
  }

  const handleAddToCart = (e) => {
    e.preventDefault()
    if (!isAuthenticated) {
      window.location.href = ROUTES.LOGIN
      return
    }
    dispatch(addCartItem(product.id))
  }

  return (
    <article className="group flex flex-col overflow-hidden rounded-xl border border-stone-200 bg-white shadow-sm transition hover:border-amber-200 hover:shadow-md">
      <div className="relative aspect-[4/5] overflow-hidden bg-stone-100">
        <Link
          to={`${ROUTES.PRODUCT}/${product.slug}`}
          className="block h-full w-full"
        >
          <img
            src={image}
            alt={product.name}
            className="h-full w-full object-cover transition duration-300 group-hover:scale-105"
          />
          {!product.in_stock && (
            <span className="absolute bottom-2 left-2 rounded bg-stone-800 px-2 py-0.5 text-xs text-white">
              Sold
            </span>
          )}
        </Link>
        <button
          type="button"
          onClick={handleWishlist}
          className={`absolute right-2 top-2 z-10 rounded-full border bg-white/95 p-2 text-sm shadow-sm backdrop-blur-sm ${
            inWishlist
              ? 'border-red-200 text-red-600'
              : 'border-stone-200 text-stone-600 hover:border-amber-500 hover:text-amber-800'
          }`}
          aria-label="Save to wishlist"
        >
          {inWishlist ? '♥' : '♡'}
        </button>
      </div>

      <div className="flex flex-1 flex-col p-4">
        <Link
          to={`${ROUTES.PRODUCT}/${product.slug}`}
          className="line-clamp-2 font-medium text-gray-900 hover:text-amber-800"
        >
          {product.name}
        </Link>
        <div className="mt-2">
          <StarRating rating={product.average_rating} />
        </div>
        <p className="mt-2 text-lg font-bold text-gray-900">{formatPrice(product.price)}</p>

        <div className="mt-auto pt-4">
          <button
            type="button"
            disabled={!product.in_stock || adding}
            onClick={handleAddToCart}
            className={`w-full rounded-lg py-2 text-sm font-semibold transition ${
              !product.in_stock
                ? 'cursor-not-allowed bg-stone-100 text-stone-400'
                : inCart
                  ? 'border border-amber-600 bg-amber-50 text-amber-900 hover:bg-amber-100'
                  : 'bg-amber-600 text-white hover:bg-amber-700'
            }`}
          >
            {!product.in_stock
              ? 'Sold out'
              : adding
                ? 'Adding…'
                : inCart
                  ? 'In cart'
                  : 'Add to cart'}
          </button>
        </div>
      </div>
    </article>
  )
}

export default ProductCard
