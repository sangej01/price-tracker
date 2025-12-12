import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { ArrowLeft, ExternalLink, TrendingDown, TrendingUp, RefreshCw, Cpu, Edit2, Save, X, Trash2 } from 'lucide-react'
import { dashboardService, productService, vendorService } from '../api/services'
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
  
  // Editing state
  const [isEditing, setIsEditing] = useState(false)
  const [editName, setEditName] = useState('')
  const [editUrl, setEditUrl] = useState('')
  const [editDescription, setEditDescription] = useState('')
  const [editImageUrl, setEditImageUrl] = useState('')
  const [editVendorId, setEditVendorId] = useState<number>(0)
  const [editFrequency, setEditFrequency] = useState(60)
  const [editActive, setEditActive] = useState(true)
  const [saving, setSaving] = useState(false)
  const [deleting, setDeleting] = useState(false)
  const [vendors, setVendors] = useState<any[]>([])

  const fetchStats = async () => {
    if (!id) return
    try {
      setLoading(true)
      const [statsRes, scraperRes, productRes, vendorsRes] = await Promise.all([
        dashboardService.getProductStats(parseInt(id), days),
        productService.getScraperInfo(parseInt(id)),
        productService.getById(parseInt(id)),
        vendorService.getAll()
      ])
      setStats(statsRes.data)
      setScraperInfo(scraperRes.data)
      setVendors(vendorsRes.data)
      
      // Initialize edit fields with current values
      const product = productRes.data
      setEditName(product.name)
      setEditUrl(product.url)
      setEditDescription(product.description || '')
      setEditImageUrl(product.image_url || '')
      setEditVendorId(product.vendor_id)
      setEditFrequency(product.scan_frequency_minutes)
      setEditActive(product.is_active)
    } catch (error) {
      console.error('Error fetching product stats:', error)
    } finally {
      setLoading(false)
    }
  }
  
  const handleSave = async () => {
    if (!id) return
    try {
      setSaving(true)
      await productService.update(parseInt(id), {
        name: editName,
        url: editUrl,
        description: editDescription || null,
        image_url: editImageUrl || null,
        vendor_id: editVendorId,
        scan_frequency_minutes: editFrequency,
        is_active: editActive,
      })
      await fetchStats()
      setIsEditing(false)
    } catch (error) {
      console.error('Error updating product:', error)
      alert('Failed to update product')
    } finally {
      setSaving(false)
    }
  }
  
  const handleDelete = async () => {
    if (!id) return
    if (!confirm(`Are you sure you want to delete "${stats?.product_name}"? This will delete all price history.`)) {
      return
    }
    try {
      setDeleting(true)
      await productService.delete(parseInt(id))
      navigate('/')
    } catch (error) {
      console.error('Error deleting product:', error)
      alert('Failed to delete product')
      setDeleting(false)
    }
  }
  
  const handleCancelEdit = () => {
    // Reset to original values
    if (stats) {
      setEditName(stats.product_name)
    }
    setIsEditing(false)
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

      {/* Product Details - Editable */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-3">
            <h2 className="text-lg font-semibold text-gray-900">Product Details</h2>
            <span className="inline-flex items-center px-3 py-1 rounded-md text-base font-mono font-semibold bg-blue-50 text-blue-700 border-2 border-blue-200">
              ID: {id}
            </span>
          </div>
          <div className="flex gap-2">
            {!isEditing ? (
              <>
                <button
                  onClick={() => setIsEditing(true)}
                  className="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                >
                  <Edit2 className="h-4 w-4 mr-1" />
                  Edit
                </button>
                <button
                  onClick={handleDelete}
                  disabled={deleting}
                  className="inline-flex items-center px-3 py-1.5 border border-red-300 rounded-md text-sm font-medium text-red-700 bg-white hover:bg-red-50 disabled:opacity-50"
                >
                  <Trash2 className="h-4 w-4 mr-1" />
                  {deleting ? 'Deleting...' : 'Delete'}
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="inline-flex items-center px-3 py-1.5 border border-transparent rounded-md text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 disabled:opacity-50"
                >
                  <Save className="h-4 w-4 mr-1" />
                  {saving ? 'Saving...' : 'Save'}
                </button>
                <button
                  onClick={handleCancelEdit}
                  disabled={saving}
                  className="inline-flex items-center px-3 py-1.5 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 disabled:opacity-50"
                >
                  <X className="h-4 w-4 mr-1" />
                  Cancel
                </button>
              </>
            )}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Product Name */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Product Name
            </label>
            {isEditing ? (
              <input
                type="text"
                value={editName}
                onChange={(e) => setEditName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
            ) : (
              <p className="text-gray-900">{stats.product_name}</p>
            )}
          </div>

          {/* URL */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Product URL
            </label>
            {isEditing ? (
              <input
                type="url"
                value={editUrl}
                onChange={(e) => setEditUrl(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm"
                placeholder="https://..."
              />
            ) : (
              <a
                href={editUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 hover:text-primary-700 flex items-center gap-1 text-sm break-all"
              >
                {editUrl}
                <ExternalLink className="h-4 w-4 flex-shrink-0" />
              </a>
            )}
          </div>

          {/* Vendor */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Vendor
            </label>
            {isEditing ? (
              <select
                value={editVendorId}
                onChange={(e) => setEditVendorId(parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                {vendors.map((vendor) => (
                  <option key={vendor.id} value={vendor.id}>
                    {vendor.name}
                  </option>
                ))}
              </select>
            ) : (
              <p className="text-gray-900">{scraperInfo?.vendor}</p>
            )}
          </div>

          {/* Scan Frequency */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Scan Frequency
            </label>
            {isEditing ? (
              <select
                value={editFrequency}
                onChange={(e) => setEditFrequency(parseInt(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              >
                <option value={5}>Every 5 minutes</option>
                <option value={15}>Every 15 minutes</option>
                <option value={30}>Every 30 minutes</option>
                <option value={60}>Every hour</option>
                <option value={120}>Every 2 hours</option>
                <option value={240}>Every 4 hours</option>
                <option value={480}>Every 8 hours</option>
                <option value={1440}>Every 24 hours</option>
              </select>
            ) : (
              <p className="text-gray-900">
                {editFrequency < 60
                  ? `Every ${editFrequency} minutes`
                  : editFrequency === 60
                  ? 'Every hour'
                  : editFrequency === 1440
                  ? 'Every 24 hours'
                  : `Every ${editFrequency / 60} hours`}
              </p>
            )}
          </div>

          {/* Active Status */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            {isEditing ? (
              <label className="flex items-center">
                <input
                  type="checkbox"
                  checked={editActive}
                  onChange={(e) => setEditActive(e.target.checked)}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <span className="ml-2 text-sm text-gray-700">Active (enable scanning)</span>
              </label>
            ) : (
              <span
                className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium ${
                  editActive
                    ? 'bg-green-100 text-green-800'
                    : 'bg-gray-100 text-gray-800'
                }`}
              >
                {editActive ? 'Active' : 'Inactive'}
              </span>
            )}
          </div>

          {/* Image URL */}
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Image URL
            </label>
            {isEditing ? (
              <input
                type="url"
                value={editImageUrl}
                onChange={(e) => setEditImageUrl(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm"
                placeholder="https://... (optional)"
              />
            ) : editImageUrl ? (
              <a
                href={editImageUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 hover:text-primary-700 flex items-center gap-1 text-sm break-all"
              >
                {editImageUrl}
                <ExternalLink className="h-4 w-4 flex-shrink-0" />
              </a>
            ) : (
              <p className="text-gray-600 text-sm">Not set</p>
            )}
          </div>

          {/* Description */}
          <div className="md:col-span-2">
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Description
            </label>
            {isEditing ? (
              <textarea
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm"
                placeholder="Optional description or notes..."
              />
            ) : (
              <p className="text-gray-600 text-sm whitespace-pre-wrap">{editDescription || 'No description'}</p>
            )}
          </div>
        </div>
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


