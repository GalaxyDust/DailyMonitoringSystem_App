# 02 · Rancangan Aplikasi DMS Digital

**Dokumen:** bagian 2 dari 3 rancangan aplikasi Daily Monitoring System (DMS)
**Status:** rancangan untuk dibangun — belum ada implementasi kode
**Tanggal:** 5 November 2026

> Sebelum membaca ini: [`01-KENAPA-DMS-DIGITAL.md`](01-KENAPA-DMS-DIGITAL.md) (alasan & tujuan) →
> file ini (bentuk aplikasi) → [`03-ALUR-SISTEM.md`](03-ALUR-SISTEM.md) (alur kerja).
> Aturan baku: [`DMS_Aturan_Sistem_v1.md`](../DMS_Aturan_Sistem_v1.md).

---

## 0. Ringkasan

**Satu aplikasi web, tiga wajah, satu basis data.**

| Wajah | Alamat | Perangkat | Untuk | Hak |
|---|---|---|---|---|
| **Papan lantai** | `/tv/<kode-tv>` | TV area produksi | semua orang di area | lihat papan + ketuk absensi |
| **Isi papan** | `/isi/<plant>/<line>` | tablet / PC line | leader, petugas divisi | isi catatan, absensi, buka kasus |
| **Kantor** | `/app` | PC | supervisor, DH, plant head, admin | dasbor, kasus, laporan, aturan |

Bukan tiga aplikasi: satu basis kode, satu login sistem, satu sumber angka. Yang berbeda hanya
tata letak, hak, dan perangkat.

---

## 1. Arsitektur

```mermaid
flowchart TB
    subgraph Klien["Perangkat di lapangan & kantor"]
        TV["TV lantai<br/>(tanpa login, terikat kode perangkat)"]
        TAB["Tablet / PC line<br/>(login leader & petugas divisi)"]
        PC["PC supervisor / DH / plant head"]
        ADM["PC admin plant & group"]
    end

    subgraph App["Aplikasi web DMS (satu basis kode)"]
        UI["Antarmuka: papan, isian, dasbor, kasus, laporan, admin"]
        API["API aplikasi<br/>(validasi, hak akses, audit)"]
        RULE["Mesin aturan<br/>insight · tenggat · eskalasi · kelengkapan"]
        JOB["Penjadwal<br/>(cut-off shift, kunci periode, snapshot TV)"]
        SYNC["Layanan sinkron Excel<br/>(baca satu arah · tanpa upload)"]
    end

    subgraph Data["Data"]
        DB[("Basis data relasional<br/>satu catatan per sel")]
        FILE[("Penyimpanan berkas<br/>foto bukti, lampiran")]
        AUD[("Jejak audit<br/>siapa · kapan · sebelum-sesudah")]
    end

    subgraph Luar["Sistem terkait"]
        ABS["Mesin absensi / jadwal shift<br/>(impor file)"]
        XLS["Workbook historis<br/>(17.201 kasus)"]
        XLSL["Workbook harian petugas<br/>(SharePoint/OneDrive atau folder)"]
        GRP["Group Manufacturing<br/>(laporan & perbandingan)"]
    end

    TV --> UI
    TAB --> UI
    PC --> UI
    ADM --> UI
    UI --> API
    API --> RULE
    API --> DB
    API --> FILE
    API --> AUD
    JOB --> RULE
    JOB --> DB
    API -->|ekspor| GRP
    ABS -.impor.-> API
    XLS -.impor sekali.-> API
    XLSL -.->|file berubah| SYNC
    SYNC -->|normalisasi + upsert| API
```

Prinsip arsitektur:

1. **Baca dan tulis lewat satu API.** Tidak ada tabel ringkasan yang ditulis tangan.
2. **TV tidak menyimpan logika.** TV menerima tampilan siap-tampil (snapshot) + mengirim ketukan absensi.
3. **Semua aturan waktu di penjadwal**, bukan di kepala orang: cut-off shift, kunci periode, tenggat, eskalasi.
4. **Audit di lapisan API**, bukan di aplikasi klien, supaya tidak bisa dilewati.
5. **Berkas (foto/dokumen) dipisah dari basis data**, hanya metadatanya yang masuk DB.
6. **Excel didatangi, bukan diunggah.** Layanan sinkron membaca workbook di tempat petugas
   menyimpannya (webhook/delta Microsoft Graph, Power Automate, atau pengawas folder), lalu
   menormalkan dan menyimpan idempoten. Aplikasi tidak pernah menulis ke workbook (R-85).
   Detail: `DMS_TV_PerDivisi_dan_Integrasi_Excel_v1.md` §5.

