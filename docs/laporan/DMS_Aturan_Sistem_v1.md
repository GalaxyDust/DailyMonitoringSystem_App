# DMS Digital — Aturan Sistem v1

Dokumen ini adalah **aturan baku** sistem Daily Monitoring System (DMS) digital: siapa mengisi apa,
kapan boleh diubah, kapan terkunci, dan apa yang boleh/tidak boleh ditampilkan. Dibuat sebagai
rujukan tunggal supaya aplikasi, TV, papan, dan rapat pagi memakai aturan yang sama.

**Cara membaca:** setiap aturan punya nomor dan tingkat.

| Tingkat | Arti |
|---|---|
| **WAJIB** | tidak boleh dilanggar; kalau dilanggar, sistem menolak atau data dianggap tidak sah |
| **BAKU** | nilai/ambang tetap, bisa diubah Admin kapan saja tetapi dicatat sebagai versi baru |
| **SARAN** | praktik yang dianjurkan; boleh berbeda per plant selama disepakati plant head |

Nomor aturan dipakai di dokumen lain dan di aplikasi (label tombol, pesan validasi) supaya mudah dirujuk.
Kalau ada aturan yang bertentangan, yang menang adalah nomor yang lebih kecil di bagian yang lebih awal.

---

## 1. Struktur, istilah, dan penomoran

| Istilah | Arti |
|---|---|
| **Group** | seluruh perusahaan; pemilik definisi dan perbandingan antar plant |
| **Plant** | satu lokasi produksi: Snack, Exist Plant, New Plant, Dairy |
| **BU / Factory** | unit di dalam plant (mis. Factory 10 di Exist Plant) |
| **Line** | baris produksi tempat papan dipasang: Snack 20 line, EP 59 line, NP 45 line |
| **Divisi / pilar** | pemilik bagian papan: SHE, Quality, Produksi, Delivery (PPIC), **Teknik** |
| **Shift** | 1, 2, 3 atau regu A/B/C sesuai pola plant |
| **Papan** | tampilan empat/lima pilar untuk satu line pada satu tanggal dan shift |
| **Catatan** | satu sel isian papan: line + tanggal + shift + divisi + item |
| **Kasus** | kejadian yang perlu ditutup dengan sebab, tindakan, bukti, PIC |
| **Temuan** | keluaran sistem dari catatan/kasus (lewat tenggat, berulang, menumpuk, dst.) |
| **TV** | layar lantai tanpa login, terikat satu profil tampilan |

- **R-01 · WAJIB — satu papan, satu catatan.** Tidak ada angka kedua. Semua tampilan (TV, dasbor, laporan,
  ekspor) membaca catatan yang sama. Dilarang membuat tabel ringkasan terpisah yang diisi tangan.
- **R-02 · WAJIB — hierarki tetap:** Group → Plant → BU/Factory → Line → Divisi. Line tidak boleh
  berpindah plant; kalau pindah, dibuat line baru dan yang lama diarsipkan.
- **R-03 · WAJIB — kode tetap dan tidak dipakai ulang:**
  `PLANT` (SN/EP/NP/DR) · `LINE` (SN-L09) · `KASUS` (SN-QC-0441) · `WORK ORDER` (EP-TK-0031) ·
  `TV` (SN-L09-TV1) · `PERIODE` (2026-11). Kode yang sudah dipakai tidak boleh dipakai untuk entitas lain.
- **R-04 · WAJIB — satu hari satu papan.** Untuk satu line + tanggal + shift hanya ada satu papan,
  walaupun diisi bergantian oleh beberapa divisi.
- **R-05 · WAJIB — hari kerja Senin–Jumat**, dikurangi kalender libur plant. Sabtu/Minggu dan hari libur
  tidak dihitung sebagai hari wajib dan tidak boleh menurunkan skor kepatuhan pengisian.
- **R-06 · BAKU — nama line dan mesin diseragamkan** sebelum sistem dipakai (satu ejaan, satu kode).
  Contoh yang harus dibereskan: `ws 02 / WS L02 / Line 2 hidup` adalah line yang sama.

---

## 2. Peran dan hak akses

### 2.1 Daftar peran

