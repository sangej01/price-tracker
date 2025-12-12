import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
/// <reference types="node" />
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

export default defineConfig(({ mode }) => {
  // Load env file from project root (parent directory)
  const projectRoot = resolve(__dirname, '..')
  const env = loadEnv(mode, projectRoot, '')
  const backendPort = env.SERVER_PORT || '8081'
  
  return {
    plugins: [react()],
    envDir: projectRoot, // Look for .env in project root
    server: {
      // Allow access from other devices/interfaces (e.g., over Tailscale)
      host: true, // equivalent to 0.0.0.0
      port: 3001,
      // Vite 5 host check: allow non-local hostnames like *.tail*.ts.net
      // If you prefer stricter, replace `true` with: ['geekom-gt1-a.tail425a06.ts.net']
      allowedHosts: true,
      proxy: {
        '/api': {
          target: `http://localhost:${backendPort}`,
          changeOrigin: true,
        },
      },
    },
  }
})


