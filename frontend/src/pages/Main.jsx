import { Link } from 'react-router-dom'
import { PILARS } from '../constants'

const HIGHLIGHT = [
  ['3', 'Plant terdaftar', 'Snack · EP · NP'],
  ['5', 'Pilar', 'SHE · Quality · Produksi · Delivery · Teknik'],
  ['7', 'Halaman TV', 'Absensi + 5 divisi + Ringkasan'],
  ['0', 'Upload untuk petugas', 'cukup Ctrl+S (R-88)'],
]

export function Main() {
  return (
    <>
      {/* HERO */}
      <section className="hero">
        <div>
          <span className="hero-eyebrow">🦅 Garudafood · Lantai Produksi</span>
          <h1>Papan monitoring harian,<br /><span className="accent">satu angka, semua sepakat.</span></h1>
          <p className="lead">DMS membaca Excel yang sama dengan yang diisi petugas — otomatis, satu arah, tanpa upload. TV lantai, landing QR di ponsel, dan dashboard ini menampilkan angka yang identik.</p>
          <div className="hero-cta">
            <Link className="btn btn-gold" to="/dashboard">📊 Buka Dashboard 5 Pilar</Link>
            <Link className="btn btn-primary" to="/absensi">✅ Absensi Shift</Link>
          </div>
          <div className="hero-meta">
            {HIGHLIGHT.map(([n, t, d]) => (
              <div key={t}><b>{n}</b><span>{t}</span></div>
            ))}
          </div>
        </div>
        <aside className="hero-card" aria-label="Cara kerja DMS">
          <h3>⚡ Cara Kerja · 10–60 detik</h3>
          <div className="step-row"><span className="step-num">1</span><div><b>Petugas isi Excel seperti biasa</b><small>Buka file divisi-nya → isi kasus → <code>Ctrl+S</code>. Tidak ada langkah baru (R-88).</small></div></div>
          <div className="step-row"><span className="step-num">2</span><div><b>Sistem membaca otomatis</b><small>Pengawas folder mendeteksi perubahan (3 dtk), parse header dari nama kolom, upsert idempoten (R-85).</small></div></div>
          <div className="step-row"><span className="step-num">3</span><div><b>TV & dashboard menyegar sendiri</b><small>Satu divisi per layar, KPI dihitung dari log kasus, gerbang absensi R-81 (R-80/R-01).</small></div></div>
          <div style={{ marginTop: 12, borderTop: '1px solid #eef1f7', paddingTop: 12, fontSize: 12, color: 'var(--grey)' }}>
            ⚠️ Petugas <b>tidak perlu</b> upload, ekspor, atau mengisi ulang di aplikasi — kolom milik Excel bersifat baca-saja (R-89).
          </div>
        </aside>
      </section>

      {/* 5 PILAR */}
      <div className="section-title">
        <h2>Lima Pilar Monitoring</h2>
        <p>Satu pilar per layar · kolom mengikuti kontrak Excel (R-83) · klik untuk detail</p>
      </div>
      <div className="pilar-grid">
        {PILARS.map((p) => (
          <Link key={p.key} to={`/pilar/${p.key}`} className="pilar-card card">
            <div className="pilar-head" style={{ background: p.warna, color: p.teksGelap ? '#2b2b28' : '#fff' }}>
              <small>Pilar</small>
              <h3>{p.nama}</h3>
            </div>
            <div className="pilar-body">
              <p>{p.deskripsi}</p>
              <span className="pilar-tag">{p.sheet}</span>
              <span className="pilar-link">Buka pilar →</span>
            </div>
          </Link>
        ))}
      </div>

      {/* ALUR CEPAT */}
      <div className="section-title">
        <h2>Alur Satu Pintu</h2>
        <p>Dari QR di TV sampai rapat pagi — semua peran lewat pintu yang sama (R-82)</p>
      </div>
      <div className="card card-pad" style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 14 }}>
        {[
          ['📷', 'Pindai QR di TV', 'atau buka /absensi di perangkat ini'],
          ['✅', 'Konfirmasi kehadiran', 'wajib sebelum DMS dibuka (R-81)'],
          ['📊', 'Divisi mulai rotasi', 'SHE → Quality → Produksi → Delivery → Teknik'],
          ['🗣️', 'Rapat pagi pakai angka TV', 'satu sumber kebenaran, tanpa rekap ulang (R-01)'],
        ].map(([ico, t, d], i) => (
          <div key={i} style={{ textAlign: 'center', padding: '8px 6px' }}>
            <div style={{ fontSize: 34 }}>{ico}</div>
            <b style={{ display: 'block', color: 'var(--navy)', margin: '8px 0 4px', fontSize: 14 }}>{i + 1}. {t}</b>
            <span style={{ fontSize: 12, color: 'var(--grey)' }}>{d}</span>
          </div>
        ))}
      </div>
    </>
  )
}
