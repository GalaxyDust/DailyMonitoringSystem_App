@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title DMS - Install

echo ============================================================
echo   DMS - DAILY MONITORING SYSTEM : INSTALL
echo   Folder: %CD%
echo ============================================================
echo.

rem --- 1. Cari Python 3 (py launcher dulu, lalu python dari PATH) ---
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY (
  echo [ERROR] Python 3 tidak ditemukan di PATH.
  echo         Install Python 3.10+ dari https://www.python.org/downloads/
  echo         Saat install, centang "Add python.exe to PATH".
  goto :fail
)
echo [1/4] Python ditemukan: %PY%
%PY% --version
if errorlevel 1 goto :fail

rem --- 2. Install dependency Python (requirements aplikasi) ---
echo.
echo [2/4] Menginstall dependency dari app\requirements.txt ...
%PY% -m pip install --upgrade pip
if errorlevel 1 goto :fail
%PY% -m pip install -r app\requirements.txt
if errorlevel 1 goto :fail

rem --- 3. Seed database HANYA bila belum ada (tidak menimpa data) ---
echo.
if exist "app\var\dms.sqlite3" (
  echo [3/4] Database app\var\dms.sqlite3 sudah ada - seed DILEWATI.
  echo        (Hapus file itu dulu bila ingin seed ulang dari nol.)
) else (
  echo [3/4] Database belum ada - seed dari docs\reference (read-only) ...
  %PY% app\seed_demo.py
  if errorlevel 1 goto :fail
)

rem --- 4. Selesai ---
echo.
echo ============================================================
echo   INSTALL SELESAI
echo   Jalankan aplikasi dengan : play.bat
echo   Lalu buka               : http://localhost:8000
echo   (Ganti port: play.bat 9000)
echo ============================================================
echo.
pause
exit /b 0

:fail
echo.
echo [GAGAL] Install tidak selesai. Baca pesan error di atas.
pause
exit /b 1
