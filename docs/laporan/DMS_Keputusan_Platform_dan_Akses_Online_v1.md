# Keputusan Platform & Akses Online — DMS

**Tanggal:** 6 November 2026 · **Status:** rekomendasi untuk dibahas, belum diputuskan
**Pemicu:** pertanyaan "pakai Power Automate atau buat dari awal?" + kebutuhan **akses dari mana-mana,
beda jaringan**, dengan **20–50 pengguna**, kapasitas pengembangan **belum diketahui**.

Melengkapi `DMS_TV_PerDivisi_dan_Integrasi_Excel_v1.md` dan `rancangan/02-RANCANGAN-APLIKASI.md`.

---

## 0. Rekomendasi satu paragraf

**Lanjutkan aplikasi sendiri (prototipe di `app/`), jangan bangun ulang di Power Platform.**
Power Automate tetap dipakai — tetapi hanya untuk notifikasi Teams/email/pengingat tenggat yang
memakai konektor standard dan **sudah termasuk M365**. Untuk kabel Excel→aplikasi, pakai pengawas
folder (sudah jalan) lalu naik ke **Microsoft Graph delta** yang tidak berlisensi per pengguna.
Akses online lewat **HTTPS publik + login akun M365 (Entra ID)**, dengan TV dibuat tahan putus internet.

---

## 1. Alasan penentu: aplikasi ini bukan aplikasi formulir

Ini yang paling sering terlewat. Karena **Excel tidak pernah dibekukan** (Sinkron Excel Otomatis) dan **kolom milik
Excel baca-saja di aplikasi** (Kepemilikan Kolom), maka:

| Yang biasa jadi kekuatan Power Apps | terpakai di DMS? |
|---|---|
| Membuat formulir input dengan cepat | **hampir tidak** — petugas tetap mengisi di Excel |
| Approval berjenjang | sedikit (bisa lewat Power Automate saja) |
| Aplikasi mobile untuk input | tidak — mobile hanya untuk absensi & lihat |

Yang justru dibutuhkan DMS:

1. **Pembaca Excel** yang tahan header bergeser, tanggal 5 format, PIC berupa tautan, sel error.
2. **Mesin aturan** — 90 aturan bernomor, 12 kartu insight, tenggat, eskalasi, skor, kunci periode.
3. **Layar TV** yang menyegar 20–30 detik, rotasi per divisi, dan bisa diketuk untuk absensi.

Ketiganya adalah bagian yang Power Platform **paling lemah**, bukan paling kuat. Membangun DMS di
Power Platform berarti membayar lisensi untuk kekuatan yang tidak kita pakai, lalu tetap membuat
bagian tersulit secara custom.

---

## 2. Tiga lapisan, bukan dua pilihan

| Lapisan | Isi | Pilihan terbaik | Alasan |
|---|---|---|---|
| **1 · Kabel** | tahu berkas berubah → ambil isinya | pengawas folder → **Graph delta** | Graph tanpa lisensi per pengguna; Power Automate kena premium bila memakai aksi HTTP |
| **2 · Otak** | aturan, sesi, tenggat, eskalasi, skor, audit | **aplikasi sendiri** | 90 aturan perlu bisa diuji otomatis; sulit dirawat sebagai flow |
| **3 · Layar** | TV per divisi, dasbor, laporan | **aplikasi sendiri** | Power BI tidak bisa 20–30 detik pada lisensi wajar (§3) |
| **Sampingan** | notifikasi Teams, email, pengingat | **Power Automate** | konektor standard, sudah dibayar M365 |

---

## 3. Fakta lisensi yang memengaruhi keputusan

Harga daftar (list price, bayar tahunan). **Perlu dikonfirmasi ke reseller Microsoft** — diskon
perjanjian perusahaan bisa berbeda.

