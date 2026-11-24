// Data contoh (fallback) — dipakai bila backend Flask /api/state tidak terjangkau.
// Bentuknya mengikuti docs/API_CONTRACT.md (GET /api/state, v1).

const PERIODE = ['S1', 'S2', 'S3', 'Harian', 'Minggu', 'Bulan']
const tgl = (offsetHari) => {
  const d = new Date()
  d.setDate(d.getDate() - offsetHari)
  return d.toISOString().slice(0, 10)
}

function kpiRow(item, target, vals, sts) {
  return { item, target, vals: vals.map((v, i) => ({ v: String(v), st: sts[i] })) }
}

function buatKpi(divisi, seed) {
  const total = seed.total
  const open = seed.open
  const close = total - open
  const comp = total ? close / total : null
  const compStr = comp === null ? '—' : comp.toFixed(2).replace('.', ',')
  const compSt = comp === null ? 3 : comp >= 0.8 ? 0 : 1
  const rows = [
    kpiRow('Kasus tercatat', '—', [seed.s1, seed.s2, seed.s3, total, total + 9, total + 31], [0, 0, 0, 0, 0, 0]),
    kpiRow('Open', '0', [seed.s1o ?? 1, seed.s2o ?? 0, seed.s3o ?? 0, open, open + 3, open + 6], [open > 0 ? 1 : 0, 0, 0, open > 0 ? 1 : 0, 1, 1]),
    kpiRow('Close', '—', [Math.max(seed.s1 - 1, 0), seed.s2, seed.s3, close, close + 6, close + 24], [0, 0, 0, 0, 0, 0]),
    kpiRow('PICA completion rate', '0,80', ['0,71', '0,83', '—', compStr, '0,80', '0,82'], [1, 0, 3, compSt, 0, 0]),
    kpiRow('Lewat tenggat', '0', [0, 1, 0, seed.lewat, seed.lewat + 1, seed.lewat + 2], [0, 2, 0, seed.lewat > 0 ? 2 : 0, 2, 2]),
  ]
  if (divisi === 'produksi') {
    rows.splice(1, 0, kpiRow('Downtime (min)', '0', [45, 20, 0, seed.dt, 130, 410], [2, 2, 0, seed.dt > 0 ? 2 : 0, 2, 2]))
  }
  return rows
}

const KOLOM = {
  she: [['Tgl', 5], ['Shift', 4], ['LBN', 8], ['Area', 8], ['Kat. Safety', 9], ['Problem Statement', 19], ['RootCause', 13], ['Action Plan', 13], ['PIC', 6], ['Due', 5], ['Umur', 4], ['Status', 6]],
  quality: [['Tanggal', 5], ['Shift', 4], ['LBN', 8], ['Category', 8], ['Prioritas', 6], ['Problem', 17], ['Validasi QCP', 13], ['Root Cause', 12], ['Action Plan', 12], ['PIC', 6], ['Due', 5], ['Status', 6]],
  produksi: [['Date', 5], ['Shift', 4], ['LBN', 8], ['Category', 8], ['Prioritas', 6], ['Problem', 17], ['DT (min)', 6], ['RootCause', 12], ['Corrective / Preventive', 13], ['PIC', 6], ['Due', 5], ['Status', 6], ['O / R', 4]],
  delivery: [['Tgl', 6], ['Shift', 5], ['PO', 10], ['Plan vs Real', 24], ['Sebab', 18], ['Tindakan', 18], ['PIC', 8], ['Status', 8]],
  teknik: [['Tgl', 6], ['Shift', 5], ['Mesin', 10], ['Temuan / Work Order', 24], ['Sebab', 18], ['Tindakan', 18], ['PIC', 8], ['Status', 8]],
}

const SEED = {
  she: { total: 4, open: 2, lewat: 1, s1: 2, s2: 1, s3: 1, dt: 0 },
  quality: { total: 6, open: 3, lewat: 1, s1: 3, s2: 2, s3: 1, dt: 0 },
  produksi: { total: 9, open: 5, lewat: 2, s1: 5, s2: 3, s3: 1, dt: 85 },
  delivery: { total: 0, open: 0, lewat: 0, s1: 0, s2: 0, s3: 0, dt: 0 },
  teknik: { total: 0, open: 0, lewat: 0, s1: 0, s2: 0, s3: 0, dt: 0 },
}

