// Ikon SVG inline (gaya feather) — stroke currentColor, tanpa dependency.
const base = {
  fill: 'none',
  stroke: 'currentColor',
  strokeWidth: 1.8,
  strokeLinecap: 'round',
  strokeLinejoin: 'round',
  'aria-hidden': 'true',
}

const make = (children) =>
  function Icon({ size = 20, ...rest }) {
    return (
      <svg width={size} height={size} viewBox="0 0 24 24" {...base} {...rest}>
        {children}
      </svg>
    )
  }

export const IconGrid = make(<>
  <rect x="3" y="3" width="7" height="7" rx="1.5" />
  <rect x="14" y="3" width="7" height="7" rx="1.5" />
  <rect x="3" y="14" width="7" height="7" rx="1.5" />
  <rect x="14" y="14" width="7" height="7" rx="1.5" />
</>)

export const IconCompare = make(<>
  <path d="M8 3 4 7l4 4" />
  <path d="M4 7h16" />
  <path d="m16 21 4-4-4-4" />
  <path d="M20 17H4" />
</>)

export const IconAlert = make(<>
  <circle cx="12" cy="12" r="9" />
  <line x1="12" y1="8" x2="12" y2="12" />
  <line x1="12" y1="16" x2="12.01" y2="16" />
</>)

export const IconTrending = make(<>
  <polyline points="23 6 13.5 15.5 8.5 10.5 1 18" />
  <polyline points="17 6 23 6 23 12" />
</>)

export const IconFileText = make(<>
  <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
  <polyline points="14 2 14 8 20 8" />
  <line x1="16" y1="13" x2="8" y2="13" />
  <line x1="16" y1="17" x2="8" y2="17" />
</>)

export const IconMonitor = make(<>
  <rect x="2" y="3" width="20" height="14" rx="2" />
  <line x1="8" y1="21" x2="16" y2="21" />
  <line x1="12" y1="17" x2="12" y2="21" />
</>)

export const IconEdit = make(<>
  <path d="M17 3a2.83 2.83 0 1 1 4 4L8 20l-5 1 1-5L17 3z" />
</>)

export const IconUsers = make(<>
  <path d="M17 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
  <circle cx="9.5" cy="7" r="4" />
  <path d="M23 21v-2a4 4 0 0 0-3-3.87" />
  <path d="M16 3.13a4 4 0 0 1 0 7.75" />
</>)

export const IconSync = make(<>
  <polyline points="23 4 23 10 17 10" />
  <polyline points="1 20 1 14 7 14" />
  <path d="M3.5 9a9 9 0 0 1 14.9-3.4L23 10M1 14l4.6 4.4A9 9 0 0 0 20.5 15" />
</>)

export const IconSliders = make(<>
  <line x1="4" y1="21" x2="4" y2="14" />
  <line x1="4" y1="10" x2="4" y2="3" />
  <line x1="12" y1="21" x2="12" y2="12" />
  <line x1="12" y1="8" x2="12" y2="3" />
  <line x1="20" y1="21" x2="20" y2="16" />
  <line x1="20" y1="12" x2="20" y2="3" />
  <line x1="1" y1="14" x2="7" y2="14" />
  <line x1="9" y1="8" x2="15" y2="8" />
  <line x1="17" y1="16" x2="23" y2="16" />
</>)

export const IconShield = make(<>
  <path d="M12 22s8-3.6 8-10V5l-8-3-8 3v7c0 6.4 8 10 8 10z" />
  <polyline points="9.2 11.6 11.4 13.8 15 10" />
</>)

export const IconUserCheck = make(<>
  <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
  <circle cx="9" cy="7" r="4" />
  <polyline points="16 11 18 13 22 9" />
</>)

export const IconSearch = make(<>
  <circle cx="11" cy="11" r="7" />
  <line x1="21" y1="21" x2="16.3" y2="16.3" />
</>)

export const IconBell = make(<>
  <path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9" />
  <path d="M13.73 21a2 2 0 0 1-3.46 0" />
</>)

export const IconExpand = make(<>
  <polyline points="15 3 21 3 21 9" />
  <polyline points="9 21 3 21 3 15" />
  <line x1="21" y1="3" x2="14" y2="10" />
  <line x1="3" y1="21" x2="10" y2="14" />
</>)

export const IconRefresh = make(<>
  <polyline points="23 4 23 10 17 10" />
  <polyline points="1 20 1 14 7 14" />
  <path d="M3.5 9a9 9 0 0 1 14.9-3.4L23 10M1 14l4.6 4.4A9 9 0 0 0 20.5 15" />
</>)

export const IconChevronDown = make(<polyline points="6 9 12 15 18 9" />)
export const IconChevronRight = make(<polyline points="9 6 15 12 9 18" />)

export const IconArrowUpRight = make(<>
  <line x1="7" y1="17" x2="17" y2="7" />
  <polyline points="7 7 17 7 17 17" />
</>)

export const IconArrowDownRight = make(<>
  <line x1="7" y1="7" x2="17" y2="17" />
  <polyline points="17 7 17 17 7 17" />
</>)

export const IconArrowOut = make(<>
  <line x1="7" y1="17" x2="17" y2="7" />
  <polyline points="7 7 17 7 17 17" />
</>)

export const IconClipboard = make(<>
  <path d="M9 2h6a1 1 0 0 1 1 1v1a1 1 0 0 1-1 1H9a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1z" />
  <path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2" />
  <line x1="9" y1="12" x2="15" y2="12" />
  <line x1="9" y1="16" x2="13" y2="16" />
</>)

export const IconCheckCircle = make(<>
  <circle cx="12" cy="12" r="9" />
  <polyline points="8.5 12.2 11.2 14.9 15.5 10" />
</>)

export const IconPieChart = make(<>
  <path d="M21.21 15.89A10 10 0 1 1 8 2.83" />
  <path d="M22 2 12 12" />
  <path d="M16 2h6v6" />
</>)

export const IconClock = make(<>
  <circle cx="12" cy="12" r="9" />
  <polyline points="12 7 12 12 15.5 14" />
</>)

export const IconActivity = make(<polyline points="22 12 16 12 13 21 11 3 8 12 2 12" />)

export const IconGlobe = make(<>
  <circle cx="12" cy="12" r="9" />
  <line x1="3" y1="12" x2="21" y2="12" />
  <path d="M12 3a14.5 14.5 0 0 1 0 18M12 3a14.5 14.5 0 0 0 0 18" />
</>)

export const IconMenu = make(<>
  <line x1="4" y1="7" x2="20" y2="7" />
  <line x1="4" y1="12" x2="20" y2="12" />
  <line x1="4" y1="17" x2="20" y2="17" />
</>)

export const IconShieldCheck = IconShield
export const IconClose = make(<>
  <line x1="18" y1="6" x2="6" y2="18" />
  <line x1="6" y1="6" x2="18" y2="18" />
</>)

// Peta nama → komponen, dipakai oleh Sidebar/kartu (data-driven).
export const iconMap = {
  grid: IconGrid,
  compare: IconCompare,
  alert: IconAlert,
  trending: IconTrending,
  fileText: IconFileText,
  monitor: IconMonitor,
  edit: IconEdit,
  users: IconUsers,
  sync: IconSync,
  sliders: IconSliders,
  shield: IconShield,
  userCheck: IconUserCheck,
  clipboard: IconClipboard,
  checkCircle: IconCheckCircle,
  pieChart: IconPieChart,
  clock: IconClock,
}
