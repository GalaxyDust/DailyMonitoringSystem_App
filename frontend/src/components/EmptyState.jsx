/**
 * Keadaan kosong jujur (R-84/R-90): "belum diisi" ≠ "belum tersinkron".
 * Halaman tetap tampil, tidak dilewati.
 */
export function EmptyState({ status = 'belum_diisi', pesan, berkas = [] }) {
  const judul = {
    menunggu_berkas: 'Menunggu berkas divisi',
    belum_tersinkron: 'Belum tersinkron',
    belum_diisi: 'Belum ada isian tanggal ini',
  }[status] || 'Belum ada data'

  return (
    <div className="card empty-state">
      <span className="tag">{String(status).replace(/_/g, ' ').toUpperCase()}</span>
      <h3>{judul}</h3>
      <p>{pesan || 'Berkas sumber belum tersedia untuk tanggal ini.'} Halaman ini tetap tampil dan tidak dilewati (R-84) — supaya jelas siapa yang belum mengisi, bukan layar mati.</p>
      {berkas.length > 0 && (
        <div style={{ marginTop: 16, display: 'grid', gap: 6 }}>
          {berkas.map((b) => (
            <code key={b.id} style={{ fontSize: 12 }}>{b.id} · {b.path} · {b.sheet || '?'} · {b.status}</code>
          ))}
        </div>
      )}
      {berkas.length === 0 && (
        <p style={{ marginTop: 14, fontSize: 12.5 }}>Daftarkan berkasnya di <code>app/registry.json</code> — tidak perlu membuat form baru (R-86).</p>
      )}
    </div>
  )
}
