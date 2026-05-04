import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import * as cartService from '../../services/cartService'

export const loadCart = createAsyncThunk('cart/load', async (_, { rejectWithValue }) => {
  try {
    const { data } = await cartService.fetchCart()
    return data
  } catch (err) {
    return rejectWithValue(err.response?.data)
  }
})

export const addCartItem = createAsyncThunk(
  'cart/add',
  async (productId, { rejectWithValue }) => {
    try {
      const { data } = await cartService.addToCart(productId)
      return data
    } catch (err) {
      return rejectWithValue(err.response?.data)
    }
  },
)

export const removeCartItem = createAsyncThunk(
  'cart/remove',
  async (productId, { rejectWithValue }) => {
    try {
      const { data } = await cartService.removeFromCart(productId)
      return data
    } catch (err) {
      return rejectWithValue(err.response?.data)
    }
  },
)

export const updateCartItemQuantity = createAsyncThunk(
  'cart/updateQuantity',
  async ({ productId, quantity }, { rejectWithValue, dispatch }) => {
    try {
      const { data } = await cartService.updateCartQuantity(productId, quantity)
      return data
    } catch (err) {
      dispatch(loadCart())
      return rejectWithValue(err.response?.data)
    }
  },
)

const BULK_DISCOUNT_RATE = 0.05

const calcCartTotals = (items) => {
  const subtotalNum = items.reduce(
    (sum, item) => sum + Number(item.product.price) * item.quantity,
    0,
  )
  const itemCount = items.reduce((sum, item) => sum + item.quantity, 0)
  const bulkDiscountEligible = itemCount > 1
  const discountAmount = bulkDiscountEligible ? subtotalNum * BULK_DISCOUNT_RATE : 0
  const total = subtotalNum - discountAmount
  return {
    subtotal: subtotalNum.toFixed(2),
    itemCount,
    bulkDiscountEligible,
    discountPercent: bulkDiscountEligible ? '5' : '0',
    discountAmount: discountAmount.toFixed(2),
    total: total.toFixed(2),
  }
}

const applyCartPayload = (state, cart) => {
  state.items = cart?.items ?? []
  state.itemCount = cart?.item_count ?? 0
  state.subtotal = cart?.subtotal ?? '0'
  state.bulkDiscountEligible = Boolean(cart?.bulk_discount_eligible)
  state.discountPercent = cart?.discount_percent ?? '0'
  state.discountAmount = cart?.discount_amount ?? '0'
  state.total = cart?.total ?? state.subtotal
  state.productIds = state.items.map((item) => item.product.id)
}

const recalcSubtotal = (state) => {
  const totals = calcCartTotals(state.items)
  state.subtotal = totals.subtotal
  state.itemCount = totals.itemCount
  state.bulkDiscountEligible = totals.bulkDiscountEligible
  state.discountPercent = totals.discountPercent
  state.discountAmount = totals.discountAmount
  state.total = totals.total
}

const applyOptimisticQuantity = (state, productId, quantity) => {
  const item = state.items.find((row) => row.product.id === productId)
  if (!item) return
  item.quantity = quantity
  item.line_total = (Number(item.product.price) * quantity).toFixed(2)
  recalcSubtotal(state)
}

const cartSlice = createSlice({
  name: 'cart',
  initialState: {
    items: [],
    productIds: [],
    itemCount: 0,
    subtotal: '0',
    bulkDiscountEligible: false,
    discountPercent: '0',
    discountAmount: '0',
    total: '0',
    loading: false,
    adding: false,
    updatingProductId: null,
    error: null,
    lastMessage: null,
  },
  reducers: {
    clearCartMessage(state) {
      state.lastMessage = null
      state.error = null
    },
    resetCart(state) {
      state.items = []
      state.productIds = []
      state.itemCount = 0
      state.subtotal = '0'
      state.bulkDiscountEligible = false
      state.discountPercent = '0'
      state.discountAmount = '0'
      state.total = '0'
    },
    setCartError(state, action) {
      state.error = action.payload
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadCart.pending, (state) => {
        state.loading = true
      })
      .addCase(loadCart.fulfilled, (state, action) => {
        state.loading = false
        applyCartPayload(state, action.payload)
      })
      .addCase(loadCart.rejected, (state) => {
        state.loading = false
      })
      .addCase(addCartItem.pending, (state) => {
        state.adding = true
        state.error = null
      })
      .addCase(addCartItem.fulfilled, (state, action) => {
        state.adding = false
        state.lastMessage = action.payload.message
        applyCartPayload(state, action.payload.cart)
      })
      .addCase(addCartItem.rejected, (state, action) => {
        state.adding = false
        state.error = action.payload?.detail || 'Could not add to cart.'
      })
      .addCase(removeCartItem.fulfilled, (state, action) => {
        state.lastMessage = action.payload.message
        applyCartPayload(state, action.payload.cart)
      })
      .addCase(updateCartItemQuantity.pending, (state, action) => {
        const { productId, quantity } = action.meta.arg
        state.updatingProductId = productId
        state.error = null
        applyOptimisticQuantity(state, productId, quantity)
      })
      .addCase(updateCartItemQuantity.fulfilled, (state, action) => {
        state.updatingProductId = null
        state.lastMessage = action.payload.message
        applyCartPayload(state, action.payload.cart)
      })
      .addCase(updateCartItemQuantity.rejected, (state, action) => {
        state.updatingProductId = null
        state.error =
          action.payload?.detail ||
          (typeof action.payload === 'string' ? action.payload : 'Could not update quantity.')
      })
  },
})

export const { clearCartMessage, resetCart, setCartError } = cartSlice.actions
export const selectIsInCart = (productId) => (state) =>
  state.cart.productIds.includes(productId)
export const selectCartItemCount = (state) => state.cart.itemCount

export default cartSlice.reducer
