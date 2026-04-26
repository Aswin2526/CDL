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

function StarRating({ rating = 0, size = 'sm', showScore = true }) {
  const stars = [1, 2, 3, 4, 5]
  const iconClass = size === 'lg' ? 'h-5 w-5' : 'h-4 w-4'
  const rounded = Math.round(Number(rating) || 0)

  return (
    <div className="inline-flex items-center gap-0.5">
      <StarOutline className={iconClass} />
      {stars.map((star) =>
        star <= rounded ? (
          <StarFilled key={star} className={iconClass} />
        ) : (
          <StarOutline key={star} className={iconClass} />
        ),
      )}
      {showScore && (
        <span className="ml-1 text-xs text-gray-500">
          ({Number(rating).toFixed(1)})
        </span>
      )}
    </div>
  )
}

export default StarRating
