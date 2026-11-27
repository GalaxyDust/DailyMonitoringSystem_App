/**
 * Keadaan kosong yang jujur — FRONTEND_STRUCTURE.md §4.7.
 *
 * Dipakai halaman divisi saat status ≠ tersinkron (Status Berkas Jujur):
 * tag status · judul humanis · pesan penyebab dari API · jam acuan · daftar berkas.
 *
 * Catatan: jam acuan wajib, karena "belum diisi" berbeda dengan
 * "belum pernah tersinkron". Jangan tampilkan angka basi tanpa cap waktunya.
 */
export default function EmptyState({
  kelas = 'warn',
  label,
  judul,
  pesan,
  jamAcuan,
  berkas = [],
  aksi,
}) {
  return (
    <div className="empty-state" role="status">
      {label && (
        <p className={`empty-tag ${kelas}`}>
          <span className="dot" aria-hidden="true" />
          {label}
        </p>
      )}

      <h1 className="empty-title">{judul}</h1>

      {pesan && <p className="empty-msg">{pesan}</p>}

      {jamAcuan && <p className="empty-jam">{jamAcuan}</p>}

      {berkas.length > 0 && (
        <ul className="empty-berkas">
          {berkas.map((b) => (
            <li key={b.id ?? b.path}>
              <code>{b.sheet}</code>
              <span>{b.path}</span>
              <span className={`pill-sm ${b.status === 'aktif' ? 'ok' : 'bad'}`}>{b.status}</span>
            </li>
          ))}
        </ul>
      )}

      {aksi && <div className="empty-aksi">{aksi}</div>}
    </div>
  )
}
