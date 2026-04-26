export function StarOutline({ className = 'h-4 w-4' }) {
  return (
    <svg
      className={`shrink-0 text-amber-500 ${className}`}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.75"
      aria-hidden
    >
      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87L18.18 22 12 18.56 5.82 22 7 14.14l-5-4.87 6.91-1.01L12 2z" />
    </svg>
  )
}

function StarFilled({ className = 'h-4 w-4' }) {
  return (
    <svg
      className={`shrink-0 text-amber-400 ${className}`}
      viewBox="0 0 24 24"
      fill="currentColor"
      aria-hidden
    >
      <path d="M12 2l3.09 6.26L22 9.27l-5 4.87L18.18 22 12 18.56 5.82 22 7 14.14l-5-4.87 6.91-1.01L12 2z" />
    </svg>
  )
}

function StarPartial({ percent, className = 'h-4 w-4' }) {
  const width = `${Math.min(100, Math.max(0, percent))}%`
  return (
    <span className={`relative inline-block shrink-0 ${className}`} aria-hidden>
      <StarOutline className={`${className} block`} />
      <span
        className="absolute left-0 top-0 h-full overflow-hidden"
        style={{ width }}
      >
        <StarFilled className={`${className} block`} />
      </span>
    </span>
  )
}

function StarRating({ rating = 0, size = 'sm', showScore = true }) {
  const stars = [1, 2, 3, 4, 5]
  const iconClass = size === 'lg' ? 'h-5 w-5' : 'h-4 w-4'
  const value = Math.min(5, Math.max(0, Number(rating) || 0))
  const fullCount = Math.floor(value)
  const fraction = value - fullCount

  return (
    <div className="inline-flex items-center gap-0.5">
      {stars.map((star) => {
        if (star <= fullCount) {
          return <StarFilled key={star} className={iconClass} />
        }
        if (star === fullCount + 1 && fraction >= 0.25) {
          return (
            <StarPartial
              key={star}
              percent={fraction * 100}
              className={iconClass}
            />
          )
        }
        return <StarOutline key={star} className={iconClass} />
      })}
      {showScore && (
        <span className="ml-1 text-xs text-gray-500">({value.toFixed(1)})</span>
      )}
    </div>
  )
}

export default StarRating
