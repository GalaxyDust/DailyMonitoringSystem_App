# DMS — TV Per Divisi, Satu Pintu QR, dan Integrasi Excel Otomatis

**Tanggal:** 6 November 2026 · **Status:** rancangan disetujui arahnya — 3 pertanyaan pokok sudah dijawab plant (§10); aturan R-80…R-90 sudah diterapkan
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
| 6 | Excel auto-update tanpa upload | Folder kerja dipindah ke OneDrive **sekali oleh IT**, junction di path lama; petugas cukup Ctrl+S | R-85, R-88 |
| 7 | Petugas jangan diribetkan | **Nol langkah tambahan**: tidak ada upload, ekspor, kirim lampiran, atau isi ulang di aplikasi | R-88 |
| 8 | Excel tetap dipakai terus | **Tidak dibekukan.** Yang dibagi adalah kepemilikan kolom, bukan waktu | R-89 |
| 9 | Tiap divisi punya Excel sendiri | Sinkron **per berkas** lewat registry; satu berkas gagal tidak menahan divisi lain | R-86 |

**Catatan sumber:** tiga workbook di `reference/` hanya memuat `Resume SHE`, `Resume QC`, dan
`Resume Prod` (`Summary DMS to KPI`: V=12 / O=5 / total 17). Menurut plant, **tiap divisi sudah punya
Excel sendiri** — jadi berkas Delivery dan Teknik cukup **didaftarkan** (R-86), bukan dibuat baru.
Contoh kedua berkas itu belum ada di repo; pemetaan kolomnya menyusul (§10).

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

**Delivery & Teknik** — berkas Excel-nya sudah ada di masing-masing divisi (R-86), tinggal
didaftarkan di registry §5.7. Kolomnya dipetakan seperti divisi lain; sementara menunggu contoh
berkas, halaman memakai kolom papan fisik: Delivery `PO · Plan (Unit) · Real (Unit) · Ach · MTD`;
Teknik `MTC Accuracy · Planning MTC · % Failure OEE · Energy Gas · Energy Listrik`.
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

### 5.1 Keadaan nyata: file ada di laptop petugas, tiap divisi punya Excel sendiri

**Tidak ada langkah tambahan untuk petugas.** Petugas tetap membuka file yang sama, di folder yang
sama, dan menekan **Ctrl+S** seperti biasa. Yang berubah hanya *di mana file itu benar-benar
berada* — dan itu dikerjakan **satu kali oleh IT**, bukan oleh petugas.

| Opsi | Cara kerja | Usaha petugas | Usaha IT | Latensi | Catatan |
|---|---|---|---|---|---|
| **1 · OneDrive + junction** ⭐ | Folder kerja dipindah **ke dalam** folder OneDrive; di lokasi lama dibuat *junction* agar path & shortcut tetap sama. OneDrive mengunggah sendiri di latar belakang → Graph/Power Automate membaca | **nol** (Ctrl+S saja) | 1× per laptop ±15 menit | 10–60 s | paling sedikit perawatan; sudah ada tenant M365 |
| **2 · Agen kecil di laptop** | Layanan Windows mengawasi folder; saat file selesai disimpan, dikirim ke API lewat HTTPS | **nol** | pasang & rawat agen di N laptop | 15–60 s | tanpa cloud; tapi N titik yang harus dirawat |
| **3 · Folder bersama + 1 pengawas** | File dipindah ke folder jaringan; petugas membuka lewat shortcut lama (mapped drive); satu pengawas di server | **nol** | pindah file + 1 server selalu hidup | 15–60 s | paling mudah dirawat tanpa cloud; butuh LAN/VPN |
| ~~4 · Kirim manual~~ | petugas unggah / kirim lampiran / ekspor CSV | **ada** | kecil | — | **ditolak** — melanggar R-88 |

**Rekomendasi: Opsi 1.** Alasannya: tidak ada aplikasi baru di laptop, tidak ada tombol baru, tidak
ada pelatihan baru, dan perawatan jangka panjang paling ringan. Opsi 2 dipakai bila kebijakan
melarang cloud; Opsi 3 bila laptop sering offline tetapi LAN selalu ada.

