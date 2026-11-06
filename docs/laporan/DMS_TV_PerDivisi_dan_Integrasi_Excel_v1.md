# DMS — TV Per Divisi, Satu Pintu QR, dan Integrasi Excel Otomatis

**Tanggal:** 6 November 2026 · **Status:** usulan rancangan (menunggu 3 keputusan di §10)
**Pemicu:** permintaan agar tampilan TV tampil **satu divisi per layar** (lebih detail, kolom mengikuti
Excel), **absensi dikerjakan di awal sebelum DMS**, **QR sebagai satu pintu masuk**, dan **Excel tetap
diisi petugas seperti biasa tetapi sistem ikut terbarui otomatis tanpa upload**.

Dokumen ini melengkapi — bukan menggantikan — `DMS_Aturan_Sistem_v1.md`, `rancangan/02`, dan
`rancangan/03`. Nomor aturan baru diusulkan mulai **R-80** (R-78/R-79 sudah dipakai §12 Replikasi plant).

---

## 0. Ringkasan keputusan

| # | Permintaan | Keputusan rancangan | Aturan |
|---|---|---|---|
| 1 | TV tampil satu-satu per divisi | TV jadi **halaman berurutan**: 1 layar = 1 divisi, bukan papan gabungan 5 kolom | R-80 |
| 2 | Kolom mengikuti Excel | Kolom TV = **kontrak kolom** yang dipetakan dari sheet Excel divisi itu | R-83 |
| 3 | Dinamis, data beda tiap hari | Kolom tetap (kontrak), **baris & angka dinamis** per tanggal/shift; kosong ≠ hilang | R-84 |
| 4 | Absensi di awal sebelum DMS | Sesi DMS punya **gerbang absensi**: absensi terkonfirmasi dulu, baru isian divisi dibuka | R-81 |
| 5 | QR satu pintu, semua terintegrasi | **QR sesi** di TV/papan → satu URL → absensi → divisi → review → kunci | R-82 |
| 6 | Excel auto-update tanpa upload | **Ingest satu arah** dari tempat file disimpan (SharePoint/OneDrive atau folder jaringan) | R-85 |

**Temuan penting:** di workbook, `Template Penilaian → Summary DMS to KPI` hanya memuat **Safety,
Quality, Productivity** (rekap V=12 / O=5 / total 17). **Delivery dan Teknik tidak punya sheet sumber
di Excel** — keduanya hanya ada di papan fisik. Jadi halaman TV Delivery & Teknik perlu sumber baru
(lihat §2.4 dan R-86).

---

## 1. Apa yang sebenarnya ada di Excel

Dibaca langsung dari tiga workbook di `reference/` (read-only). Ketiga plant memakai skema kolom
yang sama; hanya posisi baris header berbeda.

| Sheet | Baris header | Isi | Dipakai untuk |
|---|---|---|---|
| `Resume SHE` | 17 | log kasus SHE + PICA + foto | halaman TV **SHE** |
| `Resume QC` | 19 | log kasus Quality + validasi QCP | halaman TV **Quality** |
| `Resume Prod` | 24 (NP: 25) | log kasus Produksi + `DT (min)` | halaman TV **Produksi** |
| `Template Penilaian` | 4–13 | checklist harian 7 item, bobot 10/20/10/10/10/20/20 = 100, kolom tanggal 1–31 | skor proses harian |
| `Template Penilaian` | 14–29 | `Summary DMS to KPI`: item per divisi, target, tanda **V/O** | grid KPI per divisi |
| `DMS_INDEX` | per blok | Bobot (A) 0,4 / 0,4 / 0,2 · Target (B) · Realisasi (C) · Ach (D) · Scoring (E) · Nilai | kepala halaman TV (index) |
| `Ach` | 2 | monitoring problem solving per week/area | tren penutupan |
| `Resume Snack/EP/NP` | 3+ | rekap manual open/close/occurrence | **tidak dipakai** (selisih dengan tabel, lihat Insight §8.4) |

### 1.1 Kolom `Resume SHE` (26 kolom)

`No · Month · Week · Date · Shift · Line · LBN Name · Location/Area · Category Safety ·
Category Problem · Picture Before · Problem Statement (What, Who, Where, Why, When) ·
RootCause (Min 3 Why – Standart 5 Why) · Action Plan · Due Date · PIC · Progress · Status ·
Running Day · OPL/WI · PM · AM · CRMO · Training · Occurrence or Recurrence · Picture After`

