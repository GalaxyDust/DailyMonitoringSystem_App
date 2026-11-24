import { StatusPill } from './StatusPill'

/**
 * Tabel kasus — kolom mengikuti kontrak Excel (R-83), sel sudah diformat server.
 * sel sejajar dengan kolom (indeks sama).
 */
export function KasusTable({ kolom = [], baris = [], judul, sub }) {
  return (
    <div className="card">
      <div className="card-pad" style={{ paddingBottom: 0 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 12, flexWrap: 'wrap' }}>
          <h3 style={{ color: 'var(--navy)', fontSize: 15 }}>{judul || 'KASUS'}</h3>
          <small style={{ color: 'var(--grey)', fontWeight: 600 }}>{sub || 'kolom mengikuti Excel (R-83) · tidak diubah dari aplikasi'}</small>
        </div>
      </div>
      <div className="kasus-wrap" style={{ padding: '10px 14px 14px' }}>
        {baris.length === 0 ? (
          <p style={{ color: 'var(--grey)', padding: '18px 6px', fontSize: 13 }}>Tidak ada kasus pada tanggal ini.</p>
        ) : (
          <table className="kasus-table">
            <thead>
              <tr>{kolom.map((c) => <th key={c.nama}>{c.nama}</th>)}</tr>
            </thead>
            <tbody>
              {baris.slice(0, 8).map((r, i) => (
                <tr key={r.kunci || i}>
                  {kolom.map((c, j) => {
                    const v = r.sel[j] ?? '—'
                    const isStatus = c.nama === 'Status'
                    const isMono = ['Tgl', 'Tanggal', 'Date', 'Shift', 'LBN', 'PIC', 'Due', 'PO', 'Mesin', 'Umur'].includes(c.nama)
                    return (
                      <td key={j} className={isMono ? 'mono' : ''} title={r.flag && c.nama === 'PIC' ? `${v} — ⚠ ${r.flag}` : v}>
                        {isStatus ? <StatusPill status={v} /> : v}
                        {r.flag && c.nama === 'PIC' && <span className="flag-ico">⚠</span>}
                      </td>
                    )
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  )
}
