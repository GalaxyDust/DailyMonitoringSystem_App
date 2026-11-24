// Konstanta DMS — 5 pilar, urutan & warna mengikuti backend (app/dms_core.DIVISI)
// dan kontrak TV (app/server.py KOLOM/DURASI).
export const PILARS = [
  {
    key: 'she',
    nama: 'SHE / SAFETY',
    short: 'SHE',
    warna: '#B02F2F',
    teksGelap: false,
    deskripsi: 'Kecelakaan, near miss, temuan KAK, status tindakan keselamatan kerja.',
    sheet: 'Resume SHE',
    aturan: 'R-15 (produksi catat durasi, SHE catat sebab)',
  },
  {
    key: 'quality',
    nama: 'QUALITY',
    short: 'QUALITY',
    warna: '#D7B32A',
    teksGelap: true,
    deskripsi: 'Defect per line, critical point, kontaminasi, hold/release, validasi QCP.',
    sheet: 'Resume QC',
    aturan: 'R-83 (kolom mengikuti kontrak Excel)',
  },
  {
    key: 'produksi',
    nama: 'PRODUKSI / PRODUCTIVITY',
    short: 'PRODUKSI',
    warna: '#A62E2E',
    teksGelap: false,
    deskripsi: 'Output vs target, downtime, OEE, checklist harian, sebab singkat berhenti line.',
    sheet: 'Resume Prod',
    aturan: 'R-17 (downtime > 30 menit jadi kasus Teknik)',
  },
  {
    key: 'delivery',
    nama: 'DELIVERY',
    short: 'DELIVERY',
    warna: '#2E7D46',
    teksGelap: false,
    deskripsi: 'Plan vs real PO, keterlambatan pengiriman, kesiapan muat, on-time delivery.',
    sheet: 'Resume Delivery',
    aturan: 'R-86 (satu berkas per divisi)',
  },
  {
    key: 'teknik',
    nama: 'TECHNIC PERFORM',
    short: 'TEKNIK',
    warna: '#2A5CA0',
    teksGelap: false,
    deskripsi: 'Penyebab teknis downtime, PM, spare part, kalibrasi mesin & utilitas.',
    sheet: 'Resume Teknik',
    aturan: 'R-18 (diagnosa ≤ 4 jam kategori A)',
  },
]

export const PILAR_KEYS = PILARS.map((p) => p.key)
export const getPilar = (key) => PILARS.find((p) => p.key === key)

export const PLANTS = [
  { id: 'Snack', label: 'Snack' },
  { id: 'EP', label: 'EP — Exist Plant' },
  { id: 'NP', label: 'NP — New Plant' },
]

export const SIKLUS_ABSENSI = ['hadir', 'sakit', 'izin', 'alpa', 'terlambat', 'belum pasti']

// Warna sel KPI (st) dari backend/API (docs/API_CONTRACT.md §1.8)
export const ST_WARNA = ['#1C3E8A', '#C22A26', '#C22A26', '#A9A9A2']
export const ST_JUDUL = ['Sesuai target', 'Di bawah target', 'Lewat batas', 'Belum diisi']

export const STATUS_KASUS = {
  OPEN: { label: 'OPEN', warna: '#B3261E', bg: '#FDECEA' },
  PROGRESS: { label: 'PROGRESS', warna: '#8A6C10', bg: '#FBF3D9' },
  CLOSE: { label: 'CLOSE', warna: '#1E6B3A', bg: '#E8F5EC' },
}

export const STATUS_HALAMAN = {
  tersinkron: { label: 'Tersinkron', warna: '#1E6B3A', bg: '#E8F5EC' },
  belum_diisi: { label: 'Belum diisi', warna: '#8A6C10', bg: '#FBF3D9' },
  belum_tersinkron: { label: 'Belum tersinkron', warna: '#B3261E', bg: '#FDECEA' },
  menunggu_berkas: { label: 'Menunggu berkas', warna: '#8A6C10', bg: '#FBF0D6' },
}
