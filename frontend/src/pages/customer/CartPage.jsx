import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import {
  loadCart,
  removeCartItem,
  updateCartItemQuantity,
  clearCartMessage,
  setCartError,
} from '../../redux/cart/cartSlice'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import EmptyState from '../../components/common/EmptyState'
import {
  ROUTES,
  resolveMediaUrl,
  formatPrice,
  PLACEHOLDER_IMAGE,
} from '../../utils/constants'

function formatCartError(error) {
  if (!error) return null
  if (typeof error === 'string') return error
  return error.detail || 'Something went wrong.'
}

function CartPage() {
  const dispatch = useDispatch()
  const {
    items,
    subtotal,
    total,
    bulkDiscountEligible,
    discountAmount,
    loading,
    updatingProductId,
    error,
  } = useSelector((state) => state.cart)

  useEffect(() => {
    dispatch(loadCart())
  }, [dispatch])

  const handleRemove = (productId) => {
    dispatch(removeCartItem(productId))
  }

  const setQuantity = (productId, currentQty, nextQty, maxStock) => {
    if (nextQty < 1) {
      dispatch(removeCartItem(productId))
      return
    }
    if (nextQty > maxStock) {
      dispatch(
        setCartError(
          maxStock === 1
            ? 'This original painting is one-of-a-kind — only 1 available.'
            : `Only ${maxStock} available.`,
        ),
      )
      return
    }
    if (nextQty === currentQty) return
    dispatch(clearCartMessage())
    dispatch(updateCartItemQuantity({ productId, quantity: nextQty }))
  }

  const handleQuantityChange = (productId, currentQty, delta, maxStock) => {
    setQuantity(productId, currentQty, currentQty + delta, maxStock)
  }

  const handleQuantityInput = (productId, currentQty, rawValue, maxStock) => {
    const nextQty = parseInt(rawValue, 10)
    if (Number.isNaN(nextQty)) return
    setQuantity(productId, currentQty, nextQty, maxStock)
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 md:text-3xl">Your cart</h1>
      <p className="mt-1 text-gray-500">Original paintings ready to purchase</p>

      {loading && <LoadingSpinner />}

      {!loading && items.length === 0 && (
        <div className="mt-8">
          <EmptyState
            title="Your cart is empty"
            message="Browse the gallery and add paintings you would like to buy."
            action={
              <Link
                to={ROUTES.SHOP}
                className="inline-block rounded-lg bg-amber-600 px-6 py-2 font-medium text-white hover:bg-amber-700"
              >
                Browse gallery
              </Link>
            }
          />
        </div>
      )}

      {error && (
        <p className="mt-4 rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700">
          {formatCartError(error)}
        </p>
      )}

      {!loading && items.length > 0 && (
        <div className="mt-8 grid gap-8 lg:grid-cols-3">
          <ul className="space-y-4 lg:col-span-2">
            {items.map((item) => {
              const p = item.product
              const maxStock = Math.max(1, Number(p.stock) || 1)
              const isUpdating = updatingProductId === p.id
              const image = resolveMediaUrl(p.primary_image) || PLACEHOLDER_IMAGE
              return (
                <li
                  key={item.id}
                  className="flex items-center gap-4 rounded-xl border border-stone-200 bg-white p-4 shadow-sm"
                >
                  <Link
                    to={`${ROUTES.PRODUCT}/${p.slug}`}
                    className="h-28 w-24 shrink-0 overflow-hidden rounded-lg bg-stone-100"
                  >
                    <img src={image} alt={p.name} className="h-full w-full object-contain bg-stone-100" />
                  </Link>
                  <div className="min-w-0 flex-1">
                    <Link
                      to={`${ROUTES.PRODUCT}/${p.slug}`}
                      className="font-medium text-gray-900 hover:text-amber-800"
                    >
                      {p.name}
                    </Link>
                    <div className="mt-2 flex flex-wrap items-center gap-2">
                      <span className="text-sm text-gray-500">Qty</span>
                      <div className="inline-flex items-center rounded-lg border border-stone-200 bg-white">
                        <button
                          type="button"
                          disabled={isUpdating}
                          onClick={() =>
                            handleQuantityChange(p.id, item.quantity, -1, maxStock)
                          }
                          className="px-3 py-1.5 text-lg leading-none text-gray-700 hover:bg-stone-100 disabled:opacity-50"
                          aria-label="Decrease quantity"
                        >
                          −
                        </button>
                        <input
                          type="number"
                          min={1}
                          max={maxStock}
                          value={item.quantity}
                          disabled={isUpdating}
                          onChange={(e) =>
                            handleQuantityInput(
                              p.id,
                              item.quantity,
                              e.target.value,
                              maxStock,
                            )
                          }
                          className="w-12 border-x border-stone-200 py-1.5 text-center text-sm font-medium text-gray-900 [appearance:textfield] [&::-webkit-inner-spin-button]:appearance-none [&::-webkit-outer-spin-button]:appearance-none"
                          aria-label="Quantity"
                        />
                        <button
                          type="button"
                          disabled={isUpdating}
                          onClick={() =>
                            handleQuantityChange(p.id, item.quantity, 1, maxStock)
                          }
                          className="px-3 py-1.5 text-lg leading-none text-gray-700 hover:bg-stone-100 disabled:opacity-50"
                          aria-label="Increase quantity"
                        >
                          +
                        </button>
                      </div>
                      {maxStock === 1 && (
                        <span className="text-xs text-gray-400">1 piece only</span>
                      )}
                    </div>
                    <p className="mt-2 font-semibold text-gray-900">
                      {formatPrice(item.line_total)}
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={() => handleRemove(p.id)}
                    className="shrink-0 text-sm font-medium text-red-600 hover:text-red-800"
                  >
                    Remove
                  </button>
                </li>
              )
            })}
          </ul>

          <div className="h-fit rounded-xl border border-stone-200 bg-stone-50 p-6">
            <h2 className="text-lg font-semibold text-gray-900">Order summary</h2>
            <div className="mt-4 space-y-2 text-gray-700">
              <div className="flex justify-between">
                <span>Subtotal</span>
                <span>{formatPrice(subtotal)}</span>
              </div>
              {bulkDiscountEligible && (
                <div className="flex justify-between text-green-700">
                  <span>Bulk discount (5%)</span>
                  <span>−{formatPrice(discountAmount)}</span>
                </div>
              )}
              <div className="flex justify-between border-t border-stone-200 pt-2 text-base font-semibold text-gray-900">
                <span>Total</span>
                <span>{formatPrice(total)}</span>
              </div>
            </div>
            {bulkDiscountEligible ? (
              <p className="mt-3 rounded-lg bg-green-50 px-3 py-2 text-xs text-green-800">
                You saved 5% for ordering more than 1 piece.
              </p>
            ) : (
              <p className="mt-3 text-xs text-gray-500">
                Add another piece (qty 2+) to get 5% off your order.
              </p>
            )}
            <p className="mt-2 text-xs text-gray-500">
              Shipping and checkout will be available in the next update.
            </p>
            <button
              type="button"
              disabled
              className="mt-6 w-full cursor-not-allowed rounded-lg bg-stone-200 py-3 font-medium text-stone-500"
            >
              Proceed to checkout
            </button>
            <Link
              to={ROUTES.SHOP}
              className="mt-3 block text-center text-sm font-medium text-amber-800 hover:underline"
            >
              Continue shopping
            </Link>
          </div>
        </div>
      )}
    </div>
  )
}

export default CartPage
