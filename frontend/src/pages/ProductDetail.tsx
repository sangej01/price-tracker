import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, ExternalLink, TrendingDown, TrendingUp, RefreshCw, Cpu } from 'lucide-react'
import { dashboardService, productService } from '../api/services'
import { ProductPriceStats } from '../api/types'
import PriceChart from '../components/PriceChart'

export default function ProductDetail() {
  const { id } = useParams<{ id: string }>()
  const navigate = useNavigate()
  const [stats, setStats] = useState<ProductPriceStats | null>(null)
  const [scraperInfo, setScraperInfo] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [scanning, setScanning] = useState(false)
  const [days, setDays] = useState(30)

  const fetchStats = async () => {
    if (!id) return
    try {
      setLoading(true)
      const [statsRes, scraperRes] = await Promise.all([
        dashboardService.getProductStats(parseInt(id), days),
        productService.getScraperInfo(parseInt(id))
      ])
      setStats(statsRes.data)
      setScraperInfo(scraperRes.data)
    } catch (error) {
      console.error('Error fetching product stats:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleScan = async () => {
    if (!id) return
    try {
      setScanning(true)
      await productService.scan(parseInt(id))
      await fetchStats()
    } catch (error) {
      console.error('Error scanning product:', error)
    } finally {
      setScanning(false)
    }
  }

  useEffect(() => {
    fetchStats()
  }, [id, days])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!stats) {
    return <div>Product not found</div>
  }

  const priceChange = stats.current_price && stats.lowest_price 
    ? stats.current_price - stats.lowest_price 
    : null

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate('/')}
          className="inline-flex items-center text-sm font-medium text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </button>
        <button
          onClick={handleScan}
          disabled={scanning}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${scanning ? 'animate-spin' : ''}`} />
          {scanning ? 'Scanning...' : 'Scan Now'}
        </button>
      </div>

      {/* Product Name and Scraper Info */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">{stats.product_name}</h1>
        {scraperInfo && (
          <div className="mt-2 flex items-center gap-2">
            <Cpu className="h-4 w-4 text-gray-400" />
            <span className="text-sm text-gray-600">
              Using: <span className="font-medium">{scraperInfo.scraper_type}</span>
            </span>
            {scraperInfo.is_optimized && (
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                Optimized
              </span>
            )}
            {!scraperInfo.is_optimized && (
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-yellow-100 text-yellow-800">
                Generic
              </span>
            )}
          </div>
        )}
      </div>

      {/* Price Stats Cards */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-sm font-medium text-gray-500">Current Price</h3>
          <p className="mt-2 text-3xl font-bold text-gray-900">
            {stats.current_price ? `$${stats.current_price.toFixed(2)}` : 'N/A'}
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-sm font-medium text-gray-500">Lowest Price</h3>
          <p className="mt-2 text-3xl font-bold text-green-600">
            {stats.lowest_price ? `$${stats.lowest_price.toFixed(2)}` : 'N/A'}
          </p>
          {priceChange && priceChange > 0 && (
            <p className="mt-1 text-sm text-gray-600 flex items-center">
              <TrendingUp className="h-4 w-4 mr-1 text-red-500" />
              ${priceChange.toFixed(2)} above lowest
            </p>
          )}
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-sm font-medium text-gray-500">Highest Price</h3>
          <p className="mt-2 text-3xl font-bold text-red-600">
            {stats.highest_price ? `$${stats.highest_price.toFixed(2)}` : 'N/A'}
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
          <h3 className="text-sm font-medium text-gray-500">Average Price</h3>
          <p className="mt-2 text-3xl font-bold text-gray-900">
            {stats.average_price ? `$${stats.average_price.toFixed(2)}` : 'N/A'}
          </p>
        </div>
      </div>

      {/* Time Range Selector */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-gray-900">Price History</h2>
          <div className="flex gap-2">
            {[7, 14, 30, 90].map((d) => (
              <button
                key={d}
                onClick={() => setDays(d)}
                className={`px-3 py-1 text-sm font-medium rounded-md ${
                  days === d
                    ? 'bg-primary-600 text-white'
                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                }`}
              >
                {d} days
              </button>
            ))}
          </div>
        </div>

        <PriceChart data={stats.price_history} />
      </div>
    </div>
  )
}


