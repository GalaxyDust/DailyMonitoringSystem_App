"""Server prototipe DMS: TV per divisi, absensi di awal, QR satu pintu, sinkron otomatis.

Jalankan dari root repo:
    python3 app/server.py            -> http://0.0.0.0:8000

Tidak ada tombol upload. Pengawas folder membaca berkas divisi saat petugas menyimpan (R-85, R-88).
"""
from __future__ import annotations

import datetime as dt
import io
import json
import os
import secrets
import threading
import time

from flask import Flask, jsonify, redirect, render_template, request, send_file, send_from_directory

import dms_core as core

APP = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(APP, "templates"),
            static_folder=os.path.join(APP, "static"))
app.config["JSON_AS_ASCII"] = False

LOCK = threading.Lock()
WATCH_STATUS = {"hidup": False, "putaran": 0, "terakhir": None, "perubahan": []}

KOLOM = {
    "she": [("tanggal", "Tgl", 5), ("shift", "Shift", 4), ("lbn", "LBN", 8),
            ("x.area", "Area", 8), ("x.kategori", "Kat. Safety", 9),
            ("masalah", "Problem Statement", 19), ("sebab", "RootCause", 13),
            ("tindakan", "Action Plan", 13), ("pic", "PIC", 6), ("due", "Due", 5),
            ("umur", "Umur", 4), ("status", "Status", 6)],
    "quality": [("tanggal", "Tanggal", 5), ("shift", "Shift", 4), ("lbn", "LBN", 8),
                ("x.kategori", "Category", 8), ("x.prioritas", "Prioritas", 6),
                ("masalah", "Problem", 17), ("x.validasi", "Validasi QCP", 13),
                ("sebab", "Root Cause", 12), ("tindakan", "Action Plan", 12),
                ("pic", "PIC", 6), ("due", "Due", 5), ("status", "Status", 6)],
    "produksi": [("tanggal", "Date", 5), ("shift", "Shift", 4), ("lbn", "LBN", 8),
                 ("x.kategori", "Category", 8), ("x.prioritas", "Prioritas", 6),
                 ("masalah", "Problem", 17), ("x.dt_min", "DT (min)", 6),
                 ("sebab", "RootCause", 12), ("tindakan", "Corrective / Preventive", 13),
                 ("pic", "PIC", 6), ("due", "Due", 5), ("status", "Status", 6),
                 ("x.occurrence", "O / R", 4)],
    "delivery": [("tanggal", "Tgl", 6), ("shift", "Shift", 5), ("lbn", "PO", 10),
                 ("masalah", "Plan vs Real", 24), ("sebab", "Sebab", 18),
                 ("tindakan", "Tindakan", 18), ("pic", "PIC", 8), ("status", "Status", 8)],
    "teknik": [("tanggal", "Tgl", 6), ("shift", "Shift", 5), ("lbn", "Mesin", 10),
               ("masalah", "Temuan / Work Order", 24), ("sebab", "Sebab", 18),
               ("tindakan", "Tindakan", 18), ("pic", "PIC", 8), ("status", "Status", 8)],
}

DURASI = {"absensi": 30, "she": 25, "quality": 25, "produksi": 30,
          "delivery": 20, "teknik": 20, "ringkasan": 20}


# ------------------------------------------------------------------ pengawas folder


