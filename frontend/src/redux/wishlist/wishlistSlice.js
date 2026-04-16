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
  async (productId, { rejectWithValue }) => {
    try {
      const { data } = await productService.toggleWishlist(productId)
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
      .addCase(toggleWishlistItem.fulfilled, (state, action) => {
        const { productId, in_wishlist } = action.payload
        if (in_wishlist) {
          if (!state.ids.includes(productId)) state.ids.push(productId)
        } else {
          state.ids = state.ids.filter((id) => id !== productId)
          state.items = state.items.filter((item) => item.product.id !== productId)
        }
      })
  },
})

export const { setWishlistIds } = wishlistSlice.actions
export const selectIsInWishlist = (productId) => (state) =>
  state.wishlist.ids.includes(productId)

export default wishlistSlice.reducer