---

## 2. Peta modul (tujuh layar + dua pendukung)

| # | Modul | Layar | Fungsi inti | Halaman deck |
|---|---|---|---|---|
| 1 | **Isi papan** | `/isi/...` | tab divisi, sel papan, sebab, bukti, absensi, kirim bagian | 5 |
| 2 | **Papan lantai** | `/tv/...` | satu divisi per layar, rotasi Absensi → 5 divisi → ringkasan | 6, 24–25 |
| 3 | **Absensi** | panel di TV & isian | konfirmasi hadir, urungkan, rekap shift | 7 |
| 4 | **Dasbor L1–L3** | `/app/dasbor` | kartu KPI, tren, temuan berperingkat, daftar kerja | 8 |
| 5 | **Detail kasus** | `/app/kasus/:kode` | riwayat, empat kolom wajib, PICA, lampiran, dampak | 9 |
| 6 | **Laporan & KPI** | `/app/laporan` | skor proses vs hasil, KPI V/O, ekspor | 10 |
| 7 | **Admin** | `/admin` | target per versi, profil TV, kunci periode, jejak audit | 11 |
| 8 | *Masuk & peran* | `/masuk` | login, sesi, ganti plant (bila berhak) | — |
| 9 | *Notifikasi* | lonceng | temuan baru, tenggat dekat, approval menunggu | — |

Navigasi kantor (sidebar): **Hari ini · Kasus terbuka · Tren pekan · Perbandingan plant · Laporan & KPI · Pengaturan**.

---

## 3. Model data

### 3.1 Entitas inti

| Entitas | Isi pokok | Kunci aturan |
|---|---|---|
| `plant` | kode (SN/EP/NP/DR), nama, zona waktu, kalender libur | R-02, R-05 |
| `bu_factory` | unit di plant (mis. Factory 10) | R-02 |
| `line` | kode (SN-L09), nama seragam, plant, BU | R-06 (satu ejaan) |
| `mesin` | kode, nama, line, jenis | dipakai Teknik |
| `divisi` | SHE, Quality, Produksi, Teknik, Delivery; urutan, warna, ikon | R-11 |
| `item` | nama, divisi, satuan, target, jenis isian, ritme, boleh-diisi-leader, **arah** (higher-better / lower-better / exact), **berlaku per line** (`item_line`: aktif/N-A per line) | R-13, R-24, R-73 |
| `catatan` | **satu baris per sel**: line + tanggal + shift + item + nilai + status; UNIQUE(line, tanggal, shift, item) | R-01, R-04 |
| `shift` | pola per plant: kode, jam mulai–selesai, lintas tengah malam (shift 3 milik **tanggal mulai**) | R-04, R-26, R-34 |
| `kalender_libur` | tanggal libur per plant per tahun, dipelihara Admin | R-05 |
| `temuan` | hasil mesin aturan: rule_code (I-01…I-12), periode, bukti, PIC, tenggat, status tindak lanjut | R-47, R-48, R-69 |
| `pm_jadwal` | mesin, periode, item PM, PIC; status: selesai · tertunda(+alasan) · belum waktunya | R-19 |
| `spare_part` | part kritis per mesin, stok minimum, stok, rencana pengadaan | R-20 |
| `alat_ukur` | alat QC, kalibrasi terakhir, jatuh tempo, sertifikat; jatuh tempo → angka QC ditandai | R-21 |
| `po` | nomor PO, line, plan vs real, keterlambatan (sumber item Delivery per PO) | R-24 |
| `healthy_check` | nilai per plant per periode, diisi Admin, konstan dalam periode | R-28 |
| `kasus` | kode, plant, line, mesin, divisi, dampak A/B/C, sebab, tindakan, PIC, bukti, tenggat, status | R-45–R-50 |
| `pica` | kasus, tahap why-1..why-5, temuan, tindakan pencegahan | R-48 |
| `work_order` | kasus, kategori sebab (5 pilihan), komponen, teknisi, mulai/selesai | R-15–R-18 |
| `absensi` | tanggal, shift, line, orang, status, waktu ketuk, perangkat | R-31–R-39 |
| `orang` | nama, NIK opsional, regu, divisi, line utama | R-31 |
| `pengguna` | akun, peran, plant, line yang boleh diakses | R-07–R-10 |
| `target_versi` | plant, periode berlaku, target & bobot per item | R-51–R-54 |
| `profil_tv` | kode perangkat + token (bisa dicabut), cakupan **satu line atau grup line** (untuk plant berline banyak, R-59), pilar tampil, rotasi, mode | R-55–R-61 |
| `koreksi` | catatan/kasus, nilai lama, nilai baru, alasan, penyetuju | R-40–R-44 |
| `audit` | aktor, aksi, entitas, sebelum, sesudah, waktu, perangkat | R-53 |

