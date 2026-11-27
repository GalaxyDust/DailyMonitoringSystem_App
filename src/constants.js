/**
 * Konstanta bersama — FRONTEND_STRUCTURE.md §4.2.
 *
 * Semua warna diambil dari token brief §9.1. Tidak boleh di-hardcode
 * di komponen lain (§9.3 butir 10).
 */

/** Palet brief §9.1 — dipakai halaman yang butuh nilai warna langsung. */
export const WARNA = {
  navy: '#1B2C57',
  navy2: '#16224A',
  teal: '#2E868C',
  teal2: '#22666C',
  gold: '#C8A52B',
  gold2: '#8A6C10',
  bg: '#F4F6FA',
  card: '#FFFFFF',
  rule: '#DDE2EA',
  text: '#1E2430',
  grey: '#5C6472',
  blue: '#1C3E8A',
  red: '#C22A26',
  grey3: '#A9A9A2',
  green: '#1E6B3A',
}

/**
 * Lima pilar, urut seperti backend (SHE → Teknik).
 * Warna WAJIB sama dengan `dms_core.DIVISI`.
 */
export const PILARS = [
  { key: 'she', nama: 'SHE / SAFETY', short: 'SHE', nomor: '01', warna: '#B02F2F', teksGelap: false },
  { key: 'quality', nama: 'QUALITY', short: 'QUALITY', nomor: '02', warna: '#D7B32A', teksGelap: true },
  { key: 'produksi', nama: 'PRODUKSI', short: 'PRODUKSI', nomor: '03', warna: '#A62E2E', teksGelap: false },
  { key: 'delivery', nama: 'DELIVERY', short: 'DELIVERY', nomor: '04', warna: '#2E7D46', teksGelap: false },
  { key: 'teknik', nama: 'TECHNIC', short: 'TEKNIK', nomor: '05', warna: '#2A5CA0', teksGelap: false },
]

export const PILAR_KEYS = PILARS.map((p) => p.key)

/**
 * Empat status halaman divisi.
 * "belum diisi" ≠ "belum tersinkron" (Status Berkas Jujur).
 */
export const STATUS_HALAMAN = {
  tersinkron: { label: 'tersinkron', kelas: 'ok' },
  belum_diisi: { label: 'belum diisi', kelas: 'warn' },
  belum_tersinkron: { label: 'belum tersinkron', kelas: 'bad' },
  menunggu_berkas: { label: 'menunggu berkas', kelas: 'warn' },
}

/** Status kasus di tabel divisi. */
export const STATUS_KASUS = {
  OPEN: { label: 'OPEN', kelas: 'open' },
  PROGRESS: { label: 'PROGRESS', kelas: 'progress' },
  CLOSE: { label: 'CLOSE', kelas: 'close' },
}

/** Role interim v1 (A-02). */
export const ROLES = { TV: 'tv', PDCA: 'pdca', TL: 'tl' }

/** Hanya dua role ini yang boleh melihat /dashboard (A-02). */
export const ROLE_DASHBOARD = [ROLES.PDCA, ROLES.TL]

export const ROLE_LABEL = { tv: 'TV Device', pdca: 'PDCA', tl: 'TL' }
