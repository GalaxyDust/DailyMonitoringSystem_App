# backend/ — DMS Backend (Kerangka Struktur)

> **Ini KERANGKA KOSONG** — hanya peta penempatan & titik awal; **bukan** aplikasi yang jalan.
> Backend yang hidup tetap di **`app/`** (Flask + SQLite; `server.py`, `dms_core.py`,
> `seed_demo.py`, `registry.json`, `templates/`, `static/`). Jangan dipindah — dipakai live
> (TV lantai, landing sesi, panel admin).
>
> Isi kerangka ini mengikuti **`docs/BACKEND_PLAN.md`**:
> - **Tahap A** (rapikan, ±1 hari) — error handler JSON, validasi input, pyproject/pytest
> - **Tahap B** (kualitas, ±2–4 hari) — test parser/upsert/norm, contract test (jsonschema)
> - **Tahap C** (auth, ±3–5 hari) — MSAL Entra ID (C1 login · C1b PDCA/TL · C2 JWT · C3 peran)
> - **Tahap D** (produksi, ±5–10 hari) — Docker/systemd, HTTPS, backup, monitoring, runbook
>
> Aturan: **jangan tulis kode produksi di sini tanpa perintah**; placeholder hanya penanda
> penempatan (`tests/`, `fixtures/`, Docker, env). Kontrak data: `docs/API_CONTRACT.md` v1.2.