| Peran | Cakupan | Inti tugasnya |
|---|---|---|
| **Leader Line** | satu line, satu shift | isi papan bagian divisinya, absensi shift, buka kasus |
| **Petugas Divisi** (SHE / QC / Teknik / PPIC) | banyak line sesuai wilayah | isi item milik divisinya di semua line wilayahnya |
| **Supervisor** | satu area / beberapa line | koreksi, verifikasi angka, approve penutupan tahap 1 |
| **DH (Departemen Head)** | satu plant | approve penutupan, jaga mutu data divisinya |
| **Kepala Divisi** | satu plant, satu divisi | target divisi, daftar item, pemilik tindakan |
| **Plant Head** | satu plant | prioritas, approve akhir, kunci periode |
| **Admin Plant** | satu plant | master line/mesin/user, target, profil TV, kunci periode |
| **Admin Group** | semua plant | template bersama, perbandingan plant, master grup |
| **Auditor / DH Grup** | semua plant, hanya baca | audit jejak perubahan, tidak boleh mengubah |
| **TV Device** | satu profil tampilan | hanya menampilkan dan menerima ketukan absensi |

### 2.2 Matriks hak

| Kemampuan | Leader | Petugas Divisi | Supervisor | DH | Kepala Divisi | Plant Head | Admin | Auditor | TV |
|---|---|---|---|---|---|---|---|---|---|
| Isi catatan papan divisi sendiri | ✅ line sendiri | ✅ wilayahnya | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Isi catatan papan divisi lain | ⚠️ hanya item bertanda "boleh diisi leader" (R-13) | ❌ | ✅ koreksi | ✅ koreksi | ✅ koreksi | ❌ | ✅ | ❌ | ❌ |
| Ketuk absensi | ✅ shift berjalan | ❌ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ shift berjalan |
| Buka kasus | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Isi sebab & tindakan kasus | ✅ miliknya | ✅ miliknya | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Ajukan penutupan | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Setujui penutupan | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| Koreksi setelah cut-off | ❌ | ❌ | ✅ + alasan | ✅ + alasan | ✅ + alasan | ✅ | ✅ | ❌ | ❌ |
| Ubah target / bobot / item | ❌ | ❌ | ❌ | ❌ | ⚠️ usul | ⚠️ usul | ✅ | ❌ | ❌ |
| Kelola master data & user | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Profil TV | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ | ✅ baca |
| Kunci periode | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Lihat jejak audit | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ❌ |

- **R-07 · WAJIB — batas data per plant.** Setiap akses data difilter `plant_id` (dan `line_id` untuk
  leader). Tidak ada peran yang bisa membaca plant lain kecuali Admin Group dan Auditor.
- **R-08 · WAJIB — divisi hanya mengubah bagiannya.** Petugas SHE tidak dapat mengubah sel QC,
  dan sebaliknya. Ini yang mencegah angka pilar ditimpa orang lain.
- **R-09 · WAJIB — pemisahan isi dan setujui.** Orang yang mengisi sebab tidak boleh menjadi satu-satunya
  yang menyetujui penutupan kasus. Minimal satu langkah persetujuan berasal dari peran berbeda.
- **R-10 · WAJIB — TV tidak punya hak ubah data papan.** TV hanya menampilkan papan dan menerima
  ketukan absensi shift berjalan.

---

## 3. Pembagian pemilik bagian papan (termasuk Teknik)

Papan dibagi per divisi. Tiap divisi mengisi bagiannya sendiri dan **tidak saling menunggu**.

| Divisi | Isi bagiannya | Ritme | Sumber angka | Contoh item |
|---|---|---|---|---|
| **SHE** | kecelakaan, near miss, temuan KAK, status tindakan | per shift | laporan kejadian, inspeksi | zero accident, SHE index, KAK terakhir |
| **Quality** | defect per line, critical point, kontaminasi, hold/release | per shift | inspeksi QC, hasil lab | defect %, hold, status kalibrasi alat ukur |
| **Produksi** | checklist, output vs target, downtime, OEE, sebab singkat | per shift | pencatatan line | checklist A/B, output, downtime menit |
| **Delivery (PPIC)** | plan vs real PO, keterlambatan, kesiapan muat | per PO & harian | jadwal kirim, gudang | plan vs real, on-time, keterlambatan |
| **Teknik** | penyebab teknis downtime, PM, spare part, kalibrasi mesin/utilitas | per kejadian & per jadwal | work order, jadwal PM | status mesin, PM terlambat, tunggu part |

- **R-11 · WAJIB — satu sel satu pemilik.** Setiap item papan punya tepat satu divisi pemilik.
  Item yang membutuhkan dua divisi dipecah menjadi dua item (lihat aturan Teknik di bawah).
- **R-12 · WAJIB — pengisian paralel.** Papan boleh terisi sebagian. Bagian yang belum diisi
  ditandai **"belum diisi"** beserta jam terakhir pengecekan — bukan dibiarkan kosong tanpa keterangan.