#### 5.1.1 Pemasangan satu kali oleh IT (bukan oleh petugas)

```bat
:: 1. Masuk ke OneDrive dengan akun kerja petugas (sudah ada di tenant garudafood365)
:: 2. Pindahkan folder kerja ke DALAM folder OneDrive
robocopy "D:\DMS" "%OneDriveCommercial%\DMS" /E /MOVE

:: 3. Buat junction di lokasi LAMA menunjuk ke folder OneDrive
::    -> shortcut, makro, dan kebiasaan petugas tetap jalan tanpa diubah
mklink /J "D:\DMS" "%OneDriveCommercial%\DMS"
```

**Arah junction penting dan tidak boleh dibalik.** Folder asli harus berada **di dalam** OneDrive,
lalu tautan dibuat **di luar** pada path lama. Kebalikannya — menaruh junction di dalam OneDrive yang
menunjuk ke folder luar — **tidak didukung Microsoft** dan tidak akan tersinkron. OneDrive juga tidak
bisa menyinkron folder jaringan/mapped drive. Karena itu langkah 2 (pindah) wajib mendahului langkah 3.

Setelah itu petugas **tidak melakukan apa pun yang baru**: buka file dari shortcut yang sama, isi,
simpan. OneDrive mengunggah otomatis; begitu laptop online, TV ikut terbarui.

#### 5.1.2 Dari cloud ke aplikasi

Setelah file berada di OneDrive/SharePoint, pemicunya memilih salah satu:

- **Microsoft Graph** — langganan perubahan (*webhook*) + *delta query* untuk mengejar yang terlewat
  saat layanan restart. Pakai **item ID** yang stabil, bukan path, supaya file di-*rename* tidak
  membuat sinkron putus. Pilihan untuk produksi.
- **Power Automate** — flow "file berubah" → HTTP POST ke API aplikasi. Paling cepat untuk pilot.

Keduanya menghasilkan **peristiwa yang sama** (`file_berubah`), jadi pipeline di §5.2 tidak berubah
bila pemicunya diganti. Opsi 2 dan 3 juga menghasilkan peristiwa yang sama.

> Bukti tenant M365 sudah dipakai: 831 sel PIC di `Resume SHE` EP berisi tautan
> `garudafood365.sharepoint.com`. Jadi Opsi 1 tidak menuntut pengadaan baru.

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

### 5.4 Excel tidak pernah dibekukan — pembagian kepemilikan kolom

**Keputusan: tidak ada cutover, tidak ada pembekuan.** Petugas terus memakai Excel selamanya dan
sistem terus menyinkron setiap saat. Supaya dua tempat ini tidak pernah saling menimpa, yang dibagi
bukan *waktu* melainkan **kolom**:

| Jenis kolom | Contoh | Pemilik | Di aplikasi |
|---|---|---|---|
| **Ada di Excel divisi itu** | Date, Shift, Line, LBN, Problem, RootCause, Action Plan, Due, PIC, Progress, Status, DT (min) | **Excel** | **baca-saja**, badge `Excel`; koreksi dilakukan di Excel, aplikasi menyusul otomatis |
| **Tidak ada di Excel** | absensi & konfirmasi sesi, jejak audit, eskalasi, tenggat & pengingat, foto tambahan, persetujuan, skor proses | **Aplikasi** | boleh diisi; tidak pernah dikirim balik ke Excel |

Karena tidak ada satu kolom pun yang ditulis di dua tempat, **tidak ada konflik** dan tidak perlu
masa transisi. Aplikasi tidak menambah kerja petugas: ia hanya **membaca** apa yang sudah dikerjakan,
lalu menambahkan hal yang memang tidak bisa dilakukan Excel (absensi, pengingat tenggat, eskalasi,
riwayat, laporan otomatis).

Konsekuensi yang harus dipegang:

1. Tombol "ubah angka" **tidak muncul** di aplikasi untuk kolom milik Excel (R-89). Yang muncul:
   **"Perbaiki di Excel"** + nama file dan barisnya, supaya petugas tahu ke mana harus pergi.