### 1.2 Kolom `Resume QC` (21 kolom)

`No · Month · Week · Tanggal · Shift · Line · LBN Name · Category · Priority Level · Problem ·
Validasi Hasil Pengecekan QCP · Root Cause · Action Plan · Due Date · PIC · Progress · Status ·
OPL/WI · PM · V (EP: AM) · CRMO · Case Category`

### 1.3 Kolom `Resume Prod` (22 kolom)

`No · Month · Week · Date · Shift · Line · LBN Name · Category · Priority Level · Problem ·
DT (min) · RootCause · Corrective or Preventive Action · Due Date · PIC · Progress · Status ·
OPL/WI · PM · AM · CRMO · Occurrence or Recurrence`

### 1.4 Item KPI per divisi (`Summary DMS to KPI`)

| Divisi | Item | Target | Jenis |
|---|---|---|---|
| Safety | KAK | Zero | V/O |
| Safety | PICA Safety – Completion Rate | 0,8 | V |
| Safety | KPI SHE INDEX | — | V |
| Quality | Defect Internal (Packing) | — | V/O |
| Quality | PICA Quality – Completion Rate | 0,8 | V/O |
| Quality | KPI PQI INDEX | — | V |
| Productivity | Yield RM E2E · Yield PM | — | V |
| Productivity | OFR0 (AVG, target ≤10%) | 98%–110% | V/O |
| Productivity | OEE · Man Power Standart | 1 (MP) | V |
| Productivity | PICA Productivity – Completion Rate | 0,8 | V/O |

**Artinya:** grid "target vs realisasi" di TV diambil dari blok ini + `DMS_INDEX`, sedangkan
tabel kasus di bawahnya diambil dari `Resume <divisi>`. Dua sumber, satu halaman.

---

## 2. TV per divisi — satu layar, satu divisi (R-80)

### 2.1 Prinsip

1. **Satu layar = satu divisi.** Tidak lagi lima kolom berdesakan. Font besar, kolom lengkap,
   terbaca dari 3–10 m.
2. **Bentuk tetap papan**: kepala papan, grid KPI, tabel kasus, baris PICA — seperti papan fisik,
   hanya saja fokus satu divisi.
3. **Kolom mengikuti Excel** (§2.3), bukan kolom karangan.
4. **TV tetap tanpa login & tanpa ketik** (R-56, R-58); interaksi hanya absensi.

### 2.2 Susunan satu halaman divisi

```
┌──────────────────────────────────────────────────────────────────────────┐
│ DMS · SNACK · LINE 9        SHE / SAFETY            Sen, 6 Nov 2026 · S1  │  ← kepala
│ Index divisi 3,4 · Kasus terbuka 4 · Lewat tenggat 1 · Hadir 25/28         │  ← ringkas
├──────────────────────────────────────────────────────────────────────────┤
│ KPI HARIAN      │ Target │  S1  │  S2  │  S3  │ Harian │ Sem │ Bulan      │  ← grid
│ KAK             │  Zero  │  0   │  0   │  0   │   0    │  0  │   0        │    (V/O)
│ PICA Completion │  0,80  │ 0,75 │  —   │  —   │  0,75  │ 0,8 │  0,82      │
│ SHE INDEX       │   —    │  V   │  —   │  —   │   V    │  V  │   V        │
├──────────────────────────────────────────────────────────────────────────┤
│ KASUS AKTIF (dari Resume SHE)                                            │  ← tabel
│ Tgl │ Shift │ LBN │ Area │ Kat. Safety │ Masalah │ Sebab │ Tindakan │ PIC │
│ Due │ Umur │ Progress │ Status │ Foto                                  │
├──────────────────────────────────────────────────────────────────────────┤
│ PICA TERBUKA · Problem & Rootcause │ Action │ PIC │ Due │ Status         │  ← kaki
├──────────────────────────────────────────────────────────────────────────┤
│ ● Sumber: Excel (sinkron 07.12) · Pembaruan 07.14      Halaman 2 / 6  ▮▮▯▯▯▯│  ← footer
└──────────────────────────────────────────────────────────────────────────┘
```

