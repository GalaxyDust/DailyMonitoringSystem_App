# 01 · Kenapa DMS Digital Dibuat

**Dokumen:** bagian 1 dari 3 rancangan aplikasi Daily Monitoring System (DMS)
**Status:** rancangan untuk persetujuan — belum ada implementasi kode
**Pemilik:** Tim Daily Monitoring System · Group Manufacturing
**Tanggal:** 5 November 2026

> Paket dokumen: **01 Kenapa** (file ini) → **02 Rancangan Aplikasi** → **03 Alur Sistem**.
> Aturan baku yang mengikat ketiganya: [`DMS_Aturan_Sistem_v1.md`](../DMS_Aturan_Sistem_v1.md).
> Logika dan pembongkaran rumus Excel: [`DMS_Logic_Design_v1.md`](../DMS_Logic_Design_v1.md).

---

## 0. Ringkasan satu halaman

Papan DMS hari ini **sudah benar gagasannya, tetapi mahal dikerjakan**. Satu papan memuat empat pilar
(Safety, Quality, Productivity, Delivery) dan diisi tangan per line per shift, lalu direkap ulang ke
Excel, dihitung ulang dengan kalkulator, disalin ke grup WhatsApp, dan dibahas di rapat pagi.

Kerja manual itu tidak menambah keputusan apa pun — ia hanya **memindahkan angka dari satu tempat ke
tempat lain**. Dari tiga workbook (Snack, Exist Plant, New Plant) terlihat akibatnya: 17.201 kasus
dengan 3.220 kasus ditutup tanpa sebab, 729 pola berulang tanpa tindakan pencegahan, 53 kasus lewat
tenggat, dan 153 sel error yang membuat angka tidak bisa dipakai.

Aplikasi DMS dibuat untuk **menghapus lapisan rekap**, bukan untuk mengganti manusia atau menambah
administrasi. Satu kali isi → semua layar membaca angka yang sama.

| Pertanyaan | Jawaban singkat |
|---|---|
| Kenapa dibuat? | Karena ~22 jam/bulan per plant habis untuk merekap, bukan memperbaiki |
| Untuk siapa? | Leader line, petugas divisi (SHE/QC/Produksi/Teknik/Delivery), supervisor, DH, plant head, admin |
| Apa yang berubah? | Isi sekali di papan digital; TV, dasbor, laporan membaca catatan yang sama |
| Apa yang **tidak** berubah? | Bentuk papan, keputusan manusia, dan disiplin shift |
| Ukuran berhasil? | Kelengkapan pengisian ≥ 90%, close bersebab ≥ 95%, kasus lewat tenggat turun 50% |

---

## 1. Kondisi hari ini (baseline angka, bukan opini)

### 1.1 Volume yang harus dikelola

| Plant | Kasus | SHE | QC | Produksi | Line | Close tanpa sebab | Pola berulang ≥3× | Lewat tenggat |
|---|---|---|---|---|---|---|---|---|
| Snack | 5.815 | 1.185 | 1.519 | 3.111 | 20 | 1.369 | 303 / 2.001 | 23 |
| Exist Plant | 6.774 | 1.836 | 2.338 | 2.600 | 59 | 954 | 292 / 2.240 | 21 |
| New Plant | 4.612 | 1.875 | 1.266 | 1.471 | 45 | 897 | 134 / 952 | 9 |
| **Total** | **17.201** | 4.896 | 5.123 | 7.182 | 124 | **3.220 (18,7%)** | **729 / 5.193 (30,2%)** | **53** |

Tambahan temuan dari workbook:

