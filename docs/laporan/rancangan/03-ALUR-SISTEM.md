# 03 · Alur Sistem DMS Digital

**Dokumen:** bagian 3 dari 3 rancangan aplikasi Daily Monitoring System (DMS)
**Status:** rancangan untuk sosialisasi & uji terima
**Tanggal:** 5 November 2026

> Urutan baca: [`01-KENAPA-DMS-DIGITAL.md`](01-KENAPA-DMS-DIGITAL.md) → [`02-RANCANGAN-APLIKASI.md`](02-RANCANGAN-APLIKASI.md) → **file ini (alur)**.
> Setiap langkah di bawah mengacu pada aturan bernomor di [`DMS_Aturan_Sistem_v1.md`](../DMS_Aturan_Sistem_v1.md).

---

## 0. Peta besar alur

```mermaid
flowchart LR
    A["Absensi<br/>shift mulai"] --> B["Isi papan<br/>per divisi"]
    B --> C{"Di bawah<br/>target?"}
    C -- tidak --> D["Catatan sesuai<br/>terkirim"]
    C -- ya --> E["Sebab + tindakan<br/>+ PIC + bukti"]
    E --> F{"Perlu<br/>tindak lanjut?"}
    F -- ya --> G["Kasus + tenggat<br/>otomatis"]
    F -- tidak --> D
    G --> H["Pengerjaan /<br/>work order Teknik"]
    H --> I{"Lengkap 4 kolom?"}
    I -- belum --> H
    I -- sudah --> J["Persetujuan<br/>DH / plant head"]
    J --> K["Kasus ditutup<br/>periode dikunci"]
    D --> L["TV papan + dasbor<br/>+ laporan"]
    G --> L
    K --> L
    L --> M["Rapat pagi &<br/>keputusan"]
```

Sembilan alur yang dirinci:

1. Alur harian per shift (paling sering dipakai)
2. Alur absensi
3. Alur isian papan per divisi
4. Alur serah terima downtime ke Teknik
5. Alur kasus sampai ditutup (state machine)
6. Alur tenggat & eskalasi
7. Alur koreksi & kunci periode
8. Alur TV dan laporan
9. Alur replikasi plant

---

## 1. Alur harian per shift (swimlane)

```mermaid
sequenceDiagram
    autonumber
    participant TV as TV lantai
    participant L as Leader line
    participant D as Petugas divisi
    participant S as Sistem
    participant SP as Supervisor / DH

    S->>TV: tampilkan papan + daftar absensi shift
    L->>TV: ketuk nama yang tidak hadir
    TV->>S: kirim status absensi (waktu, perangkat)
    S-->>TV: ringkasan hadir/total

    par Pengisian paralel
        L->>S: isi tab Produksi (output, downtime, checklist)
    and
        D->>S: isi tab SHE / Quality / Teknik / Delivery
    end

    S->>S: validasi, hitung status, hitung kelengkapan
    alt ada nilai di bawah target
        S-->>L: minta sebab + tindakan + PIC + bukti
        L->>S: lengkapi
        S->>S: buat kasus + tenggat otomatis
    end

    S->>TV: perbarui papan (≤ 30 detik)
    S->>S: jalankan 12 aturan temuan
    S-->>SP: notifikasi temuan berperingkat
    S->>S: cut-off shift: kunci untuk leader
    SP->>S: rapat pagi: koreksi + alasan bila perlu
```

| Waktu | Siapa | Langkah | Keluaran |
|---|---|---|---|
| 06.00–06.30 | Sistem | siapkan papan + daftar absensi shift | papan kosong bertanda "belum diisi" |
| 06.30–07.00 | Leader | konfirmasi absensi (hanya yang tidak hadir) | kehadiran shift |
| 06.30–07.30 | Leader & divisi | isi bagian masing-masing | sel papan terisi |
| 07.30 | Sistem | validasi & buat kasus bila di bawah target | kasus + tenggat |
| 07.30 | Sistem | perbarui TV & dasbor | papan terkini |
| 08.30 | Supervisor/DH | rapat pagi memakai temuan berperingkat | keputusan & penugasan |
| akhir shift + 30 mnt | Sistem | cut-off untuk leader | catatan terkunci |

