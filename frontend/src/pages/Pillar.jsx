import { Link, useParams, Navigate } from 'react-router-dom'
import { PILARS, getPilar, PILAR_KEYS } from '../constants'
import { KpiGrid } from '../components/KpiGrid'
import { KasusTable } from '../components/KasusTable'
import { PicaList } from '../components/PicaList'
import { EmptyState } from '../components/EmptyState'
import { PageStatusPill } from '../components/StatusPill'

/**
 * Halaman detail satu pilar — generik untuk SHE / Quality / Produksi / Delivery / Teknik.
 * Isi: hero pilar → grid KPI → tabel kasus (kolom mengikuti Excel) → PICA terbuka.
 */
export function Pillar({ state }) {
  const { key } = useParams()
  const pilar = getPilar(key)
  if (!pilar) return <Navigate to="/dashboard" replace />

  const h = (state.halaman || []).find((x) => x.key === key)
  const i = PILAR_KEYS.indexOf(key)
  const prev = PILARS[(i - 1 + PILARS.length) % PILARS.length]
  const next = PILARS[(i + 1) % PILARS.length]
  const ter = h?.status === 'tersinkron'
  const gelap = pilar.teksGelap

  return (
    <>
      {/* HERO PILAR */}
      <section className="pillar-hero" style={{ background: pilar.warna, color: gelap ? '#2b2b28' : '#fff' }}>
        <div>
          <small>{pilar.sheet} · Pilar {i + 1} dari 5</small>
          <h1>{pilar.nama}</h1>
          <p style={{ color: gelap ? 'rgba(43,43,40,.85)' : 'rgba(255,255,255,.92)' }}>{pilar.deskripsi}</p>
        </div>
        <div className="pillar-hero-side" style={{ color: gelap ? '#2b2b28' : '#fff' }}>
          <PageStatusPill status={h?.status || 'menunggu_berkas'} />
          <span>Sinkron terakhir: <b>{h?.sinkron_terakhir || '—'}</b></span>
          <span>Jumlah kasus tanggal ini: <b>{h?.jumlah ?? 0}</b></span>
          <span>{pilar.aturan}</span>
        </div>
      </section>

      {!ter ? (
        <EmptyState status={h?.status} pesan={h?.pesan} berkas={h?.berkas || []} />
      ) : (
        <div style={{ display: 'grid', gap: 16 }}>
          {/* KPI */}
          <KpiGrid kpi={h.kpi} warna={pilar.warna} gelap={gelap} />

          {/* Kasus + PICA */}
          <KasusTable
            kolom={h.kolom}
            baris={h.baris}
            judul={`KASUS · sheet ${h.berkas?.[0]?.sheet || pilar.sheet} · ${h.jumlah} baris pada tanggal ini`}
            sub="kolom mengikuti Excel (R-83) · angka tidak diubah dari aplikasi (R-89)"
          />
          <PicaList baris={h.baris} kolom={h.kolom} />
        </div>
      )}

      {/* Navigasi antar pilar */}
      <div className="pillar-nav">
        <Link className="btn btn-outline" to={`/pilar/${prev.key}`}>← {prev.short}</Link>
        <Link className="btn btn-outline" to="/dashboard">Semua Pilar</Link>
        <Link className="btn btn-outline" to={`/pilar/${next.key}`}>{next.short} →</Link>
      </div>
    </>
  )
}
