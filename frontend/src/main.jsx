/**
 * main.jsx — entry point DMS Web (§4.1 FRONTEND_STRUCTURE.md)
 *
 * Tanggung jawab file ini HANYA bootstrap:
 *   1. impor design tokens global (`index.css` — §9);
 *   2. pasang React ke `#root` dengan `<StrictMode><App /></StrictMode>`;
 *   3. jaga layar TV (A-01) agar tidak pernah putih polos saat App gagal dimuat.
 *
 * Yang BUKAN urusan file ini (jangan ditambah di sini):
 *   • router & aturan akses A-01/A-02                      → `App.jsx` + `RequireRole.jsx` (§5, §5.1)
 *   • plant aktif + role interim (`dms.plant`, `dms.role`) → `context/DmsContext.jsx` (§4.5)
 *   • polling `GET /api/state`                             → `hooks/useDmsState.js` (§4.4)
 *   • semua panggilan HTTP                                 → `api/client.js` (§4.3)
 */
import { StrictMode, createElement } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'

/**
 * Layar tunggu ringkas — dipakai hanya selama `App.jsx` masih kerangka.
 * Memakai inline style (bukan kelas `index.css`) supaya tetap terbaca
 * walau design tokens belum lengkap, dan `createElement` (bukan JSX +
 * komponen) agar file entry tetap bebas dari aturan fast-refresh.
 */
const GAYA = {
  wadah: {
    minHeight: '100vh',
    display: 'grid',
    placeItems: 'center',
    padding: '2rem',
    background: '#1B2C57', // --navy
    color: '#FFFFFF',
    fontFamily: 'system-ui, sans-serif',
    textAlign: 'center',
  },
  kotak: { maxWidth: '46rem' },
  judul: { fontSize: '2.5rem', margin: '0 0 .75rem' },
  pesan: { fontSize: '1.25rem', lineHeight: 1.5, color: '#DDE2EA', margin: 0 },
}

function layarInfo(judul, pesan) {
  return createElement(
    'div',
    { style: GAYA.wadah },
    createElement(
      'div',
      { style: GAYA.kotak },
      createElement('h1', { style: GAYA.judul }, judul),
      createElement('p', { style: GAYA.pesan }, pesan),
    ),
  )
}

/**
 * Bootstrap aplikasi.
 * `App.jsx` diimpor dinamis supaya entry tidak gagal total selama berkas itu
 * masih berupa kerangka (belum mengekspor komponen). Begitu `App.jsx` selesai,
 * jalur ini otomatis memakai komponen aslinya tanpa perlu diubah.
 */
async function mulai() {
  const wadah = document.getElementById('root')

  if (!wadah) {
    // Salah pasang shell HTML (`index.html` wajib punya <div id="root">`, §4.1).
    console.error('[DMS] Elemen #root tidak ditemukan — periksa index.html.')
    document.body.textContent =
      'DMS gagal dimuat: elemen #root tidak ada di index.html.'
    return
  }

  const akar = createRoot(wadah)

  try {
    const mod = await import('./App.jsx')
    const App = mod?.default

    if (typeof App !== 'function') {
      // Kondisi sah selama repo masih tahap kerangka (§14 M1 belum selesai).
      console.warn('[DMS] src/App.jsx belum mengekspor komponen App — tampil layar info.')
      akar.render(
        layarInfo(
          'DMS · Garudafood',
          'Kerangka aplikasi. Halaman belum diimplementasikan — lihat docs/FRONTEND_STRUCTURE.md §14 (M1).',
        ),
      )
      return
    }

    akar.render(
      <StrictMode>
        <App />
      </StrictMode>,
    )
  } catch (err) {
    // Gagal impor/render: TV tetap menampilkan pesan, bukan layar putih.
    console.error('[DMS] Gagal memuat aplikasi:', err)
    akar.render(
      layarInfo(
        'DMS tidak dapat dimuat',
        `${err?.message || err}. Muat ulang halaman; bila berulang, hubungi tim DMS.`,
      ),
    )
  }
}

mulai()
