import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import * as productService from '../../services/productService'

function normalizeWishlistPayload(data) {
  if (Array.isArray(data)) return data
  if (Array.isArray(data?.results)) return data.results
  return []
}

export const loadWishlist = createAsyncThunk(
  'wishlist/load',
  async (_, { rejectWithValue }) => {
    try {
      const { data } = await productService.fetchWishlist()
      return normalizeWishlistPayload(data)
    } catch (err) {
      return rejectWithValue(err.response?.data)
    }
  },
)

export const toggleWishlistItem = createAsyncThunk(
  'wishlist/toggle',
  async (productId, { rejectWithValue, dispatch }) => {
    try {
      const { data } = await productService.toggleWishlist(productId)
      await dispatch(loadWishlist())
      return { productId, in_wishlist: data.in_wishlist }
    } catch (err) {
      await dispatch(loadWishlist())
      return rejectWithValue(err.response?.data)
    }
  },
)

const wishlistSlice = createSlice({
  name: 'wishlist',
  initialState: {
    items: [],
    ids: [],
    loading: false,
    togglingId: null,
    error: null,
  },
  reducers: {
    setWishlistIds(state, action) {
      state.ids = action.payload
    },
    resetWishlist(state) {
      state.items = []
      state.ids = []
      state.error = null
      state.togglingId = null
    },
    clearWishlistError(state) {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadWishlist.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(loadWishlist.fulfilled, (state, action) => {
        state.loading = false
        state.items = action.payload
        state.ids = action.payload.map((item) => item.product.id)
      })
      .addCase(loadWishlist.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload?.detail || 'Could not load wishlist.'
      })
      .addCase(toggleWishlistItem.pending, (state, action) => {
        state.togglingId = action.meta.arg
        state.error = null
        const productId = action.meta.arg
        const wasIn = state.ids.includes(productId)
        if (wasIn) {
          state.ids = state.ids.filter((id) => id !== productId)
          state.items = state.items.filter((item) => item.product.id !== productId)
        } else {
          state.ids.push(productId)
        }
      })
      .addCase(toggleWishlistItem.fulfilled, (state) => {
        state.togglingId = null
      })
      .addCase(toggleWishlistItem.rejected, (state, action) => {
        state.togglingId = null
        state.error = action.payload?.detail || 'Wishlist update failed.'
      })
  },
})

export const { setWishlistIds, resetWishlist, clearWishlistError } = wishlistSlice.actions
export const selectIsInWishlist = (productId) => (state) =>
  state.wishlist.ids.includes(productId)
export const selectWishlistCount = (state) => state.wishlist.ids.length

export default wishlistSlice.reducer
