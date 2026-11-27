import { useEffect, useState } from 'react'
import { ROLE_DASHBOARD, ROLES } from '../constants'

const KUNCI = 'dms.role'

/**
 * Role interim v1 (A-02) — tanpa login, dibaca dari `?role=` → localStorage → `tv`.
 *
 * Dipakai untuk dua hal:
 * 1. Menentukan apakah tautan Dashboard boleh tampil (hanya pdca/tl).
 * 2. Penjaga rute /dashboard.
 *
 * Ini HANYA lapisan tampilan; proteksi sebenarnya menyusul saat auth
 * Entra ID dipasang (BACKEND_PLAN Tahap C).
 */
export function useRole() {
  const [role, setRole] = useState(() => {
    try {
      const dariQuery = new URLSearchParams(window.location.search).get('role')
      if (dariQuery && Object.values(ROLES).includes(dariQuery)) return dariQuery
      const tersimpan = localStorage.getItem(KUNCI)
      if (tersimpan && Object.values(ROLES).includes(tersimpan)) return tersimpan
    } catch {
      // localStorage bisa diblokir di kiosk — pakai default, jangan gagalkan render
    }
    return ROLES.TV
  })

  // Simpan pilihan agar tetap konsisten antar navigasi.
  useEffect(() => {
    try {
      localStorage.setItem(KUNCI, role)
    } catch {
      // diabaikan dengan sengaja
    }
  }, [role])

  return {
    role,
    setRole,
    /** A-02: hanya pdca/tl yang boleh melihat /dashboard. */
    bolehDashboard: ROLE_DASHBOARD.includes(role),
  }
}

export default useRole
