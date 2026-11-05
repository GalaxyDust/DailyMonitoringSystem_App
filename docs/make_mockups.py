#!/usr/bin/env python3
"""
Ilustrasi layar sistem DMS (bukan tangkapan aplikasi asli):
  docs/assets/mockup/form.png   -> form harian di tablet
  docs/assets/mockup/dasbor.png -> dasbor L1-L3 di laptop
  docs/assets/mockup/tv.png     -> layar lantai di TV
  docs/assets/mockup/admin.png  -> halaman admin

Semua digambar 1600x1000 dengan warna template (navy/teal/gold/merah).

Jalankan: python3 docs/make_mockups.py
"""
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 1000
OUT = "docs/assets/mockup"

NAVY = (0x1F, 0x33, 0x64)
TEAL = (0x2E, 0x86, 0x8C)
GOLD = (0xC8, 0xA5, 0x2B)
RED = (0xB0, 0x2F, 0x2F)
INK = (0x22, 0x28, 0x33)
GREY = (0x5C, 0x64, 0x72)
LGREY = (0x8B, 0x93, 0xA1)
RULE = (0xD5, 0xDA, 0xE3)
SOFT = (0xF4, 0xF6, 0xFA)
PALE = (0xE9, 0xED, 0xF4)
WHITE = (0xFF, 0xFF, 0xFF)
DARK = (0x20, 0x26, 0x33)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def f(size, bold=False):
    return ImageFont.truetype(FB if bold else FR, size)


def canvas():
    im = Image.new("RGB", (W, H), WHITE)
    return im, ImageDraw.Draw(im)


def rr(d, box, r, fill=None, line=None, w=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=line, width=w)


def t(d, xy, s, size=22, color=INK, bold=False, anchor="la"):
    d.text(xy, s, font=f(size, bold), fill=color, anchor=anchor)


