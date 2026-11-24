import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// DMS frontend — proxy ke backend Flask (app/server.py, port 8000) saat dev.
// Produksi: `npm run build` lalu sajikan folder dist/ lewat Flask atau Nginx.
export default defineConfig({
  plugins: [react()],
  server: {
    host: true,
    port: 5173,
    // Izinkan host preview (e2b.app) dan LAN — Vite 8 menolak host asing secara default.
    allowedHosts: true,
    proxy: {
      '/api': 'http://localhost:8000',
      '/qr': 'http://localhost:8000',
      '/s': 'http://localhost:8000',
    },
  },
  preview: { host: true, port: 4173 },
})
