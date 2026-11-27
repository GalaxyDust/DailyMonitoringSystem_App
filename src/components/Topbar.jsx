import { useEffect, useRef, useState } from 'react'
import { user, notifications } from '../data/dummy'
import {
  IconMenu, IconSearch, IconExpand, IconRefresh, IconBell,
  IconChevronDown, IconShield, IconAlert, IconSync, IconFileText,
} from './icons'

const notifIcon = { danger: IconAlert, warn: IconSync, info: IconFileText }

export default function Topbar({ onMenu }) {
  const searchRef = useRef(null)
  const [refreshing, setRefreshing] = useState(false)
  const [showNotifs, setShowNotifs] = useState(false)
  const notifRef = useRef(null)

  // Ctrl/Cmd + K fokus ke pencarian
  useEffect(() => {
    const onKey = (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault()
        searchRef.current?.focus()
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  // Tutup panel notifikasi saat klik di luar
  useEffect(() => {
    if (!showNotifs) return
    const onClick = (e) => {
      if (notifRef.current && !notifRef.current.contains(e.target)) setShowNotifs(false)
    }
    window.addEventListener('mousedown', onClick)
    return () => window.removeEventListener('mousedown', onClick)
  }, [showNotifs])

  const toggleFullscreen = () => {
    if (document.fullscreenElement) document.exitFullscreen()
    else document.documentElement.requestFullscreen?.().catch(() => {})
  }

  const refresh = () => {
    setRefreshing(true)
    window.setTimeout(() => setRefreshing(false), 900)
  }

  return (
    <header className="topbar">
      <button className="icon-btn" onClick={onMenu} aria-label="Buka/tutup menu" title="Buka/tutup menu">
        <IconMenu size={21} />
      </button>

      <label className="search">
        <IconSearch size={18} className="search-icon" />
        <input
          ref={searchRef}
          type="text"
          placeholder="Cari dasbor, kasus, line, PIC…"
          aria-label="Pencarian"
        />
        <kbd>Ctrl K</kbd>
      </label>

      <div className="topbar-actions">
        <button className="icon-btn" onClick={toggleFullscreen} aria-label="Layar penuh" title="Layar penuh">
          <IconExpand size={19} />
        </button>
        <button
          className={`icon-btn${refreshing ? ' is-spinning' : ''}`}
          onClick={refresh}
          aria-label="Segarkan data"
          title="Segarkan data"
        >
          <IconRefresh size={19} />
        </button>

        <div className="notif-wrap" ref={notifRef}>
          <button
            className="icon-btn has-dot"
            onClick={() => setShowNotifs((v) => !v)}
            aria-label="Notifikasi"
            aria-expanded={showNotifs}
            title="Notifikasi"
          >
            <IconBell size={19} />
          </button>
          {showNotifs && (
            <div className="notif-panel" role="dialog" aria-label="Notifikasi">
              <div className="notif-head">
                <strong>Notifikasi</strong>
                <span>{notifications.length} baru</span>
              </div>
              {notifications.map((n) => {
                const Icon = notifIcon[n.tone] ?? IconAlert
                return (
                  <div className="notif-item" key={n.id}>
                    <span className={`notif-icon notif-icon--${n.tone}`}><Icon size={16} /></span>
                    <span className="notif-text">
                      <strong>{n.title}</strong>
                      <small>{n.caption}</small>
                    </span>
                  </div>
                )
              })}
            </div>
          )}
        </div>

        <button className="user-chip" title="Akun saya">
          <span className="avatar" aria-hidden="true">{user.initials}</span>
          <span className="user-meta">
            <strong>{user.name}</strong>
            <small><IconShield size={12} /> {user.role}</small>
          </span>
          <IconChevronDown size={16} className="user-chevron" />
        </button>
      </div>
    </header>
  )
}