- **Due date di sheet SHE: 0% terisi** — tidak ada satu pun tenggat yang tercatat, sehingga tidak ada yang bisa ditagih.
- **Bukti foto saat kasus ditutup: 4,5%–22,6%** — sebagian besar penutupan tanpa bukti visual.
- **Sebab terisi di sheet SHE: 52%–57%** — hampir separuh kasus tanpa sebab tertulis.
- **153 sel error** (`#VALUE!`, `#N/A`, teks di kolom angka) — 51 sel per plant.
- **Ringkasan sheet ≠ isi tabel** sampai dua kali lipat (contoh: QC Snack 1.018 di ringkasan vs 1.519 baris; Prod Snack 988 vs 3.111).
- **Downtime tercatat 508.226 menit** dengan median 50–60 menit per kasus, tetapi sebab teknisnya tidak pernah sampai ke Teknik dalam bentuk kerja resmi.

### 1.2 Waktu yang habis untuk rekap

| Ukuran | Angka | Artinya |
|---|---|---|
| Kasus 12 bulan terakhir | 2.272 (rata-rata 189/bulan, puncak 366) | beban papan tidak pernah turun di bawah ~100 kasus/bulan |
| Waktu merekapitulasi | ~6 jam/bulan | menyalin papan → rekap → file |
| Waktu menyusun laporan harian | ~16 jam/bulan | 3 plant × 21 hari × 15 menit |
| **Total beban manual** | **~22 jam/bulan** | setara ±3 hari kerja orang, setiap bulan, per lingkup plant |

Angka 22 jam ini bukan angka mati: ia bergerak sebanding jumlah line dan jumlah pilar yang diisi.

---

## 2. Tujuh masalah yang sebenarnya terjadi

Bukan "orangnya kurang disiplin", tetapi **sistem kerjanya** yang membuat disiplin sulit dipertahankan.

| # | Masalah | Gejala di lapangan | Akibat yang terukur |
|---|---|---|---|
| M1 | **Angka ditulis di banyak tempat** | papan → buku rekap → Excel → grup WA | ringkasan dan isi tabel berbeda sampai dua kali lipat |
| M2 | **Tidak ada satu pemilik angka** | siapa pun bisa mengubah sel | angka satu divisi bisa ditimpa divisi lain |
| M3 | **Penutupan kasus tidak bergerbang** | kasus "selesai" tanpa sebab/bukti | 3.220 kasus tanpa sebab, bukti 4,5–22,6% |
| M4 | **Tidak ada tenggat yang dihitung** | tenggat hanya ingatan orang | due date SHE 0%, 53 kasus lewat tenggat (tertua 1.182 hari) |
| M5 | **Masalah berulang tidak dikenali** | label "Occurrence" dipakai berulang | 729 pola berulang, 30,2% tanpa tindakan pencegahan |
| M6 | **Sebab teknis tidak sampai ke Teknik** | telepon/grup pribadi, tanpa nomor kerja | 508.226 menit downtime tanpa analisis penyebab yang bisa dibandingkan |
| M7 | **Bahan rapat disusun ulang tiap pagi** | copy-paste, print, format berbeda | waktu rapat habis untuk menyamakan angka, bukan memutuskan |

---

## 3. Yang hilang kalau aplikasi ini dibuat (dan bukan sekadar "pindah ke web")

Sepuluh pekerjaan manual yang **berhenti dikerjakan**, bukan dipindahkan:

| Pekerjaan manual sekarang | Yang berhenti dikerjakan |
|---|---|
| Rekap harian dari papan dan kertas | menyalin ke buku rekap |
| Memindahkan angka ke beberapa file | copy-paste antar file |
| Menghitung nilai harian | menghitung dengan kalkulator |
| Mencari kolom yang belum diisi | menyisir kolom satu per satu |
| Menyusun bahan rapat pagi | menyiapkan slide/printout |
| Menagih tindak lanjut | menelepon/chat pribadi |
| Menebak masalah berulang | menandai manual di kolom |
| Mengumpulkan angka antar plant | menggabung sheet manual |
| Mencari riwayat perubahan angka | menanyakan siapa yang mengubah |
| Menyusun laporan bulanan | merangkum ulang tiap bulan |

---

## 4. Tujuan dan ukuran keberhasilan