> Papan **boleh terisi sebagian**. Pilar yang belum diisi ditandai "belum diisi" + jam terakhir dicek,
> bukan dikosongkan (R-12, R-14).

---

## 2. Alur absensi

```mermaid
flowchart TD
    A["Admin menyiapkan daftar:<br/>nama · regu · shift · line"] --> B["Sistem menyiapkan daftar<br/>shift berjalan · status awal HADIR"]
    B --> C{"Sumber ketukan"}
    C -- "TV lantai (tanpa login)" --> D["Lapangan ketuk nama<br/>yang tidak hadir"]
    C -- "Form web (tablet/PC)" --> E["Leader/supervisor<br/>mengubah status"]
    D --> F{"Salah ketuk?"}
    E --> F
    F -- ya --> G["Urungkan dalam 2 menit"]
    F -- tidak --> H["Tersimpan: status · waktu ·<br/>perangkat · pengguna"]
    G --> H
    H --> I["Menutup otomatis saat<br/>cut-off shift"]
    I --> J["Dipakai: TV, dasbor,<br/>penjelas output turun"]
    I --> K["Koreksi setelah cut-off:<br/>hanya supervisor/DH/Admin"]
```

Aturan kunci:

| Aturan | Isi |
|---|---|
| R-31 | daftar nama disiapkan Admin (impor Excel dianjurkan) |
| R-32 | status awal **hadir**; lapangan hanya menandai yang tidak hadir |
| R-33 | TV dan form menulis ke catatan absensi yang sama |
| R-34 | TV hanya bisa absen untuk shift berjalan & line miliknya |
| R-35 | setiap ketukan tercatat; urungkan 2 menit |
| R-37 | absensi jadi penjelas otomatis bila output di bawah target |
| R-38 | absensi **tidak** dipakai menilai orang di dalam sistem |

Status yang tersedia: `hadir` · `sakit` · `izin` · `alpa` · `terlambat` · `dinas luar`.

---

## 3. Alur isian papan per divisi

```mermaid
flowchart LR
    subgraph SHE
        S1["kecelakaan ·<br/>near miss · KAK"] --> S2["status tindakan"]
    end
    subgraph QC
        Q1["defect per line ·<br/>critical point"] --> Q2["hold/release ·<br/>kalibrasi alat"]
    end
    subgraph Produksi
        P1["checklist · output ·<br/>downtime menit"] --> P2["OEE · sebab singkat"]
    end
    subgraph Teknik
        T1["kategori sebab ·<br/>komponen"] --> T2["PM · spare part ·<br/>work order"]
    end
    subgraph Delivery
        D1["plan vs real PO"] --> D2["keterlambatan ·<br/>kesiapan muat"]
    end
    S2 --> X["Satu papan<br/>(sel terpisah per divisi)"]
    Q2 --> X
    P2 --> X
    T2 --> X
    D2 --> X
    X --> Y["TV · dasbor · laporan"]
```

| Langkah | Siapa | Yang dikerjakan | Batas |
|---|---|---|---|
| 1 | Leader | buka papan line-nya, pilih shift | awal shift |
| 2 | Petugas divisi | isi tab divisi sendiri (target menempel pada item) | sebelum cut-off |
| 3 | Sistem | validasi: hasil wajib, sebab wajib bila di bawah target | saat simpan |
| 4 | Leader | isi tab Produksi; tab lain hanya bila ditandai "boleh diisi leader" | sebelum cut-off |
| 5 | Sistem | tandai pilar "belum diisi" + jam cek terakhir | berjalan |
| 6 | Divisi | kirim bagian sendiri (tombol kirim per divisi) | kapan saja |

