# Insight dari Workbook xlsx dan Terjemahannya untuk Aplikasi DMS

Dokumen pendamping `DMS_Digitalisasi_v1.pptx` dan `DMS_Logic_Design_v1.md`.
Sumber: tiga workbook DMS — `Snack`, `EP` (Exist Plant), `NP` (New Plant) — masing-masing 11–12 sheet.
Bagian 1–7 memakai contoh Snack; **bagian 8 memuat pembaruan angka tiga plant** yang dipakai di deck terbaru.
Semua angka diambil langsung dari workbook, bukan asumsi.

---

## 1. Tiga lapis insight yang diambil dari xlsx

| Lapis | Pertanyaan | Contoh di workbook | Dipakai untuk apa di aplikasi |
|---|---|---|---|
| **Isi** (apa yang terjadi) | Berapa kasus, line mana, mesin mana, kapan | 5.817 kasus; Pilus L1 3.014 kasus; MHM 26,8% downtime | Isi kartu TV dan dasbor L1–L3 |
| **Mutu data** (boleh dipercaya?) | Kolom wajib terisi atau tidak | SHE 0% sebab, QC 79%, Produksi 78% | Skor proses + tombol "kirim ulang" |
| **Logika** (apakah hitungannya benar) | Apakah rumus memberi arti yang sama | `0,88 ÷ 0,80 = 1,0999 → skor 3` padahal 110% = skor 4 | Aturan hitung baku di aplikasi |

Kesalahan umum: orang hanya mengambil lapis isi (jumlah kasus), lalu aplikasi dibangun di atas logika yang belum dibereskan. Workbook ini justru kaya pada lapis 2 dan 3.

---

## 2. Insight isi — apa yang bisa dibaca dari data

| # | Insight | Angka | Sheet asal |
|---|---|---|---|
| 1 | Beban kasus terkonsentrasi di Produksi | 3.112 dari 5.817 kasus (53,5%) | Resume Prod |
| 2 | Satu line mendominasi kasus | Pilus L1 = 3.014 kasus (96,9% kasus line itu) | Resume Prod |
| 3 | Dua mesin menyumbang hampir separuh downtime | MHM 26,8% + BCAT 14,1% = 40,9% | Resume Prod |
| 4 | Masalah berulang, bukan acak | 184 pola ≥3× mencakup 816 kasus (26,2%) | Resume Prod, Resume QC |
| 5 | Ekor masalah menua | 22 kasus lewat tenggat, tertua 1.045 hari | Resume SHE |
| 6 | Label berulang diisi manual dan tidak konsisten | 849 dari 902 label (94%) keliru | Resume QC, Resume Prod |

**Arti untuk aplikasi:** angka-angka ini bukan laporan bulanan, melainkan **pemilih kartu**. Layar TV hanya boleh memuat temuan dengan dampak besar (kasus terbanyak), berulang (≥3×), menua (aging), dan bisa dikendalikan line sendiri.

---

## 3. Insight mutu data — bagian yang paling sering hilang saat pindah dari Excel

| # | Temuan | Angka | Konsekuensi |
|---|---|---|---|
| 7 | Status "Close" diisi karena kolomnya berisi | 973 kasus Close tanpa sebab (16,7%) | Capaian terlihat selesai, padahal belum diperbaiki |
| 8 | Bukti foto hampir tidak ada | Resume SHE: sebab 0%, due date 0%, bukti 0% | Kasus tidak bisa diaudit ulang |
| 9 | Prioritas tidak membedakan | High muncul di hampir 100% kasus | Urutan kerja tidak terbentuk dari prioritas |
| 10 | PIC bukan pemilik hasil | 99,7% PIC adalah fungsi Teknik, skor dinilai ke leader line | Yang dinilai ≠ yang mengerjakan |
| 11 | Satu kasus bisa tercatat dua kali | Sheet IIAA Snack (120 baris) menduplikasi resume | Volume bisa dobel |
| 12 | Rumus rusak tertinggal di sheet | 51 sel error di Resume Prod (`#VALUE!` 44, `#REF!` 7); 24 `#DIV/0!` di Resume Snack | Angka bisa kosong tanpa disadari |

**Arti untuk aplikasi:** mutu data harus dijadikan **skor**, bukan sekadar catatan. Empat kolom wajib (sebab, tindakan, bukti, PIC) adalah gerbang sebelum kasus boleh ditutup — lihat slide 4 deck.

---

## 4. Insight logika — bukti dari sheet `DMS_INDEX`

Workbook menyimpan enam blok penilaian: Agustus, W27, W28, W29, W30, W31. Nilainya:

| Blok | DMS Compliance | Checklist | Healthy Check | DMS Index |
|---|---|---|---|---|
| Agustus | 0,88 → Ach 1,0999 → skor 3 | 0,89 → 1,1125 → skor 4 | 0,80 → 1,00 → skor 3 | **3,40** |
| W31 | 0,88 → 1,0999 → skor 3 | 0,88 → 1,0999 → skor 3 | 0,80 → skor 3 | **3,00** |
| W27 | 0,92 → 1,15 → skor 4 | 0,90 → 1,125 → skor 4 | 0,80 → skor 3 | **3,80** |
| W28 | 0,87 → 1,0875 → skor 3 | 0,90 → 1,125 → skor 4 | 0,80 → skor 3 | **3,40** |
| W29 | 0,87 → 1,0875 → skor 3 | 0,90 → 1,125 → skor 4 | 0,80 → skor 3 | **3,40** |
| W30 | 0,86 → 1,075 → skor 3 | 0,88 → 1,0999 → skor 3 | 0,80 → skor 3 | **3,00** |

Empat hal yang terbaca dari tabel ini:

1. **Ambang kehilangan satu tingkat.** Ach 1,0999 dibaca 109% sehingga jatuh ke skor 3; kalau dibandingkan dua desimal (110%) seharusnya skor 4. Terjadi di 5 dari 6 blok.
2. **Healthy Check tidak pernah berubah.** Selalu 0,80 → Ach 1,00 → skor 3 → menyumbang 0,60 tetap. Parameter ini tidak mengukur apa pun.
3. **Blok bertumpuk tanpa urutan waktu.** W31 berada sebelum W27; W28 dan W29 identik sampai dua desimal — indikasi salin tempel.
4. **Penyebut tidak terlihat.** Skor checklist memakai target 0,80 per hari, tetapi jumlah hari wajib tidak tersimpan, sehingga 1 hari terisi bisa terlihat 125%.

**Arti untuk aplikasi:** hitungan tidak boleh disimpan sebagai hasil tempel, melainkan sebagai **rumus + jejak input**. Aplikasi wajib menyimpan: jumlah hari wajib, hari terisi, nilai per item, versi parameter, dan siapa yang mengubah.

---

## 5. Insight yang tidak bisa diambil dari xlsx (harus dari aplikasi)

| Yang dicari | Kenapa xlsx tidak bisa | Yang harus dicatat aplikasi |
|---|---|---|
| Waktu respons | Tidak ada jam buka → jam tutup | Timestamp buka, verifikasi, tutup |
| Kepemilikan tindakan | PIC hanya kolom teks | PIC + tenggat + status per tindakan |
| Efektivitas perbaikan | Kasus berulang tidak terhubung | Relasi kasus → PICA → standar baru (OPL/PM) |
| Kepatuhan mengisi | Tidak ada log pengisian | Log harian per line, siapa, jam berapa |
| Riwayat perubahan skor | Nilai tertimpa | Audit trail sebelum–sesudah |

Kelima hal ini yang membuat aplikasi bernilai lebih daripada workbook — bukan karena tampilannya, tetapi karena **bukti prosesnya tersimpan**.

---

## 6. Peta insight → fitur aplikasi

| Insight workbook | Fitur di aplikasi | Kanal |
|---|---|---|
| 973 kasus Close tanpa sebab | Gerbang tutup kasus: 4 kolom wajib | Form kasus (User) |
| 0% bukti di Resume SHE | Unggah foto/dokumen wajib, kompres otomatis | Form kasus |
| 184 pola ≥3× | Deteksi otomatis pola + rekomendasi Preventive | Dasbor L2 |
| 22 kasus lewat tenggat | Hitung mundur + eskalasi berjenjang | TV, L1, L2 |
| 94% label berulang keliru | Label diambil dari master sebab, bukan diketik | Form kasus |
| MHM 26,8% · BCAT 14,1% | Kartu tetap "mesin penyumbang downtime" | TV, L3 |
| 51 sel error | Validasi input + tidak ada rumus di sel bebas | Semua kanal |
| Healthy Check konstan | Parameter teredisi Admin, bertanggal & berversi | Halaman admin |
| Blok W28 = W29 | Kunci periode; nilai berasal dari perhitungan, bukan salinan | Halaman admin |
| 6 item × bobot 10–20 | Template inti 6 item, bobot 10/20/10/20/20/20 | Form harian |

---

## 7. Ringkas untuk rapat

