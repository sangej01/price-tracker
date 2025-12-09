import { useState } from 'react'
import { TestTube, CheckCircle, XCircle, AlertCircle } from 'lucide-react'
import { productService } from '../api/services'

interface UrlTesterProps {
  url: string
  onClose: () => void
}

export default function UrlTester({ url, onClose }: UrlTesterProps) {
  const [testing, setTesting] = useState(false)
  const [result, setResult] = useState<any>(null)

  const handleTest = async () => {
    if (!url) return
    
    try {
      setTesting(true)
      setResult(null)
      const response = await productService.testUrl(url)
      setResult(response.data)
    } catch (error) {
      console.error('Error testing URL:', error)
      setResult({ success: false, error: 'Failed to test URL' })
    } finally {
      setTesting(false)
    }
  }

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-md p-4 mb-4">
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center">
          <TestTube className="h-5 w-5 text-blue-600 mr-2" />
          <h3 className="text-sm font-medium text-blue-900">Test URL Scraper</h3>
        </div>
        <button onClick={onClose} className="text-blue-600 hover:text-blue-800">
          ×
        </button>
      </div>

      <p className="text-xs text-blue-700 mb-3">
        Test if this URL can be scraped successfully before adding it as a product.
      </p>

      <button
        onClick={handleTest}
        disabled={testing || !url}
        className="w-full inline-flex justify-center items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
      >
        {testing ? (
          <>
            <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
            Testing...
          </>
        ) : (
          <>
            <TestTube className="h-4 w-4 mr-2" />
            Test URL
          </>
        )}
      </button>

      {result && (
        <div className={`mt-3 p-3 rounded-md ${
          result.success ? 'bg-green-50 border border-green-200' : 'bg-red-50 border border-red-200'
        }`}>
          <div className="flex items-start">
            {result.success ? (
              <CheckCircle className="h-5 w-5 text-green-600 mr-2 flex-shrink-0 mt-0.5" />
            ) : (
              <XCircle className="h-5 w-5 text-red-600 mr-2 flex-shrink-0 mt-0.5" />
            )}
            <div className="flex-1">
              <h4 className={`text-sm font-medium ${
                result.success ? 'text-green-900' : 'text-red-900'
              }`}>
                {result.success ? 'Scraping Successful!' : 'Scraping Failed'}
              </h4>
              
              {result.success && (
                <div className="mt-2 text-sm text-green-800 space-y-1">
                  <p><strong>Scraper:</strong> {result.scraper_used}</p>
                  {result.is_optimized && (
                    <p className="flex items-center">
                      <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-green-100 text-green-800">
                        Optimized Scraper
                      </span>
                    </p>
                  )}
                  {!result.is_optimized && (
                    <p className="flex items-center">
                      <AlertCircle className="h-4 w-4 mr-1" />
                      <span className="text-xs">Using generic scraper (may be less accurate)</span>
                    </p>
                  )}
                  {result.price && (
                    <p><strong>Price Found:</strong> {result.currency} ${result.price.toFixed(2)}</p>
                  )}
                  <p><strong>Stock Status:</strong> {result.in_stock ? 'In Stock' : 'Out of Stock'}</p>
                </div>
              )}
              
              {!result.success && result.error && (
                <p className="mt-1 text-sm text-red-700">
                  {result.error}
                </p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