### 3.2 Relasi

```mermaid
erDiagram
    PLANT ||--o{ LINE : punya
    LINE ||--o{ MESIN : punya
    DIVISI ||--o{ ITEM : memiliki
    LINE ||--o{ CATATAN : dicatat
    ITEM ||--o{ CATATAN : "satu sel"
    CATATAN ||--o| KASUS : "memicu bila di luar target"
    KASUS ||--o| PICA : "wajib bila berulang"
    KASUS ||--o| WORK_ORDER : "bila sebab teknis"
    LINE ||--o{ ABSENSI : "per shift"
    ORANG ||--o{ ABSENSI : "status hadir"
    PLANT ||--o{ TARGET_VERSI : "berlaku per periode"
    PLANT ||--o{ PROFIL_TV : "layar lantai"
    PENGGUNA ||--o{ AUDIT : menghasilkan
```

### 3.3 Bentuk `catatan` (inti sistem)

```
catatan
├─ id
├─ plant_id · line_id · divisi_id · item_id     (pemilik sel)
├─ tanggal · shift · ritme                      (kapan berlaku)
├─ nilai_angka | nilai_pilihan | nilai_biner    (salah satu sesuai jenis item)
├─ status  : SESUAI | DI_BAWAH | LEWAT | NIHIL | BELUM | N_A
│            (N_A hanya dari konfigurasi item_line, R-73 — bukan diketik;
│             SESUAI/DI_BAWAH/LEWAT dihitung sistem memakai arah item)
├─ sebab_teks · tindakan_teks · pic_id
├─ kasus_id (opsional, bila memicu kasus)
├─ diisi_oleh · diisi_pada · perangkat
└─ versi (naik saat koreksi, nilai lama disimpan di `koreksi`)
```

Aturan bentuk: **satu sel satu baris**. Ringkasan apa pun (per line, per pilar, per bulan) dihitung
dari tabel ini, tidak disimpan sebagai angka yang bisa diedit.

---

## 4. Peran dan hak (ringkas)

| Kemampuan | Leader | Petugas divisi | Supervisor | DH | Plant head | Admin | TV |
|---|---|---|---|---|---|---|---|
| Isi tab divisi sendiri | ✅ Produksi | ✅ divisinya | ✅ | ✅ | ❌ | ✅ | ❌ |
| Koreksi setelah cut-off | ❌ | ❌ | ✅ + alasan | ✅ + alasan | ✅ | ✅ | ❌ |
| Ketuk absensi | ✅ shift berjalan | ❌ | ✅ | ✅ | ❌ | ✅ | ✅ |
| Buka kasus / isi PICA | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Setujui penutupan | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Ubah target & item | ❌ | ❌ | ❌ | ❌ | usul | ✅ | ❌ |
| Kunci periode | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ |
| Kelola profil TV & daftar nama | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | baca |

Matriks penuh dan alasannya: `DMS_Aturan_Sistem_v1.md` bagian 2.

---

## 5. Tujuh layar: isi dan komponen