def pengawas_folder(interval=3, stabil=4):
    """Deteksi berkas berubah tanpa petugas melakukan apa pun.

    Debounce: tunggu mtime stabil supaya tidak membaca file yang sedang disimpan.
    Berkas kunci Excel (~$nama.xlsx) dilewati.
    """
    WATCH_STATUS["hidup"] = True
    jejak = {}
    kandidat = {}
    while True:
        try:
            con = core.connect()
            sumber = [dict(r) for r in con.execute("SELECT * FROM sumber WHERE status<>'berhenti'")]
            con.close()
            for s in sumber:
                p = s["path"]
                kunci = s["sumber_id"]
                if not os.path.exists(p):
                    continue
                lock = os.path.join(os.path.dirname(p), "~$" + os.path.basename(p))
                sig = (os.path.getmtime(p), os.path.getsize(p))
                if jejak.get(kunci) is None:
                    jejak[kunci] = sig
                    continue
                if sig != jejak[kunci]:
                    kandidat[kunci] = (sig, time.time())
                    jejak[kunci] = sig
            for kunci, (sig, ts) in list(kandidat.items()):
                if time.time() - ts < stabil:
                    continue
                s = next((x for x in sumber if x["sumber_id"] == kunci), None)
                kandidat.pop(kunci, None)
                if s is None:
                    continue
                lock = os.path.join(os.path.dirname(s["path"]), "~$" + os.path.basename(s["path"]))
                if os.path.exists(lock):
                    kandidat[kunci] = (sig, time.time())  # masih dibuka Excel: tunggu
                    continue
                with LOCK:
                    con = core.connect()
                    r = core.ingest_file(con, kunci)
                    con.close()
                WATCH_STATUS["terakhir"] = core.now()
                WATCH_STATUS["perubahan"].insert(0, {
                    "sumber_id": kunci, "waktu": core.now(),
                    "tambah": r.get("tambah", 0), "ubah": r.get("ubah", 0),
                    "pesan": r.get("pesan", "tersinkron"),
                })
                del WATCH_STATUS["perubahan"][20:]
            WATCH_STATUS["putaran"] += 1
        except Exception as exc:  # pengawas tidak boleh mati karena satu berkas
            WATCH_STATUS["terakhir"] = f"galat: {exc}"
        time.sleep(interval)


# ------------------------------------------------------------------ pembantu state


def sesi_aktif(con, plant, line="*"):
    row = con.execute(
        "SELECT * FROM sesi WHERE plant=? AND line=? ORDER BY dibuka_pada DESC LIMIT 1",
        (plant, line),
    ).fetchone()
    if row:
        return dict(row)
    tanggal = dt.date.today().strftime("%Y-%m-%d")
    sid = f"{plant}-{line}-{tanggal}-1".replace(" ", "")
    con.execute(
        "INSERT INTO sesi(sesi_id,plant,line,tanggal,shift,status,token,dibuka_pada) "
        "VALUES(?,?,?,?,?,'DIBUKA',?,?)",
        (sid, plant, line, tanggal, "1", secrets.token_urlsafe(8), core.now()),
    )
    from seed_demo import NAMA_DEMO
    for nm in NAMA_DEMO:
        con.execute("INSERT OR IGNORE INTO absensi(sesi_id,nama,status,diubah_pada,perangkat) "
                    "VALUES(?,?,'hadir',?,'auto')", (sid, nm, core.now()))
    con.commit()
    return dict(con.execute("SELECT * FROM sesi WHERE sesi_id=?", (sid,)).fetchone())


def nilai_kolom(row, key, today):
    if key.startswith("x."):
        return json.loads(row.get("extras") or "{}").get(key[2:], "") or "—"
    if key == "umur":
        try:
            d0 = dt.date.fromisoformat(row["tanggal"])
            return str(max((today - d0).days, 0))
        except (ValueError, TypeError):
            return "—"
    if key in ("tanggal", "due") and row.get(key):
        try:
            d = dt.date.fromisoformat(row[key])
            return f"{d.day} {['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des'][d.month-1]}"
        except ValueError:
            return row[key]
    return row.get(key) or "—"


def bangun_halaman(con, plant, line, tanggal, today):
    halaman = []
    for key, nama, warna in core.DIVISI:
        info = core.ambil_divisi(con, key, tanggal, plant=plant,
                                 line=None if line == "*" else line)
        src = info["sumber"]
        terdaftar = bool(src)
        sinkron = max([s["sinkron_terakhir"] or "" for s in src], default="")
        if not terdaftar:
            status, pesan = "menunggu_berkas", "Berkas Excel divisi ini belum didaftarkan (R-86)"
        elif not sinkron:
            status, pesan = "belum_tersinkron", "Berkas terdaftar tetapi belum pernah tersinkron"
        elif not info["semua"]:
            status, pesan = "belum_diisi", f"Tidak ada baris bertanggal {tanggal} pada berkas ini"
        else:
            status, pesan = "tersinkron", ""
        cols = KOLOM[key]
        baris = []
        for r in info["semua"][:7]:
            baris.append({
                "sel": [nilai_kolom(r, c[0], today) for c in cols],
                "status": r["status"],
                "flag": r["flagged"],
                "kunci": r["kunci_baris"],
                "sumber_id": r["sumber_id"],
                "baris_excel": r["baris_excel"],
            })
        halaman.append({
            "key": key, "nama": nama, "warna": warna, "durasi": DURASI[key],
            "status": status, "pesan": pesan, "terdaftar": terdaftar,
            "sinkron_terakhir": sinkron,
            "jumlah": len(info["semua"]),
            "kpi": core.kpi_periode(con, key, tanggal, plant) if terdaftar else [],
            "kolom": [{"nama": c[1], "bobot": c[2]} for c in cols],
            "baris": baris,
            "berkas": [{"id": s["sumber_id"], "path": os.path.basename(s["path"] or ""),
                        "sheet": s["sheet"], "status": s["status"],
                        "sinkron": s["sinkron_terakhir"], "pesan": s["pesan"]} for s in src],
        })
    return halaman


