export interface Vendor {
  id: number
  name: string
  domain: string
  is_active: boolean
  created_at: string
}

export interface Product {
  id: number
  name: string
  url: string
  vendor_id: number
  image_url: string | null
  description: string | null
  is_active: boolean
  scan_frequency_minutes: number
  created_at: string
  last_scanned_at: string | null
}

export interface PriceHistory {
  id: number
  product_id: number
  price: number
  currency: string
  in_stock: boolean
  scraped_at: string
}

export interface ProductWithLatestPrice {
  id: number
  name: string
  url: string
  vendor_name: string
  image_url: string | null
  current_price: number | null
  previous_price: number | null
  price_change: number | null
  price_change_percent: number | null
  in_stock: boolean
  last_scanned_at: string | null
  currency: string
}

export interface ProductPriceStats {
  product_id: number
  product_name: string
  current_price: number | null
  lowest_price: number | null
  highest_price: number | null
  average_price: number | null
  price_history: PriceHistory[]
}

export interface DashboardSummary {
  total_products: number
  total_vendors: number
  recently_scanned: number
  total_price_records: number
}


