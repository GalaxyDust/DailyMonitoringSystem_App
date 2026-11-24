import { Link, NavLink, useNavigate } from 'react-router-dom'
import { PILARS, PLANTS } from '../constants'

/** Layout utama: topbar (logo + nav + plant switch) + konten + footer. */
export function Layout({ plant, onPlantChange, online, children }) {
  const navigate = useNavigate()
  return (
    <div className="shell">
      <header className="topbar">
        <div className="topbar-inner">
          <Link className="brand" to="/">
            <img src="/logo.png" alt="Garudafood Daily Monitoring" />
            <span className="brand-name">DMS<small>Garudafood Daily Monitoring</small></span>
          </Link>
          <nav className="nav" aria-label="Navigasi utama">
            <NavLink to="/" end className={({ isActive }) => 'navlink' + (isActive ? ' active' : '')}>Beranda</NavLink>
            <NavLink to="/dashboard" className={({ isActive }) => 'navlink' + (isActive ? ' active' : '')}>Dashboard</NavLink>
            {PILARS.map((p) => (
              <NavLink key={p.key} to={`/pilar/${p.key}`} className={({ isActive }) => 'navlink' + (isActive ? ' active' : '')}>
                {p.short}
              </NavLink>
            ))}
            <NavLink to="/absensi" className={({ isActive }) => 'navlink' + (isActive ? ' active' : '')}>Absensi</NavLink>
          </nav>
          <div className="topbar-right">
            <span className={`conn${online ? '' : ' off'}`} title={online ? 'Terhubung ke /api/state' : 'Server tidak terjangkau — data contoh'}>
              <span className="conn-dot" />{online ? 'LIVE' : 'CONTOH'}
            </span>
            <select className="plant-select" value={plant} onChange={(e) => onPlantChange(e.target.value)} aria-label="Pilih plant">
              {PLANTS.map((p) => <option key={p.id} value={p.id}>{p.label}</option>)}
            </select>
          </div>
        </div>
      </header>

      <main className="main">
        <div className={`banner ${online ? 'demo' : 'offline'}`} role="status">
          <span aria-hidden="true">{online ? '🟡' : '🔌'}</span>
          <span>
            {online
              ? 'Data dari server DMS. Bila ini mode demo, pita MODE DEMO tampil di TV — angka dihitung dari log kasus Excel asli.'
              : 'Server /api/state tidak terjangkau — menampilkan DATA CONTOH. Jalankan backend: python3 app/server.py (port 8000).'}
          </span>
        </div>
        {children}
      </main>

      <footer className="footer">
        <div className="footer-inner">
          <span><b>DMS — Garudafood Daily Monitoring System</b> · satu kali isi di Excel, semua layar membaca angka yang sama (R-01).</span>
          <span>R-81 Absensi dulu · R-85 Excel otomatis · R-88 tanpa upload · R-89 kolom milik Excel · <a href="/admin">Panel Admin</a></span>
        </div>
      </footer>
    </div>
  )
}
