# Dokumentasi DMS — Digitalisasi Daily Monitoring System

Semua laporan, skrip, data, dan aset proyek DMS berkumpul di folder ini.
Sumber angka adalah tiga workbook di `reference/` (root repo) — **read-only, tidak diubah**.

## Struktur folder

```
docs/
├── laporan/                        ← SEMUA LAPORAN & DECK FINAL
│   ├── DMS_Digitalisasi_v1.pptx        deck presentasi (25 slide) — deliverable utama
│   ├── DMS_Review_Rancangan_v1.md      review rancangan + status perbaikan + verifikasi xlsx
│   ├── DMS_Insight_xlsx_ke_Aplikasi.md insight dari 3 workbook → terjemahan ke aplikasi
│   ├── DMS_Aturan_Sistem_v1.md         aturan sistem (R-01 … R-77)
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
│   ├── mockup/                         ilustrasi layar (termasuk papan DMS realistis: tv, tv_absen)
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
- Ilustrasi papan DMS (slide 6–7) digambar menyerupai papan fisik: 5 kolom pilar berwarna,
  grid shift 1–3, angka spidol biru/merah (font Kalam), dan baris PICA.
- `render_deck.py` dipakai untuk memeriksa visual slide (menghasilkan PNG per slide).

## Catatan

- `reference/` dan foto papan asli diperlakukan sebagai acuan tetap (tidak diubah).
- Angka kanonik ada di `laporan/DMS_Insight_xlsx_ke_Aplikasi.md` §8; ringkasan verifikasi
  (78/78 cocok dengan xlsx) ada di `laporan/DMS_Review_Rancangan_v1.md`.