- **R-13 · WAJIB — leader line melihat semua pilar, mengubah hanya pilar Produksi.** Kalau petugas
  divisi tidak ada di shift tersebut, leader boleh mengisi item divisi lain **hanya bila Admin
  menandai item itu "boleh diisi leader"**; kalau tidak, item tetap "belum diisi" dan menjadi temuan.
- **R-14 · BAKU — TV menampilkan bagian yang sudah masuk**, dengan jam terakhir pembaruan di setiap
  pilar. Pilar yang belum diisi tidak dikosongkan, tetapi diberi tanda abu-abu "belum diisi".

### 3.1 Aturan khusus Teknik (Maintenance)

Teknik adalah pemilik **sebab teknis** dan **pencegahan**, bukan pencatat durasi line berhenti.
Pembagian ini yang membuat tidak ada dua orang mencatat hal yang sama.

| Langkah | Siapa | Yang dicatat | Batas waktu |
|---|---|---|---|
| 1. Line berhenti | Produksi (leader) | mesin, jam mulai, jam selesai, menit downtime, output hilang | saat kejadian |
| 2. Dipanggil | Produksi | tanda "menunggu teknik" | langsung |
| 3. Diagnosis & perbaikan | Teknik | kategori sebab (mekanik/elektrik/utilitas/setting/operator), komponen, tindakan (sementara/permanen), work order, spare part, teknisi | **≤ 4 jam** untuk kategori A, ≤ 24 jam untuk B |
| 4. Serah terima | Teknik | mesin dinyatakan jalan / uji coba | setelah perbaikan |
| 5. Konfirmasi | Produksi | "normal" atau "masih bermasalah" (kasus dibuka kembali) | 1 shift berikutnya |

- **R-15 · WAJIB — produksi mencatat durasi, teknik mencatat sebab.** Satu kejadian downtime hanya
  punya satu baris, diisi bertahap oleh dua divisi. Dilarang mencatat downtime di dua tempat.
- **R-16 · WAJIB — kategori sebab downtime terbatas pada lima pilihan** agar bisa dibandingkan antar
  plant: mekanik · elektrik · utilitas · setting/changeover · operator/metode. Penyebab lain masuk
  "lain-lain" + penjelasan teks.
- **R-17 · WAJIB — setiap downtime di atas ambang (BAKU, awal 30 menit per kejadian) otomatis menjadi
  kasus Teknik** dengan tenggat diagnosis. Downtime di bawah ambang cukup tercatat sebagai angka.
- **R-18 · WAJIB — teknik tidak menunggu surat.** Kasus downtime yang belum didiagnosis melewati batas
  waktu muncul di papan Teknik, dasbor, dan TV area teknik. Eskalasi ke Kepala Divisi Teknik setelah
  dua kali batas waktu.
- **R-19 · BAKU — PM (preventive maintenance) terjadwal** per mesin: daftar mesin, periode, item PM,
  penanggung jawab. Status hanya tiga: **selesai · tertunda (+alasan) · belum waktunya**. PM tertunda
  dua periode berturut menjadi temuan berulang.
- **R-20 · BAKU — spare part kritis**: daftar part kritis per mesin, stok minimum, dan status.
  Stok di bawah minimum menjadi kartu TV "tunggu part" dan harus punya rencana pengadaan.
- **R-21 · BAKU — kalibrasi alat ukur** (milik QC, jadwal milik Teknik): alat, tanggal kalibrasi
  terakhir, jatuh tempo, sertifikat. Alat yang jatuh tempo tidak boleh dipakai untuk mengesahkan
  angka QC — sistem menandai angkanya.
- **R-22 · SARAN — jam mesin dan utilitas** (listrik, udara tekan, steam, chiller) dibaca harian bila
  tersedia dari mesin; kalau tidak, cukup dicatat kejadian anomali. Jangan menambah isian tanpa data.
- **R-23 · SARAN — papan kedua di ruang teknik** (mesin × status) memakai data yang sama; tidak ada
  isian tambahan. Ini hanya tampilan berbeda dari catatan yang sama.

---

## 4. Pengisian harian

- **R-24 · WAJIB — satu isian per sel.** Leader/petugas mengisi hasil; target dan satuan sudah menempel
  pada item, tidak diketik ulang. Isian yang sudah disimpan tidak perlu dikirim dua kali.
- **R-25 · WAJIB — validasi sebelum simpan:** hasil wajib angka atau pilihan yang sah; kalau hasil di
  luar target, **sebab wajib diisi**; kalau sebab dipilih "lain-lain", teks wajib diisi.