### 5.1 Isi papan (tablet/PC line)

- **Kepala:** plant › line › tanggal, badge hari kerja, sisa waktu sebelum cut-off.
- **Tab divisi:** SHE · Quality · Produksi · Teknik · Delivery (badge titik bila belum diisi).
- **Tabel sel:** item · target · hasil · status (warna) · sebab/bukti.
- **Panel kanan:** kelengkapan harian (x/y), status divisi lain, absensi shift, tombol kirim.
- **Bawah:** kotak sebab & tindakan (muncul wajib bila status di bawah target) + PIC + tenggat otomatis.
- **Perilaku:** simpan otomatis draf, validasi sebelum kirim, kirim hanya bagian divisi sendiri.

### 5.2 Papan lantai (TV)

- **Satu divisi per layar** (R-80), bukan papan gabungan lima kolom. Bentuk tetap papan:
  kepala papan → grid KPI (target vs S1/S2/S3/harian/mingguan/bulanan) → tabel kasus aktif →
  baris PICA → footer.
- **Kolom mengikuti Excel** (R-83): SHE dari `Resume SHE` (Area, Category Safety, Problem Statement,
  Running Day→Umur, foto), Quality dari `Resume QC` (Priority Level, Validasi QCP, Case Category),
  Produksi dari `Resume Prod` (**DT (min)** ditonjolkan). Grid KPI dari `Template Penilaian →
  Summary DMS to KPI`; index dari `DMS_INDEX`.
- Kepala papan: plant, line, divisi, tanggal, shift, index divisi, kasus terbuka, lewat tenggat,
  hadir/total, **jam pembaruan terakhir + badge sumber** (R-87).
- Rotasi (R-59): **Absensi → SHE → Quality → Produksi → Delivery → Teknik → Ringkasan**, 20–30 detik
  per halaman, dengan penanda `Halaman n/N`. Urutan & durasi diatur Admin.
- Kolom statis, baris & angka dinamis per hari (R-84). Divisi tanpa data tetap tampil "belum diisi".
- Tanpa interaksi, kecuali tombol absensi. Tidak ada kolom pencarian plant/line.
- Bila data hari ini belum ada: tampilkan angka kemarin dengan tanda **"data kemarin"**.
- Delivery & Teknik belum punya sheet Excel → perlu sumber sendiri (R-86).

### 5.3 Absensi

- **Dikerjakan paling awal, sebelum isian DMS** (R-81). Sesi: `DIBUKA → ABSENSI → ISI DIVISI →
  REVIEW → DIKUNCI`. Tombol kirim divisi terkunci sampai kehadiran dikonfirmasi; Supervisor/DH
  dapat membuka dengan alasan tercatat.
- Pintu masuk: **QR sesi** di TV/papan (R-82) — token terikat plant/line/tanggal/shift, berputar
  tiap shift, dapat dicabut; menulis wajib SSO. Satu tautan untuk absensi, isian, PICA, dan review.
- Sumber nama: impor daftar (Excel) atau tarik dari mesin absensi bila tersedia; default semua **hadir**.
- Lapangan menandai yang tidak hadir: sakit · izin · alpa · terlambat · dinas luar.
- Ketukan dari TV atau dari isian menulis ke catatan absensi yang sama.
- Tersedia **urungkan 2 menit**; semua ketukan tercatat (waktu, perangkat, pengguna bila login).
- Menutup otomatis saat cut-off shift. Shift yang **tidak pernah dikonfirmasi** sampai cut-off
  ditandai "belum dikonfirmasi" — bukan dianggap hadir semua; penjelas output (R-37) hanya
  memakai absensi terkonfirmasi.

### 5.4 Dasbor L1–L3

| Tingkat | Pertanyaan yang dijawab | Isi |
|---|---|---|
| **L1** | hari ini aman? | kelengkapan pengisian, kasus hari ini, yang lewat tenggat |
| **L2** | apa yang harus ditutup? | daftar kasus berumur, temuan berperingkat, tombol aksi |
| **L3** | plant/line mana yang perlu perhatian? | perbandingan plant & line, tren, skor proses vs hasil |

