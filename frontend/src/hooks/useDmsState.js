import { useEffect, useState, useCallback } from 'react'
import { api } from '../api/client'
import { buatDemoState } from '../data/demoState'

/**
 * Hook state DMS: polling /api/state tiap `intervalMs` (default 15 dtk).
 * Bila server tidak terjangkau → fallback ke data contoh + flag `online=false`
 * supaya halaman tetap render dan jelas bahwa ini data contoh.
 */
export function useDmsState({ plant = 'Snack', line = '*', demo = '1', tanggal, intervalMs = 15000 } = {}) {
  const [state, setState] = useState(null)
  const [online, setOnline] = useState(true)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const load = useCallback(async () => {
    try {
      const data = await api.getState({ plant, line, demo, tanggal })
      setState(data)
      setOnline(true)
      setError(null)
    } catch (err) {
      setState(buatDemoState(plant))
      setOnline(false)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }, [plant, line, demo, tanggal])

  useEffect(() => {
    setLoading(true)
    load()
    const t = setInterval(load, intervalMs)
    return () => clearInterval(t)
  }, [load, intervalMs])

  return { state, online, loading, error, reload: load }
}
