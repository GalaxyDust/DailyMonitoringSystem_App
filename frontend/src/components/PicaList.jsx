import { StatusPill } from './StatusPill'

/** PICA terbuka — diambil dari baris berstatus non-CLOSE (maks 4). */
export function PicaList({ baris = [], kolom = [] }) {
  const idx = (names) => {
    for (const n of names) {
      const i = kolom.findIndex((c) => c.nama === n)
      if (i >= 0) return i
    }
    return -1
  }
  const iProb = idx(['Problem Statement', 'Problem'])
  const iSebab = idx(['RootCause', 'Root Cause'])
  const iTindak = idx(['Action Plan', 'Corrective / Preventive', 'Tindakan'])
  const iPic = idx(['PIC'])
  const iDue = idx(['Due'])
  const pick = (r, i) => (i >= 0 ? r.sel[i] : '—')
  const open = baris.filter((b) => b.status !== 'CLOSE').slice(0, 4)

  return (
    <div className="card card-pad">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 10, marginBottom: 10 }}>
        <h3 style={{ color: 'var(--navy)', fontSize: 15 }}>PICA TERBUKA</h3>
        <small style={{ color: 'var(--grey)', fontWeight: 600 }}>Problem → Rootcause → Action · PIC · Due</small>
      </div>
      {open.length === 0 ? (
        <p style={{ color: 'var(--grey)', fontSize: 13 }}>Tidak ada PICA terbuka pada tanggal ini.</p>
      ) : (
        <div className="pica-grid">
          {open.map((r, i) => (
            <div key={r.kunci || i} className="pica-item">
              <StatusPill status={r.status} />
              <b style={{ display: 'block', marginTop: 6 }}>{pick(r, iProb)}</b>
              <dl>
                <dt>Rootcause</dt><dd>{pick(r, iSebab)}</dd>
                <dt>Action</dt><dd>{pick(r, iTindak)}</dd>
                <dt>PIC</dt><dd>{pick(r, iPic)}</dd>
                <dt>Due</dt><dd>{pick(r, iDue)}</dd>
              </dl>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
