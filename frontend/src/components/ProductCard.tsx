import { useState } from 'react'
import { ProductWithLatestPrice } from '../api/types'
import { TrendingDown, TrendingUp, Minus, ExternalLink, Eye, Clock } from 'lucide-react'
import { Link } from 'react-router-dom'
import api from '../api/client'
import { formatCurrency } from '../utils/formatters'

interface ProductCardProps {
  product: ProductWithLatestPrice
  onUpdate?: () => void
}

export default function ProductCard({ product, onUpdate }: ProductCardProps) {
  const [scanFrequency, setScanFrequency] = useState(product.scan_frequency_minutes)
  const [updating, setUpdating] = useState(false)

  const handleFrequencyChange = async (newFrequency: number) => {
    try {
      setUpdating(true)
      setScanFrequency(newFrequency)
      await api.put(`/api/products/${product.id}`, {
        scan_frequency_minutes: newFrequency
      })
      if (onUpdate) onUpdate()
    } catch (error) {
      console.error('Error updating scan frequency:', error)
      setScanFrequency(product.scan_frequency_minutes) // Revert on error
    } finally {
      setUpdating(false)
    }
  }
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
            +{formatCurrency(Math.abs(product.price_change), product.currency).substring(1)} ({product.price_change_percent?.toFixed(1)}%)
          </span>
        </div>
      )
    }
    
    return (
      <div className="flex items-center text-green-600">
        <TrendingDown className="h-4 w-4 mr-1" />
        <span className="text-sm font-medium">
          -{formatCurrency(Math.abs(product.price_change), product.currency).substring(1)} ({Math.abs(product.price_change_percent || 0).toFixed(1)}%)
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
              {/* Auction Badge */}
              {product.is_auction && (
                <div className="flex items-center mb-2">
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                    🔨 Auction
                  </span>
                  {product.current_bid_count !== null && product.current_bid_count !== undefined && (
                    <span className="ml-2 text-xs text-gray-600">
                      {product.current_bid_count} {product.current_bid_count === 1 ? 'bid' : 'bids'}
                    </span>
                  )}
                </div>
              )}
              <div className="flex items-baseline mb-2">
                <span className="text-3xl font-bold text-gray-900">
                  {product.is_auction && <span className="text-sm text-gray-500 mr-1">Current:</span>}
                  {formatCurrency(product.current_price, product.currency)}
                </span>
              </div>
              {/* Buy It Now Price for Auctions */}
              {product.is_auction && product.buy_it_now_price && (
                <div className="text-sm text-blue-600 font-medium mb-1">
                  Buy It Now: {formatCurrency(product.buy_it_now_price, product.currency)}
                </div>
              )}
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

        {/* Scan Frequency Quick Edit */}
        <div className="mt-3 pt-3 border-t border-gray-100">
          <div className="flex items-center justify-between text-xs">
            <div className="flex items-center text-gray-500">
              <Clock className="h-3 w-3 mr-1" />
              <span>Scan every:</span>
            </div>
            <select
              value={scanFrequency}
              onChange={(e) => handleFrequencyChange(parseInt(e.target.value))}
              disabled={updating}
              className="text-xs rounded border-gray-300 focus:border-primary-500 focus:ring-primary-500 disabled:opacity-50"
            >
              <option value={5}>5 min</option>
              <option value={10}>10 min</option>
              <option value={15}>15 min</option>
              <option value={30}>30 min</option>
              <option value={60}>1 hour</option>
              <option value={120}>2 hours</option>
              <option value={240}>4 hours</option>
              <option value={480}>8 hours</option>
              <option value={1440}>24 hours</option>
            </select>
          </div>
        </div>

        {/* Last Scanned */}
        {product.last_scanned_at && (
          <p className="text-xs text-gray-400 mt-2">
            Last checked: {new Date(product.last_scanned_at + 'Z').toLocaleString()}
          </p>
        )}
      </div>
    </div>
  )
}