| Fakta | Angka | Sumber |
|---|---|---|
| Aksi **HTTP** adalah premium connector; satu langkah premium membuat **seluruh flow** premium | — | [1](https://kpbsolutions.io/en/guides/power-automate-licensing), [2](https://nordflux.de/en/insights/power-automate-premium-connector-costs) |
| Power Automate Premium | **$15 / pengguna / bulan** | [1](https://kpbsolutions.io/en/guides/power-automate-licensing), [3](https://alphavima.com/blog/power-platform-pricing/) |
| Power Automate Process (kapasitas per flow) | **$150 / bot / bulan** | [4](https://a8gent.com/platforms/power-automate) |
| Power Apps Premium | **$20 / pengguna / bulan** | [3](https://alphavima.com/blog/power-platform-pricing/) |
| Power Apps per-app (paket lama, lebih murah) | **$5 / pengguna / app / bulan** | [5](https://www.qservicesit.com/power-platform-premium-connectors-standard) |
| Power BI Pro | **$14 / pengguna / bulan**, **8 refresh/hari** | [6](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-scheduled-refresh), [7](https://www.epcgroup.net/blog/power-bi-pro-vs-premium-per-user-comparison) |
| Power BI Premium per user | **$24 / pengguna / bulan**, **48 refresh/hari** (tercepat 30 menit) | [3](https://alphavima.com/blog/power-platform-pricing/), [6](https://learn.microsoft.com/en-us/power-bi/connect-data/refresh-scheduled-refresh) |
| Konektor standard (SharePoint, OneDrive, Excel Online, Outlook, Teams) | **termasuk M365** | [1](https://kpbsolutions.io/en/guides/power-automate-licensing), [5](https://www.qservicesit.com/power-platform-premium-connectors-standard) |

**Benturan langsung dengan kebutuhan kita:** TV harus menyegar **20–30 detik**. Power BI Pro
8×/hari berarti data bisa basi ~3 jam; PPU 48×/hari berarti paling cepat 30 menit — dan untuk
lantai produksi 30 menit masih dinilai kurang [7](https://www.epcgroup.net/blog/power-bi-pro-vs-premium-per-user-comparison).
Jalur real-time Power BI (DirectQuery/streaming) menuntut database SQL, artinya aplikasi tetap
harus dibangun [7](https://www.epcgroup.net/blog/power-bi-pro-vs-premium-per-user-comparison).

**Contoh jebakan biaya:** satu langkah HTTP mengubah tim 5 orang dari $0 menjadi $900/tahun
[4](https://a8gent.com/platforms/power-automate).

---

## 4. Perhitungan biaya · 20–50 pengguna

Asumsi terbuka: 10 orang membuka dasbor (sisanya membuka TV yang tidak perlu lisensi pengguna);
1 flow otomatis dengan satu pemilik. Semua angka **per bulan, harga daftar USD**.

### Skenario A — Power Platform penuh

| Komponen | 20 pengguna | 35 pengguna | 50 pengguna |
|---|---|---|---|
| **A1 · hemat** (Apps per-app $5 + Automate $15 + BI Pro 10×$14) | **$255** | **$330** | **$405** |
| **A2 · penuh** (Apps Premium $20 + Automate $15 + PPU 10×$24) | **$655** | **$955** | **$1.255** |
| Setahun A1 | $3.060 | $3.960 | $4.860 |
| Setahun A2 | $7.860 | $11.460 | $15.060 |

Belum termasuk: kapasitas Dataverse tambahan (15.940 kasus + foto akan melewati kuota bawaan),
dan **TV tetap tidak bisa 20–30 detik** tanpa membangun database + DirectQuery sendiri.

### Skenario B — aplikasi sendiri

| Komponen | Biaya |
|---|---|
| Lisensi per pengguna | **$0** |
| Server kecil (VM 2 vCPU / 4 GB) + cadangan | **±$30/bulan** *(perkiraan kasar, perlu dicek ke penyedia)* |
| Domain | subdomain perusahaan — $0 |
| Sertifikat HTTPS | Let's Encrypt / disediakan tunnel — $0 |
| Login | akun M365 yang sudah ada (Entra ID) — tanpa lisensi aplikasi per pengguna |
| Power Automate untuk notifikasi Teams/email | konektor standard — **sudah termasuk M365** |
| **Setahun** | **±$360** + waktu pengembangan |

**Selisih berulang:** ±$2.700–14.700 per tahun, tergantung skenario. Dalam 3 tahun, selisih itu
membiayai banyak waktu pengembangan. Biaya sesungguhnya skenario B adalah **orang**, bukan lisensi.

---

## 5. Karena kapasitas dev belum tahu — aturan keputusannya

| Keadaan | Pilihan | Catatan |
|---|---|---|
| Ada **1 orang** yang bisa Python/JavaScript (internal atau vendor) | **Skenario B** | prototipe sudah ada; bukan dari nol |
| Tidak ada sekarang, tapi bisa kontrak vendor | **Skenario B** | kode kecil dan bisa diserahterimakan; minta vendor rawat |
| Benar-benar tidak ada dan tidak akan ada | **A1 (hemat)** | **terima konsekuensinya:** TV menyegar 30 menit, bukan 30 detik; aturan berat dipindah ke Excel |
| Ingin tengah-tengah | **B untuk TV + A untuk sisanya** | TV tetap satu halaman web kecil (sudah jadi), sisanya Power Platform |

Ukuran prototipe saat ini agar bisa dinilai beban rawatnya: ±1.200 baris Python + ±500 baris
JavaScript, satu proses, satu berkas database. Ini bukan sistem besar.

---

## 6. Akses dari mana-mana, beda jaringan

Kebutuhan: leader dari rumah (kuota HP), supervisor dari plant lain, Group dari kantor pusat —
**jaringan berbeda-beda**, tanpa VPN manual.

| Opsi | Cara | Kelebihan | Kekurangan |
|---|---|---|---|
| **1 · Cloud VM + HTTPS publik** ⭐ | aplikasi di satu VM, domain `dms.<perusahaan>`, login M365 | paling mudah dijangkau dari jaringan apa pun; tanpa perangkat di plant; ingest ke OneDrive langsung | TV bergantung internet plant (§7) |
| **2 · Server di plant + tunnel** | server lokal, dibuka ke internet lewat tunnel HTTPS (tanpa buka port firewall) | TV **tetap hidup** saat internet putus; data tetap di plant | perlu 1 perangkat selalu hidup; akses luar ikut mati bila internet plant mati |
| **3 · Hybrid** | server lokal untuk TV+absensi, replika baca ke cloud untuk Group | paling tahan gangguan | dua tempat dirawat; paling banyak pekerjaan |

**Rekomendasi:** **Opsi 1** karena kebutuhan utamanya justru akses lintas jaringan, dan tidak perlu
pengadaan perangkat. Kekurangan satu-satunya (TV saat internet plant putus) ditutup dengan §7.
Bila IT lebih suka data tidak keluar plant, **Opsi 2** adalah pilihan kedua yang sah.

Yang harus disiapkan IT untuk keduanya:

1. Subdomain + sertifikat HTTPS (wajib — QR dan login tidak boleh lewat HTTP).
2. **Entra ID app registration** untuk login memakai akun M365 yang sudah ada. Kebijakan MFA /
   Conditional Access mengikuti lisensi M365 yang sudah dimiliki.
3. Izin **Graph `Files.Read.All` (application)** untuk membaca berkas divisi — baca saja, tanpa hak tulis.
4. Cadangan harian basis data + uji pemulihan.

---

## 7. TV tidak boleh mati saat internet putus

Ini syarat pabrik, bukan kemewahan. Yang harus dibangun di sisi TV (pekerjaan terbatas, jelas):

| Keadaan | Perilaku yang diwajibkan |
|---|---|
| Internet putus | TV terus menampilkan **snapshot terakhir** + jamnya (sudah ada di prototipe) |
| Ketuk absensi saat offline | ketukan **diantrekan di perangkat**, dikirim saat online (belum ada — perlu dibangun) |
| Ketukan tiba setelah cut-off | masuk sebagai **usulan koreksi** ke Supervisor, bukan menimpa (rancangan/03 §8) |
| Online kembali | ambil snapshot baru tanpa restart; antrean dikirim berurutan |
| Laptop petugas offline | TV menulis **"belum tersinkron"**, bukan "belum diisi" (Status Berkas Jujur) |

Catatan: saat internet plant putus, petugas juga tidak bisa mengunggah ke OneDrive — jadi tidak ada
data baru yang hilang. Yang perlu diselamatkan hanya **tampilan** dan **ketukan absensi**.

---

## 8. Baca di mana saja ≠ tulis di mana saja

Karena akses dibuka lintas jaringan, hak perlu dibedakan:

| Aksi | Dari mana saja | Batasan |
|---|---|---|
| Lihat TV / dasbor / laporan | ✅ boleh | sesuai hak plant/line (Nama Line Diseragamkan…TV Tanpa Hak Ubah) |
| Isi absensi | ⚠️ dibatasi | hanya sesi berjalan + leader pemilik line; opsional wajib jaringan plant |
| Konfirmasi kehadiran | ⚠️ dibatasi | leader / Supervisor / DH, tercatat di audit |
| Ubah angka milik Excel | ❌ tidak ada | koreksi di Excel (Kepemilikan Kolom) |
| Ubah aturan / kunci periode | ✅ boleh | hanya Admin, dari halaman admin, beralasan |

QR sesi tetap berputar tiap shift dan bisa dicabut (QR Satu Pintu), sehingga foto QR yang tersebar tidak
menjadi izin permanen.

---

## 9. Yang masih perlu diputuskan

| # | Pertanyaan | Kenapa penting | Siapa |
|---|---|---|---|
| 1 | Ada orang yang bisa merawat kode? | menentukan Skenario A atau B (§5) | manajemen + IT |
| 2 | Data produksi boleh di cloud? | menentukan Opsi 1 atau 2 (§6) | IT / keamanan |
| 3 | Subdomain & Entra ID app registration | prasyarat akses lintas jaringan | IT |
| 4 | Harga nyata setelah diskon perusahaan | angka §4 masih harga daftar | procurement |
| 5 | Contoh berkas Excel Delivery & Teknik | melengkapi 5 divisi | kepala divisi |

---

## 10. Langkah berikutnya bila Skenario B disetujui

1. Ganti SQLite → PostgreSQL; tambah login Entra ID + HTTPS. **(pekan 1–2)**
2. Graph delta menggantikan pengawas folder untuk produksi; pengawas tetap ada sebagai cadangan. **(pekan 2–3)**
3. TV offline-first: cache snapshot + antrean ketukan absensi. **(pekan 3)**
4. Mesin eskalasi + 12 kartu insight + ekspor laporan. **(pekan 4–6)**
5. Daftarkan berkas Delivery & Teknik; perluas ke semua laptop lewat `setup_onedrive.ps1`. **(pekan 6–8)**
6. Power Automate untuk notifikasi Teams/email — konektor standard, tanpa biaya tambahan. **(kapan saja)**

---

**Ringkas satu kalimat:** karena Excel tetap menjadi tempat petugas mengisi, DMS bukan aplikasi
formulir melainkan pembaca Excel + mesin aturan + layar TV — jadi membayar lisensi per pengguna
Power Platform berarti membayar untuk kekuatan yang tidak dipakai, sementara bagian tersulitnya
tetap harus dibangun sendiri.