2. Bila aplikasi menemukan angka yang tampak salah (mis. PIC berisi URL), aplikasi **tidak menebak
   dan tidak mengubahnya** — hanya menandai dan memberi tahu.
3. Baris yang hilang dari Excel ditandai **"terhapus di sumber"**; riwayat tetap tersimpan (retensi ≥5 tahun).
4. Aplikasi **tidak pernah menulis** ke workbook. Sekali pun petugas meminta, jalurnya adalah
   laporan/peringatan, bukan sunting file.

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

### 5.7 Satu berkas per divisi — daftar sumber (registry)

Karena **tiap divisi sudah punya Excel sendiri**, sinkronisasi dilakukan **per berkas** dan saling
bebas: file Quality bermasalah tidak menahan halaman SHE.

| Kolom registry | Isi | Contoh |
|---|---|---|
| `sumber_id` | kunci tetap | `SN-L09-SHE` |
| `plant · line · divisi` | pemilik data | Snack · Line 9 · SHE |
| `lokasi` | path lama di laptop (untuk petunjuk "Perbaiki di Excel") | `D:\DMS\Resume SHE.xlsx` |
| `cloud_item_id` | ID OneDrive/SharePoint yang stabil walaupun file di-rename | `01ABC…` |
| `sheet · baris_header` | boleh `auto` — dicari dari nama kolom | `Resume SHE · auto` |
| `peta_kolom` | pemetaan kolom Excel → kolom model | §2.3 |
| `pemilik_akun` | akun kerja yang mengunggah | petugas SHE line 9 |
| `status` | aktif · berhenti · karantina | aktif |

Satu divisi boleh punya **lebih dari satu berkas** (mis. per line atau per shift); registry cukup
ditambah baris, aplikasi menggabungkan hasilnya per divisi.

### 5.8 Laptop mati atau offline — dibedakan dari "belum diisi"

Ini penting supaya orang tidak salah menuduh divisi belum bekerja:

| Keadaan | Yang tampil di TV | Yang dilakukan sistem |
|---|---|---|
| File belum tersentuh hari itu | **"belum diisi"** + nama penanggung jawab | tetap tampil, tidak dilewati (R-84) |
| Laptop mati / belum online | **"belum tersinkron · terakhir 07.12"** | angka terakhir tetap tampil dengan jamnya; antrean OneDrive menyusul saat online |
| Online tapi sinkron gagal | **"sinkron tertunda"** | coba ulang; 3× gagal → notifikasi Admin |
| File sedang dibuka di Excel | tidak ada tanda khusus | tunggu selesai disimpan (debounce), jangan baca file setengah jadi |

Tidak ada data yang hilang karena offline: OneDrive mengantre di laptop dan mengirim begitu jaringan
kembali; *delta query* mengejar semua versi yang terlewat.

---

## 6. Aturan baru (sudah diterapkan di `DMS_Aturan_Sistem_v1.md`)

| Kode | Isi ringkas |
|---|---|
| **R-80** | TV menampilkan **satu divisi per layar** dengan pager; bukan papan gabungan. Urutan & durasi diatur Admin. |
| **R-81** | **Absensi lebih dulu**: isian divisi tidak bisa dikirim sebelum kehadiran sesi dikonfirmasi; override Supervisor/DH beralasan & tercatat. |
| **R-82** | **QR sesi = satu pintu**: token terikat plant/line/tanggal/shift, berputar tiap shift, dapat dicabut; menulis wajib SSO. |
| **R-83** | Kolom TV & form **mengikuti kontrak kolom Excel** divisi itu; kolom baru masuk staging, tidak otomatis tampil. |
| **R-84** | Kolom statis, **baris & angka dinamis** per hari/shift; divisi tanpa data tetap tampil dengan status "belum diisi". |
| **R-85** | Integrasi Excel **satu arah, otomatis, terus-menerus**. Excel **tidak dibekukan**; aplikasi tidak pernah menulis ke workbook. |
| **R-86** | Tiap divisi memakai Excel-nya sendiri; sinkron **per berkas** lewat registry. Delivery & Teknik cukup didaftarkan, bukan dibuat baru. |
| **R-88** | **Nol langkah tambahan bagi petugas.** Dilarang meminta upload, ekspor, kirim lampiran, atau isi ulang data yang sudah ada di Excel. |
| **R-89** | **Kepemilikan kolom**: kolom yang ada di Excel bersifat baca-saja di aplikasi (koreksi di Excel); aplikasi hanya memiliki kolom yang tidak ada di Excel. |
| **R-90** | TV membedakan **"belum diisi"** dan **"belum tersinkron"** (laptop offline); angka terakhir tetap tampil dengan jamnya. |
| **R-87** | Setiap angka membawa **badge sumber** (Excel/Aplikasi) dan waktu sinkron terakhir. |

