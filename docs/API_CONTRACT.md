# DMS — Kontrak API (API Contract)

> **Frontend (Vite + React, branch `front-end`) ↔ Backend (Flask, `app/`)**
>
> Versi kontrak: **v1.1** · 24 November 2026 (v1.1: §10 Aturan akses A-01/A-02 — tanpa perubahan skema endpoint) · Ditulis dari kode aktual `app/server.py` & `app/dms_core.py`.
> Kalau perilaku endpoint berubah di kode, kontrak ini **wajib** ikut diperbarui — frontend bergantung padanya.

| Item | Keterangan |
|---|---|
| Base URL (dev) | `http://localhost:8000` |
| Base URL (prod) | HTTPS domain perusahaan (belum ditentukan — lihat `BACKEND_PLAN.md` §8) |
| Format | JSON (`Content-Type: application/json`, `ensure_ascii=False`, charset UTF-8) |
| Autentikasi v1 | **Belum ada** — semua endpoint terbuka (prototipe). Rencana auth: §10 |
| Tanggal | `YYYY-MM-DD` (contoh `2026-11-24`) |
| Waktu | `YYYY-MM-DD HH:MM:SS` (contoh `2026-11-24 06:31:12`), lokal server |
| Jam TV | `HH.MM` dengan titik (contoh `08.30`) |
| Bahasa pesan | Bahasa Indonesia |
| Kunci error | Selalu `pesan` — **bukan** `error` / `message` |

---

## Daftar Isi

