"""Isi basis data prototipe dari daftar sumber, lalu siapkan satu sesi DMS.

Tidak mengubah berkas Excel sedikit pun (R-85). Jalankan dari root repo:
    python3 app/seed_demo.py
"""
from __future__ import annotations

import datetime as dt
import json
import os
import secrets
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dms_core as core

REG = os.path.join(core.ROOT, "app", "registry.json")

NAMA_DEMO = [
    "Dhani", "Rani", "Sigit", "Asep", "Yanti", "Budi", "Wawan",
    "Rina", "Joko", "Sari", "Agus", "Dewi", "Bagas", "Nita",
    "Fajar", "Putri", "Rizal", "Maya", "Hendra", "Lilis", "Yoga",
    "Tari", "Bayu", "Nisa", "Iwan", "Ratna", "Doni", "Wulan",
]


def daftarkan(con, ubah_path=None):
    cfg = json.load(open(REG, encoding="utf-8"))
    for s in cfg["sumber"]:
        path = s["path"]
        if ubah_path:
            path = os.path.join(ubah_path, os.path.basename(path))
        if not os.path.isabs(path):
            path = os.path.join(core.ROOT, path)
        con.execute(
            "INSERT INTO sumber(sumber_id,plant,line,divisi,path,sheet) VALUES(?,?,?,?,?,?) "
            "ON CONFLICT(sumber_id) DO UPDATE SET plant=excluded.plant,line=excluded.line,"
            "divisi=excluded.divisi,path=excluded.path,sheet=excluded.sheet",
            (s["sumber_id"], s["plant"], s["line"], s["divisi"], path, s.get("sheet")),
        )
    con.commit()
    return [s["sumber_id"] for s in cfg["sumber"]]


def sesi_baru(con, plant="Snack", line="Line 9"):
    tanggal = dt.date.today().strftime("%Y-%m-%d")
    sid = f"{plant}-{line}-{tanggal}-1".replace(" ", "")
    token = secrets.token_urlsafe(8)
    con.execute(
        "INSERT INTO sesi(sesi_id,plant,line,tanggal,shift,status,token,dibuka_pada) "
        "VALUES(?,?,?,?,?,'DIBUKA',?,?) ON CONFLICT(sesi_id) DO NOTHING",
        (sid, plant, line, tanggal, "1", token, core.now()),
    )
    for nm in NAMA_DEMO:
        con.execute(
            "INSERT INTO absensi(sesi_id,nama,status,diubah_pada,perangkat) VALUES(?,?,?, ?, ?) "
            "ON CONFLICT(sesi_id,nama) DO NOTHING",
            (sid, nm, "hadir", core.now(), "seed"),
        )
    con.commit()
    return sid


def main():
    con = core.connect()
    ids = daftarkan(con)
    print(f"{len(ids)} sumber terdaftar. Membaca (read-only)…\n")
    total_t = total_u = 0
    for sid in ids:
        r = core.ingest_file(con, sid, force=True)
        if r.get("ok"):
            total_t += r.get("tambah", 0)
            total_u += r.get("ubah", 0)
            print(f"  {sid:9s} sheet={r.get('sheet','?'):12s} header={r.get('header','?'):>3} "
                  f"baris={r.get('baris',0):>5} karantina={r.get('karantina',0):>4}")
        else:
            print(f"  {sid:9s} GAGAL: {r.get('pesan')}")
    n = con.execute("SELECT COUNT(*) c FROM kasus").fetchone()["c"]
    q = con.execute("SELECT COUNT(*) c FROM karantina").fetchone()["c"]
    flagged = con.execute("SELECT COUNT(*) c FROM kasus WHERE flagged<>''").fetchone()["c"]
    print(f"\nTotal kasus di basis data : {n}")
    print(f"Baris dikarantina        : {q}")
    print(f"Baris bertanda (mis. PIC berupa tautan): {flagged}")
    tg = core.tanggal_tersedia(con)
    print(f"Tanggal tersedia         : {len(tg)} · terbaru {tg[0] if tg else '-'} · terlama {tg[-1] if tg else '-'}")
    sid = sesi_baru(con)
    s = con.execute("SELECT * FROM sesi WHERE sesi_id=?", (sid,)).fetchone()
    print(f"\nSesi demo: {sid} · token {s['token']} · {len(NAMA_DEMO)} nama absensi")
    con.close()


if __name__ == "__main__":
    main()