---

## 7. Dampak ke dokumen & model data

Perubahan pada empat dokumen di bawah **sudah diterapkan** pada versi ini.

| Dokumen | Perubahan |
|---|---|
| `DMS_Aturan_Sistem_v1` §5, §9, §10, §13, §14 | ✅ tambah R-80…R-90; R-55/R-59 disesuaikan; §14: 3 keputusan terbuka + 5 sudah diputuskan |
| `rancangan/02` §1, §5.2, §5.3, §5.7 | ✅ komponen ingest di arsitektur; TV per divisi; absensi sebagai gerbang; profil TV & sinkronisasi |
| `rancangan/03` §1, §8 | ✅ urutan harian: QR → absensi → divisi; alur TV per divisi |
| `DMS_Logic_Design` §9.8 | ✅ aturan TV: rotasi per divisi, penanda halaman, kolom kontrak, badge sumber |
| `DMS_Digitalisasi_v1.pptx` | ✅ 25 → 28 slide: slide 6–7 diperbarui; slide 24–26 baru (Quality & Produksi, QR, Ctrl+S→TV); slide 27 memuat 3 keputusan terbuka + kotak "sudah dijawab" |
| `docs/assets/mockup/` | ✅ `tv.png` (SHE), `tv_quality.png`, `tv_produksi.png`, `tv_absen.png` (absensi awal), `tv_qr.png` |

Entitas baru / tambahan:

```
sesi_dms      (id, plant, line, tanggal, shift, status, qr_token_id, dibuka_pada, dikunci_pada)
qr_token      (id, sesi_id, scope, kedaluwarsa, dicabut_pada, perangkat_id)
sumber_data   (id, jenis[excel|aplikasi], path, etag, sinkron_terakhir, status)
ingest_log    (id, sumber_id, mulai, selesai, tambah, ubah, karantina, pesan)
baris_asal    (kunci_baris, sidik_isi, sumber_id, sheet, baris_excel, catatan_id)
kolom_peta    (plant, sheet, kolom_excel, kolom_model, wajib, transformasi, pemilik[excel|app])
registry      (sumber_id, plant, line, divisi, path_lama, cloud_item_id, sheet, status, akun)
```

---

## 8. Rencana bertahap (masuk rencana 8 pekan)

| Pekan | Hasil | Bukti selesai |
|---|---|---|
| 1 | Kontrak kolom + pemetaan 3 sheet; parser tahan geser header; **IT memasang OneDrive+junction di 1 laptop** | parser membaca 3 workbook; petugas cukup Ctrl+S |
| 2 | Ingest jalan pada 1 plant, **per berkas divisi** | ubah 1 sel di Excel lalu Ctrl+S → TV berubah < 60 s **tanpa petugas buka aplikasi** |
| 3 | QR sesi + gerbang absensi | pindai → absensi → divisi terbuka; tanpa absensi tidak bisa kirim |
| 4–5 | TV per divisi (SHE, Quality, Produksi) + pager | 3 halaman detail, kolom sesuai Excel, data hari itu |
| 6 | Daftarkan berkas Delivery & Teknik + petakan kolomnya | 5 divisi lengkap dari Excel masing-masing |
| 7 | Panel sinkronisasi + karantina + badge sumber | gagal sinkron terlihat, bukan diam |
| 8 | Perluas ke semua laptop/divisi; **Excel tetap dipakai** | semua divisi tersinkron; tidak ada langkah upload di SOP mana pun |

---

## 9. Uji terima

