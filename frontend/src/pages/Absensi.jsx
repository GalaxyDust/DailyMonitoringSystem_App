import { useState } from 'react'
import { api } from '../api/client'
import { SIKLUS_ABSENSI } from '../constants'

const KELAS = { hadir: '', sakit: 'sakit', izin: 'izin', alpa: 'alpa', terlambat: 'terlambat', 'belum pasti': 'belum' }

/**
 * Absensi shift — gerbang sebelum DMS (R-81).
 * Online: tulis ke /api/absensi & /api/konfirmasi.
 * Offline (server mati): tampilan tetap, aksi dinonaktifkan dengan penjelasan.
 */
export function Absensi({ state, online, reload }) {
  const a = state.absensi
  const [toast, setToast] = useState(null)
  const [sibuk, setSibuk] = useState(false)
  const dikonfirmasi = a.dikonfirmasi

  const showToast = (msg) => { setToast(msg); setTimeout(() => setToast(null), 3500) }

  const ketukChip = async (nama) => {
    if (!online) return showToast('Server tidak terjangkau — perubahan absensi tidak tersimpan.')
    if (dikonfirmasi) return showToast('Absensi sudah dikonfirmasi. Koreksi lewat Supervisor (R-81).')
    const sekarang = a.nama.find((n) => n.nama === nama)?.status || 'hadir'
    const berikut = SIKLUS_ABSENSI[(SIKLUS_ABSENSI.indexOf(sekarang) + 1) % SIKLUS_ABSENSI.length]
    setSibuk(true)
    try {
      await api.postAbsensi({ nama, status: berikut, plant: state.plant, line: state.line, perangkat: 'web' })
      await reload()
    } catch (err) {
      showToast(err.status === 409 ? 'Absensi sudah dikonfirmasi — koreksi lewat Supervisor.' : `Gagal: ${err.message}`)
    } finally {
      setSibuk(false)
    }
  }

  const konfirmasi = async () => {
    if (!online) return showToast('Server tidak terjangkau — tidak bisa mengonfirmasi.')
    setSibuk(true)
    try {
      await api.postKonfirmasi({ plant: state.plant, line: state.line, pelaku: 'web' })
      showToast('Kehadiran terkonfirmasi. Rotasi divisi terbuka (R-81).')
      await reload()
    } catch (err) {
      showToast(`Gagal: ${err.message}`)
    } finally {
      setSibuk(false)
    }
  }

  const h = a.hitung
  return (
    <>
      <div className="db-head">
        <div>
          <h1>✅ Absensi Shift {state.sesi?.shift}</h1>
          <p>{state.plant} · {state.label_line} · tanggal {state.tanggal} · status sesi <b>{state.sesi?.status}</b> · QR berlaku per shift (R-82)</p>
        </div>
        <PageGate dikonfirmasi={dikonfirmasi} />
      </div>

      <div className="abs-wrap">
        {/* KIRI — ringkasan + grid nama */}
        <section className="card card-pad">
          <div className="abs-big">
            <div className="num">{h.hadir || 0}</div>
            <div>
              <div className="lbl">hadir dari {a.total} orang</div>
              <div className="det">{h.sakit || 0} sakit · {h.izin || 0} izin · {h.alpa || 0} alpa · {h.terlambat || 0} terlambat · {h['belum pasti'] || 0} belum pasti</div>
              <div className="progress" style={{ marginTop: 10, height: 10, width: 260 }}>
                <i style={{ width: `${(100 * (h.hadir || 0)) / Math.max(a.total, 1)}%` }} />
              </div>
            </div>
          </div>
          <p style={{ fontSize: 12, color: 'var(--grey)', marginTop: 14 }}>Ketuk nama untuk mengubah status: <b>hadir → sakit → izin → alpa → terlambat → belum pasti</b>. Status awal semua hadir (R-32) — lapangan hanya menandai yang tidak hadir.</p>
          <div className="abs-grid">
            {a.nama.map((n) => (
              <button key={n.nama} className={`chip ${KELAS[n.status] || ''}`} onClick={() => ketukChip(n.nama)} disabled={sibuk || dikonfirmasi || !online} title={dikonfirmasi ? 'Terkunci — sudah dikonfirmasi' : `Klik: ubah ke status berikutnya`}>
                <span className="av">{n.nama.slice(0, 2).toUpperCase()}</span>
                <span><span className="nm">{n.nama}</span><br /><span className="stt">{n.status}</span></span>
              </button>
            ))}
          </div>
        </section>

        {/* KANAN — konfirmasi & penjelasan */}
        <aside className="abs-side">
          <div className="confirm-box">
            <h3>🔐 Gerbang DMS (R-81)</h3>
            <p>Absensi dikerjakan <b>lebih dulu</b>. Setelah tombol di bawah ditekan, sesi berubah jadi <b>DIKONFIRMASI</b>, rotasi divisi di TV terbuka, dan sisa status <b>belum pasti</b> otomatis menjadi hadir.</p>
            <button className="btn btn-gold" style={{ width: '100%', justifyContent: 'center' }} onClick={konfirmasi} disabled={dikonfirmasi || sibuk || !online}>
              {dikonfirmasi ? '✓ KEHADIRAN TERKONFIRMASI' : sibuk ? 'Mengonfirmasi…' : 'KONFIRMASI KEHADIRAN'}
            </button>
            <p style={{ marginTop: 12, fontSize: 11.5, opacity: 0.85 }}>Salah tandai setelah konfirmasi? Hanya Supervisor/DH yang bisa membuka ulang sesi, dengan alasan tercatat di audit (R-81).</p>
          </div>

          <div className="card card-pad">
            <h3 style={{ color: 'var(--navy)', fontSize: 13, letterSpacing: 1.2, textTransform: 'uppercase', marginBottom: 8 }}>Kenapa tidak ada tombol upload?</h3>
            <p style={{ fontSize: 12, color: 'var(--grey)' }}>Petugas tetap mengisi Excel seperti biasa dan menekan <code>Ctrl+S</code>. Folder kerja dipindahkan ke OneDrive sekali oleh IT (junction di path lama) — TV menyusul dalam 10–60 detik. Kolom Excel bersifat baca-saja (R-89).</p>
            <div style={{ display: 'flex', gap: 8, marginTop: 12, flexWrap: 'wrap' }}>
              <a className="btn btn-outline btn-sm" href="/admin">Panel Sinkron</a>
              <a className="btn btn-outline btn-sm" href="/">Buka TV</a>
            </div>
          </div>
        </aside>
      </div>

      {toast && <div className="toast" role="status">{toast}</div>}
    </>
  )
}

function PageGate({ dikonfirmasi }) {
  return dikonfirmasi
    ? <span className="pill ok"><i className="pill-dot" /> Rotasi divisi terbuka</span>
    : <span className="pill warn"><i className="pill-dot" /> Terkunci di Absensi (R-81)</span>
}