const BARIS = {
  she: [
    ['6 Nov', '1', 'Line 9', 'Frying', 'Near Miss', 'Pelindung belt frying terbuka saat shift 1', 'Baut cover lepas, tidak ada pengecekan rutin', 'Pasang cover + cek per shift', 'Dhani', '9 Nov', '3', 'OPEN'],
    ['6 Nov', '1', 'Line 9', 'Packing', 'Unsafe action', 'Operator naik conveyor tanpa APD', 'Jalur tanggap jauh, belum tersedia akses', 'Sediakan tangga + briefing K3', 'Rani', '8 Nov', '2', 'PROGRESS'],
    ['5 Nov', '3', 'Line 2', 'Gudang RM', 'Housekeeping', 'Tumpukan karung menutup jalur evakuasi', 'Area staging tidak ditandai', 'Tandai area + rapikan', 'Sigit', '6 Nov', '5', 'OPEN'],
    ['4 Nov', '1', 'Line 9', 'Seasoning', 'APD', 'Sarung tangan tidak dipakai saat membilas', 'Stok sarung tangan ukuran L habis', 'Restock + cek harian', 'Yanti', '5 Nov', '6', 'CLOSE'],
  ],
  quality: [
    ['6 Nov', '1', 'Line 9', 'Packing', 'High', 'Defect seal tidak rapat pada standing pouch', 'Suhu sealer di bawah SOP', 'Set suhu 175°C + verifikasi tiap jam', 'Dewi', '7 Nov', 'OPEN'],
    ['6 Nov', '2', 'Line 9', 'Filling', 'Medium', 'Berat isi kurang 4% dari klaim', 'Timbangan tidak terkalibrasi', 'Kalibrasi + double check', 'Budi', '8 Nov', 'OPEN'],
    ['5 Nov', '1', 'Line 10', 'Frying', 'High', 'Kontaminasi minyak: partikel asing > 2 mm', 'Filter minyak terlambat diganti', 'Ganti filter + pengecekan per shift', 'Ayu', '6 Nov', 'PROGRESS'],
    ['4 Nov', '2', 'Line 2', 'Seasoning', 'Low', 'Rasa tidak konsisten batch ke batch', 'Dosis bumbu manual', 'Pasang dosing machine', 'Eko', '12 Nov', 'CLOSE'],
  ],
  produksi: [
    ['6 Nov', '1', 'Line 9', 'Machine', 'High', 'Mesin MHM39 stop — BCAT sensor error', 'Sensor BCAT kotor dan aus', 'Ganti sensor + PM mingguan', 'Teknik', '6 Nov', '55', 'OPEN', 'R'],
    ['6 Nov', '1', 'Line 9', 'Machine', 'Medium', 'SVB13 downtime resin conveyor macet', 'Resin conveyor aus', 'Ganti belt conveyor', 'Tekpro', '7 Nov', '30', 'PROGRESS', 'R'],
    ['5 Nov', '2', 'Line 10', 'Setting', 'Medium', 'Changeover pilus terlalu lama 45 menit', 'Setup tidak standar', 'OPL changeover + checklist', 'Andi', '9 Nov', '45', 'OPEN', 'O'],
    ['4 Nov', '1', 'Line 2', 'Machine', 'High', 'MHM12 motor utama overheat', 'Pelumas kurang + bearing aus', 'Ganti bearing + jadwalkan PM', 'Teknik', '5 Nov', '72', 'OPEN', 'R'],
    ['3 Nov', '3', 'Line 9', 'Operator', 'Low', 'Output di bawah target 12%', 'Operator baru belum lancar', 'Pendampingan 1 minggu', 'Sari', '10 Nov', '0', 'CLOSE', 'O'],
  ],
}

const BERKAS = {
  she: [{ id: 'SN-SHE', path: '12. Konsep Penilaian DMS Snack Des 24.xlsx', sheet: 'Resume SHE', status: 'aktif', sinkron: `${tgl(0)} 06:31:12`, pesan: 'header baris 17 · 2 baris dikarantina' }],
  quality: [{ id: 'SN-QC', path: '12. Konsep Penilaian DMS Snack Des 24.xlsx', sheet: 'Resume QC', status: 'aktif', sinkron: `${tgl(0)} 06:31:40`, pesan: 'header baris 19 · 1 baris dikarantina' }],
  produksi: [{ id: 'SN-PROD', path: '12. Konsep Penilaian DMS Snack Des 24.xlsx', sheet: 'Resume Prod', status: 'aktif', sinkron: `${tgl(0)} 06:31:58`, pesan: 'header baris 24 · 58 baris dikarantina' }],
  delivery: [],
  teknik: [],
}