1. [Konvensi & enum](#1-konvensi--enum)
2. [Ringkasan endpoint (12 route)](#2-ringkasan-endpoint-12-route)
3. [GET `/api/state` — state lengkap TV](#3-get-apistate--state-lengkap-tv)
4. [POST `/api/absensi` — ubah status satu nama](#4-post-apiabsensi--ubah-status-satu-nama)
5. [POST `/api/konfirmasi` — konfirmasi kehadiran](#5-post-apikonfirmasi--konfirmasi-kehadiran)
6. [POST `/api/buka` — buka ulang sesi (Supervisor/DH)](#6-post-apibuka--buka-ulang-sesi-supervisordh)
7. [POST `/api/sync` — sinkron paksa Excel](#7-post-apisync--sinkron-paksa-excel)
8. [GET `/api/admin` — data panel admin](#8-get-apiadmin--data-panel-admin)
9. [Endpoint pendukung (halaman, QR, font, health)](#9-endpoint-pendukung-halaman-qr-font-health)
10. [Autentikasi (target) & header](#10-autentikasi-target--header)
11. [Ketidakkonsistenan & known gaps](#11-ketidakkonsistenan--known-gaps)
12. [Perubahan kontrak & versioning](#12-perubahan-kontrak--versioning)
13. [Contoh alur frontend](#13-contoh-alur-frontend)

---

## 1. Konvensi & enum

### 1.1 Enum `plant`

| Nilai | Keterangan |
|---|---|
| `Snack` | Snack plant (kode SN) — default di semua endpoint |
| `EP` | Exist Plant |
| `NP` | New Plant |

> Plant tidak divalidasi oleh server saat ini; nilai lain akan menghasilkan papan kosong.

### 1.2 Enum `line`

Format `Line <angka>` (mis. `Line 9`) atau `*` = semua line. Line lain dibiarkan apa adanya (tidak divalidasi).

### 1.3 Enum divisi

| `key` | Nama tampilan | Warna |
|---|---|---|
| `she` | `SHE / SAFETY` | `#B02F2F` |
| `quality` | `QUALITY` | `#D7B32A` |
| `produksi` | `PRODUKSI / PRODUCTIVITY` | `#A62E2E` |
| `delivery` | `DELIVERY` | `#2E7D46` |
| `teknik` | `TECHNIC PERFORM` | `#2A5CA0` |

### 1.4 Enum status absensi per nama

`hadir` · `sakit` · `izin` · `alpa` · `terlambat` · `dinas luar` · `belum pasti`

Siklus klik di TV: `hadir → sakit → izin → alpa → terlambat → belum pasti → hadir …`

### 1.5 Enum status sesi

| Status | Arti |
|---|---|
| `DIBUKA` | Sesi dibuka, absensi belum dikonfirmasi — TV terkunci di halaman Absensi |
| `DIKONFIRMASI` | Kehadiran dikonfirmasi — rotasi divisi berjalan |

### 1.6 Enum status kasus

`OPEN` · `PROGRESS` · `CLOSE` (urutan tampil OPEN → PROGRESS → CLOSE, lalu `due` terdekat)

### 1.7 Enum status halaman divisi (`halaman[].status`)

| Status | Arti |
|---|---|
| `tersinkron` | Berkas terdaftar, pernah tersinkron, ada baris bertanggal tampil |
| `belum_diisi` | Tersinkron tetapi tidak ada baris bertanggal tampil |
| `belum_tersinkron` | Berkas terdaftar tetapi belum pernah tersinkron |
| `menunggu_berkas` | Berkas divisi belum didaftarkan (Delivery & Teknik) |

### 1.8 Kode warna KPI (`kpi[].vals[].st`)

| `st` | Warna | Arti |
|---|---|---|
| `0` | Biru `#1C3E8A` | Sesuai target |
| `1` | Merah `#C22A26` | Di bawah target |
| `2` | Merah `#C22A26` | Lewat batas (mis. lewat tenggat > 0) |
| `3` | Abu `#A9A9A2` | Belum diisi / tidak ada data |

### 1.9 Struktur sel & kolom (kontrak Excel → layar, R-83/R-84)

`kolom` = kontrak kolom **statis** per divisi (nama + bobot lebar). `baris[].sel` = array string **sebaris dengan `kolom`**, sudah diformat untuk tampilan (`D Mon` untuk tanggal). Kolom yang tidak ada nilainya berisi string `"—"`. Format angka desimal memakai **koma** (`0,75`).

---

## 2. Ringkasan endpoint (12 route)

| # | Method & path | Fungsi | Body / query | Sukses | Error |
|---|---|---|---|---|---|
| 1 | `GET /` | Shell TV (HTML) | — | 200 HTML | — |
| 2 | `GET /admin` | Shell panel admin (HTML) | — | 200 HTML | — |
| 3 | `GET /s/<token>` | Landing QR sesi (HTML) | path `token` | 200 HTML sesi | **404** token tidak dikenal |
| 4 | `GET /qr/<token>.png` | Gambar QR sesi | path `token` | 200 `image/png` | — |
| 5 | `GET /fonts/<nama>` | Font Kalam | path `nama` | 200 font | — |
| 6 | `GET /healthz` | Health check | — | 200 `{"ok":true,"pengawas":<bool>}` | — |
| 7 | `GET /api/state` | State lengkap untuk TV | query: `plant`, `line`, `demo`, `tanggal` | 200 JSON | — |
| 8 | `POST /api/absensi` | Ubah status satu nama | JSON | 200 `{"ok":true}` | **409** |
| 9 | `POST /api/konfirmasi` | Konfirmasi kehadiran | JSON (boleh `{}`) | 200 `{"ok":true}` | — |
| 10 | `POST /api/buka` | Buka ulang sesi (Supervisor/DH) | JSON | 200 `{"ok":true}` | — |
| 11 | `POST /api/sync` | Sinkron paksa Excel | JSON `{"sumber_id"?}` | 200 `{"ok":true,"hasil":[…]}` | per-item `ok:false` |
| 12 | `GET /api/admin` | Data panel admin | — | 200 JSON | — |

**Komposisi:** 6 route API JSON (`/api/*`) + 3 halaman HTML (`/`, `/admin`, `/s/<token>`) + 3 pendukung (`/qr/...png`, `/fonts/...`, `/healthz`).

---

## 3. GET `/api/state` — state lengkap TV

Endpoint utama yang dipanggil TV (polling 15 dtk) dan dapat dipakai semua tampilan React.

### 3.1 Query parameters

| Param | Tipe | Default | Keterangan |
|---|---|---|---|
| `plant` | string | `Snack` | `Snack` / `EP` / `NP` |
| `line` | string | `*` | `*` = semua line; atau `Line 9` |
| `demo` | string | `1` | `1` = boleh memutar data historis (label MODE DEMO); `0` = data hari ini |
| `tanggal` | string | — | `YYYY-MM-DD`; bila diisi, dipakai apa adanya (menang atas `demo`) |

**Logic pemilihan tanggal tampil:**

```
bila ada ?tanggal=  → tanggal = ?tanggal
bila tidak & demo=1 → tanggal = tanggal dengan kasus terbanyak (tanggal_terpadat), atau hari ini bila kosong
bila tidak & demo=0 → tanggal = hari ini
```

`demo` di respons = `true` hanya bila `demo=1` **dan** tanggal tampil ≠ hari ini.

### 3.2 Respons — struktur lengkap (200)

```json
{
  "plant": "Snack",
  "line": "*",
  "label_line": "Semua line",
  "tanggal": "2026-11-24",
  "hari_ini": "2026-11-24",
  "demo": true,
  "tanggal_tersedia": ["2026-11-24", "2026-11-23", "..."],
  "sesi": {
    "sesi_id": "Snack-*-2026-11-24-1",
    "plant": "Snack",
    "line": "*",
    "tanggal": "2026-11-24",
    "shift": "1",
    "status": "DIBUKA",
    "token": "AbCdEfGh12",
    "dibuka_pada": "2026-11-24 06:00:01",
    "dikonfirmasi_pada": null
  },
  "absensi": {
    "nama": [
      {"nama": "Ahmad Fauzi", "status": "hadir"}
    ],
    "total": 28,
    "hitung": {
      "hadir": 25, "sakit": 1, "izin": 0, "alpa": 0,
      "terlambat": 1, "dinas luar": 0, "belum pasti": 1
    },
    "dikonfirmasi": false
  },
  "halaman": [ /* 5 item divisi, urutan: she, quality, produksi, delivery, teknik */ ],
  "ringkasan": [ /* 5 item ringkas, urutan sama */ ],
  "durasi": {"absensi": 30, "she": 25, "quality": 25, "produksi": 30,
             "delivery": 20, "teknik": 20, "ringkasan": 20},
  "pengawas": {
    "hidup": true,
    "putaran": 1234,
    "terakhir": "2026-11-24 06:31:12",
    "perubahan": [
      {"sumber": "SN-SHE", "waktu": "2026-11-24 06:31:12",
       "tambah": 0, "ubah": 1, "pesan": "OK"}
    ]
  },
  "jam": "08.30"
}
```

#### 3.2.1 `halaman[]` — satu item per divisi

| Field | Tipe | Keterangan |
|---|---|---|
| `key` | string | `she` / `quality` / `produksi` / `delivery` / `teknik` |
| `nama` | string | Nama tampilan (lihat §1.3) |
| `warna` | string | Hex warna divisi |
| `durasi` | number | Detik rotasi di TV |
| `status` | string | `tersinkron` / `belum_diisi` / `belum_tersinkron` / `menunggu_berkas` |
| `pesan` | string | Pesan keadaan kosong; string kosong bila `tersinkron` |
| `terdaftar` | boolean | Apakah berkas divisi terdaftar di `registry.json` |
| `sinkron_terakhir` | string\|"" | Waktu sinkron terakhir; `""` bila belum pernah |
| `jumlah` | number | Jumlah baris kasus pada tanggal tampil |
| `kpi` | array | Grid KPI (lihat 3.2.2); **kosong** bila `!terdaftar` |
| `kolom` | array | `{nama, bobot}` — kontrak kolom statis (lihat 3.2.3) |
| `baris` | array | Maks **7** baris; tampilkan 6 (lihat 3.2.4) |
| `berkas` | array | Berkas sumber divisi itu (lihat 3.2.5) |

#### 3.2.2 `kpi[]` — grid KPI per periode

| Field | Keterangan |
|---|---|
| `item` | `Kasus tercatat` · `Open` · `Close` · `PICA completion rate` · `Lewat tenggat` · (+`Downtime (min)` khusus `produksi`, diletakkan di posisi ke-2) · `Total downtime (min)` pada KPI tunggal |
| `target` | `—`, `0`, atau `0,80` (completion rate) |
| `vals` | **6 angka**, urutan kolom: `S1 · S2 · S3 · Harian · Minggu · Bulan` |
| `vals[].v` | string tampilan; `"—"` bila tidak ada data |
| `vals[].st` | kode warna `0..3` (§1.8) |

Contoh:

```json
{
  "item": "PICA completion rate",
  "target": "0,80",
  "vals": [
    {"v": "0,75", "st": 1},
    {"v": "—",    "st": 3},
    {"v": "—",    "st": 3},
    {"v": "0,75", "st": 1},
    {"v": "0,80", "st": 0},
    {"v": "0,82", "st": 0}
  ]
}
```

#### 3.2.3 `kolom[]`

```json
[{"nama": "Tgl", "bobot": 5}, {"nama": "Shift", "bobot": 4}, {"nama": "LBN", "bobot": 8}]
```

Bobot dipakai sebagai `fr` grid (`gridTemplateColumns = bobot.map(b => b + 'fr').join(' ')`).

#### 3.2.4 `baris[]`

```json
{
  "sel": ["6 Nov", "1", "Line 9", "Area 3", "Near Miss", "…", "…", "…", "Budi", "9 Nov", "12", "OPEN"],
  "status": "OPEN",
  "flag": "",
  "kunci": "sha1…",
  "sumber_id": "SN-SHE",
  "baris_excel": 42
}
```

- `sel` **sejajar** dengan `kolom` (indeks sama).
- `status` ∈ `OPEN` / `PROGRESS` / `CLOSE` — dipakai untuk kelas warna dan urutan.
- `flag` berisi alasan flag (mis. `PIC berupa tautan, bukan nama`) atau string kosong; tampilkan ⚠ + tooltip.
- `kunci` = PK baris (`kunci_baris`) — jangan diuraikan; dipakai untuk referensi audit/koreksi.

#### 3.2.5 `berkas[]`

```json
{
  "id": "SN-SHE",
  "path": "12. Konsep Penilaian DMS Snack Des 24.xlsx",
  "sheet": "Resume SHE",
  "status": "aktif",
  "sinkron": "2026-11-24 06:31:12",
  "pesan": "header baris 17 · 3 baris dikarantina"
}
```

`path` hanya **nama berkas** (basename), bukan path lengkap.

#### 3.2.6 `ringkasan[]`

```json
{
  "key": "she",
  "nama": "SHE / SAFETY",
  "warna": "#B02F2F",
  "jumlah": 7,
  "status": "tersinkron",
  "open": "2",
  "completion": "0,71",
  "lewat": "1"
}
```

`open`, `completion`, `lewat` = string dari kolom **Harian** KPI masing-masing divisi (`"—"` bila tidak ada).

### 3.3 Catatan perilaku

- Baris kasus = `info["semua"][:7]` — maksimal 7 baris dari query (sudah terurut OPEN → PROGRESS → CLOSE lalu `due` terdekat).
- `tanggal_tersedia` dibatasi 30 entri terbaru.
- Tidak ada HTTP error dari endpoint ini; kegagalan server = 500 HTML (belum JSON — lihat §11).

---

## 4. POST `/api/absensi` — ubah status satu nama

### 4.1 Request

```json
{
  "nama": "Ahmad Fauzi",
  "status": "sakit",
  "plant": "Snack",
  "line": "*",
  "perangkat": "tv"
}
```

| Field | Wajib | Keterangan |
|---|---|---|
| `nama` | ✅ | Harus ada di daftar absensi sesi aktif; **tidak divalidasi** — nama yang salah tidak mengenai baris mana pun (respons tetap `ok:true`) — lihat §11 |
| `status` | ✅ (default `hadir`) | Enum §1.4 |
| `plant` | — (default `Snack`) | |
| `line` | — (default `*`) | |
| `perangkat` | — (default `tv`) | Dicatat di audit (`pelaku`) |

### 4.2 Respons sukses (200)

```json
{"ok": true}
```

Efek samping: `UPDATE absensi …` + `INSERT audit(…, 'absensi', {"nama":…, "status":…})`.

### 4.3 Respons ditolak (409) — absensi sudah dikonfirmasi

```json
{"ok": false, "pesan": "Absensi sudah dikonfirmasi; koreksi lewat Supervisor"}
```

Satu-satunya jalan koreksi setelah konfirmasi: `POST /api/buka` (Supervisor/DH) lalu `POST /api/konfirmasi` lagi (§5–6).

---

## 5. POST `/api/konfirmasi` — konfirmasi kehadiran

### 5.1 Request

```json
{"plant": "Snack", "line": "*", "pelaku": "leader"}
```

Body boleh kosong (`{}`) — semua field opsional.

| Field | Default | Keterangan |
|---|---|---|
| `plant` | `Snack` | |
| `line` | `*` | |
| `pelaku` | `leader` | TV memakai `leader`; landing QR memakai `QR sesi` |

### 5.2 Respons sukses (200)

```json
{"ok": true}
```

Efek samping (berurutan):

1. `sesi.status` → `DIKONFIRMASI`, `sesi.dikonfirmasi_pada` → waktu sekarang
2. Semua `absensi.status = 'belum pasti'` → `hadir`
3. `INSERT audit(…, pelaku, 'konfirmasi_absensi', sesi_id)`

> Idempoten dari sisi TV/QR (tombol nonaktif setelah konfirmasi), tetapi endpoint ini **tidak menolak** konfirmasi kedua — ia hanya menulis ulang. Tidak menimbulkan kerusakan data, tetapi audit akan berisi dua entri.

---

## 6. POST `/api/buka` — buka ulang sesi (Supervisor/DH)

Jalan keluar darurat R-81 bila absensi salah setelah dikonfirmasi.

### 6.1 Request

```json
{
  "plant": "Snack",
  "line": "*",
  "pelaku": "supervisor",
  "alasan": "Salah tandai alpa, yang benar izin"
}
```

| Field | Default | Keterangan |
|---|---|---|
| `plant` | `Snack` | |
| `line` | `*` | |
| `pelaku` | `supervisor` | Dicatat di audit |
| `alasan` | `(tanpa alasan)` | Dicatat di audit — selalu diisi, walau kosong |

### 6.2 Respons sukses (200)

```json
{"ok": true}
```

Efek samping: `sesi.status` → `DIBUKA`, `sesi.dikonfirmasi_pada` → NULL, `INSERT audit(…, pelaku, 'buka_ulang_sesi', alasan)`.

---

## 7. POST `/api/sync` — sinkron paksa Excel

Membaca ulang berkas Excel **tanpa menunggu** pengawas folder. Dipakai tombol **Sinkronkan sekarang** di `/admin` dan tombol `S` di TV.

### 7.1 Request

```json
{}                    → semua sumber
{"sumber_id": "SN-SHE"} → satu sumber
```

Body boleh kosong. Method `POST`.

### 7.2 Respons sukses (200)

```json
{
  "ok": true,
  "hasil": [
    {
      "sumber_id": "SN-SHE",
      "ok": true,
      "tambah": 1,
      "ubah": 2,
      "karantina": 0,
      "baris": 352,
      "sheet": "Resume SHE",
      "header": 17
    }
  ]
}
```

Item `hasil[]` — field umum:

| Field | Keterangan |
|---|---|
| `sumber_id` | ID sumber yang diproses |
| `ok` | `true` bila berhasil; `false` bila berkas tidak ada / gagal baca |
| `skip` | `true` bila tidak ada perubahan (`sidik_file` sama, bukan force) — hanya muncul saat skip |
| `tambah` / `ubah` / `karantina` / `baris` / `sheet` / `header` | Statistik ingest |
| `pesan` | Pesan (selalu ada saat `ok:false`; saat sukses/skip, berisi keterangan) |

**Perhatian:** HTTP tetap **200** walaupun satu/semua item gagal — kegagalan per-berkas ada di `ok:false` per item, bukan di status HTTP (lihat §11).

---

## 8. GET `/api/admin` — data panel admin

### 8.1 Respons sukses (200)

```json
{
  "sumber": [
    {
      "sumber_id": "SN-SHE", "plant": "Snack", "line": "*", "divisi": "she",
      "path": "reference/12. Konsep Penilaian DMS Snack Des 24.xlsx",
      "sheet": "auto", "status": "aktif",
      "sinkron_terakhir": "2026-11-24 06:31:12",
      "tambah": 12, "ubah": 340, "baris_terbaca": 352,
      "pesan": "header baris 17 · 3 baris dikarantina",
      "sidik_file": "…"
    }
  ],
  "log": [
    {"id": 12, "sumber_id": "SN-SHE", "mulai": "2026-11-24 06:31:05",
     "selesai": "2026-11-24 06:31:12", "tambah": 1, "ubah": 2,
     "karantina": 0, "pesan": "sheet Resume SHE, header 17"}
  ],
  "karantina": [
    {"id": 5, "sumber_id": "SN-QC", "baris_excel": 88,
     "alasan": "tanggal tidak terbaca", "data": "[…]",
     "dibuat_pada": "2026-11-24 06:31:10"}
  ],
  "karantina_total": 61,
  "flagged": 708,
  "kasus": 15940,
  "terhapus": 3,
  "audit": [
    {"id": 99, "waktu": "2026-11-24 07:02:11", "pelaku": "tv",
     "aksi": "absensi", "rinci": "{\"nama\": \"Ahmad\", \"status\": \"sakit\"}"}
  ],
  "pengawas": {
    "hidup": true, "putaran": 1234,
    "perubahan": [{"sumber": "SN-SHE", "waktu": "2026-11-24 06:31:12",
                   "tambah": 0, "ubah": 1, "pesan": "OK"}],
    "terakhir": "2026-11-24 06:31:12"
  }
}
```

| Field | Keterangan |
|---|---|
| `sumber[]` | Semua kolom tabel `sumber`, terurut `plant, divisi` |
| `log[]` | 25 `ingest_log` terbaru (`ORDER BY id DESC`) |
| `karantina[]` | 25 `karantina` terbaru |
| `karantina_total` | Total karantina (semua waktu, semua sumber) |
| `flagged` | Jumlah kasus `flagged <> ''` |
| `kasus` | Jumlah kasus aktif (`terhapus = 0`) |
| `terhapus` | Jumlah kasus ditandai hilang dari sumber |
| `audit[]` | 20 `audit` terbaru |

---

## 9. Endpoint pendukung (halaman, QR, font, health)

| Endpoint | Perilaku |
|---|---|
| `GET /` | HTML TV (`tv.html`). Data via `GET /api/state` |
| `GET /admin` | HTML panel admin (`admin.html`). Data via `GET /api/admin` |
| `GET /s/<token>` | HTML landing sesi; **404** `"Sesi tidak berlaku"` bila token tidak ada di tabel `sesi` |
| `GET /qr/<token>.png` | PNG QR (`box_size=8, border=2`) berisi `https://<host>/s/<token>` |
| `GET /fonts/<nama>` | Berkas dari `docs/assets/fonts/` (mis. Kalam) |
| `GET /healthz` | `{"ok": true, "pengawas": <bool>}` |

---

## 10. Autentikasi (target) & header

**v1 (sekarang):** tanpa header auth; semua endpoint terbuka di jaringan.

**Aturan akses permukaan frontend (v1.1, 24 Nov 2026 — keputusan produk, "A-01/A-02"):**

| Permukaan | Siapa | Mekanisme |
|---|---|---|
| **Landing `/` (React, menu pilar + QR absensi)** | **Semua perangkat TV (TV Device)** | A-01 — **tampil di semua TV, tanpa login**; sumbernya `GET /api/state` + `GET /qr/<token>.png` (publik) |
| **Dashboard `/dashboard` (React)** | **PDCA** (semua plant) · **TL / Team Leader** (plant miliknya) | A-02 — **hanya untuk PDCA & TL terkait**; rute terproteksi di frontend (lihat `docs/FRONTEND_STRUCTURE.md` §5.1); menu disembunyikan untuk role lain, termasuk TV |
| `/api/state`, `/api/absensi`, `/api/konfirmasi`, `/qr/*.png`, `/s/<token>` | TV / sesi absensi / ponsel | Tetap publik di v1 (layar bersama + token sesi per shift) |
| `/api/admin`, `/api/buka`, `/api/sync`, `/admin` | Admin / IT / Supervisor | Publik di v1 — wajib dibatasi di v2/tahap C |

Penegakan A-02 **tidak** bisa dilakukan lewat kontrak ini di v1 (endpoint tetap publik); pembatasan sementara
ada di sisi UI/operasi (TV hanya membuka `/`; `/dashboard` tidak ditautkan; guard `RequireRole`). Penegakan
sesungguhnya menunggu **tahap C (MSAL Entra ID)**: JWT → klaim grup — `DMS-PDCA-*` (semua plant) vs
`DMS-TL-*` + klaim plant (plant sendiri); endpoint agregat lintas plant wajib menjawab **403** untuk TL (R-07).

**v2 (target produksi):**

| Endpoint | Auth |
|---|---|
| `GET /api/state`, `GET /s/<token>`, `GET /qr/<token>.png`, `GET /healthz` | Tidak wajib (layar bersama), boleh dibatasi IP/jaringan |
| `POST /api/absensi` | SSO (Entra ID) — siapa yang mengubah tercatat sebagai `pelaku` |
| `POST /api/konfirmasi` | SSO |
| `POST /api/buka` | SSO + peran Supervisor/DH/Admin |
| `POST /api/sync`, `GET /api/admin`, `/admin` | SSO + peran Admin/Supervisor |
| Halaman `/dashboard` (React) + endpoint agregat lintas plant | SSO + peran **PDCA** (semua plant) atau **TL** (plant di klaim token) — A-02; TL lintas plant → **403** (R-07) |

Rencana: frontend login via **MSAL** (Entra ID) → access token → header `Authorization: Bearer <token>` → backend verifikasi JWT (PyJWT + JWKS tenant). Token sesi QR kedaluwarsa per shift + dapat dicabut (R-82).

---

## 11. Ketidakkonsistenan & known gaps

| # | Temuan | Dampak | Rencana |
|---|---|---|---|
| 1 | Kunci error memakai `pesan`, bukan `error`/`message` | Frontend harus pakai `pesan` | Pertahankan di v1; v2 bisa distandarkan (`{ok, error: {code, message}}`) dengan masa transisi |
| 2 | `POST /api/absensi` tidak memvalidasi `nama`/`status` | Nama salah → 0 baris ter-update, respons tetap `ok:true` | Validasi + 400 di v2 |
| 3 | `POST /api/sync` selalu HTTP 200; kegagalan per item di `hasil[].ok:false` | Frontend wajib membaca per item | Dokumentasikan; v2 bisa 207/500 bila semua gagal |
| 4 | `POST /api/konfirmasi` boleh dipanggil berulang | Audit dobel | Idempotency check di v2 |
| 5 | Kegagalan server (exception) = 500 HTML, bukan JSON | Frontend perlu fallback parse | Error handler JSON di v2 |
| 6 | `field sesi` dari `sesi_aktif()` bisa **membuat sesi baru** saat dipanggil API state pertama kali | TV membuka sesi otomatis — disengaja | Tetap, tetapi catat di audit |
| 7 | `tanggal_tersedia` & baris kasus dibatasi (30 / 7) | Bukan bug; batas tampilan | Paginate bila diperlukan nanti |
| 8 | Tidak ada `Content-Type`/CORS handling khusus | Dev lintas origin gagal | Pakai proxy Vite (lihat `BACKEND_PLAN.md` §5) |
| 9 | Field `demo` di respons `true` hanya bila data historis | Banner MODE DEMO | Sesuai desain |
| 10 | `hitung` punya 7 kunci (`dinas luar` tidak dipakai chip TV) | — | Pertahankan |

---

## 12. Perubahan kontrak & versioning

- Kontrak ini **v1** (v1.1, 24 Nov 2026: **§10 ditambah aturan akses permukaan A-01/A-02** — landing untuk semua TV; Dashboard hanya PDCA/TL. **Tidak ada perubahan skema endpoint/field** — aditif, aman).
- Tambahan field baru bersifat aditif (aman); menghapus/mengubah nama field = **v2** dan wajib update frontend + dokumen ini.
- Frontend harus **defensif**: abaikan field yang tidak dikenal; siapkan fallback untuk nilai `"—"` dan array kosong.
- Setiap perubahan pada `app/server.py` yang menyentuh route/payload **wajib** menyertakan update `docs/API_CONTRACT.md` (checklist PR).
- Header versi kontrak opsional nanti: `X-DMS-Contract: v1`.

---

## 13. Contoh alur frontend

### 13.1 TV (polling 15 dtk)

```
GET /api/state?plant=Snack&line=*&demo=1
  → simpan state
  → render halaman sesuai idx; rotasi timer sesuai durasi
  → setiap aksi (ketuk chip / konfirmasi) → POST /api/… → fetch ulang state
```

### 13.2 Landing QR (ponsel)

```
GET /s/<token>  (HTML) atau data dari /api/state
  → tampilkan 3 langkah + status dikonfirmasi
  → klik KONFIRMASI → POST /api/konfirmasi {plant, line, pelaku:"QR sesi"}
  → reload
```

### 13.3 Panel admin

```
GET /api/admin (10 dtk) → kartu + tabel
tombol Sinkronkan sekarang → POST /api/sync {} → baca hasil[] → tampilkan ringkasan tambah/ubah
```

### 13.4 Kode warna cepat untuk grid KPI

```
st 0 → #1C3E8A (biru, sesuai target)
st 1 → #C22A26 (merah, di bawah target)
st 2 → #C22A26 (merah, lewat batas)
st 3 → #A9A9A2 (abu, belum diisi)
```

---

*Ditulis dari kode per 24 November 2026. Sumber kebenaran: `app/server.py`, `app/dms_core.py`.*
