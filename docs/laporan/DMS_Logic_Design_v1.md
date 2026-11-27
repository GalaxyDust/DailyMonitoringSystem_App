# Digitalisasi DMS — Dokumen Logika & Desain v1

**Plant pilot:** Snack (BU.E — Factory 10 & Factory 30)
**Sumber acuan:** `docs/reference/12. Konsep Penilaian DMS Snack Des 24.xlsx`
**Status:** draft untuk diskusi — belum ada implementasi kode
**Tanggal:** 29 Oktober 2026

> **Status dokumen (5 Nov 2026):** sebagian digantikan oleh paket rancangan 5 November
> (`DMS_Aturan_Sistem_v1.md` + `docs/laporan/rancangan/01–03`). Bila bertentangan, **paket 5 Nov menang**.
> Yang tetap berlaku dari dokumen ini: pembongkaran rumus Excel (§3), katalog insight (§7,
> dengan penyesuaian), dan analisis migrasi (§12). Angka baseline di bawah adalah **Snack saja,
> definisi lama**; angka kanonik tiga plant ada di `DMS_Insight_xlsx_ke_Aplikasi.md` §8
> (17.201 kasus · 3.220 tanpa sebab · 53 overdue · 729 pola berulang).

---

## 0. Ringkasan satu halaman

Aplikasi ini **bukan** pemindahan Excel ke web. Nilai utamanya ada di tiga hal yang tidak dimiliki Excel:

1. **Angka yang tidak bisa "diatur"** — denominator, penilaian objektif, dan penutupan kasus dihitung/dikunci sistem.
2. **Insight otomatis** — aplikasi mendeteksi masalah (aging, recurrence, standardisasi gagal) dan mengusulkan tindakan.
3. **Satu sumber angka** untuk form, dashboard manajemen, dan display TV lantai produksi.

Baseline yang menjadi titik tolak (dari workbook asli):

| Ukuran | Nilai |
|---|---|
| Total kasus historis | **5.817** (SHE 1.185 · QC 1.520 · Prod 3.112) |
| Kasus ditutup tanpa root cause | **973** |
| Kasus berulang yang tetap dilabeli "Occurrence" | **849 dari 902 (94%)** |
| Kasus lewat due date masih Open | **22** (tertua 1.045 hari) |
| PIC kasus produktivitas = Teknik/Tekpro | **99,7%** |
| Kategori kasus = Machine | **99,8%** |
| Prioritas = High | **~100%** |

---

## 1. Konteks & keputusan yang sudah dikunci

| # | Keputusan | Alasan / bukti |
|---|---|---|
| 1 | ~~2 role~~ → **10 role** (Aturan §2.1) + kanal TV | Keputusan 2 role digantikan 5 Nov 2026; TV boleh menerima ketukan absensi (Absensi TV/QR/Web) |
| 2 | Hierarki **Group → Plant → Factory/BU → Line** | Satu plant Snack sudah punya Factory 10 (QC/Prod) dan Factory 30 (SHE) |
| 3 | Template **core wajib + KPI tambahan plant**, versioned | Ditemukan 3 versi checklist berbeda (7 / 6 / 5 item) |
| 4 | **Skor proses** → KPI orang; **skor hasil** → monitoring | 99,7% PIC kasus adalah Teknik, bukan leader |
| 5 | Pekan = **ISO week** | `Sheet1` & kolom Week cocok ISO 98,4–98,6% |
| 6 | Hari wajib = **Senin–Jumat − hari libur** | Data: 18 dari 21 hari kerja Mei 2026 terisi, nol Sabtu/Minggu |
| 7 | KPI harian = **V/O biner**; Ach = V/(V+O) | Keputusan bisnis |
| 8 | Recurrence **dideteksi otomatis**, bukan input manual | Field manual 94% salah |
| 9 | Close wajib: root cause + action + bukti + approval | 973 kasus ditutup tanpa root cause |
| 10 | Healthy Check = parameter editable + `effective_date` | Nilai konstan 0,8 → kontribusi tetap 0,6 |
| 11 | TV = **profil tampilan** yang diatur Admin | Jumlah kartu, jenis insight, refresh, jam aktif |
| 12 | Pilot = **Snack** | Seluruh data di workbook adalah Snack |
| 13 | Skala audit = **menengah** (laporan manajemen, bukan HR) | Keputusan bisnis: bukan penilaian personalia formal |
| 14 | Pensiunkan `Sheet1`, `IIAA Snack`, `Ach`, `Template Penilaian` (hidden) | Duplikat / kosong / arsip |

---

## 2. Baseline data — hasil audit workbook

### 2.1 Volume & cakupan

| Sheet | Baris terkurasi | Baris mentah | Rentang tanggal | Catatan |
|---|---|---|---|---|
| `Resume SHE` | 527 | 658 | 2023-01-30 → 2025-12-23 | **Dua tabel ditumpuk** |
| `Resume QC` | 1.520 | — | 2023-08-01 → 2026-10-21 | Normal |
| `Resume Prod` | 3.112 | — | 2023-08-02 → 2026-10-21 | Normal |
| `IIAA Snack` | 120 | — | 2024–2026 | Duplikat, 100% Close |