Divisi **tidak bisa** menimpa sel divisi lain (R-08) — inilah yang mencegah angka pilar ditimpa.

---

## 4. Alur serah terima downtime ke Teknik

Ini alur yang paling sering menimbulkan kerja ganda; karena itu dipecah dua pemilik.

```mermaid
sequenceDiagram
    autonumber
    participant L as Leader (Produksi)
    participant S as Sistem
    participant SK as Supervisor/DH
    participant T as Teknik
    participant TV as TV area Teknik

    L->>S: catat downtime (mesin, jam mulai, menit)
    S->>S: cek ambang (mis. ≥ 30 menit)
    alt di atas ambang
        S->>T: buat work order + tenggat diagnosis
        S->>TV: kartu "menunggu Teknik"
    else di bawah ambang
        S->>S: cukup tercatat sebagai angka
    end
    T->>S: diagnosis: kategori sebab, komponen, tindakan
    T->>S: selesai perbaikan + spare part terpakai
    S->>L: minta konfirmasi "normal / masih bermasalah"
    alt masih bermasalah
        L->>S: buka kembali kasus
    else normal
        L->>S: konfirmasi
        S->>S: kasus siap ditutup (bila 4 kolom lengkap)
    end
```

| Langkah | Pemilik | Isi | Batas waktu |
|---|---|---|---|
| 1 | Produksi | mesin, jam mulai–selesai, menit berhenti, output hilang | saat kejadian |
| 2 | Sistem | bandingkan ambang → buat work order | ≤ 1 menit |
| 3 | Teknik | kategori sebab (mekanik/elektrik/utilitas/setting/operator), komponen, tindakan, WO, spare part, teknisi | **≤ 4 jam** (dampak A) / ≤ 24 jam (B) |
| 4 | Teknik | serah terima: mesin jalan / uji coba | setelah perbaikan |
| 5 | Produksi | konfirmasi normal atau kasus dibuka lagi | 1 shift berikutnya |

Kategori sebab **dikunci lima pilihan** supaya antar plant bisa dibandingkan (R-16).

---

## 5. Alur kasus sampai ditutup (state machine)

```mermaid
stateDiagram-v2
    [*] --> Baru : sel di bawah target / kejadian
    Baru --> Dikerjakan : sebab + tindakan + PIC ditetapkan
    Dikerjakan --> MenungguBukti : pekerjaan selesai
    Dikerjakan --> LewatTenggat : tenggat terlewat
    MenungguBukti --> LewatTenggat : tenggat terlewat
    MenungguBukti --> Diajukan : bukti dilampirkan
    Diajukan --> Ditolak : kolom belum lengkap
    Ditolak --> Dikerjakan : dilengkapi
    Diajukan --> Ditutup : disetujui DH / plant head
    LewatTenggat --> Dikerjakan : ditangani (naik L2/L3)
    Ditutup --> DibukaKembali : koreksi beralasan (versi baru)
    DibukaKembali --> Dikerjakan
    Ditutup --> [*]
```

Gerbang penutupan (R-45):

| Kolom | Isi minimal | Bila kosong |
|---|---|---|
| Sebab | penyebab sebenarnya (bukan "operator") | tombol ajukan nonaktif |
| Tindakan | perbaikan + pencegahan bila berulang | tombol ajukan nonaktif |
| Bukti | ≥ 1 foto/dokumen | tombol ajukan nonaktif |
| PIC | nama pemilik kasus | tombol ajukan nonaktif |

Tambahan: **persetujuan** harus dari peran berbeda dengan pengaju (R-09), dan kasus berulang ≥3×/90 hari
wajib memuat **PICA + tindakan pencegahan** (R-48).

---

## 6. Alur tenggat & eskalasi

