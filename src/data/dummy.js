// Data dummy untuk dasbor DMS — bukan data produksi.
// Nanti diganti dengan respons API back-end (lihat app/ di repo).

export const user = {
  name: 'Dhani Pratama',
  role: 'Admin',
  initials: 'DP',
  plant: 'Snack · Line 9',
  tanggal: 'Sen, 30 Nov 2026',
}

export const navSections = [
  {
    label: 'Dashboard',
    items: [
      { id: 'ringkasan', label: 'Ringkasan', icon: 'grid' },
      { id: 'perbandingan', label: 'Perbandingan Plant', icon: 'compare' },
      { id: 'kasus', label: 'Kasus Terbuka', icon: 'alert', badge: '8' },
      { id: 'tren', label: 'Tren Pekan', icon: 'trending' },
      { id: 'laporan', label: 'Laporan & KPI', icon: 'fileText' },
    ],
  },
  {
    label: 'Monitoring',
    items: [
      { id: 'snack', label: 'Snack', icon: 'dot', dot: 'ok', hint: 'Pilot' },
      { id: 'ep', label: 'Exist Plant', icon: 'dot', dot: 'ok', hint: '59 line' },
      { id: 'np', label: 'New Plant', icon: 'dot', dot: 'warn', hint: '45 line' },
      { id: 'dairy', label: 'Dairy', icon: 'dot', dot: 'idle', hint: 'segera' },
    ],
  },
  {
    label: 'Aplikasi',
    items: [
      { id: 'tv', label: 'TV Lantai', icon: 'monitor' },
      { id: 'isian', label: 'Isian Papan', icon: 'edit' },
      { id: 'absensi', label: 'Absensi', icon: 'users' },
      { id: 'sinkron', label: 'Sinkron Excel', icon: 'sync' },
      { id: 'pengaturan', label: 'Pengaturan', icon: 'sliders', chevron: true },
    ],
  },
  {
    label: 'Administrasi',
    items: [
      { id: 'audit', label: 'Jejak Audit', icon: 'shield' },
      { id: 'pengguna', label: 'Pengguna & Peran', icon: 'userCheck' },
    ],
  },
]

export const kpiCards = [
  {
    id: 'kasus-hari-ini',
    label: 'Kasus Hari Ini',
    value: '96',
    delta: '+12 vs kemarin',
    trend: 'up',
    tone: 'purple',
    icon: 'clipboard',
  },
  {
    id: 'close-lengkap',
    label: 'Close Lengkap',
    value: '74%',
    delta: '+6 poin vs pekan lalu',
    trend: 'up',
    tone: 'green',
    icon: 'checkCircle',
  },
  {
    id: 'kelengkapan',
    label: 'Kelengkapan Pengisian',
    value: '92%',
    delta: '+4,1% vs pekan lalu',
    trend: 'up',
    tone: 'teal',
    icon: 'pieChart',
  },
  {
    id: 'lewat-tenggat',
    label: 'Lewat Tenggat',
    value: '8',
    delta: '-3 vs kemarin',
    trend: 'down',
    tone: 'orange',
    icon: 'clock',
  },
]

export const quickLinks = [
  { id: 'tv', title: 'TV Lantai', caption: 'Papan per divisi', icon: 'monitor', tint: 'purple' },
  { id: 'isian', title: 'Isian Papan', caption: 'Form leader & divisi', icon: 'edit', tint: 'green' },
  { id: 'kasus', title: 'Kasus', caption: 'Tindak lanjut & PICA', icon: 'alert', tint: 'orange' },
  { id: 'laporan', title: 'Laporan', caption: 'KPI & ekspor', icon: 'fileText', tint: 'blue' },
  { id: 'sinkron', title: 'Sinkron Excel', caption: 'Status ingest', icon: 'sync', tint: 'teal' },
  { id: 'atur', title: 'Pengaturan', caption: 'Target & profil TV', icon: 'sliders', tint: 'pink' },
]

// Tren 7 hari terakhir (Sen–Min)
export const weeklyCases = {
  labels: ['Sen', 'Sel', 'Rab', 'Kam', 'Jum', 'Sab', 'Min'],
  values: [14, 22, 19, 31, 42, 38, 55],
  yMax: 60,
  yTicks: [0, 20, 40, 60],
}

// Kasus per divisi (minggu berjalan)
export const divisionCases = {
  labels: ['SHE', 'QC', 'Produksi', 'Teknik', 'Delivery', 'Lain'],
  values: [62, 90, 78, 34, 24, 18],
  yMax: 100,
  yTicks: [0, 30, 60, 90],
}

export const notifications = [
  { id: 1, tone: 'danger', title: '8 kasus lewat tenggat', caption: '6 di antaranya di L2/L3 eskalasi' },
  { id: 2, tone: 'warn', title: 'Sinkron Excel tertunda · Exist Plant', caption: 'Berkas Resume Prod gagal 2×, coba lagi otomatis' },
  { id: 3, tone: 'info', title: 'Laporan November menunggu kunci', caption: 'Periode siap dilaporkan, menunggu plant head' },
]