Komponen: 4 kartu KPI + tren, grafik per pilar, temuan 3 teratas, tabel kasus lewat tenggat.
Semua angka dapat diklik menuju daftar detailnya.

### 5.5 Detail kasus

- Kepala kasus: kode, mesin/line, pelapor, dampak (A/B/C), umur vs tenggat, tingkat eskalasi.
- Riwayat lima tahap: dilaporkan → diagnosis → perbaikan → verifikasi → penutupan.
- Empat kolom wajib dengan status; tombol **Ajukan penutupan** nonaktif sampai lengkap.
- PICA 4–5 pertanyaan + tindakan pencegahan (wajib bila berulang ≥3×/90 hari).
- Lampiran (foto/dokumen) dan dampak (menit berhenti, output hilang, jumlah berulang).

### 5.6 Laporan & KPI

- Filter plant / periode / shift; hanya periode **terkunci** yang bisa dibagikan.
- Skor proses (kelengkapan & ketepatan waktu) dan skor hasil (target pilar) dilaporkan **terpisah**.
- KPI V/O biner: tercapai / tidak, dengan jumlah (mis. 18/24).
- Tren 6 bulan + skor per line; ekspor Excel/PDF; kirim ke Group.

### 5.7 Admin

- Target & bobot KPI **per versi** (berlaku per periode) + simulasi dampak sebelum simpan.
- Profil TV: pilih halaman divisi yang tampil, urutan, durasi rotasi, absensi di awal, penanda halaman.
- Sumber data & sinkronisasi: daftarkan workbook, lihat status sinkron, karantina, dan peta kolom.
- Daftar nama, regu, shift, line; impor Excel.
- Kunci periode; buka kunci dengan alasan.
- Jejak audit: siapa, kapan, sebelum–sesudah.

---

## 6. Mesin aturan (logika di balik layar)

| Aturan | Pemicu | Keluaran |
|---|---|---|
| **Validasi isian** | simpan sel | tolak bila hasil kosong, di luar batas wajar, atau sebab kosong saat di bawah target |
| **Kelengkapan** | harian | persen item terisi per line/divisi; dipakai skor proses |
| **Tenggat kasus** | kasus dibuat | tenggat = f(dampak A/B/C) hari kerja, bukan ketikan |
| **Eskalasi** | tenggat lewat | naik L1→L2→L3 tiap 2 hari kerja |
| **Berulang** | kasus baru | sama sebab/kategori ≥3× dalam 90 hari → wajib pencegahan |
| **I-01…I-12** | harian | katalog kanonik 12 kartu temuan (Logic_Design §7); I-01…I-08 dulu (gerbang G3), I-09…I-12 sebelum Display; I-13/I-14 = pemeriksaan mutu data Admin, bukan kartu |
| **Kunci periode** | akhir bulan/laporan | data periode terkunci; koreksi jadi versi baru |
| **Cut-off shift** | akhir shift | leader tidak bisa ubah lagi; supervisor/DH dengan alasan |
| **Snapshot TV** | tiap 20–30 detik | TV menerima tampilan siap-tampil; hemat beban dan tahan jaringan putus |
| **Kiriman offline** | sinkron setelah cut-off | diterima sebagai **usulan koreksi** ke Supervisor (tidak ditolak diam-diam, tidak menimpa langsung); hak edit dinilai dari timestamp perangkat |

### 6.1 Mesin penilaian (jembatan papan → skor)

Menyatukan model papan per shift dengan rumus penilaian `DMS_Logic_Design_v1.md` §3.
Rumus tetap; grain input berubah dari meeting harian menjadi sel papan per shift.