### 2.3 Kontrak kolom TV per divisi (Excel → layar)

Kolom Excel yang panjang dipadatkan di layar, tetapi **tetap satu makna** dan bisa dibuka
detailnya di dasbor. Urutan kolom di bawah adalah urutan tampil.

**SHE** — grid: KAK · PICA Completion · SHE INDEX
Tabel: `Date` · `Shift` · `LBN Name` · `Location/Area` · `Category Safety` · `Category Problem` ·
`Problem Statement` · `RootCause` · `Action Plan` · `Due Date` · `PIC` · `Running Day`→**Umur** ·
`Progress` · `Status` · `Picture Before/After`→**ikon foto** · `Occurrence/Recurrence`→**badge**

**Quality** — grid: Defect Internal (Packing) · PICA Completion · PQI INDEX
Tabel: `Tanggal` · `Shift` · `LBN Name` · `Category` · `Priority Level`→**badge** · `Problem` ·
`Validasi Hasil Pengecekan QCP` · `Root Cause` · `Action Plan` · `Due Date` · `PIC` · `Progress` ·
`Status` · `Case Category` · `OPL/WI · PM · V/AM · CRMO`→**4 ikon standar**

**Produksi** — grid: Yield RM E2E · Yield PM · OFR0 · OEE · Man Power Standart · PICA Completion
Tabel: `Date` · `Shift` · `LBN Name` · `Category` · `Priority Level` · `Problem` ·
**`DT (min)`** (ditonjolkan) · `RootCause` · `Corrective or Preventive Action` · `Due Date` · `PIC` ·
`Progress` · `Status` · `Occurrence/Recurrence` · ikon standar

**Delivery & Teknik** — belum ada sheet Excel (R-86). Halaman tetap disiapkan dengan kolom papan
fisik: Delivery `PO · Plan (Unit) · Real (Unit) · Ach · MTD`; Teknik `MTC Accuracy · Planning MTC ·
% Failure OEE · Energy Gas · Energy Listrik`. Sumber: form aplikasi **atau** sheet baru
`Resume Delivery` / `Resume Teknik` dengan kontrak kolom yang sama.

### 2.4 Urutan & rotasi

| Urutan | Halaman | Lama | Catatan |
|---|---|---|---|
| 1 | **Absensi** | 30 s (atau sampai terkonfirmasi) | **tampil pertama** saat sesi dibuka (R-81) |
| 2 | SHE | 25 s | |
| 3 | Quality | 25 s | |
| 4 | Produksi | 30 s | biasanya kasus terbanyak |
| 5 | Delivery | 20 s | bila sumber aktif |
| 6 | Teknik | 20 s | bila sumber aktif |
| 7 | Ringkasan / DMS Index | 20 s | penutup putaran |

- Semua durasi, urutan, dan halaman aktif **diatur Admin** (profil TV, R-57).
- **Pager wajib** (`Halaman 4/6` + titik) supaya orang tahu masih ada halaman lain.
- Halaman divisi tanpa data **tetap tampil** dengan pesan "belum ada isian hari ini" +
  siapa yang belum mengisi — tidak dilewati diam-diam (R-84).
- Bila tabel kasus lebih panjang dari layar: gulir per blok maksimal 2 sub-halaman, lalu lanjut
  divisi berikutnya. Angka ringkas di kepala tidak pernah terpotong.

### 2.5 Dinamis setiap hari (R-84)

| Unsur | Statis / dinamis | Sumber |
|---|---|---|
| Daftar kolom | **statis** (kontrak §2.3) | pemetaan sheet |
| Baris kasus | **dinamis** per tanggal & shift | `Resume <divisi>` |
| Item KPI & target | dinamis per versi target | master target + `Template Penilaian` |
| Angka index | dinamis | `DMS_INDEX` / mesin penilaian |
| Hadir / total | dinamis | catatan absensi sesi itu |
| Kolom baru di Excel | **tidak langsung tampil** → masuk staging + notifikasi Admin | ingest §5 |

---

## 3. Absensi di awal, sebelum DMS (R-81)

Sesi DMS punya status jelas dan **gerbang**:

```
DIBUKA ──► ABSENSI ──► ISI DIVISI ──► REVIEW ──► DIKUNCI
   │          │            │            │
   │          │            │            └─ semua divisi kirim + temuan disepakati
   │          │            └─ SHE · Quality · Produksi · Delivery · Teknik
   │          └─ konfirmasi hadir/tidak hadir (wajib selesai dulu)
   └─ dipicu QR / jadwal shift
```

Aturan:

1. Saat sesi dibuka (QR dipindai atau jadwal shift tiba), **TV otomatis pindah ke halaman Absensi**
   dan form divisi **belum bisa dikirim**.
2. Absensi selesai = tombol **"Konfirmasi kehadiran"** ditekan leader (atau otomatis saat semua
   nama punya status). Setelah itu halaman divisi terbuka dan TV mulai rotasi.
3. Status awal tetap **hadir** (R-32); lapangan hanya menandai yang tidak hadir. Shift yang tidak
   pernah dikonfirmasi sampai cut-off tetap **"belum dikonfirmasi"** (R-36).
4. **Override:** Supervisor/DH boleh membuka isian bila absensi tertunda, dengan alasan tercatat
   di audit. Berguna saat listrik/jaringan mati.
5. Absensi tetap bisa dari TV tanpa login (R-33) **atau** dari hasil pindai QR — menulis ke catatan
   yang sama, tidak ada dua rekap.
6. Setelah absensi dikonfirmasi, angkanya langsung menjadi penjelas output (R-37) di halaman Produksi.

---

## 4. QR satu pintu (R-82)

### 4.1 Isi QR

QR di TV/papan **bukan tautan permanen**. Isinya tautan sesi bertoken:

```
https://dms.<domain>/s/<token-sesi>
token mengikat: plant · line · tanggal · shift · sesi_id · kedaluwarsa
```

- **Berputar setiap shift** (dan bisa dicabut Admin). Token tidak memberi hak ubah angka lampau.
- TV memperoleh token lewat pairing perangkat (kode perangkat + token yang bisa dicabut, R-34).
- Bila token kedaluwarsa, halaman menampilkan "sesi sudah ditutup — minta QR terbaru di TV",
  bukan form kosong.

### 4.2 Alur satu pintu

```
Pindai QR di TV
      │
      ▼
Landing sesi: "DMS Snack · Line 9 · Shift 1 · 6 Nov" + status sesi
      │
      ├─ belum login ──► SSO/login sekali ──► kembali ke sesi (tidak kehilangan konteks)
      ▼
Langkah 1 · ABSENSI  (leader)  ── wajib selesai ──┐
      ▼                                          │
Langkah 2 · PILIH DIVISI (hanya divisi milikku)   │  semua langkah menulis
      ▼                                          │  ke sesi & catatan yang sama
Langkah 3 · ISI (kolom mengikuti Excel)           │
      ▼                                          │
Langkah 4 · REVIEW & KIRIM ───────────────────────┘
      ▼
Sesi terkunci · TV otomatis pindah dari Absensi ke rotasi divisi
```

**Satu pintu artinya:** tidak ada aplikasi terpisah untuk absensi, isian, PICA, atau laporan.
Semua peran masuk lewat tautan sesi yang sama; yang membedakan hanya **hak** (role/SSO), bukan
alamat aplikasi. Dasbor L1–L3 dan admin tetap di aplikasi yang sama.

### 4.3 Pengamanan

| Risiko | Penanganan |
|---|---|
| QR difoto & dipakai orang luar | token per shift + kedaluwarsa + wajib SSO untuk menulis |
| Token bocor | cabut dari Admin; dampak terbatas line & shift itu (R-34) |
| Absen berjamaah tidak sah | setiap ketukan tercatat waktu + perangkat (R-35); urungkan 2 menit |
| Spam pindai | rate limit per token/perangkat; audit semua percobaan |

---

## 5. Excel tetap diisi petugas, sistem auto-update — caranya (R-85)

Ini jawaban inti pertanyaan "bagaimana?". Prinsipnya: **jangan minta petugas upload. Datangi
file-nya di tempat ia sudah disimpan.** Sistem membaca **satu arah** (Excel → aplikasi); petugas
tidak berubah kebiasaan.

### 5.1 Tiga opsi teknis

