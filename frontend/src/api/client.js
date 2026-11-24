// API client DMS — mengikuti docs/API_CONTRACT.md (v1).
// Semua fungsi melempar Error bila HTTP tidak ok; biarkan hook menangani fallback.

const TIMEOUT_MS = 4000

async function request(path, options = {}) {
  const ctrl = new AbortController()
  const t = setTimeout(() => ctrl.abort(), TIMEOUT_MS)
  try {
    const res = await fetch(path, {
      headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
      signal: ctrl.signal,
      ...options,
    })
    const text = await res.text()
    let body = null
    try { body = text ? JSON.parse(text) : null } catch { body = null }
    if (!res.ok) {
      const pesan = body?.pesan || `HTTP ${res.status}`
      const err = new Error(pesan)
      err.status = res.status
      err.body = body
      throw err
    }
    return body
  } finally {
    clearTimeout(t)
  }
}

export const api = {
  /** State lengkap TV/dashboard. Query: plant, line, demo, tanggal. */
  getState({ plant = 'Snack', line = '*', demo = '1', tanggal } = {}) {
    const q = new URLSearchParams({ plant, line, demo })
    if (tanggal) q.set('tanggal', tanggal)
    return request(`/api/state?${q.toString()}`)
  },
  /** Ubah status absensi satu nama. 409 bila sudah dikonfirmasi. */
  postAbsensi({ nama, status, plant = 'Snack', line = '*', perangkat = 'web' }) {
    return request('/api/absensi', {
      method: 'POST',
      body: JSON.stringify({ nama, status, plant, line, perangkat }),
    })
  },
  /** Konfirmasi kehadiran (pelaku: web / QR sesi). */
  postKonfirmasi({ plant = 'Snack', line = '*', pelaku = 'web' } = {}) {
    return request('/api/konfirmasi', {
      method: 'POST',
      body: JSON.stringify({ plant, line, pelaku }),
    })
  },
  /** Buka ulang sesi (Supervisor/DH). */
  postBuka({ plant = 'Snack', line = '*', pelaku = 'supervisor', alasan = '' } = {}) {
    return request('/api/buka', {
      method: 'POST',
      body: JSON.stringify({ plant, line, pelaku, alasan: alasan || '(tanpa alasan)' }),
    })
  },
  /** Sinkron paksa semua / satu sumber. */
  postSync(sumberId) {
    return request('/api/sync', {
      method: 'POST',
      body: JSON.stringify(sumberId ? { sumber_id: sumberId } : {}),
    })
  },
  /** Data panel admin. */
  getAdmin() {
    return request('/api/admin')
  },
  health() {
    return request('/healthz')
  },
}