```
// ---------- DARI SEL KE V/O (tidak diketik tangan) ----------
status_sel   = bandingkan(hasil, target, arah_item)      // SESUAI / DI_BAWAH / LEWAT
V            = status SESUAI (atau NIHIL bila item kejadian dan tidak ada kejadian)
O            = status DI_BAWAH / LEWAT yang berarti gagal target
N/A          = dari konfigurasi item_line (R-73), keluar dari penyebut
BELUM        = tidak dihitung V/O; menurunkan skor proses (kelengkapan)

// ---------- SHIFT → HARI ----------
// item per-shift : nilai hari = agregasi antar shift sesuai jenis item
//   angka acumulatif (output, downtime) → jumlah; rasio (defect %, OEE) → rata-rata terbobot
// item harian/Per-PO : satu nilai per hari, tidak diagregasi shift
ach_kpi_harian = jumlah_V / (jumlah_V + jumlah_O)        // semua item KPI hari itu

// ---------- HARI → PEKAN (denominator tetap, bukan hari terisi) ----------
penyebut      = hari_kerja(Sen–Jum) − libur_plant        // R-05; hari belum isi = 0, bukan hilang
ach_checklist = Σ nilai_harian / (penyebut × target)     // target BAKU 0,8
ach_kpi       = Σ ach_kpi_harian / (penyebut × target)

// ---------- BAND (config versioned; bandingkan 2 desimal) ----------
skor = 5 jika ach ≥ 1,20 · 4 jika ≥ 1,10 · 3 jika ≥ 1,00 · 2 jika ≥ 0,90 · 1 lainnya

// ---------- INDEX & PELAPISAN ----------
DMS Index   = skor_KPI×0,4 + skor_Checklist×0,4 + skor_Healthy×0,2   // target 3, max 5
skor_proses = kelengkapan pengisian (R-69) + ketepatan waktu (R-26)  // dilaporkan TERPISAH
skor_hasil  = pencapaian target pilar (V/O)                          // dilaporkan TERPISAH
```

Ketentuan:

1. **Checklist meeting 6 item** (bobot 10/20/10/20/20/20) tetap dinilai per line per hari —
   menjadi bagian tab Produksi ritme harian; item on-time & kelengkapan dihitung sistem.
2. **Healthy Check** konstan per periode (R-28), masuk index dengan bobot 0,2; perubahannya
   wajib lewat simulasi dampak (R-54).
3. Semua parameter (bobot, band, target, ambang) dari `target_versi` yang berlaku pada
   periode tersebut — periode lalu tidak berubah (R-52).
4. **Index tidak menggantikan skor proses/hasil** — ketiganya tampil berdampingan (R-71);
   index untuk perbandingan antar periode/plant, proses-hasil untuk tindakan.

---

## 7. Non-fungsional

| Aspek | Target | Catatan |
|---|---|---|
| Kecepatan isi | satu shift selesai **< 5 menit** per leader | target UX, diuji di pilot |
| Waktu muat dasbor | < 3 detik pada data 12 bulan | indeks pada `plant, line, tanggal` |
| Kesegaran TV | data terlihat ≤ 30 detik dari input | snapshot push, bukan polling berat |
| Ketersediaan | jam produksi ≥ 99% | mode baca tetap jalan saat tulis gagal |
| Offline sementara | draf tersimpan lokal di tablet | kirim otomatis saat jaringan kembali |
| Keamanan | sesi login, hak per plant/line, audit penuh | TV memakai kode perangkat + token yang bisa dicabut Admin; dampak kebocoran terbatas: baca papan + absensi line itu (R-34) |
| Retensi | kasus & catatan ≥ 5 tahun; **foto bukti ≥ 5 tahun mengikuti kasusnya** | bukti tidak boleh hilang lebih dulu dari kasusnya (R-29, R-45) |
| Backup | harian penuh + log harian | uji restore tiap kuartal |
| Aksesibilitas TV | kontras tinggi, huruf besar, warna + label | jangan bergantung pada warna saja |
| Jejak audit | semua perubahan nilai & konfigurasi | tidak bisa dihapus peran mana pun |

---

## 8. Teknologi usulan (dan alasannya)

| Lapisan | Usulan | Alasan |
|---|---|---|
| Basis data | PostgreSQL | transaksi kuat untuk satu-catatan-per-sel, query laporan mudah, gratis |
| Backend | satu layanan HTTP (mis. Node/NestJS atau Python/FastAPI) | satu API untuk tiga wajah, mudah dirawat tim kecil |
| Frontend | web (React/Next) responsif | satu basis kode untuk tablet, PC, dan TV (mode kios) |
| Berkas | penyimpanan objek / folder terkelola | foto bukti tidak membebani DB |
| Penjadwal | cron/worker di server yang sama | cut-off, snapshot TV, tenggat, eskalasi |
| Deploy | server plant (on-premise) + satu server group | data produksi tidak keluar jaringan plant |
| Monitoring | log terpusat + alert | deteksi TV mati / kiriman gagal |