- **R-26 · WAJIB — cut-off per shift.** Leader dapat mengubah catatan sampai **30 menit setelah shift
  berakhir**. Setelah itu catatan terkunci untuk leader (lihat bagian 6).
- **R-27 · WAJIB — hari tanpa aktivitas tetap diisi.** Bila tidak ada kejadian, leader memilih
  "nihil" — bukan membiarkan kosong. Sistem membedakan **kosong** (belum diisi) dan **nihil** (sudah
  dikonfirmasi tidak ada kejadian).
- **R-28 · BAKU — Healthy Check** diisi Admin, bukan lapangan; nilainya konstan per periode.
- **R-29 · WAJIB — bukti foto** ditempel pada kasus, bukan disimpan di ponsel. Satu kasus minimal satu
  bukti bila statusnya "ditutup".
- **R-30 · WAJIB — input dari satu tempat.** Angka papan diisi dari tablet/PC line (atau HP bila
  mendesak). TV tidak dipakai untuk mengetik angka (lihat R-58).

---

## 5. Absensi harian

- **R-31 · WAJIB — daftar nama disiapkan Admin**, bukan diketik lapangan: nama, regu/shift, line,
  divisi, dan masa berlaku. Impor dari file (Excel) dianjurkan; mengetik manual hanya untuk koreksi.
- **R-32 · WAJIB — status awal "hadir".** Sistem mengisi seluruh daftar shift sebagai hadir, lalu
  lapangan hanya menandai yang **tidak hadir**: sakit · izin · alpa · dinas luar · terlambat.
- **R-33 · WAJIB — absensi bisa dikerjakan dari TV (tanpa login), form web, atau hasil pindai QR sesi (R-82)**, hasilnya sama.
  Dua jalur ini menulis ke catatan absensi yang sama — tidak ada rekap ulang.
- **R-34 · WAJIB — TV hanya bisa mengabsen shift berjalan dan line miliknya sendiri** (terikat kode
  perangkat). Tanggal lampau tidak bisa diubah dari TV.
- **R-35 · WAJIB — setiap ketukan tercatat**: waktu, perangkat, dan (bila login) nama pengguna.
  Tersedia **Urungkan 2 menit** untuk salah ketuk.
- **R-36 · BAKU — absensi menutup otomatis** pada cut-off shift; setelah itu hanya Supervisor/DH/Admin.
  Shift yang tidak pernah dikonfirmasi sampai cut-off ditandai **"belum dikonfirmasi"** — tidak
  dianggap hadir semua; penjelas output (R-37) hanya memakai absensi terkonfirmasi.
- **R-37 · BAKU — absensi menjadi penjelas otomatis:** bila output di bawah target, sistem menampilkan
  jumlah hadir/total di samping angka output pada TV dan dasbor. Tidak perlu menulis sebab "orang kurang"
  secara manual — tetapi alasannya tetap bisa ditambahkan bila penyebabnya lain.
- **R-38 · WAJIB — absensi tidak dipakai menilai orang** di dalam sistem ini. Yang dipakai untuk KPI
  adalah kehadiran terkonfirmasi per shift dan kelengkapan pengisian, bukan peringkat individu.
- **R-39 · SARAN — absensi per line dan shift** sebagai default. Bila sebuah divisi punya regu sendiri
  (mis. Teknik lintas line), Admin menandai divisi itu punya daftar absensi terpisah.

- **R-81 · WAJIB — absensi dikerjakan lebih dulu, sebelum DMS.** Saat sesi dibuka, TV tampil halaman
  Absensi dan isian divisi **belum bisa dikirim** sampai kehadiran sesi dikonfirmasi leader.
  Supervisor/DH boleh membuka isian bila absensi tertunda, dengan alasan tercatat di jejak audit.
- **R-82 · WAJIB — QR sesi adalah satu pintu masuk.** Satu QR per sesi mengikat plant · line ·
  tanggal · shift, berputar tiap shift, dan dapat dicabut Admin. Semua peran masuk lewat tautan
  sesi yang sama (absensi → divisi → review → kunci); menulis tetap wajib login/SSO. QR bukan
  kanal baru dan bukan izin mengubah angka lampau.

---

## 6. Tiga tingkat kunci dan aturan koreksi

| Status | Siapa yang boleh ubah | Kapan | Syarat |
|---|---|---|---|
| **Draf** | Leader / petugas divisi pemilik | selama shift + 30 menit | bebas, otomatis tercatat |
| **Terkunci** | Supervisor, DH, Kepala Divisi | sampai rapat pagi hari kerja berikutnya (BAKU 08.30, mengikuti jam rapat plant — deck hal. 3) | wajib **alasan koreksi**; nilai lama tetap tersimpan |
| **Arsip** | Admin Plant | setelah periode dikunci | koreksi menjadi **versi baru**, bukan menimpa |

