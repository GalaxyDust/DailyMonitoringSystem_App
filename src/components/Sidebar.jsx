import { navSections, user } from '../data/dummy'
import { iconMap, IconChevronDown, IconClose } from './icons'

export default function Sidebar({ collapsed, open, onClose, active, onSelect }) {
  return (
    <aside className={`sidebar${collapsed ? ' is-collapsed' : ''}${open ? ' is-open' : ''}`} aria-label="Navigasi utama">
      {/* Brand */}
      <div className="sidebar-brand">
        <span className="brand-mark" aria-hidden="true">
          <svg viewBox="0 0 40 40" width="36" height="36">
            <path d="M20 3 36 33H27.5L20 17.5 12.5 33H4L20 3Z" fill="url(#dmsGrad)" />
            <circle cx="20" cy="28.4" r="3.1" fill="#fff" opacity="0.92" />
            <defs>
              <linearGradient id="dmsGrad" x1="6" y1="4" x2="34" y2="33" gradientUnits="userSpaceOnUse">
                <stop stopColor="#ffb03a" />
                <stop offset="0.55" stopColor="#ff7a1a" />
                <stop offset="1" stopColor="#f04e23" />
              </linearGradient>
            </defs>
          </svg>
        </span>
        <span className="brand-text">
          <strong>DMS&nbsp;Admin</strong>
          <small>DAILY MONITORING SYSTEM</small>
        </span>
        <button className="icon-btn sidebar-close" onClick={onClose} aria-label="Tutup menu">
          <IconClose size={18} />
        </button>
      </div>

      {/* Navigasi */}
      <nav className="sidebar-nav">
        {navSections.map((section) => (
          <div className="nav-section" key={section.label}>
            <p className="nav-section-label">{section.label}</p>
            <ul>
              {section.items.map((item) => {
                const Icon = iconMap[item.icon]
                const isActive = active === item.id
                return (
                  <li key={item.id}>
                    <button
                      type="button"
                      className={`nav-item${isActive ? ' is-active' : ''}`}
                      onClick={() => onSelect(item.id)}
                      title={collapsed ? item.label : undefined}
                      aria-current={isActive ? 'page' : undefined}
                    >
                      {item.icon === 'dot' ? (
                        <span className={`plant-dot plant-dot--${item.dot}`} aria-hidden="true" />
                      ) : (
                        Icon && <Icon size={18} className="nav-item-icon" />
                      )}
                      <span className="nav-item-label">{item.label}</span>
                      {item.badge && <span className="nav-badge">{item.badge}</span>}
                      {item.hint && <span className="nav-hint">{item.hint}</span>}
                      {item.chevron && (
                        <IconChevronDown size={15} className="nav-chevron" />
                      )}
                    </button>
                  </li>
                )
              })}
            </ul>
          </div>
        ))}
      </nav>

      {/* Kaki sidebar */}
      <div className="sidebar-foot">
        <span className="foot-dot" aria-hidden="true" />
        <div className="foot-text">
          <strong>{user.plant}</strong>
          <small>{user.tanggal} · Shift 1</small>
        </div>
      </div>
    </aside>
  )
}
