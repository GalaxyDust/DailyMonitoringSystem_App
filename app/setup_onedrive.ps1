<#
.SYNOPSIS
    Pemasangan SATU KALI oleh IT agar Excel divisi tersinkron otomatis tanpa petugas upload.
    Sesuai R-85 / R-88 dan docs/laporan/DMS_TV_PerDivisi_dan_Integrasi_Excel_v1.md §5.1.1.

.DESCRIPTION
    Urutan aman (tidak langsung memindah):
      1. periksa folder kerja lokal dan folder OneDrive
      2. SALIN folder kerja ke dalam OneDrive
      3. verifikasi jumlah berkas dan total byte sama
      4. ganti nama folder lama menjadi .lama-<waktu> (TIDAK dihapus, jadi cadangan)
      5. buat junction di path lama menunjuk ke folder OneDrive
    Sesudah itu petugas membuka file dari path/shortcut yang SAMA dan cukup Ctrl+S.

    Arah junction wajib begini: folder asli DI DALAM OneDrive, tautan DI LUAR pada path lama.
    Kebalikannya (junction di dalam OneDrive menunjuk folder luar) tidak didukung Microsoft.

.PARAMETER FolderKerja
    Path folder yang biasa dipakai petugas, mis. "D:\DMS\SHE".

.PARAMETER Divisi
    Label divisi untuk nama folder tujuan: she | quality | produksi | delivery | teknik.

.PARAMETER OneDriveRoot
    Opsional. Default memakai %OneDriveCommercial% (akun kerja).

.PARAMETER RencanaSaja
    Tampilkan rencana tanpa mengubah apa pun.

.EXAMPLE
    .\setup_onedrive.ps1 -FolderKerja "D:\DMS\SHE" -Divisi she -RencanaSaja
    .\setup_onedrive.ps1 -FolderKerja "D:\DMS\SHE" -Divisi she
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$FolderKerja,
    [Parameter(Mandatory = $true)][ValidateSet('she', 'quality', 'produksi', 'delivery', 'teknik')][string]$Divisi,
    [string]$OneDriveRoot = $env:OneDriveCommercial,
    [switch]$RencanaSaja
)

$ErrorActionPreference = 'Stop'
function Tulis($pesan, $warna = 'Gray') { Write-Host $pesan -ForegroundColor $warna }

Tulis "=== DMS · sinkron Excel tanpa upload (pemasangan satu kali oleh IT) ===" 'Cyan'

# ---- 1. pemeriksaan ----------------------------------------------------------
if ([string]::IsNullOrWhiteSpace($OneDriveRoot)) {
    throw "Folder OneDrive akun kerja tidak ditemukan. Masuk dulu ke OneDrive dengan akun kerja, atau isi -OneDriveRoot."
}
if (-not (Test-Path -LiteralPath $OneDriveRoot)) { throw "OneDriveRoot tidak ada: $OneDriveRoot" }
if (-not (Test-Path -LiteralPath $FolderKerja)) { throw "Folder kerja tidak ada: $FolderKerja" }
if ($FolderKerja.StartsWith('\\')) { throw "Folder jaringan tidak didukung OneDrive. Pakai Opsi 3 (folder bersama + satu pengawas di server)." }