- **R-40 · WAJIB — koreksi tidak pernah menghapus nilai lama.** Riwayat: nilai, siapa, kapan, alasan.
- **R-41 · WAJIB — angka yang dikoreksi di atas ambang** (BAKU: perubahan > 5% atau mengubah status
  close) harus disetujui satu tingkat di atas pengoreksi. Untuk item **biner/pilihan/status**,
  setiap perubahan nilai dianggap "besar" (ambang 5% hanya berlaku untuk item angka).
- **R-42 · WAJIB — periode dikunci** setelah laporan bulanan disahkan. Periode terkunci hanya bisa
  dibuka Admin Plant dengan alasan, dan pembukaan tercatat di jejak audit.
- **R-43 · WAJIB — sengketa angka saat rapat** diselesaikan dengan urutan: bukti (foto/work order) →
  catatan mesin/absensi → kesepakatan plant head. Hasilnya dikoreksi lewat jalur R-40, bukan dengan
  mencatat angka baru di tempat lain.
- **R-44 · WAJIB — hapus data tidak tersedia untuk peran mana pun.** Yang ada hanya pembatalan
  (batal) dengan alasan, dan arsip.

---

## 7. Kasus, tenggat, dan eskalasi

- **R-45 · WAJIB — empat kolom wajib sebelum kasus ditutup:** sebab · tindakan · bukti · PIC.
  Tombol "tutup" tidak aktif bila salah satu kosong.
- **R-46 · WAJIB — setiap kasus punya tenggat** yang dihitung sistem dari tingkat dampak, bukan
  diketik tangan. Tingkat dampak: **A** (lini berhenti / keselamatan) · **B** (mutu/hold) ·
  **C** (administratif). Tenggat awal BAKU: A = 1 hari kerja, B = 3 hari kerja, C = 5 hari kerja.
  Tingkat dampak **ditetapkan otomatis dari jenis item/kejadian** (pemetaan di konfigurasi Admin);
  pengisi boleh mengusulkan naik, penurunan hanya oleh Supervisor ke atas dengan alasan.
- **R-47 · WAJIB — kasus lewat tenggat naik otomatis**: saat tenggat lewat, kasus langsung naik
  ke **L2** (supervisor/DH); setiap **2 hari kerja** keterlambatan berikutnya naik satu tingkat:
  **L3** (plant head) pada hari ke-2, masuk **laporan Group** pada hari ke-4. Kartu eskalasi
  tampil di TV area terkait dan dasbor tingkatnya.
- **R-48 · WAJIB — berulang dihitung sistem**: kejadian dengan **signature** sama ≥ 3 kali dalam
  BAKU 90 hari menjadi **temuan berulang** dan wajib punya tindakan pencegahan, bukan hanya
  perbaikan. Signature = **(line, mesin/LBN, kategori sebab)** — sama dengan pemicu I-03;
  teks problem bebas tidak dipakai sebagai kunci.
- **R-49 · WAJIB — penutupan butuh persetujuan** satu tingkat di atas pengaju (R-09).
  Bila pengaju adalah **Plant Head**, penyetuju adalah **Admin Group**; bila pengaju Admin Plant
  satu-satunya, penyetuju adalah Plant Head. Tidak ada peran yang menyetujui pengajuannya sendiri.
- **R-50 · BAKU — kasus tanpa aktivitas 14 hari** ditandai "dingin" dan dipertanyakan pada rapat
  berikutnya; bukan langsung ditutup.

---

## 8. Konfigurasi dinamis vs aturan tetap

### 8.1 Yang boleh diubah Admin tanpa menyentuh aplikasi

1. Divisi/pilar: tambah, ganti nama, urutkan.
2. Item checklist per line per divisi, beserta satuan dan target.
3. Jenis isian per item: angka+target · biner (ya/tidak) · pilihan status · teks sebab · foto · tanggal.
4. Ritme per item: per shift · harian · per PO · mingguan · per kejadian.
5. Target, bobot, dan band penilaian per plant — **versioned**.
6. Profil TV: pilar yang tampil, urutan, lama rotasi, mode layar (papan penuh / papan + absensi).
7. Daftar nama absensi, regu, dan pola shift.
8. Hak akses per divisi dan per line.

### 8.2 Yang tidak boleh diubah siapa pun

- **R-51 · WAJIB — satu angka per catatan**: tidak ada jalur kedua untuk memasukkan angka yang sama.
- **R-52 · WAJIB — data historis tidak ikut berubah** saat konfigurasi diubah. Target baru berlaku
  untuk periode berikutnya; periode lalu tetap memakai versi lamanya.
