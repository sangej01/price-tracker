import { useState, useEffect } from 'react'
import { Plus, Edit, Trash2, ExternalLink, ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react'
import { productService, vendorService } from '../api/services'
import { Product, Vendor } from '../api/types'
import UrlTester from '../components/UrlTester'

export default function Products() {
  const [products, setProducts] = useState<Product[]>([])
  const [vendors, setVendors] = useState<Vendor[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [showUrlTester, setShowUrlTester] = useState(false)
  const [editingProduct, setEditingProduct] = useState<Product | null>(null)
  
  // Filters and sorting
  const [filterActive, setFilterActive] = useState<'all' | 'active' | 'inactive'>('all')
  const [filterAuction, setFilterAuction] = useState<'all' | 'auction' | 'regular'>('all')
  const [sortField, setSortField] = useState<'id' | 'name' | 'vendor' | 'frequency'>('id')
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('asc')
  
  const [formData, setFormData] = useState({
    name: '',
    url: '',
    vendor_id: 0,
    image_url: '',
    description: '',
    scan_frequency_minutes: 60,
    is_active: true,
  })

  const fetchData = async () => {
    try {
      setLoading(true)
      const [productsRes, vendorsRes] = await Promise.all([
        productService.getAll(),
        vendorService.getAll(),
      ])
      setProducts(productsRes.data)
      setVendors(vendorsRes.data)
    } catch (error) {
      console.error('Error fetching data:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      if (editingProduct) {
        await productService.update(editingProduct.id, formData)
      } else {
        await productService.create(formData)
      }
      setShowModal(false)
      setEditingProduct(null)
      resetForm()
      fetchData()
    } catch (error) {
      console.error('Error saving product:', error)
    }
  }

  const handleEdit = (product: Product) => {
    setEditingProduct(product)
    setFormData({
      name: product.name,
      url: product.url,
      vendor_id: product.vendor_id,
      image_url: product.image_url || '',
      description: product.description || '',
      scan_frequency_minutes: product.scan_frequency_minutes,
      is_active: product.is_active,
    })
    setShowModal(true)
  }

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this product?')) {
      try {
        await productService.delete(id)
        fetchData()
      } catch (error) {
        console.error('Error deleting product:', error)
      }
    }
  }

  const resetForm = () => {
    setFormData({
      name: '',
      url: '',
      vendor_id: 0,
      image_url: '',
      description: '',
      scan_frequency_minutes: 60,
      is_active: true,
    })
  }

  const getVendorName = (vendorId: number) => {
    const vendor = vendors.find((v) => v.id === vendorId)
    return vendor?.name || 'Unknown'
  }

  const formatScanFrequency = (minutes: number) => {
    if (minutes >= 60) {
      const hours = minutes / 60
      return hours === 1 ? '1 hour' : `${hours} hours`
    }
    return `${minutes} min`
  }

  // Filter and sort products
  const filteredAndSortedProducts = () => {
    let filtered = [...products]
    
    // Apply active filter
    if (filterActive === 'active') {
      filtered = filtered.filter(p => p.is_active)
    } else if (filterActive === 'inactive') {
      filtered = filtered.filter(p => !p.is_active)
    }
    
    // Apply auction filter
    if (filterAuction === 'auction') {
      filtered = filtered.filter(p => p.is_auction)
    } else if (filterAuction === 'regular') {
      filtered = filtered.filter(p => !p.is_auction)
    }
    
    // Sort
    filtered.sort((a, b) => {
      let compareA: any
      let compareB: any
      
      switch (sortField) {
        case 'id':
          compareA = a.id
          compareB = b.id
          break
        case 'name':
          compareA = a.name.toLowerCase()
          compareB = b.name.toLowerCase()
          break
        case 'vendor':
          compareA = getVendorName(a.vendor_id).toLowerCase()
          compareB = getVendorName(b.vendor_id).toLowerCase()
          break
        case 'frequency':
          compareA = a.scan_frequency_minutes
          compareB = b.scan_frequency_minutes
          break
        default:
          return 0
      }
      
      if (compareA < compareB) return sortDirection === 'asc' ? -1 : 1
      if (compareA > compareB) return sortDirection === 'asc' ? 1 : -1
      return 0
    })
    
    return filtered
  }

  const handleSort = (field: typeof sortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('asc')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Products</h1>
          <p className="mt-2 text-sm text-gray-600">
            {filteredAndSortedProducts().length} of {products.length} products
          </p>
        </div>
        <button
          onClick={() => {
            resetForm()
            setEditingProduct(null)
            setShowModal(true)
          }}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700"
        >
          <Plus className="h-4 w-4 mr-2" />
          Add Product
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-4">
        <div className="flex flex-wrap gap-4 items-center">
          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Status</label>
            <select
              value={filterActive}
              onChange={(e) => setFilterActive(e.target.value as any)}
              className="block w-full pl-3 pr-10 py-2 text-sm border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 rounded-md"
            >
              <option value="all">All Products</option>
              <option value="active">Active Only</option>
              <option value="inactive">Inactive Only</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-700 mb-1">Type</label>
            <select
              value={filterAuction}
              onChange={(e) => setFilterAuction(e.target.value as any)}
              className="block w-full pl-3 pr-10 py-2 text-sm border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 rounded-md"
            >
              <option value="all">All Types</option>
              <option value="auction">Auctions Only</option>
              <option value="regular">Regular Products</option>
            </select>
          </div>

          {(filterActive !== 'all' || filterAuction !== 'all') && (
            <button
              onClick={() => {
                setFilterActive('all')
                setFilterAuction('all')
              }}
              className="mt-5 text-sm text-primary-600 hover:text-primary-700 font-medium"
            >
              Clear Filters
            </button>
          )}
        </div>
      </div>

      {/* Products Table */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-200 overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th 
                onClick={() => handleSort('id')}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              >
                <div className="flex items-center gap-1">
                  ID
                  {sortField === 'id' ? (
                    sortDirection === 'asc' ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />
                  ) : <ArrowUpDown className="h-3 w-3 text-gray-400" />}
                </div>
              </th>
              <th 
                onClick={() => handleSort('name')}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              >
                <div className="flex items-center gap-1">
                  Name
                  {sortField === 'name' ? (
                    sortDirection === 'asc' ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />
                  ) : <ArrowUpDown className="h-3 w-3 text-gray-400" />}
                </div>
              </th>
              <th 
                onClick={() => handleSort('vendor')}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              >
                <div className="flex items-center gap-1">
                  Vendor
                  {sortField === 'vendor' ? (
                    sortDirection === 'asc' ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />
                  ) : <ArrowUpDown className="h-3 w-3 text-gray-400" />}
                </div>
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                URL
              </th>
              <th 
                onClick={() => handleSort('frequency')}
                className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
              >
                <div className="flex items-center gap-1">
                  Frequency
                  {sortField === 'frequency' ? (
                    sortDirection === 'asc' ? <ArrowUp className="h-3 w-3" /> : <ArrowDown className="h-3 w-3" />
                  ) : <ArrowUpDown className="h-3 w-3 text-gray-400" />}
                </div>
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {filteredAndSortedProducts().map((product) => (
              <tr key={product.id}>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-mono font-medium bg-gray-100 text-gray-800">
                    {product.id}
                  </span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm font-medium text-gray-900">{product.name}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="text-sm text-gray-500">{getVendorName(product.vendor_id)}</div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {product.is_auction ? (
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
                      🔨 Auction
                    </span>
                  ) : (
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600">
                      Regular
                    </span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <a
                    href={product.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-primary-600 hover:text-primary-900 flex items-center"
                  >
                    <ExternalLink className="h-4 w-4 mr-1" />
                    Link
                  </a>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {formatScanFrequency(product.scan_frequency_minutes)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  {product.is_active ? (
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                      Active
                    </span>
                  ) : (
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-gray-100 text-gray-800">
                      Inactive
                    </span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <button
                    onClick={() => handleEdit(product)}
                    className="text-primary-600 hover:text-primary-900 mr-4"
                  >
                    <Edit className="h-4 w-4" />
                  </button>
                  <button
                    onClick={() => handleDelete(product.id)}
                    className="text-red-600 hover:text-red-900"
                  >
                    <Trash2 className="h-4 w-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed z-10 inset-0 overflow-y-auto">
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={() => setShowModal(false)}></div>

            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <form onSubmit={handleSubmit}>
                <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium text-gray-900">
                      {editingProduct ? 'Edit Product' : 'Add New Product'}
                    </h3>
                    {editingProduct && (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-md text-xs font-mono font-medium bg-gray-100 text-gray-800 border border-gray-300">
                        ID: {editingProduct.id}
                      </span>
                    )}
                  </div>

                  {/* URL Tester */}
                  {showUrlTester && formData.url && (
                    <UrlTester 
                      url={formData.url} 
                      onClose={() => setShowUrlTester(false)}
                    />
                  )}

                  <div className="space-y-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700">Name</label>
                      <input
                        type="text"
                        required
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      />
                    </div>

                    <div>
                      <div className="flex justify-between items-center">
                        <label className="block text-sm font-medium text-gray-700">URL</label>
                        {formData.url && !showUrlTester && (
                          <button
                            type="button"
                            onClick={() => setShowUrlTester(true)}
                            className="text-xs text-primary-600 hover:text-primary-800"
                          >
                            Test URL
                          </button>
                        )}
                      </div>
                      <input
                        type="url"
                        required
                        value={formData.url}
                        onChange={(e) => {
                          setFormData({ ...formData, url: e.target.value })
                          setShowUrlTester(false)
                        }}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">Vendor</label>
                      <select
                        required
                        value={formData.vendor_id}
                        onChange={(e) => setFormData({ ...formData, vendor_id: parseInt(e.target.value) })}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      >
                        <option value={0}>Select Vendor</option>
                        {vendors.map((vendor) => (
                          <option key={vendor.id} value={vendor.id}>
                            {vendor.name}
                          </option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">Image URL (optional)</label>
                      <input
                        type="url"
                        value={formData.image_url}
                        onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">Description (optional)</label>
                      <textarea
                        value={formData.description}
                        onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                        rows={3}
                        placeholder="Add notes or description..."
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700">Scan Frequency</label>
                      <select
                        required
                        value={formData.scan_frequency_minutes}
                        onChange={(e) => setFormData({ ...formData, scan_frequency_minutes: parseInt(e.target.value) })}
                        className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500"
                      >
                        <option value={15}>15 minutes</option>
                        <option value={60}>1 hour</option>
                        <option value={240}>4 hours</option>
                        <option value={480}>8 hours</option>
                        <option value={720}>12 hours</option>
                        <option value={1440}>1 day</option>
                        <option value={2880}>2 days</option>
                        <option value={5760}>4 days</option>
                        <option value={10080}>1 week</option>
                        <option value={43200}>1 month (30 days)</option>
                      </select>
                    </div>

                    <div>
                      <label className="flex items-center">
                        <input
                          type="checkbox"
                          checked={formData.is_active}
                          onChange={(e) => setFormData({ ...formData, is_active: e.target.checked })}
                          className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                        />
                        <span className="ml-2 text-sm font-medium text-gray-700">Active (enable scanning)</span>
                      </label>
                    </div>
                  </div>
                </div>

                <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                  <button
                    type="submit"
                    className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:ml-3 sm:w-auto sm:text-sm"
                  >
                    {editingProduct ? 'Update' : 'Create'}
                  </button>
                  <button
                    type="button"
                    onClick={() => {
                      setShowModal(false)
                      setEditingProduct(null)
                      resetForm()
                    }}
                    className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}


