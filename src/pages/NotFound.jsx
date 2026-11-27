/**
 * Halaman 404 — route `*`. FRONTEND_STRUCTURE.md §4.7:
 *
 *   "404 sederhana + link Beranda (Dashboard hanya ditampilkan bila role pdca/tl)"
 *
 * Kepatuhan brief:
 * - Tombol "Ke Beranda" SELALU ada — halaman ini publik (semua TV, tanpa login).
 * - Tombol "Ke Dashboard" HANYA muncul untuk role pdca/tl (A-02).
 *   Untuk role tv, tautan /dashboard tidak dirender sama sekali.
 * - Warna memakai token brief §9.1 (navy · teal · bg · card · rule · text · grey).
 *
 * Susunan mengikuti desain acuan: logo → angka 404 besar → judul →
 * keterangan → tombol aksi.
 */
import { useRole } from '../hooks/useRole'

export default function NotFound() {
  const { bolehDashboard } = useRole()

  return (
    <div className="nf">
      <div className="nf-inner">
        <a className="nf-brand" href="#/">
          <img src="/logo-192.png" alt="" width="56" height="56" />
          <span className="nf-brand-text">
            <b>DMS</b>
            <small>Daily Monitoring System</small>
          </span>
        </a>

        <p className="nf-code" aria-hidden="true">
          404
        </p>

        <h1 className="nf-title">Halaman Tidak Ditemukan</h1>

        <p className="nf-msg">
          Alamat yang Anda buka tidak ada atau sudah dipindahkan. Periksa kembali tautannya,
          atau kembali ke papan utama.
        </p>

        <div className="nf-aksi">
          {/* Selalu tampil — halaman publik, tanpa login (A-01) */}
          <a className="btn btn-primary" href="#/">
            ← Ke Beranda
          </a>

          {/* A-02: hanya untuk role pdca/tl */}
          {bolehDashboard && (
            <a className="btn btn-outline" href="#/dashboard">
              Ke Dashboard
            </a>
          )}
        </div>

        <p className="nf-catatan">
          Tanpa login · tampil di semua TV · absensi dikerjakan lebih dulu
        </p>
      </div>
    </div>
  )
}
