import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { ROUTES } from '../../utils/constants'

function SearchBar({ initialValue = '', className = '' }) {
  const [query, setQuery] = useState(initialValue)
  const navigate = useNavigate()

  const handleSubmit = (e) => {
    e.preventDefault()
    const q = query.trim()
    navigate(q ? `${ROUTES.SHOP}?q=${encodeURIComponent(q)}` : ROUTES.SHOP)
  }

  return (
    <form onSubmit={handleSubmit} className={`flex w-full ${className}`}>
      <input
        type="search"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search paintings, artists, styles..."
        className="w-full rounded-l-lg border border-gray-300 bg-white px-4 py-2.5 text-sm focus:border-amber-500 focus:outline-none focus:ring-1 focus:ring-amber-500"
      />
      <button
        type="submit"
        className="rounded-r-lg bg-amber-600 px-5 py-2.5 text-sm font-medium text-white hover:bg-amber-700"
      >
        Search
      </button>
    </form>
  )
}

export default SearchBar
