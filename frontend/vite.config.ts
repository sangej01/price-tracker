import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig(({ mode }) => {
  // Load env file from project root (parent directory)
  const env = loadEnv(mode, path.resolve(__dirname, '..'), '')
  const backendPort = env.SERVER_PORT || '8081'
  
  return {
    plugins: [react()],
    envDir: path.resolve(__dirname, '..'), // Look for .env in project root
    server: {
      host: '0.0.0.0', // Listen on all network interfaces
      port: 3000,
      proxy: {
        '/api': {
          target: `http://localhost:${backendPort}`,
          changeOrigin: true,
        },
      },
    },
  }
})


