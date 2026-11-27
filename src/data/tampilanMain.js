/**
 * Data tampilan Landing TV — contoh statis.
 *
 * Fase ini khusus TAMPILAN: belum ada pengambilan data, belum ada API,
 * belum ada state server. Semua nilai di bawah adalah contoh dari
 * docs/mockup/index.html agar tata letak bisa dinilai.
 *
 * Saat integrasi (fase berikutnya) file ini diganti sumber data sungguhan
 * (GET /api/state) tanpa mengubah komponennya.
 *
 * Angka di sini mengikuti contoh mockup: SHE 2 · Quality 7 · Produksi 19;
 * Delivery & Teknik belum punya berkas → "menunggu berkas", bukan 0 kasus.
 */

/** Identitas papan + jam. */
export const PAPAN = {
  plant: 'SNACK · LINE 9',
  plantLabel: 'Snack Plant',
  tanggal: '27 OKT 2023',
  hari: 'Jumat',
  shift: '1',
  jam: '06.43',
  excel: '06.31',
}

/** Sesi absensi yang sedang berjalan (QR Satu Pintu). */
export const SESI = {
  nama: 'Snack-L9-27Oct',
  status: 'DIBUKA',
  hadir: 28,
  total: 28,
  /** Gambar QR contoh — di produksi berasal dari /qr/<token>.png */
  qrSrc: '/qr-contoh.png',
  qrTujuan: 'dms.contoh.id/s/9f2c-s1',
}

/**
 * Lima pilar, urut seperti backend (SHE → Teknik).
 * `terdaftar: false` = berkas Excel divisi belum ada (Status Berkas Jujur).
 * Warna wajib sama dengan dms_core.DIVISI.
 */
export const PILAR_TAMPILAN = [
  {
    key: 'she',
    nomor: '01',
    nama: 'SHE / SAFETY',
    deskripsi: 'Zero accident · SHE index · KAK (K3)',
    sheet: 'Resume SHE',
    kasus: 2,
    status: 'tersinkron',
    terdaftar: true,
  },
  {
    key: 'quality',
    nomor: '02',
    nama: 'QUALITY',
    deskripsi: 'Defect per line · critical point · hold / release',
    sheet: 'Resume QC',
    kasus: 7,
    status: 'tersinkron',
    terdaftar: true,
    // Kontras teks putih di atas #D7B32A tidak lolos WCAG → teks gelap (§9.3).
    teksGelap: true,
  },
  {
    key: 'produksi',
    nomor: '03',
    nama: 'PRODUKSI',
    deskripsi: 'Output vs target · OEE · downtime · checklist',
    sheet: 'Resume Prod',
    kasus: 19,
    status: 'tersinkron',
    terdaftar: true,
  },
  {
    key: 'delivery',
    nomor: '04',
    nama: 'DELIVERY',
    deskripsi: 'Plan vs real PO · on-time · kesiapan muat',
    sheet: 'Resume Delivery',
    kasus: 0,
    status: 'menunggu_berkas',
    terdaftar: false,
  },
  {
    key: 'teknik',
    nomor: '05',
    nama: 'TECHNIC',
    deskripsi: 'Sebab teknis downtime · PM · spare part · kalibrasi',
    sheet: 'Resume Teknik',
    kasus: 0,
    status: 'menunggu_berkas',
    terdaftar: false,
  },
]
