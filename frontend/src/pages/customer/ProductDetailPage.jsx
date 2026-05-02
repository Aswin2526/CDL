import { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { loadProductDetail } from '../../redux/product/productSlice'
import { toggleWishlistItem, selectIsInWishlist } from '../../redux/wishlist/wishlistSlice'
import { addCartItem, selectIsInCart } from '../../redux/cart/cartSlice'
import { selectIsAuthenticated } from '../../redux/auth/authSlice'
import { addProductReview, fetchProductReviews } from '../../services/productService'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import EmptyState from '../../components/common/EmptyState'
import StarRating, { StarOutline } from '../../components/common/StarRating'
import {
  ROUTES,
  PLACEHOLDER_IMAGE,
  resolveMediaUrl,
  formatPrice,
  formatMedium,
} from '../../utils/constants'

function ProductDetailPage() {
  const { slug } = useParams()
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const isAuthenticated = useSelector(selectIsAuthenticated)
  const { detail, detailLoading, detailError } = useSelector((state) => state.products)
  const inWishlist = useSelector(selectIsInWishlist(detail?.id))
  const inCart = useSelector(selectIsInCart(detail?.id))
  const cartAdding = useSelector((state) => state.cart.adding)
  const cartError = useSelector((state) => state.cart.error)

  const [reviews, setReviews] = useState([])
  const [reviewForm, setReviewForm] = useState({ rating: 5, comment: '' })
  const [reviewMsg, setReviewMsg] = useState('')
  const [activeImage, setActiveImage] = useState(0)

  useEffect(() => {
    if (slug) dispatch(loadProductDetail(slug))
  }, [slug, dispatch])

  useEffect(() => {
    if (detail?.id) {
      fetchProductReviews(detail.id)
        .then((res) => setReviews(res.data.results ?? res.data))
        .catch(() => setReviews(detail.reviews || []))
    }
  }, [detail])

  const images =
    detail?.images?.length > 0
      ? detail.images.map((img) => resolveMediaUrl(img.image))
      : [PLACEHOLDER_IMAGE]

  const handleReview = async (e) => {
    e.preventDefault()
    if (!isAuthenticated) return
    try {
      await addProductReview(detail.id, reviewForm)
      setReviewMsg('Review submitted!')
      const res = await fetchProductReviews(detail.id)
      setReviews(res.data.results ?? res.data)
      dispatch(loadProductDetail(slug))
      setReviewForm({ rating: 5, comment: '' })
    } catch (err) {
      setReviewMsg(err.response?.data?.detail || 'Could not submit review.')
    }
  }

  if (detailLoading) return <LoadingSpinner label="Loading artwork..." />
  if (detailError || !detail) {
    return (
      <EmptyState
        title="Artwork not found"
        message="This piece may have been sold or removed from the gallery."
        action={
          <Link to={ROUTES.SHOP} className="text-amber-800 hover:underline">
            Back to gallery
          </Link>
        }
      />
    )
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8">
      <nav className="mb-6 text-sm text-gray-500">
        <Link to={ROUTES.HOME} className="hover:text-amber-800">Home</Link>
        <span className="mx-2">/</span>
        <Link to={ROUTES.SHOP} className="hover:text-amber-800">Gallery</Link>
        <span className="mx-2">/</span>
        <span className="text-gray-800">{detail.name}</span>
      </nav>

      <div className="grid gap-10 lg:grid-cols-2">
        <div>
          <div className="aspect-[4/5] overflow-hidden rounded-xl border border-stone-200 bg-stone-50">
            <img
              src={images[activeImage]}
              alt={detail.name}
              className="h-full w-full object-cover"
            />
          </div>
          {images.length > 1 && (
            <div className="mt-3 flex gap-2 overflow-x-auto">
              {images.map((src, i) => (
                <button
                  key={i}
                  type="button"
                  onClick={() => setActiveImage(i)}
                  className={`h-16 w-16 shrink-0 overflow-hidden rounded-lg border-2 ${
                    activeImage === i ? 'border-amber-600' : 'border-stone-200'
                  }`}
                >
                  <img src={src} alt="" className="h-full w-full object-cover" />
                </button>
              ))}
            </div>
          )}
        </div>

        <div>
          <h1 className="text-2xl font-bold text-gray-900 md:text-3xl">{detail.name}</h1>
          {detail.artist_name && (
            <p className="mt-2 text-lg text-stone-600">by {detail.artist_name}</p>
          )}
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <StarRating rating={detail.average_rating} size="lg" />
            <span className="text-sm text-gray-500">
              {detail.review_count} review{detail.review_count !== 1 ? 's' : ''}
            </span>
          </div>
          <p className="mt-4 text-3xl font-bold text-gray-900">{formatPrice(detail.price)}</p>

          <dl className="mt-6 grid grid-cols-2 gap-3 rounded-xl border border-stone-200 bg-stone-50 p-4 text-sm">
            {detail.medium && (
              <>
                <dt className="text-stone-500">Medium</dt>
                <dd className="font-medium text-gray-900">
                  {formatMedium(detail.medium, detail.medium_display)}
                </dd>
              </>
            )}
            {detail.dimensions && (
              <>
                <dt className="text-stone-500">Size</dt>
                <dd className="font-medium text-gray-900">{detail.dimensions}</dd>
              </>
            )}
            {detail.year_created && (
              <>
                <dt className="text-stone-500">Year</dt>
                <dd className="font-medium text-gray-900">{detail.year_created}</dd>
              </>
            )}
            <dt className="text-stone-500">Framed</dt>
            <dd className="font-medium text-gray-900">
              {detail.is_framed ? 'Yes' : 'Unframed'}
            </dd>
          </dl>

          <p
            className={`mt-4 inline-block rounded-full px-3 py-1 text-sm font-medium ${
              detail.in_stock
                ? 'bg-amber-50 text-amber-900'
                : 'bg-red-100 text-red-800'
            }`}
          >
            {detail.in_stock
              ? detail.stock === 1
                ? 'One-of-a-kind — available'
                : `Available (${detail.stock} in stock)`
              : 'Sold out'}
          </p>
          <p className="mt-6 leading-relaxed text-gray-600">{detail.description}</p>
          <p className="mt-4 text-sm text-gray-500">
            Style:{' '}
            <Link
              to={`${ROUTES.SHOP}?category=${detail.category?.slug}`}
              className="font-medium text-amber-800 hover:underline"
            >
              {detail.category?.name}
            </Link>
          </p>

          <div className="mt-8 flex flex-wrap gap-3">
            <button
              type="button"
              disabled={!detail.in_stock || cartAdding}
              onClick={() => {
                if (!isAuthenticated) {
                  window.location.href = ROUTES.LOGIN
                  return
                }
                if (inCart) {
                  navigate(ROUTES.CART)
                  return
                }
                dispatch(addCartItem(detail.id))
              }}
              className={`flex-1 rounded-lg py-3 font-semibold sm:flex-none sm:px-8 ${
                !detail.in_stock
                  ? 'cursor-not-allowed bg-stone-200 text-stone-500'
                  : inCart
                    ? 'border border-amber-600 bg-amber-50 text-amber-900 hover:bg-amber-100'
                    : 'bg-amber-600 text-white hover:bg-amber-700'
              }`}
            >
              {!detail.in_stock
                ? 'Sold out'
                : cartAdding
                  ? 'Adding…'
                  : inCart
                    ? 'In cart — view cart'
                    : 'Add to cart'}
            </button>
            {inCart && (
              <Link
                to={ROUTES.CART}
                className="rounded-lg border border-amber-600 px-6 py-3 font-medium text-amber-800 hover:bg-amber-50"
              >
                View cart
              </Link>
            )}
            <button
              type="button"
              onClick={() => {
                if (!isAuthenticated) {
                  window.location.href = ROUTES.LOGIN
                  return
                }
                dispatch(toggleWishlistItem(detail.id))
              }}
              className={`rounded-lg border px-6 py-3 font-medium ${
                inWishlist
                  ? 'border-red-300 bg-red-50 text-red-700'
                  : 'border-stone-300 text-gray-700 hover:border-amber-500'
              }`}
            >
              {inWishlist ? 'Saved to wishlist' : 'Save to wishlist'}
            </button>
          </div>
          {cartError && (
            <p className="mt-2 text-sm text-red-600">{cartError}</p>
          )}

          {detail.store && (
            <div className="mt-8 rounded-xl border border-stone-200 bg-stone-50 p-4">
              <h3 className="font-semibold text-gray-900">Sold by</h3>
              <p className="mt-1 text-gray-700">{detail.store.name}</p>
              {detail.store.address && (
                <p className="text-sm text-gray-500">{detail.store.address}</p>
              )}
            </div>
          )}
        </div>
      </div>

      <section className="mt-16 border-t border-stone-200 pt-12">
        <h2 className="flex items-center gap-2 text-xl font-bold text-gray-900">
          <StarOutline className="h-5 w-5" />
          Collector reviews
        </h2>

        {isAuthenticated && (
          <form
            onSubmit={handleReview}
            className="mt-6 max-w-lg rounded-xl border border-stone-200 bg-white p-4"
          >
            <label className="flex items-center gap-2 text-sm font-medium text-gray-700">
              <StarOutline className="h-5 w-5" />
              Your rating
            </label>
            <select
              value={reviewForm.rating}
              onChange={(e) => setReviewForm((f) => ({ ...f, rating: Number(e.target.value) }))}
              className="mt-1 rounded-lg border border-gray-300 px-3 py-2 text-sm"
            >
              {[5, 4, 3, 2, 1].map((n) => (
                <option key={n} value={n}>
                  {n} stars
                </option>
              ))}
            </select>
            <label className="mt-3 block text-sm font-medium text-gray-700">Comment</label>
            <textarea
              rows={3}
              value={reviewForm.comment}
              onChange={(e) => setReviewForm((f) => ({ ...f, comment: e.target.value }))}
              className="mt-1 w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
            {reviewMsg && <p className="mt-2 text-sm text-amber-700">{reviewMsg}</p>}
            <button
              type="submit"
              className="mt-3 rounded-lg bg-amber-700 px-4 py-2 text-sm font-medium text-white hover:bg-amber-700"
            >
              Submit review
            </button>
          </form>
        )}

        <div className="mt-8 space-y-4">
          {reviews.length === 0 && (
            <p className="text-gray-500">No reviews yet. Be the first to share your thoughts.</p>
          )}
          {reviews.map((r) => (
            <div key={r.id} className="rounded-lg border border-stone-100 bg-white p-4">
              <div className="flex items-center justify-between">
                <span className="font-medium text-gray-900">{r.user_name}</span>
                <StarRating rating={r.rating} />
              </div>
              {r.comment && <p className="mt-2 text-sm text-gray-600">{r.comment}</p>}
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}

export default ProductDetailPage