- **R-53 · WAJIB — setiap perubahan konfigurasi tercatat** (siapa, kapan, sebelum–sesudah).
- **R-54 · WAJIB — rumus penilaian tidak boleh diubah per pengguna.** Yang bisa diubah hanya parameter
  yang tercantum di 8.1, dan setiap perubahan harus memperlihatkan simulasi dampak sebelum disimpan.

---

## 9. Tampilan TV dan layar lain

- **R-55 · WAJIB — TV berbentuk papan**, bukan daftar kartu lepas: kepala papan (plant, line, tanggal,
  shift), grid KPI (target vs realisasi per shift), tabel kasus, dan baris PICA — disajikan
  **satu divisi per layar** (R-80), sel dengan warna status dibanding target.
- **R-56 · WAJIB — TV tanpa login dan tanpa interaksi**, kecuali panel absensi.
- **R-57 · WAJIB — TV terikat satu profil** (kode perangkat). TV tidak punya kolom pencarian plant/line.
- **R-58 · WAJIB — angka papan tidak diubah dari TV.** TV bukan alat ketik.
- **R-59 · BAKU — rotasi per divisi**: **Absensi (saat sesi dibuka) → SHE → Quality → Produksi →
  Delivery → Teknik → Ringkasan/DMS Index**, lalu ulang. BAKU 20–30 detik per halaman; urutan,
  durasi, dan halaman aktif diatur Admin lewat profil TV. Bukan lagi papan gabungan lima kolom.
- **R-60 · WAJIB — TV selalu menunjukkan kesegaran data**: jam pembaruan terakhir dan tanda
  "data kemarin" bila hari ini belum ada isian. TV tidak boleh terlihat seperti angka hari ini
  padahal masih kemarin.
- **R-61 · WAJIB — layar PC/admin**: dasbor L1–L3 (lihat), halaman admin (ubah aturan, koreksi,
  kunci periode, profil TV). Hanya dari sini data dan aturan boleh diubah.
- **R-62 · BAKU — empat kanal tetap**: form/tablet isian · dasbor L1–L3 · TV lantai · halaman admin.
  Menambah kanal baru harus lewat aturan, bukan aplikasi terpisah. QR sesi (R-82) adalah pintu
  masuk kanal isian, bukan kanal kelima.

- **R-80 · WAJIB — satu divisi per layar.** TV menampilkan satu divisi penuh per halaman dengan
  penanda halaman (`Halaman 4/6`), bukan papan gabungan. Lebih detail, kolom lengkap, tetap
  terbaca 3–10 m.
- **R-83 · WAJIB — kolom TV & form mengikuti kontrak kolom Excel** divisi itu (`Resume SHE`,
  `Resume QC`, `Resume Prod`). Kolom baru yang muncul di Excel **tidak otomatis tampil**: masuk
  staging dan diberitahukan ke Admin untuk dipetakan lebih dulu.
- **R-84 · BAKU — kolom statis, isi dinamis.** Daftar kolom tetap sesuai kontrak; baris kasus,
  angka, dan target berubah mengikuti tanggal/shift. Divisi tanpa data hari itu **tetap tampil**
  dengan tanda "belum diisi" — tidak dilewati diam-diam.
- **R-87 · WAJIB — setiap angka membawa sumber dan waktu.** TV dan dasbor menampilkan badge
  sumber (`Excel` / `Aplikasi`) serta jam sinkron terakhir, selain jam pembaruan (R-60).

---

## 10. Mutu data

- **R-63 · WAJIB — kolom wajib tidak boleh disimpan kosong**; pesan kesalahan menyebut nama kolom.
- **R-64 · WAJIB — nilai di luar batas wajar ditolak** (mis. downtime lebih besar dari jam shift),
  bukan disimpan lalu dibiarkan.
- **R-65 · WAJIB — sel error tidak disimpan.** Tidak ada `#VALUE!`, `#N/A`, atau teks bebas di kolom angka.
- **R-66 · WAJIB — satu nilai tidak boleh ditulis ganda** (contoh lama: satu blok bernilai 0,6 di satu
  plant dan 3,0 di plant lain akibat salin manual). Nilai diambil dari konfigurasi, bukan dari sel.
- **R-67 · WAJIB — tanggal wajib menempel pada setiap ringkasan.** Ringkasan tanpa tanggal dianggap
  tidak sah dan tidak dipakai untuk perbandingan.