1. Petugas mengubah satu sel `Resume Prod` di laptopnya lalu **Ctrl+S** — tidak membuka aplikasi,
   tidak mengunggah apa pun → angka di TV Produksi berubah ≤ 60 s dan tercatat di `ingest_log`.
1b. Shortcut lama (`D:\DMS\...`) masih membuka file yang sama setelah pemasangan junction.
2. File dibuka di Excel (terkunci) lalu disimpan → ingest tidak membaca file setengah jadi.
3. Kolom baru ditambahkan di Excel → tidak muncul di TV, masuk staging + notifikasi Admin.
4. Baris dihapus di Excel → kasus ditandai "terhapus di sumber", riwayat tetap ada.
5. Sesi baru dibuka → TV tampil **Absensi** lebih dulu; tombol kirim divisi terkunci.
6. Absensi dikonfirmasi → TV mulai rotasi SHE → Quality → Produksi → … dengan pager benar.
7. QR kedaluwarsa dipindai → pesan sesi ditutup, bukan form kosong.
8. Jaringan mati 10 menit → setelah hidup, *delta*/watcher mengejar semua perubahan (tidak ada baris hilang).
9. Divisi tanpa data hari itu → halaman tetap tampil "belum diisi", bukan dilewati.
10. Angka yang sama dilihat di TV, dasbor, dan laporan → identik, dengan badge sumber sama.
11. Kolom milik Excel tidak punya tombol ubah di aplikasi; yang muncul "Perbaiki di Excel" + nama berkas.
12. Laptop dimatikan 30 menit lalu dinyalakan → semua perubahan tersusul, tidak ada baris hilang;
    selama mati TV menulis "belum tersinkron", bukan "belum diisi".

---

## 10. Keputusan

**Sudah dijawab (6 Nov 2026):**

| # | Pertanyaan | Jawaban | Akibat pada rancangan |
|---|---|---|---|
| 1 | Di mana file Excel disimpan? | **masih di laptop petugas** | §5.1 Opsi 1: pindah folder ke OneDrive + junction di path lama, dikerjakan IT satu kali |
| 2 | Sumber Delivery & Teknik? | **tiap divisi sudah punya Excel sendiri** | tidak ada form baru; cukup daftarkan berkasnya di registry §5.7 (R-86) |
| 3 | Kapan Excel dibekukan? | **tidak dibekukan — sinkron terus setiap saat** | §5.4 kepemilikan kolom, bukan cutover (R-85, R-89) |

**Masih perlu dilengkapi (tidak menahan pembangunan):**

| # | Perlu | Untuk apa | Siapa |
|---|---|---|---|
| 1 | Contoh file Excel **Delivery** dan **Teknik** | memetakan kolomnya seperti §2.3 — tiga workbook di `reference/` hanya memuat SHE/QC/Prod | Kepala divisi terkait |
| 2 | Daftar laptop + path folder kerja tiap divisi | skrip pemasangan satu kali (§5.1.1) | IT plant |
| 3 | Kebijakan akun: akun kerja petugas atau akun layanan bersama | menentukan izin Graph dan kepemilikan berkas | IT + Admin DMS |
| 4 | Laptop yang sering offline / tidak boleh cloud | dipakai untuk memilih Opsi 2 atau 3 pada laptop itu saja | IT plant |

---

**Ringkas satu kalimat:** petugas tetap membuka Excel di folder yang sama dan menekan Ctrl+S —
IT hanya memindahkan folder itu ke OneDrive sekali dan meninggalkan junction di path lama; sistem
membaca setiap perubahan tanpa petugas mengunggah apa pun, Excel tetap dipakai selamanya, TV
menampilkan **satu divisi per layar** dengan kolom yang sama seperti Excel, dan semua orang masuk
lewat **satu QR sesi** yang meminta **absensi lebih dulu**.

**Rujukan teknis arah junction:** folder asli harus di dalam OneDrive, tautan di luar pada path lama;
kebalikannya tidak didukung Microsoft — <https://geekchamp.com/how-to-sync-any-folder-to-onedrive-on-windows/>
dan <https://www.itechguides.com/how-to-sync-any-folder-to-onedrive-on-windows/>.