> **Temuan kritis:** `Resume SHE` baris 18–544 = data terkurasi (bernomor); baris 545–1202 = dump mentah (timestamp berjam, format Google Forms). Di blok kedua: `Status` kosong 647/658, `Week` kosong 100%, `Occurrence/Recurrence` kosong 100%. Artinya dashboard PICA Safety **75,4%** hanya menghitung blok lama; 658 kasus 2025 tidak masuk hitungan.

### 2.2 Kualitas data per sheet

| Field | SHE | QC | Prod |
|---|---|---|---|
| Root cause terisi | **0%** (blok 1) | 79% | 78% |
| Due date terisi | **0%** (blok 1) | 100% | 99% |
| Action plan terisi | 28% | 100% | 100% |
| Picture before/after | **0%** | — | — |
| Case category terisi | 16% | 100% | 100% |
| Progress terisi | 0% | 0% | 0% |
| Close tanpa root cause | — | **320** | **653** |

### 2.3 Distribusi & pola

| Dimensi | Temuan |
|---|---|
| Line | Pilus L1 / Line 9 mendominasi (Prod 3.014 dari 3.112) |
| Kategori | Machine 99,8% (Prod) |
| PIC | Teknik/Tekpro 99,7% (Prod) |
| Prioritas | High ~100% → field tidak lagi membedakan |
| Recurrence tercatat | 4,0% (Prod) — padahal **26,2%** kasus berpola berulang |
| Pasangan (LBN + problem) berulang ≥3× | **184 pola**, mencakup **816 kasus** |
| Top pola | `M03 BCAT` 15× · `SVB13 BCAT` 14× · `MHM39 LSTR` 13× · `SVB19 LSTR` 13× · `M39 LSTR` 12× |
| Prefix mesin | `MHM` 26,8% · `BCAT` 14,1% · `LSTR` 9,5% · `pecah` 9,1% |
| Downtime (Prod) | median **50 menit**/kasus, total **208.848 menit** |
| Standardisasi (OPL/PM/AM/CRMO) | dominan `O` = 88–98% → pencegahan hampir tidak pernah didokumentasikan |

### 2.4 Inkonsistensi master data (harus dibersihkan sebelum impor)

| Jenis | Contoh |
|---|---|
| Nama line | `Pilus L1` 2.815 · `Pilus L01` 169 · `pilus L1` 16 · `PILUS` 5 · `Pellet L1` / `Pelet L1` / `Pellet L01` |
| PIC | `Teknik` 2.038 · `teknik` 771 · `tekpro` 215 · `Tekpro` 78 · `Teknic` |
| Kategori | `Machine` vs `Machine ` (spasi) · `Hlgh` / `HIgh` |
| Label kasus | `Ocurrence` (18×) vs `Occurrence` |
| Tanggal | 10 nilai berupa teks: `13/03/2025`, `11//2025`, `\xa09/2/2024` |
| Plant bocor | 1 entri **"Prosesing Dairy"** di sheet Snack |

---

## 3. Dekonstruksi logic Excel → logic aplikasi

### 3.1 Lima lapis

| Lapis | Di Excel | Di aplikasi |
|---|---|---|
| 1. Referensi | `Sheet1`, `Guideline Score Daily` | Master kalender ISO, line, shift, kategori, PIC, band skor |
| 2. Input | kolom tanggal `Template Rev01`, tabel `Resume *` | Form meeting harian + form kasus |
| 3. Agregasi | `AVERAGEIF` per pekan, `SUM` per bulan | Engine agregasi multi-grain (hari/pekan/bulan/YTD) |
| 4. Skoring | `IF(Ach>=120%,5, …)` | Band skor dari config, versioned |
| 5. Index | `=G5*C5+…` (KPI 0,4 · Checklist 0,4 · Healthy 0,2) | Weighted score engine + target gap |

### 3.2 Rumus asli (disederhanakan)

```
nilai_harian = Σ (skor_item/10 × bobot_item)/100          → 0..1
ach_pekan    = AVERAGEIF(pekan) / target(0,8)
skor         = 1..5 menurut band 90/100/110/120%
nilai_param  = skor × bobot_param
DMS Index    = Σ nilai_param                               → target 3, max 5
```

### 3.3 Rumus final aplikasi

```
// ---------- MEETING HARIAN ----------
bobot_item   = [10, 20, 10, 20, 20, 20]     // config, sum = 100
skor_item    = 0 | 5 | 8 | 10                // rubric config
nilai_harian = Σ (skor_item/10 × bobot_item)/100             → 0..1

// item 1 & 2 dihitung sistem, bukan manusia:
item1 = on_time(jam_mulai, jam_selesai, toleransi = 10 menit)
item2 = kelengkapan_form(tabel_wajib_terisi)

// ---------- KPI HARIAN (V/O) ----------
ach_kpi_harian = jumlah_V / (jumlah_V + jumlah_O)   // N/A dikeluarkan dari penyebut

// ---------- PEKAN ----------
penyebut      = jumlah_hari_kerja − hari_libur      // BUKAN jumlah hari terisi
ach_checklist = Σ nilai_harian / (penyebut × target)
ach_kpi       = Σ ach_kpi_harian / (penyebut × target)

// ---------- SKOR (band config, bandingkan pada 2 desimal) ----------
skor = 5 if ach ≥ 1.20
     = 4 if ach ≥ 1.10
     = 3 if ach ≥ 1.00
     = 2 if ach ≥ 0.90
     = 1 if ach <  0.90

// ---------- INDEX ----------
nilai_param = skor × bobot_param            // 0,4 / 0,4 / 0,2
DMS Index   = Σ nilai_param                 // target 3, max 5
```

