@echo off
setlocal EnableExtensions
cd /d "%~dp0"

rem --- Port (default 8000): play.bat [port] ---
set "PORT=%~1"
if not defined PORT set "PORT=8000"

title DMS - Daily Monitoring System (port %PORT%)

rem --- Cari Python 3 (sama seperti install.bat) ---
set "PY="
where py >nul 2>nul && set "PY=py -3"
if not defined PY (where python >nul 2>nul && set "PY=python")
if not defined PY (
  echo [ERROR] Python 3 tidak ditemukan di PATH. Jalankan install.bat dulu.
  pause
  exit /b 1
)

rem --- Dependency belum terpasang? Jalankan install.bat dulu ---
%PY% -c "import flask" >nul 2>nul
if errorlevel 1 (
  echo Dependency belum terpasang - menjalankan install.bat ...
  call install.bat
  if errorlevel 1 exit /b 1
)

rem --- Buka browser ~2 detik kemudian (server sempat start dulu) ---
start "" /min cmd /c "timeout /t 2 /nobreak >nul & start http://localhost:%PORT%/"

echo.
echo ============================================================
echo   DMS berjalan di  http://localhost:%PORT%/   (bind 0.0.0.0:%PORT%)
echo     TV lantai  : http://localhost:%PORT%/
echo     Admin      : http://localhost:%PORT%/admin
echo     Health     : http://localhost:%PORT%/healthz
echo   Tekan CTRL+C untuk berhenti.
echo ============================================================
echo.
set "PORT=%PORT%"
%PY% app\server.py