```mermaid
flowchart LR
    A["Kasus dibuat"] --> B["Tenggat dihitung sistem<br/>A=1 hari · B=3 hari · C=5 hari kerja"]
    B --> C{"Lewat tenggat?"}
    C -- tidak --> D["Dikerjakan normal"]
    C -- ya --> E["Hari ke-0 lewat:<br/>naik L2 supervisor / DH"]
    E --> F{"Hari ke-2 kerja<br/>masih lewat?"}
    F -- ya --> G["Naik L3: plant head"]
    F -- tidak --> D
    G --> H{"Hari ke-4 kerja<br/>masih lewat?"}
    H -- ya --> I2["Masuk laporan Group<br/>+ prioritas rapat"]
    H -- tidak --> D
    D --> I["Ditutup dengan bukti"]
    I2 --> I
```

| Aturan | Isi |
|---|---|
| R-46 | tenggat dihitung dari dampak, bukan diketik |
| R-47 | lewat tenggat → L2 hari ke-0 · L3 hari ke-2 · laporan Group hari ke-4 (hari kerja) |
| R-50 | tanpa aktivitas 14 hari → ditandai "dingin", ditanyakan di rapat (bukan ditutup) |

Kartu di TV selalu menampilkan **umur kasus** dan **tingkat eskalasi** supaya tidak menunggu rapat.

---

## 7. Alur koreksi & kunci periode

```mermaid
flowchart TD
    A["Catatan / kasus tersimpan"] --> B{"Masih dalam<br/>shift + 30 menit?"}
    B -- ya --> C["DRAF: leader/divisi bebas koreksi<br/>(tercatat otomatis)"]
    B -- tidak --> D["TERKUNCI: hanya supervisor / DH<br/>+ alasan koreksi"]
    C --> E["Tersimpan sebagai versi baru"]
    D --> F{"Perubahan besar?<br/>(>5% atau ubah close)"}
    F -- ya --> G["Butuh persetujuan<br/>satu tingkat di atas"]
    F -- tidak --> E
    G --> E
    E --> H{"Periode sudah<br/>dilaporkan?"}
    H -- ya --> I["ARSIP: hanya Admin plant<br/>+ alasan · tercatat audit"]
    H -- tidak --> J["Laporan bulanan disusun"]
    I --> K["Versi baru, nilai lama tetap ada"]
```

| Status | Siapa boleh ubah | Syarat |
|---|---|---|
| **Draf** | leader / petugas divisi pemilik | otomatis tercatat |
| **Terkunci** | supervisor, DH, kepala divisi | wajib alasan; nilai lama disimpan |
| **Arsip** | admin plant | koreksi = versi baru, bukan menimpa |

Tidak ada fitur hapus untuk peran mana pun — hanya **batal** dan **arsip** (R-44).

---

## 8. Alur TV dan laporan

```mermaid
flowchart LR
    A["Catatan & kasus<br/>(satu sumber)"] --> B["Mesin aturan<br/>kelengkapan · temuan · skor"]
    B --> C["Snapshot papan<br/>tiap 20-30 detik"]
    C --> D["TV lantai<br/>tanpa login"]
    B --> E["Dasbor L1-L3<br/>+ daftar kerja"]
    B --> F["Laporan bulanan<br/>skor proses vs hasil"]
    F --> G{"Periode<br/>dikunci?"}
    G -- belum --> H["Draf laporan<br/>(internal)"]
    G -- sudah --> I["Ekspor / kirim Group"]
    D --> J["Rapat pagi:<br/>temuan berperingkat"]
    E --> J
    I --> J
```

TV tahan gangguan:

| Keadaan | Perilaku TV |
|---|---|
| Data hari ini belum ada | tampilkan angka kemarin + tanda **"data kemarin"** |
| Jaringan putus | tampilkan snapshot terakhir + jam pembaruan |
| Pilar belum diisi | sel abu-abu "belum diisi", bukan kosong |
| Jaringan pulih | ambil snapshot baru, tanpa perlu restart |
| Absensi | tetap bisa diketuk (terkirim saat jaringan kembali); ketukan yang tiba setelah cut-off masuk sebagai usulan koreksi ke Supervisor, bukan menimpa langsung |