### 3.4 Pengaruh perubahan rumus (contoh nyata)

| Skenario | Excel | Aplikasi |
|---|---|---|
| 5 hari wajib, hanya 1 hari diisi (skor sempurna) | Ach 125% → **skor 5** | 1/(5×0,8)=25% → **skor 1** |
| 0,88/0,80 | `1,0999999999999999` → **skor 3** | dibulatkan 1,10 → **skor 4** |
| 0,89/0,80 | 1,1125 → skor 4 | skor 4 (sama) |

> Di Excel, **tidak mengisi lebih menguntungkan daripada mengisi jelek**. Ini yang dibalik aplikasi.

---

## 4. Sembilan cacat logic Excel & perbaikannya

| # | Cacat | Bukti | Perbaikan |
|---|---|---|---|
| 1 | `AVERAGEIF` mengabaikan sel kosong | Line mengisi 1 hari → Ach 125% | Denominator = hari kerja − libur |
| 2 | Skor objektif dinilai manusia | Item on-time & kelengkapan (bobot 30) | Dihitung sistem |
| 3 | 6 item → 1 angka | `I11` hanya total | Simpan skor per item |
| 4 | Healthy Check konstan | realisasi 0,8 = target 0,8 | Parameter editable |
| 5 | Recurrence manual | 849/902 salah label | Deteksi otomatis |
| 6 | Close tanpa bukti | 973 kasus | Gate close |
| 7 | Kasus tidak terhubung ke checklist | Item 5 & 6 dinilai manual | Skor dihitung dari data kasus |
| 8 | Tidak ada dimensi waktu | Tak ada aging/trend | Aging, trend, lead indicator |
| 9 | Ambang tanpa pembulatan | 1,0999 → skor 3 | Bandingkan 2 desimal |

---

## 5. Arsitektur informasi

### 5.1 Hierarki

```
Group
 └── Plant            : Dairy · Exist · New · Snack
      └── Factory/BU  : Factory 10 (QC+Prod) · Factory 30 (SHE)
           └── Line   : Pilus L1 (9) · Pellet L1 (10) · Line A–F
```

Kode stabil: `SN`, `EP`, `NP`, `DR` (Kode Tetap). Kode `PLT-*` pada draft awal tidak dipakai. Nama tampilan boleh berubah.

### 5.2 Entitas inti

> Model kanonik: rancangan/02 §3 (papan per shift + 5 divisi). Tabel di bawah model awal
> meeting harian; `meeting`/`kpi_check` kini menjadi item ritme harian pada tab Produksi.

| Entitas | Isi | Kunci |
|---|---|---|
| `plant` · `factory` · `line` | master lokasi | kode stabil, `plant_id` wajib di semua transaksi |
| `user` · `role_scope` | user + cakupan plant | user bisa punya banyak plant |
| `meeting` | tanggal, line, leader, jam mulai/selesai | unique (line, tanggal) |
| `meeting_score` | 6 skor item + catatan | per meeting |
| `kpi_check` | 15 item V/O/N-A | per meeting |
| `case` | masalah, root cause, action, PIC, due date, status, bukti | `discipline` (safety/quality/productivity) |
| `case_stage` | OPL/WI → PM → AM → CRMO → close | state machine |
| `insight` | hasil rule engine + status tindak lanjut | rule_code, periode |
| `assessment_config` | bobot, band, target, hari wajib | `effective_date` |
| `audit_log` | before/after + alasan | semua tabel sensitif |

### 5.3 Satu tabel kasus, bukan tiga

| Aspek | SHE | QC | Prod |
|---|---|---|---|
| Kolom identitas (No, Month, Week, Date, Shift, Line, LBN) | ✅ | ✅ | ✅ |
| Kategori + prioritas | ✅ | ✅ | ✅ |
| Problem · root cause · action · due date · PIC · status | ✅ | ✅ | ✅ |
| OPL/WI · PM · AM · CRMO · Occurrence | ✅ | ✅ | ✅ |
| **Khusus** | Location/Area · Category Safety · Running Day · Picture | Validasi QCP | DT (min) |

→ Satu tabel `case` + `discipline` + kolom kondisional. Menghindari laporan ganda antar sheet.

---

## 6. Role & akses

> Matriks di bawah adalah model 2 role (draft awal). Matriks kanonik 10 role: `DMS_Aturan_Sistem_v1.md` §2.2.

