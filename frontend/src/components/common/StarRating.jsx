function StarRating({ rating = 0, size = 'sm' }) {
  const stars = [1, 2, 3, 4, 5]
  const sizeClass = size === 'lg' ? 'text-lg' : 'text-sm'

  return (
    <div className={`flex items-center gap-0.5 text-amber-400 ${sizeClass}`}>
      {stars.map((star) => (
        <span key={star}>{star <= Math.round(rating) ? '★' : '☆'}</span>
      ))}
      <span className="ml-1 text-xs text-gray-500">({Number(rating).toFixed(1)})</span>
    </div>
  )
}

export default StarRating
