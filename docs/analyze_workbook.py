#!/usr/bin/env python3
"""Analisis tiga workbook DMS (Snack, Exist Plant, New Plant) dengan definisi sama.

Definisi baris kasus: baris pada tabel kasus yang punya tanggal valid.
Keluaran: docs/data_plants.json + ringkasan stdout.
Jalankan: python3 docs/analyze_workbook.py
"""
import json
import re
import statistics
from collections import Counter
from datetime import datetime

from openpyxl import load_workbook

FILES = {
    "Snack": "reference/12. Konsep Penilaian DMS Snack Des 24.xlsx",
    "Exist Plant": "reference/12. Konsep Penilaian DMS EP Des 24.xlsx",
    "New Plant": "reference/12. Konsep Penilaian DMS NP Des 24 (1).xlsx",
}
TODAY = datetime(2026, 11, 2)
SHEETS = {"SHE": "Resume SHE", "QC": "Resume QC", "Prod": "Resume Prod"}
FMT = ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y", "%d %B %Y", "%d/%m/%y")


def norm(v):
    return re.sub(r"\s+", " ", str(v)).strip().lower() if v is not None else ""


def parse_date(v):
    if isinstance(v, datetime):
        return v
    if isinstance(v, str):
        s = v.replace("\xa0", " ").strip()
        for f in FMT:
            try:
                return datetime.strptime(s[:11].strip(), f)
            except ValueError:
                continue
    return None


def find_header(ws):
    for i, row in enumerate(ws.iter_rows(min_row=1, max_row=60, values_only=True)):
        heads = [norm(c) for c in row]
        if "no" in heads and ("date" in heads or any("tanggal" in h for h in heads)):
            return i, heads
    return None, None


def col(heads, *names, exclude=()):
    for want in names:
        for i, h in enumerate(heads):
            if not h or any(e in h for e in exclude):
                continue
            if h == want or h.startswith(want):
                return i
    return None


def summary_block(ws):
    """Angka ringkasan PICA di dalam sheet (OPEN/CLOSE/TOTAL + Occ/Rec)."""
    out = {}
    for row in ws.iter_rows(min_row=1, max_row=40, values_only=True):
        cells = [norm(c) for c in row]
        for j, c in enumerate(cells):
            if c in ("open", "close", "total") and j <= 2 and c.upper() not in out:
                for k in (j + 1, j + 2):
                    if k < len(row) and isinstance(row[k], (int, float)):
                        out[c.upper()] = int(row[k])
                        break
            if c in ("occurrence", "recurrence") and j in (4, 5, 24, 25) and c.title() not in out:
                for k in (j + 1, j + 2):
                    if k < len(row) and isinstance(row[k], (int, float)):
                        out[c.title()] = int(row[k])
                        break
    return out


def analyse_sheet(wb, sheet_name):
    if sheet_name not in wb.sheetnames:
        return None
    ws = wb[sheet_name]
    hi, heads = find_header(ws)
    if hi is None:
        return {"error": "header tidak ditemukan"}
    c = {
        "date": col(heads, "date", "tanggal"),
        "line": col(heads, "line", exclude=("lbn",)),
        "lbn": col(heads, "lbn name", "lbn"),
        "cat": col(heads, "category", exclude=("problem", "safety", "case")),
        "prio": col(heads, "priority level", "priority"),
        "prob": col(heads, "problem", exclude=("statement",)),
        "rc": col(heads, "rootcause", "root cause"),
        "due": col(heads, "due date"),
        "status": col(heads, "status"),
        "dt": col(heads, "dt (min)", "dt"),
        "pic": col(heads, "pic"),
        "before": col(heads, "picture before"),
        "after": col(heads, "picture after"),
    }

    rows, dates = [], []
    for r in ws.iter_rows(min_row=hi + 2, values_only=True):
        def g(k):
            i = c[k]
            return r[i] if i is not None and i < len(r) else None
        d = parse_date(g("date"))
        if d is None:
            continue
        rows.append(r)
        dates.append(d)

    n = len(rows)

    def g(r, k):
        i = c[k]
        return r[i] if i is not None and i < len(r) else None

    def filled(k):
        return sum(1 for r in rows if norm(g(r, k)))

    status_close = [r for r in rows if "close" in norm(g(r, "status"))]
    close_no_rc = [r for r in status_close if not norm(g(r, "rc"))]

    keys = Counter()
    for r in rows:
        k = (norm(g(r, "lbn")) + " | " + norm(g(r, "prob"))[:60]).strip(" |")
        if k and k != "|":
            keys[k] += 1
    reps = {k: v for k, v in keys.items() if v >= 3}

    def cnt(k):
        return Counter(norm(g(r, k)) for r in rows if norm(g(r, k)))

    dts = []
    for r in rows:
        v = g(r, "dt")
        if isinstance(v, (int, float)) and v > 0:
            dts.append(float(v))
        elif isinstance(v, str):
            m = re.match(r"\s*(\d+(?:[.,]\d+)?)", v)
            if m:
                dts.append(float(m.group(1).replace(",", ".")))

    overdue = []
    for r in rows:
        dd = parse_date(g(r, "due"))
        st = norm(g(r, "status"))
        if dd and dd < TODAY and st != "close":
            overdue.append((TODAY - dd).days)

    errs = Counter()
    for r in ws.iter_rows(min_row=1, max_row=min(ws.max_row, 4000), values_only=True):
        for v in r:
            if isinstance(v, str) and v.startswith("#"):
                errs[v] += 1

    return {
        "kasus": n,
        "rentang": [min(dates).strftime("%Y-%m-%d"), max(dates).strftime("%Y-%m-%d")],
        "root_cause_pct": round(100 * filled("rc") / n, 1),
        "due_date_pct": round(100 * filled("due") / n, 1),
        "bukti_pct": round(100 * (filled("before") + filled("after")) / (2 * n), 1) if c["before"] is not None else None,
        "pic_pct": round(100 * filled("pic") / n, 1) if c["pic"] is not None else None,
        "close": len(status_close),
        "close_tanpa_sebab": len(close_no_rc),
        "pola_3x": len(reps),
        "kasus_dalam_pola": sum(reps.values()),
        "pola_teratas": sorted([[*k.split(" | "), v] for k, v in reps.items()], key=lambda x: -x[-1])[:3],
        "top_lbn": cnt("lbn").most_common(3),
        "top_line": cnt("line").most_common(3),
        "top_kategori": cnt("cat").most_common(2),
        "high_pct": round(100 * cnt("prio").get("high", 0) / max(sum(cnt("prio").values()), 1), 1),
        "top_pic": cnt("pic").most_common(2),
        "dt_median": round(statistics.median(dts)) if dts else None,
        "dt_total": round(sum(dts)) if dts else None,
        "overdue": len(overdue),
        "overdue_tertua": max(overdue) if overdue else 0,
        "ringkasan_sheet": summary_block(ws),
        "error_sel": dict(errs),
    }