---

## 9. Alur replikasi plant

```mermaid
flowchart LR
    A["Snack<br/>pilot 8 pekan"] --> G1{{"G4 siap<br/>replikasi"}}
    G1 --> B["Exist Plant<br/>4 pekan"]
    B --> G2{{"uji<br/>5 ukuran"}}
    G2 --> C["New Plant<br/>4 pekan"]
    C --> G3{{"uji<br/>5 ukuran"}}
    G3 --> D["Dairy<br/>4 pekan"]
    G1 -.gagal.-> A
    G2 -.gagal.-> B
    G3 -.gagal.-> C
```

| Dibawa saat replikasi | Tetap lokal di plant |
|---|---|
| master line & mesin (pola) | target plant |
| template item & aturan insight | kalender libur |
| profil TV (pola tampilan) | daftar nama, regu, dan shift |
| struktur kasus & PICA | PIC dan jalur persetujuan |

Total: 8 + 4 + 4 + 4 = **20 pekan**.

---

## 10. Ringkasan SLA dan batas waktu

| Hal | Batas waktu | Siapa yang menjaga |
|---|---|---|
| Isi papan satu shift | selesai sebelum cut-off (shift + 30 menit) | leader & divisi |
| Konfirmasi absensi | sebelum shift berjalan berakhir | leader (via TV/form) |
| Perbaikan data setelah cut-off | sebelum rapat pagi berikutnya | supervisor / DH |
| Diagnosis downtime | 4 jam (dampak A) / 24 jam (dampak B) | Teknik |
| Penutupan kasus | sesuai tenggat dampak (1/3/5 hari kerja) | PIC + penyetuju |
| Kunci periode | setelah laporan bulanan disahkan | plant head / admin |
| Perbarui tampilan TV | ≤ 30 detik dari input | sistem |

---

## 11. Uji alur (dipakai saat uji terima)

| # | Skenario | Hasil yang diharapkan |
|---|---|---|
| 1 | Leader mengisi output di bawah target tanpa sebab | sistem menolak simpan, menyebut kolom sebab |
| 2 | Petugas SHE mencoba mengubah sel QC | ditolak, tercatat |
| 3 | Leader mengubah catatan 45 menit setelah shift | ditolak; harus supervisor + alasan |
| 4 | Kasus downtime 48 menit dicatat Produksi | work order Teknik otomatis muncul dengan tenggat |
| 5 | Kasus ditutup tanpa bukti | tombol nonaktif, pesan jelas |
| 6 | Kasus berulang ke-3 dalam 90 hari | wajib PICA sebelum boleh ditutup |
| 7 | Kasus lewat tenggat 2 hari kerja | sudah di L3 (plant head) sejak hari ke-2; L2 sejak hari ke-0; muncul di dasbor tingkatnya |
| 8 | TV dimatikan saat jaringan putus | tetap menampilkan papan terakhir + jam |
| 9 | Absensi diketuk di TV lalu dibuka di form | status sama, tidak ada duplikat |
| 10 | Laporan Oktober dibuka setelah dikunci | hanya Admin, dengan alasan, versi baru |

---

## 12. Ringkasan: siapa melakukan apa

| Peran | Alur yang dijalankan | Keluaran |
|---|---|---|
| Leader line | 1, 2, 3 | papan terisi, absensi, kasus baru |
| Petugas divisi | 3 | bagian pilar terisi |
| Teknik | 4, 5 | work order, diagnosis, PM |
| Supervisor / DH | 5, 6, 7 | persetujuan, koreksi, eskalasi |
| Plant head | 6, 7 | keputusan prioritas, kunci periode |
| Admin plant | 2, 7, 8 | daftar nama, target versi, profil TV, audit |
| Group | 8, 9 | perbandingan plant, gerbang replikasi |
| TV | 1, 2, 8 | tampilan papan + ketukan absensi |
