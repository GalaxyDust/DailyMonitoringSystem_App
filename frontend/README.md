# DMS — Frontend (React + Vite)

Frontend DMS (Daily Monitoring System) Garudafood: **Beranda (Main)**, **Dashboard 5 Pilar**,
satu halaman per pilar (**SHE · QUALITY · PRODUKSI/PRODUCTIVITY · DELIVERY · TECHNIK**), dan **Absensi** —
dengan fallback data contoh bila backend belum jalan.

> Branch: dibuat di branch backend (`arena/…`), folder `frontend/` — pindahkan ke branch `front-end`
> (root repo) bila sudah cocok. Kontrak API: `../docs/API_CONTRACT.md` (v1).

## Menjalankan

```bash
cd frontend
npm install
npm run dev      # http://localhost:5173  (proxy /api,/qr,/s → http://localhost:8000)
```

Pastikan backend Flask jalan untuk data asli:

```bash
python3 app/seed_demo.py    # sekali saja
python3 app/server.py       # port 8000
```

## Build & preview

```bash
npm run build    # → dist/
npm run preview  # serve dist/ di http://localhost:4173
```

Produksi: sajikan `dist/` lewat Flask (static) atau Nginx — lihat `docs/BACKEND_PLAN.md` §5.

## Struktur

```
frontend/
├── index.html
├── vite.config.js            proxy dev → :8000
├── public/                   logo.png · logo-192.png · favicon-32x32.png
└── src/
    ├── main.jsx · App.jsx    HashRouter + plant switch (localStorage)
    ├── constants.js          5 pilar (urutan & warna = backend) · enum KPI/status
    ├── index.css             design system (navy/teal/gold)
    ├── api/client.js         fetch wrapper (timeout 4 dtk, error → {pesan})
    ├── hooks/useDmsState.js  polling /api/state 15 dtk (+ fallback data contoh)
    ├── data/demoState.js     data contoh (bentuk = API contract)
    ├── components/           Layout · KpiGrid · KasusTable · PicaList
    │                         StatusPill · EmptyState
    └── pages/                Main (beranda) · Dashboard (5 pilar) · Pillar (generik)
                              Absensi (gerbang R-81) · NotFound
```

## Halaman

| Route | Isi |
|---|---|
| `/` | Beranda: hero, cara kerja, kartu 5 pilar, alur satu pintu |
| `/dashboard` | Ringkasan 5 pilar: KPI agregat, kartu per pilar, bar perbandingan |
| `/pilar/she` · `/pilar/quality` · `/pilar/produksi` · `/pilar/delivery` · `/pilar/teknik` | Grid KPI (S1–Bulan), tabel kasus (kolom Excel), PICA terbuka |
| `/absensi` | Absensi shift (gerbang R-81): chip status + konfirmasi kehadiran |

## Catatan

- **Tidak ada upload/form input kasus** — data mengalir satu arah dari Excel (R-85/R-88/R-89).
- Kolom & warna divisi **tidak boleh** berbeda dari backend (`app/dms_core.py`, `app/server.py`).
- State absensi menulis ke `/api/absensi` & `/api/konfirmasi` — sesi yang sama dengan TV.
- Bila server mati, halaman tetap render dengan pita merah "DATA CONTOH".
