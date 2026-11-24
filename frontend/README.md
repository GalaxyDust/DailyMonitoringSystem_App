# frontend/ — DMS Web (Kerangka Struktur)

> **Ini KERANGKA KOSONG.** Tidak ada kode implementasi di sini — hanya penempatan
> berkas yang **mengikuti scaffold branch `front-end`** (aplikasi Vite+React di root repo)
> dan **`docs/FRONTEND_STRUCTURE.md`** (pohon folder, fungsi tiap file, aturan akses A-01/A-02).
>
> Branch `front-end` (milik frontend, cf13dab) berisi scaffold Vite+React di **root repo**
> (React 19 · Vite 8 · ESLint; `index.html`, `vite.config.js`, `src/main.jsx`, `src/App.jsx`,
> `public/favicon.svg`, `public/icons.svg`, `src/assets/*` — masih template default).
>
> Cara pakai:
> 1. Buka branch `front-end` (milik teman/frontend).
> 2. Isi setiap berkas di bawah ini sesuai `docs/FRONTEND_STRUCTURE.md` §4 (fungsi tiap file)
>    dan §5 (routing + aturan akses A-01/A-02). Urutan kerja: §14 (M1 → M3).
> 3. Folder ini (`frontend/` di branch backend) hanya referensi struktur — **jangan di-merge
>    ke `main` bersamaan dengan implementasi**, isinya akan redundan.
>
> Perbedaan yang disengaja vs scaffold `front-end`:
> - Plant **Dairy** (kode DR) ikut enum `plant` (4 plant: Snack · EP · NP · Dairy); belum ada berkas sumber — tampil `menunggu_berkas`.
- Istilah aturan memakai **nama manusiawi** (Aturan Sistem v1.1) — tidak ada kode R-xx; lihat `docs/laporan/DMS_Aturan_Sistem_v1.md` Lampiran A bila merujuk dokumen lama.
- Aset DMS memakai **logo GARUDAFOOD** (`public/logo*.png`, `favicon-32x32.png`) — bukan ikon Vite.
> - `App.css`, `src/assets/react.svg|vite.svg|hero.png`, `public/icons.svg` **tidak dipakai** —
>   gaya global di `src/index.css`; aset dari `Logo/` (root repo) atau `docs/assets/`.
> - Routing & halaman sesuai spec (HashRouter, `/` landing TV, `/dashboard` PDCA/TL).
