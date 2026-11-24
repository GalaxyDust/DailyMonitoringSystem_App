# DMS — Struktur Frontend (Spesifikasi)

> **Dokumen struktur & penempatan frontend DMS** — panduan untuk developer frontend (branch `front-end`).
> Berisi: posisi repo, tech stack, **pohon folder lengkap**, fungsi setiap file, routing, pohon komponen,
> bentuk data dari API, aturan gaya, aset, cara build/deploy, dan checklist pengerjaan.
>
> **Ini bukan berisi kode implementasi** — kode ditulis oleh developer frontend mengikuti struktur ini.
> Kontrak data: **`docs/API_CONTRACT.md` (v1)**. Alur pengguna: **`docs/ALUR_APLIKASI_DMS.md` §15**.
>
> Versi: **v1.2** · 24 November 2026 — v1.1 tambah **§5.1 Role & akses** (A-01 landing untuk semua TV · A-02 dashboard hanya PDCA/TL); v1.2 **plant Dairy** (4 plant) + rujukan Aturan Sistem v1.1 (nama manusiawi, tanpa kode R-xx)

---

## Daftar Isi

1. [Tujuan & prinsip](#1-tujuan--prinsip)
2. [Tech stack & posisi di repo](#2-tech-stack--posisi-di-repo)
3. [Pohon folder lengkap](#3-pohon-folder-lengkap)
4. [Fungsi setiap file](#4-fungsi-setiap-file)
5. [Routing & halaman](#5-routing--halaman) — termasuk **§5.1 Role & akses (A-01/A-02)**
6. [Pohon komponen per halaman](#6-pohon-komponen-per-halaman)
7. [Data & API — pemetaan per halaman](#7-data--api--pemetaan-per-halaman)
8. [State management & polling](#8-state-management--polling)
9. [Styling & design tokens](#9-styling--design-tokens)
10. [Aset & logo](#10-aset--logo)
11. [Build, dev & deployment](#11-build-dev--deployment)
12. [Naming convention & aturan folder](#12-naming-convention--aturan-folder)
13. [Yang TIDAK boleh / tidak perlu dibuat](#13-yang-tidak-boleh--tidak-perlu-dibuat)
14. [Checklist pengerjaan (M1 → M3)](#14-checklist-pengerjaan-m1--m3)

---

## 1. Tujuan & prinsip

Frontend DMS menampilkan **satu kebenaran yang sama** dengan TV dan panel admin: angka dari log kasus
Excel, lewat API Flask. Aplikasi ini **bukan** tempat mengisi data — semua isian lewat Excel petugas.

Prinsip yang mengikat UI (aturan sistem (lihat `docs/laporan/DMS_Aturan_Sistem_v1.md` v1.1 — nama manusiawi, tanpa kode R-xx)):

| Aturan | Implikasi ke desain frontend |
|---|---|
| **Satu papan, satu catatan** satu papan satu catatan | Semua halaman membaca `GET /api/state` — tidak ada fetch ke endpoint lain yang tumpang tindih |
| **Satu Divisi per Layar** satu divisi per layar | Satu halaman pilar = satu divisi penuh (bukan 5 kolom kecil) |
| **Absensi Dulu** absensi lebih dulu | Absensi adalah gerbang; UI harus menampilkan status sesi & mengunci rotasi |
| **QR Satu Pintu** QR satu pintu | Landing `/s/<token>` (ponsel) satu alur: absensi → review |
| **Kolom Statis, Isi Dinamis** kolom statis, isi dinamis | Kolom tabel **statis** mengikuti kontrak Excel; baris dinamis per tanggal — jangan bikin kolom dinamis dari API |
| **Nol Langkah Tambahan** nol langkah tambahan | Tidak ada tombol upload/ekspor di mana pun |
| **Kepemilikan Kolom** kepemilikan kolom | Tidak ada form edit sel kasus; koreksi dilakukan di Excel |
| **Status Berkas Jujur** (v1.1) | 4 status yang bisa dibedakan sistem (`tersinkron` / `belum_diisi` / `belum_tersinkron` / `menunggu_berkas`) + **jam acuan selalu tampil** + angka basi **bercap waktu** ("data terakhir hh.mm") — rincian di `DMS_Aturan_Sistem_v1.md` §10 |

**Aturan akses (v1.1, 24 Nov 2026 — keputusan produk):**

| Aturan | Implikasi ke desain frontend |
|---|---|
| **A-01 · Landing untuk semua TV** | Halaman `/` (menu 5 pilar + QR absensi sesi berjalan) adalah **permukaan TV**: tanpa login, dibuka fullscreen di setiap perangkat TV Device. TV tidak menampilkan link apa pun ke `/dashboard` |
| **A-02 · Dashboard hanya untuk PDCA & TL terkait** | `/dashboard` **hanya** untuk role **PDCA** (lihat semua plant: Snack · EP · NP · Dairy) dan **TL / Team Leader** (**hanya plant miliknya**). Role lain — termasuk perangkat TV — tidak melihat dan tidak bisa membuka `/dashboard` (rute terproteksi, bukan sekadar menu disembunyikan) |

Kedua aturan ini diusulkan menjadi **Landing untuk Semua TV (A-01)/Dashboard PDCA & TL (A-02)** pada `DMS_Aturan_Sistem` v1.1; selama dokumen itu belum direvisi, referensikan sebagai **A-01/A-02** seperti di atas.

---

## 2. Tech stack & posisi di repo

| Aspek | Pilihan | Catatan |
|---|---|---|
| Framework | **React 19** | Sesuai scaffold di branch `front-end` |
| Build tool | **Vite 8** + `@vitejs/plugin-react` | HMR, proxy dev ke Flask |
| Routing | **react-router-dom** | `HashRouter` (aman untuk static hosting tanpa fallback server) atau `BrowserRouter` bila Nginx rewrite |
| Bahasa | **JavaScript (JSX)** | TypeScript opsional di versi berikutnya (bukan wajib) |
| Komponen UI | **Tidak ada library** | CSS murni + design tokens (sesuai §9); hindari MUI/Ant agar bundle kecil |
| State | React hooks + context tipis | Tidak perlu Redux/Zustand untuk skala ini |
| Lint | ESLint flat config (js/recommended + react-hooks + react-refresh) | Sudah ada di scaffold |
| Test | Vitest (opsional) | Minimal: smoke test render beranda |

**Posisi di repo:** implementasi berada di **root branch `front-end`** (bukan di dalam folder `frontend/`) — itu scaffold milik tim frontend (`index.html`, `src/`, `package.json`, … di root).

> **Kerangka kosong tersedia:** folder **`frontend/`** di branch backend (`arena/ca138dd1-…`) berisi struktur yang sama (per folder, dengan `README.md` penjelas + berkas placeholder berisi komentar TODO — **tanpa kode**). Gunakan sebagai peta penempatan saat mengisi branch `front-end`; isinya tidak untuk di-merge ke `main`.

Struktur repo (konteks):

```
root (branch front-end)/
├── app/            ← BACKEND (read-only untuk frontend; jangan ubah)
├── docs/           ← dokumen ini tinggal di sini
├── Logo/           ← sumber logo (salin yang perlu ke public/)
├── docs/reference/      ← workbook acuan (read-only)
└── <isi frontend>  ← scaffold React yang sudah ada
```

---

## 3. Pohon folder lengkap

```
front-end/                          (root branch)
├── index.html                      shell HTML; mount #root; <title> DMS · Garudafood
├── package.json                    scripts: dev · build · preview · lint
├── package-lock.json               terkunci — jangan edit manual
├── vite.config.js                  plugin react · proxy dev · allowedHosts
├── eslint.config.js                flat config ESLint
├── .gitignore
├── README.md                       cara jalan (npm install · dev · build)
├── public/                         ← aset statis (disalin 1:1 ke dist/)
│   ├── logo.png                    logo utama (512px, dari Logo/Logo.png)
│   ├── logo-192.png                apple-touch-icon
│   └── favicon-32x32.png           favicon tab
└── src/
    ├── main.jsx                    entry: <StrictMode><App/></StrictMode>
    ├── App.jsx                     router + layout + plant context
    ├── index.css                   design tokens + semua kelas (§9)
    ├── constants.js                PILARS · PLANTS · enum status/KPI/siklus (§4.2)
    ├── api/
    │   └── client.js               fetch wrapper + semua fungsi endpoint (§4.3)
    ├── hooks/
    │   ├── useDmsState.js          polling /api/state (15 dtk) + fallback data contoh (§8)
    │   └── useNow.js               (opsional) jam berjalan untuk header
    ├── context/
    │   └── DmsContext.jsx          plant aktif + state global + online/offline (§8)
    ├── data/
    │   └── demoState.js            data contoh bentuk kontrak API (dipakai bila API mati)
    ├── components/                 ← komponen reusable (dipakai lintas halaman)
    │   ├── RequireRole.jsx          gerbang rute terproteksi — `/dashboard` hanya pdca/tl (A-02)
    │   ├── Layout.jsx              topbar + plant switch + konten + footer
    │   ├── KpiGrid.jsx             grid KPI Target·S1·S2·S3·Harian·Minggu·Bulan
    │   ├── KasusTable.jsx          tabel kasus (kolom statis dari API)
    │   ├── PicaList.jsx            kartu PICA terbuka (≤4)
    │   ├── StatusPill.jsx          pill status kasus & status halaman
    │   ├── EmptyState.jsx          keadaan kosong jujur (Kolom Statis, Isi Dinamis/Status Berkas Jujur)
    │   └── Toast.jsx               notifikasi aksi (konfirmasi, error 409)
    └── pages/                      ← satu file per route
        ├── Main.jsx                / — beranda/portal
        ├── Dashboard.jsx           /dashboard — ringkasan 5 pilar
        ├── Pillar.jsx              /pilar/:key — 5 pilar (generik, satu komponen)
        ├── Absensi.jsx             /absensi — gerbang Absensi Dulu
        └── NotFound.jsx            * — 404
```

**Aturan penempatan:**

- `components/` = reusable, tidak tahu route. `pages/` = tahu route, meracik komponen.
- Satu komponen pilar **untuk lima divisi** — jangan buat `ShePage.jsx`, `QualityPage.jsx`, … (duplikasi).
- Aset sumber (logo besar, font) **tidak** di-`src/assets/`; simpan di `public/` supaya tidak di-hash & mudah dirujuk.
- File di luar pohon di atas hanya bila benar-benar perlu (mis. `src/styles/fonts.css` bila font di-bundle).

---

## 4. Fungsi setiap file

### 4.1 Akar & entry

| File | Fungsi | Isi kunci |
|---|---|---|
| `index.html` | Shell; `<div id="root">`; `<title>`, meta deskripsi, favicon | Bahasa `id`; title "DMS · Garudafood Daily Monitoring System" |
| `src/main.jsx` | Bootstrap React | `createRoot(...render(<StrictMode><App/></StrictMode>))` |
| `src/App.jsx` | Router + plant context provider | `HashRouter`; route `/`, `/dashboard` (**dibungkus `<RequireRole>`**), `/pilar/:key`, `/absensi`, `*`; render `<Layout>` |
| `src/index.css` | Design tokens + kelas | Variabel CSS (navy/teal/gold), layout shell, topbar, cards, tabel, pill, absensi chip, breakpoints |
| `vite.config.js` | Build + dev proxy | `plugins:[react()]`; `server.proxy: {'/api':'http://localhost:8000', '/qr':…, '/s':…}`; `allowedHosts: true`; `host: true` |

### 4.2 `src/constants.js`

| Konstanta | Isi |
|---|---|
| `PILARS` | Array 5 pilar **urut backend**: `she` (merah `#B02F2F`) · `quality` (kuning `#D7B32A`, teks gelap) · `produksi` (`#A62E2E`) · `delivery` (`#2E7D46`) · `teknik` (`#2A5CA0`) — masing-masing: `key, nama, short, warna, teksGelap, deskripsi, sheet, aturan` |
| `PLANTS` | `Snack` · `EP` · `NP` · `Dairy` (+label panjang) · kode DR · rollout ke-4 (tanpa data — halaman tampil *menunggu berkas*) |
| `SIKLUS_ABSENSI` | `hadir → sakit → izin → alpa → terlambat → belum pasti` |
| `STATUS_KASUS` | Map `OPEN/PROGRESS/CLOSE` → warna + label |
| `STATUS_HALAMAN` | Map 4 status Status Berkas Jujur → label + warna |
| `ST_WARNA` / `ST_JUDUL` | Warna sel KPI `st` 0–3 → hex & judul tooltip |
| `ROLES` | Role login interim (v1, pre-MSAL): `tv` (default perangkat TV) · `pdca` · `tl`; kunci `localStorage["dms.role"]`; dipakai `RequireRole` & `Layout`. **Diganti klaim MSAL Entra ID pada tahap C** (A-02) — lihat `BACKEND_PLAN.md` §7.3 |
| `ROLE_LABEL` | Map `tv/pdca/tl` → label tampilan (`TV Device` / `PDCA` / `Team Leader`) |

### 4.3 `src/api/client.js`

Satu module fetch wrapper, bukan library axios — kecil & cukup.

| Bagian | Fungsi |
|---|---|
| `request(path, options)` | `AbortController` timeout **4 detik**; parse JSON aman; bila `!res.ok` lempar `Error(body.pesan \|\| 'HTTP '+status)` dengan `.status` & `.body` |
| `getState({plant, line, demo, tanggal})` | `GET /api/state?…` — data TV/dashboard |
| `getAdmin()` | `GET /api/admin` — data panel (opsional dipakai halaman admin internal) |
| `postAbsensi({nama, status, plant, line, perangkat})` | `POST /api/absensi` — 409 → lempar `{status:409}` |
| `postKonfirmasi({plant, line, pelaku})` | `POST /api/konfirmasi` |
| `postBuka({plant, line, pelaku, alasan})` | `POST /api/buka` (Supervisor/DH) |
| `postSync(sumberId?)` | `POST /api/sync` |
| `health()` | `GET /healthz` |

Aturan: **semua** call API lewat sini — tidak ada `fetch` liar di komponen.

### 4.4 Hooks

| Hook | Fungsi |
|---|---|
| `useDmsState({ plant, line, demo, tanggal, intervalMs = 15000 })` | `useState` + `useEffect` + `setInterval`; panggil `getState`; bila gagal → `buatDemoState(plant)` + flag `online=false`; return `{ state, online, loading, error, reload }` |
| `useNow()` (opsional) | Tick tiap 30 dtk untuk jam header (`HH.MM` dengan titik) |

### 4.5 Context

`DmsContext.jsx` (opsional, bila ingin state global): `{ plant, setPlant, state, online }` dengan `plant` dipersist ke `localStorage["dms.plant"]`. Bila tanpa context, plant dipegang di `App` dan diteruskan via props — cukup untuk skala ini.

### 4.6 Components

| Komponen | Props | Tanggung jawab |
|---|---|---|
| `Layout` | `plant, onPlantChange, online, children` | Topbar (logo, nav: Beranda·Absensi·5 short; **link Dashboard hanya untuk role PDCA/TL**, A-02 · plant select — **dikunci untuk TL**, bebas untuk PDCA/TV · indikator LIVE/CONTOH), pita banner (demo/offline), `<main>`, footer (aturan R) |
| `RequireRole` | `allow: ['pdca','tl'], children` | Gerbang rute terproteksi (A-02): baca role dari `localStorage["dms.role"]` (default `tv`); bila role tidak diizinkan → `<Navigate to="/" />` + `Toast` "Dashboard hanya untuk PDCA & TL (plant terkait)" |
| `KpiGrid` | `kpi[], warna, gelap` | Tabel `Item · Target · S1 · S2 · S3 · Harian · Minggu · Bulan`; sel `st0–3` berwarna; tanda `now` pada kolom Harian; empty note bila `kpi` kosong |
| `KasusTable` | `kolom[{nama,bobot}], baris[{sel,status,flag,kunci}]` | Judul `KASUS · sheet … · n baris`, tabel min-width scroll-X, maks 8 baris; sel status → `StatusPill`; sel PIC dengan `flag` → ⚠ + `title` |
| `PicaList` | `baris[], kolom[]` | Filter `status != 'CLOSE'`, maks 4 kartu: Problem (bold), Rootcause, Action, PIC, Due |
| `StatusPill` | `status` | Dua varian: status kasus (`open/progress/close`) & status halaman (`tersinkron/belum_diisi/belum_tersinkron/menunggu_berkas`) |
| `EmptyState` | `status, pesan, berkas[], sinkronTerakhir?` | Sesuai **Status Berkas Jujur** v1.1: tag besar status (4 nilai) · judul humanis · pesan penyebab (dari `pesan` API) · **jam acuan** — `belum_diisi` → "dicek terakhir hh.mm"; `belum_tersinkron` → "sinkron terakhir berhasil hh.mm" (+"belum pernah tersinkron" bila `sinkronTerakhir` kosong) · daftar `berkas[]` (`id · path · sheet · status`) atau ajakan daftarkan di `registry.json` (`menunggu_berkas`). Angka basi yang masih tampil diberi cap "data terakhir hh.mm" |
| `Toast` | `msg, onDone` | Overlay bawah-tengah, auto hilang 3,5 dtk; dipakai untuk 409/gagal konfirmasi |

### 4.7 Pages

| Page | Route | Fungsi |
|---|---|---|
| `Main.jsx` | `/` | **Landing TV (A-01)**: hero (logo + tagline singkat), **menu 5 pilar** (kartu SHE→Teknik — head berwarna, deskripsi, badge sheet, klik → `/pilar/:key`), **panel QR absensi** besar (dari `state.sesi.token` → gambar `/qr/<token>.png` + teks "Pindai untuk absensi" + status sesi: DIBUKA/DIKONFIRMASI). **Tanpa** CTA/link Dashboard (A-02). Optimal untuk layar TV/kiosk (font besar, kontras tinggi) |
| `Dashboard.jsx` | `/dashboard` | **Hanya PDCA & TL (A-02)** — dibungkus `<RequireRole allow={['pdca','tl']}>` di `App.jsx`. Ringkasan per tanggal: strip 4 KPI agregat, kartu per pilar, bar chart CSS perbandingan beban antar pilar. **PDCA**: plant switch Snack/EP/NP/Dairy bebas; **TL**: plant terkunci ke plant miliknya |
| `Pillar.jsx` | `/pilar/:key` | **Generik**: baca `useParams().key` → validasi terhadap `PILAR_KEYS` (redirect `/` bila aneh — **bukan** `/dashboard`, A-02); hero pilar (nama, sheet, status sinkron, aturan); bila `status !== 'tersinkron'` → `EmptyState`; selain itu `KpiGrid` + `KasusTable` + `PicaList`; navigasi prev/next pilar + "Semua Pilar" |
| `Absensi.jsx` | `/absensi` | Dua kolom: kiri ringkasan hadir (angka besar + detail + progress) + grid chip nama (klik = siklus status → `postAbsensi`; terkunci bila `dikonfirmasi`/offline) ; kanan kartu **Gerbang Absensi Dulu** (tombol konfirmasi → `postKonfirmasi` pelaku `web`, note audit) + kartu "Kenapa tidak ada tombol upload?" |
| `NotFound.jsx` | `*` | 404 sederhana + link Beranda (Dashboard hanya ditampilkan bila role `pdca`/`tl`) |

---

## 5. Routing & halaman

| Route | Halaman | Akses (A-01/A-02) | Pita banner | Data |
|---|---|---|---|---|
| `/` | `Main` — **landing semua TV** | 🌐 **Publik** — TV Device tanpa login (A-01) | opsional | `state.sesi.token` (QR), `state.sesi.status`, `state.tanggal`, `state.jam`, `state.plant/label_line` |
| `/dashboard` | `Dashboard` | 🔒 **PDCA** (semua plant) · **TL** (plant miliknya) — di luar itu redirect `/` + toast (A-02) | ya (offline/demo) | `state.ringkasan`, `state.tanggal`, `state.jam`, `state.pengawas`, `state.absensi.dikonfirmasi` |
| `/pilar` | → redirect `/` (landing) | 🌐 Publik | — | — |
| `/pilar/she` … `/pilar/teknik` | `Pillar` | 🌐 Publik (target klik menu di TV; aman dibuka semua orang) | ya | `state.halaman.find(h => h.key === key)` |
| `/absensi` | `Absensi` | 🌐 Publik (aksi tulis yang diaudit) | ya | `state.absensi`, `state.sesi` |
| `*` | `NotFound` | 🌐 Publik | — | — |

> **Perubahan v1.1:** redirect `/pilar` dulu mengarah ke `/dashboard` — sekarang mengarah ke `/` (landing, A-01), karena TV/role umum tidak boleh mendarat di rute terproteksi.

Catatan: **TV rotasi (`/` di Flask) dan landing QR (`/s/<token>`) tetap dirender Flask/HTML** atau dibuat halaman React terpisah di tahap berikutnya — jangan dipaksakan masuk SPA ini pada fase 1 (lihat `BACKEND_PLAN.md` §5).

### 5.1 Role & akses — Landing (semua TV) vs Dashboard (PDCA/TL)

Keputusan produk (24 Nov 2026): **landing tampil di setiap TV; dashboard hanya untuk role PDCA dan TL terkait.**

```
Setiap perangkat TV (TV Device)          Perangkat internal (laptop/HP)
┌───────────────────────────────┐        ┌───────────────────────────────┐
│  /  LANDING (A-01, publik)    │        │  login (interim: ?role=…)     │
│  ┌─ menu pilar SHE → Teknik ─┐│        │  role = pdca | tl             │
│  │  └─ klik → /pilar/<key>   ││        │  ┌─ /dashboard (RequireRole) ┐│
│  └─ panel QR absensi sesi    ┘│        │  │  PDCA → semua plant        ││
│       ( /qr/<token>.png )     │        │  │  TL   → plant sendiri      ││
└───────────────────────────────┘        └──┴─────────────────────────────┘
```

**Definisi role akses Dashboard (A-02):**

| Role | Singkatan | Plant | Dashboard ringkasan |
|---|---|---|---|
| **PDCA** | PDCA | **Semua** (Snack · EP · NP · Dairy) | ✅ lihat semua plant; plant switch bebas |
| **TL (Team Leader)** | TL | Plant miliknya saja | ✅ hanya plant plant sendiri; plant switch **terkunci** |
| Semua role lain (Leader Line, Petugas, Supervisor, DH, Admin, Auditor, **TV Device**) | — | — | ❌ tidak melihat menu, tidak bisa membuka `/dashboard` |

**Mekanisme interim v1 (pre-MSAL) — sampai login Entra ID (BACKEND_PLAN Tahap C) tersedia:**

- Role dibaca dari `localStorage["dms.role"]`, default **`tv`** bila kosong.
- Perangkat TV: kunjungi `/?role=tv` **sekali**; browser kiosk menyimpannya — akses tetap tanpa login,
  Dashboard tidak muncul (A-01/A-02). Plant TV di-set `?plant=EP` sekali (tersimpan di `dms.plant`).
- Pengguna internal: `/?role=pdca` (Plant Head/PDCA kantor) atau `/?role=tl` (Team Leader). TL **tidak**
  boleh mengganti plant; plant switch nonaktif dengan `title="TL hanya melihat plant-nya"`.
- `RequireRole` bukan sekadar menyembunyikan link — **rute `/dashboard` ditolak** (redirect `/` + toast).
  Ini guard sisi klien; **enforcement server menunggu tahap C** (lihat di bawah).
- Saat MSAL tersedia (tahap C), mekanisme `?role=` **dihapus** dan diganti: grup Entra **`DMS-PDCA-*`**
  → PDCA (semua plant), grup **`DMS-TL-*`** + klaim plant → TL (plant sendiri). Backend menolak `/api/state`
  agregat lintas plant untuk TL (403) — Batas Data per Plant.

**Yang harus terlihat di TV vs tidak:**

| Elemen | TV (`role=tv`) | PDCA | TL |
|---|---|---|---|
| Menu 5 pilar (klik → pilar) | ✅ | ✅ | ✅ |
| QR absensi + status sesi | ✅ | ✅ | ✅ |
| Link Dashboard di topbar | ❌ | ✅ | ✅ |
| Halaman `/pilar/<key>` | ✅ | ✅ | ✅ |
| `/dashboard` via URL langsung | ❌ (redirect `/`) | ✅ | ✅ plant sendiri |
| Plant switch Snack/EP/NP/Dairy | ❌/terkunci (dari profil TV) | ✅ bebas | 🔒 terkunci plant sendiri |

---

## 6. Pohon komponen per halaman

```
App
├── RequireRole (khusus /dashboard: pdca/tl; lainnya → redirect / + toast)
└── Layout (topbar · banner · footer; link Dashboard hanya pdca/tl)
    └── Routes
        ├── / ................ Main  — LANDING TV (A-01)
        │     ├── Hero (tagline singkat — font besar, kontras tinggi)
        │     ├── MenuPilar → 5 × Link.pilar-card → /pilar/<key>
        │     ├── QrPanel (gambar /qr/<token>.png · “Pindai untuk absensi” · status sesi/shift)
        │     └── AlurSatuPintu (4 langkah, ringkas)
        ├── /dashboard ....... Dashboard  — HANYA PDCA/TL (A-02)
        │     ├── StripKpi (4 tile: total · open · completion rata² · lewat)
        │     ├── PilarDashGrid → 5 × Link.pillar-dash (angka · progress · kv rows · pill)
        │     └── BarPerbandingan (bar CSS per pilar, max = nilai terbesar)
        ├── /pilar/:key ...... Pillar
        │     ├── PillarHero (nama · sheet · aturan · PageStatusPill · sinkron terakhir · jumlah)
        │     ├── EmptyState            ← bila status ≠ tersinkron
        │     └── (else) KpiGrid + KasusTable + PicaList
        ├── /absensi ......... Absensi
        │     ├── AbsensiRingkasan (angka besar hadir/total + det + progress)
        │     ├── ChipGrid → n × ChipNama (avatar 2 huruf · nama · status; onClick siklus)
        │     ├── GerbangCard (status sesi · tombol KONFIRMASI → postKonfirmasi)
        │     └── InfoCard (Kenapa tidak ada tombol upload?)
        └── * ................ NotFound
```

---

## 7. Data & API — pemetaan per halaman

Semua field mengikuti **`docs/API_CONTRACT.md`**. Endpoint yang dipakai: `GET /api/state` (polling 15 dtk)
+ `POST /api/absensi` & `POST /api/konfirmasi` (aksi). Panel admin (`/api/admin`) tidak dibutuhkan fase 1.

| Halaman | Field yang dibaca | Aksi |
|---|---|---|
| `Layout` (global) | `state.plant`, `state.label_line`, `state.sesi.status`, `state.demo`, `online` (lokal), `role` (lokal) | plant switch → refetch; **TL: terkunci** |
| `Dashboard` | _(A-02: hanya pdca/tl — role lain tidak pernah render halaman ini)_ `ringkasan[]` (`key,nama,warna,jumlah,status,open,completion,lewat`), `tanggal`, `hari_ini`, `jam`, `pengawas.hidup/putaran`, `sesi.status/shift`, `absensi.dikonfirmasi` | — (link ke pilar) |
| `Pillar` | `halaman[]` item: `key,nama,warna,status,pesan,jumlah,sinkron_terakhir,kpi[],kolom[],baris[],berkas[]`, `durasi` (abaikan), `tanggal` | — |
| `Absensi` | `absensi.nama[]` (`nama,status`), `absensi.total`, `absensi.hitung{…7 kunci}`, `absensi.dikonfirmasi`, `sesi.shift/status`, `plant`, `line` | `postAbsensi` per chip, `postKonfirmasi` tombol |
| `Main` | `sesi.token` (→ `<img src="/qr/<token>.png">`), `sesi.status`, `sesi.shift`, `sesi.sesi_id`, `tanggal`, `jam`, `plant`, `label_line` | — (QR murni gambar, tanpa aksi) |

**Pemetaan visual KPI (`st` → warna):** `0 → #1C3E8A` biru · `1 → #C22A26` merah-bawah target · `2 → #C22A26` merah-lewat batas · `3 → #A9A9A2` abu (belum diisi). Kolom `Harian` diberi outline emas (`now`).

**Format angka:** desimal memakai **koma** (`0,75`) dari server — tampilkan apa adanya.
**Urutan baris kasus:** sudah terurut server (OPEN → PROGRESS → CLOSE, due terdekat) — jangan di-sort ulang.

---

## 8. State management & polling

```
App (plant, setPlant)  ──pass──►  Layout(plant, online)  ──pass──►  pages
      │
      └─ useDmsState({ plant, line:'*', demo:'1', intervalMs:15000 })
             └─ state = GET /api/state … tiap 15 dtk (tanpa re-render kedip: setState replace)
                     └─ error → demoState(plant) + online=false (pita merah wajib tampil)
```

Aturan:

1. **Satu sumber state** — setiap halaman menerima `state` dari App lewat props; tidak ada fetch kedua.
2. Setelah aksi (`postAbsensi` / `postKonfirmasi`) → panggil `reload()` (fetch sekali langsung), jangan tunggu 15 dtk.
3. Polling berhenti otomatis saat tab ditutup (interval dibersihkan di `useEffect` return).
4. Plant tersimpan di `localStorage` — refresh tidak mereset pilihan.
5. **Optimistic UI minimal**: untuk chip absensi, panggil API dulu lalu `reload()`; jangan ubah lokal diam-diam (sumber kebenaran = server).
6. Error 409 (konfirmasi sudah dilakukan) → tampilkan toast "Absensi sudah dikonfirmasi; koreksi lewat Supervisor", bukan silent fail.
7. **Role & plant (v1.1):** `role` dibaca sekali dari `localStorage["dms.role"]` (default `tv`). **TL:** `plant` terkunci (dari profil/login), plant switch nonaktif — hanya melihat data plant-nya (A-02). **PDCA:** plant switch bebas (Snack/EP/NP/Dairy). **tv:** topbar tanpa Dashboard, plant dari profil TV (`?plant=`). Setelah tahap C (MSAL), `dms.role` tidak dipakai lagi.

---

## 9. Styling & design tokens

### 9.1 Token (variabel CSS)

```
--navy:#1B2C57  --navy-2:#16224A   (topbar, judul, grid KPI head)
--teal:#2E868C  --teal-2:#22666C   (aksen, tombol primer)
--gold:#C8A52B  --gold-2:#8A6C10   (CTA emas, tagline)
--bg:#F4F6FA    --card:#FFF  --rule:#DDE2EA   (latar, kartu, garis)
--text:#1E2430  --grey:#5C6472
--blue:#1C3E8A  --red:#C22A26  --grey-3:#A9A9A2  (sel KPI st0/1/2/3)
--green:#1E6B3A --green-bg:#E8F5EC   (pill OK)
--red-bg:#FDECEA                      (pill danger)
--warn-bg:#FBF3D9                     (pill warning)
--radius:14px   --shadow / --shadow-sm
```

### 9.2 Kelas utama (yang diharapkan tersedia di `index.css`)

- Layout shell: `.shell`, `.main`, `.topbar`, `.topbar-inner`, `.nav`, `.navlink(.active)`, `.brand`, `.plant-select`, `.conn(.off)`, `.footer`
- Banner: `.banner.demo` (kuning MODE DEMO) · `.banner.offline` (merah DATA CONTOH)
- Tombol: `.btn`, `.btn-primary`, `.btn-gold`, `.btn-outline`, `.btn-sm`
- Kartu: `.card`, `.card-pad`, `.section-title`, `.kpi-tile`, `.progress`, `.pill(.ok/.warn/.bad/.open/.progress/.close)`
- Hero Main: `.hero`, `.hero-eyebrow`, `.hero-cta`, `.hero-meta`, `.hero-card`, `.step-row/.step-num`
- Kartu pilar: `.pilar-grid/.pilar-card/.pilar-head/.pilar-body/.pilar-tag/.pilar-link`, `.pillar-dash-grid/.pillar-dash/.pd-head/.pd-num/.pd-kv`
- KPI: `.kpi-table`, `.cell.st0–st3`, `.cell.now`
- Kasus: `.kasus-table`, `.mono`, `.flag-ico`
- PICA: `.pica-grid`, `.pica-item`
- Absensi: `.abs-wrap`, `.abs-big`, `.abs-grid`, `.chip(.sakit/.izin/.alpa/.terlambat/.belum)`, `.confirm-box`, `.toast`
- Landing TV: `.qr-panel`, `.qr-img`, `.qr-status`, `.menu-pilar(.pilar-card)`, `.role-badge`
- Util: `.empty-state`, `.legend`, `.loading`

### 9.3 Aturan gaya

- Breakpoints: **≤1100px** kartu pilar 3 kolom & hero jadi 1 kolom; **≤760px** nav tersembunyi, pilar 2 kolom.
- Font: `system-ui` stack — tidak meng-download font web; terminal/pabrik friendly.
- Warna pilar **tidak boleh** menyimpang dari backend (`PILARS` di `constants.js` = `dms_core.DIVISI`).
- Angka KPI: `font-variant-numeric: tabular-nums`.
- Kontras: teks putih di atas `#D7B32A` (Quality) tidak lolos — pakai teks gelap `#2B2B28` (flag `teksGelap`).

---

## 10. Aset & logo

| Aset | Sumber | Tujuan |
|---|---|---|
| `public/logo.png` | `Logo/Logo.png` → resize 512px | Header brand (40px) + hero bila perlu |
| `public/logo-192.png` | resize 192px | `apple-touch-icon` |
| `public/favicon-32x32.png` | `Logo/favicon-32x32.png` | Tab browser |
| `docs/assets/mockup/tv.png` | referensi desain (bukan aset app) | Acuan visual saat review design |

Jangan menyimpan aset > 300 KB di `public/`; jangan menyimpan logo master asli (1000px, 1,4 MB) — simpan versi resize mengikuti tabel di atas.

---

## 11. Build, dev & deployment

### 11.1 Dev

```bash
npm install
npm run dev          # http://localhost:5173 (proxy /api,/qr,/s → http://localhost:8000)
python3 app/server.py  # backend, port 8000 — wajib untuk data asli
```

Bila backend mati, UI tetap render dengan pita **DATA CONTOH** (fallback `demoState.js`) — ini sengaja,
supaya desain bisa dikerjakan tanpa server.

Simulasi role (interim v1, sebelum MSAL): buka `/​?role=pdca` atau `/​?role=tl` sekali —
role tersimpan ke `localStorage`; `?plant=EP` untuk memilih plant TV. Untuk kembali ke tampilan TV:
`/​?role=tv`. Nilai interim ini dihapus di tahap C (lihat `BACKEND_PLAN.md` §7.3).

### 11.2 Production build

```bash
npm run build        # → dist/ (hashed assets)
npm run preview      # serve dist/ :4173
```

### 11.3 Deploy (opsi, selaras `BACKEND_PLAN.md` §5)

| Opsi | Cara | Catatan |
|---|---|---|
| **P1 · Flask serve `dist/`** | Flask route `/` → `FileResponse(dist/index.html)`; `/assets/*` static | Satu origin, tanpa CORS |
| **P2 · Nginx di depan** | `location / { root /path/dist; try_files $uri /index.html; }` + `location /api { proxy_pass http://127.0.0.1:8000; }` | Gunakan bila butuh HTTPS/caching |

`HashRouter` membuat P1 paling sederhana (tidak perlu rewrite `try_files`). Bila memilih `BrowserRouter`, wajib `try_files … /index.html` di Nginx atau equivalent di Flask.

**Setup perangkat TV (A-01):** setiap TV dibuka pada `http://<host>/` (kiosk/fullscreen), **bukan** `/dashboard`;
atur `?role=tv&plant=<Snack|EP|NP>` sekali agar tersimpan. TV hanya menampilkan landing; rotasi 7 halaman
TV-legacy tetap `GET /` Flask terpisah sampai fase TV-React (A-01/A-02 tidak memberi TV akses Dashboard).

### 11.4 Environment

Tidak ada secret di frontend. Satu-satunya konfigurasi: base URL API — **kosong** (same-origin) di produksi;
dev mengandalkan proxy Vite. Bila perlu beda host, tambah `VITE_API_BASE` di `.env` dan pakai sebagai prefix di `api/client.js`.

---

## 12. Naming convention & aturan folder

| Aspek | Aturan |
|---|---|
| Komponen file | `PascalCase.jsx` (`KasusTable.jsx`) |
| Hook | `useCamelCase.js` (`useDmsState.js`) |
| Util/api | `camelCase.js` (`client.js`) |
| Konstanta | `UPPER_SNAKE` di `constants.js` |
| CSS | satu file global `index.css` dengan kelas kebab-case `.pilar-grid` — hindari CSS-in-JS/module di fase 1 |
| Folder | `components/` · `pages/` · `hooks/` · `api/` · `data/` · `context/` — tanpa folder `utils/` kosong |
| Bahasa | Identifier/kode **Inggris**; teks UI **Indonesia** |
| Komentar | Bahasa Indonesia, singkat; kaitkan ke nomor aturan (`Absensi Dulu` …) bila relevan |

---

## 13. Yang TIDAK boleh / tidak perlu dibuat

1. ❌ **Tombol/form upload Excel** — melanggar Sinkron Excel Otomatis/Nol Langkah Tambahan.
2. ❌ **Form edit sel kasus** — kolom milik Excel, baca-saja (Kepemilikan Kolom).
3. ❌ **Kolom tabel dinamis dari API** — kolom kontrak statis; baris saja yang dinamis (Kolom Statis, Isi Dinamis).
4. ❌ **Lima file halaman pilar** (`ShePage`, `QualityPage`, …) — satu `Pillar.jsx` generik.
5. ❌ **Library UI besar** (MUI, AntD, Chakra) — CSS tokens cukup.
6. ❌ **State global kompleks** (Redux) — context/props cukup.
7. ❌ **Grafik custom dari nol** — fase 1 cukup bar chart CSS; library chart menyusul bila diminta.
8. ❌ **Halaman admin baru** — panel admin sudah ada di Flask (`/admin`); React cukup menautkan.
9. ❌ **Halaman TV rotasi di fase 1** — tetap Flask; menyusul di fase TV-React (`BACKEND_PLAN.md` M2).
10. ❌ **Hardcode plant/divisi/warna di luar `constants.js`** — satu sumber.
11. ❌ **Landing TV menampilkan link/tombol Dashboard** — TV (A-01) tidak boleh menautkan ke `/dashboard`; menu TV hanya 5 pilar + QR absensi.
12. ❌ **"Sembunyikan" tanpa proteksi rute** — `/dashboard` wajib dibungkus `RequireRole` (redirect `/` + toast), bukan hanya menghilangkan item menu.
13. ❌ **TL mengganti plant** — plant TL terkunci ke plant miliknya; hanya PDCA yang bebas lintas plant (A-02).
14. ❌ **TV diminta login / dashboard butuh role tapi bisa dibuka anonim** — TV Device tetap tanpa login; interim v1 pakai `?role=` di localStorage, final = MSAL (A-02, BACKEND_PLAN §7.3).
15. ❌ **Menambahkan route/halaman tanpa memperbarui akses A-01/A-02 di §5** dan dokumen ini.

---

## 14. Checklist pengerjaan (M1 → M3)

### M1 — Kerangka & halaman inti (estimasi 2–3 hari)

- [x] Scaffold Vite + React di root `front-end` (sudah ada)
- [ ] Salin aset logo ke `public/` (§10)
- [ ] `constants.js`, `api/client.js`, `index.css` (§4.2, §4.3, §9)
- [ ] `Layout` + `App` router + plant switch (localStorage) — topbar tanpa Dashboard untuk `role=tv`
- [ ] `useDmsState` + `demoState` fallback
- [ ] `Main.jsx` (**landing TV, A-01**): menu 5 pilar + panel QR absensi (`state.sesi.token` → `/qr/<token>.png`) + status sesi — **tanpa CTA Dashboard**
- [ ] `Dashboard.jsx` selesai — KPI agregat cocok dengan TV — **dibungkus `RequireRole`** (A-02)
- [ ] `RequireRole.jsx` + `ROLES` di `constants.js` (interim `?role=`, lihat §5.1)
- [ ] `Pillar.jsx` untuk `she` jalan end-to-end dari `/api/state`

### M2 — Paritas & aksi (estimasi 2–4 hari)

- [ ] 5 pilar via satu komponen — Delivery/Teknik tampil `EmptyState`
- [ ] `Absensi.jsx` — chip siklus + konfirmasi + toast 409
- [ ] Plant switch EP/NP menampilkan data plant itu — **PDCA bebas; TL terkunci plant sendiri (A-02)**
- [ ] Polling 15 dtk + `reload()` setelah aksi
- [ ] Pita MODE DEMO & DATA CONTOH bekerja
- [ ] **Uji A-01:** `?role=tv` → landing tanpa Dashboard; `/dashboard` via URL → redirect `/` + toast
- [ ] **Uji A-02:** `?role=pdca` → Dashboard + plant switch bebas · `?role=tl` → Dashboard, plant switch nonaktif
- [ ] `NotFound`, favicon, title/meta
- [ ] `npm run build` bersih, bundle < 350 KB gzip

### M3 — Produksi (setelah backend Tahap C–D)

- [ ] **Hapus mekanisme interim `?role=`/`dms.role`** — diganti MSAL (Entra ID): grup `DMS-PDCA-*` → PDCA (semua plant), grup `DMS-TL-*` + klaim plant → TL (plant sendiri); backend 403 untuk TL lintas plant (Batas Data per Plant, A-02)
- [ ] Login MSAL (Entra ID) bila endpoint dilindungi
- [ ] Serve `dist/` lewat Flask/Nginx (§11.3)
- [ ] Setup kiosk TV: `/` fullscreen, tanpa Dashboard (A-01)
- [ ] Smoke test: TV + ponsel QR + admin bersamaan

**Definisi selesai M1/M2:** demo internal — buka `/` (tampilan TV: menu pilar + QR, tanpa Dashboard), switch `?role=pdca` → buka `/dashboard` & klik setiap pilar, `?role=tl` → pastikan plant terkunci, konfirmasi absensi, semua angka sama dengan TV Flask (`http://localhost:8000/`).

---

*Dokumen ini v1.1 (24 Nov 2026). Perubahan struktur folder atau aturan akses (A-01/A-02) harus diperbarui di sini agar developer frontend tidak bekerja dari asumsi.*