| Opsi | Cara kerja | Latensi | Syarat | Effort | Risiko |
|---|---|---|---|---|---|
| **A. Microsoft Graph** (cloud) | File di **SharePoint/OneDrive**; layanan berlangganan perubahan (webhook) + *delta query* untuk mengejar yang terlewat | 10–60 s | File sudah/akan dipindah ke library M365; izin `Files.Read.All` (application) | sedang | webhook kedaluwarsa → perlu renew + delta sebagai jaring |
| **B. Power Automate** (no-code) | Flow "When a file is modified" di SharePoint → HTTP POST ke API aplikasi (atau langsung kirim isi tabel) | 5–60 s | Lisensi Power Automate; konektor Excel butuh data berbentuk **Table** | **kecil** | batas throttling; perlu akun service & connection yang tidak putus |
| **C. Folder + watcher** (on-prem) | File di folder jaringan (SMB) atau folder OneDrive yang disinkron ke server; agen pengawas folder membaca saat file selesai disimpan | 15–60 s | Server selalu hidup + akses baca ke folder | sedang | file terkunci saat dibuka Excel; butuh debounce |

**Rekomendasi:**
- **Pilot (pekan 1–3): opsi B** — paling cepat membuktikan "isi Excel → TV berubah tanpa upload".
- **Produksi: opsi A** — paling tahan lama, ada *delta* untuk mengejar saat layanan restart.
- **Tanpa cloud / jaringan tertutup: opsi C** — pipeline di dalamnya identik, hanya pemicunya beda.

Ketiganya menghasilkan **peristiwa yang sama** (`file_berubah`), jadi aplikasi tidak perlu tahu
opsi mana yang dipakai. Ini membuat pilihan bisa diganti tanpa membongkar aplikasi.

> Catatan: workbook EP sudah memuat tautan `garudafood365.sharepoint.com` di kolom PIC (831 sel),
> jadi lingkungan Microsoft 365 memang sudah dipakai — opsi A/B realistis.

### 5.2 Pipeline ingest (sama untuk semua opsi)

```
1. PICU        file_berubah(path, etag/modified)
2. DEBOUNCE    tunggu 5–10 s sampai penyimpanan selesai; lewati berkas kunci ~$*.xlsx
3. SNAPSHOT    salin berkas ke area baca (jangan baca file yang sedang ditulis)
4. PARSE       cari baris header berdasarkan NAMA kolom, bukan nomor baris
               (header SHE 17 · QC 19 · Prod 24/25 — sudah terbukti bergeser antar plant)
5. NORMALISASI tanggal (5 format) · status (close/open/kosong) · nama line (ws l02 ↔ 2)
               · PIC berupa URL → tandai "PIC tidak valid"
6. VALIDASI    kolom wajib ada? tipe cocok? tanggal masuk rentang sesi?
               gagal → karantina + notifikasi Admin, bukan dibuang diam-diam
7. UPSERT      idempoten per baris (kunci di §5.3); hitung tambah/ubah/hapus
8. TERBIT      peristiwa data_berubah → TV & dasbor menyegar (refresh 20–30 s)
```

### 5.3 Kunci idempoten (supaya tidak dobel)

Kolom `No` di Excel bisa dinomori ulang, jadi **jangan** dipakai sebagai kunci.

```
kunci_baris = hash(plant, sheet, tanggal, shift, line_norm, lbn_norm, problem_norm)
sidik_isi   = hash(seluruh kolom yang dipetakan)
```

- `kunci_baris` sama + `sidik_isi` beda → **perbarui** (dan catat di audit: sumber Excel).
- `kunci_baris` baru → **tambah**.
- Baris hilang dari Excel → **tandai terhapus di sumber**, jangan hapus permanen (retensi ≥5 th).
- Dua baris berkunci sama dalam satu sheet → masuk karantina "duplikat", Admin yang memutuskan.

### 5.4 Dua arah? Tidak — sampai cutover

Selama masa transisi ada dua tempat menulis (Excel & aplikasi). Supaya tidak saling menimpa:

| Fase | Excel | Aplikasi | Yang menang |
|---|---|---|---|
| 1 · Bayangan | ditulis petugas | hanya membaca | **Excel** |
| 2 · Sejajar | ditulis petugas | petugas juga isi di aplikasi | Excel untuk baris yang ada di Excel; aplikasi untuk baris baru, diberi badge sumber |
| 3 | dibekukan (read-only) per divisi | satu-satunya tempat menulis | **Aplikasi** |
| 4 | arsip | aplikasi | aplikasi |

