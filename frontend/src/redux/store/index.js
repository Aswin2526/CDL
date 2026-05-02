import { configureStore } from '@reduxjs/toolkit'
import authReducer from '../auth/authSlice'
import productReducer from '../product/productSlice'
import wishlistReducer from '../wishlist/wishlistSlice'
import cartReducer from '../cart/cartSlice'

export const store = configureStore({
  reducer: {
    auth: authReducer,
    products: productReducer,
    wishlist: wishlistReducer,
    cart: cartReducer,
  },
})
