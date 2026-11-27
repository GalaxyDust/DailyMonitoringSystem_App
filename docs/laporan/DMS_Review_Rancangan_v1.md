# DMS — Review Rancangan v1

**Tanggal:** 5 November 2026 · **Status: perbaikan sudah diterapkan** (lihat tabel status di bawah)

## Status perbaikan (5 Nov 2026)

Seluruh temuan P0 dan P1 **sudah diselaraskan di dokumen** (PPT dan folder `docs/reference/` tidak
diubah — keduanya diperlakukan sebagai acuan tetap). Keputusan diambil mengikuti deck dan
paket rancangan 5 November sebagai kanonik.

| Temuan | Status | Keputusan / lokasi perbaikan |
|---|---|---|
| A1 mesin penilaian hilang | ✅ | rancangan/02 **§6.1 Mesin penilaian**: sel→V/O otomatis, shift→hari→pekan, denominator tetap, band, index, proses≠hasil |
| A2 role 2 vs 10 | ✅ | 10 role kanonik; banner + decision log di Logic_Design |
| A3 insight 14 vs 12 | ✅ | 12 kartu (I-01…I-12, sesuai deck hal. 18); I-13/I-14 → pemeriksaan Admin; I-12 rule-based; G3 = I-01…I-08 dulu |
| A4 lubang model data | ✅ | rancangan/02 §3: +10 entity (shift, kalender_libur, temuan, pm_jadwal, spare_part, alat_ukur, po, healthy_check, item_line, arah item); N_A di enum; UNIQUE sel; shift 3 milik tanggal mulai; profil TV multi-line |
| A5 aturan waktu | ✅ | Eskalasi Otomatis: L2 hari ke-0, L3 ke-2, Group ke-4 · batas koreksi = rapat 08.30 · Temuan Berulang signature (line, mesin, kategori sebab) · Ambang Koreksi Besar biner = selalu besar · Tenggat Kasus A/B/C dampak otomatis dari konfigurasi · Penutupan Butuh Persetujuan fallback approval Plant Head→Admin Group |
| B1 kode plant | ✅ | SN/EP/NP/DR (Kode Tetap); PLT-* ditandai tidak dipakai |
| B2 urutan replikasi | ✅ | Snack → EP → NP → Dairy (Urutan Replikasi) di semua dokumen |
| B3 retensi | ✅ | kasus & catatan ≥5 th; **foto ≥5 th mengikuti kasus** (tidak lagi 2 th) |
| B4 angka baseline lama | ✅ | banner di Logic_Design → angka kanonik Insight §8 |
| B5 ukuran keberhasilan | ✅ | **5 ukuran gerbang** (deck hal. 20) di rancangan/01 §4.2, Gerbang Replikasi, G4, gerbang replikasi; waktu rekap & insight = ukuran tambahan |
| B6 hari wajib | ✅ | Hari Kerja Senin–Jumat menang (tidak editable); Hari Wajib merujuk Hari Kerja Senin–Jumat; config Logic_Design disesuaikan |
| B7 TV read-only | ✅ | token = baca papan + tulis absensi shift berjalan; bisa dicabut |
| B8 pertanyaan terbuka basi | ✅ | Aturan §14 ditulis ulang: 3 keputusan rapat (deck hal. 27) + 3 keputusan tambahan TV/Excel + tabel sudah diputuskan |
| B9 gerbang G2 | ✅ | "selisih terjelaskan penuh dalam laporan rekonsiliasi" |
| B10 matriks vs Batas Leader | ✅ | pengecualian "boleh diisi leader" masuk matriks |
| P2-1 legacy banjiri TV | ✅ | Historis Ditandai + migrasi: kasus historis tidak ke TV/eskalasi/I-02; laporan terpisah ber-PIC |
| P2-2 offline vs cut-off | ✅ | kiriman pasca-cut-off = usulan koreksi ke Supervisor; timestamp perangkat menentukan hak |
| P2-3 absensi default hadir | ✅ | Absensi Tutup di Cut-off: shift tanpa konfirmasi ditandai "belum dikonfirmasi" |
| P2-4 eskalasi tak terlihat | ✅ | Eskalasi Otomatis: kartu eskalasi wajib tampil di TV area + dasbor tingkatnya |
| P2-5 kode TV bocor | ✅ | rancangan/02 §7: token bisa dicabut, dampak terbatas Absensi Shift Berjalan |
| P2-6 template deck | ✅ | deck dimaksimalkan (5 Nov, instruksi baru): judul auto-fit agar tidak menabrak nomor halaman; ilustrasi TV/papan digambar ulang menyerupai papan DMS fisik (5 kolom pilar, grid shift, angka spidol biru/merah, baris PICA); koreksi I-10 WS L02 22,6%→22,9% |