Cutover **per divisi**, bukan serentak — mulai dari divisi yang paling siap. Setiap baris di TV dan
dasbor membawa **badge sumber** (`Excel` / `Aplikasi`) supaya jelas siapa yang terakhir mengubah.

### 5.5 Yang harus dibersihkan lebih dulu (dari verifikasi xlsx)

| Masalah | Bukti | Penanganan ingest |
|---|---|---|
| PIC berisi URL, bukan nama | 831 sel di `Resume SHE` EP | tandai `PIC tidak valid`, minta nama; jangan tebak |
| Nama line tidak seragam | `ws l02` vs `2`; `3&7`; `2,3,4,5,6,7,8` | tabel alias per plant; gabungan multi-line dipecah jadi relasi |
| Sel error rumus | 153 sel (`#VALUE!`, `#REF!`, `#DIV/0!`) | baca `data_only`; error → kosong + flagged |
| Ringkasan ≠ tabel | QC EP 993 vs 2.338 | **abaikan sheet rekap**, hitung dari baris kasus |
| Kolom beda antar plant | QC Snack/NP `V`, EP `AM` | pemetaan per plant, bukan satu peta global |

### 5.6 Panel status sinkronisasi (wajib ada)

Di Admin **dan** kecil di footer TV:

- per berkas: `nama · plant · sinkron terakhir · hasil (tambah/ubah) · durasi · status`
- tombol **"Sinkronkan sekarang"** (paksa satu putaran) & **"Lihat karantina"**
- peringatan bila tidak ada perubahan > N menit pada jam kerja, atau gagal 3× berturut
- TV tetap menampilkan **jam pembaruan terakhir** (R-60) + **sumber** (R-87)

---

## 6. Usulan aturan baru

| Kode | Isi ringkas |
|---|---|
| **R-80** | TV menampilkan **satu divisi per layar** dengan pager; bukan papan gabungan. Urutan & durasi diatur Admin. |
| **R-81** | **Absensi lebih dulu**: isian divisi tidak bisa dikirim sebelum kehadiran sesi dikonfirmasi; override Supervisor/DH beralasan & tercatat. |
| **R-82** | **QR sesi = satu pintu**: token terikat plant/line/tanggal/shift, berputar tiap shift, dapat dicabut; menulis wajib SSO. |
| **R-83** | Kolom TV & form **mengikuti kontrak kolom Excel** divisi itu; kolom baru masuk staging, tidak otomatis tampil. |
| **R-84** | Kolom statis, **baris & angka dinamis** per hari/shift; divisi tanpa data tetap tampil dengan status "belum diisi". |
| **R-85** | Integrasi Excel **satu arah & otomatis** (tanpa upload manual). Aplikasi tidak menulis ke workbook. |
| **R-86** | Delivery & Teknik perlu sumber data sendiri (form aplikasi atau sheet baru) karena tidak ada di workbook. |
| **R-87** | Setiap angka membawa **badge sumber** (Excel/Aplikasi) dan waktu sinkron terakhir. |

---

## 7. Dampak ke dokumen & model data

Perubahan pada empat dokumen di bawah **sudah diterapkan** pada versi ini.

| Dokumen | Perubahan |
|---|---|
| `DMS_Aturan_Sistem_v1` §5, §9, §10, §13, §14 | ✅ tambah R-80…R-87; R-55/R-59 disesuaikan; §14 jadi 6 keputusan |
| `rancangan/02` §1, §5.2, §5.3, §5.7 | ✅ komponen ingest di arsitektur; TV per divisi; absensi sebagai gerbang; profil TV & sinkronisasi |
| `rancangan/03` §1, §8 | ✅ urutan harian: QR → absensi → divisi; alur TV per divisi |
| `DMS_Logic_Design` §9.8 | ✅ aturan TV: rotasi per divisi, penanda halaman, kolom kontrak, badge sumber |
| `DMS_Digitalisasi_v1.pptx` | ✅ 25 → 28 slide: slide 6–7 diperbarui; slide 24–26 baru (Quality & Produksi, QR, sinkron Excel); slide 27 jadi 6 keputusan |
| `docs/assets/mockup/` | ✅ `tv.png` (SHE), `tv_quality.png`, `tv_produksi.png`, `tv_absen.png` (absensi awal), `tv_qr.png` |

