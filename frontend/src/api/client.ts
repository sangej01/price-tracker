import axios from 'axios'

// IMPORTANT:
// - If you're accessing the frontend remotely (LAN/Tailscale), DO NOT default to http://localhost:8081
//   because "localhost" would be the *client* machine.
// - Default to same-origin instead, so requests like "/api/..." hit the Vite dev server and get proxied.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default api


