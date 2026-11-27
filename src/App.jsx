import { useState } from 'react'
import Sidebar from './components/Sidebar'
import Topbar from './components/Topbar'
import KpiCard from './components/KpiCard'
import QuickLink from './components/QuickLink'
import AreaChart from './components/AreaChart'
import BarChart from './components/BarChart'
import { IconActivity, IconGlobe, IconArrowOut } from './components/icons'
import { kpiCards, quickLinks } from './data/dummy'

export default function App() {
  const [active, setActive] = useState('ringkasan')
  const [collapsed, setCollapsed] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)

  const handleMenu = () => {
    if (window.innerWidth <= 1024) setMobileOpen((v) => !v)
    else setCollapsed((v) => !v)
  }

  const closeMobile = () => setMobileOpen(false)

  return (
    <div className="app">
      {mobileOpen && <button className="scrim" aria-label="Tutup menu" onClick={closeMobile} />}
      <Sidebar
        collapsed={collapsed}
        open={mobileOpen}
        onClose={closeMobile}
        active={active}
        onSelect={(id) => { setActive(id); setMobileOpen(false) }}
      />

      <div className="main">
        <Topbar onMenu={handleMenu} />

        <main className="content">
          {/* Kartu KPI */}
          <section className="kpi-grid" aria-label="Ringkasan kinerja">
            {kpiCards.map((card) => (
              <KpiCard key={card.id} {...card} />
            ))}
          </section>

          {/* Pintasan modul */}
          <section className="quick-grid" aria-label="Pintasan modul">
            {quickLinks.map((link) => (
              <QuickLink key={link.id} {...link} onClick={() => setActive(link.id)} />
            ))}
          </section>

          {/* Grafik */}
          <section className="chart-grid" aria-label="Grafik">
            <div className="panel panel--wide">
              <div className="panel-head">
                <h2 className="panel-title">
                  <span className="panel-icon panel-icon--purple"><IconActivity size={17} /></span>
                  Kasus &amp; Penutupan
                </h2>
                <button className="panel-link panel-link--purple" type="button">
                  Lihat detail <IconArrowOut size={13} strokeWidth={2} />
                </button>
              </div>
              <AreaChart />
            </div>

            <div className="panel">
              <div className="panel-head">
                <h2 className="panel-title">
                  <span className="panel-icon panel-icon--pink"><IconGlobe size={17} /></span>
                  Kasus per Divisi
                </h2>
                <button className="panel-link panel-link--pink" type="button">
                  Detail <IconArrowOut size={13} strokeWidth={2} />
                </button>
              </div>
              <BarChart />
            </div>
          </section>
        </main>
      </div>
    </div>
  )
}