@app.route("/api/state")
def api_state():
    con = core.connect()
    plant = request.args.get("plant", "Snack")
    line = request.args.get("line", "*")
    today = dt.date.today()
    tersedia = core.tanggal_tersedia(con, plant)
    demo = request.args.get("demo", "1") == "1"
    minta = request.args.get("tanggal")
    if minta:
        tanggal = minta
    elif demo:
        tanggal = core.tanggal_terpadat(con, plant) or (tersedia[0] if tersedia else today.strftime("%Y-%m-%d"))
    else:
        tanggal = today.strftime("%Y-%m-%d")
    s = sesi_aktif(con, plant, line)
    ab = [dict(r) for r in con.execute(
        "SELECT nama,status FROM absensi WHERE sesi_id=? ORDER BY rowid", (s["sesi_id"],))]
    hit = {k: sum(1 for a in ab if a["status"] == k) for k in
           ("hadir", "sakit", "izin", "alpa", "terlambat", "dinas luar", "belum pasti")}
    halaman = bangun_halaman(con, plant, line, tanggal, today)
    ring = []
    for h in halaman:
        k = {}
        for i in h["kpi"]:
            harian = i["vals"][3] if len(i["vals"]) > 3 else {"v": "—"}
            k[i["item"]] = harian["v"]
        ring.append({"key": h["key"], "nama": h["nama"], "warna": h["warna"],
                     "jumlah": h["jumlah"], "status": h["status"],
                     "open": k.get("Open", "—"),
                     "completion": k.get("PICA completion rate", "—"),
                     "lewat": k.get("Lewat tenggat", "—")})
    out = {
        "plant": plant, "line": line, "label_line": "Semua line" if line == "*" else line,
        "tanggal": tanggal,
        "hari_ini": today.strftime("%Y-%m-%d"),
        "demo": bool(demo and tanggal != today.strftime("%Y-%m-%d")),
        "tanggal_tersedia": tersedia[:30],
        "sesi": s,
        "absensi": {"nama": ab, "total": len(ab), "hitung": hit,
                    "dikonfirmasi": bool(s["dikonfirmasi_pada"])},
        "halaman": halaman, "ringkasan": ring,
        "durasi": DURASI,
        "pengawas": WATCH_STATUS,
        "jam": dt.datetime.now().strftime("%H.%M"),
    }
    con.close()
    return jsonify(out)


@app.route("/api/absensi", methods=["POST"])
def api_absensi():
    d = request.get_json(force=True)
    con = core.connect()
    s = sesi_aktif(con, d.get("plant", "Snack"), d.get("line", "*"))
    if s["dikonfirmasi_pada"]:
        con.close()
        return jsonify({"ok": False, "pesan": "Absensi sudah dikonfirmasi; koreksi lewat Supervisor"}), 409
    status = d.get("status", "hadir")
    con.execute("UPDATE absensi SET status=?, diubah_pada=?, perangkat=? WHERE sesi_id=? AND nama=?",
                (status, core.now(), d.get("perangkat", "tv"), s["sesi_id"], d["nama"]))
    con.execute("INSERT INTO audit(waktu,pelaku,aksi,rinci) VALUES(?,?,?,?)",
                (core.now(), d.get("perangkat", "tv"), "absensi",
                 json.dumps({"nama": d["nama"], "status": status}, ensure_ascii=False)))
    con.commit()
    con.close()
    return jsonify({"ok": True})