| Kemampuan | User | Admin Plant | Admin Group | TV |
|---|---|---|---|---|
| Isi form meeting | ✅ line sendiri | ✅ | ✅ | ❌ |
| Buat / update kasus | ✅ miliknya | ✅ | ✅ | ❌ |
| **Close kasus** | ⚠️ *ajukan* | ✅ approve | ✅ | ❌ |
| Dashboard | ✅ plant sendiri | ✅ plant | ✅ semua | ❌ |
| Ubah bobot/rubrik/target | ❌ | ✅ plant | ✅ group | ❌ |
| Master data & user | ❌ | ✅ | ✅ | ❌ |
| Audit log | ❌ | ✅ | ✅ | ❌ |
| Kelola profil TV | ❌ | ✅ | ✅ | ✅ read-only |

**Setiap query wajib ter-filter `plant_id`** — ini pencegahan kebocoran data antar plant yang paling sering terlewat.

---

## 7. Katalog insight (14 aturan; **12 aktif sebagai kartu**)

> **Kanonik (deck hal. 18):** kartu temuan = **I-01…I-12**. I-13 dan I-14 pensiun dari kartu
> dan menjadi **pemeriksaan mutu data Admin** (kelengkapan = Kelengkapan Terukur; PIC non-controllable =
> pemisahan skor proses/hasil, Skor Proses & Hasil). I-12 dijalankan sebagai **peringatan rule-based sederhana**
> (PICA lemah + kasus baru naik), bukan model prediksi statistik — sesuai larangan analitik
> prediktif fase 1 (rancangan/01 §6). Fase Insight mengaktifkan **I-01…I-08 lebih dulu**
> (diperiksa G3), lalu I-09…I-12 sebelum fase Display.

### 7.1 Format baku setiap insight

```
TEMUAN      : satu kalimat
BUKTI       : angka + periode + sumber
SEBAB       : kenapa terjadi
DAMPAK      : akibat bila dibiarkan
REKOMENDASI : tindakan konkret
PEMILIK     : siapa yang bertindak
```

### 7.2 Daftar aturan

| Kode | Trigger | Contoh output | Kanal |
|---|---|---|---|
| I-01 | Hari kerja tanpa meeting | "Line 10 tidak DMS 3 hari berturut — compliance pekan 60%" | L1, TV |
| I-02 | Due date lewat + Open | "22 kasus lewat due date, tertua 1.045 hari" | TV, L1 |
| I-03 | Signature (line, mesin/LBN, kategori sebab) sama ≥3× / 90 hari (Temuan Berulang) | "M03 BCAT 15× di Pilus L1 — recurrence tersembunyi" | TV, L2 |
| I-04 | Recurrence + root cause identik | "Ditutup dengan Correction yang sama 4× → naikkan Preventive" | L2 |
| I-05 | Close tapi OPL/PM/AM/CRMO = O | "Close tanpa standardisasi — 88–98% tidak di-institutionalize" | L2, L3 |
| I-06 | Close tanpa root cause / bukti | "973 kasus ditutup tanpa akar masalah" | Admin |
| I-07 | >80% prioritas High | "Field prioritas tidak lagi membedakan" | Admin |
| I-08 | Ach dalam 1% di bawah band | "Kurang 0,1% dari band 4 — rawan salah hitung" | Admin |
| I-09 | 3 periode menurun berturut | "Checklist turun 3 pekan (slope −4%/pekan)" | L2, L3 |
| I-10 | Satu line/mesin >20% kasus | "Pilus L1 = 90% kasus; MHM 26,8%" | L3 |
| I-11 | DT besar × frekuensi tinggi | "MHM38: 7×, median DT 50 menit" | L2 |
| I-12 | PICA lemah + kasus baru naik | "PICA lemah pekan ini → prediksi lonjakan pekan depan" | L3 |
| I-13 | Field wajib kosong >10% — **pensiun dari kartu → pemeriksaan Admin (Kelengkapan Terukur)** | "Kelengkapan data line ini 78% — insight tidak bisa dipercaya" | Admin |
| I-14 | KPI non-controllable dinilai ke leader — **pensiun dari kartu → skor proses/hasil (Skor Proses & Hasil)** | "99,7% PIC = Teknik → bukan KPI leader" | Admin |

### 7.3 Peringkat tampil

```
prioritas = dampak (1–3) × volume × kebaruan × (controllable ? 1 : 0,5)
```

Ditampilkan **maksimal 3** di TV & dashboard L1 (dapat diubah Admin). Sisanya di daftar lengkap.

---

## 8. Kanal tampilan

### 8.1 Prinsip

| Kanal | Untuk | Prinsip desain |
|---|---|---|
| Form | Leader/DH saat rapat | **< 5 menit**, satu layar, autosave |
| Dashboard L1 | Supervisor | hari ini, sedikit angka, aksi |
| Dashboard L2 | Admin/Manager | tren, semua angka bisa drill-down |
| Dashboard L3 | Plant head | 1 angka + 3 kartu, tanpa scroll |
| TV | Lantai produksi | terbaca 3–10 m, tanpa interaksi, rotasi |

### 8.2 Prinsip yang tidak boleh dilanggar