**Sisa yang benar-benar terbuka** (menunggu rapat, bukan cacat dokumen): 3 keputusan di
Aturan §14 / deck hal. 27 — cut-off leader, ambang downtime Teknik, sumber nama absensi;
 ditambah tempat file Excel, sumber Delivery & Teknik, dan waktu pembekuan Excel.

---

## Verifikasi ulang langsung dari xlsx (5 Nov 2026)

Seluruh angka kanonik dihitung ulang **read-only** dari tiga workbook di `docs/reference/`
(openpyxl), dibandingkan dengan `docs/data/data_plants.json`, lalu ditelusuri ke dokumen.

**Hasil: 78/78 statistik inti COCOK** — kasus, close, close-tanpa-sebab, root-cause %,
overdue, pola ≥3×, downtime (total & median) per sheet; total 17.201 / 3.220 / 729 /
5.193 / 53 / 153; tabel bulanan §8.7 (12 bulan × 3 plant, total 2.272); selisih
ringkasan-vs-tabel §8.4; blok DMS_INDEX §4; downtime gabungan 508.226 menit (8.470 jam).
`data_plants.json` dapat dipercaya — tidak perlu regenerasi.

Klaim line yang sempat dicurigai ternyata **BENAR** — angkanya memakai kolom **LBN Name**
(bukan kolom Line yang berisi nomor polos):
- EP "WS L02 535 kasus" = LBN `ws l02` di Resume QC (535). ✓
- NP "WS L11 615 kasus QC (48,6%)" = LBN `ws l11` (615/1.266 = 48,6%). ✓
- Snack "Line 9 = 3.014 (96,9%)" = kolom Line Produksi. ✓

**Satu perbaikan diterapkan** — Insight §8.5: klaim "puluhan sel PIC berisi URL SharePoint"
dikoreksi menjadi **831 sel di Resume SHE Exist Plant** (hasil hitung langsung).

**Catatan (tidak mengubah dokumen/deck):**
- Deck hal. 18 "Exist WS L02 = 22,6%" — angka tepat 535/2.338 = **22,9%**; deck tidak
  disentuh sesuai instruksi (22,6% kebetulan sama dengan % bukti foto SHE EP).
- Jumlah "20/59/45 line" berasal dari gabungan unik kolom Line + LBN Name
  (`jumlah_entitas_line`), bukan jumlah line fisik terverifikasi. Angka mengikuti deck;
  **validasi ke layout plant** sebelum memodelkan entitas line / papan TV (Rotasi TV).

---

**Tanggal review awal:** 5 November 2026
**Metode:** pembacaan silang seluruh dokumen (`DMS_Aturan_Sistem_v1`, `DMS_Logic_Design_v1`,
`DMS_Insight_xlsx_ke_Aplikasi`, `rancangan/01–03`) + verifikasi angka ke `data_plants.json`.
Tanpa pengujian aplikasi (belum ada kode). Semua temuan menunjuk lokasi sumbernya.

**Kesimpulan umum:** konsep dan aturan sudah matang dan konsisten secara filosofi. Masalah utamanya:
**ada dua generasi dokumen yang belum disatukan** — `DMS_Logic_Design_v1` (29 Okt, model *meeting
harian*, 2 role) dan paket `rancangan/01–03` + `Aturan_Sistem` (5 Nov, model *papan per shift*,
10 role). Keduanya masih berlaku tanpa penanda mana yang menang, dan **logika penilaian (DMS Index)
belum punya tempat di model baru**. Itu blocker terbesar sebelum coding.

