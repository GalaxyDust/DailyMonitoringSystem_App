import { PAPAN, PILAR_TAMPILAN, SESI } from '../data/tampilanMain'

/**
 * Landing TV (A-01) — route `/`.
 * Acuan desain: docs/mockup/index.html, layar "LANDING · TV (A-01)".
 *
 * FASE TAMPILAN — sengaja belum mengambil data:
 * - Tidak ada fetch, tidak ada API, tidak ada state server.
 * - Semua isi berasal dari `data/tampilanMain.js` (contoh statis).
 * - Nanti tinggal ganti sumber data; struktur komponen tidak perlu diubah.
 *
 * Aturan desain yang dipegang (docs/FRONTEND_STRUCTURE.md §9 & §5):
 * - Layar TV: font besar, kontras tinggi, jarak lega.
 * - TANPA tautan /dashboard dalam bentuk apa pun (A-02).
 * - Delivery & Teknik tampil "menunggu berkas" — bukan "0 kasus" (Status Berkas Jujur).
 * - Warna pilar dari konstanta, bukan hardcode di sini.
 */

const KELAS_STATUS = {
  tersinkron: 'ok',
  belum_diisi: 'warn',
  belum_tersinkron: 'bad',
  menunggu_berkas: 'warn',
}

/**
 * Label status untuk layar TV: spasi, bukan garis bawah.
 * "menunggu_berkas" → "menunggu berkas" supaya terbaca petugas lantai.
 */
function labelStatus(status) {
  return String(status ?? '').replace(/_/g, ' ')
}

function PilarCard({ pilar }) {
  const kelas = KELAS_STATUS[pilar.status] ?? 'warn'

  return (
    <a
      className={`pilar ${pilar.key}${pilar.teksGelap ? ' dark' : ''}`}
      href={`#/pilar/${pilar.key}`}
      aria-label={`${pilar.nama} — ${labelStatus(pilar.status)}`}
    >
      <div className="head">
        <span className="num">{pilar.nomor}</span>
        <span className="nama">{pilar.nama}</span>
      </div>

      <div className="body">
        <p className="desc">{pilar.deskripsi}</p>

        <p className="sheet">
          {pilar.terdaftar ? (
            <>
              berkas <code>{pilar.sheet}</code> · {pilar.kasus} kasus ·{' '}
              <code className={`st ${kelas}`}>{labelStatus(pilar.status)}</code>
            </>
          ) : (
            <>
              berkas <code>belum didaftarkan</code> · status{' '}
              <code className={`st ${kelas}`}>{labelStatus(pilar.status)}</code>
            </>
          )}
        </p>

        <span className="go">{pilar.terdaftar ? 'BUKA HALAMAN →' : 'LIHAT STATUS →'}</span>
      </div>
    </a>
  )
}

export default function Main() {
  const dikonfirmasi = SESI.status === 'DIKONFIRMASI'

  return (
    <div className="screen">
      {/* ── Header papan: identitas + jam ── */}
      <header className="board-head">
        <div className="brand">
          <img src="/logo-192.png" alt="" width="52" height="52" />
          <h1>
            DMS
            <small>Daily Monitoring System · Garudafood</small>
          </h1>
        </div>

        <div className="head-spacer" />

        <div className="chip">
          <b>{PAPAN.plant}</b>
          <span>{PAPAN.plantLabel}</span>
        </div>

        <div className="chip">
          <b>{PAPAN.tanggal}</b>
          <span>
            {PAPAN.hari} · Shift {PAPAN.shift}
          </span>
        </div>

        <div className="chip gold">
          <b className="big">{PAPAN.jam}</b>
          <span>WIB · Excel {PAPAN.excel}</span>
        </div>
      </header>

      {/* ── Isi: panel QR (kiri) + menu pilar (kanan) ── */}
      <div className="landing-main">
        <aside className="qr-panel" aria-label="Panel QR absensi">
          <p className="qr-kicker">ABSENSI DULU</p>

          <h2 className="qr-title">
            PINDAI
            <br />
            UNTUK ABSEN
          </h2>

          <div className="qr-box">
            <img src={SESI.qrSrc} alt="QR absensi sesi berjalan" width="212" height="212" />
          </div>

          <p className="qr-meta">
            <b>Sesi {SESI.nama}</b>
            <br />
            {SESI.qrTujuan} · berlaku untuk shift ini saja · dapat dicabut Admin
          </p>

          <span className={`pill ${dikonfirmasi ? 'ok' : 'open'}`}>
            <span className={`dot${dikonfirmasi ? '' : ' blink'}`} aria-hidden="true" />
            {dikonfirmasi ? 'KEHADIRAN DIKONFIRMASI' : 'SESI DIBUKA'}
          </span>

          <p className="hadir">
            Hadir <b>{SESI.hadir}</b> / {SESI.total} orang
          </p>
        </aside>

        <section className="menu-pilar" aria-label="Menu pilar DMS">
          <div className="menu-title">
            <h2>MENU PILAR</h2>
            <span>satu divisi per layar · kolom mengikuti Excel · angka baca-saja</span>
          </div>

          <div className="pillars">
            {PILAR_TAMPILAN.map((pilar) => (
              <PilarCard key={pilar.key} pilar={pilar} />
            ))}

            {/* Kartu penanda rotasi TV — bukan tautan (A-02). */}
            <article className="pilar ringkasan" aria-label="Ringkasan putaran">
              <div className="head">
                <span className="num">∑</span>
                <span className="nama">RINGKASAN</span>
              </div>
              <div className="body">
                <p className="desc">Akhir putaran — rekap lima divisi hari ini</p>
                <p className="sheet">tampil otomatis di TV lantai (rotasi)</p>
                <span className="go muted">DI TV → /</span>
              </div>
            </article>
          </div>
        </section>
      </div>

      {/* ── Footer strip ── */}
      <footer className="strip">
        <span>
          <b>Alur:</b> absensi → divisi → review → kunci
        </span>
        <span aria-hidden="true">·</span>
        <span>
          <b>Sumber:</b> Excel (baca-saja)
        </span>
        <span aria-hidden="true">·</span>
        <span>
          <b>Data:</b> {PAPAN.tanggal} · {PAPAN.excel}
        </span>
        <span aria-hidden="true">·</span>
        <span>
          <b>Nol upload</b>
        </span>
        <span className="a01">A-01 · TAMPIL DI SEMUA TV · TANPA LOGIN</span>
      </footer>
    </div>
  )
}
