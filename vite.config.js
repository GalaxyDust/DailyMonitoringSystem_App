import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// Fase tampilan: halaman belum mengambil data, jadi belum ada proxy API.
// Proxy /api, /qr, /s ditambahkan saat fase integrasi (FRONTEND_STRUCTURE.md §4.1).
//
// host + allowedHosts diperlukan agar dev server bisa dibuka lewat host preview
// (bukan hanya localhost) dan tetap bisa diakses dari perangkat lain di jaringan.
export default defineConfig({
  plugins: [react()],
  server: { host: true, allowedHosts: true },
  preview: { host: true, allowedHosts: true },
})