Ringkasan: **5 blocker (P0)** · **10 inkonsistensi (P1)** · **6 risiko/saran (P2)**.

---

## A. P0 — Blocker: harus diputuskan sebelum implementasi

### A1. Dua model input yang bertentangan, dan mesin skor tidak terbawa

| Sumber | Model |
|---|---|
| `Logic_Design` §5.2, §9.2 | `meeting` unik per (line, tanggal) — **harian**; 6 checklist + 15 KPI V/O diketik saat rapat |
| `Aturan` Satu Hari Satu Papan, `rancangan/02` §3.3 | `catatan` per (line, tanggal, **shift**, item) — 5 divisi mengisi paralel |

Konsekuensi yang belum dijawab:

1. **Rumus penilaian hilang di rancangan baru.** `Logic_Design` §3.3 mendefinisikan lengkap:
   bobot 6 item, band 90/100/110/120%, denominator hari kerja − libur, bobot index 0,4/0,4/0,2,
   target 3. `rancangan/02` hanya menyebut "skor proses vs hasil" dan "KPI V/O" tanpa satu pun
   rumus, tanpa posisi Healthy Check (Healthy Check), tanpa aturan agregasi pekan.
2. **Grain berbeda:** meeting = harian; papan = per shift. Skor harian dihitung dari shift yang
   mana? Rata-rata 3 shift? Shift terburuk? Belum ada aturan.
3. **V/O diketik atau dihitung?** `Logic_Design` §9.2: user menandai [V][O][N/A] manual.
   `Aturan` Satu Isian per Sel/Validasi Sebelum Simpan: hasil angka dibandingkan target oleh sistem. Kalau V/O tetap diketik
   tangan, masalah "angka bisa diatur" yang jadi alasan aplikasi ini dibuat akan kembali.

**Perbaikan yang disarankan:** tulis satu bagian "Mesin Penilaian" di `rancangan/02` yang
menjembatani: item papan → status otomatis (V/O dari perbandingan target; N/A dari konfigurasi
item, bukan ketikan) → agregasi shift→hari→pekan dengan denominator tetap → band → index.
Nyatakan eksplisit apakah checklist 6 item meeting masih dinilai terpisah atau dilebur ke
kelengkapan papan (Kelengkapan Terukur). Tanpa ini, dua developer akan membangun dua aplikasi berbeda.

### A2. Jumlah role: 2 vs 10

- `Logic_Design` keputusan #1 (status ✅ terkunci): **2 role** (User & Admin) + TV.
- `Aturan` §2.1 + `rancangan/02` §4: **10 role** (Leader, Petugas Divisi, Supervisor, DH,
  Kepala Divisi, Plant Head, Admin Plant, Admin Group, Auditor, TV).

**Perbaikan:** paket 5-Nov jelas lebih baru dan lebih lengkap — jadikan itu kanonik, lalu
**perbarui decision log `Logic_Design` #1** menjadi "digantikan: 10 role per Aturan §2.1".
Jangan biarkan keputusan berstatus ✅ yang sudah tidak berlaku.

### A3. Katalog insight: 14 vs 12 aturan

- `Logic_Design` §7: **14 aturan** (I-01…I-14), termasuk I-12 yang prediktif.
- `rancangan/02` §6 & G3, `rancangan/03` §1: **"12 aturan" / "I-01..I-12"** — tanpa menyebut
  2 mana yang dibuang. Padahal `rancangan/01` §6 melarang analitik prediktif di fase 1
  (I-12 kontradiktif bila ikut).
- Profil TV (`Logic_Design` §9.7) mencentang kode I-xx — harus cocok dengan katalog final.

**Perbaikan:** terbitkan katalog kanonik 12 aturan bernomor tetap (jangan geser nomor —
Kode Tetap: kode tidak dipakai ulang; kode yang dibuang ditandai `retired`), dan samakan rujukan
di G3, profil TV, dan mesin aturan.

### A4. Lubang model data `rancangan/02` §3

Entity yang diwajibkan aturan tetapi belum ada di model:

