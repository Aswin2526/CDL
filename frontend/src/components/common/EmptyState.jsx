function EmptyState({ title, message, action }) {
  return (
    <div className="rounded-xl border border-dashed border-gray-300 bg-gray-50 px-6 py-16 text-center">
      <p className="text-lg font-semibold text-gray-800">{title}</p>
      {message && <p className="mt-2 text-sm text-gray-500">{message}</p>}
      {action && <div className="mt-6">{action}</div>}
    </div>
  )
}

export default EmptyState
