import { iconMap, IconArrowUpRight, IconArrowDownRight } from './icons'

export default function KpiCard({ label, value, delta, trend, tone, icon }) {
  const Icon = iconMap[icon]
  const TrendIcon = trend === 'down' ? IconArrowDownRight : IconArrowUpRight
  return (
    <article className={`kpi-card kpi-card--${tone}`}>
      <span className="kpi-deco" aria-hidden="true" />
      {Icon && (
        <span className="kpi-icon" aria-hidden="true">
          <Icon size={26} strokeWidth={1.6} />
        </span>
      )}
      <p className="kpi-label">{label}</p>
      <p className="kpi-value">{value}</p>
      <p className="kpi-delta">
        <TrendIcon size={14} strokeWidth={2.2} />
        <span>{delta}</span>
      </p>
    </article>
  )
}
