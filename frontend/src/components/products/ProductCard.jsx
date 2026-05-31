import { Link, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { selectIsAdmin, selectIsAuthenticated } from '../../redux/auth/authSlice'
import {
  toggleWishlistItem,
  selectIsInWishlist,
} from '../../redux/wishlist/wishlistSlice'
import { addCartItem, selectIsInCart } from '../../redux/cart/cartSlice'
import {
  ROUTES,
  resolveMediaUrl,
  formatPrice,
} from '../../utils/constants'
import StarRating from '../common/StarRating'

function ProductCard({ product }) {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const isAuthenticated = useSelector(selectIsAuthenticated)
  const isAdmin = useSelector(selectIsAdmin)
  const canShop = isAuthenticated && !isAdmin
  const inWishlist = useSelector(selectIsInWishlist(product.id))
  const wishlistToggling = useSelector(
    (state) => state.wishlist.togglingId === product.id,
  )
  const inCart = useSelector(selectIsInCart(product.id))
  const adding = useSelector((state) => state.cart.adding)
  const image = resolveMediaUrl(product.primary_image)

  const handleWishlist = async (e) => {
    e.preventDefault()
    e.stopPropagation()
    if (!isAuthenticated) {
      navigate(ROUTES.LOGIN)
      return
    }
    await dispatch(toggleWishlistItem(product.id))
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
            className="h-full w-full object-contain transition duration-300 group-hover:scale-105"
          />
          {!product.in_stock && (
            <span className="absolute bottom-2 left-2 rounded bg-stone-800 px-2 py-0.5 text-xs text-white">
              Sold
            </span>
          )}
        </Link>
        {canShop && (
          <button
            type="button"
            onClick={handleWishlist}
            disabled={wishlistToggling}
            className={`absolute right-2 top-2 z-10 rounded-full border bg-white/95 p-2 text-lg leading-none shadow-sm backdrop-blur-sm transition ${
              inWishlist
                ? 'border-red-300 bg-red-50 text-red-600'
                : 'border-stone-200 text-stone-500 hover:border-red-200 hover:text-red-500'
            } disabled:opacity-60`}
            aria-label={inWishlist ? 'Remove from wishlist' : 'Add to wishlist'}
            aria-pressed={inWishlist}
          >
            {inWishlist ? '♥' : '♡'}
          </button>
        )}
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
          {canShop ? (
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
          ) : (
            <Link
              to={`${ROUTES.PRODUCT}/${product.slug}`}
              className="block w-full rounded-lg border border-stone-300 py-2 text-center text-sm font-semibold text-gray-700 hover:border-amber-400 hover:text-amber-800"
            >
              View artwork
            </Link>
          )}
        </div>
      </div>
    </article>
  )
}

export default ProductCard
