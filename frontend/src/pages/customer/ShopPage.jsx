import { useEffect, useCallback } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useSearchParams } from 'react-router-dom'
import FilterSidebar from '../../components/filters/FilterSidebar'
import SortDropdown from '../../components/filters/SortDropdown'
import ProductGrid from '../../components/products/ProductGrid'
import LoadingSpinner from '../../components/common/LoadingSpinner'
import EmptyState from '../../components/common/EmptyState'
import {
  loadProducts,
  loadCategories,
  loadGalleryTotalCount,
  setFilters,
  resetFilters,
} from '../../redux/product/productSlice'
import { loadWishlist } from '../../redux/wishlist/wishlistSlice'
import { selectIsAuthenticated } from '../../redux/auth/authSlice'

function ShopPage() {
  const dispatch = useDispatch()
  const [searchParams, setSearchParams] = useSearchParams()
  const isAuthenticated = useSelector(selectIsAuthenticated)
  const { list, listCount, totalAvailable, listLoading, listError, categories, filters } =
    useSelector((state) => state.products)

  const buildParams = useCallback(() => {
    const params = { sort: filters.sort, page: filters.page }
    if (filters.q) params.q = filters.q
    if (filters.category) params.category = filters.category
    if (filters.medium) params.medium = filters.medium
    if (filters.min_price) params.min_price = filters.min_price
    if (filters.max_price) params.max_price = filters.max_price
    if (filters.min_rating) params.min_rating = filters.min_rating
    return params
  }, [filters])

  useEffect(() => {
    dispatch(
      setFilters({
        q: searchParams.get('q') || '',
        category: searchParams.get('category') || '',
        medium: searchParams.get('medium') || '',
        min_price: searchParams.get('min_price') || '',
        max_price: searchParams.get('max_price') || '',
        min_rating: searchParams.get('min_rating') || '',
        sort: searchParams.get('sort') || 'latest',
        page: Number(searchParams.get('page')) || 1,
      }),
    )
  }, [searchParams, dispatch])

  useEffect(() => {
    dispatch(loadCategories())
    dispatch(loadGalleryTotalCount())
    if (isAuthenticated) dispatch(loadWishlist())
  }, [dispatch, isAuthenticated])

  useEffect(() => {
    dispatch(loadProducts(buildParams()))
  }, [dispatch, buildParams])

  const applyFilters = () => {
    const next = new URLSearchParams()
    Object.entries(filters).forEach(([key, val]) => {
      if (val !== '' && val != null) next.set(key, String(val))
    })
    setSearchParams(next)
  }

  const handleReset = () => {
    dispatch(resetFilters())
    setSearchParams({})
  }

  return (
    <div className="mx-auto max-w-7xl px-4 py-8">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900 md:text-3xl">Gallery</h1>
        <p className="mt-1 text-gray-500">
          {totalAvailable > 0
            ? `${totalAvailable} painting${totalAvailable !== 1 ? 's' : ''} available`
            : 'Browse original artworks from our gallery'}
        </p>
      </div>

      <div className="flex flex-col gap-8 lg:flex-row">
        <div className="w-full shrink-0 lg:w-64">
          <FilterSidebar
            categories={categories}
            filters={filters}
            onChange={(patch) => dispatch(setFilters(patch))}
            onApply={applyFilters}
            onReset={handleReset}
          />
        </div>

        <div className="min-w-0 flex-1">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm text-gray-600">
              Showing {listCount > 0 ? listCount : list.length} artwork
              {(listCount > 0 ? listCount : list.length) !== 1 ? 's' : ''}
            </p>
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">Sort:</span>
              <SortDropdown
                value={filters.sort}
                onChange={(sort) => {
                  dispatch(setFilters({ sort }))
                  const next = new URLSearchParams(searchParams)
                  next.set('sort', sort)
                  setSearchParams(next)
                }}
              />
            </div>
          </div>

          {listLoading && <LoadingSpinner />}
          {!listLoading && listError && (
            <EmptyState title="Something went wrong" message={listError.detail || 'Try again later.'} />
          )}
          {!listLoading && !listError && list.length === 0 && (
            <EmptyState
              title="No paintings found"
              message="Try adjusting your style or medium filters."
            />
          )}
          {!listLoading && !listError && list.length > 0 && <ProductGrid products={list} />}
        </div>
      </div>
    </div>
  )
}

export default ShopPage
