import Main from './pages/Main'

/**
 * Root aplikasi.
 *
 * Inilah satu-satunya baris yang menentukan apa yang tampil saat membuka `/`.
 * `index.html` sudah memanggil `/src/main.jsx`, dan `src/main.jsx` merender
 * komponen ini — jadi cukup ganti isi file ini, tanpa menyentuh `main.jsx`.
 *
 * Fase ini hanya Landing TV (A-01): tampilan statis, tanpa fetch/API,
 * tanpa router, dan tanpa tautan /dashboard (A-02).
 * Halaman lain (/pilar/:key, /absensi, /dashboard) menyusul sesuai
 * docs/FRONTEND_STRUCTURE.md §14.
 */
export default function App() {
  return <Main />
}
