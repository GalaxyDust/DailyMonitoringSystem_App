# DMS Digital — Aturan Sistem (v1.1)

Dokumen ini adalah **aturan baku** sistem Daily Monitoring System (DMS): siapa mengisi apa,
kapan boleh diubah, kapan terkunci, dan apa yang boleh/tidak boleh ditampilkan. Ini rujukan
tunggal supaya aplikasi, TV, papan, dan rapat pagi memakai aturan yang sama.

> **v1.1 (24 Nov 2026) — ditulis ulang agar mudah dibaca.**
> Setiap aturan sekarang memakai **nama manusiawi** + **komentar praktis**, bukan kode "R-xx".
> **Isi normatifnya tidak berubah** — hanya cara tulis + satu perbaikan substantif:
> aturan *Status Berkas Jujur* (sebelumnya "R-90") diperjelas supaya TV/aplikasi membedakan
> **kosong karena belum diisi** dan **kosong karena gagal sinkron**.
> Kode lama (R-01…R-90) sengaja dipindah ke **Lampiran A** — hanya untuk rujukan silang
> terhadap dokumen/deck lama, jangan dipakai di UI maupun dokumen baru.

**Cara membaca:** setiap aturan punya **tingkat** (Wajib / Baku / Saran) dan **komentar**
(kenapa aturan itu ada dan apa dampaknya kalau dilanggar).

| Tingkat | Arti |
|---|---|
| **WAJIB** | tidak boleh dilanggar; kalau dilanggar, sistem menolak atau data dianggap tidak sah |
| **BAKU** | nilai/ambang tetap, bisa diubah Admin kapan pun tetapi dicatat sebagai versi baru |
| **SARAN** | praktik dianjurkan; boleh berbeda per plant selama disepakati plant head |

Kalau ada aturan yang bertentangan, yang menang adalah bagian yang lebih awal di dokumen ini.

---

## Daftar isi