Entitas baru / tambahan:

```
sesi_dms      (id, plant, line, tanggal, shift, status, qr_token_id, dibuka_pada, dikunci_pada)
qr_token      (id, sesi_id, scope, kedaluwarsa, dicabut_pada, perangkat_id)
sumber_data   (id, jenis[excel|aplikasi], path, etag, sinkron_terakhir, status)
ingest_log    (id, sumber_id, mulai, selesai, tambah, ubah, karantina, pesan)
baris_asal    (kunci_baris, sidik_isi, sumber_id, sheet, baris_excel, catatan_id)
kolom_peta    (plant, sheet, kolom_excel, kolom_model, wajib, transformasi)
```

---

## 8. Rencana bertahap (masuk rencana 8 pekan)

| Pekan | Hasil | Bukti selesai |
|---|---|---|
| 1 | Kontrak kolom + pemetaan 3 sheet; parser tahan geser header | parser membaca 3 workbook, hasil = `data_plants.json` |
| 2 | Ingest opsi B/C jalan pada 1 plant | ubah 1 sel di Excel → TV berubah < 60 s **tanpa upload** |
| 3 | QR sesi + gerbang absensi | pindai → absensi → divisi terbuka; tanpa absensi tidak bisa kirim |
| 4–5 | TV per divisi (SHE, Quality, Produksi) + pager | 3 halaman detail, kolom sesuai Excel, data hari itu |
| 6 | Delivery & Teknik (sumber baru) | 5 divisi lengkap |
| 7 | Panel sinkronisasi + karantina + badge sumber | gagal sinkron terlihat, bukan diam |
| 8 | Cutover divisi pertama; Excel dibekukan per divisi | satu divisi 100% dari aplikasi |

---

## 9. Uji terima

1. Petugas mengubah satu sel `Resume Prod`, **tidak menekan tombol apa pun** di aplikasi →
   angka di TV Produksi berubah ≤ 60 s dan tercatat di `ingest_log`.
2. File dibuka di Excel (terkunci) lalu disimpan → ingest tidak membaca file setengah jadi.
3. Kolom baru ditambahkan di Excel → tidak muncul di TV, masuk staging + notifikasi Admin.
4. Baris dihapus di Excel → kasus ditandai "terhapus di sumber", riwayat tetap ada.
5. Sesi baru dibuka → TV tampil **Absensi** lebih dulu; tombol kirim divisi terkunci.
6. Absensi dikonfirmasi → TV mulai rotasi SHE → Quality → Produksi → … dengan pager benar.
7. QR kedaluwarsa dipindai → pesan sesi ditutup, bukan form kosong.
8. Jaringan mati 10 menit → setelah hidup, *delta*/watcher mengejar semua perubahan (tidak ada baris hilang).
9. Divisi tanpa data hari itu → halaman tetap tampil "belum diisi", bukan dilewati.
10. Angka yang sama dilihat di TV, dasbor, dan laporan → identik, dengan badge sumber sama.

---

## 10. Keputusan yang perlu dijawab

| # | Pertanyaan | Pilihan | Rekomendasi |
|---|---|---|---|
| 1 | **Di mana file Excel disimpan sekarang?** | SharePoint/OneDrive M365 · folder jaringan (SMB) · laptop petugas | SharePoint/OneDrive → opsi A/B; kalau masih di laptop, pindahkan dulu ke library bersama |
| 2 | Delivery & Teknik: sumber datanya? | form aplikasi · sheet Excel baru | form aplikasi (tidak menambah kerja rekap) |
| 3 | Kapan Excel dibekukan per divisi? | setelah 2 pekan sejajar · setelah gerbang G4 | setelah 2 pekan sejajar per divisi |

---

**Ringkas satu kalimat:** petugas tetap mengisi Excel seperti biasa; sebuah layanan membaca file
itu di tempat ia disimpan dan memperbarui basis data, TV menampilkan **satu divisi per layar**
dengan kolom yang sama seperti Excel, dan semua orang masuk lewat **satu QR sesi** yang meminta
**absensi lebih dulu** sebelum isian DMS dibuka.
