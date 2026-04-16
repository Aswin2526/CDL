import ProductCard from './ProductCard'

function ProductGrid({ products }) {
  return (
    <div className="grid grid-cols-2 gap-4 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4">
      {products.map((product) => (
        <ProductCard key={product.id} product={product} />
      ))}
    </div>
  )
}

export default ProductGrid