1. **Setiap angka bisa diklik sampai baris penyebabnya** (index → parameter → hari → item → kasus).
2. **Setiap insight punya PIC & due date** — kalau tidak, ia berhenti jadi insight dan menjadi keluhan.
3. **TV bukan dashboard yang diperbesar** — punya tata letak sendiri.
4. **Tidak ada layar kosong** — bila gagal memuat, tampilkan snapshot terakhir + timestamp.

---

## 9. Wireframe tekstual

> Bentuk kanonik adalah **papan per shift** (rancangan/02 §5.1), bukan meeting harian.
> Wireframe §9.2–9.3 di bawah adalah model awal; **V/O kini diturunkan sistem dari status sel,
> tidak diketik tangan** (rancangan/02 §6.1).

### 9.1 User — Beranda (hari ini)

```
┌──────────────────────────────────────────────────────────────┐
│ DMS · PILUS L1 (Line 9)            Kam, 29 Okt 2026  14:32   │
├──────────────────────────────────────────────────────────────┤
│ [ ⏱ MULAI MEETING ]     status: BELUM DIMULAI               │
├──────────────────────────────────────────────────────────────┤
│ Tugas saya hari ini                                          │
│  • Isi 6 checklist meeting            → belum                │
│  • 3 kasus menunggu update            → lihat                │
│  • 1 kasus lewat due date (7 hari)    → tindak lanjuti       │
├──────────────────────────────────────────────────────────────┤
│ Insight untuk line saya                                      │
│  🔴 M03 BCAT muncul 3× bulan ini — cek Preventive Action     │
│  🟠 2 kasus close tanpa bukti — lengkapi dokumentasi         │
└──────────────────────────────────────────────────────────────┘
```

### 9.2 User — Form Meeting (satu layar, < 5 menit)

```
┌──────────────────────────────────────────────────────────────┐
│ Meeting Harian · 29 Okt 2026 · Pilus L1                      │
│ Leader: [dropdown]      Mulai: 07:00  Selesai: 07:08  ✅ On-time
├──────────────────────────────────────────────────────────────┤
│ A. CHECKLIST (6 item)                                        │
│ 1. On time .................... (otomatis: nilai 10)         │
│ 2. Kelengkapan form ........... (otomatis: 3/4 sheet = 5)    │
│ 3. Peserta aktif .......... [0] [5] [8] [10]   📝catatan*    │
│ 4. Leader menjalankan tugas [0] [5] [8] [10]   📝catatan*    │
│ 5. PICA lengkap ............ [0] [5] [8] [10]   📝catatan*   │
│ 6. Action direview ......... [0] [5] [8] [10]   📝catatan*   │
│    *) wajib bila skor < 8                                    │
├──────────────────────────────────────────────────────────────┤
│ B. KPI (V/O/N-A)  — 15 item, grid 3 kolom                    │
│ Safety      KAK [V][O][N/A]  PICA Safety [V][O][N/A]  …      │
│ Quality     Defect Packing [V][O][N/A]  …                    │
│ Productivity OEE [V][O][N/A]  Yield RM [V][O][N/A]  …        │
│ Energy      Gas Engine [V][O][N/A]  …                        │
├──────────────────────────────────────────────────────────────┤
│ [ + MASALAH BARU ]                    [ SIMPAN DRAFT ]        │
└──────────────────────────────────────────────────────────────┘
```

### 9.3 User — Form Kasus (ringkas, 30 detik)

```
Problem*        : ______________________  (wajib)
Kategori*       : [Machine|Material|Method|Man|Environment]
Prioritas*      : [High|Medium|Low]   (default Medium, bukan High)
LBN / Mesin*    : [dropdown + kode mesin]
Root cause*     : ______________________ (min. 1 baris, 5-Why menyusul)
Action*         : ______________________
PIC*            : [dropdown]
Due date*       : [tanggal]
Foto bukti      : [📷 kamera]
[ SIMPAN & LANJUTKAN DETAIL 5-WHY ]
```

### 9.4 User — Kasus Saya

```
┌──────────────────────────────────────────────────────────────┐
│ Kasus Saya (12)                    [Semua|Open|Overdue]      │
├──────┬─────────────────┬────────┬───────┬────────┬───────────┤
│ ID   │ Problem         │ PIC    │ Due   │ Aging  │ Status    │
│ C-081│ M03 BCAT        │ Teknik │ 27/10 │ 🔴 +2h │ Open      │
│ C-079│ MHM39 LSTR      │ Teknik │ 05/11 │ 🟢 7h  │ In review │
├──────────────────────────────────────────────────────────────┤
│ Detail → 5-Why · Action · Bukti · Riwayat · [AJUKAN CLOSE]   │
└──────────────────────────────────────────────────────────────┘
```

### 9.5 Admin — Review & Approve