| Hilang | Diwajibkan oleh | Isi minimal |
|---|---|---|
| `temuan`/`insight` | Eskalasi Otomatis, Temuan Berulang, prinsip "tiap insight punya PIC & due date" | rule_code, periode, bukti, PIC, tenggat, status tindak lanjut |
| `shift` / `pola_shift` | Satu Hari Satu Papan, Cut-off 30 Menit, Absensi Shift Berjalan | jam mulai/selesai per plant; **aturan lintas tengah malam** (shift 3 milik tanggal mana?) |
| `kalender_libur` | Hari Kerja Senin–Jumat, Hari Wajib | tanggal per plant per tahun |
| `pm_jadwal` | PM Terjadwal | mesin, periode, item, PIC, status 3 nilai |
| `spare_part` | Spare Part Kritis | part kritis, stok minimum, status |
| `alat_ukur` + kalibrasi | Kalibrasi Alat Ukur | alat, jatuh tempo, sertifikat, flag angka QC |
| `po` / referensi PO | item Delivery "per PO" (§3, Satu Isian per Sel ritme) | nomor PO, plan vs real |
| `healthy_check` per periode | Healthy Check | nilai konstan per periode, diisi Admin |
| relasi **item ↔ line/plant** | §8.1 "item checklist per line per divisi" | `item` sekarang hanya milik divisi — target per line tidak bisa dibedakan |
| cakupan **profil TV multi-line** | Rotasi TV (rotasi per divisi, Satu Divisi per Layar; EP 59 line) | `profil_tv` sekarang plant/line tunggal |

Plus dua perbaikan pada `catatan`:

- Enum status `SESUAI | DI_BAWAH | LEWAT | NIHIL | BELUM` **tidak memuat `N/A`** padahal Status N/A
  mewajibkannya dan N/A harus keluar dari penyebut.
- Arah perbandingan tidak dimodelkan: untuk output, di atas target = baik; untuk downtime/defect,
  di atas target = buruk. `item` butuh kolom `arah` (higher-better / lower-better / exact) agar
  status dan V/O bisa dihitung sistem. Nyatakan juga UNIQUE(line, tanggal, shift, item).

### A5. Aturan waktu & kunci yang belum presisi

| # | Temuan | Sumber | Keputusan yang dibutuhkan |
|---|---|---|---|
| 1 | Eskalasi: Eskalasi Otomatis "naik satu tingkat **setiap 2 hari kerja** keterlambatan" vs alur 03 §6: lewat tenggat → **langsung L2**, +2 hari → L3 | Aturan Eskalasi Otomatis vs rancangan/03 §6 | L2 pada hari ke-0 atau ke-2 keterlambatan? |
| 2 | Jendela koreksi berakhir "rapat pagi (BAKU **10.00**)" vs timeline rapat pagi **08.30** | Aturan §6 vs rancangan/03 §1 | Satu jam kanonik; saran: batas koreksi = jam mulai rapat |
| 3 | Kunci recurrence berbeda: Temuan Berulang "**sebab/kategori** sama ≥3×/90 hari" vs I-03 "**signature** (LBN+problem) sama" | Aturan Temuan Berulang vs Logic_Design I-03 | Definisikan signature tunggal, mis. (line, mesin, kategori_sebab); keduanya bisa hidup tapi harus eksplisit |
| 4 | Ambang Koreksi Besar "perubahan >5%" tidak bermakna untuk item biner/pilihan/status | Aturan Ambang Koreksi Besar | Tambah: perubahan status/biner/close = selalu "besar"; >5% hanya untuk angka |
| 5 | Siapa menetapkan dampak A/B/C kasus? (tenggat dihitung darinya) | Tenggat Kasus A/B/C, rancangan/02 `kasus` | Otomatis dari jenis item/kategori, atau dipilih pengisi dengan validasi? |
| 6 | Rantai approval buntu di puncak: Plant Head mengajukan → siapa menyetujui? Admin tunggal menyetujui pengajuannya sendiri? | Pemisahan Isi dan Setujui, Penutupan Butuh Persetujuan | Aturan fallback (mis. Admin Group / plant head lain) |

---

## B. P1 — Inkonsistensi antar-dokumen (rapikan, tidak memblok arsitektur)