### 4.1 Tujuan (urut prioritas)

1. **Satu catatan, satu angka** — semua kanal membaca catatan yang sama.
2. **Sekali isi** — leader dan tiap divisi mengisi bagiannya sendiri, tanpa mengetik ulang.
3. **Gerbang mutu** — kasus tidak bisa ditutup tanpa sebab, tindakan, bukti, dan PIC.
4. **Tenggat berjalan sendiri** — dihitung sistem, naik tingkat otomatis.
5. **Masalah berulang dikenali** — minimal 3 kejadian dalam 90 hari wajib punya pencegahan.
6. **Papan tetap papan** — TV dan isian mengikuti bentuk yang sudah dikenal lapangan.
7. **Konfigurasi lentur, data tegas** — divisi/item/target bisa berubah, angka historis tidak ikut berubah.

### 4.2 Ukuran keberhasilan (dipakai evaluasi pekan ke-8)

**Lima ukuran gerbang** (dipakai R-77, G4, dan gerbang replikasi — sama dengan deck hal. 20):

| Ukuran | Kondisi hari ini | Target | Cara ukur |
|---|---|---|---|
| Hari terisi tanpa diingatkan | belum terukur | ≥ 90% | hari terisi ÷ hari wajib (Sen–Jum − libur) |
| Kasus dengan sebab lengkap | SHE 52–57% · QC 79–98% · Prod 79–92% | ≥ 95% | kolom sebab terisi |
| Tenggat tercatat | 0% di sheet SHE | ≥ 95% | kolom tenggat terisi sistem |
| Kasus lewat tenggat | 53 kasus | turun 50% | umur kasus > tenggat |
| Pola berulang punya tindakan | 729 pola | 100% | pola dengan pencegahan tertutup |

Ukuran tambahan (dipantau, bukan gerbang):

| Ukuran | Kondisi hari ini | Target | Cara ukur |
|---|---|---|---|
| Waktu rekap | 22 jam/bulan | ≤ 4 jam/bulan | jam kerja rekap per bulan |
| Insight ditindaklanjuti | belum terukur | ≥ 70% | temuan dengan tindakan tercatat |

---

## 5. Tujuh prinsip desain (dipakai saat memutuskan fitur)

| # | Prinsip | Konsekuensi praktis |
|---|---|---|
| P1 | **Papan tetap papan** | Bentuk papan dipertahankan (grid KPI × baris item × kolom shift), tetapi TV menyajikan **satu divisi per layar** dengan kolom mengikuti Excel (R-80, R-83) |
| P2 | **Satu catatan per sel** | tidak ada tabel ringkasan yang diisi tangan; ringkasan dihitung |
| P3 | **Sekali isi, banyak layar** | TV, dasbor, laporan, ekspor membaca catatan yang sama |
| P4 | **Tiap divisi pemilik bagiannya** | SHE/QC/Produksi/Teknik/Delivery mengisi tabnya, tidak bisa menimpa tab lain |
| P5 | **Konfigurasi lentur, data tegas** | Admin boleh ubah item/target/pilar; angka periode lalu tidak berubah |
| P6 | **TV tanpa login, tetapi terikat** | TV hanya menampilkan + menerima absensi, terikat satu profil (kode perangkat) |
| P7 | **Keputusan tetap di manusia** | sistem mengingatkan dan menggerbangi, bukan memutuskan prioritas |

Prinsip ini yang mencegah aplikasi menjadi "Excel dengan warna baru".

---

## 6. Yang sengaja **tidak** dibuat pada fase 1

