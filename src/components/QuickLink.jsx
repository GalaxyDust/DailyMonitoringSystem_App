import { iconMap } from './icons'

export default function QuickLink({ title, caption, icon, tint, onClick }) {
  const Icon = iconMap[icon]
  return (
    <button type="button" className="quick-link" onClick={onClick} title={title}>
      {Icon && <Icon size={22} className={`quick-link-icon quick-link-icon--${tint}`} />}
      <span className="quick-link-title">{title}</span>
      <span className="quick-link-caption">{caption}</span>
    </button>
  )
}
