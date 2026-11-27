import { HashRouter, Route, Routes } from 'react-router-dom'
import Main from './pages/Main'
import NotFound from './pages/NotFound'

/**
 * Router aplikasi — FRONTEND_STRUCTURE.md §4.1.
 *
 * `HashRouter` dipakai karena aplikasi bisa dilayani sebagai berkas statis
 * tanpa aturan rewrite di server (§2 baris "Routing").
 *
 * Route yang sudah ada:
 * - `/`         → Landing TV (A-01), publik, tanpa login
 * - `*`         → NotFound (404)
 *
 * Route yang belum dibuat: `/pilar/:key`, `/absensi`, `/dashboard` (A-02).
 * Sengaja tidak didaftarkan supaya jatuh ke `*` — lebih jujur daripada
 * menampilkan halaman kosong. Dashboard nanti dibungkus <RequireRole>.
 */
export default function App() {
  return (
    <HashRouter>
      <Routes>
        <Route path="/" element={<Main />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </HashRouter>
  )
}