```
┌──────────────────────────────────────────────────────────────┐
│ Persetujuan (hari ini)                                       │
├──────────────────────────────────────────────────────────────┤
│ Menunggu close: 5   Ditolak: 1   Perlu bukti: 3              │
├──────────────────────────────────────────────────────────────┤
│ C-076  M03 BCAT   root cause ✅  action ✅  bukti ❌          │
│        → [Minta bukti]  [Tolak]  [Setujui]                   │
│ C-072  MHM38 LSTR root cause ✅  action ✅  bukti ✅          │
│        ⚠️ recurrence ke-7 → wajib Preventive Action          │
│        → [Setujui dengan syarat]  [Tolak]                    │
└──────────────────────────────────────────────────────────────┘
```

### 9.6 Admin — Pengaturan Penilaian (versioned)

```
┌──────────────────────────────────────────────────────────────┐
│ Konfigurasi Penilaian · berlaku mulai [ 01/11/2026 ]         │
├──────────────────────────────────────────────────────────────┤
│ Bobot checklist    [10][20][10][20][20][20]  Σ = 100          │
│ Band skor          ≥120%→5  ≥110%→4  ≥100%→3  ≥90%→2  <90%→1 │
│ Target Ach pekan   [0,8]                                     │
│ Healthy Check      nilai [0,8]  bobot [0,2]  mode [konstan]  │
│ Bobot index        KPI [0,4]  Checklist [0,4]  Healthy [0,2] │
│ Target DMS Index   [3]                                       │
│ Hari wajib         Sen–Jum (Hari Kerja Senin–Jumat, tetap — tidak diedit)      │
│ Kalender libur     [ + tambah tanggal ]                      │
│ Window recurrence  [90] hari    Ambang aging [30] hari       │
├──────────────────────────────────────────────────────────────┤
│ Simulasi: index akan turun 0,20 → 3,20 (dari data 30 hari)   │
│                                  [ BATAL ]  [ SIMPAN VERSI ] │
└──────────────────────────────────────────────────────────────┘
```

### 9.7 Admin — Kelola Display TV

```
┌──────────────────────────────────────────────────────────────┐
│ Profil Display · [TV Frying]                    [Preview]    │
├──────────────────────────────────────────────────────────────┤
│ Plant/Line     [Snack / Factory 10 / Pilus L1]               │
│ Jumlah kartu   [3]         Rotasi [20] detik                 │
│ Refresh        [30] detik   Jam aktif [06:00]–[22:00]        │
│ Jenis insight  ☑ I-01 ☑ I-02 ☑ I-03 ☐ I-05 ☐ I-10            │
│ Urutan         [index] [meeting] [insight] [pareto]          │
│ Ambang warna   hijau ≥[90]%  kuning ≥[75]%  merah <[75]%     │
│ Token akses    [••••••] [Salin] [Cabut]                      │
└──────────────────────────────────────────────────────────────┘
```

### 9.8 TV Display — 1920×1080 · satu divisi per layar (Satu Divisi per Layar)

```
┌───────────────────────────────────────────────────────────────┐
│ DMS FACTORY 10 — PILUS L1        Kam, 29 Okt 2026  14:32:10   │
├──────────────────────────────┬────────────────────────────────┤
│  DMS INDEX HARI INI         │   STATUS MEETING                │
│         3,40  ▲             │   ✅ Line 9   selesai 07:12     │
│      TARGET 3,00            │   ⏳ Line 10  belum mulai       │
│  ████████████░░ (gauge)     │   ⚠ Frying   telat 25 menit    │
├──────────────────────────────┴────────────────────────────────┤
│ KASUS TERBUKA: 142   AGING >30 HARI: 37   RECURRENCE: 5,3%    │
├───────────────────────────────────────────────────────────────┤
│ PERLU TINDAKAN (halaman Ringkasan, akhir putaran)             │
│ 🔴 MHM38 BCAT — 7× dalam 60 hari — PIC Teknik — sisa 4 hari   │
│ 🟠 PICA Safety 75,4% < 90% — 37 kasus lewat due date          │
│ 🟡 Checklist "PICA" skor < 8 tiga hari berturut               │
└───────────────────────────────────────────────────────────────┘
```

Aturan TV:

| Aturan | Nilai |
|---|---|
| Font teks isi | ≥ 40 px |
| Font angka hero | ≥ 120 px |
| Refresh | 20–30 detik, snapshot (kesegaran ≤ 30 detik — rancangan/02 §7) |
| Rotasi halaman | Absensi (saat sesi dibuka) → SHE → Quality → Produksi → Delivery → Teknik → Ringkasan; 20–30 s/halaman (Rotasi TV) |
| Penanda halaman | wajib `Halaman n/N` + titik, supaya jelas masih ada divisi lain |
| Kolom tabel | mengikuti kontrak kolom Excel divisi itu (Kolom Ikuti Kontrak Excel); kolom baru → staging |
| Isi dinamis | kolom tetap, baris & angka per tanggal/shift (Kolom Statis, Isi Dinamis); divisi kosong tetap tampil |
| Sumber & sinkron | badge `Excel`/`Aplikasi` + jam sinkron terakhir di footer (Angka Bersumber) |
| Laptop offline | "belum tersinkron · terakhir hh.mm" — dibedakan dari "belum diisi" (Status Berkas Jujur) |
| Warna | hanya 3 status; tanpa gradasi |
| Anti burn-in | panel bergulir, posisi jam digeser |
| Gagal memuat | snapshot terakhir + timestamp |
| Interaksi | tidak ada, kecuali panel absensi (Absensi TV/QR/Web, TV Tanpa Login) |