| # | Topik | Dokumen A | Dokumen B | Saran pemenang |
|---|---|---|---|---|
| B1 | Kode plant | `Logic_Design` §5.1: `PLT-SNK/PLT-EX1/PLT-NW1/PLT-DRY` | `Aturan` Kode Tetap: `SN/EP/NP/DR`, line `SN-L09` | Kode Tetap (aturan baku) |
| B2 | Urutan replikasi | `Logic_Design` fase 6: Exist → **Dairy → New** | Urutan Replikasi + rancangan/02: Snack → EP → **NP → Dairy** | Urutan Replikasi |
| B3 | Retensi | `Logic_Design` §13: arsip setelah **3 tahun** (perlu keputusan) | `rancangan/02` §7: kasus **≥5 th**, foto **≥2 th** | Putuskan; catatan: foto 2 th < kasus 5 th membuat bukti kasus lama hilang — selaraskan dengan Bukti Foto |
| B4 | Angka baseline | `Logic_Design`: 5.817 / 973 / 22 / 184 pola / 1.045 hari (Snack saja, definisi lama) | `Insight` §8 + rancangan/01: 17.201 / 3.220 / 53 / 729 / 1.182 (tiga plant) | Angka baru — sudah saya verifikasi cocok dengan `data_plants.json` (1.182 = NP Prod). Beri banner "angka lama, lihat Insight §8" di Logic_Design |
| B5 | Ukuran keberhasilan | Gerbang Replikasi & G3/G4: "**lima** ukuran" (versi Logic_Design §14) | `rancangan/01` §4.2: **6 ukuran**; `rancangan/03` §9: "uji **4** ukuran" | Tetapkan daftar final satu kali (saran: 6 versi rancangan/01), rujuk dari Gerbang Replikasi, G4, dan gerbang replikasi |
| B6 | Hari wajib | Hari Kerja Senin–Jumat **WAJIB** Sen–Jum vs Hari Wajib **BAKU** Sen–Jum (isi sama, tingkat beda) | `Logic_Design` §11: hari wajib **editable** oleh Admin | Hari Kerja Senin–Jumat menang (nomor lebih kecil) → berarti tidak editable; atau ubah Hari Kerja Senin–Jumat jadi BAKU. Pilih satu |
| B7 | TV read-only | `Logic_Design`: "Interaksi: tidak ada", "token **read-only**" | Absensi TV/QR/Web/TV Tanpa Login: TV menerima **ketukan absensi** (tulis) | Model baru; scope token = baca + tulis-absensi-saja, bukan read-only murni |
| B8 | Pertanyaan terbuka basi | `Aturan` §14 masih membuka: cut-off (#2), koreksi via TV (#3), status absensi (#5), ambang downtime (#7) | Sudah diputuskan di Cut-off 30 Menit (30 mnt), TV Bukan Alat Ketik (tidak), Status Awal Hadir (5 status), Ambang Downtime (30 mnt) | Tandai "sudah diputuskan" + nomor aturannya; sisakan yang benar-benar terbuka |
| B9 | Gerbang G2 mustahil persis | G2: "total kasus sistem = jumlah baris workbook" | Migrasi: 153 sel error dibuang + de-dup antar sheet | Ubah G2: "selisih **terjelaskan penuh** dalam laporan rekonsiliasi", bukan sama persis |
| B10 | Matriks vs Batas Leader | Matriks §2.2: Leader isi divisi lain = ❌ tanpa pengecualian | Batas Leader: boleh bila item ditandai "boleh diisi leader" | Tambahkan catatan pengecualian di matriks |

---

## C. P2 — Risiko & saran desain

1. **Kasus legacy akan membanjiri TV.** 53 kasus overdue historis (tertua 1.182 hari) +
   flag `legacy` hanya dikecualikan dari I-06/I-13 (`Logic_Design` §12.2). I-02 (overdue) tidak
   dikecualikan → TV pilot hari pertama langsung merah oleh warisan lama.
   **Saran:** kasus `legacy` masuk laporan kualitas-data terpisah, tidak ke TV/eskalasi;
   buat program pembersihan bertahap dengan PIC.
2. **Offline vs cut-off & urungkan.** Draf tablet tersimpan lokal (rancangan/02 §7) dan ketukan
   absensi TV dikirim saat jaringan pulih (rancangan/03 §8). Belum diatur: kiriman yang tiba
   **setelah cut-off** ditolak atau masuk sebagai koreksi? Timer "urungkan 2 menit" dihitung
   dari ketukan atau dari sinkron? **Saran:** timestamp perangkat menentukan hak; kiriman
   pasca-cut-off otomatis menjadi usulan koreksi ke Supervisor, bukan ditolak diam-diam.
3. **Absensi default "hadir" tanpa konfirmasi.** Status Awal Hadir membuat semua hadir bila tak ada yang
   menandai — shift yang lupa konfirmasi terlihat 100% hadir. **Saran:** tambah status
   "belum dikonfirmasi" per shift; Absensi Penjelas Output (penjelas output) hanya memakai absensi terkonfirmasi.
4. **Eskalasi hanya lonceng in-app.** L3 ke plant head tidak berguna bila beliau tidak membuka
   aplikasi. Integrasi WA/email memang di luar fase 1 — **saran minimal:** kartu eskalasi L2/L3
   wajib tampil di TV area terkait + rekap harian satu layar untuk rapat pagi.
5. **Kode TV di URL = secret.** `/tv/<kode-tv>` bisa difoto/disalin. `Logic_Design` sudah punya
   token cabut — bawa ke rancangan/02: kode perangkat + token yang bisa dicabut Admin, dan
   batas dampak bila bocor hanya absensi line itu (sudah dibatasi Absensi Shift Berjalan, pertahankan).
6. **Reproducibility deck.** `build_deck.py` memakai `docs/template/template_master.pptx`
   (kini tersimpan di repo, hasil rekonstruksi dari deck). Deck bisa dibangun ulang siapa pun:
   jalankan skrip di `docs/scripts/` berurutan — `analyze_workbook.py` → `make_mockups.py` →
   `build_deck.py` (font tulisan tangan Kalam ada di `docs/assets/fonts/`).

---

## D. Yang sudah baik (pertahankan)

- Angka baseline baru **bisa ditelusuri** ke `data_plants.json` (saya cek: 17.201; 3.220; 53;
  729/5.193; 508.226 menit; overdue tertua 1.182 — semuanya cocok).
- Pemisahan Produksi (durasi) vs Teknik (sebab) — Durasi vs Sebab menyelesaikan kerja ganda dengan rapi.
- Gerbang tutup 4 kolom + approval beda peran + larangan hapus + koreksi berversi: rantai audit kuat.
- Prinsip "konfigurasi lentur, data tegas" (versioned target, historis tidak berubah) sudah benar.
- Denominator hari wajib (bukan hari terisi) menutup cacat logika Excel paling berbahaya.
- Uji terima di rancangan/02 §11 dan uji alur di rancangan/03 §11 konkret dan bisa dijalankan.

---

## E. Urutan pengerjaan yang disarankan

1. **Satu keputusan induk:** paket 5-Nov (Aturan + rancangan/01–03) = kanonik;
   `Logic_Design` diberi banner "sebagian digantikan; bagian rumus §3 tetap acuan sampai
   ditulis ulang di rancangan/02". Update decision log-nya. *(menutup A2, B1, B2, B4, B7)*
2. **Tulis "Mesin Penilaian" di rancangan/02** — jembatan papan per shift → skor harian/pekan
   → index. *(A1)*
3. **Lengkapi model data** (10 entity/relasi di A4) + enum N/A + arah item. *(A4)*
4. **Presisikan 6 aturan waktu/kunci** di A5 — cukup satu baris keputusan masing-masing.
5. **Terbitkan katalog insight final 12 aturan** dengan kode tetap. *(A3)*
6. Sapu bersih B3, B5, B6, B8, B9, B10 — semuanya suntingan kecil.
7. Putuskan mitigasi P2-1 (legacy) dan P2-2 (offline) sebelum fase Capture mulai.

Setelah langkah 1–5 selesai, rancangan layak masuk fase Fondasi (master data + skema DB).
