import { divisionCases } from '../data/dummy'

const W = 420
const H = 230
const PAD = { top: 18, right: 8, bottom: 28, left: 34 }

export default function BarChart() {
  const { labels, values, yMax, yTicks } = divisionCases
  const innerW = W - PAD.left - PAD.right
  const innerH = H - PAD.top - PAD.bottom
  const baseline = PAD.top + innerH
  const slot = innerW / labels.length
  const barW = Math.min(30, slot * 0.52)
  const yAt = (v) => baseline - (v / yMax) * innerH

  return (
    <svg className="chart" viewBox={`0 0 ${W} ${H}`} role="img"
      aria-label="Jumlah kasus per divisi minggu berjalan">
      <defs>
        <linearGradient id="barFill" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#a78bfa" />
          <stop offset="100%" stopColor="#6d3df0" />
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

      {labels.map((label, i) => {
        const x = PAD.left + slot * i + (slot - barW) / 2
        const y = yAt(values[i])
        const h = baseline - y
        return (
          <g key={label}>
            <rect x={x} y={y} width={barW} height={h} rx="5" fill="url(#barFill)">
              <title>{`${label}: ${values[i]} kasus`}</title>
            </rect>
            <text x={x + barW / 2} y={y - 6} textAnchor="middle"
              className="chart-value">{values[i]}</text>
            <text x={x + barW / 2} y={baseline + 19} textAnchor="middle"
              className="chart-tick">{label}</text>
          </g>
        )
      })}
    </svg>
  )
}
