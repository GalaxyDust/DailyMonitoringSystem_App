const PERIODE = ['Target', 'S1', 'S2', 'S3', 'Harian', 'Minggu', 'Bulan']

/**
 * Grid KPI per periode — Target · S1..S3 · Harian · Minggu · Bulan.
 * Bentuk data mengikuti API /api/state → halaman[].kpi (docs/API_CONTRACT.md §3.2.2).
 */
export function KpiGrid({ kpi, warna = '#1b2c57', gelap = false }) {
  if (!kpi || kpi.length === 0) {
    return <p style={{ color: 'var(--grey)', fontSize: 13 }}>KPI belum tersedia — berkas sumber belum terdaftar.</p>
  }
  return (
    <div className="kpi-table-wrap card">
      <table className="kpi-table">
        <thead>
          <tr>
            <th>KPI · dihitung dari log kasus Excel</th>
            {PERIODE.map((p) => <th key={p}>{p}</th>)}
          </tr>
        </thead>
        <tbody>
          {kpi.map((k) => (
            <tr key={k.item}>
              <td className="item">{k.item}</td>
              <td className="target">{k.target}</td>
              {k.vals.map((v, i) => (
                <td key={i}>
                  <span className={`cell st${v.st}${i === 3 ? ' now' : ''}`} title={i === 3 ? 'Harian (sekarang)' : PERIODE[i + 1]}>
                    {v.v}
                  </span>
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