1. [Struktur, istilah, dan penomoran](#1-struktur-istilah-dan-penomoran)
2. [Peran dan hak akses](#2-peran-dan-hak-akses)
3. [Pembagian pemilik bagian papan (termasuk Teknik)](#3-pembagian-pemilik-bagian-papan-termasuk-teknik)
4. [Pengisian harian](#4-pengisian-harian)
5. [Absensi harian](#5-absensi-harian)
6. [Tiga tingkat kunci dan aturan koreksi](#6-tiga-tingkat-kunci-dan-aturan-koreksi)
7. [Kasus, tenggat, dan eskalasi](#7-kasus-tenggat-dan-eskalasi)
8. [Konfigurasi dinamis vs aturan tetap](#8-konfigurasi-dinamis-vs-aturan-tetap)
9. [Tampilan TV dan layar lain](#9-tampilan-tv-dan-layar-lain)
10. [Mutu data](#10-mutu-data)
11. [Penilaian dan periode](#11-penilaian-dan-periode)
12. [Replikasi plant](#12-replikasi-plant)
13. [Larangan tegas](#13-larangan-tegas)
14. [Status keputusan](#14-status-keputusan)
15. [Lampiran A — Pemetaan kode lama → nama aturan](#lampiran-a--pemetaan-kode-lama--nama-aturan)

---

## 1. Struktur, istilah, dan penomoran

| Istilah | Arti |
|---|---|
| **Group** | seluruh perusahaan; pemilik definisi dan perbandingan antar plant |
| **Plant** | satu lokasi produksi: **Snack, Exist Plant, New Plant, Dairy** |
| **BU / Factory** | unit di dalam plant (mis. Factory 10 di Exist Plant) |
| **Line** | baris produksi tempat papan dipasang: Snack 20 line, EP 59 line, NP 45 line |
| **Divisi / pilar** | pemilik bagian papan: SHE, Quality, Produksi, Delivery (PPIC), **Teknik** |
| **Shift** | 1, 2, 3 atau regu A/B/C sesuai pola plant |
| **Papan** | tampilan lima pilar untuk satu line pada satu tanggal dan shift |
| **Catatan** | satu sel isian papan: line + tanggal + shift + divisi + item |
| **Kasus** | kejadian yang perlu ditutup dengan sebab, tindakan, bukti, PIC |
| **Temuan** | keluaran sistem dari catatan/kasus (lewat tenggat, berulang, menumpuk, dst.) |
| **TV** | layar lantai tanpa login, terikat satu profil tampilan |

### Satu papan, satu catatan — WAJIB
Tidak ada angka kedua. Semua tampilan (TV, dasbor, laporan, ekspor) membaca catatan yang sama.

> **Komentar:** kalau muncul angka "hasil hitung ulang" di Excel atau dasbor terpisah, dua papan
> itu akan berbeda saat rapat — dan rapat habis untuk berdebat angka, bukan keputusan.

### Hierarki tetap: Group → Plant → BU/Factory → Line → Divisi — WAJIB
Line tidak boleh berpindah plant; kalau pindah, dibuat line baru dan yang lama diarsipkan.

> **Komentar:** hierarki adalah kunci semua filter di sistem. Sekali line pindah tanpa line baru,
> semua perbandingan antar plant rusak.

### Kode tetap, tidak dipakai ulang — WAJIB
`PLANT` (SN/EP/NP/DR) · `LINE` (SN-L09) · `KASUS` (SN-QC-0441) · `WORK ORDER` (EP-TK-0031) ·
`TV` (SN-L09-TV1) · `PERIODE` (2026-11). Kode yang sudah dipakai tidak boleh dipakai untuk entitas lain.

> **Komentar:** kode mengikat label di TV, nama berkas, dan arsip kasus; mengganti arti kode =
> menulis ulang sejarah.

### Satu hari satu papan — WAJIB
Untuk satu line + tanggal + shift hanya ada satu papan, walaupun diisi bergantian oleh beberapa divisi.

> **Komentar:** mencegah "papan 07.00" dan "papan 08.00" dengan angka berbeda untuk hari yang sama.

### Hari kerja Senin–Jumat — WAJIB
Dikurangi kalender libur plant. Sabtu/Minggu dan hari libur tidak dihitung sebagai hari wajib dan
tidak boleh menurunkan skor kepatuhan pengisian.

> **Komentar:** orang tidak boleh dihukum skor karena hari libur pabrik tutup.

### Nama line dan mesin diseragamkan — BAKU
Sebelum sistem dipakai, satu ejaan satu kode (`ws 02 / WS L02 / Line 2 hidup` adalah line yang sama).

> **Komentar:** nama yang tidak seragam = kasus yang tidak bisa dibandingkan antar bulan.

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
| **PDCA** *(v1.1)* | semua plant | lihat Dashboard ringkasan seluruh plant (A-02) |
| **TL (Team Leader)** *(v1.1)* | plant miliknya | lihat Dashboard ringkasan plant sendiri (A-02) |
| **TV Device** | satu profil tampilan | hanya menampilkan dan menerima ketukan absensi |

> **Komentar:** **PDCA** dan **TL** ditambahkan (24 Nov 2026) sebagai role akses **Dashboard ringkasan**,
> bukan peran pengisian data. Aturan akses permukaan aplikasi: **Landing untuk semua TV** (A-01) dan
> **Dashboard hanya PDCA (semua plant) & TL (plant miliknya)** (A-02) — lihat `docs/FRONTEND_STRUCTURE.md` §5.1.

### 2.2 Matriks hak

| Kemampuan | Leader | Petugas Divisi | Supervisor | DH | Kepala Divisi | Plant Head | Admin | Auditor | TV |
|---|---|---|---|---|---|---|---|---|---|
| Isi catatan papan divisi sendiri | ✅ line sendiri | ✅ wilayahnya | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| Isi catatan papan divisi lain | ⚠️ hanya item bertanda "boleh diisi leader" (lihat *Batas Leader*) | ❌ | ✅ koreksi | ✅ koreksi | ✅ koreksi | ❌ | ✅ | ❌ | ❌ |
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
| Lihat Dashboard ringkasan | ❌ | ❌ | ❌ | ❌ | ❌ | ⚠️ bila ditunjuk PDCA | ❌ | ❌ | ❌ |

> Kolom PDCA/TL disengaja dipisah dari pengisi papan: keduanya **hanya membaca Dashboard ringkasan**,
> tidak menulis data papan (A-02).

### Batas data per plant — WAJIB
Setiap akses data difilter `plant_id` (dan `line_id` untuk leader). Tidak ada peran yang bisa membaca
plant lain kecuali Admin Group, Auditor, dan PDCA (read-only).

> **Komentar:** salah filter `plant_id` = kebocoran data antar plant — kejadian nyata yang perlu ditolak sistem, bukan diingatkan di chat.

### Divisi hanya mengubah bagiannya — WAJIB
Petugas SHE tidak dapat mengubah sel QC, dan sebaliknya.

> **Komentar:** ini yang mencegah angka pilar ditimpa orang lain; pelanggaran paling halus biasanya "membantu mengisi milik divisi lain".

### Pemisahan isi dan setujui — WAJIB
Orang yang mengisi sebab tidak boleh menjadi satu-satunya yang menyetujui penutupan kasus. Minimal satu langkah persetujuan berasal dari peran berbeda.

> **Komentar:** cegah kasus "ditutup sendiri oleh pengisi" — semua alur tutup kasus wajib punya mata kedua.

### TV tidak punya hak ubah data papan — WAJIB
TV hanya menampilkan papan dan menerima ketukan absensi shift berjalan.

> **Komentar:** TV = layar bersama tanpa pemilik sesi; kalau bisa mengubah data, siapa pun di lantai bisa mengubah angka rapat.

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

### Satu sel satu pemilik — WAJIB
Setiap item papan punya tepat satu divisi pemilik. Item yang membutuhkan dua divisi dipecah menjadi dua item (lihat tabel Teknik di bawah).

> **Komentar:** satu sel dua pemilik = sel yang tidak pernah selesai diisi.

### Pengisian paralel — WAJIB
Papan boleh terisi sebagian. Bagian yang belum diisi ditandai **"belum diisi"** beserta jam terakhir pengecekan — bukan dibiarkan kosong tanpa keterangan.

> **Komentar:** kosong tanpa penjelasan tidak bisa dibedakan dari lupa; penanda + jam membuatnya bisa diaudit.

### Batas Leader — WAJIB
Leader line melihat semua pilar, mengubah hanya pilar Produksi. Kalau petugas divisi tidak ada di shift tersebut, leader boleh mengisi item divisi lain **hanya bila Admin menandai item itu "boleh diisi leader"**; kalau tidak, item tetap "belum diisi" dan menjadi temuan.

> **Komentar:** memberi leader hak penuh = menghapus kepemilikan divisi; memberi nol hak = papan Produksi terisi tapi SHE kosong.

### TV menampilkan bagian yang sudah masuk — BAKU
TV menampilkan bagian papan yang sudah masuk, dengan jam terakhir pembaruan di setiap pilar. Pilar yang belum diisi tidak dikosongkan, tetapi diberi tanda abu-abu "belum diisi".

> **Komentar:** TV tidak boleh terlihat "selesai" padahal separuh papan belum diisi.

### 3.1 Aturan khusus Teknik (Maintenance)

Teknik adalah pemilik **sebab teknis** dan **pencegahan**, bukan pencatat durasi line berhenti.
Pembagian ini yang membuat tidak ada dua orang mencatat hal yang sama.

| Langkah | Siapa | Yang dicatat | Batas waktu |
|---|---|---|---|
| 1. Line berhenti | Produksi (leader) | mesin, jam mulai, jam selesai, menit downtime, output hilang | saat kejadian |
| 2. Dipanggil | Produksi | tanda "menunggu teknik" | langsung |
| 3. Diagnosis & perbaikan | Teknik | kategori sebab (mekanik/elektrik/utilitas/setting/operator), komponen, tindakan (sementara/permanen), work order, spare part, teknisi | **≤ 4 jam** kategori A, ≤ 24 jam kategori B |
| 4. Serah terima | Teknik | mesin dinyatakan jalan / uji coba | setelah perbaikan |
| 5. Konfirmasi | Produksi | "normal" atau "masih bermasalah" (kasus dibuka kembali) | 1 shift berikutnya |

### Produksi mencatat durasi, Teknik mencatat sebab — WAJIB
Satu kejadian downtime hanya punya satu baris, diisi bertahap oleh dua divisi. Dilarang mencatat downtime di dua tempat.

> **Komentar:** dua baris untuk satu kejadian = dua angka downtime berbeda untuk line yang sama.

### Kategori sebab downtime terbatas lima — WAJIB
Mekanik · elektrik · utilitas · setting/changeover · operator/metode. Penyebab lain masuk "lain-lain" + penjelasan teks.

> **Komentar:** kategori standar adalah syarat membandingkan antar plant dan antar bulan.

### Ambang downtime menjadi kasus Teknik — WAJIB
Setiap downtime di atas ambang (BAKU: **30 menit per kejadian**) otomatis menjadi kasus Teknik dengan tenggat diagnosis. Di bawah ambang cukup tercatat sebagai angka.

> **Komentar:** ambang mencegah setiap berhenti mesin 5 menit membanjiri Teknik dengan kasus.

### Teknik tidak menunggu surat — WAJIB
Kasus downtime yang belum didiagnosis melewati batas waktu muncul di papan Teknik, dasbor, dan TV area teknik. Eskalasi ke Kepala Divisi Teknik setelah dua kali batas waktu.

> **Komentar:** kalau eskalasi hanya lewat pemberitahuan chat, yang tidak dibaca = tidak pernah terjadi.

### PM terjadwal — BAKU
Per mesin: daftar mesin, periode, item PM, penanggung jawab. Status hanya tiga: **selesai · tertunda (+alasan) · belum waktunya**. PM tertunda dua periode berturut = temuan berulang.

> **Komentar:** tiga status memaksa alasan tercatat, bukan centang abu-abu.

### Spare part kritis — BAKU
Daftar part kritis per mesin, stok minimum, dan status. Stok di bawah minimum menjadi kartu TV "tunggu part" dan harus punya rencana pengadaan.

> **Komentar:** part kosong lebih mahal dari kartu TV; kartu menjadikannya terlihat sebelum line berhenti lagi.

### Kalibrasi alat ukur — BAKU
(Milik QC, jadwal milik Teknik) alat, tanggal kalibrasi terakhir, jatuh tempo, sertifikat. Alat yang jatuh tempo tidak boleh dipakai untuk mengesahkan angka QC — sistem menandai angkanya.

> **Komentar:** satu alat kadaluarsa = semua angka QC shift itu kehilangan dasarnya.

### Jam mesin dan utilitas — SARAN
Listrik, udara tekan, steam, chiller dibaca harian bila tersedia dari mesin; kalau tidak, cukup dicatat kejadian anomali. Jangan menambah isian tanpa data.

> **Komentar:** kolom isian tanpa sumber data hanya melahirkan angka ketikan.

### Papan kedua di ruang teknik — SARAN
Mesin × status memakai data yang sama; tidak ada isian tambahan. Ini hanya tampilan berbeda dari catatan yang sama.

> **Komentar:** papan kedua adalah TV lain dari data yang sama, bukan papan baru.

---

## 4. Pengisian harian

### Satu isian per sel — WAJIB
Leader/petugas mengisi hasil; target dan satuan sudah menempel pada item, tidak diketik ulang. Isian yang sudah disimpan tidak perlu dikirim dua kali.

> **Komentar:** target yang diketik ulang = target yang berbeda antara pagi dan sore.

### Validasi sebelum simpan — WAJIB
Hasil wajib angka atau pilihan yang sah; kalau hasil di luar target, **sebab wajib diisi**; kalau sebab = "lain-lain", teks wajib diisi.

> **Komentar:** validasi yang mengizinkan "asal simpan" memindahkan masalah ke rapat; tolak saat itu juga.

### Cut-off per shift — WAJIB
Leader dapat mengubah catatan sampai **30 menit setelah shift berakhir**. Setelah itu catatan terkunci untuk leader (lihat bagian 6).

> **Komentar:** tanpa cut-off, angka pagi bisa berubah sore hari — dan rapat pagi berikutnya membahas angka yang sudah kadaluarsa.

### Hari tanpa aktivitas tetap diisi — WAJIB
Bila tidak ada kejadian, leader memilih "nihil" — bukan membiarkan kosong. Sistem membedakan **kosong** (belum diisi) dan **nihil** (sudah dikonfirmasi tidak ada kejadian).

> **Komentar:** "nihil" adalah jawaban yang sah; kosong adalah tugas yang belum selesai. Keduanya harus bisa dibedakan oleh sistem.

### Healthy Check — BAKU
Diisi Admin, bukan lapangan; nilainya konstan per periode.

> **Komentar:** konstan per periode mencegah angka sehat "diutak-atik ulang" tiap shift.

### Bukti foto — WAJIB
Ditempel pada kasus, bukan disimpan di ponsel. Satu kasus minimal satu bukti bila statusnya "ditutup".

> **Komentar:** bukti di ponsel hilang saat HP diganti; bukti di kasus bisa dicari siapa pun, kapan pun.

### Input dari satu tempat — WAJIB
Angka papan diisi dari tablet/PC line (atau HP bila mendesak). TV tidak dipakai untuk mengetik angka.

> **Komentar:** input dari tempat yang sama = jejak audit yang utuh; TV untuk melihat, bukan mengetik.

---

## 5. Absensi harian

### Daftar nama disiapkan Admin — WAJIB
Nama, regu/shift, line, divisi, dan masa berlaku. Impor dari file (Excel) dianjurkan; mengetik manual hanya untuk koreksi.

> **Komentar:** daftar diketik lapangan = nama ganda, regu salah, orang yang sudah resign tetap absen.

### Status awal "hadir" — WAJIB
Sistem mengisi seluruh daftar shift sebagai hadir, lalu lapangan hanya menandai yang **tidak hadir**: sakit · izin · alpa · dinas luar · terlambat.

> **Komentar:** menandai yang tidak hadir jauh lebih cepat & akurat daripada menandai 28 orang hadir satu per satu.

### Absensi dari TV, form web, atau QR — WAJIB
Ketiganya menulis ke catatan absensi yang sama — tidak ada rekap ulang. QR sesi (lihat *QR Satu Pintu*) adalah satu pintu masuknya.

> **Komentar:** tiga jalur, satu catatan; rekap manual = angka absensi versi kedua.

### Absensi shift berjalan & line miliknya — WAJIB
TV hanya bisa mengabsen shift berjalan dan line miliknya sendiri (terikat kode perangkat). Tanggal lampau tidak bisa diubah dari TV.

> **Komentar:** TV tamu tidak boleh mengabsen line lain.

### Setiap ketukan tercatat — WAJIB
Waktu, perangkat, dan (bila login) nama pengguna. Tersedia **Urungkan 2 menit** untuk salah ketuk.

> **Komentar:** ketukan yang tidak tercatat = koreksi yang tidak bisa diaudit; Urungkan 2 menit menampung salah tekan jari tanpa membuka jalur koreksi.

### Absensi menutup otomatis — BAKU
Pada cut-off shift; setelah itu hanya Supervisor/DH/Admin. Shift yang tidak pernah dikonfirmasi sampai cut-off ditandai **"belum dikonfirmasi"** — tidak dianggap hadir semua; penjelas output (lihat *Absensi = Penjelas Output*) hanya memakai absensi terkonfirmasi.

> **Komentar:** absensi yang menggantung diperlakukan sebagai "belum ada jawaban", bukan "semua hadir".

### Absensi = penjelas output — BAKU
Bila output di bawah target, sistem menampilkan jumlah hadir/total di samping angka output pada TV dan dasbor. Tidak perlu menulis sebab "orang kurang" secara manual.

> **Komentar:** angka tanpa konteks kehadiran memancing tuduhan; angka + hadir 19/28 adalah informasi.

### Absensi bukan alat menilai orang — WAJIB
Yang dipakai untuk KPI adalah kehadiran terkonfirmasi per shift dan kelengkapan pengisian, bukan peringkat individu.

> **Komentar:** begitu absensi jadi ranking orang, datanya mulai dimanipulasi.

### Absensi per line & shift default — SARAN
Bila sebuah divisi punya regu sendiri (mis. Teknik lintas line), Admin menandai divisi itu punya daftar absensi terpisah.

> **Komentar:** Teknik lintas line dengan daftar per line = orang teknik absen dua kali.

### Absensi dikerjakan lebih dulu — WAJIB
Saat sesi dibuka, TV tampil halaman Absensi dan isian divisi **belum bisa dikirim** sampai kehadiran sesi dikonfirmasi leader. Supervisor/DH boleh membuka isian bila absensi tertunda, dengan alasan tercatat di jejak audit.

> **Komentar:** angka tanpa tahu siapa yang mengerjakan = angka tanpa penanggung jawab; karena itu gerbang ini tidak bisa dilompati tanpa alasan tertulis.

### QR satu pintu — WAJIB
Satu QR per sesi mengikat plant · line · tanggal · shift, berputar tiap shift, dan dapat dicabut Admin. Semua peran masuk lewat tautan sesi yang sama (absensi → divisi → review → kunci); menulis tetap wajib login/SSO. QR bukan kanal baru dan bukan izin mengubah angka lampau.

> **Komentar:** satu QR = satu pintu; QR yang beredar di grup WA dicabut dan diganti per shift.

---

## 6. Tiga tingkat kunci dan aturan koreksi

| Status | Siapa yang boleh ubah | Kapan | Syarat |
|---|---|---|---|
| **Draf** | Leader / petugas divisi pemilik | selama shift + 30 menit | bebas, otomatis tercatat |
| **Terkunci** | Supervisor, DH, Kepala Divisi | sampai rapat pagi hari kerja berikutnya (BAKU 08.30, mengikuti jam rapat plant) | wajib **alasan koreksi**; nilai lama tetap tersimpan |
| **Arsip** | Admin Plant | setelah periode dikunci | koreksi menjadi **versi baru**, bukan menimpa |

### Koreksi tidak menghapus nilai lama — WAJIB
Riwayat: nilai, siapa, kapan, alasan.

> **Komentar:** angka yang "benar sejak awal" tidak bisa dipercaya; angka dengan riwayat bisa diaudit.

### Ambang koreksi besar — WAJIB
Koreksi di atas ambang (BAKU: perubahan > 5% atau mengubah status close) harus disetujui satu tingkat di atas pengoreksi. Untuk item **biner/pilihan/status**, setiap perubahan nilai dianggap "besar" (ambang 5% hanya berlaku untuk item angka).

> **Komentar:** memindahkan satu tanggal jatuh tempo mengubah warna seluruh kartu kasus; perubahan kecil membawa dampak besar.

### Periode dikunci — WAJIB
Setelah laporan bulanan disahkan. Periode terkunci hanya bisa dibuka Admin Plant dengan alasan, dan pembukaan tercatat di jejak audit.

> **Komentar:** laporan yang sudah disahkan tidak boleh bergeser senyap setelah dikirim Group.

### Sengketa angka saat rapat — WAJIB
Diselesaikan dengan urutan: bukti (foto/work order) → catatan mesin/absensi → kesepakatan plant head. Hasilnya dikoreksi lewat jalur koreksi di atas, bukan dengan mencatat angka baru di tempat lain.

> **Komentar:** sengketa tanpa urutan bukti = suara terkeras menang; urutan bukti membawa kembali fakta.

### Hapus data tidak tersedia — WAJIB
Tidak ada satu peran pun yang bisa menghapus; yang ada hanya pembatalan (batal) dengan alasan, dan arsip.

> **Komentar:** menghapus menghilangkan pelajaran; membatalkan menyisakan jejak.

---

## 7. Kasus, tenggat, dan eskalasi

### Empat kolom wajib sebelum kasus ditutup — WAJIB
Sebab · tindakan · bukti · PIC. Tombol "tutup" tidak aktif bila salah satu kosong.

> **Komentar:** kasus tanpa sebab = kasus yang berulang; kasus tanpa bukti = kasus yang tidak pernah bisa dipelajari.

### Setiap kasus punya tenggat — WAJIB
Dihitung sistem dari tingkat dampak, bukan diketik tangan. Tingkat dampak: **A** (lini berhenti/keselamatan) · **B** (mutu/hold) · **C** (administratif). Tenggat awal BAKU: A = 1 hari kerja, B = 3 hari kerja, C = 5 hari kerja. Tingkat dampak **ditetapkan otomatis dari jenis item/kejadian** (pemetaan di konfigurasi Admin); pengisi boleh mengusulkan naik, penurunan hanya oleh Supervisor ke atas dengan alasan.

> **Komentar:** tenggat ketikan tangan selalu "nanti saja"; tenggat sistem bisa dihitung dan dipantau.

### Kasus lewat tenggat naik otomatis — WAJIB
Saat tenggat lewat, kasus langsung naik ke **L2** (Supervisor/DH); setiap **2 hari kerja** keterlambatan berikutnya naik satu tingkat: **L3** (Plant Head) pada hari ke-2, masuk **laporan Group** pada hari ke-4. Kartu eskalasi tampil di TV area terkait dan dasbor tingkatnya.

> **Komentar:** eskalasi manual berhenti saat orang sibuk; eskalasi otomatis tidak.

### Berulang dihitung sistem — WAJIB
Kejadian dengan **signature** sama ≥ 3 kali dalam BAKU 90 hari menjadi **temuan berulang** dan wajib punya tindakan pencegahan, bukan hanya perbaikan. Signature = **(line, mesin/LBN, kategori sebab)**; teks problem bebas tidak dipakai sebagai kunci.

> **Komentar:** manusia malas menyadari pola ke-3; sistem tidak.

### Penutupan butuh persetujuan — WAJIB
Satu tingkat di atas pengaju. Bila pengaju **Plant Head**, penyetuju adalah **Admin Group**; bila pengaju Admin Plant satu-satunya, penyetuju adalah Plant Head. Tidak ada peran yang menyetujui pengajuannya sendiri.

> **Komentar:** aturan ini menutup celah "saya tutup sendiri, tidak ada yang melihat".

### Kasus tanpa aktivitas 14 hari = dingin — BAKU
Ditandai "dingin" dan dipertanyakan pada rapat berikutnya; bukan langsung ditutup.

> **Komentar:** kasus dingin = prioritas yang mati; menanyakan ulang lebih murah daripada menutupnya.

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

### Satu angka per catatan — WAJIB
Tidak ada jalur kedua untuk memasukkan angka yang sama.

> **Komentar:** kalau ada dua jalur, dua jalur itu akan berbeda hasil.

### Data historis tidak ikut berubah — WAJIB
Target baru berlaku untuk periode berikutnya; periode lalu tetap memakai versi lamanya.

> **Komentar:** menilai Desember dengan target Januari = ketidakadilan terstruktur.

### Setiap perubahan konfigurasi tercatat — WAJIB
Siapa, kapan, sebelum–sesudah.

> **Komentar:** konfigurasi yang berubah senyap = angka yang berubah tanpa sebab.

### Rumus penilaian tidak boleh diubah per pengguna — WAJIB
Yang bisa diubah hanya parameter yang tercantum di 8.1, dan setiap perubahan harus memperlihatkan simulasi dampak sebelum disimpan.

> **Komentar:** satu rumus per orang = satu kebenaran per orang.

---

## 9. Tampilan TV dan layar lain

### TV berbentuk papan — WAJIB
Kepala papan (plant, line, tanggal, shift), grid KPI (target vs realisasi per shift), tabel kasus, dan baris PICA — **satu divisi per layar** (lihat *Satu Divisi per Layar*), sel dengan warna status dibanding target.

> **Komentar:** TV bukan galeri kartu; TV adalah representasi satu papan fisik.

### TV tanpa login dan interaksi — WAJIB
Kecuali panel absensi.

> **Komentar:** setiap klik ekstra di TV = peluang salah sentuh untuk seluruh shift.

### TV terikat satu profil — WAJIB
Kode perangkat. TV tidak punya kolom pencarian plant/line.

> **Komentar:** kolom pencarian membuat TV bisa menampilkan data plant lain — kebocoran by accident.

### Angka papan tidak diubah dari TV — WAJIB
TV bukan alat ketik.

> **Komentar:** input dari TV menghilangkan lineage; input dari tablet line menjaga audit.

### Rotasi halaman TV — BAKU
**Absensi (saat sesi dibuka) → SHE → Quality → Produksi → Delivery → Teknik → Ringkasan/DMS Index**, lalu ulang. BAKU 20–30 detik per halaman; urutan, durasi, dan halaman aktif diatur Admin lewat profil TV.

> **Komentar:** rotasi = semua divisi dapat waktu layar yang sama tanpa papan penuh lima kolom yang tidak terbaca.

### TV menunjukkan kesegaran data — WAJIB
Jam pembaruan terakhir dan tanda "data kemarin" bila hari ini belum ada isian. TV tidak boleh terlihat seperti angka hari ini padahal masih kemarin.

> **Komentar:** angka lama yang terlihat baru lebih berbahaya dari angka kosong.

### Layar PC/admin — WAJIB
Dasbor L1–L3 dan halaman admin (ubah aturan, koreksi, kunci periode, profil TV). Hanya dari sini data dan aturan boleh diubah.

> **Komentar:** layar bersama = baca; layar admin = tulis (dengan jejak).

### Empat kanal tetap — BAKU
Form/tablet isian · dasbor L1–L3 · TV lantai · halaman admin. Menambah kanal baru harus lewat aturan, bukan aplikasi terpisah. QR sesi adalah pintu masuk kanal isian, bukan kanal kelima.

> **Komentar:** kanal kelima yang "sementara" berumur selamanya.

### Satu divisi per layar — WAJIB
TV menampilkan satu divisi penuh per halaman dengan penanda halaman (`Halaman 4/6`), bukan papan gabungan. Lebih detail, kolom lengkap, tetap terbaca 3–10 m.

> **Komentar:** lima kolom kecil di satu layar terbaca 0 orang dari 8 meter.

### Kolom TV & form mengikuti kontrak kolom Excel — WAJIB
Kolom mengikuti divisi yang bersangkutan (`Resume SHE`, `Resume QC`, `Resume Prod`). Kolom baru yang muncul di Excel **tidak otomatis tampil**: masuk staging dan diberitahukan ke Admin untuk dipetakan lebih dulu.

> **Komentar:** kolom liar di Excel tidak boleh membobol tata letak TV.

### Kolom statis, isi dinamis — BAKU
Daftar kolom tetap sesuai kontrak; baris kasus, angka, dan target berubah mengikuti tanggal/shift. Divisi tanpa data hari itu **tetap tampil** dengan tanda "belum diisi" — tidak dilewati diam-diam.

> **Komentar:** melewati pilar yang kosong membuat orang mengira pilar itu tidak ada.

### Setiap angka membawa sumber dan waktu — WAJIB
TV dan dasbor menampilkan badge sumber (`Excel` / `Aplikasi`) serta jam sinkron terakhir, selain jam pembaruan.

> **Komentar:** "Excel, 06.31" mengalahkan "6.31" telanjang.

---

## 10. Mutu data

### Kolom wajib tidak boleh kosong — WAJIB
Pesan kesalahan menyebut nama kolom.

> **Komentar:** "gagal simpan" tanpa nama kolom = tiket komplain.

### Nilai di luar batas wajar ditolak — WAJIB
Mis. downtime lebih besar dari jam shift.

> **Komentar:** menangkap salah ketik saat isi jauh lebih murah daripada saat rapat.

### Sel error tidak disimpan — WAJIB
Tidak ada `#VALUE!`, `#N/A`, atau teks bebas di kolom angka.

> **Komentar:** satu sel error menular ke semua rumus yang membacanya.

### Satu nilai tidak ditulis ganda — WAJIB
Nilai diambil dari konfigurasi, bukan dari sel (contoh kegagalan: satu blok bernilai 0,6 di satu plant dan 3,0 di plant lain akibat salin manual).

> **Komentar:** nilai ketikan tangan selalu berbeda antar plant.

### Tanggal wajib menempel pada ringkasan — WAJIB
Ringkasan tanpa tanggal dianggap tidak sah dan tidak dipakai untuk perbandingan.

> **Komentar:** ringkasan tanpa tanggal adalah artefak rapat lama yang tersesat.

### Ringkasan dihitung dari baris kasus — BAKU
Bukan diketik. Selisih ringkasan vs isi tabel (saat ini sampai dua kali lipat) tidak boleh terulang.

> **Komentar:** ringkasan ketikan = ringkasan yang tidak akan pernah cocok.

### Kelengkapan diukur dan ditampilkan — WAJIB
Persen item terisi per line per hari, per divisi. Inilah ukuran mutu data yang dipakai rapat, bukan perasaan.

> **Komentar:** "terasa rapi" bukan ukuran; 78% terisi adalah ukuran.

### Integrasi Excel otomatis, satu arah, terus-menerus — WAJIB
Petugas tetap mengisi workbook di laptopnya seperti biasa; sistem membaca setiap perubahan dan memperbarui basis data **tanpa upload manual**. Excel **tidak pernah dibekukan** dan tidak ada cutover. Aplikasi **tidak menulis** ke workbook. Baris yang hilang dari Excel ditandai "terhapus di sumber", tidak dihapus permanen. Folder kerja dipindah ke OneDrive **satu kali oleh IT** dengan *junction* di path lama.

> **Komentar:** begitu diminta upload, petugas berhenti — upload adalah langkah tambahan; lihat *Nol Langkah Tambahan*.

### Satu berkas per divisi — BAKU
Tiap divisi memakai Excel-nya sendiri dan didaftarkan di daftar sumber (plant · line · divisi · path lama · ID cloud · sheet · peta kolom). Delivery dan Teknik **cukup didaftarkan**, bukan dibuatkan form baru. Satu berkas gagal tidak menahan divisi lain. ID cloud dipakai sebagai kunci agar file yang di-rename tidak memutus sinkron.

> **Komentar:** gagalnya SHE tidak boleh menahan Quality.

### Nol langkah tambahan bagi petugas — WAJIB
Sistem tidak boleh meminta petugas mengunggah file, mengekspor CSV, mengirim lampiran, menyalin ke folder lain, atau mengisi ulang data yang sudah ada di Excel. Bila sebuah rancangan menuntut langkah tambahan dari petugas, rancangan itu yang harus berubah — bukan petugasnya.

> **Komentar:** setiap langkah tambahan adalah titik kegagalan kepatuhan.

### Kepemilikan kolom — WAJIB
Kolom yang ada di Excel divisi itu dimiliki Excel dan **baca-saja** di aplikasi; koreksi dilakukan di Excel dan aplikasi menyusul otomatis. Aplikasi hanya memiliki kolom yang tidak ada di Excel (absensi, konfirmasi sesi, jejak audit, eskalasi, tenggat, foto tambahan, persetujuan, skor proses). Tidak ada satu kolom pun ditulis di dua tempat — tidak ada konflik, tidak perlu masa transisi. Untuk kolom milik Excel, aplikasi menampilkan **"Perbaiki di Excel"** beserta nama berkas dan barisnya.

> **Komentar:** kepemilikan yang jelas = tidak ada rebutan siapa yang "membetulkan" angka.

### Angka membawa sumber dan waktu — WAJIB
Lihat *Setiap Angka Membawa Sumber dan Waktu* di bagian TV; aturan yang sama berlaku untuk ekspor dan laporan.

> **Komentar:** angka tanpa sumber di laporan = angka yang dipercaya sekali lalu menagih dua kali.

### Status berkas jujur — WAJIB (**diperbaiki v1.1**)
TV/aplikasi **wajib membedakan empat keadaan** berikut (bukan cuma "kosong" atau "terisi"), dan **wajib menampilkan jam** kapan terakhir sistem berhasil membaca/mengecek sumber:

| # | Status | Arti sebenarnya | Yang wajib tampil di TV/aplikasi |
|---|---|---|---|
| 1 | **`tersinkron`** | Berkas terdaftar, sinkron terakhir berhasil, ada baris bertanggal untuk tanggal yang ditampilkan | Angka + badge sumber + jam sinkron terakhir |
| 2 | **`belum_diisi`** | Berkas **terbaca normal**, sinkron berhasil, hanya saja **tidak ada baris untuk tanggal itu** | Tag "belum diisi" + **jam terakhir pengecekan** — bukan angka nol (seolah "0 kasus") dan bukan data kosong tanpa keterangan |
| 3 | **`belum_tersinkron`** | Berkas **terdaftar tetapi gagal/ belum pernah terbaca** (laptop mati, folder OneDrive belum sync, sheet salah, error formula) | Tag "belum tersinkron" + **jam sinkron terakhir yang berhasil** + pesan penyebab (dari daftar sumber/log) — angka terakhir (bila ada) ditampilkan **dengan cap "data terakhir hh.mm — belum diperbarui"** |
| 4 | **`menunggu_berkas`** | Berkas divisi **belum didaftarkan** sama sekali (mis. Delivery/Teknik/plant Dairy yang belum punya sumber) | Tag "menunggu berkas" + daftar berkas yang diharapkan / ajakan daftarkan di daftar sumber (*Satu Berkas per Divisi*) |

Ketentuan tambahan:

1. **Frasa baku untuk kasus 3:** tampilkan persis **"belum tersinkron · terakhir HH.MM"** (atau "belum pernah tersinkron" bila memang belum pernah berhasil). Dilarang menulis "belum diisi" untuk kasus 3 — keduanya berbeda arti.
2. **Angka basi tetap boleh tampil, tapi tidak boleh berpura-pura segar** — cap waktu wajib menyertainya (lihat *TV Menunjukkan Kesegaran Data*).
3. **Pulih otomatis:** begitu sinkron berhasil lagi, halaman kembali `tersinkron` pada putaran refresh berikutnya — tanpa campur tangan manual.
4. **Tidak boleh ada baris hilang** saat transisi status; perubahan yang tertunda wajib tersusul saat online (upsert idempoten + baris hilang ditandai "terhapus di sumber", tidak dihapus permanen).
5. **Satu divisi gagal tidak menahan divisi lain** (*Satu Berkas per Divisi*), dan satu berkas gagal tidak menjadikan papan terlihat "kosong" — hanya divisi itu yang berstatus kasus 3.
6. **"Belum diisi" tidak dihitung sebagai kesalahan sinkron**; sebaliknya, kegagalan sinkron tidak boleh ditampilkan sebagai "nihil".

> **Komentar:** aturan lama hanya punya dua kata ("belum diisi" / "belum tersinkron") dan tidak mewajibkan jam tampil, sehingga TV bisa menampilkan halaman abu-abu tanpa informasi. Aturan v1.1 mewajibkan: (a) empat keadaan yang bisa dibedakan sistem dari data registry + hasil sinkron + baris tanggal, (b) jam acuan di setiap halaman, (c) angka basi yang tidak berpura-pura segar. Aturan ini mengikat frontend (`EmptyState`/`StatusPill`), backend (`bangun_halaman`), dan rapat pagi (bedah status, bukan angka).
>
> **Catatan implementasi saat ini (jujur):** backend sudah membedakan empat status di atas di `app/server.py::bangun_halaman`, tetapi belum menampilkan "jam terakhir pengecekan" pada status `belum_diisi` dan belum memisahkan "gagal sync terakhir" dari "belum pernah sync" untuk pesan kasus 3. Perbaikan backend mengikuti tahap B (error JSON terstruktur) & tahap D (health check) di `BACKEND_PLAN.md` — dokumen ini adalah spesifikasi yang harus diikuti.

---

## 11. Penilaian dan periode

### KPI V/O biner — WAJIB
Tercapai / tidak, tanpa nilai antara yang bisa ditawar.

> **Komentar:** ambang biner menghilangkan ruang tawar "0,74 vs 0,75".

### Skor proses dan hasil dipisah — BAKU
Proses = kelengkapan dan ketepatan waktu pengisian; hasil = pencapaian target pilar. Keduanya dilaporkan berdampingan, tidak digabung menjadi satu angka yang menutupi masalah.

> **Komentar:** satu angka gabungan menyembunyikan apakah masalahnya di kepatuhan atau di hasil.

### Perhitungan memakai hari wajib — BAKU
Senin–Jumat dikurangi kalender libur; hari tanpa kewajiban tidak dihitung.

> **Komentar:** libur tidak boleh menjadi alasan skor turun.

### Status N/A — BAKU
Dipakai bila item memang tidak berlaku untuk line tersebut (mis. line tanpa proses tertentu); N/A tidak dihitung sebagai tidak tercapai.

> **Komentar:** N/A adalah pernyataan "tidak berlaku", bukan "gagal".

### Angka rapat dan KPI berasal dari catatan — WAJIB
Bukan dari rekap manual.

> **Komentar:** satu rapat dengan dua angka = rapat tanpa keputusan.

### Angka impor historis bertanda historis — SARAN
17.201 kasus dari tiga workbook masuk sebagai arsip bertanda "historis" agar bisa dibandingkan, tanpa mencampur mutu datanya dengan data baru. Kasus historis **tidak memicu kartu TV, eskalasi, atau temuan**; masuk laporan kualitas-data terpisah dan program pembersihan bertahap dengan PIC.

> **Komentar:** menghukum masa lalu dengan aturan baru = data historis tidak akan dipercaya lagi.

---

## 12. Replikasi plant

### Urutan replikasi — BAKU
Snack (pilot 8 pekan) → Exist Plant (4 pekan) → New Plant (4 pekan) → **Dairy (4 pekan)**.

> **Komentar:** Dairy adalah plant keempat dan belum memiliki berkas sumber — sampai didaftarkan, seluruh halamannya tampil "menunggu berkas" (lihat *Status Berkas Jujur*).

### Gerbang sebelum replikasi — WAJIB
Data master bersih · angka sistem cocok dengan workbook atau selisihnya terjelaskan penuh dalam laporan rekonsiliasi · aturan jalan satu periode penuh · **lima ukuran keberhasilan** (hari terisi, sebab lengkap, tenggat tercatat, kasus lewat tenggat, pola berulang) terpenuhi di pilot.

> **Komentar:** replicating kekacauan ke plant keempat hanya memperluas kekacauan.

### Yang dibawa saat replikasi — BAKU
Master line & mesin, template item dan target (versi baru per plant), aturan insight, profil TV.

> **Komentar:** membawa template = tidak mulai dari nol; membawa target = membawa konteks yang salah.

### Yang tetap lokal — WAJIB
Target plant, kalender libur, daftar nama & regu, PIC dan jalur persetujuan.

> **Komentar:** yang lokal tidak boleh dipaksakan dari template grup.

---

## 13. Larangan tegas

1. Mencatat angka yang sama di dua tempat (papan + Excel + grup WA). Excel tetap pemilik kolomnya dan aplikasi hanya membaca (lihat *Kepemilikan Kolom*), jadi tidak ada pencatatan ganda.
2. Menutup kasus tanpa sebab, tindakan, bukti, dan PIC.
3. Mengubah angka periode yang sudah dikunci tanpa jejak.
4. Mengetik angka papan dari TV.
5. Menghapus data (hanya batal/arsip).
6. Memakai TV untuk keperluan selain menampilkan papan dan absensi.
7. Menilai orang memakai absensi di dalam sistem (lihat *Absensi Bukan Alat Menilai Orang*).
8. Menyimpan sel error atau teks bebas di kolom angka.
9. Membuat aplikasi atau file baru di luar empat kanal (lihat *Empat Kanal Tetap*).
10. Menyebut pekerjaan manual sebagai kesalahan orang; yang dinilai adalah pekerjaan yang hilang.

---

## 14. Status keputusan

**Tiga keputusan diminta pada rapat persetujuan** (deck hal. 27). Sampai rapat memutuskan, nilai
BAKU di aturan tetap berlaku; bila rapat memilih lain, aturan direvisi sebagai versi baru
(lihat *Setiap Perubahan Konfigurasi Tercatat*). Tiga pertanyaan tambahan tentang TV &
integrasi Excel **sudah dijawab plant pada 6 Nov 2026**.

| No | Pertanyaan | Pilihan | Nilai berlaku sekarang |
|---|---|---|---|
| 1 | Cut-off edit leader | 30 menit · 60 menit · sampai akhir shift | 30 menit (lihat *Cut-off per Shift*) |
| 2 | Ambang downtime jadi kasus Teknik | 30 menit · 60 menit · per mesin | 30 menit (lihat *Ambang Downtime Menjadi Kasus Teknik*) |
| 3 | Sumber nama absensi | Admin ketik · impor Excel · tarik dari mesin absensi | impor Excel dianjurkan (lihat *Daftar Nama Disiapkan Admin*) |

**Sudah diputuskan** (tidak dibuka lagi):

| Pertanyaan | Keputusan | Rujukan |
|---|---|---|
| Daftar divisi final | 5 divisi: SHE, Quality, Produksi, Delivery, Teknik | §3, *Satu Sel Satu Pemilik* |
| Koreksi angka dari TV | Tidak; TV hanya tampil + absensi | *Angka Papan Tidak Diubah dari TV*, *TV Tidak Punya Hak Ubah Data Papan* |
| Absensi per line vs per divisi | Default per line; divisi lintas line boleh daftar terpisah atas tanda Admin | *Absensi per Line & Shift Default* |
| Status absensi | hadir · sakit · izin · alpa · terlambat · dinas luar | §5, *Status Awal "hadir"* |
| Item checklist | Ditetapkan dari papan Factory 10, dilengkapi bertahap oleh Admin | §8.1 |
| Retensi | Kasus & catatan ≥ 5 tahun; foto mengikuti kasusnya | rancangan/02 §7 |
| Kalender libur | Master tahunan per plant, dipelihara Admin | *Hari Kerja Senin–Jumat* |
| N/A item | Dari konfigurasi item per line, bukan diketik saat mengisi | *Status N/A* |
| Impor historis | Masuk berflag historis; tidak ke TV/eskalasi | *Angka Impor Historis Bertanda Historis* |
| Tempat file Excel | Masih di laptop petugas → folder dipindah ke OneDrive sekali oleh IT, junction di path lama | *Integrasi Excel Otomatis* |
| Sumber Delivery & Teknik | Tiap divisi sudah punya Excel sendiri → cukup didaftarkan, bukan form baru | *Satu Berkas per Divisi* |
| Pembekuan Excel | **Tidak dibekukan.** Excel dipakai terus, sinkron setiap saat; yang dibagi adalah kepemilikan kolom | *Integrasi Excel Otomatis*, *Kepemilikan Kolom* |
| Usaha petugas | Nol langkah tambahan; dilarang meminta upload/ekspor/isi ulang | *Nol Langkah Tambahan bagi Petugas* |

---

## Lampiran A — Pemetaan kode lama → nama aturan

Kode ini **tidak dipakai lagi** di UI/dokumen baru. Disimpan hanya untuk rujukan ke dokumen lama (deck, laporan v1, skrip).

| Kode | Nama aturan (v1.1) | Kode | Nama aturan (v1.1) |
|---|---|---|---|
| R-01 | Satu papan, satu catatan | R-46 | Setiap kasus punya tenggat |
| R-02 | Hierarki tetap | R-47 | Kasus lewat tenggat naik otomatis |
| R-03 | Kode tetap, tidak dipakai ulang | R-48 | Berulang dihitung sistem |
| R-04 | Satu hari satu papan | R-49 | Penutupan butuh persetujuan |
| R-05 | Hari kerja Senin–Jumat | R-50 | Kasus tanpa aktivitas 14 hari = dingin |
| R-06 | Nama line & mesin diseragamkan | R-51 | Satu angka per catatan |
| R-07 | Batas data per plant | R-52 | Data historis tidak ikut berubah |
| R-08 | Divisi hanya mengubah bagiannya | R-53 | Setiap perubahan konfigurasi tercatat |
| R-09 | Pemisahan isi dan setujui | R-54 | Rumus penilaian tidak boleh diubah per pengguna |
| R-10 | TV tidak punya hak ubah data papan | R-55 | TV berbentuk papan |
| R-11 | Satu sel satu pemilik | R-56 | TV tanpa login dan interaksi |
| R-12 | Pengisian paralel | R-57 | TV terikat satu profil |
| R-13 | Batas Leader | R-58 | Angka papan tidak diubah dari TV |
| R-14 | TV menampilkan bagian yang sudah masuk | R-59 | Rotasi halaman TV |
| R-15 | Produksi mencatat durasi, Teknik sebab | R-60 | TV menunjukkan kesegaran data |
| R-16 | Kategori sebab downtime terbatas lima | R-61 | Layar PC/admin |
| R-17 | Ambang downtime menjadi kasus Teknik | R-62 | Empat kanal tetap |
| R-18 | Teknik tidak menunggu surat | R-63 | Kolom wajib tidak boleh kosong |
| R-19 | PM terjadwal | R-64 | Nilai di luar batas wajar ditolak |
| R-20 | Spare part kritis | R-65 | Sel error tidak disimpan |
| R-21 | Kalibrasi alat ukur | R-66 | Satu nilai tidak ditulis ganda |
| R-22 | Jam mesin dan utilitas | R-67 | Tanggal wajib menempel pada ringkasan |
| R-23 | Papan kedua di ruang teknik | R-68 | Ringkasan dihitung dari baris kasus |
| R-24 | Satu isian per sel | R-69 | Kelengkapan diukur dan ditampilkan |
| R-25 | Validasi sebelum simpan | R-70 | KPI V/O biner |
| R-26 | Cut-off per shift | R-71 | Skor proses dan hasil dipisah |
| R-27 | Hari tanpa aktivitas tetap diisi | R-72 | Perhitungan memakai hari wajib |
| R-28 | Healthy Check | R-73 | Status N/A |
| R-29 | Bukti foto | R-74 | Angka rapat dan KPI berasal dari catatan |
| R-30 | Input dari satu tempat | R-75 | Angka impor historis bertanda historis |
| R-31 | Daftar nama disiapkan Admin | R-76 | Urutan replikasi (Snack→EP→NP→Dairy) |
| R-32 | Status awal "hadir" | R-77 | Gerbang sebelum replikasi |
| R-33 | Absensi dari TV, form web, atau QR | R-78 | Yang dibawa saat replikasi |
| R-34 | Absensi shift berjalan & line miliknya | R-79 | Yang tetap lokal |
| R-35 | Setiap ketukan tercatat | R-80 | Satu divisi per layar |
| R-36 | Absensi menutup otomatis | R-81 | Absensi dikerjakan lebih dulu |
| R-37 | Absensi = penjelas output | R-82 | QR satu pintu |
| R-38 | Absensi bukan alat menilai orang | R-83 | Kolom TV & form mengikuti kontrak Excel |
| R-39 | Absensi per line & shift default | R-84 | Kolom statis, isi dinamis |
| R-40 | Koreksi tidak menghapus nilai lama | R-85 | Integrasi Excel otomatis, satu arah |
| R-41 | Ambang koreksi besar | R-86 | Satu berkas per divisi |
| R-42 | Periode dikunci | R-87 | Angka membawa sumber dan waktu |
| R-43 | Sengketa angka saat rapat | R-88 | Nol langkah tambahan bagi petugas |
| R-44 | Hapus data tidak tersedia | R-89 | Kepemilikan kolom |
| R-45 | Empat kolom wajib sebelum kasus ditutup | R-90 | Status berkas jujur (**diperbaiki v1.1**) |

*Dokumen Sources: Aturan Sistem v1 (6 Nov 2026) — isi normatif dipertahankan; penulisan v1.1 (24 Nov 2026).*
