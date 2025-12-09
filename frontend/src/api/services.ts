import api from './client'
import { Product, Vendor, ProductWithLatestPrice, ProductPriceStats, DashboardSummary } from './types'

// Vendor API
export const vendorService = {
  getAll: () => api.get<Vendor[]>('/api/vendors/'),
  getById: (id: number) => api.get<Vendor>(`/api/vendors/${id}`),
  create: (data: Omit<Vendor, 'id' | 'is_active' | 'created_at'>) => 
    api.post<Vendor>('/api/vendors/', data),
  update: (id: number, data: Partial<Vendor>) => 
    api.put<Vendor>(`/api/vendors/${id}`, data),
  delete: (id: number) => api.delete(`/api/vendors/${id}`),
}

// Product API
export const productService = {
  getAll: (activeOnly = false) => 
    api.get<Product[]>('/api/products/', { params: { active_only: activeOnly } }),
  getById: (id: number) => api.get<Product>(`/api/products/${id}`),
  create: (data: Omit<Product, 'id' | 'is_active' | 'created_at' | 'last_scanned_at'>) => 
    api.post<Product>('/api/products/', data),
  update: (id: number, data: Partial<Product>) => 
    api.put<Product>(`/api/products/${id}`, data),
  delete: (id: number) => api.delete(`/api/products/${id}`),
  scan: (id: number) => api.post(`/api/products/${id}/scan`),
  getScraperInfo: (id: number) => api.get(`/api/products/${id}/scraper-info`),
  testUrl: (url: string) => api.post('/api/products/test-url', null, { params: { url } }),
}

// Dashboard API
export const dashboardService = {
  getProducts: () => api.get<ProductWithLatestPrice[]>('/api/dashboard/products'),
  getProductStats: (productId: number, days = 30) => 
    api.get<ProductPriceStats>(`/api/dashboard/products/${productId}/stats`, { params: { days } }),
  getSummary: () => api.get<DashboardSummary>('/api/dashboard/summary'),
}

// Scanner API
export const scannerService = {
  scanAll: () => api.post('/api/scanner/scan-all'),
  getStatus: () => api.get('/api/scanner/status'),
}