def chip(d, x, y, w, h, label, color, size=15, fs=WHITE):
    rr(d, (x, y, x + w, y + h), h // 2, fill=color)
    t(d, (x + w / 2, y + h / 2 - 1), label, size, fs, True, "mm")


def shadow(im, box, blur=26, alpha=26):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle(box, radius=30, fill=(20, 30, 50, alpha))
    from PIL import ImageFilter
    lay = lay.filter(ImageFilter.GaussianBlur(blur))
    im.paste(Image.alpha_composite(im.convert("RGBA"), lay).convert("RGB"), (0, 0))


# --------------------------------------------------------------- 1 · form harian
def form():
    im, d = canvas()
    shadow(im, (66, 76, 1534, 944))
    d = ImageDraw.Draw(im)
    rr(d, (60, 70, 1540, 938), 34, fill=DARK)
    d.ellipse((790, 82, 810, 102), fill=(0x3A, 0x42, 0x52))
    rr(d, (82, 116, 1518, 916), 12, fill=WHITE)

    d.rectangle((82, 116, 1518, 186), fill=NAVY)
    t(d, (112, 138), "ISI PAPAN  ·  SNACK  ·  LINE 9", 26, WHITE, True)
    t(d, (1488, 140), "Sen, 3 Nov 2026 · Shift 1", 21, (0xC9, 0xD3, 0xE6), anchor="ra")

    # tab divisi: tiap divisi mengisi bagiannya sendiri
    tabs = [("SHE", False), ("QUALITY", False), ("PRODUKSI", True), ("TEKNIK", False),
            ("DELIVERY", False)]
    x = 100
    for name, on in tabs:
        tw = 26 + len(name) * 12
        if on:
            rr(d, (x, 196, x + tw, 244), 8, fill=NAVY)
            t(d, (x + tw / 2, 220), name, 18, WHITE, True, "mm")
        else:
            rr(d, (x, 196, x + tw, 244), 8, fill=(0xF2, 0xF4, 0xF8), line=RULE, w=2)
            t(d, (x + tw / 2, 220), name, 18, GREY, True, "mm")
        x += tw + 10
    t(d, (1488, 210), "draf tersimpan 07.08", 18, GREY, anchor="ra")
    t(d, (1488, 232), "tab lain: milik divisi lain", 16, LGREY, anchor="ra")

    cols = [(112, 600), (600, 770), (770, 940), (940, 1200), (1200, 1490)]
    head = ["ITEM · PRODUKSI", "TARGET", "HASIL", "STATUS", "SEBAB / BUKTI"]
    d.rectangle((112, 258, 1490, 296), fill=SOFT)
    for (x0, x1), h_ in zip(cols, head):
        t(d, (x0 + 12, 268), h_, 16, LGREY, True)

    rows = [("Checklist A · critical point", "100%", "100%", "SESUAI", "", TEAL),
            ("Checklist B · suhu ruang", "≤ 18 °C", "16 °C", "SESUAI", "", TEAL),
            ("Output shift", "8.400 pcs", "8.120 pcs", "DI BAWAH TARGET", "tunggu material", GOLD),
            ("Downtime · WS L02", "≤ 20 mnt", "48 mnt", "LEWAT BATAS", "belt aus · ke teknik", RED),
            ("OEE line", "≥ 85%", "78%", "DI BAWAH TARGET", "ikut downtime", GOLD)]
    y = 296
    for i, (item, tg, hs, st, sb, col) in enumerate(rows):
        if i % 2:
            d.rectangle((112, y, 1490, y + 72), fill=(0xFA, 0xFB, 0xFD))
        d.line((112, y + 72, 1490, y + 72), fill=RULE, width=1)
        t(d, (124, y + 24), item, 21, INK)
        t(d, (612, y + 24), tg, 21, GREY)
        t(d, (782, y + 24), hs, 21, INK, True)
        cw = 22 + len(st) * 10
        chip(d, 950, y + 20, cw, 34, st, col, 14)
        t(d, (1213, y + 24), sb if sb else "—", 17, GREY)
        y += 72

    rr(d, (112, 668, 700, 884), 12, fill=(0xFD, 0xF3, 0xF3), line=(0xD9, 0x9C, 0x9C), w=2)
    t(d, (132, 684), "SEBAB WAJIB DIISI · DI BAWAH TARGET", 16, RED, True)
    t(d, (132, 714), "Belt WS L02 aus, diganti", 24, INK)
    t(d, (132, 756), "Tindakan: ganti belt, cek sebelum shift 2", 18, GREY)
    t(d, (132, 784), "PIC: Dhani  ·  tenggat 3 Nov 16.00", 18, GREY)
    t(d, (132, 818), "Sudah dikirim ke Teknik sebagai WO EP-TK-0031", 17, TEAL, True)

    rr(d, (716, 668, 1200, 884), 12, fill=SOFT, line=RULE, w=2)
    t(d, (736, 684), "BUKTI FOTO · 1 BERKAS", 16, LGREY, True)
    for i in range(3):
        x0 = 736 + i * 148
        rr(d, (x0, 716, x0 + 130, 828), 8,
           fill=(0xD8, 0xE4, 0xDD) if i == 0 else (0xE3, 0xE8, 0xF0),
           line=(0xC2, 0xCB, 0xD9), w=2)
        t(d, (x0 + 65, 772), "foto" if i == 0 else "+", 18, GREY, False, "mm")
    t(d, (736, 844), "foto menempel pada kasus, bukan di ponsel", 16, GREY)

    rr(d, (1218, 668, 1490, 748), 12, fill=NAVY)
    t(d, (1354, 708), "Kirim bagian produksi", 21, WHITE, True, "mm")
    t(d, (1218, 762), "angka langsung masuk", 18, GREY)
    t(d, (1218, 788), "papan, TV, dan dasbor", 18, GREY)
    t(d, (1218, 824), "tidak ada salinan kedua", 17, TEAL, True)

    im.save(f"{OUT}/form.png")


# --------------------------------------------------------------- 2 · dasbor
def dasbor():
    im, d = canvas()
    shadow(im, (170, 70, 1430, 830))
    d = ImageDraw.Draw(im)
    rr(d, (170, 70, 1430, 830), 18, fill=DARK)
    rr(d, (188, 88, 1412, 812), 8, fill=WHITE)
    # alas laptop
    rr(d, (110, 838, 1490, 902), 14, fill=(0xD8, 0xDD, 0xE7), line=(0xB9, 0xC1, 0xD0), w=2)
    d.rounded_rectangle((690, 838, 910, 852), radius=7, fill=(0xBF, 0xC7, 0xD6))

    # navigasi kiri
    d.rectangle((188, 88, 424, 812), fill=NAVY)
    t(d, (212, 112), "DMS", 30, WHITE, True)
    t(d, (212, 150), "Daily Monitoring", 16, (0xA9, 0xB8, 0xD4))
    nav = [("Hari ini", True), ("Kasus terbuka", False), ("Tren pekan", False),
           ("Perbandingan plant", False), ("Laporan", False), ("Pengaturan", False)]
    y = 210
    for name, on in nav:
        if on:
            rr(d, (204, y - 8, 408, y + 34), 8, fill=(0x2C, 0x45, 0x7C))
        t(d, (222, y), name, 18, WHITE if on else (0xB6, 0xC3, 0xDA), on)
        y += 52
    t(d, (212, 742), "SNACK · LINE 9", 16, GOLD, True)

    # kepala
    d.rectangle((424, 88, 1412, 158), fill=WHITE)
    d.line((424, 158, 1412, 158), fill=RULE, width=2)
    t(d, (448, 108), "Dasbor L2 · Supervisor", 27, NAVY, True)
    t(d, (1388, 114), "Sen, 3 Nov 2026 · 07.10", 18, GREY, anchor="ra")

    # kartu KPI
    kpi = [("Kasus hari ini", "96", NAVY), ("Close lengkap", "74%", TEAL),
           ("Lewat tenggat", "8", RED), ("Pola berulang", "5", GOLD)]
    x = 448
    for name, val, col in kpi:
        rr(d, (x, 178, x + 220, 300), 10, fill=SOFT, line=RULE, w=2)
        d.rectangle((x, 178, x + 6, 300), fill=col)
        t(d, (x + 22, 196), name, 17, GREY)
        t(d, (x + 22, 226), val, 44, col, True)
        x += 234

    # grafik batang
    rr(d, (448, 318, 940, 590), 10, fill=WHITE, line=RULE, w=2)
    t(d, (468, 332), "Kasus per pilar · 7 hari", 20, NAVY, True)
    bars = [("SHE", 62, 48, NAVY), ("QC", 90, 74, TEAL), ("Prod", 78, 55, GOLD)]
    base = 552
    for i, (name, a, b, col) in enumerate(bars):
        x0 = 500 + i * 152
        d.rectangle((x0, base - a * 1.9, x0 + 46, base), fill=col)
        d.rectangle((x0 + 54, base - b * 1.9, x0 + 100, base), fill=PALE)
        t(d, (x0 + 23, base + 8), name, 16, GREY, False, "ma")
        t(d, (x0 + 23, base - a * 1.9 - 26), str(a), 16, col, True, "ma")

    # temuan terbuka
    rr(d, (958, 318, 1388, 590), 10, fill=WHITE, line=RULE, w=2)
    t(d, (978, 332), "Temuan terbuka · 3 teratas", 20, NAVY, True)
    items = [("Downtime WS L02", "menunggu bukti", "6 HARI", RED),
             ("BCT WS L04 P02", "berulang 134×", "BERULANG", GOLD),
             ("Checklist line 3", "kosong 3 hari", "HARI INI", TEAL)]
    y = 372
    for name, sub, badge, col in items:
        d.rectangle((978, y, 1368, y + 66), fill=(0xFA, 0xFB, 0xFD))
        d.rectangle((978, y, 984, y + 66), fill=col)
        t(d, (998, y + 12), name, 19, INK, True)
        t(d, (998, y + 38), sub, 15, GREY)
        chip(d, 1218, y + 18, 136, 30, badge, col, 13)
        y += 74

    # tabel kasus
    rr(d, (448, 608, 1388, 796), 10, fill=WHITE, line=RULE, w=2)
    t(d, (468, 620), "Kasus lewat tenggat", 20, NAVY, True)
    d.line((468, 656, 1368, 656), fill=RULE, width=2)
    rows = [("DT-0912  WS L02", "belt aus", "Dhani", "hari ini", RED),
            ("QC-0441  packing", "film roll", "Sigit", "2 hari", RED),
            ("PR-0087  line 3", "tunggu material", "Rani", "4 hari", GOLD)]
    y = 664
    for a, b, c_, d_, col in rows:
        t(d, (472, y + 6), a, 17, INK)
        t(d, (776, y + 6), b, 17, GREY)
        t(d, (1058, y + 6), c_, 17, GREY)
        t(d, (1330, y + 6), d_, 17, col, True, "ra")
        y += 42
    t(d, (440, 792), "", 12, GREY)

    im.save(f"{OUT}/dasbor.png")


# --------------------------------------------------------------- 3 · layar TV
def board(d, x, y, w, h, scale=1.0, cell=46, vf=13, shifts=("S1", "S2", "S3")):
    """Papan empat pilar bergaya papan hari ini: kolom pilar, baris item, kolom shift."""
    pillars = [
        ("SAFETY", (0xB0, 0x2F, 0x2F),
         [("zero accident", "0", "0", "0"),
          ("near miss", "1", "0", "2"),
          ("temuan KAK", "3", "1", "2"),
          ("tindakan buka", "2", "2", "1")]),
        ("QUALITY", (0xC8, 0xA5, 0x2B),
         [("defect visual %", "0,9", "0,5", "0,6"),
          ("critical point", "1", "0", "0"),
          ("hold / release", "2", "1", "0"),
          ("kalibrasi alat", "ok", "ok", "ok")]),
        ("PRODUCTIVITY", (0x1F, 0x33, 0x64),
         [("output shift", "8.120", "8.360", "8.400"),
          ("downtime (mnt)", "48", "22", "15"),
          ("checklist A/B", "ok", "ok", "ok"),
          ("OEE %", "78", "81", "84")]),
        ("DELIVERY", (0x2E, 0x86, 0x8C),
         [("plan vs real PO", "6/6", "5/6", "6/6"),
          ("keterlambatan", "1", "0", "0"),
          ("kesiapan muat", "ok", "ok", "ok"),
          ("retur kirim", "0", "0", "0")]),
    ]
    gap = 14 * scale
    cw = (w - gap * 3) / 4
    for i, (name, col, rows) in enumerate(pillars):
        cx = x + i * (cw + gap)
        d.rectangle((cx, y, cx + cw, y + 34 * scale), fill=col)
        t(d, (cx + cw / 2, y + 17 * scale), name, int(17 * scale), WHITE, True, "mm")
        hy = y + 34 * scale
        d.rectangle((cx, hy, cx + cw, hy + 26 * scale), fill=(0xF2, 0xF4, 0xF8))
        t(d, (cx + 10 * scale, hy + 13 * scale), "ITEM", int(12 * scale), GREY, True, "lm")
        ns = len(shifts)
        for k, sh in enumerate(shifts):
            cxx = cx + cw - (ns - k) * cell * scale
            t(d, (cxx + (cell / 2 - 1) * scale, hy + 13 * scale), sh, int(12 * scale), GREY, True, "mm")
        ry = hy + 26 * scale
        rh = (h - (ry - y)) / len(rows)
        for j, (item, a, b, c_) in enumerate(rows):
            if j % 2:
                d.rectangle((cx, ry, cx + cw, ry + rh), fill=(0xFA, 0xFB, 0xFD))
            d.line((cx, ry + rh, cx + cw, ry + rh), fill=RULE, width=1)
            t(d, (cx + 10 * scale, ry + rh / 2), item, int(13 * scale), INK, anchor="lm")
            for k, val in enumerate((a, b, c_)[:ns]):
                cxx = cx + cw - (ns - k) * cell * scale
                hit = hit_test(item, val)
                cell_col = {0: (0xE3, 0xF1, 0xE7), 1: (0xFB, 0xF0, 0xD6),
                            2: (0xF8, 0xE0, 0xE0), 3: (0xEF, 0xF1, 0xF5)}[hit]
                d.rectangle((cxx + 2 * scale, ry + 5 * scale,
                             cxx + (cell - 3) * scale, ry + rh - 5 * scale), fill=cell_col)
                tcol = {0: (0x1E, 0x6B, 0x3A), 1: (0x8A, 0x6C, 0x10),
                        2: RED, 3: LGREY}[hit]
                t(d, (cxx + (cell / 2 - 1) * scale, ry + rh / 2), val, int(vf * scale), tcol, True, "mm")
            ry += rh


def hit_test(item, val):
    """0 sesuai · 1 di bawah target · 2 lewat batas · 3 belum diisi."""
    if val == "—":
        return 3
    if item.startswith("output"):
        return 2 if val == "8.120" else 0
    if item.startswith("downtime"):
        return 2 if val == "48" else 0
    if item.startswith("defect"):
        return 1 if val == "0,9" else 0
    if item == "near miss" and val == "2":
        return 1
    if item == "plan vs real PO":
        return 1 if val == "5/6" else 0
    if item in ("tindakan buka", "hold / release") and val == "2":
        return 1
    if item == "keterlambatan" and val == "1":
        return 1
    return 0


def legend(d, x, y):
    items = [("sesuai target", (0xE3, 0xF1, 0xE7), (0x1E, 0x6B, 0x3A)),
             ("di bawah target", (0xFB, 0xF0, 0xD6), (0x8A, 0x6C, 0x10)),
             ("lewat batas", (0xF8, 0xE0, 0xE0), RED),
             ("belum diisi", (0xEF, 0xF1, 0xF5), GREY)]
    for name, fillc, tc in items:
        d.rectangle((x, y, x + 26, y + 22), fill=fillc)
        t(d, (x + 34, y + 11), name, 16, tc, True, "lm")
        x += 210


def tv():
    """Layar lantai berbentuk papan (bukan kartu)."""
    im, d = canvas()
    shadow(im, (50, 50, 1550, 900))
    d = ImageDraw.Draw(im)
    rr(d, (44, 44, 1556, 906), 16, fill=DARK)
    rr(d, (68, 68, 1532, 882), 6, fill=WHITE)

    d.rectangle((68, 68, 1532, 150), fill=NAVY)
    t(d, (100, 94), "PAPAN DMS  ·  SNACK  ·  LINE 9", 30, WHITE, True)
    t(d, (1500, 96), "Sen, 3 Nov 2026  ·  SHIFT 1", 21, GOLD, True, "ra")

    t(d, (100, 168), "Empat pilar, kolom shift, warna dibanding target  —  sama seperti papan hari ini",
      18, GREY)
    legend(d, 100, 200)

    board(d, 92, 244, 1416, 520, scale=1.35)

    d.rectangle((68, 800, 1532, 882), fill=(0xF4, 0xF6, 0xFA))
    t(d, (100, 826), "Pembaruan terakhir 07.12  ·  absensi shift 1: 25 dari 28 hadir", 20, NAVY, True)
    t(d, (1500, 826), "TANPA LOGIN  ·  BERGANTI PILAR TIAP 20 DETIK", 17, LGREY, True, "ra")
    im.save(f"{OUT}/tv.png")


def tv_absen():
    """Papan + panel absensi di layar yang sama (lapangan tinggal ketuk)."""
    im, d = canvas()
    shadow(im, (50, 50, 1550, 900))
    d = ImageDraw.Draw(im)
    rr(d, (44, 44, 1556, 906), 16, fill=DARK)
    rr(d, (68, 68, 1532, 882), 6, fill=WHITE)

    d.rectangle((68, 68, 1532, 150), fill=NAVY)
    t(d, (100, 94), "PAPAN DMS  ·  SNACK  ·  LINE 9", 30, WHITE, True)
    t(d, (1500, 96), "Sen, 3 Nov 2026  ·  SHIFT 1", 21, GOLD, True, "ra")

    legend(d, 100, 176)
    board(d, 92, 216, 900, 560, scale=0.98, cell=72, vf=15, shifts=("SHIFT 1",))

    # panel absensi
    px, py, pw = 1010, 176, 466
    rr(d, (px, py, px + pw, py + 600), 14, fill=(0xFA, 0xFB, 0xFD), line=RULE, w=2)
    d.rectangle((px, py, px + pw, py + 46), fill=TEAL)
    t(d, (px + 20, py + 23), "ABSENSI SHIFT 1", 22, WHITE, True, "lm")
    t(d, (px + pw - 20, py + 23), "TANPA LOGIN", 15, (0xD8, 0xEE, 0xEA), True, "rm")

    t(d, (px + 20, py + 66), "25 hadir", 34, (0x1E, 0x6B, 0x3A), True)
    t(d, (px + 190, py + 66), "· 2 sakit · 1 izin", 24, GREY)
    t(d, (px + 20, py + 112), "4 nama belum dikonfirmasi — ketuk namanya", 17, GREY)

    names = [("Rani", "hadir", 0), ("Dhani", "hadir", 0), ("Sigit", "sakit", 1),
             ("Asep", "?", 2), ("Yanti", "hadir", 0), ("Budi", "izin", 3),
             ("Wawan", "?", 2), ("Lina", "hadir", 0)]
    y = py + 148
    fills = {0: WHITE, 1: (0xFB, 0xF0, 0xD6), 2: (0xFF, 0xFF, 0xFF), 3: (0xF2, 0xF4, 0xF8)}
    for i, (name, st, kind) in enumerate(names):
        hh = 44 if kind != 2 else 52
        d.rectangle((px + 20, y, px + pw - 20, y + hh), fill=fills[kind],
                    outline=(0xE0, 0xC9, 0x8C) if kind == 2 else RULE, width=3 if kind == 2 else 1)
        t(d, (px + 34, y + hh / 2), name, 21, INK, kind == 2, "lm")
        if kind == 0:
            chip(d, px + 330, y + 8, 108, 28, "HADIR", (0x1E, 0x6B, 0x3A), 13)
        elif kind == 1:
            chip(d, px + 330, y + 8, 108, 28, "SAKIT", GOLD, 13)
        elif kind == 3:
            chip(d, px + 330, y + 8, 108, 28, "IZIN", LGREY, 13)
        else:
            chip(d, px + 322, y + 10, 124, 32, "KETUK", TEAL, 14)
        y += hh + 6

    t(d, (px + 20, py + 566), "Urungkan 2 menit tersedia bila salah ketuk", 15, LGREY)

    d.rectangle((68, 800, 1532, 882), fill=(0xF4, 0xF6, 0xFA))
    t(d, (100, 826), "Absensi tampil berdampingan dengan papan  ·  hasilnya langsung dipakai dasbor",
      19, NAVY, True)
    im.save(f"{OUT}/tv_absen.png")


# --------------------------------------------------------------- 4 · admin
def admin():
    im, d = canvas()
    shadow(im, (150, 80, 1450, 900))
    d = ImageDraw.Draw(im)
    rr(d, (146, 76, 1454, 896), 16, fill=DARK)
    rr(d, (168, 98, 1432, 874), 6, fill=WHITE)

    d.rectangle((168, 98, 1432, 168), fill=NAVY)
    t(d, (196, 122), "HALAMAN ADMIN  ·  ADMIN PLANT SNACK", 26, WHITE, True)
    t(d, (1404, 126), "audit: siapa, kapan", 19, (0xC9, 0xD3, 0xE6), anchor="ra")

    tabs = ["Pengguna", "Target plant", "Layar TV", "Kunci periode", "Audit"]
    x = 196
    for i, name in enumerate(tabs):
        col = NAVY if i == 1 else GREY
        t(d, (x, 190), name, 21, col, i == 1)
        if i == 1:
            d.rectangle((x, 220, x + 148, 224), fill=GOLD)
        x += 196

    # kartu pengaturan
    rr(d, (196, 250, 760, 560), 10, fill=SOFT, line=RULE, w=2)
    t(d, (218, 266), "Target & bobot KPI · versi", 20, NAVY, True)
    t(d, (218, 300), "versi 2 · berlaku Nov 2026 – Jan 2027", 17, GREY)
    rows = [("SHE · zero accident", "bobot 30%", "V/O", NAVY),
            ("QC · defect per line", "bobot 30%", "V/O", TEAL),
            ("Prod · OEE", "bobot 25%", "V/O", TEAL),
            ("Delivery · plan vs real", "bobot 15%", "V/O", GOLD)]
    y = 344
    for a, b, c_, col in rows:
        d.rectangle((218, y, 740, y + 50), fill=WHITE)
        t(d, (232, y + 14), a, 18, INK)
        t(d, (560, y + 14), b, 18, GREY)
        chip(d, 664, y + 12, 62, 26, c_, col, 14)
        y += 54

    # kartu layar TV
    rr(d, (784, 250, 1404, 560), 10, fill=WHITE, line=RULE, w=2)
    t(d, (806, 266), "Layar TV yang aktif", 20, NAVY, True)
    tv_rows = [("TV Lantai 1 · Snack", "aktif", TEAL),
               ("TV Lantai 2 · Snack", "aktif", TEAL),
               ("TV Dairy · menunggu", "belum", LGREY)]
    y = 310
    for a, b, col in tv_rows:
        d.rectangle((806, y, 1382, y + 62), fill=(0xFA, 0xFB, 0xFD))
        t(d, (822, y + 18), a, 19, INK)
        chip(d, 1252, y + 16, 118, 30, b.upper(), col, 14)
        y += 70

    # baris bawah: kunci periode + audit
    rr(d, (196, 584, 760, 850), 10, fill=(0xFD, 0xF6, 0xE8), line=(0xE0, 0xC9, 0x8C), w=2)
    t(d, (218, 600), "KUNCI PERIODE", 17, GOLD, True)
    t(d, (218, 632), "Oktober 2026 sudah dilaporkan", 22, INK, True)
    t(d, (218, 672), "Periode terkunci tidak dapat diubah;", 18, GREY)
    t(d, (218, 698), "koreksi dicatat sebagai versi baru.", 18, GREY)
    rr(d, (218, 744, 470, 796), 10, fill=NAVY)
    t(d, (344, 770), "Buka kunci (admin)", 18, WHITE, True, "mm")

    rr(d, (784, 584, 1404, 850), 10, fill=SOFT, line=RULE, w=2)
    t(d, (806, 600), "JEJAK AUDIT", 17, LGREY, True)
    log = [("07.04  Dhani", "menutup DT-0912 · bukti 1 berkas"),
           ("07.06  Sigit", "mengubah target QC line 4"),
           ("07.09  Admin", "mengunci periode Oktober")]
    y = 636
    for a, b in log:
        t(d, (806, y), a, 18, NAVY, True)
        t(d, (1010, y), b, 18, GREY)
        y += 44

    im.save(f"{OUT}/admin.png")


def trim(name):
    """Pangkas margin putih di sekitar mockup agar memenuhi kartu slide."""
    p = f"{OUT}/{name}.png"
    im = Image.open(p).convert("RGB")
    from PIL import ImageChops
    diff = ImageChops.difference(im, Image.new("RGB", im.size, WHITE))
    bb = diff.getbbox()
    if bb:
        pad = 10
        bb = (max(bb[0] - pad, 0), max(bb[1] - pad, 0),
              min(bb[2] + pad, im.width), min(bb[3] + pad, im.height))
        im.crop(bb).save(p)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    form()
    dasbor()
    tv()
    tv_absen()
    admin()
    for name in ("form", "dasbor", "tv", "tv_absen", "admin"):
        trim(name)
        p = f"{OUT}/{name}.png"
        print(p, Image.open(p).size, f"{os.path.getsize(p) / 1024:.0f} KB")
