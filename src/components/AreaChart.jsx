import { weeklyCases } from '../data/dummy'

const W = 600
const H = 230
const PAD = { top: 14, right: 10, bottom: 28, left: 34 }

// Catmull-Rom → cubic Bézier supaya garis halus
function smoothPath(points) {
  if (points.length < 2) return ''
  const r = (n) => n.toFixed(1)
  let d = `M ${r(points[0].x)},${r(points[0].y)}`
  for (let i = 0; i < points.length - 1; i += 1) {
    const p0 = points[Math.max(0, i - 1)]
    const p1 = points[i]
    const p2 = points[i + 1]
    const p3 = points[Math.min(points.length - 1, i + 2)]
    const c1x = p1.x + (p2.x - p0.x) / 6
    const c1y = p1.y + (p2.y - p0.y) / 6
    const c2x = p2.x - (p3.x - p1.x) / 6
    const c2y = p2.y - (p3.y - p1.y) / 6
    d += ` C ${r(c1x)},${r(c1y)} ${r(c2x)},${r(c2y)} ${r(p2.x)},${r(p2.y)}`
  }
  return d
}

export default function AreaChart() {
  const { labels, values, yMax, yTicks } = weeklyCases
  const innerW = W - PAD.left - PAD.right
  const innerH = H - PAD.top - PAD.bottom
  const xAt = (i) => PAD.left + (innerW * i) / (labels.length - 1)
  const yAt = (v) => PAD.top + innerH - (v / yMax) * innerH
  const points = values.map((v, i) => ({ x: xAt(i), y: yAt(v) }))
  const line = smoothPath(points)
  const area = `${line} L ${xAt(labels.length - 1).toFixed(1)},${(PAD.top + innerH).toFixed(1)} L ${PAD.left},${(PAD.top + innerH).toFixed(1)} Z`
  const baseline = PAD.top + innerH

  return (
    <svg className="chart" viewBox={`0 0 ${W} ${H}`} role="img"
      aria-label="Tren kasus 7 hari terakhir">
      <defs>
        <linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#7c5cf0" stopOpacity="0.32" />
          <stop offset="100%" stopColor="#7c5cf0" stopOpacity="0.02" />
        </linearGradient>
      </defs>

      {yTicks.map((t) => (
        <g key={t}>
          <line x1={PAD.left} x2={W - PAD.right} y1={yAt(t)} y2={yAt(t)}
            stroke="#e7e7ef" strokeDasharray="4 5" strokeWidth="1" />
          <text x={PAD.left - 8} y={yAt(t) + 4} textAnchor="end"
            className="chart-tick">{t}</text>
        </g>
      ))}

      <path d={area} fill="url(#areaFill)" />
      <path d={line} fill="none" stroke="#6d3df0" strokeWidth="2.5"
        strokeLinecap="round" strokeLinejoin="round" />

      {points.map((p, i) => (
        <circle key={labels[i]} cx={p.x} cy={p.y} r="3.4"
          fill="#fff" stroke="#6d3df0" strokeWidth="2" />
      ))}

      {labels.map((label, i) => (
        <text key={label} x={xAt(i)} y={baseline + 19} textAnchor="middle"
          className="chart-tick">{label}</text>
      ))}
    </svg>
  )
}
