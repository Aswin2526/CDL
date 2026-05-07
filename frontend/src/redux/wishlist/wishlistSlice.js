import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import * as productService from '../../services/productService'

export const loadWishlist = createAsyncThunk(
  'wishlist/load',
  async (_, { rejectWithValue }) => {
    try {
      const { data } = await productService.fetchWishlist()
      return data.results ?? data
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
      return { productId, ...data }
    } catch (err) {
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
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadWishlist.pending, (state) => {
        state.loading = true
      })
      .addCase(loadWishlist.fulfilled, (state, action) => {
        state.loading = false
        state.items = action.payload
        state.ids = action.payload.map((item) => item.product.id)
      })
      .addCase(loadWishlist.rejected, (state) => {
        state.loading = false
      })
      .addCase(toggleWishlistItem.pending, (state) => {
        state.error = null
      })
      .addCase(toggleWishlistItem.fulfilled, (state) => {
        // loadWishlist runs in the thunk; fulfilled state comes from that chain
      })
      .addCase(toggleWishlistItem.rejected, (state, action) => {
        state.error = action.payload?.detail || 'Wishlist update failed.'
      })
  },
})

export const { setWishlistIds, resetWishlist } = wishlistSlice.actions
export const selectIsInWishlist = (productId) => (state) =>
  state.wishlist.ids.includes(productId)
export const selectWishlistCount = (state) => state.wishlist.ids.length

export default wishlistSlice.reducer