Alternatif yang sah: memakai **platform internal group** bila sudah tersedia — yang penting tiga wajah,
satu API, satu DB (bukan tiga aplikasi terpisah).

---

## 9. Rencana 8 pekan

```mermaid
gantt
    title Rencana implementasi (pilot Snack)
    dateFormat  YYYY-MM-DD
    axisFormat  %d %b
    section Fondasi
    Master line, mesin, pengguna, daftar nama   :a1, 2026-11-09, 14d
    section Capture
    Isi papan lima divisi + absensi             :a2, 2026-11-09, 21d
    section Measure
    Angka otomatis + dasbor L1                   :a3, 2026-11-23, 14d
    section Insight
    Kartu temuan I-01…I-08, lalu I-09…I-12       :a4, 2026-12-07, 7d
    section Display
    TV papan + panel absensi                     :a5, 2026-12-21, 7d
    section Analitik
    Laporan KPI + ekspor                         :a6, 2026-12-21, 7d
    section Gerbang
    Uji terima & gerbang replikasi               :a7, 2026-12-28, 7d
```

| Gerbang | Syarat lulus | Bila gagal |
|---|---|---|
| **G1 Kesiapan data** | master line/mesin cocok dengan laporan lama, nama seragam | rapikan master dulu, jangan mulai isian |
| **G2 Angka cocok** | angka sistem = workbook, **atau selisih terjelaskan penuh** dalam laporan rekonsiliasi (de-dup, sel error dibuang, baris tanpa tanggal valid) | telusuri selisih sebelum dasbor dibuka |
| **G3 Aturan jalan** | 8 aturan pertama (I-01…I-08) memunculkan kartu dengan pemilik & tenggat; I-09…I-12 aktif sebelum Display | aturan dipertajam, layar lantai ditunda |
| **G4 Siap replikasi** | lima ukuran keberhasilan (rancangan/01 §4.2) terpenuhi di Snack | perbaikan satu putaran, replikasi digeser |

Replikasi: Snack (8 pekan) → Exist Plant (4) → New Plant (4) → Dairy (4) = **20 pekan**.

---

## 10. Migrasi data historis

| Sumber | Nasib | Catatan |
|---|---|---|
| 17.201 kasus tiga workbook | arsip bertanda `historis` | dipakai pembanding; **tidak memicu kartu TV/eskalasi/I-02** (R-75) — masuk laporan kualitas-data & program pembersihan ber-PIC |
| Ringkasan sheet | **tidak diimpor** | dihitung ulang dari baris kasus |
| Sel error (153) | dibuang, dicatat sebagai temuan mutu | tidak boleh masuk sistem |
| Master line/mesin | dibersihkan dulu (satu ejaan) | syarat G1 |
| Daftar nama & regu | impor Excel | dasar absensi |
| Target & bobot | dibuat sebagai **versi 1** per plant | periode lalu memakai versi historis |

Urutan impor wajib: plant → line → mesin → divisi/item → target versi → pengguna → kasus historis → absensi.

---

## 11. Uji terima (diterima bila…)

1. Satu shift bisa diselesaikan leader **di bawah 5 menit** tanpa pelatihan panjang.
2. Angka TV = angka dasbor = angka laporan untuk tanggal yang sama.
3. Kasus tanpa bukti **tidak bisa** ditutup (uji coba sengaja).
4. Koreksi setelah cut-off tercatat lengkap (siapa, kapan, alasan, nilai lama).
5. TV tetap menampilkan papan terakhir saat jaringan putus, dengan penanda waktu.
6. Absensi dari TV dan dari form menghasilkan catatan yang sama (tanpa duplikat).
7. Laporan bulanan bisa diekspor tanpa menyusun ulang di Excel.
8. Perbandingan plant memakai definisi identik (target versi masing-masing).
