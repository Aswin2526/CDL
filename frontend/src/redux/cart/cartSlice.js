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
  async ({ productId, quantity }, { rejectWithValue }) => {
    try {
      const { data } = await cartService.updateCartQuantity(productId, quantity)
      return data
    } catch (err) {
      return rejectWithValue(err.response?.data)
    }
  },
)

const applyCartPayload = (state, cart) => {
  state.items = cart?.items ?? []
  state.itemCount = cart?.item_count ?? 0
  state.subtotal = cart?.subtotal ?? '0'
  state.productIds = state.items.map((item) => item.product.id)
}

const cartSlice = createSlice({
  name: 'cart',
  initialState: {
    items: [],
    productIds: [],
    itemCount: 0,
    subtotal: '0',
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
        state.updatingProductId = action.meta.arg.productId
        state.error = null
      })
      .addCase(updateCartItemQuantity.fulfilled, (state, action) => {
        state.updatingProductId = null
        state.lastMessage = action.payload.message
        applyCartPayload(state, action.payload.cart)
      })
      .addCase(updateCartItemQuantity.rejected, (state, action) => {
        state.updatingProductId = null
        state.error = action.payload?.detail || 'Could not update quantity.'
      })
  },
})

export const { clearCartMessage, resetCart } = cartSlice.actions
export const selectIsInCart = (productId) => (state) =>
  state.cart.productIds.includes(productId)
export const selectCartItemCount = (state) => state.cart.itemCount

export default cartSlice.reducer
