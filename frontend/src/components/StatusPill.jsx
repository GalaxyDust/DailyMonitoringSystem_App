import { STATUS_KASUS } from '../constants'

/** Pill status kasus: OPEN / PROGRESS / CLOSE */
export function StatusPill({ status }) {
  const s = STATUS_KASUS[status] || STATUS_KASUS.OPEN
  return (
    <span className="pill" style={{ background: s.bg, color: s.warna }}>
      <i className="pill-dot" /> {s.label}
    </span>
  )
}

/** Pill status halaman divisi (tersinkron / menunggu_berkas / …) */
export function PageStatusPill({ status }) {
  const map = {
    tersinkron: { cls: 'ok', label: 'Tersinkron' },
    belum_diisi: { cls: 'warn', label: 'Belum diisi' },
    belum_tersinkron: { cls: 'bad', label: 'Belum tersinkron' },
    menunggu_berkas: { cls: 'warn', label: 'Menunggu berkas' },
  }
  const m = map[status] || { cls: 'warn', label: String(status).replace(/_/g, ' ') }
  return (
    <span className={`pill ${m.cls}`}>
      <i className="pill-dot" /> {m.label}
    </span>
  )
}