@app.route("/api/konfirmasi", methods=["POST"])
def api_konfirmasi():
    d = request.get_json(force=True) if request.data else {}
    con = core.connect()
    s = sesi_aktif(con, d.get("plant", "Snack"), d.get("line", "*"))
    con.execute("UPDATE sesi SET status='DIKONFIRMASI', dikonfirmasi_pada=? WHERE sesi_id=?",
                (core.now(), s["sesi_id"]))
    con.execute("UPDATE absensi SET status='hadir' WHERE sesi_id=? AND status='belum pasti'",
                (s["sesi_id"],))
    con.execute("INSERT INTO audit(waktu,pelaku,aksi,rinci) VALUES(?,?,?,?)",
                (core.now(), d.get("pelaku", "leader"), "konfirmasi_absensi", s["sesi_id"]))
    con.commit()
    con.close()
    return jsonify({"ok": True})


@app.route("/api/buka", methods=["POST"])
def api_buka():
    """Supervisor/DH membuka ulang sesi (alasan tercatat) — jalan keluar darurat R-81."""
    d = request.get_json(force=True)
    con = core.connect()
    s = sesi_aktif(con, d.get("plant", "Snack"), d.get("line", "*"))
    con.execute("UPDATE sesi SET status='DIBUKA', dikonfirmasi_pada=NULL WHERE sesi_id=?",
                (s["sesi_id"],))
    con.execute("INSERT INTO audit(waktu,pelaku,aksi,rinci) VALUES(?,?,?,?)",
                (core.now(), d.get("pelaku", "supervisor"), "buka_ulang_sesi",
                 d.get("alasan", "(tanpa alasan)")))
    con.commit()
    con.close()
    return jsonify({"ok": True})


@app.route("/api/sync", methods=["POST"])
def api_sync():
    d = request.get_json(force=True) if request.data else {}
    con = core.connect()
    ids = [d["sumber_id"]] if d.get("sumber_id") else [
        r["sumber_id"] for r in con.execute("SELECT sumber_id FROM sumber")]
    hasil = []
    with LOCK:
        for sid in ids:
            hasil.append({"sumber_id": sid, **core.ingest_file(con, sid, force=True)})
    con.close()
    return jsonify({"ok": True, "hasil": hasil})


@app.route("/api/admin")
def api_admin():
    con = core.connect()
    out = {
        "sumber": [dict(r) for r in con.execute("SELECT * FROM sumber ORDER BY plant, divisi")],
        "log": [dict(r) for r in con.execute("SELECT * FROM ingest_log ORDER BY id DESC LIMIT 25")],
        "karantina": [dict(r) for r in con.execute(
            "SELECT * FROM karantina ORDER BY id DESC LIMIT 25")],
        "karantina_total": con.execute("SELECT COUNT(*) c FROM karantina").fetchone()["c"],
        "flagged": con.execute("SELECT COUNT(*) c FROM kasus WHERE flagged<>''").fetchone()["c"],
        "kasus": con.execute("SELECT COUNT(*) c FROM kasus WHERE terhapus=0").fetchone()["c"],
        "terhapus": con.execute("SELECT COUNT(*) c FROM kasus WHERE terhapus=1").fetchone()["c"],
        "audit": [dict(r) for r in con.execute("SELECT * FROM audit ORDER BY id DESC LIMIT 20")],
        "pengawas": WATCH_STATUS,
    }
    con.close()
    return jsonify(out)


@app.route("/qr/<token>.png")
def qr(token):
    import qrcode
    url = request.host_url.rstrip("/") + f"/s/{token}"
    img = qrcode.make(url, box_size=8, border=2)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return send_file(buf, mimetype="image/png")


@app.route("/s/<token>")
def landing_sesi(token):
    con = core.connect()
    s = con.execute("SELECT * FROM sesi WHERE token=?", (token,)).fetchone()
    con.close()
    if s is None:
        return render_template("sesi.html", sesi=None, token=token), 404
    return render_template("sesi.html", sesi=dict(s), token=token)


@app.route("/fonts/<path:name>")
def fonts(name):
    return send_from_directory(os.path.join(core.ROOT, "docs", "assets", "fonts"), name)


@app.route("/")
def tv():
    return render_template("tv.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


@app.route("/healthz")
def healthz():
    return jsonify({"ok": True, "pengawas": WATCH_STATUS["hidup"]})


def mulai():
    t = threading.Thread(target=pengawas_folder, daemon=True, name="pengawas-excel")
    t.start()
    return t


mulai()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True, use_reloader=False)