import { Link } from 'react-router-dom'
import { PILARS, getPilar } from '../constants'
import { PageStatusPill } from '../components/StatusPill'

const parseNum = (v) => {
  const n = parseFloat(String(v ?? '').replace(',', '.'))
  return Number.isFinite(n) ? n : 0
}

/** Dashboard — ringkasan 5 pilar untuk satu tanggal tampil. */
export function Dashboard({ state }) {
  const { ringkasan = [], tanggal, jam, pengawas, sesi } = state

  const total = ringkasan.reduce((a, r) => a + (r.status === 'tersinkron' ? r.jumlah : 0), 0)
  const open = ringkasan.reduce((a, r) => a + parseNum(r.open), 0)
  const lewat = ringkasan.reduce((a, r) => a + parseNum(r.lewat), 0)
  const completions = ringkasan.map((r) => parseNum(r.completion)).filter((n) => n > 0)
  const avgComp = completions.length ? completions.reduce((a, b) => a + b, 0) / completions.length : null
  const maxJumlah = Math.max(...ringkasan.map((r) => r.jumlah), 1)
  const tersinkron = ringkasan.filter((r) => r.status === 'tersinkron').length

  return (
    <>
      <div className="db-head">
        <div>
          <h1>📊 Dashboard 5 Pilar</h1>
          <p>Ringkasan tanggal <b>{tanggal}</b> · shift {sesi?.shift} · sesi {sesi?.status} · plant <b>{state.plant}</b> · {state.label_line}</p>
        </div>
        <div className="db-sync">
          <div>Sinkron Excel terakhir: <b>{jam}</b></div>
          <div>Pengawas folder: <b>{pengawas?.hidup ? `aktif · putaran ${pengawas.putaran}` : 'mati (mode contoh)'}</b></div>
          <div style={{ marginTop: 6 }}><Link to="/absensi" className="btn btn-primary btn-sm">✅ Absensi dulu (R-81)</Link></div>
        </div>
      </div>

      {/* Strip KPI agregat */}
      <div className="kpi-strip">
        <div className="card kpi-tile"><small>Kasus tanggal ini</small><b>{total}</b><span>dari {tersinkron}/5 pilar tersinkron</span></div>
        <div className="card kpi-tile"><small>Open</small><b style={{ color: open > 0 ? 'var(--red)' : 'var(--green)' }}>{open}</b><span>belum ditutup pada tanggal ini</span></div>
        <div className="card kpi-tile"><small>Completion rata-rata</small><b>{avgComp === null ? '—' : `${Math.round(avgComp * 100)}%`}</b><span>target 0,80 (80%)</span></div>
        <div className="card kpi-tile"><small>Lewat tenggat</small><b style={{ color: lewat > 0 ? 'var(--red)' : 'var(--green)' }}>{lewat}</b><span>status ≠ CLOSE &amp; due lewat</span></div>
      </div>

      {/* Kartu 5 pilar */}
      <div className="section-title">
        <h2>Status per Pilar</h2>
        <p>Klik kartu untuk KPI detail, tabel kasus &amp; PICA</p>
      </div>
      <div className="pillar-dash-grid">
        {PILARS.map((p) => {
          const r = ringkasan.find((x) => x.key === p.key) || {}
          const ter = r.status === 'tersinkron'
          const comp = parseNum(r.completion)
          return (
            <Link key={p.key} to={`/pilar/${p.key}`} className="pillar-dash card">
              <div className="pd-head" style={{ background: p.warna, color: p.teksGelap ? '#2b2b28' : '#fff' }}>
                <b>{p.short}</b>
                <PageStatusPill status={r.status || 'menunggu_berkas'} />
              </div>
              <div className="pd-body">
                <div className="pd-num">{ter ? r.jumlah : '—'}<small>kasus tanggal ini</small></div>
                <div className={`progress${comp < 0.8 ? ' low' : ''}`} style={{ marginTop: 10 }}>
                  <i style={{ width: `${Math.min(comp * 100, 100)}%` }} />
                </div>
                <div className="pd-kv"><span>Open</span><b>{ter ? r.open : '—'}</b></div>
                <div className="pd-kv"><span>Completion</span><b>{ter ? r.completion : '—'}</b></div>
                <div className="pd-kv"><span>Lewat tenggat</span><b style={{ color: parseNum(r.lewat) > 0 ? 'var(--red)' : 'inherit' }}>{ter ? r.lewat : '—'}</b></div>
              </div>
            </Link>
          )
        })}
      </div>

      {/* Perbandingan antar pilar (bar chart CSS) */}
      <div className="section-title">
        <h2>Perbandingan Beban Kerja</h2>
        <p>Jumlah kasus per pilar pada tanggal {tanggal}</p>
      </div>
      <div className="card card-pad">
        <div style={{ display: 'grid', gap: 12 }}>
          {PILARS.map((p) => {
            const r = ringkasan.find((x) => x.key === p.key) || {}
            const j = r.status === 'tersinkron' ? r.jumlah : 0
            const w = Math.max((j / maxJumlah) * 100, j > 0 ? 3 : 0)
            return (
              <div key={p.key} style={{ display: 'grid', gridTemplateColumns: '150px 1fr 46px', gap: 12, alignItems: 'center' }}>
                <span style={{ fontSize: 12, fontWeight: 800, color: 'var(--navy)', letterSpacing: 0.4 }}>{p.short}</span>
                <div className="progress" style={{ margin: 0, height: 18 }}>
                  <i style={{ width: `${w}%`, background: p.warna }} />
                </div>
                <b style={{ fontSize: 13, textAlign: 'right', fontVariantNumeric: 'tabular-nums' }}>{r.status === 'tersinkron' ? j : '—'}</b>
              </div>
            )
          })}
        </div>
        <p style={{ marginTop: 14, fontSize: 11.5, color: 'var(--grey)' }}>Angka dihitung dari log kasus pada berkas Excel tiap divisi — tidak ada angka karangan (R-01). Pilar tanpa berkas ditampilkan sebagai "—", bukan 0 (R-90).</p>
      </div>
    </>
  )
}
