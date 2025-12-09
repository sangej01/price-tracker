import { ProductWithLatestPrice } from '../api/types'
import { TrendingDown, TrendingUp, Minus, ExternalLink, Eye } from 'lucide-react'
import { Link } from 'react-router-dom'

interface ProductCardProps {
  product: ProductWithLatestPrice
}

export default function ProductCard({ product }: ProductCardProps) {
  const getPriceChangeIndicator = () => {
    if (!product.price_change || product.price_change === 0) {
      return (
        <div className="flex items-center text-gray-500">
          <Minus className="h-4 w-4 mr-1" />
          <span className="text-sm">No change</span>
        </div>
      )
    }
    
    if (product.price_change > 0) {
      return (
        <div className="flex items-center text-red-600">
          <TrendingUp className="h-4 w-4 mr-1" />
          <span className="text-sm font-medium">
            +${Math.abs(product.price_change).toFixed(2)} ({product.price_change_percent?.toFixed(1)}%)
          </span>
        </div>
      )
    }
    
    return (
      <div className="flex items-center text-green-600">
        <TrendingDown className="h-4 w-4 mr-1" />
        <span className="text-sm font-medium">
          -${Math.abs(product.price_change).toFixed(2)} ({Math.abs(product.price_change_percent || 0).toFixed(1)}%)
        </span>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
      {/* Product Image */}
      <div className="aspect-w-16 aspect-h-9 bg-gray-100">
        {product.image_url ? (
          <img
            src={product.image_url}
            alt={product.name}
            className="w-full h-48 object-cover"
          />
        ) : (
          <div className="w-full h-48 flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100">
            <span className="text-4xl text-primary-300">📦</span>
          </div>
        )}
      </div>

      {/* Product Info */}
      <div className="p-5">
        <div className="flex items-start justify-between mb-2">
          <h3 className="text-lg font-semibold text-gray-900 line-clamp-2 flex-1">
            {product.name}
          </h3>
        </div>

        <p className="text-sm text-gray-500 mb-4">{product.vendor_name}</p>

        {/* Price Section */}
        <div className="mb-4">
          {product.current_price ? (
            <>
              <div className="flex items-baseline mb-2">
                <span className="text-3xl font-bold text-gray-900">
                  ${product.current_price.toFixed(2)}
                </span>
                <span className="ml-2 text-sm text-gray-500">{product.currency}</span>
              </div>
              {getPriceChangeIndicator()}
            </>
          ) : (
            <p className="text-gray-500">Price not available</p>
          )}
        </div>

        {/* Stock Status */}
        <div className="mb-4">
          {product.in_stock ? (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
              In Stock
            </span>
          ) : (
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800">
              Out of Stock
            </span>
          )}
        </div>

        {/* Actions */}
        <div className="flex gap-2">
          <Link
            to={`/products/${product.id}`}
            className="flex-1 inline-flex justify-center items-center px-4 py-2 border border-primary-600 rounded-md shadow-sm text-sm font-medium text-primary-600 bg-white hover:bg-primary-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <Eye className="h-4 w-4 mr-2" />
            View Details
          </Link>
          <a
            href={product.url}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
          >
            <ExternalLink className="h-4 w-4" />
          </a>
        </div>

        {/* Last Scanned */}
        {product.last_scanned_at && (
          <p className="text-xs text-gray-400 mt-3">
            Last checked: {new Date(product.last_scanned_at).toLocaleString()}
          </p>
        )}
      </div>
    </div>
  )
}


