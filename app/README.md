# Prototipe DMS — TV per divisi, absensi di awal, QR satu pintu, sinkron Excel otomatis

Prototipe yang **benar-benar berjalan** untuk membuktikan rancangan di
`docs/laporan/DMS_TV_PerDivisi_dan_Integrasi_Excel_v1.md`. Bukan gambar lagi: angka di layar
dihitung dari log kasus pada workbook `docs/reference/`.

## Menjalankan

Dari root repo:

```bash
pip install -r app/requirements.txt
python3 app/seed_demo.py     # baca workbook (read-only) -> app/var/dms.sqlite3
python3 app/server.py        # http://0.0.0.0:8000
```

|Alamat|Isi|
|---|---|
|`/`|TV lantai — rotasi 7 halaman|
|`/admin`|panel sinkronisasi: daftar sumber, riwayat ingest, karantina, jejak audit|
|`/s/<token>`|landing QR satu pintu (tampilan ponsel)|
|`/api/state`|state papan (JSON)|

Navigasi TV: `←`/`→` pindah halaman · `spasi` jeda · `A` kembali ke absensi · `S` paksa sinkron.
Ganti plant lewat `/?plant=EP` atau `/?plant=NP`. Lingkup line: `/?line=Line%209` (default semua line).

## Yang sudah nyata

- **Parser tahan geser header.** Baris header dicari dari **nama kolom**, bukan nomor baris —
  terbukti membaca SHE baris 17, QC 19, Prod 24, dan Prod NP 25 tanpa konfigurasi per plant.
- **Data asli, bukan angka contoh.** 15.940 kasus dari 9 berkas-divisi (3 plant × SHE/QC/Produksi).
- **KPI dihitung, tidak diketik.** Grid `Target · S1 · S2 · S3 · Harian · Minggu · Bulan` dihitung
  dari log kasus (jumlah, open, close, completion rate, lewat tenggat, total downtime).
- **Idempoten.** Kunci baris = hash(plant, divisi, tanggal, shift, line, LBN, masalah) — bukan kolom
  `No` yang bisa dinomori ulang. Baca ulang berkas yang sama tidak mendobel data.
- **Terverifikasi ujung ke ujung.** berkas uji disimpan ulang → pengawas membaca dalam ±7 detik →
  papan berubah. Ubah kolom non-kunci (PIC/progress) menghasilkan **1 ubah**, bukan baris baru;
  baca ulang berkas yang sama menghasilkan **0 tambah / 0 ubah**. `docs/reference/` tidak tersentuh.
- **Batas yang perlu diketahui:** kunci baris memakai teks masalah. Bila petugas **menyunting teks
  masalah**, baris lama ditandai "terhapus di sumber" dan baris baru muncul — riwayat tetap ada,
  tetapi secara statistik terlihat sebagai kasus baru. Menyunting sebab/tindakan/PIC/status
  memperbarui di tempat. Bila ini mengganggu, tambahkan kolom ID tetap di Excel dan pakai itu
  sebagai kunci.
- **Karantina, bukan buang diam-diam.** 61 baris tidak terbaca tanggal/masalahnya dikarantina;
  708 baris bertanda karena PIC berisi tautan SharePoint, bukan nama.
- **Pengawas folder aktif.** Thread memeriksa berkas tiap 3 detik, menunggu mtime stabil 4 detik,
  melewati berkas kunci `~$nama.xlsx`. Simpan Excel → TV menyusul tanpa tombol apa pun.
- **Absensi jadi gerbang.** Rotasi divisi terkunci sampai kehadiran dikonfirmasi; setiap ketukan
  masuk jejak audit.
- **QR sesi betulan.** `/qr/<token>.png` berisi tautan sesi yang bisa dipindai ponsel.
- **Keadaan kosong jujur.** Delivery & Teknik menampilkan **"menunggu berkas"**, bukan angka karangan.

## Yang masih demo (ditandai di layar)

- **Mode demo** memutar ulang tanggal dengan kasus terbanyak (bukan hari ini), karena workbook acuan
  adalah data lampau. Ada **pita kuning** di atas layar yang menyebut tanggal aslinya. Matikan
  dengan `/?demo=0` untuk melihat keadaan kosong hari ini.
- **Mode demo tidak melanggar R-75** (historis tidak ke TV) karena seluruh layar diberi tanda
  MODE DEMO dan tidak dipakai untuk keputusan produksi.
- Daftar nama absensi masih daftar contoh. Di produksi diisi Admin/impor (R-31).
- Satu arah saja: aplikasi **tidak pernah menulis** ke workbook (R-85). Belum ada SSO; menulis
  absensi masih terbuka di prototipe.

## Memasang di laptop petugas (satu kali oleh IT)

```powershell
# lihat rencana dulu, tidak mengubah apa pun
.\app\setup_onedrive.ps1 -FolderKerja "D:\DMS\SHE" -Divisi she -RencanaSaja

# pasang: salin -> verifikasi -> folder lama jadi cadangan -> junction di path lama
.\app\setup_onedrive.ps1 -FolderKerja "D:\DMS\SHE" -Divisi she
```

Skrip **tidak langsung memindah**: ia menyalin, memverifikasi jumlah berkas dan total byte, mengganti
nama folder lama menjadi `.lama-<waktu>` sebagai cadangan, baru membuat junction. Bila verifikasi
gagal, folder lama tidak disentuh. Bila `mklink` gagal, nama folder lama dikembalikan.

Arah junction wajib: **folder asli di dalam OneDrive, tautan di luar pada path lama.** Kebalikannya
tidak didukung Microsoft. Folder jaringan tidak didukung OneDrive — untuk itu pakai folder bersama
plus satu pengawas di server.

Setelah dipasang, daftarkan berkasnya di `app/registry.json`:

```json
{ "sumber_id": "SN-SHE", "plant": "Snack", "line": "*", "divisi": "she",
  "sheet": "auto", "path": "C:/Users/nama/OneDrive - Garudafood/DMS/she/Resume SHE.xlsx" }
```

`"sheet": "auto"` membuat parser mencari sheet `Resume*` dan baris header dari nama kolom.
Petugas tidak perlu tahu semua ini — cukup buka file yang sama dan tekan **Ctrl+S**.

## Berkas

|Berkas|Isi|
|---|---|
|`dms_core.py`|skema SQLite, parser header-toleran, normalisasi, upsert idempoten, KPI per periode|
|`server.py`|Flask: API, TV, admin, QR, dan thread pengawas folder|
|`seed_demo.py`|daftarkan sumber dari registry, ingest semua, siapkan sesi + daftar absensi|
|`registry.json`|daftar sumber per berkas divisi (R-86)|
|`setup_onedrive.ps1`|pemasangan satu kali di laptop petugas|
|`templates/`, `static/`|TV (panggung 1600×900 diskalakan), landing sesi, panel sinkron|
|`var/dms.sqlite3`|basis data lokal — **tidak ikut Git**|

## Rujukan aturan

R-80 satu divisi per layar · R-81 absensi dulu · R-82 QR satu pintu · R-83 kolom mengikuti Excel ·
R-84 kolom tetap isi dinamis · R-85 sinkron satu arah terus-menerus · R-86 per berkas divisi ·
R-87 badge sumber · R-88 nol langkah tambahan · R-89 kepemilikan kolom · R-90 belum diisi ≠ belum tersinkron.