Rincian susunan halaman per divisi, pemetaan kolom Excel→layar, dan alur QR satu pintu:
`DMS_TV_PerDivisi_dan_Integrasi_Excel_v1.md` §2–§5.

Yang **tidak** ditampilkan di TV: ranking individu/PIC, angka mentah panjang, KPI di luar wewenang lantai.

---

## 10. Dashboard — 3 level

| Level | Audiens | Isi | Contoh kartu |
|---|---|---|---|
| **L1 Ops** | Leader, Supervisor | status meeting, index hari ini, open & aging | "3 line belum DMS", "22 kasus overdue" |
| **L2 Analitik** | Admin, Manager | tren pekan/bulan, recurrence, Pareto, per line/PIC | "Recurrence 26,2% vs 4,0% tercatat" |
| **L3 Eksekutif** | Plant head | 1 angka + 3 insight | "Index 3,40 · 2 di bawah target" |

---

## 11. Konfigurasi yang dapat diedit Admin

| Parameter | Default | Editable | Versioned |
|---|---|---|---|
| Bobot 6 checklist | 10/20/10/20/20/20 | ✅ | ✅ |
| Band skor | 90/100/110/120% | ✅ | ✅ |
| Target Ach pekan | 0,8 | ✅ | ✅ |
| Healthy Check (nilai & bobot) | 0,8 · 0,2 | ✅ | ✅ |
| Bobot index | 0,4/0,4/0,2 | ✅ | ✅ |
| Target DMS Index | 3 | ✅ | ✅ |
| Hari wajib | Sen–Jum (Hari Kerja Senin–Jumat, tidak editable) | ❌ | — |
| Kalender libur | nasional + cuti bersama | ✅ | ✅ |
| Ambang aging | 30 hari | ✅ | ✅ |
| Window recurrence | 90 hari | ✅ | ✅ |
| Profil TV | 3 kartu · rotasi 20s · refresh 30s | ✅ | — |

> **Healthy Check:** karena nilainya konstan, bobot 0,2 berfungsi sebagai **lantai index**. Admin harus melihat **simulasi dampak** sebelum menyimpan, bukan angka tersembunyi.

---

## 12. Data & migrasi

### 12.1 Pemetaan sheet

| Sheet Excel | Nasib | Modul |
|---|---|---|
| `Sheet1` | **Pensiun** — 100% ISO, cukup fungsi tanggal | Master kalender |
| `Guideline Score Daily` | Config rubric, versioned | Pengaturan penilaian |
| `Template Penilaian` (hidden) | Arsip, jangan migrasi | — |
| `Template Penilaian, Rev01` | Form meeting harian | Form |
| `Resume SHE/QC/Prod` | Tabel kasus tunggal | Kasus & Insight |
| `Resume Snack` | Dashboard analitik otomatis | Dashboard L2 |
| `IIAA Snack` | Tidak dimigrasi — duplikat, 100% Close | — |
| `Ach` | Tidak dimigrasi — semua 0 | — |
| `Indah Z` | Arsip — versi 5 item | — |

### 12.2 Urutan impor (wajib berurutan)

1. **Bersihkan master** (line, PIC, kategori, prioritas) — normalisasi 5 varian nama line, 4 varian PIC, spasi/kapital.
2. **Pisahkan blok SHE** — baris 18–544 (terkurasi) vs 545–1202 (mentah).
3. **Lengkapi field wajib blok SHE mentah** — status, kategori, occurrence (dilakukan manual oleh SHE).
4. **Impor kasus** dengan `plant_id`, `factory_id`, `line_id` hasil mapping.
5. **Tandai kasus historis** sebagai `legacy = true` → dikecualikan dari aturan I-06/I-13 agar tidak membanjiri insight.
6. **Reprocess recurrence** otomatis → bandingkan dengan label lama (untuk laporan selisih 4,0% vs 26,2%).

### 12.3 Risiko migrasi

| Risiko | Mitigasi |
|---|---|
| 973 close tanpa root cause masuk sebagai "valid" | flag `legacy` + laporan kualitas data terpisah |
| Tanggal teks gagal parse | daftar 10 nilai disimpan untuk koreksi manual |
| Duplikat kasus antar sheet | de-dup berdasarkan (tanggal, LBN, problem) sebelum impor |
| Plant lain bocor (Dairy) | validasi `plant_id` saat impor |

---

## 13. Non-fungsional

| Aspek | Ketentuan |
|---|---|
| Audit trail | semua perubahan skor/kasus/config: siapa, kapan, before→after, alasan |
| Period lock | periode yang sudah dilaporkan tidak dapat diedit; koreksi = adjustment beralasan |
| Snapshot | laporan terkirim tidak berubah retroaktif |
| Offline resilience | autosave per field; antrian sinkron untuk sinyal lemah |
| Akses TV | token per perangkat: baca papan + tulis absensi shift berjalan (Absensi Shift Berjalan); dapat dicabut |
| Retensi | kasus & catatan ≥ 5 tahun; foto bukti ≥ 5 tahun mengikuti kasusnya (keputusan 5 Nov, lihat rancangan/02 §7) |
| Bahasa | Indonesia; istilah teknis (`Occurrence`, `OPL/WI`) dipertahankan |