def analyse_bulanan(wb):
    """Jumlah kasus per bulan (YYYY-MM) untuk ketiga sheet kasus."""
    out = {}
    for _, sheet in SHEETS.items():
        if sheet not in wb.sheetnames:
            continue
        ws = wb[sheet]
        hi, heads = find_header(ws)
        if hi is None:
            continue
        c_date = col(heads, "date", "tanggal")
        if c_date is None:
            continue
        for r in ws.iter_rows(min_row=hi + 2, values_only=True):
            d = parse_date(r[c_date] if c_date < len(r) else None)
            if d is None:
                continue
            key = d.strftime("%Y-%m")
            out[key] = out.get(key, 0) + 1
    return dict(sorted(out.items()))


def jumlah_line(wb):
    """Jumlah nama line unik (setelah normalisasi) pada sheet QC dan Prod."""
    names = set()
    for sheet in ("Resume QC", "Resume Prod"):
        if sheet not in wb.sheetnames:
            continue
        ws = wb[sheet]
        hi, heads = find_header(ws)
        if hi is None:
            continue
        c_line = col(heads, "line", exclude=("lbn",))
        c_lbn = col(heads, "lbn name", "lbn")
        for r in ws.iter_rows(min_row=hi + 2, values_only=True):
            for idx in (c_line, c_lbn):
                if idx is not None and idx < len(r) and norm(r[idx]):
                    names.add(norm(r[idx]))
    return len(names)


def analyse_index(wb):
    if "DMS_INDEX" not in wb.sheetnames:
        return []
    out, cur = [], None
    for r in wb["DMS_INDEX"].iter_rows(values_only=True):
        a = str(r[1]) if len(r) > 1 and r[1] is not None else ""
        low = a.lower()
        if "dms - inde" in low:
            cur = {"blok": re.sub(r"(?i)dms\s*-\s*inde[x]?", "", a).strip(),
                   "rows": [], "index": None}
            out.append(cur)
        elif cur is not None and a in ("Summary DMS to KPI", "Ceklist Daily", "Corporate"):
            cur["rows"].append([a, r[4], r[5], r[6]])
        elif cur is not None and a == "DMS Index":
            cur["index"] = round(r[7], 2) if isinstance(r[7], (int, float)) else r[7]
    return out


result = {}
for plant, path in FILES.items():
    wb = load_workbook(path, read_only=True, data_only=True)
    d = {"file": path.split("/")[-1]}
    for key, sheet in SHEETS.items():
        d[key] = analyse_sheet(wb, sheet)
    d["index_blok"] = analyse_index(wb)
    d["bulanan"] = analyse_bulanan(wb)
    d["jumlah_entitas_line"] = jumlah_line(wb)
    tot = sum(d[k]["kasus"] for k in SHEETS if d[k])
    d["total_kasus"] = tot
    d["close_tanpa_sebab"] = sum(d[k]["close_tanpa_sebab"] for k in SHEETS if d[k])
    d["pola_3x"] = sum(d[k]["pola_3x"] for k in SHEETS if d[k])
    d["kasus_dalam_pola"] = sum(d[k]["kasus_dalam_pola"] for k in SHEETS if d[k])
    d["overdue"] = sum(d[k]["overdue"] for k in SHEETS if d[k])
    d["error_sel_total"] = sum(sum(d[k]["error_sel"].values()) for k in SHEETS if d[k])
    result[plant] = d
    print(f"{plant:<14} kasus {tot:>6} | SHE {d['SHE']['kasus']:>5} QC {d['QC']['kasus']:>5} "
          f"Prod {d['Prod']['kasus']:>5} | close tanpa sebab {d['close_tanpa_sebab']:>4} | "
          f"pola {d['pola_3x']:>3} | overdue {d['overdue']:>3} | error sel {d['error_sel_total']}")

bulan_total = {}
for v in list(result.values()):
    for k, c in v.get("bulanan", {}).items():
        bulan_total[k] = bulan_total.get(k, 0) + c
result["_bulanan_total"] = dict(sorted(bulan_total.items()))

plants = {k: v for k, v in result.items() if not k.startswith("_")}
grand = {k: sum(v[k] for v in plants.values()) for k in
         ("total_kasus", "close_tanpa_sebab", "pola_3x", "kasus_dalam_pola", "overdue", "error_sel_total")}
result["_total"] = grand
print("bulan terakhir:", list(bulan_total.items())[-6:])
print("TOTAL", grand)

with open("docs/data_plants.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=1, ensure_ascii=False, default=str)
print("saved docs/data_plants.json")