- **R-68 · BAKU — ringkasan dihitung dari baris kasus**, bukan diketik. Selisih ringkasan vs isi tabel
  (saat ini sampai dua kali lipat) tidak boleh terulang.
- **R-69 · WAJIB — kelengkapan diukur dan ditampilkan**: persen item terisi per line per hari, per divisi.
  Inilah ukuran mutu data yang dipakai rapat, bukan perasaan.

- **R-85 · WAJIB — integrasi Excel otomatis, satu arah, terus-menerus.** Petugas tetap mengisi
  workbook di laptopnya seperti biasa; sistem membaca setiap perubahan dan memperbarui basis data
  **tanpa upload manual**. Excel **tidak pernah dibekukan** dan tidak ada cutover. Aplikasi **tidak
  menulis** ke workbook. Baris yang hilang dari Excel ditandai "terhapus di sumber", tidak dihapus
  permanen. Karena file masih di laptop, folder kerja dipindah ke OneDrive **satu kali oleh IT**
  dengan *junction* di path lama agar shortcut dan kebiasaan petugas tidak berubah.
- **R-86 · BAKU — satu berkas per divisi, sinkron per berkas.** Tiap divisi memakai Excel-nya sendiri
  dan didaftarkan di daftar sumber (plant · line · divisi · path lama · ID cloud · sheet · peta kolom).
  Delivery dan Teknik **cukup didaftarkan**, bukan dibuatkan form baru. Satu berkas gagal tidak
  menahan divisi lain. ID cloud dipakai sebagai kunci agar file di-*rename* tidak memutus sinkron.
- **R-88 · WAJIB — nol langkah tambahan bagi petugas.** Sistem tidak boleh meminta petugas
  mengunggah file, mengekspor CSV, mengirim lampiran, menyalin ke folder lain, atau mengisi ulang
  data yang sudah ada di Excel. Bila sebuah rancangan menuntut langkah tambahan dari petugas,
  rancangan itu yang harus berubah — bukan petugasnya.
- **R-89 · WAJIB — kepemilikan kolom, bukan kepemilikan aplikasi.** Kolom yang ada di Excel divisi
  itu dimiliki Excel dan **baca-saja** di aplikasi; koreksi dilakukan di Excel dan aplikasi menyusul
  otomatis. Aplikasi hanya memiliki kolom yang tidak ada di Excel (absensi, konfirmasi sesi, jejak
  audit, eskalasi, tenggat, foto tambahan, persetujuan, skor proses). Tidak ada satu kolom pun
  ditulis di dua tempat, sehingga tidak ada konflik dan tidak perlu masa transisi. Untuk kolom
  milik Excel, aplikasi menampilkan **"Perbaiki di Excel"** beserta nama berkas dan barisnya.
- **R-90 · WAJIB — bedakan "belum diisi" dan "belum tersinkron".** Bila laptop petugas mati atau
  offline, TV menulis **"belum tersinkron · terakhir hh.mm"** dan tetap menampilkan angka terakhir
  beserta jamnya. "Belum diisi" hanya dipakai bila berkas memang belum menyentuh hari itu. Perubahan
  yang tertunda wajib tersusul saat online; tidak boleh ada baris hilang.

---

## 11. Penilaian dan periode

- **R-70 · WAJIB — KPI V/O bersifat biner** (tercapai / tidak), tanpa nilai antara yang bisa ditawar.
- **R-71 · BAKU — skor proses dan skor hasil dipisah.** Proses = kelengkapan dan ketepatan waktu
  pengisian; hasil = pencapaian target pilar. Keduanya dilaporkan berdampingan, tidak digabung
  menjadi satu angka yang menutupi masalah.
- **R-72 · BAKU — perhitungan memakai hari wajib R-05** (Senin–Jumat dikurangi kalender libur);
  hari tanpa kewajiban tidak dihitung. Definisi hari wajib ada di R-05 dan tidak ganda di sini.
- **R-73 · BAKU — status N/A** dipakai bila item memang tidak berlaku untuk line tersebut (mis. line
  tanpa proses tertentu), dan N/A tidak dihitung sebagai tidak tercapai.
- **R-74 · WAJIB — angka yang dipakai rapat dan KPI berasal dari catatan**, bukan dari rekap manual.
- **R-75 · SARAN — angka impor historis** (17.201 kasus dari tiga workbook) masuk sebagai arsip
  bertanda "historis" agar bisa dibandingkan, tanpa mencampur mutu datanya dengan data baru.
  Kasus historis **tidak memicu kartu TV, eskalasi, atau temuan I-02**; ia masuk laporan
  kualitas-data terpisah dan program pembersihan bertahap dengan PIC.

