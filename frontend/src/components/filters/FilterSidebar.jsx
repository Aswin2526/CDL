import { MEDIUM_OPTIONS } from '../../utils/constants'

function FilterSidebar({ categories, filters, onChange, onApply, onReset }) {
  const handle = (key, value) => onChange({ [key]: value })

  return (
    <aside className="rounded-xl border border-stone-200 bg-white p-5 shadow-sm">
      <div className="flex items-center justify-between">
        <h2 className="font-semibold text-gray-900">Filters</h2>
        <button
          type="button"
          onClick={onReset}
          className="text-xs font-medium text-amber-800 hover:underline"
        >
          Clear all
        </button>
      </div>

      <div className="mt-5 space-y-5">
        <div>
          <label className="mb-2 block text-sm font-medium text-gray-700">Style</label>
          <select
            value={filters.category}
            onChange={(e) => handle('category', e.target.value)}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
          >
            <option value="">All styles</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.slug}>
                {cat.name} ({cat.product_count ?? 0})
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-gray-700">Medium</label>
          <select
            value={filters.medium}
            onChange={(e) => handle('medium', e.target.value)}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
          >
            {MEDIUM_OPTIONS.map((opt) => (
              <option key={opt.value || 'all'} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-gray-700">Price (Rs.)</label>
          <div className="flex gap-2">
            <input
              type="number"
              placeholder="Min"
              value={filters.min_price}
              onChange={(e) => handle('min_price', e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
            <input
              type="number"
              placeholder="Max"
              value={filters.max_price}
              onChange={(e) => handle('max_price', e.target.value)}
              className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
            />
          </div>
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-gray-700">Rating</label>
          <select
            value={filters.min_rating}
            onChange={(e) => handle('min_rating', e.target.value)}
            className="w-full rounded-lg border border-gray-300 px-3 py-2 text-sm"
          >
            <option value="">Any</option>
            <option value="4">4+ stars</option>
            <option value="3">3+ stars</option>
            <option value="2">2+ stars</option>
          </select>
        </div>

        <button
          type="button"
          onClick={onApply}
          className="w-full rounded-lg bg-amber-700 py-2.5 text-sm font-medium text-white hover:bg-amber-700"
        >
          Apply filters
        </button>
      </div>
    </aside>
  )
}

export default FilterSidebar
