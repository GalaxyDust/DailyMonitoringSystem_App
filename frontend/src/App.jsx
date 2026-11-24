import { HashRouter, Routes, Route, Navigate, useLocation } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { Layout } from './components/Layout'
import { useDmsState } from './hooks/useDmsState'
import { Main } from './pages/Main'
import { Dashboard } from './pages/Dashboard'
import { Pillar } from './pages/Pillar'
import { Absensi } from './pages/Absensi'
import { NotFound } from './pages/NotFound'

function ScrollToTop() {
  const { pathname } = useLocation()
  useEffect(() => { window.scrollTo(0, 0) }, [pathname])
  return null
}

export default function App() {
  const [plant, setPlant] = useState(() => localStorage.getItem('dms.plant') || 'Snack')
  const { state, online, reload } = useDmsState({ plant, line: '*', demo: '1', intervalMs: 15000 })

  const onPlantChange = (p) => {
    setPlant(p)
    localStorage.setItem('dms.plant', p)
  }

  return (
    <HashRouter>
      <ScrollToTop />
      <Layout plant={plant} onPlantChange={onPlantChange} online={online}>
        {!state ? (
          <div className="loading">Menghubungkan ke basis data DMS…</div>
        ) : (
          <Routes>
            <Route path="/" element={<Main />} />
            <Route path="/dashboard" element={<Dashboard state={state} />} />
            <Route path="/pilar" element={<Navigate to="/dashboard" replace />} />
            <Route path="/pilar/:key" element={<Pillar state={state} />} />
            <Route path="/absensi" element={<Absensi state={state} online={online} reload={reload} />} />
            <Route path="*" element={<NotFound />} />
          </Routes>
        )}
      </Layout>
    </HashRouter>
  )
}