$item = Get-Item -LiteralPath $FolderKerja -Force
if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) {
    throw "Folder kerja sudah berupa junction/symbolic link. Hentikan supaya tidak membuat tautan bertingkat."
}
if ($FolderKerja.TrimEnd('\').ToLower().StartsWith($OneDriveRoot.TrimEnd('\').ToLower())) {
    Tulis "Folder kerja sudah berada di dalam OneDrive. Tidak perlu dipasang lagi." 'Green'
    return
}

$tujuan = Join-Path (Join-Path $OneDriveRoot 'DMS') $Divisi
if (Test-Path -LiteralPath $tujuan) {
    throw "Tujuan sudah ada: $tujuan. Periksa dulu isinya; skrip tidak menimpa folder yang sudah ada."
}

$berkas = Get-ChildItem -LiteralPath $FolderKerja -Recurse -File -Force |
          Where-Object { $_.Name -notlike '~$*' }
$jumlah = @($berkas).Count
$byte = ($berkas | Measure-Object -Property Length -Sum).Sum
if ($jumlah -eq 0) { throw "Folder kerja kosong — tidak ada yang perlu disinkron." }

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$lama = "$FolderKerja.lama-$stamp"

Tulis ""
Tulis "Rencana:" 'Yellow'
Tulis "  sumber   : $FolderKerja  ($jumlah berkas, $([math]::Round($byte/1MB,2)) MB)"
Tulis "  tujuan   : $tujuan"
Tulis "  cadangan : $lama  (folder lama diganti nama, tidak dihapus)"
Tulis "  junction : $FolderKerja  ->  $tujuan"
if ($RencanaSaja) { Tulis "`n-RencanaSaja: tidak ada yang diubah." 'Cyan'; return }

# ---- 2. salin ---------------------------------------------------------------
Tulis "`n[2/5] Menyalin ke OneDrive…" 'Cyan'
$null = New-Item -ItemType Directory -Path (Split-Path $tujuan -Parent) -Force
$rc = Start-Process -FilePath 'robocopy.exe' -ArgumentList @(
    "`"$FolderKerja`"", "`"$tujuan`"", '/E', '/COPY:DAT', '/R:2', '/W:2', '/NFL', '/NDL', '/NJH', '/NP'
) -NoNewWindow -Wait -PassThru
if ($rc.ExitCode -ge 8) { throw "robocopy gagal (kode $($rc.ExitCode)). Folder lama tidak disentuh." }

# ---- 3. verifikasi ----------------------------------------------------------
Tulis "[3/5] Memverifikasi hasil salinan…" 'Cyan'
$cek = Get-ChildItem -LiteralPath $tujuan -Recurse -File -Force |
       Where-Object { $_.Name -notlike '~$*' }
$jumlah2 = @($cek).Count
$byte2 = ($cek | Measure-Object -Property Length -Sum).Sum
if ($jumlah2 -ne $jumlah -or $byte2 -ne $byte) {
    throw "Verifikasi gagal: sumber $jumlah berkas/$byte byte, tujuan $jumlah2 berkas/$byte2 byte. Folder lama tidak disentuh."
}
Tulis "      cocok: $jumlah2 berkas, $byte2 byte" 'Green'

# ---- 4. simpan folder lama sebagai cadangan ---------------------------------
Tulis "[4/5] Mengganti nama folder lama menjadi cadangan…" 'Cyan'
$excel = Get-Process -Name EXCEL -ErrorAction SilentlyContinue
if ($excel) { Tulis "      PERINGATAN: Excel sedang berjalan. Tutup dulu semua workbook divisi ini." 'Yellow' }
Rename-Item -LiteralPath $FolderKerja -NewName (Split-Path $lama -Leaf)

# ---- 5. junction di path lama ----------------------------------------------
Tulis "[5/5] Membuat junction di path lama…" 'Cyan'
$cmd = "mklink /J `"$FolderKerja`" `"$tujuan`""
$p = Start-Process -FilePath 'cmd.exe' -ArgumentList @('/c', $cmd) -NoNewWindow -Wait -PassThru
if ($p.ExitCode -ne 0) {
    Rename-Item -LiteralPath $lama -NewName (Split-Path $FolderKerja -Leaf)
    throw "mklink gagal (kode $($p.ExitCode)). Folder lama sudah dikembalikan seperti semula."
}

Tulis "`n=== SELESAI ===" 'Green'
Tulis "Petugas TIDAK perlu melakukan apa pun yang baru: buka file dari path/shortcut yang sama, isi, Ctrl+S."
Tulis "Cadangan lama ada di: $lama  (hapus manual setelah 1-2 pekan aman)"
Tulis ""
Tulis "Langkah terakhir di server DMS — tambahkan berkas ini ke app/registry.json:" 'Cyan'
$contoh = Get-ChildItem -LiteralPath $tujuan -Recurse -File -Force -Filter '*.xlsx' |
          Where-Object { $_.Name -notlike '~$*' } | Select-Object -First 5
foreach ($f in $contoh) {
    Tulis ('  { "sumber_id": "<PLANT>-' + $Divisi.ToUpper() + '", "plant": "<PLANT>", "line": "*", "divisi": "' + $Divisi + '", "sheet": "auto", "path": "' + ($f.FullName -replace '\\', '/') + '" }')
}
Tulis "`nCatatan: 'sheet':'auto' membuat parser mencari sheet Resume* dan baris header dari nama kolom." 'DarkGray'