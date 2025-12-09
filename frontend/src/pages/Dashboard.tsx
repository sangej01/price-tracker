import { useState, useEffect } from 'react'
import { Package, Store, Clock, Database, RefreshCw } from 'lucide-react'
import { dashboardService, scannerService } from '../api/services'
import { ProductWithLatestPrice, DashboardSummary } from '../api/types'
import StatCard from '../components/StatCard'
import ProductCard from '../components/ProductCard'

export default function Dashboard() {
  const [products, setProducts] = useState<ProductWithLatestPrice[]>([])
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [loading, setLoading] = useState(true)
  const [scanning, setScanning] = useState(false)

  const fetchData = async () => {
    try {
      setLoading(true)
      const [productsRes, summaryRes] = await Promise.all([
        dashboardService.getProducts(),
        dashboardService.getSummary(),
      ])
      setProducts(productsRes.data)
      setSummary(summaryRes.data)
    } catch (error) {
      console.error('Error fetching dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleScanAll = async () => {
    try {
      setScanning(true)
      await scannerService.scanAll()
      await fetchData()
    } catch (error) {
      console.error('Error scanning products:', error)
    } finally {
      setScanning(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
          <p className="mt-2 text-sm text-gray-600">
            Track prices across multiple vendors
          </p>
        </div>
        <button
          onClick={handleScanAll}
          disabled={scanning}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${scanning ? 'animate-spin' : ''}`} />
          {scanning ? 'Scanning...' : 'Scan All Products'}
        </button>
      </div>

      {/* Stats */}
      {summary && (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
          <StatCard
            title="Total Products"
            value={summary.total_products}
            icon={Package}
            iconColor="text-primary-600"
            bgColor="bg-primary-50"
          />
          <StatCard
            title="Total Vendors"
            value={summary.total_vendors}
            icon={Store}
            iconColor="text-purple-600"
            bgColor="bg-purple-50"
          />
          <StatCard
            title="Recently Scanned"
            value={summary.recently_scanned}
            icon={Clock}
            iconColor="text-green-600"
            bgColor="bg-green-50"
          />
          <StatCard
            title="Price Records"
            value={summary.total_price_records}
            icon={Database}
            iconColor="text-orange-600"
            bgColor="bg-orange-50"
          />
        </div>
      )}

      {/* Products Grid */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Tracked Products</h2>
        {products.length === 0 ? (
          <div className="text-center py-12 bg-white rounded-lg border-2 border-dashed border-gray-300">
            <Package className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No products</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by adding a product to track
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {products.map((product) => (
              <ProductCard key={product.id} product={product} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}