function kolomDari(key) {
  return KOLOM[key].map(([nama, bobot]) => ({ nama, bobot }))
}
function barisDari(key) {
  return (BARIS[key] || []).map((s, i) => {
    // Produksi: elemen terakhir adalah kolom O / R, status ada di posisi sebelumnya
    const status = key === 'produksi' ? s[s.length - 2] : s[s.length - 1]
    return {
      sel: s,
      status: ['OPEN', 'PROGRESS', 'CLOSE'].includes(status) ? status : 'OPEN',
      flag: '',
      kunci: `demo-${key}-${i}`,
      sumber_id: BERKAS[key][0]?.id || '',
      baris_excel: 20 + i,
    }
  })
}

const NAMA = ['Ahmad', 'Budi', 'Citra', 'Dhani', 'Eko', 'Fajar', 'Gilang', 'Hana', 'Indra', 'Joko', 'Kiki', 'Lina', 'Maya', 'Novi', 'Omar', 'Putri', 'Queen', 'Rani', 'Sigit', 'Tari', 'Udin', 'Vira', 'Wawan', 'Yudi', 'Zaki', 'Sari', 'Dewi', 'Ayu']

export function buatDemoState(plant = 'Snack') {
  const tanggal = tgl(0)
  const halaman = ['she', 'quality', 'produksi', 'delivery', 'teknik'].map((key) => {
    const seed = SEED[key]
    const menunggu = key === 'delivery' || key === 'teknik'
    return {
      key,
      nama: { she: 'SHE / SAFETY', quality: 'QUALITY', produksi: 'PRODUKSI / PRODUCTIVITY', delivery: 'DELIVERY', teknik: 'TECHNIC PERFORM' }[key],
      warna: { she: '#B02F2F', quality: '#D7B32A', produksi: '#A62E2E', delivery: '#2E7D46', teknik: '#2A5CA0' }[key],
      durasi: { she: 25, quality: 25, produksi: 30, delivery: 20, teknik: 20 }[key],
      status: menunggu ? 'menunggu_berkas' : 'tersinkron',
      pesan: menunggu ? 'Berkas Excel divisi ini belum didaftarkan (R-86)' : '',
      terdaftar: !menunggu,
      sinkron_terakhir: menunggu ? '' : `${tanggal} 06:31:00`,
      jumlah: seed.total,
      kpi: menunggu ? [] : buatKpi(key, seed),
      kolom: kolomDari(key),
      baris: barisDari(key),
      berkas: BERKAS[key],
    }
  })
  const ringkasan = halaman.map((h) => ({
    key: h.key,
    nama: h.nama,
    warna: h.warna,
    jumlah: h.jumlah,
    status: h.status,
    open: h.status === 'tersinkron' ? String(SEED[h.key].open) : '—',
    completion: h.status === 'tersinkron' ? '0,75' : '—',
    lewat: h.status === 'tersinkron' ? String(SEED[h.key].lewat) : '—',
  }))
  return {
    plant,
    line: '*',
    label_line: 'Semua line',
    tanggal,
    hari_ini: tgl(0),
    demo: true,
    tanggal_tersedia: [tgl(0), tgl(1), tgl(2), tgl(6), tgl(13)],
    sesi: {
      sesi_id: `${plant}-*-${tanggal}-1`,
      plant, line: '*', tanggal, shift: '1',
      status: 'DIBUKA', token: 'demo-token',
      dibuka_pada: `${tanggal} 06:00:00`, dikonfirmasi_pada: null,
    },
    absensi: {
      nama: NAMA.map((nama, i) => ({ nama, status: i === 3 ? 'sakit' : i === 9 ? 'izin' : i === 17 ? 'terlambat' : 'hadir' })),
      total: NAMA.length,
      hitung: { hadir: 25, sakit: 1, izin: 1, alpa: 0, terlambat: 1, 'dinas luar': 0, 'belum pasti': 0 },
      dikonfirmasi: false,
    },
    halaman,
    ringkasan,
    durasi: { absensi: 30, she: 25, quality: 25, produksi: 30, delivery: 20, teknik: 20, ringkasan: 20 },
    pengawas: { hidup: false, putaran: 0, terakhir: null, perubahan: [] },
    jam: new Date().toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' }).replace(':', '.'),
    _demoFallback: true,
  }
}
