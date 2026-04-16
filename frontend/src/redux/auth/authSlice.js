import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'
import * as authService from '../../services/authService'
import { ROUTES, STORAGE_KEYS } from '../../utils/constants'

const savedUser = localStorage.getItem(STORAGE_KEYS.USER)

const initialState = {
  user: savedUser ? JSON.parse(savedUser) : null,
  accessToken: localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN),
  refreshToken: localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN),
  loading: false,
  error: null,
}

const persistAuth = (user, tokens) => {
  if (tokens?.access) {
    localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, tokens.access)
  }
  if (tokens?.refresh) {
    localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, tokens.refresh)
  }
  if (user) {
    localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user))
  }
}

const clearAuthStorage = () => {
  localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN)
  localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN)
  localStorage.removeItem(STORAGE_KEYS.USER)
}

export const register = createAsyncThunk(
  'auth/register',
  async (payload, { rejectWithValue }) => {
    try {
      const { data } = await authService.registerUser(payload)
      return data
    } catch (err) {
      return rejectWithValue(
        err.response?.data || { detail: 'Registration failed.' },
      )
    }
  },
)

export const login = createAsyncThunk(
  'auth/login',
  async (payload, { rejectWithValue }) => {
    try {
      const { data } = await authService.loginUser(payload)
      return data
    } catch (err) {
      return rejectWithValue(err.response?.data || { detail: 'Login failed.' })
    }
  },
)

export const logout = createAsyncThunk('auth/logout', async (_, { getState }) => {
  const { accessToken } = getState().auth
  if (accessToken) {
    try {
      await authService.logoutUser()
    } catch {
      // Clear local session even if API call fails
    }
  }
  clearAuthStorage()
})

const getDashboardRoute = (role) => {
  if (role === 'admin') return ROUTES.ADMIN_DASHBOARD
  return ROUTES.CUSTOMER_HOME
}

const authSlice = createSlice({
  name: 'auth',
  initialState,
  reducers: {
    clearError(state) {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(register.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(register.fulfilled, (state, action) => {
        state.loading = false
        state.user = action.payload.user
        state.accessToken = action.payload.tokens.access
        state.refreshToken = action.payload.tokens.refresh
        persistAuth(action.payload.user, action.payload.tokens)
      })
      .addCase(register.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      .addCase(login.pending, (state) => {
        state.loading = true
        state.error = null
      })
      .addCase(login.fulfilled, (state, action) => {
        state.loading = false
        state.user = action.payload.user
        state.accessToken = action.payload.access
        state.refreshToken = action.payload.refresh
        persistAuth(action.payload.user, {
          access: action.payload.access,
          refresh: action.payload.refresh,
        })
      })
      .addCase(login.rejected, (state, action) => {
        state.loading = false
        state.error = action.payload
      })
      .addCase(logout.fulfilled, (state) => {
        state.user = null
        state.accessToken = null
        state.refreshToken = null
        state.loading = false
        state.error = null
      })
  },
})

export const { clearError } = authSlice.actions
export const selectAuth = (state) => state.auth
export const selectIsAuthenticated = (state) => Boolean(state.auth.accessToken)
export { getDashboardRoute }
export default authSlice.reducer