| Tidak dibuat | Alasan |
|---|---|
| Aplikasi mobile native | form/isi papan berbasis web cukup; hemat biaya dan perawatan |
| Login di TV | lapangan butuh nol hambatan; TV terikat perangkat dan hanya menerima absensi |
| Mengedit angka papan dari TV | mengetik di TV lambat dan rawan salah; TV bukan alat ketik |
| Angka manual selain Healthy Check | angka harus datang dari catatan, bukan ketikan bebas |
| Fitur analitik prediktif | butuh data bersih dulu; fase 2 setelah 3 bulan data rapi |
| Integrasi penuh mesin/PLC | dimulai dari ekspor/impor file; integrasi langsung setelah kebutuhan jelas |

---

## 7. Risiko bila tidak dikerjakan

| Risiko | Dampak |
|---|---|
| Angka terus berbeda antar sumber | rapat berhenti di debat angka, keputusan tertunda |
| Kasus tanpa sebab menumpuk | masalah yang sama terulang; perbaikan hanya menambal |
| Downtime tidak terklasifikasi | investasi perbaikan mesin tidak berbasis data |
| Beban rekap menetap ~22 jam/bulan | waktu supervisor habis di belakang meja, bukan di line |
| Pengetahuan pindah bersama orang | riwayat hanya ada di papan dan ingatan |
| Sulit membandingkan plant | tiap plant memakai format dan definisi berbeda |

---

## 8. Pemangku kepentingan dan manfaatnya

| Peran | Yang mereka dapat |
|---|---|
| **Leader line** | isi sekali, di bawah 5 menit; tidak menyalin ke buku rekap |
| **Petugas divisi** (SHE/QC/Teknik/PPIC) | mengisi bagiannya saja; tahu mana yang belum diisi |
| **Supervisor / DH** | melihat temuan berperingkat dan menutup kasus dengan bukti |
| **Plant head** | skor proses vs skor hasil, prioritas berbasis dampak |
| **Admin plant** | satu tempat untuk target, daftar nama, profil TV, kunci periode |
| **Group Manufacturing** | perbandingan antar plant dengan definisi yang sama |
| **Teknik** | downtime masuk sebagai work order dengan tenggat, bukan telepon |

---

## 9. Cara menggabungkan ketiga dokumen

```bash
# gabung jadi satu dokumen utuh
cd docs/laporan/rancangan
cat 01-KENAPA-DMS-DIGITAL.md 02-RANCANGAN-APLIKASI.md 03-ALUR-SISTEM.md > ../DMS_Rancangan_Lengkap.md

# atau ke PDF/DOCX bila pandoc tersedia
pandoc 01-KENAPA-DMS-DIGITAL.md 02-RANCANGAN-APLIKASI.md 03-ALUR-SISTEM.md -o DMS_Rancangan_Lengkap.pdf
```

Hubungan dengan dokumen lain:

| Dokumen | Isi | Dipakai kapan |
|---|---|---|
| **01 (ini)** | alasan, baseline angka, tujuan, prinsip | saat meminta persetujuan/anggaran |
| **02 Rancangan Aplikasi** | modul, data, peran, teknologi, non-fungsional | saat membangun dan menguji |
| **03 Alur Sistem** | alur harian, absensi, kasus, eskalasi, koreksi, laporan | saat sosialisasi ke plant dan saat uji terima |
| `DMS_Aturan_Sistem_v1.md` | 87 aturan bernomor (WAJIB/BAKU/SARAN) | rujukan hukum sistem; tidak boleh dilanggar |
| `DMS_Logic_Design_v1.md` | pembongkaran rumus Excel → logika aplikasi (sebagian digantikan paket ini; lihat banner di dokumennya) | saat memindahkan penilaian |
| `DMS_Review_Rancangan_v1.md` | review silang antar-dokumen + status perbaikan | saat mengecek konsistensi rancangan |
| `DMS_TV_PerDivisi_dan_Integrasi_Excel_v1.md` | TV satu divisi per layar, absensi di awal, QR satu pintu, sinkron Excel otomatis | saat menyepakati tampilan TV dan cara integrasi Excel |
| `DMS_Digitalisasi_v1.pptx` | deck 28 halaman untuk rapat | saat presentasi ke manajemen |
