import { Link } from 'react-router-dom'

export function NotFound() {
  return (
    <div className="card empty-state" style={{ maxWidth: 640, margin: '40px auto' }}>
      <span className="tag">404</span>
      <h3>Halaman tidak ditemukan</h3>
      <p>Alamat yang kamu buka tidak dikenal. Kembali ke Beranda atau Dashboard.</p>
      <div style={{ marginTop: 16, display: 'flex', gap: 10, justifyContent: 'center' }}>
        <Link className="btn btn-primary" to="/">Beranda</Link>
        <Link className="btn btn-outline" to="/dashboard">Dashboard</Link>
      </div>
    </div>
  )
}
