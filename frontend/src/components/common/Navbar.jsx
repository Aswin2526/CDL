import { Link, useNavigate } from 'react-router-dom'
import { useDispatch, useSelector } from 'react-redux'
import { logout, selectAuth, selectIsAuthenticated } from '../../redux/auth/authSlice'
import { selectCartItemCount } from '../../redux/cart/cartSlice'
import { selectWishlistCount } from '../../redux/wishlist/wishlistSlice'
import SearchBar from '../filters/SearchBar'
import { APP_NAME, ROUTES } from '../../utils/constants'

function Navbar() {
  const dispatch = useDispatch()
  const navigate = useNavigate()
  const isAuthenticated = useSelector(selectIsAuthenticated)
  const { user } = useSelector(selectAuth)
  const cartCount = useSelector(selectCartItemCount)
  const wishlistCount = useSelector(selectWishlistCount)

  const handleLogout = async () => {
    await dispatch(logout())
    navigate(ROUTES.HOME)
  }

  return (
    <header className="sticky top-0 z-50 border-b border-gray-200 bg-white shadow-sm">
      <nav className="mx-auto max-w-7xl px-4 py-3">
        <div className="flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
          <div className="flex items-center justify-between">
            <Link to="/" className="text-xl font-bold text-amber-700">
              {APP_NAME}
            </Link>
            <ul className="flex items-center gap-3 text-sm font-medium text-gray-600 md:hidden">
              <li>
                <Link to={ROUTES.SHOP}>Gallery</Link>
              </li>
              {isAuthenticated ? (
                <>
                  <li>
                    <Link to={ROUTES.CART}>Cart{cartCount > 0 ? ` (${cartCount})` : ''}</Link>
                  </li>
                  <li>
                    <Link
                      to={ROUTES.WISHLIST}
                      className={wishlistCount > 0 ? 'text-red-600' : ''}
                    >
                      ♥{wishlistCount > 0 ? ` (${wishlistCount})` : ''}
                    </Link>
                  </li>
                  {user?.role === 'customer' && (
                    <li>
                      <Link to={ROUTES.CUSTOMER_HOME}>Account</Link>
                    </li>
                  )}
                  <li>
                    <button type="button" onClick={handleLogout} className="text-amber-700">
                      Logout
                    </button>
                  </li>
                </>
              ) : (
                <>
                  <li>
                    <Link to={ROUTES.LOGIN}>Login</Link>
                  </li>
                  <li>
                    <Link to={ROUTES.REGISTER} className="text-amber-700">
                      Register
                    </Link>
                  </li>
                </>
              )}
            </ul>
          </div>
          <div className="hidden flex-1 max-w-md md:mx-6 md:block">
            <SearchBar />
          </div>
          <ul className="hidden items-center gap-5 text-sm font-medium text-gray-600 md:flex">
            <li>
              <Link to={ROUTES.HOME} className="hover:text-amber-700">
                Home
              </Link>
            </li>
            <li>
              <Link to={ROUTES.SHOP} className="hover:text-amber-700">
                Gallery
              </Link>
            </li>
            {isAuthenticated && (
              <>
                <li>
                  <Link to={ROUTES.CART} className="hover:text-amber-700">
                    Cart
                    {cartCount > 0 && (
                      <span className="ml-1 rounded-full bg-amber-600 px-1.5 py-0.5 text-xs text-white">
                        {cartCount}
                      </span>
                    )}
                  </Link>
                </li>
                <li>
                  <Link
                    to={ROUTES.WISHLIST}
                    className={`hover:text-amber-700 ${
                      wishlistCount > 0 ? 'text-red-600' : ''
                    }`}
                  >
                    Wishlist
                    {wishlistCount > 0 && (
                      <span className="ml-1 rounded-full bg-red-500 px-1.5 py-0.5 text-xs text-white">
                        {wishlistCount}
                      </span>
                    )}
                  </Link>
                </li>
              </>
            )}
            {isAuthenticated ? (
              <>
                {user?.role === 'admin' && (
                  <li>
                    <Link to={ROUTES.ADMIN_DASHBOARD} className="hover:text-amber-700">
                      Admin
                    </Link>
                  </li>
                )}
                {user?.role === 'customer' && (
                  <li>
                    <Link to={ROUTES.CUSTOMER_HOME} className="hover:text-amber-700">
                      My account
                    </Link>
                  </li>
                )}
                <li>
                  <button
                    type="button"
                    onClick={handleLogout}
                    className="rounded-lg border border-gray-300 px-3 py-1.5 hover:border-amber-600 hover:text-amber-700"
                  >
                    Logout
                  </button>
                </li>
              </>
            ) : (
              <>
                <li>
                  <Link to={ROUTES.LOGIN} className="hover:text-amber-700">
                    Login
                  </Link>
                </li>
                <li>
                  <Link
                    to={ROUTES.REGISTER}
                    className="rounded-lg bg-amber-600 px-3 py-1.5 text-white hover:bg-amber-700"
                  >
                    Register
                  </Link>
                </li>
              </>
            )}
          </ul>
        </div>
        <div className="md:hidden">
          <SearchBar />
        </div>
      </nav>
    </header>
  )
}

export default Navbar