1. Workbook sudah memberi **bahan lengkap**: volume, sebaran, pola berulang, dan aging.
2. Yang belum ada bukan data, tetapi **jaminan mutu**: sebab, bukti, pemilik, dan waktu.
3. Karena itu aplikasi dibangun dengan urutan: **kunci logika → paksa mutu → baru tampilkan**.
4. Empat angka yang layak dipantau mingguan: **973** (tanpa sebab), **94%** (label), **22** (aging), **184** (pola berulang).


---

## 8. Pembaruan data: tiga workbook (Snack, Exist Plant, New Plant)

Angka di bagian ini yang dipakai deck `DMS_Digitalisasi_v1.pptx` versi terbaru.
Definisi baris kasus: satu baris pada tabel kasus yang punya tanggal valid (dihitung ulang dengan
`docs/analyze_workbook.py`, hasil mentah di `docs/data_plants.json`).

### 8.1 Volume per plant dan per sheet

| Plant | Kasus | SHE | QC | Prod | Close tanpa sebab |
|---|---|---|---|---|---|
| Snack | 5.815 | 1.185 | 1.519 | 3.111 | 1.369 |
| Exist Plant | 6.774 | 1.836 | 2.338 | 2.600 | 954 |
| New Plant | 4.612 | 1.875 | 1.266 | 1.471 | 897 |
| **Total** | **17.201** | **4.896** | **5.123** | **7.182** | **3.220** |

### 8.2 Mutu data per sheet (root cause terisi)

| Sheet | Snack | Exist Plant | New Plant |
|---|---|---|---|
| Resume SHE | 54,2% | 51,9% | 56,7% |
| Resume QC | 78,9% | 97,6% | 92,8% |
| Resume Prod | 78,5% | 91,9% | 89,7% |
| Due date SHE | 0% | 0% | 0% |
| Bukti foto SHE | 4,5% | 22,6% | 19,4% |

### 8.3 Pola dan downtime

| Ukuran | Snack | Exist Plant | New Plant |
|---|---|---|---|
| Pola berulang ≥3× | 303 pola / 2.001 kasus | 292 / 2.240 | 134 / 952 |
| Pola teratas | Pilus L1 · SVB13 BCAT 20× | WS L04 · P02 BCT 134× | WS L09 · E08 BCT 33× |
| Downtime total (Prod) | 208.848 menit | 196.525 menit | 102.853 menit |
| Median downtime | 50 menit | 60 menit | 60 menit |
| Kasus lewat tenggat | 23 | 21 | 9 |
| Sel error di sheet resume | 51 | 51 | 51 |

### 8.4 Selisih ringkasan sheet vs isi tabel

| Plant | QC ringkasan | QC tabel | Prod ringkasan | Prod tabel |
|---|---|---|---|---|
| Snack | 1.018 | 1.519 | 988 | 3.111 |
| Exist Plant | 993 | 2.338 | 977 | 2.600 |
| New Plant | 999 | 1.266 | 1.003 | 1.471 |

Blok STATUS PICA menyimpan angka sendiri tanpa periode, dan di ketiga plant angkanya lebih kecil
dari jumlah baris kasus. Kesimpulan untuk aplikasi: **hitung dari baris kasus, jangan dari sel ringkasan.**

### 8.5 Temuan khas per plant

| Plant | Temuan | Angka |
|---|---|---|
| Snack | Satu line mendominasi | Line 9 = 96,9% kasus Produksi (3.014) |
| Exist Plant | Satu line + satu LBN mendominasi QC | WS L02 535 kasus; WS L04 P02 BCT 134× |
| New Plant | Pola terkonsentrasi di dua line | WS L11 615 kasus QC (48,6%) |
| Exist Plant | Kolom PIC berisi tautan foto | Puluhan sel berisi URL SharePoint, bukan nama PIC |
| Exist Plant | DMS Index satu blok 0,6 | Blok lain 3,0 → indikasi salah input |
| Semua | Prioritas tidak membedakan | High = 100% kasus |
| Semua | Healthy Check konstan | 0,80 di semua blok → kontribusi tetap 0,6 |

### 8.6 Angka pengganti di deck

| Sebelum (Snack saja) | Sesudah (tiga plant) |
|---|---|
| 5.817 kasus | 17.201 kasus |
| 973 close tanpa sebab (16,7%) | 3.220 close tanpa sebab (18,7%) |
| 184 pola / 816 kasus | 729 pola / 5.193 kasus (30,2%) |
| 22 kasus lewat tenggat | 53 kasus lewat tenggat |
| 208.848 menit downtime | 508.226 menit (8.470 jam mesin) |
