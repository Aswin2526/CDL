import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import * as productService from '../../services/productService'

export const loadProducts = createAsyncThunk(
  'products/loadList',
  async (params, { rejectWithValue }) => {
    try {
      const { data } = await productService.fetchProducts(params)
      return data
    } catch (err) {
      return rejectWithValue(err.response?.data || { detail: 'Failed to load products.' })
    }
  },
)

export const loadProductDetail = createAsyncThunk(
  'products/loadDetail',
  async (slug, { rejectWithValue }) => {
    try {
      const { data } = await productService.fetchProductDetail(slug)
      return data
    } catch (err) {
      return rejectWithValue(err.response?.data || { detail: 'Product not found.' })
    }
  },
)

export const loadCategories = createAsyncThunk(
  'products/loadCategories',
  async (_, { rejectWithValue }) => {
    try {
      const { data } = await productService.fetchCategories()
      return data
    } catch (err) {
      return rejectWithValue(err.response?.data)
    }
  },
)

/** Total active paintings in the gallery (unfiltered). */
export const loadGalleryTotalCount = createAsyncThunk(
  'products/loadGalleryTotal',
  async (_, { rejectWithValue }) => {
    try {
      const { data } = await productService.fetchProducts({ page: 1 })
      const list = data.results ?? data
      return data.count ?? list.length
    } catch (err) {
      return rejectWithValue(err.response?.data)
    }
  },
)

export const loadHomeData = createAsyncThunk(
  'products/loadHome',
  async (_, { rejectWithValue }) => {
    try {
      const [latest, topRated, categories] = await Promise.all([
        productService.fetchLatestProducts(),
        productService.fetchTopRatedProducts(),
        productService.fetchCategories(),
      ])
      return {
        latest: latest.data.results ?? latest.data,
        topRated: topRated.data.results ?? topRated.data,
        categories: categories.data.results ?? categories.data,
      }
    } catch (err) {
      return rejectWithValue(err.response?.data)
    }
  },
)

const productSlice = createSlice({
  name: 'products',
  initialState: {
    list: [],
    listCount: 0,
    totalAvailable: 0,
    listLoading: false,
    listError: null,
    detail: null,
    detailLoading: false,
    detailError: null,
    categories: [],
    latest: [],
    topRated: [],
    homeLoading: false,
    filters: {
      q: '',
      category: '',
      medium: '',
      min_price: '',
      max_price: '',
      min_rating: '',
      sort: 'latest',
      page: 1,
    },
  },
  reducers: {
    setFilters(state, action) {
      state.filters = { ...state.filters, ...action.payload }
    },
    resetFilters(state) {
      state.filters = {
        q: '',
        category: '',
        medium: '',
        min_price: '',
        max_price: '',
        min_rating: '',
        sort: 'latest',
        page: 1,
      }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(loadProducts.pending, (state) => {
        state.listLoading = true
        state.listError = null
      })
      .addCase(loadProducts.fulfilled, (state, action) => {
        state.listLoading = false
        state.list = action.payload.results ?? action.payload
        state.listCount = action.payload.count ?? state.list.length
      })
      .addCase(loadProducts.rejected, (state, action) => {
        state.listLoading = false
        state.listError = action.payload
      })
      .addCase(loadProductDetail.pending, (state) => {
        state.detailLoading = true
        state.detailError = null
      })
      .addCase(loadProductDetail.fulfilled, (state, action) => {
        state.detailLoading = false
        state.detail = action.payload
      })
      .addCase(loadProductDetail.rejected, (state, action) => {
        state.detailLoading = false
        state.detailError = action.payload
      })
      .addCase(loadCategories.fulfilled, (state, action) => {
        state.categories = action.payload.results ?? action.payload
      })
      .addCase(loadGalleryTotalCount.fulfilled, (state, action) => {
        state.totalAvailable = action.payload
      })
      .addCase(loadHomeData.pending, (state) => {
        state.homeLoading = true
      })
      .addCase(loadHomeData.fulfilled, (state, action) => {
        state.homeLoading = false
        state.latest = action.payload.latest
        state.topRated = action.payload.topRated
        state.categories = action.payload.categories
      })
      .addCase(loadHomeData.rejected, (state) => {
        state.homeLoading = false
      })
  },
})

export const { setFilters, resetFilters } = productSlice.actions
export default productSlice.reducer
