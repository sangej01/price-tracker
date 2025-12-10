import { useState, useEffect } from 'react'
import { Save, RefreshCw } from 'lucide-react'
import api from '../api/client'

interface Vendor {
  id: number
  name: string
  domain: string
}

interface ScanFrequencySettings {
  default_frequency: number
  vendor_overrides: { [vendorId: number]: number }
}

export default function Settings() {
  const [vendors, setVendors] = useState<Vendor[]>([])
  const [settings, setSettings] = useState<ScanFrequencySettings>({
    default_frequency: 60,
    vendor_overrides: {}
  })
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [applyingToProducts, setApplyingToProducts] = useState(false)
  const [message, setMessage] = useState<{ type: 'success' | 'error', text: string } | null>(null)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      setLoading(true)
      const [vendorsRes, settingsRes] = await Promise.all([
        api.get<Vendor[]>('/api/vendors/'),
        api.get<ScanFrequencySettings>('/api/settings/scan-frequency')
      ])
      setVendors(vendorsRes.data)
      setSettings(settingsRes.data)
    } catch (error) {
      console.error('Error fetching data:', error)
      showMessage('error', 'Failed to load settings')
    } finally {
      setLoading(false)
    }
  }

  const handleSave = async () => {
    try {
      setSaving(true)
      await api.put('/api/settings/scan-frequency', settings)
      showMessage('success', 'Settings saved successfully!')
    } catch (error) {
      console.error('Error saving settings:', error)
      showMessage('error', 'Failed to save settings')
    } finally {
      setSaving(false)
    }
  }

  const handleApplyToProducts = async (vendorId?: number) => {
    try {
      setApplyingToProducts(true)
      const params = vendorId ? { vendor_id: vendorId } : {}
      const res = await api.post('/api/settings/scan-frequency/apply-to-products', null, { params })
      showMessage('success', `Updated ${res.data.updated_count} products`)
    } catch (error) {
      console.error('Error applying settings:', error)
      showMessage('error', 'Failed to apply settings to products')
    } finally {
      setApplyingToProducts(false)
    }
  }

  const showMessage = (type: 'success' | 'error', text: string) => {
    setMessage({ type, text })
    setTimeout(() => setMessage(null), 5000)
  }

  const updateVendorOverride = (vendorId: number, minutes: number | null) => {
    const newOverrides = { ...settings.vendor_overrides }
    if (minutes === null || minutes === settings.default_frequency) {
      delete newOverrides[vendorId]
    } else {
      newOverrides[vendorId] = minutes
    }
    setSettings({ ...settings, vendor_overrides: newOverrides })
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  const frequencyOptions = [5, 10, 15, 30, 60, 120, 240, 480, 1440]

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Scan Frequency Settings</h1>
        <p className="mt-2 text-sm text-gray-600">
          Configure how often products are scanned for price updates
        </p>
      </div>

      {/* Message */}
      {message && (
        <div className={`p-4 rounded-md ${
          message.type === 'success' ? 'bg-green-50 text-green-800' : 'bg-red-50 text-red-800'
        }`}>
          {message.text}
        </div>
      )}

      {/* Global Default */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Global Default</h2>
        <p className="text-sm text-gray-600 mb-4">
          Default scan frequency for all products (unless overridden per vendor)
        </p>
        <div className="flex items-center space-x-4">
          <label className="text-sm font-medium text-gray-700">Scan every:</label>
          <select
            value={settings.default_frequency}
            onChange={(e) => setSettings({ ...settings, default_frequency: parseInt(e.target.value) })}
            className="mt-1 block w-48 rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
          >
            {frequencyOptions.map(minutes => (
              <option key={minutes} value={minutes}>
                {minutes < 60 ? `${minutes} minutes` : `${minutes / 60} hour${minutes > 60 ? 's' : ''}`}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Per-Vendor Overrides */}
      <div className="bg-white shadow-sm rounded-lg border border-gray-200 p-6">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Vendor-Specific Overrides</h2>
        <p className="text-sm text-gray-600 mb-4">
          Set different scan frequencies for specific vendors (e.g., scan eBay auctions more frequently)
        </p>
        <div className="space-y-4">
          {vendors.map(vendor => {
            const currentOverride = settings.vendor_overrides[vendor.id]
            const effectiveFrequency = currentOverride || settings.default_frequency

            return (
              <div key={vendor.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <h3 className="font-medium text-gray-900">{vendor.name}</h3>
                  <p className="text-sm text-gray-500">{vendor.domain}</p>
                </div>
                <div className="flex items-center space-x-4">
                  <select
                    value={effectiveFrequency}
                    onChange={(e) => updateVendorOverride(vendor.id, parseInt(e.target.value))}
                    className="block w-48 rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
                  >
                    {frequencyOptions.map(minutes => (
                      <option key={minutes} value={minutes}>
                        {minutes < 60 ? `${minutes} minutes` : `${minutes / 60} hour${minutes > 60 ? 's' : ''}`}
                        {minutes === settings.default_frequency && !currentOverride ? ' (default)' : ''}
                      </option>
                    ))}
                  </select>
                  <button
                    onClick={() => handleApplyToProducts(vendor.id)}
                    disabled={applyingToProducts}
                    className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
                    title={`Apply this frequency to all EXISTING ${vendor.name} products`}
                  >
                    <RefreshCw className={`h-4 w-4 ${applyingToProducts ? 'animate-spin' : ''}`} />
                  </button>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      {/* Save Buttons */}
      <div className="flex items-center justify-between bg-white shadow-sm rounded-lg border border-gray-200 p-6">
        <div>
          <h3 className="font-medium text-gray-900">Apply Changes</h3>
          <p className="text-sm text-gray-500 mt-1">
            Save settings for NEW products, and optionally update EXISTING products
          </p>
        </div>
        <div className="flex space-x-3">
          <button
            onClick={handleSave}
            disabled={saving}
            className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
          >
            <Save className={`h-4 w-4 mr-2 ${saving ? 'animate-spin' : ''}`} />
            Save Settings
          </button>
          <button
            onClick={() => handleApplyToProducts()}
            disabled={applyingToProducts}
            className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
            title="Update all existing products to use the settings above"
          >
            <RefreshCw className={`h-4 w-4 mr-2 ${applyingToProducts ? 'animate-spin' : ''}`} />
            Apply to All Existing Products
          </button>
        </div>
      </div>
    </div>
  )
}

