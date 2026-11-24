# Dokumentasi DMS — Digitalisasi Daily Monitoring System

Semua laporan, skrip, data, dan aset proyek DMS berkumpul di folder ini.
Sumber angka adalah tiga workbook di `reference/` (root repo) — **read-only, tidak diubah**.

## Struktur folder

```
docs/
├── ALUR_APLIKASI_DMS.md              ← ALUR APLIKASI (peran, 2 menu dashboard, landing QR, sinkron Excel)
├── API_CONTRACT.md                   ← KONTRAK API v1 (pegangan frontend React ↔ backend Flask)
├── BACKEND_PLAN.md                   ← RENCANA BACKEND (tahap A–D, SQL/SQLite→PostgreSQL, auth, deploy)
├── FRONTEND_STRUCTURE.md             ← STRUKTUR FRONTEND (pohon folder, routing, komponen, data flow)
├── laporan/                        ← SEMUA LAPORAN & DECK FINAL
│   ├── DMS_Digitalisasi_v1.pptx        deck presentasi (28 slide) — deliverable utama
│   ├── DMS_Review_Rancangan_v1.md      review rancangan + status perbaikan + verifikasi xlsx
│   ├── DMS_Insight_xlsx_ke_Aplikasi.md insight dari 3 workbook → terjemahan ke aplikasi
│   ├── DMS_Aturan_Sistem_v1.md         aturan sistem (R-01 … R-90)
│   ├── DMS_TV_PerDivisi_dan_Integrasi_Excel_v1.md  TV per divisi · absensi awal · QR · sinkron Excel
│   ├── DMS_Keputusan_Platform_dan_Akses_Online_v1.md  Power Platform vs aplikasi sendiri · akses lintas jaringan
│   ├── DMS_Logic_Design_v1.md          logika & model data
│   └── rancangan/                      paket rancangan 5 Nov (kanonik)
│       ├── 01-KENAPA-DMS-DIGITAL.md
│       ├── 02-RANCANGAN-APLIKASI.md
│       └── 03-ALUR-SISTEM.md
│
├── scripts/                        ← SKRIP BUILD & ANALISIS
│   ├── analyze_workbook.py             baca reference/*.xlsx → docs/data/data_plants.json
│   ├── make_mockups.py                 gambar ilustrasi layar/papan → docs/assets/mockup/
│   ├── build_deck.py                   rakit deck → docs/laporan/DMS_Digitalisasi_v1.pptx
│   └── render_deck.py                  render slide → PNG (verifikasi visual, tanpa LibreOffice)
│
├── data/
│   └── data_plants.json                hasil ekstraksi 3 workbook (terverifikasi 78/78 cocok)
│
├── assets/                         ← GAMBAR, FONT, MOCKUP
│   ├── papan/                          foto papan DMS asli B.U.E Factory 10
│   ├── mockup/                         ilustrasi layar (tv=SHE, tv_quality, tv_produksi, tv_absen, tv_qr, form, dasbor, admin, kasus, laporan)
│   ├── fonts/                          Kalam (tulisan tangan spidol untuk ilustrasi papan)
│   ├── gf_logo.png, gf_cover_band.jpg
│
└── template/
    └── template_master.pptx            template master deck (hasil rekonstruksi dari deck)
```

## Cara membangun ulang deck

Dari root repo, jalankan berurutan:

```bash
pip install python-pptx pillow openpyxl

python3 docs/scripts/analyze_workbook.py   # reference/*.xlsx  → docs/data/data_plants.json
python3 docs/scripts/make_mockups.py       # ilustrasi layar   → docs/assets/mockup/
python3 docs/scripts/build_deck.py         # rakit deck        → docs/laporan/DMS_Digitalisasi_v1.pptx
```

- Seluruh angka di deck dibaca dari `docs/data/data_plants.json`, jadi bila workbook diperbarui,
  cukup jalankan ulang `analyze_workbook.py` lalu `build_deck.py`.
- Ilustrasi TV (slide 6–7 dan 24–26) memakai bentuk papan fisik — grid KPI, angka spidol
  biru/merah (font Kalam), baris PICA — tetapi **satu divisi per layar** dengan kolom mengikuti
  Excel, ditambah halaman absensi awal dan layar QR satu pintu.
- `render_deck.py` dipakai untuk memeriksa visual slide (menghasilkan PNG per slide).

## Aplikasi prototipe

Prototipe yang berjalan ada di **`app/`** (lihat `app/README.md`): ingest Excel otomatis, TV per
divisi, absensi sebagai gerbang, QR sesi, dan panel sinkronisasi. Alur lengkap aplikasi (role,
landing QR, 2 dashboard, sinkron Excel, KPI, model data) didokumentasikan di
**`docs/ALUR_APLIKASI_DMS.md`**. Untuk pengembangan frontend/backend: **`docs/API_CONTRACT.md`**
(kontrak endpoint), **`docs/BACKEND_PLAN.md`** (rencana backend), dan **`docs/FRONTEND_STRUCTURE.md`**
(struktur & penempatan frontend untuk branch `front-end`). Jalankan:

```bash
pip install -r app/requirements.txt
python3 app/seed_demo.py
python3 app/server.py        # http://0.0.0.0:8000
```

## Catatan

- `reference/` dan foto papan asli diperlakukan sebagai acuan tetap (tidak diubah).
- Angka kanonik ada di `laporan/DMS_Insight_xlsx_ke_Aplikasi.md` §8; ringkasan verifikasi
  (78/78 cocok dengan xlsx) ada di `laporan/DMS_Review_Rancangan_v1.md`.