---

## 12. Replikasi plant

- **R-76 · BAKU — urutan replikasi:** Snack (pilot 8 pekan) → Exist Plant (4 pekan) → New Plant
  (4 pekan) → Dairy (4 pekan).
- **R-77 · WAJIB — gerbang sebelum replikasi:** data master bersih · angka sistem cocok dengan
  workbook atau selisihnya terjelaskan penuh dalam laporan rekonsiliasi · aturan jalan satu
  periode penuh · **lima ukuran keberhasilan** (rancangan/01 §4.2: hari terisi, sebab lengkap,
  tenggat tercatat, kasus lewat tenggat, pola berulang) terpenuhi di pilot.
- **R-78 · BAKU — yang dibawa saat replikasi:** master line & mesin, template item dan target (versi
  baru per plant), aturan insight, profil TV.
- **R-79 · WAJIB — yang tetap lokal:** target plant, kalender libur, daftar nama & regu, PIC dan
  jalur persetujuan.

---

## 13. Larangan tegas

1. Mencatat angka yang sama di dua tempat (papan + Excel + grup WA). Excel tetap pemilik kolomnya
   dan aplikasi hanya membaca (R-89), jadi tidak ada pencatatan ganda.
2. Menutup kasus tanpa sebab, tindakan, bukti, dan PIC.
3. Mengubah angka periode yang sudah dikunci tanpa jejak.
4. Mengetik angka papan dari TV.
5. Menghapus data (hanya batal/arsip).
6. Memakai TV untuk keperluan selain menampilkan papan dan absensi.
7. Menilai orang memakai absensi di dalam sistem (R-38).
8. Menyimpan sel error atau teks bebas di kolom angka.
9. Membuat aplikasi atau file baru di luar empat kanal (R-62).
10. Menyebut pekerjaan manual sebagai kesalahan orang; yang dinilai adalah pekerjaan yang hilang.

---

## 14. Status keputusan

**Tiga keputusan diminta pada rapat persetujuan** (deck hal. 27). Sampai rapat memutuskan, nilai
BAKU di aturan tetap berlaku; bila rapat memilih lain, aturan direvisi sebagai versi baru (R-53).
Tiga pertanyaan tambahan tentang TV & integrasi Excel **sudah dijawab plant pada 6 Nov 2026** —
lihat tabel "Sudah diputuskan" di bawah.

| No | Pertanyaan | Pilihan | Nilai berlaku sekarang |
|---|---|---|---|
| 1 | Cut-off edit leader | 30 menit · 60 menit · sampai akhir shift | 30 menit (R-26) |
| 2 | Ambang downtime jadi kasus Teknik | 30 menit · 60 menit · per mesin | 30 menit (R-17) |
| 3 | Sumber nama absensi | Admin ketik · impor Excel · tarik dari mesin absensi | impor Excel dianjurkan (R-31) |

**Sudah diputuskan** (tidak dibuka lagi):

| Pertanyaan | Keputusan | Rujukan |
|---|---|---|
| Daftar divisi final | 5 divisi: SHE, Quality, Produksi, Delivery, Teknik | §3, R-11 |
| Koreksi angka dari TV | Tidak; TV hanya tampil + absensi | R-58, R-10 |
| Absensi per line vs per divisi | Default per line; divisi lintas line boleh daftar terpisah atas tanda Admin | R-39 |
| Status absensi | hadir · sakit · izin · alpa · terlambat · dinas luar | R-32, rancangan/03 §2 |
| Item checklist | Ditetapkan dari papan Factory 10, dilengkapi bertahap oleh Admin | §8.1 |
| Retensi | Kasus & catatan ≥ 5 tahun; foto mengikuti kasusnya | rancangan/02 §7 |
| Kalender libur | Master tahunan per plant, dipelihara Admin | R-05 |
| N/A item | Dari konfigurasi item per line, bukan diketik saat mengisi | R-73 |
| Impor historis | Masuk berflag historis; tidak ke TV/eskalasi | R-75 |
| Tempat file Excel | Masih di laptop petugas → folder dipindah ke OneDrive sekali oleh IT, junction di path lama | R-85, rancangan TV §5.1 |
| Sumber Delivery & Teknik | Tiap divisi sudah punya Excel sendiri → cukup didaftarkan, bukan form baru | R-86 |
| Pembekuan Excel | **Tidak dibekukan.** Excel dipakai terus, sinkron setiap saat; yang dibagi adalah kepemilikan kolom | R-85, R-89 |
| Usaha petugas | Nol langkah tambahan; dilarang meminta upload/ekspor/isi ulang | R-88 |
