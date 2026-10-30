# Insight dari Workbook xlsx dan Terjemahannya untuk Aplikasi DMS

Dokumen pendamping `DMS_Digitalisasi_v1.pptx` dan `DMS_Logic_Design_v1.md`.
Sumber: `reference/12. Konsep Penilaian DMS Snack Des 24.xlsx` (12 sheet).
Semua angka di bawah diambil langsung dari workbook, bukan asumsi.

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