---

## 14. Roadmap pilot Snack

| Fase | Isi | Keluaran | Estimasi |
|---|---|---|---|
| **0. Fondasi** | master data bersih, config versioned, auth & scope | database terisi, login siap | 2 pekan |
| **1. Capture** | form meeting + form kasus + approve | 5 line Snack mengisi harian | 3 pekan |
| **2. Measure** | engine skor + dashboard L1 | index harian akurat | 2 pekan |
| **3. Insight** | 8 aturan pertama (I-01…I-08); I-13/I-14 menjadi pemeriksaan Admin | kartu insight di L1 | 2 pekan |
| **4. Display** | TV + profil display | 1 TV di area Pilus L1 | 1 pekan |
| **5. Analitik** | L2 + L3 + ekspor laporan | laporan manajemen otomatis | 2 pekan |
| **6. Generalisasi** | template plant + rollout Exist → New → Dairy (Urutan Replikasi) | multi-plant | setelah pilot stabil |

Kriteria keberhasilan pilot (terukur) — **kanonik: 5 ukuran di rancangan/01 §4.2** (hari terisi, sebab lengkap, tenggat tercatat, overdue, pola berulang). Tabel di bawah adalah draft awal; "insight ditindaklanjuti" menjadi ukuran tambahan, bukan gerbang.

| Metrik | Target 8 pekan |
|---|---|
| Kepatuhan isi form | ≥ 90% hari kerja |
| Kelengkapan root cause | ≥ 95% |
| Kasus overdue | turun 50% |
| Recurrence terdeteksi & ditindak | 100% pola ≥3× punya action |
| Insight ditindaklanjuti | ≥ 70% |

---

## 15. Asumsi & risiko

| # | Asumsi | Bila salah |
|---|---|---|
| 1 | Disiplin meeting harian di Snack masih berjalan | Pilot mengukur "belum dipakai", bukan "berhasil" |
| 2 | Definisi V/O dapat disepakati per item | Ach KPI jadi perdebatan tiap rapat |
| 3 | Hari libur dapat dipelihara Admin | Skor turun tidak adil pada hari libur |
| 4 | Teknik/Maintenance bersedia jadi PIC di sistem | 99,7% kasus tetap tanpa pemilik |
| 5 | Angka tidak dipakai untuk sanksi personalia | Orang akan mengisi asal → data rusak lagi |

---

## 16. Decision log

| # | Keputusan | Status | Pemilik |
|---|---|---|---|
| 1 | ~~2 role + kanal TV~~ → 10 role (Aturan §2.1); TV boleh absensi | 🔁 digantikan 5 Nov | bisnis |
| 2 | Hierarki 4 lapis | ✅ | bisnis |
| 3 | Template core + KPI plant | ✅ | Production |
| 4 | Skor proses vs skor hasil | ✅ | Production + HR |
| 5 | Pekan ISO | ✅ | data |
| 6 | Hari wajib Sen–Jum − libur | ✅ | Production |
| 7 | KPI V/O biner | ✅ | bisnis |
| 8 | Recurrence otomatis | ✅ | data |
| 9 | Gate close | ✅ | QC/SHE |
| 10 | Healthy Check editable | ✅ | Admin |
| 11 | TV = profil editable | ✅ | Admin |
| 12 | Pilot Snack | ✅ | bisnis |
| 13 | Skala audit menengah | ✅ | bisnis |
| 14 | Sheet yang dipensiunkan | ✅ | IT |
| 15 | Kalender libur: master tahunan per plant, dipelihara Admin | ✅ 5 Nov | Admin |
| 16 | Item KPI bisa N/A (Status N/A); N/A ditetapkan di konfigurasi item, bukan diketik | ✅ 5 Nov | Production |
| 17 | Data historis diimpor dengan flag legacy; kasus legacy tidak naik ke TV/eskalasi | ✅ 5 Nov | bisnis |

---

## 17. Pertanyaan terbuka

1. **Kalender libur** — master tahunan (Admin isi sekali setahun) atau input manual per tanggal?
2. **Item KPI N/A** — apakah item yang tidak relevan (mis. Gas Engine di line tanpa gas engine) boleh berstatus N/A dan keluar dari penyebut?
3. **Impor historis** — setuju impor 5.817 kasus dengan flag `legacy` (dikecualikan dari aturan kualitas data)?
4. **PIC lintas fungsi** — apakah Teknik/Maintenance mendapat akun & KPI sendiri, mengingat 99,7% kasus adalah milik mereka?
5. **Retensi data** — berapa tahun sebelum diarsipkan?

---

*Dokumen ini adalah acuan diskusi. Belum ada implementasi kode. Setiap perubahan pada dokumen ini dicatat pada decision log di atas.*
