#!/usr/bin/env python3
"""
Ilustrasi layar aplikasi DMS (rancangan, bukan tangkapan aplikasi asli).
Semua digambar 1600x1000 dengan satu sistem desain: warna template
(navy/teal/gold/merah), app bar, sidebar, kartu, tabel, pill status.

  docs/assets/mockup/form.png      isi papan per divisi (tablet)
  docs/assets/mockup/tv.png        TV berbentuk papan
  docs/assets/mockup/tv_absen.png  papan + panel absensi
  docs/assets/mockup/dasbor.png    dasbor L1-L3 (laptop)
  docs/assets/mockup/admin.png     halaman admin
  docs/assets/mockup/kasus.png     detail kasus + PICA
  docs/assets/mockup/laporan.png   laporan & skor KPI

Jalankan: python3 docs/scripts/make_mockups.py
"""
import os

from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1600, 1000
OUT = "docs/assets/mockup"

NAVY = (0x1B, 0x2C, 0x57)
NAVY_D = (0x14, 0x20, 0x40)
NAVY_L = (0x2C, 0x45, 0x7C)
TEAL = (0x2E, 0x86, 0x8C)
TEAL_D = (0x1E, 0x6B, 0x3A)
GOLD = (0xC8, 0xA5, 0x2B)
GOLD_D = (0x8A, 0x6C, 0x10)
RED = (0xB0, 0x2F, 0x2F)
INK = (0x1E, 0x24, 0x30)
GREY = (0x5C, 0x64, 0x72)
LGREY = (0x8B, 0x93, 0xA1)
RULE = (0xDD, 0xE2, 0xEA)
SOFT = (0xF4, 0xF6, 0xFA)
SOFT2 = (0xFA, 0xFB, 0xFD)
DARK = (0x1C, 0x22, 0x2E)
WHITE = (0xFF, 0xFF, 0xFF)
OK = (0x1E, 0x6B, 0x3A)
OK_BG = (0xE3, 0xF1, 0xE7)
WARN_BG = (0xFB, 0xF0, 0xD6)
BAD_BG = (0xF8, 0xE0, 0xE0)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def f(size, bold=False):
    return ImageFont.truetype(FB if bold else FR, size)


def canvas():
    im = Image.new("RGB", (W, H), (0xEC, 0xEF, 0xF5))
    return im, ImageDraw.Draw(im)


def rr(d, box, r, fill=None, line=None, w=2):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=line, width=w)


def t(d, xy, s, size=22, color=INK, bold=False, anchor="la"):
    d.text(xy, s, font=f(size, bold), fill=color, anchor=anchor)


def tw(d, s, size, bold=False):
    return d.textlength(s, font=f(size, bold))


def wrap(d, xy, text, width, size=12, color=GREY, bold=False, lh=None):
    """Tulis teks dengan pembungkus sederhana sesuai lebar piksel."""
    x, y = xy
    lh = lh or size * 1.45
    line = ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if tw(d, trial, size, bold) > width and line:
            t(d, (x, y), line, size, color, bold)
            y += lh
            line = word
        else:
            line = trial
    if line:
        t(d, (x, y), line, size, color, bold)
        y += lh
    return y


def soft_shadow(im, box, blur=24, alpha=40, r=18):
    lay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(lay)
    dd.rounded_rectangle(box, radius=r, fill=(15, 25, 45, alpha))
    lay = lay.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(im.convert("RGBA"), lay).convert("RGB")


def pill(d, x, y, text, color, size=14, h=28, solid=True, align="l"):
    w = 26 + tw(d, text, size, True)
    if align == "r":
        x -= w
    elif align == "c":
        x -= w / 2
    if solid:
        rr(d, (x, y, x + w, y + h), h / 2, fill=color)
        t(d, (x + w / 2, y + h / 2 - 1), text, size, WHITE, True, "mm")
    else:
        rr(d, (x, y, x + w, y + h), h / 2, fill=WHITE, line=color, w=2)
        t(d, (x + w / 2, y + h / 2 - 1), text, size, color, True, "mm")
    return w


def btn(d, box, text, color, size=19, ghost=False, radius=10):
    x0, y0, x1, y1 = box
    if ghost:
        rr(d, box, radius, fill=WHITE, line=color, w=2)
        t(d, ((x0 + x1) / 2, (y0 + y1) / 2), text, size, color, True, "mm")
    else:
        rr(d, box, radius, fill=color)
        t(d, ((x0 + x1) / 2, (y0 + y1) / 2), text, size, WHITE, True, "mm")


def avatar(d, cx, cy, initials, color=NAVY, r=22, size=17):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=color)
    t(d, (cx, cy - 1), initials, size, WHITE, True, "mm")


def icon(d, x, y, s, kind, color):
    """Ikon garis sederhana 24x24 yang diperbesar sesuai skala."""
    u = s / 24
    if kind == "grid":
        for i in range(2):
            for j in range(2):
                rr(d, (x + i * 13 * u, y + j * 13 * u, x + (i * 13 + 10) * u, y + (j * 13 + 10) * u),
                   2 * u, fill=None, line=color, w=int(max(2, 2.2 * u)))
    elif kind == "chart":
        d.line((x, y + 22 * u, x + 22 * u, y + 22 * u), fill=color, width=int(max(2, 2 * u)))
        for i, hh in enumerate((8, 15, 11)):
            d.rectangle((x + (2 + i * 7) * u, y + (22 - hh) * u, x + (7 + i * 7) * u, y + 21 * u), fill=color)
    elif kind == "doc":
        rr(d, (x + 2 * u, y + 1 * u, x + 20 * u, y + 23 * u), 2 * u, fill=None, line=color,
           w=int(max(2, 2 * u)))
        for i in range(3):
            d.line((x + 6 * u, y + (7 + i * 5) * u, x + 16 * u, y + (7 + i * 5) * u), fill=color,
                   width=int(max(1, 1.8 * u)))
    elif kind == "gear":
        d.ellipse((x + 5 * u, y + 5 * u, x + 19 * u, y + 19 * u), outline=color, width=int(max(2, 2 * u)))
        d.ellipse((x + 10 * u, y + 10 * u, x + 14 * u, y + 14 * u), fill=color)
        for dx, dy in ((11, 0), (11, 22), (0, 11), (22, 11)):
            d.line((x + 11 * u + (dx - 11) / 2 * u, y + 11 * u + (dy - 11) / 2 * u,
                    x + (dx if dx != 11 else 11) * u, y + (dy if dy != 11 else 11) * u), fill=color, width=2)
    elif kind == "tv":
        rr(d, (x + 1 * u, y + 4 * u, x + 23 * u, y + 18 * u), 2 * u, fill=None, line=color,
           w=int(max(2, 2 * u)))
        d.line((x + 8 * u, y + 22 * u, x + 16 * u, y + 22 * u), fill=color, width=2)
    elif kind == "users":
        d.ellipse((x + 2 * u, y + 4 * u, x + 12 * u, y + 14 * u), outline=color, width=2)
        d.ellipse((x + 12 * u, y + 7 * u, x + 20 * u, y + 15 * u), outline=color, width=2)
        d.arc((x + 1 * u, y + 14 * u, x + 23 * u, y + 28 * u), 200, 340, fill=color, width=2)
    elif kind == "bell":
        d.arc((x + 5 * u, y + 3 * u, x + 19 * u, y + 17 * u), 180, 360, fill=color, width=2)
        d.line((x + 5 * u, y + 10 * u, x + 5 * u, y + 18 * u), fill=color, width=2)
        d.line((x + 19 * u, y + 10 * u, x + 19 * u, y + 18 * u), fill=color, width=2)
        d.line((x + 3 * u, y + 18 * u, x + 21 * u, y + 18 * u), fill=color, width=2)
        d.ellipse((x + 10 * u, y + 20 * u, x + 14 * u, y + 24 * u), fill=color)
    elif kind == "check":
        d.line((x + 4 * u, y + 12 * u, x + 10 * u, y + 19 * u), fill=color, width=int(max(2, 3 * u)))
        d.line((x + 10 * u, y + 19 * u, x + 21 * u, y + 5 * u), fill=color, width=int(max(2, 3 * u)))


def sparkline(d, box, vals, color):
    x0, y0, x1, y1 = box
    mx, mn = max(vals), min(vals)
    rng = (mx - mn) or 1
    pts = [(x0 + (x1 - x0) * i / (len(vals) - 1),
            y1 - (y1 - y0) * (v - mn) / rng) for i, v in enumerate(vals)]
    d.line(pts, fill=color, width=3, joint="curve")
    d.ellipse((pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4), fill=color)


# ------------------------------------------------------------------ kerangka
def device_tablet(im, box=(60, 60, 1540, 940)):
    im = soft_shadow(im, box, 26, 45)
    d = ImageDraw.Draw(im)
    rr(d, box, 30, fill=DARK)
    d.ellipse((795, 72, 805, 82), fill=(0x3A, 0x42, 0x52))
    inner = (box[0] + 22, box[1] + 44, box[2] - 22, box[3] - 24)
    rr(d, inner, 6, fill=WHITE)
    return im, inner


def device_laptop(im, box=(150, 60, 1450, 830)):
    im = soft_shadow(im, box, 26, 45)
    d = ImageDraw.Draw(im)
    rr(d, box, 16, fill=DARK)
    inner = (box[0] + 18, box[1] + 18, box[2] - 18, box[3] - 18)
    rr(d, inner, 5, fill=WHITE)
    rr(d, (90, 838, 1510, 906), 12, fill=(0xD9, 0xDF, 0xE9), line=(0xBB, 0xC3, 0xD2), w=2)
    rr(d, (682, 840, 918, 852), 6, fill=(0xC0, 0xC8, 0xD7))
    return im, inner


def appbar(d, inner, title, right_chips=(), h=64, sub=None, initials="DN"):
    x0, y0, x1, _ = inner
    d.rectangle((x0, y0, x1, y0 + h), fill=NAVY)
    # logogram
    rr(d, (x0 + 20, y0 + 16, x0 + 52, y0 + 48), 8, fill=GOLD)
    rr(d, (x0 + 26, y0 + 22, x0 + 46, y0 + 42), 4, fill=NAVY)
    t(d, (x0 + 64, y0 + 14), "DMS", 21, WHITE, True)
    t(d, (x0 + 64, y0 + 38), "Daily Monitoring", 12, (0xA9, 0xB8, 0xD4))
    d.line((x0 + 176, y0 + 18, x0 + 176, y0 + 46), fill=(0x3C, 0x52, 0x84), width=2)
    t(d, (x0 + 194, y0 + 13), title, 22, WHITE, True)
    if sub:
        t(d, (x0 + 194, y0 + 40), sub, 14, (0xB6, 0xC3, 0xDA))
    cx = x1 - 24
    avatar(d, cx - 18, y0 + h / 2, initials, TEAL, 20, 15)
    cx -= 56
    icon(d, cx - 22, y0 + h / 2 - 12, 24, "bell", (0xC9, 0xD3, 0xE6))
    cx -= 44
    for text, col in reversed(list(right_chips)):
        w = 26 + tw(d, text, 14, True)
        pill(d, cx - w, y0 + 18, text, col, 14, 28, solid=False, align="l")
        cx -= w + 10
    return y0 + h


def sidebar(d, inner, y0, items, active, foot="SNACK · LINE 9", w=246):
    x0, y, _, y1 = inner
    d.rectangle((x0, y0, x0 + w, y1), fill=NAVY)
    yy = y0 + 22
    for name, ic, badge in items:
        on = name == active
        if on:
            rr(d, (x0 + 14, yy - 6, x0 + w - 14, yy + 34), 8, fill=NAVY_L)
            d.rectangle((x0 + 14, yy - 6, x0 + 18, yy + 34), fill=GOLD)
        icon(d, x0 + 30, yy + 4, 22, ic, WHITE if on else (0x9F, 0xB0, 0xCE))
        t(d, (x0 + 62, yy + 3), name, 16, WHITE if on else (0xB6, 0xC3, 0xDA), on)
        if badge:
            pill(d, x0 + w - 18, yy + 3, badge, RED, 12, 24, True, "r")
        yy += 50
    d.line((x0 + 18, y1 - 74, x0 + w - 18, y1 - 74), fill=(0x33, 0x48, 0x74), width=2)
    t(d, (x0 + 22, y1 - 62), foot, 14, GOLD, True)
    t(d, (x0 + 22, y1 - 40), "Sen, 3 Nov 2026", 13, (0x9F, 0xB0, 0xCE))
    return x0 + w


def card(d, box, title=None, sub=None, right=None, fill=WHITE):
    rr(d, box, 12, fill=fill, line=RULE, w=2)
    if title:
        t(d, (box[0] + 20, box[1] + 16), title, 18, NAVY, True)
    if sub:
        t(d, (box[0] + 20, box[1] + 42), sub, 14, GREY)
    if right:
        t(d, (box[2] - 20, box[1] + 18), right, 14, LGREY, True, "ra")


def table_head(d, x0, x1, y, cols, h=38):
    d.rectangle((x0, y, x1, y + h), fill=SOFT)
    for cx, name, al in cols:
        t(d, (cx, y + h / 2), name, 13, LGREY, True, "lm" if al == "l" else ("rm" if al == "r" else "mm"))
    return y + h


# ------------------------------------------------------------------ 1 · isi papan
def form():
    im, _ = canvas()
    im, inner = device_tablet(im)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = inner
    y = appbar(d, inner, "Isi papan · Snack · Line 9", [("Shift 1", TEAL), ("Draf tersimpan 07.08", GOLD)])

    # baris filter
    d.rectangle((x0, y, x1, y + 62), fill=WHITE)
    d.line((x0, y + 62, x1, y + 62), fill=RULE, width=2)
    t(d, (x0 + 24, y + 20), "Snack", 16, GREY)
    t(d, (x0 + 92, y + 20), "›", 16, LGREY)
    t(d, (x0 + 112, y + 20), "Line 9", 16, INK, True)
    t(d, (x0 + 190, y + 20), "›", 16, LGREY)
    t(d, (x0 + 210, y + 20), "3 November 2026", 16, GREY)
    pill(d, x0 + 380, y + 16, "HARI KERJA", TEAL, 12, 26, solid=False)
    pill(d, x1 - 470, y + 16, "DEADLINE 07.30", RED, 12, 26, solid=False)
    t(d, (x1 - 300, y + 20), "Sisa 22 menit", 15, GREY)
    y += 62

    # tab divisi
    tabs = [("SHE", "users", False), ("Quality", "check", False), ("Produksi", "grid", True),
            ("Teknik", "gear", False), ("Delivery", "doc", False)]
    tab_y = y + 16
    tx = x0 + 24
    for name, ic, on in tabs:
        w = 46 + tw(d, name, 17, True)
        if on:
            rr(d, (tx, tab_y, tx + w, tab_y + 44), 8, fill=NAVY)
            icon(d, tx + 14, tab_y + 10, 22, ic, WHITE)
            t(d, (tx + 42, tab_y + 12), name, 17, WHITE, True)
            d.rectangle((tx, tab_y + 44, tx + w, tab_y + 48), fill=GOLD)
        else:
            icon(d, tx + 14, tab_y + 10, 22, ic, LGREY)
            t(d, (tx + 42, tab_y + 12), name, 17, GREY)
        tx += w + 8
    t(d, (x1 - 24, tab_y + 12), "5 item · wajib 4", 15, LGREY, anchor="ra")
    y = tab_y + 62

    # panel kiri: tabel isian
    lx0, lx1 = x0 + 24, x1 - 432
    card(d, (lx0, y, lx1, y1 - 150))
    tbl_bottom = y + 14 + 36 + 58 * 5 + 10
    cols = [(lx0 + 18, "ITEM", "l"), (lx0 + 360, "TARGET", "l"), (lx0 + 470, "HASIL", "l"),
            (lx0 + 590, "STATUS", "l"), (lx0 + 760, "SEBAB / BUKTI", "l")]
    ty = table_head(d, lx0, lx1, y + 14, cols, 36)
    rows = [("Checklist A · critical point", "100%", "100%", "SESUAI", "", OK, OK_BG),
            ("Checklist B · suhu ruang", "≤ 18 °C", "16 °C", "SESUAI", "", OK, OK_BG),
            ("Output shift", "8.400 pcs", "8.120 pcs", "DI BAWAH", "tunggu material", GOLD_D, WARN_BG),
            ("Downtime · WS L02", "≤ 20 mnt", "48 mnt", "LEWAT BATAS", "belt aus", RED, BAD_BG),
            ("OEE line", "≥ 85%", "78%", "DI BAWAH", "ikut downtime", GOLD_D, WARN_BG)]
    ry = ty
    for i, (item, tg, hs, st, sb, col, bg) in enumerate(rows):
        hh = 58
        d.rectangle((lx0 + 1, ry, lx1 - 1, ry + hh), fill=SOFT2 if i % 2 else WHITE)
        d.line((lx0 + 14, ry + hh, lx1 - 14, ry + hh), fill=RULE, width=1)
        t(d, (lx0 + 18, ry + 18), item, 17, INK)
        t(d, (lx0 + 360, ry + 18), tg, 16, GREY)
        t(d, (lx0 + 470, ry + 18), hs, 16, INK, True)
        rr(d, (lx0 + 580, ry + 16, lx0 + 580 + tw(d, st, 11, True) + 22, ry + 42), 13, fill=bg)
        t(d, (lx0 + 591, ry + 20), st, 11, col, True)
        t(d, (lx0 + 760, ry + 18), sb if sb else "—", 14, GREY)
        ry += hh

    # catatan shift di dalam kartu tabel
    t(d, (lx0 + 18, tbl_bottom + 18), "CATATAN SHIFT (OPSIONAL)", 12, LGREY, True)
    rr(d, (lx0 + 18, tbl_bottom + 40, lx1 - 18, tbl_bottom + 96), 8, fill=SOFT2, line=RULE, w=2)
    t(d, (lx0 + 32, tbl_bottom + 52), "Material dari gudang datang 06.40, output tertahan 25 menit.",
      14, GREY)
    t(d, (lx1 - 32, tbl_bottom + 60), "0/240", 11, LGREY, anchor="ra")

    # drawer sebab
    dy = y1 - 138
    rr(d, (lx0, dy, lx1, y1 - 24), 10, fill=(0xFD, 0xF3, 0xF3), line=(0xD9, 0x9C, 0x9C), w=2)
    d.rectangle((lx0, dy + 20, lx0 + 5, y1 - 44), fill=RED)
    t(d, (lx0 + 22, dy + 14), "SEBAB & TINDAKAN · WAJIB KARENA STATUS DI BAWAH TARGET", 13, RED, True)
    t(d, (lx0 + 22, dy + 38), "Belt WS L02 aus, diganti sementara", 20, INK)
    t(d, (lx0 + 22, dy + 70), "Tindakan: ganti belt, cek line 9 sebelum shift 2 · PIC Dhani · tenggat 3 Nov 16.00",
      14, GREY)
    t(d, (lx0 + 22, dy + 94), "Terkirim ke Teknik · WO EP-TK-0031", 14, TEAL, True)

    # panel kanan
    rx0, rx1 = x1 - 408, x1 - 24
    card(d, (rx0, y, rx1, y + 210), "Kelengkapan harian")
    t(d, (rx0 + 20, y + 46), "12/15", 38, NAVY, True)
    t(d, (rx0 + 20, y + 96), "item terisi · sisa 4 menit", 13, GREY)
    d.rectangle((rx0 + 20, y + 124, rx1 - 20, y + 134), fill=SOFT)
    d.rectangle((rx0 + 20, y + 124, rx0 + 20 + (rx1 - rx0 - 40) * 0.8, y + 134), fill=TEAL)
    t(d, (rx0 + 20, y + 144), "Bagian divisi lain", 14, GREY)
    for i, (nm, st, col) in enumerate([("SHE", "sudah", OK), ("Quality", "sudah", OK),
                                       ("Teknik", "belum", LGREY), ("Delivery", "belum", LGREY)]):
        yy = y + 168 + (i // 2) * 24
        xx = rx0 + 20 + (i % 2) * 190
        d.ellipse((xx, yy + 4, xx + 10, yy + 14), fill=col)
        t(d, (xx + 18, yy), nm, 14, INK)

    card(d, (rx0, y + 222, rx1, y + 408), "Absensi shift 1")
    t(d, (rx0 + 20, y + 266), "25", 30, OK, True)
    t(d, (rx0 + 20, y + 302), "hadir dari 28 orang", 13, GREY)
    t(d, (rx0 + 20, y + 322), "2 sakit · 1 izin · 0 alpa", 13, GREY)
    btn(d, (rx0 + 20, y + 344, rx1 - 20, y + 378), "Buka absensi", TEAL, 14, ghost=True, radius=8)
    t(d, (rx0 + 20, y + 386), "bisa dari TV tanpa login", 11, LGREY)

    rr(d, (rx0, y + 420, rx1, y1 - 24), 12, fill=NAVY)
    t(d, (rx0 + 20, y + 438), "Kirim bagian Produksi", 20, WHITE, True)
    t(d, (rx0 + 20, y + 470), "Angka masuk papan, TV, dan dasbor.", 14, (0xC9, 0xD3, 0xE6))
    t(d, (rx0 + 20, y + 492), "Tidak ada salinan kedua.", 14, GOLD, True)
    btn(d, (rx0 + 20, y1 - 96, rx1 - 20, y1 - 48), "KIRIM SEKARANG", GOLD, 17)
    im.save(f"{OUT}/form.png")


# ------------------------------------------------------------------ papan
# Palet papan tulis (whiteboard) — meniru papan DMS fisik B.U.E Factory 10.
WB_BG = (0xFB, 0xFB, 0xF5)      # putih papan
WB_EDGE = (0xB7, 0xB2, 0xA4)    # bingkai aluminium
WB_GRID = (0x90, 0x90, 0x88)    # garis grid tipis
WB_HEAD = (0xF2, 0xF0, 0xE7)    # kepala kolom tabel
MARK_BLUE = (0x1C, 0x3E, 0x8A)  # spidol biru
MARK_RED = (0xC2, 0x2A, 0x26)   # spidol merah
MARK_DARK = (0x2B, 0x2B, 0x28)  # spidol hitam
FKB = "docs/assets/fonts/Kalam-Bold.ttf"
FKR = "docs/assets/fonts/Kalam-Regular.ttf"


def fk(size, bold=True):
    return ImageFont.truetype(FKB if bold else FKR, max(int(size), 6))


def hw(d, xy, s, size=18, color=MARK_BLUE, bold=True, anchor="mm"):
    d.text(xy, s, font=fk(size, bold), fill=color, anchor=anchor)


# Warna kepala pilar sesuai papan asli (Safety merah, Quality kuning, dst.)
P_SAFETY = (0xB0, 0x2F, 0x2F)
P_QUALITY = (0xD7, 0xB3, 0x2A)
P_PROD = (0xA6, 0x2E, 0x2E)
P_DELIV = (0x2E, 0x7D, 0x46)
P_TECH = (0x2A, 0x5C, 0xA0)


def mark_color(st):
    return {0: MARK_BLUE, 1: MARK_RED, 2: MARK_RED, 3: (0xA9, 0xA9, 0xA2)}[st]


def board_columns():
    """Isi tiap pilar papan: (nama, warna kepala, warna teks, subjudul, baris).
    Tiap baris = (label, [(nilai, status) x3]); status 0=biru 1/2=merah 3=kosong."""
    return [
        ("SAFETY", P_SAFETY, WHITE, "Zero Accident · KAK · Genba", [
            ("zero accident", [("0", 0), ("0", 0), ("0", 0)]),
            ("near miss", [("1", 0), ("0", 0), ("2", 1)]),
            ("temuan KAK", [("3", 1), ("1", 0), ("2", 1)]),
            ("tindakan buka", [("2", 1), ("2", 1), ("1", 0)]),
            ("APD / housekeeping", [("ok", 0), ("ok", 0), ("ok", 0)]),
        ]),
        ("QUALITY", P_QUALITY, MARK_DARK, "Quality & Internal Defect", [
            ("defect visual %", [("0,9", 1), ("0,5", 0), ("0,6", 0)]),
            ("critical point", [("1", 0), ("0", 0), ("0", 0)]),
            ("kontaminasi", [("0", 0), ("0", 0), ("1", 2)]),
            ("hold / release", [("2", 1), ("1", 0), ("0", 0)]),
            ("kalibrasi alat", [("ok", 0), ("ok", 0), ("ok", 0)]),
        ]),
        ("PRODUCTIVITY", P_PROD, WHITE, "Operation · Yield · OEE", [
            ("yield RM %", [("96,2", 0), ("95,8", 0), ("96,5", 0)]),
            ("yield PM %", [("97,1", 0), ("96,8", 0), ("97,3", 0)]),
            ("OEE %", [("78", 1), ("81", 0), ("84", 0)]),
            ("output shift", [("8.120", 2), ("8.360", 0), ("8.400", 0)]),
            ("downtime (mnt)", [("48", 2), ("22", 0), ("15", 0)]),
        ]),
        ("DELIVERY", P_DELIV, WHITE, "Plan vs Real PO", [
            ("PO (unit)", [("6/6", 0), ("5/6", 1), ("6/6", 0)]),
            ("keterlambatan", [("1", 1), ("0", 0), ("0", 0)]),
            ("kesiapan muat", [("ok", 0), ("ok", 0), ("ok", 0)]),
            ("retur kirim", [("0", 0), ("0", 0), ("0", 0)]),
            ("ach order %", [("98", 0), ("92", 1), ("100", 0)]),
        ]),
        ("TECHNIC PERFORM", P_TECH, WHITE, "Maintenance · Energy", [
            ("MTC accuracy %", [("99", 0), ("100", 0), ("100", 0)]),
            ("% failure OEE", [("2,1", 1), ("1,8", 0), ("1,5", 0)]),
            ("energy gas", [("360", 0), ("355", 0), ("358", 0)]),
            ("energy listrik", [("628", 0), ("641", 1), ("635", 0)]),
            ("work order open", [("2", 1), ("2", 1), ("1", 0)]),
        ]),
    ]


def realistic_board(d, x, y, w, h, scale=1.0, ncols=5):
    """Papan DMS gaya whiteboard: bingkai, kepala pilar berwarna, grid shift,
    angka tulisan tangan biru/merah, seperti papan fisik di lantai produksi."""
    s = scale
    d.rectangle((x - 6 * s, y - 6 * s, x + w + 6 * s, y + h + 6 * s), fill=WB_EDGE)
    d.rectangle((x, y, x + w, y + h), fill=WB_BG)
    cols = board_columns()[:ncols]
    gap, pad = 8 * s, 8 * s
    cw = (w - 2 * pad - gap * (ncols - 1)) / ncols
    head_h, sub_h = 34 * s, 24 * s
    shifts = ("S1", "S2", "S3")
    cell_w = 50 * s
    for i, (name, hcol, htxt, sub, rows) in enumerate(cols):
        cx = x + pad + i * (cw + gap)
        top = y + pad
        d.rectangle((cx, top, cx + cw, top + head_h), fill=hcol)
        t(d, (cx + cw / 2, top + head_h / 2), name, int(15 * s), htxt, True, "mm")
        sy = top + head_h
        t(d, (cx + cw / 2, sy + sub_h / 2), sub, int(11 * s), GREY, False, "mm")
        gy = sy + sub_h
        item_w = cw - 3 * cell_w
        hrh = 24 * s
        d.rectangle((cx, gy, cx + cw, gy + hrh), fill=WB_HEAD)
        t(d, (cx + 6 * s, gy + hrh / 2), "ITEM", int(10 * s), GREY, True, "lm")
        for k, sh in enumerate(shifts):
            cxx = cx + item_w + k * cell_w
            t(d, (cxx + cell_w / 2, gy + hrh / 2), sh, int(11 * s), GREY, True, "mm")
        gh = (y + h - pad) - gy
        rh = (gh - hrh) / len(rows)
        # garis grid
        for k in range(1, 4):
            vx = cx + item_w + (k - 1) * cell_w
            d.line((vx, gy, vx, y + h - pad), fill=WB_GRID, width=1)
        d.rectangle((cx, gy, cx + cw, y + h - pad), outline=WB_GRID, width=1)
        ry = gy + hrh
        for j, (label, vals) in enumerate(rows):
            if j:
                d.line((cx, ry, cx + cw, ry), fill=WB_GRID, width=1)
            hw(d, (cx + 7 * s, ry + rh / 2), label, int(14 * s), MARK_DARK, False, "lm")
            for k, (val, st) in enumerate(vals):
                cxx = cx + item_w + k * cell_w
                col = mark_color(st)
                hw(d, (cxx + cell_w / 2, ry + rh / 2), val, int(18 * s), col, True, "mm")
                if st == 2 and len(val) <= 3:  # lingkaran spidol merah utk 'lewat batas'
                    d.ellipse((cxx + 5 * s, ry + rh / 2 - 13 * s,
                               cxx + cell_w - 5 * s, ry + rh / 2 + 13 * s),
                              outline=MARK_RED, width=2)
            ry += rh


def pica_strip(d, x, y, w, h, scale=1.0):
    """Baris PICA di kaki papan, seperti papan asli (Problem·Action·PIC·Due·Status)."""
    s = scale
    d.rectangle((x, y, x + w, y + h), fill=WB_BG, outline=WB_GRID, width=1)
    hh = 26 * s
    d.rectangle((x, y, x + w, y + hh), fill=(0x8A, 0x2A, 0x2A))
    t(d, (x + 10 * s, y + hh / 2), "PICA", int(13 * s), WHITE, True, "lm")
    t(d, (x + 70 * s, y + hh / 2), "Problem & Rootcause", int(11 * s), (0xF0, 0xD8, 0xD8), True, "lm")
    rows = [
        ("Belt WS L02 aus", "ganti belt + cek line 9", "Dhani", "3 Nov", "OPEN"),
        ("Defect visual naik", "cek nozzle seasoning", "Sigit", "4 Nov", "OPEN"),
    ]
    widths = [0.30, 0.34, 0.12, 0.10, 0.14]
    heads = ["", "", "PIC", "Due", "Status"]
    xx = x
    for k, frac in enumerate(widths):
        if heads[k]:
            t(d, (xx + 8 * s, y + hh / 2), heads[k], int(11 * s), (0xF0, 0xD8, 0xD8), True, "lm")
        xx += w * frac
    ry, rh = y + hh, (h - hh) / len(rows)
    for j, row in enumerate(rows):
        yy = ry + j * rh
        if j:
            d.line((x, yy, x + w, yy), fill=WB_GRID, width=1)
        xx = x
        for k, (val, frac) in enumerate(zip(row, widths)):
            col = MARK_RED if k == 4 else (MARK_BLUE if k in (2, 3) else MARK_DARK)
            hw(d, (xx + 8 * s, yy + rh / 2), val, int(14 * s), col, k == 4, "lm")
            xx += w * frac


def board_legend(d, x, y, size=13):
    """Legenda spidol: biru sesuai, merah di bawah/lewat, abu belum diisi."""
    for name, col in [("sesuai target", MARK_BLUE), ("di bawah / lewat batas", MARK_RED),
                      ("belum diisi", (0xA9, 0xA9, 0xA2))]:
        d.rectangle((x, y - 8, x + 18, y + 8), fill=col)
        t(d, (x + 26, y), name, size, GREY, True, "lm")
        x += 26 + tw(d, name, size, True) + 26
    return x


# ------------------------------------------------------------------ TV per divisi (R-80)
import datetime as _dt

_HARI = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]
_TGL = _dt.date(2026, 11, 6)
TGL_ID = f"{_HARI[_TGL.weekday()]}, {_TGL.day} Nov {_TGL.year}"


def fit(d, s, size, maxw, bold=False, hand=False):
    """Potong teks agar tidak melewati lebar kolom."""
    fo = fk(size, bold) if hand else f(size, bold)
    if d.textlength(s, font=fo) <= maxw:
        return s
    out = s
    while out and d.textlength(out + "…", font=fo) > maxw:
        out = out[:-1]
    return (out + "…") if out else "…"


def tv_head(d, box, divname=None, divcol=None, divtxt=WHITE, sub=None):
    x0, y0, x1, y1 = box
    d.rectangle((x0, y0, x1, y0 + 72), fill=(0xF7, 0xF5, 0xEE))
    d.line((x0, y0 + 72, x1, y0 + 72), fill=WB_EDGE, width=2)
    t(d, (x0 + 22, y0 + 12), "DMS · SNACK · LINE 9", 24, NAVY, True)
    bx = x0 + 22 + tw(d, "DMS · SNACK · LINE 9", 24, True) + 26
    if divname:
        bw = tw(d, divname, 22, True) + 40
        rr(d, (bx, y0 + 10, bx + bw, y0 + 48), 8, fill=divcol)
        t(d, (bx + bw / 2, y0 + 29), divname, 22, divtxt, True, "mm")
        t(d, (bx + bw + 16, y0 + 29), sub or "SATU DIVISI PER LAYAR", 12, LGREY, True, "lm")
    board_legend(d, x0 + 22, y0 + 60, 12)
    t(d, (x1 - 22, y0 + 12), TGL_ID + " · Minggu 45", 17, NAVY, True, "ra")
    t(d, (x1 - 22, y0 + 42), "Shift 1 · PKI 08.30 · Leader: Dhani", 14, MARK_RED, True, "ra")


def tv_foot(d, box, page, total=7, src="EXCEL", sync="07.12", upd="07.14", extra="Hadir 25/28"):
    x0, y0, x1, y1 = box
    fy = y1 - 58
    d.rectangle((x0, fy, x1, y1), fill=SOFT)
    d.line((x0, fy, x1, fy), fill=RULE, width=2)
    d.ellipse((x0 + 22, fy + 23, x0 + 34, fy + 35), fill=TEAL)
    t(d, (x0 + 44, fy + 18), f"Sinkron Excel {sync}", 15, NAVY, True)
    x = x0 + 44 + tw(d, f"Sinkron Excel {sync}", 15, True) + 14
    x += pill(d, x, fy + 15, "SUMBER: " + src, TEAL, 12, 26, False)
    t(d, (x + 16, fy + 18), f"·  Pembaruan {upd}  ·  {extra}", 15, INK)
    lbl = f"Halaman {page}/{total}"
    t(d, (x1 - 22, fy + 18), lbl, 15, NAVY, True, "ra")
    dx = x1 - 30 - tw(d, lbl, 15, True) - total * 16
    for i in range(total):
        col = NAVY if i == page - 1 else (0xC7, 0xCE, 0xDA)
        d.ellipse((dx + i * 16, fy + 24, dx + i * 16 + 9, fy + 33), fill=col)
    return fy


def kpi_grid(d, x, y, w, rows, color):
    """Grid KPI: ITEM | Target | S1 | S2 | S3 | Harian | Minggu | Bulan."""
    heads = ["Target", "S1", "S2", "S3", "Harian", "Minggu", "Bulan"]
    cw, hh = 96, 28
    rh = 34 if len(rows) <= 3 else 30
    h = hh + rh * len(rows)
    d.rectangle((x - 5, y - 5, x + w + 5, y + h + 5), fill=WB_EDGE)
    d.rectangle((x, y, x + w, y + h), fill=WB_BG)
    d.rectangle((x, y, x + w, y + hh), fill=color)
    t(d, (x + 10, y + hh / 2), "KPI HARIAN  ·  target vs realisasi", 13, WHITE, True, "lm")
    iw = w - cw * len(heads)
    for k, hd in enumerate(heads):
        t(d, (x + iw + cw * k + cw / 2, y + hh / 2), hd, 13, WHITE, True, "mm")
    ry = y + hh
    for j, (label, tgt, vals) in enumerate(rows):
        if j:
            d.line((x, ry, x + w, ry), fill=WB_GRID, width=1)
        hw(d, (x + 10, ry + rh / 2), label, 16, MARK_DARK, False, "lm")
        t(d, (x + iw + cw / 2, ry + rh / 2), tgt, 14, GREY, True, "mm")
        for k, (val, st) in enumerate(vals):
            cx = x + iw + cw * (k + 1)
            if k == 2:
                d.rectangle((cx, ry + 1, cx + cw, ry + rh - 1), fill=(0xF2, 0xF0, 0xE7))
            col = mark_color(st)
            hw(d, (cx + cw / 2, ry + rh / 2), val, 20, col, True, "mm")
            if st == 2 and len(val) <= 3:
                d.ellipse((cx + 22, ry + rh / 2 - 13, cx + cw - 22, ry + rh / 2 + 13),
                          outline=MARK_RED, width=2)
        ry += rh
    for k in range(len(heads) + 1):
        vx = x + iw + cw * k
        d.line((vx, y + hh, vx, y + h), fill=WB_GRID, width=1)
    d.rectangle((x, y, x + w, y + h), outline=WB_GRID, width=1)
    return y + h


ST_COL = {"OPEN": MARK_RED, "PROGRESS": (0x8A, 0x6C, 0x10), "CLOSE": MARK_BLUE}


def case_table(d, x, y, w, h, sheet, cols, rows, note):
    d.rectangle((x, y, x + w, y + h), fill=WB_BG, outline=WB_GRID, width=1)
    tb = 30
    d.rectangle((x, y, x + w, y + tb), fill=(0x3A, 0x3F, 0x4A))
    t(d, (x + 10, y + tb / 2), f"KASUS · sheet {sheet}", 14, WHITE, True, "lm")
    t(d, (x + w - 10, y + tb / 2), note, 12, (0xC9, 0xCF, 0xDA), True, "rm")
    tot = sum(c[1] for c in cols)
    widths = [w * c[1] / tot for c in cols]
    hy, hh = y + tb, 26
    d.rectangle((x, hy, x + w, hy + hh), fill=WB_HEAD)
    xx = x
    for (hd, _), cw in zip(cols, widths):
        t(d, (xx + 7, hy + hh / 2), fit(d, hd, 11, cw - 12, True), 11, GREY, True, "lm")
        xx += cw
    ry, rh = hy + hh, (h - tb - hh) / len(rows)
    for j, row in enumerate(rows):
        if j:
            d.line((x, ry, x + w, ry), fill=WB_GRID, width=1)
        if j % 2:
            d.rectangle((x + 1, ry + 1, x + w - 1, ry + rh - 1), fill=(0xF7, 0xF7, 0xF0))
        xx = x
        for k, (val, cw) in enumerate(zip(row, widths)):
            hd = cols[k][0]
            if val == "@foto":
                for q in range(2):
                    d.rectangle((xx + 8 + q * 20, ry + rh / 2 - 8, xx + 22 + q * 20, ry + rh / 2 + 8),
                                outline=MARK_BLUE, width=2)
                t(d, (xx + 52, ry + rh / 2), "1·1", 11, GREY, True, "lm")
            elif hd in ("Status",):
                col = ST_COL.get(val, MARK_DARK)
                hw(d, (xx + 7, ry + rh / 2), val, 15, col, True, "lm")
            else:
                col = MARK_RED if hd in ("Prioritas", "Priority", "Umur", "DT (min)") and val not in ("—", "Rendah", "0") else MARK_DARK
                if hd in ("PIC", "Due", "Tanggal", "Tgl", "Date", "Shift", "LBN"):
                    col = MARK_BLUE
                hw(d, (xx + 7, ry + rh / 2), fit(d, val, 15, cw - 12, False, True), 15, col, False, "lm")
            xx += cw
        ry += rh
    xx = x
    for cw in widths[:-1]:
        xx += cw
        d.line((xx, hy, xx, y + h), fill=WB_GRID, width=1)
    d.line((x, hy + hh, x + w, hy + hh), fill=WB_GRID, width=1)


DIV = {
    "she": dict(
        out="tv", name="SHE / SAFETY", color=P_SAFETY, txt=WHITE, sheet="Resume SHE", page=2,
        kpi=[("KAK (kecelakaan kerja)", "Zero", [("0", 0)] * 6),
             ("PICA Safety – completion", "0,80", [("0,75", 1), ("—", 3), ("—", 3), ("0,75", 1), ("0,80", 0), ("0,82", 0)]),
             ("KPI SHE INDEX", "—", [("V", 0), ("—", 3), ("—", 3), ("V", 0), ("V", 0), ("V", 0)])],
        cols=[("Tgl", 5), ("Shift", 4), ("LBN", 8), ("Area", 8), ("Kat. Safety", 8),
              ("Problem Statement", 19), ("RootCause", 13), ("Action Plan", 13),
              ("PIC", 6), ("Due", 5), ("Umur", 5), ("Status", 6), ("Foto", 6)],
        rows=[("6 Nov", "1", "WS L09", "Frying", "Unsafe condition", "Pelindung belt frying terbuka",
               "Baut cover lepas, tidak ada cek awal", "Pasang cover + cek per shift", "Dhani", "7 Nov", "1", "OPEN", "@foto"),
              ("6 Nov", "1", "WS L09", "Packing", "Unsafe action", "Operator naik conveyor tanpa APD",
               "Jalur tangga jauh, belum disosialisasi", "Sediakan tangga + briefing", "Rani", "8 Nov", "1", "PROGRESS", "@foto"),
              ("5 Nov", "3", "WS L02", "Gudang RM", "Housekeeping", "Tumpukan karung tutup jalur evakuasi",
               "Area staging belum ditandai", "Tandai area + rapikan", "Sigit", "6 Nov", "2", "OPEN", "@foto"),
              ("5 Nov", "2", "WS L09", "Seasoning", "Near miss", "Terpeleset ceceran minyak",
               "Seal pompa bocor, drip tray penuh", "Ganti seal + jadwal kuras", "Asep", "9 Nov", "2", "PROGRESS", "@foto"),
              ("4 Nov", "1", "WS L09", "Frying", "APD", "Sarung tangan tidak dipakai saat bersih mesin",
               "Stok APD ukuran L habis", "Restock APD + cek mingguan", "Yanti", "5 Nov", "3", "CLOSE", "@foto")],
        note="26 kolom Excel · kolom lain: OPL/WI · PM · AM · CRMO · Training · Occurrence",
        pica=True),
    "quality": dict(
        out="tv_quality", name="QUALITY", color=P_QUALITY, txt=MARK_DARK, sheet="Resume QC", page=3,
        kpi=[("Defect internal (packing)", "≤ 0,8%", [("0,9", 1), ("0,5", 0), ("—", 3), ("0,7", 0), ("0,8", 0), ("0,76", 0)]),
             ("PICA Quality – completion", "0,80", [("0,88", 0), ("—", 3), ("—", 3), ("0,88", 0), ("0,92", 0), ("0,97", 0)]),
             ("KPI PQI INDEX", "—", [("V", 0), ("—", 3), ("—", 3), ("V", 0), ("V", 0), ("V", 0)])],
        cols=[("Tanggal", 5), ("Shift", 4), ("LBN", 8), ("Category", 8), ("Prioritas", 6),
              ("Problem", 18), ("Validasi QCP", 13), ("Root Cause", 12), ("Action Plan", 12),
              ("PIC", 6), ("Due", 5), ("Status", 6), ("Case Category", 7)],
        rows=[("6 Nov", "1", "WS L09", "Visual", "Tinggi", "Seal bocor pada kemasan 20 g",
               "QCP suhu seal: di luar batas", "Suhu heater turun 8 °C", "Set ulang + kunci parameter", "Sigit", "7 Nov", "OPEN", "Mesin"),
              ("6 Nov", "1", "WS L09", "Berat", "Sedang", "Berat bersih di bawah label",
               "QCP checkweigher: lolos", "Setting filler drift", "Kalibrasi filler per shift", "Rani", "7 Nov", "PROGRESS", "Metode"),
              ("5 Nov", "3", "WS L02", "Kontaminasi", "Tinggi", "Serpihan logam terdeteksi MD",
               "QCP metal detector: fungsi", "Knife scraper aus", "Ganti scraper + cek harian", "Asep", "6 Nov", "OPEN", "Material"),
              ("5 Nov", "2", "WS L09", "Kode produksi", "Sedang", "Kode kedaluwarsa kurang jelas",
               "QCP coding: cek 30 mnt", "Ribbon printer habis", "Stok ribbon + alarm", "Yanti", "8 Nov", "PROGRESS", "Mesin"),
              ("4 Nov", "1", "WS L09", "Visual", "Rendah", "Warna bumbu tidak seragam",
               "QCP warna: sesuai standar", "Nozzle seasoning tersumbat", "Bersihkan nozzle per shift", "Budi", "5 Nov", "CLOSE", "Metode")],
        note="21 kolom Excel · kolom lain: Progress · OPL/WI · PM · V/AM · CRMO",
        pica=True),
    "produksi": dict(
        out="tv_produksi", name="PRODUKSI / PRODUCTIVITY", color=P_PROD, txt=WHITE, sheet="Resume Prod", page=4,
        kpi=[("Yield RM E2E %", "96,0", [("96,2", 0), ("95,8", 1), ("—", 3), ("96,0", 0), ("96,4", 0), ("96,1", 0)]),
             ("Yield PM %", "97,0", [("97,1", 0), ("96,8", 1), ("—", 3), ("97,0", 0), ("97,2", 0), ("97,0", 0)]),
             ("OFR0 (AVG ≤ 10%)", "98–110%", [("101", 0), ("104", 0), ("—", 3), ("102", 0), ("103", 0), ("101", 0)]),
             ("OEE %", "85", [("78", 2), ("81", 1), ("—", 3), ("80", 1), ("82", 1), ("84", 1)]),
             ("Man Power Standart", "1,00", [("1,00", 0), ("1,08", 1), ("—", 3), ("1,04", 1), ("1,02", 0), ("1,01", 0)]),
             ("PICA Prod – completion", "0,80", [("0,97", 0), ("—", 3), ("—", 3), ("0,97", 0), ("0,96", 0), ("0,97", 0)])],
        cols=[("Date", 5), ("Shift", 4), ("LBN", 8), ("Category", 8), ("Prioritas", 6),
              ("Problem", 17), ("DT (min)", 6), ("RootCause", 12), ("Corrective / Preventive", 13),
              ("PIC", 6), ("Due", 5), ("Status", 6), ("O / R", 5)],
        rows=[("6 Nov", "1", "WS L09", "Downtime", "Tinggi", "Frying stop — belt slip", "48",
               "Belt aus, tension turun", "Ganti belt + set tension", "Dhani", "7 Nov", "OPEN", "R"),
              ("6 Nov", "1", "WS L09", "Output", "Tinggi", "Output 8.120 < target 8.400", "22",
               "Changeover lama + tunggu QC", "SMED + jadwal QC tetap", "Rani", "8 Nov", "PROGRESS", "R"),
              ("5 Nov", "3", "WS L02", "Yield", "Sedang", "Yield RM 95,8 < 96,0", "0",
               "Ceceran di transfer conveyor", "Pasang guide + bersihkan", "Sigit", "6 Nov", "OPEN", "O"),
              ("5 Nov", "2", "WS L09", "Speed", "Sedang", "Speed packer turun 12%", "15",
               "Sensor foto kotor", "Bersihkan + cek per shift", "Asep", "9 Nov", "PROGRESS", "R"),
              ("4 Nov", "1", "WS L09", "Man power", "Rendah", "MP 1,08 > standar 1,00", "0",
               "Operator baru belum multiskill", "Matriks latih + pairing", "Yanti", "5 Nov", "CLOSE", "O")],
        note="22 kolom Excel · kolom lain: Progress · OPL/WI · PM · AM · CRMO",
        pica=True),
}


def tv_divisi(key="she"):
    cfg = DIV[key]
    im, _ = canvas()
    im, inner = device_tablet(im, (44, 44, 1556, 912))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = inner
    tv_head(d, inner, cfg["name"], cfg["color"], cfg["txt"])
    x, w = x0 + 20, x1 - x0 - 40
    fy = tv_foot(d, inner, cfg["page"])
    y = y0 + 84
    kpi_end = kpi_grid(d, x, y, w, cfg["kpi"], cfg["color"])
    py, ph = fy - 102, 90
    ty = kpi_end + 16
    case_table(d, x, ty, w, py - 12 - ty, cfg["sheet"], cfg["cols"], cfg["rows"], cfg["note"])
    pica_strip(d, x, py, w, ph, scale=1.0)
    im.save(f"{OUT}/{cfg['out']}.png")


def tv():
    """Halaman TV divisi SHE — halaman 2 dari 7 (R-80, satu divisi per layar)."""
    tv_divisi("she")


def qr_pattern(d, x, y, size, seed=20261106):
    """Gambar QR ilustratif (pola tetap, bukan QR yang bisa dipindai)."""
    import random
    n, q = 25, 2
    m = size / (n + q * 2)
    d.rectangle((x, y, x + size, y + size), fill=WHITE)
    rnd = random.Random(seed)
    ox, oy = x + q * m, y + q * m
    def finder(cx, cy):
        d.rectangle((ox + cx * m, oy + cy * m, ox + (cx + 7) * m, oy + (cy + 7) * m), fill=INK)
        d.rectangle((ox + (cx + 1) * m, oy + (cy + 1) * m, ox + (cx + 6) * m, oy + (cy + 6) * m), fill=WHITE)
        d.rectangle((ox + (cx + 2) * m, oy + (cy + 2) * m, ox + (cx + 5) * m, oy + (cy + 5) * m), fill=INK)
    reserved = lambda r, c: ((r < 8 and c < 8) or (r < 8 and c > n - 9) or (r > n - 9 and c < 8))
    for r in range(n):
        for c in range(n):
            if reserved(r, c):
                continue
            if rnd.random() < 0.46:
                d.rectangle((ox + c * m, oy + r * m, ox + (c + 1) * m - 0.6, oy + (r + 1) * m - 0.6), fill=INK)
    finder(0, 0); finder(n - 7, 0); finder(0, n - 7)


def tv_absen():
    """Halaman 1/7 — absensi dikerjakan paling awal, sebelum DMS (R-81)."""
    im, _ = canvas()
    im, inner = device_tablet(im, (44, 44, 1556, 912))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = inner
    tv_head(d, inner, "LANGKAH 1 · ABSENSI", TEAL, WHITE, "DIKERJAKAN SEBELUM DMS")
    fy = tv_foot(d, inner, 1, extra="Belum dikonfirmasi")
    lx, lw = x0 + 20, 960
    px, pw = x1 - 20 - 448, 448
    ty = y0 + 84
    rr(d, (lx, ty, lx + lw, ty + 100), 12, fill=WHITE, line=RULE, w=2)
    t(d, (lx + 20, ty + 16), "25", 40, OK, True)
    t(d, (lx + 88, ty + 34), "hadir dari 28 orang", 18, GREY, True)
    t(d, (lx + 20, ty + 68), "2 sakit · 1 izin · 0 alpa · 4 nama belum dikonfirmasi", 15, GOLD_D, True)
    d.rectangle((lx + 430, ty + 30, lx + lw - 20, ty + 42), fill=SOFT)
    d.rectangle((lx + 430, ty + 30, lx + 430 + (lw - 450) * 25 / 28, ty + 42), fill=TEAL)
    t(d, (lx + 430, ty + 56), "Ketuk nama untuk menandai tidak hadir — status awal semua hadir", 13, LGREY, True)
    t(d, (lx + lw - 20, ty + 74), "Urungkan 2 menit", 13, TEAL, True, "ra")

    names = ["Dhani", "Rani", "Sigit", "Asep", "Yanti", "Budi", "Wawan",
             "Rina", "Joko", "Sari", "Agus", "Dewi", "Bagas", "Nita",
             "Fajar", "Putri", "Rizal", "Maya", "Hendra", "Lilis", "Yoga",
             "Tari", "Bayu", "Nisa", "Iwan", "Ratna", "Doni", "Wulan"]
    sick = {"Sigit", "Agus"}
    permit = {"Budi"}
    unknown = {"Asep", "Wawan", "Fajar", "Nisa"}
    gy = ty + 116
    cols, gap = 4, 10
    cw = (lw - gap * (cols - 1)) / cols
    rh, vg = 54, 8
    for i, nm in enumerate(names):
        r, c = divmod(i, cols)
        cx, cy = lx + c * (cw + gap), gy + r * (rh + vg)
        if nm in unknown:
            fill_, edge, st, sc = WARN_BG, GOLD, "belum pasti", GOLD_D
        elif nm in sick:
            fill_, edge, st, sc = BAD_BG, RED, "sakit", RED
        elif nm in permit:
            fill_, edge, st, sc = SOFT, LGREY, "izin", GREY
        else:
            fill_, edge, st, sc = OK_BG, OK, "hadir", OK
        rr(d, (cx, cy, cx + cw, cy + rh), 9, fill=fill_, line=edge, w=2)
        avatar(d, cx + 28, cy + rh / 2, nm[:2].upper(), edge, 17, 14)
        t(d, (cx + 54, cy + 12), nm, 17, INK, True)
        t(d, (cx + 54, cy + 33), st, 12, sc, True)
        if nm in unknown:
            t(d, (cx + cw - 14, cy + rh / 2), "?", 22, GOLD_D, True, "rm")

    rr(d, (px, ty, px + pw, fy - 12), 12, fill=WHITE, line=RULE, w=2)
    d.rectangle((px, ty, px + pw, ty + 48), fill=TEAL)
    t(d, (px + 18, ty + 24), "SATU PINTU · QR SESI", 19, WHITE, True, "lm")
    qs = 236
    qr_pattern(d, px + (pw - qs) / 2, ty + 66, qs)
    t(d, (px + pw / 2, ty + 316), "Pindai untuk absen & isi DMS", 16, NAVY, True, "mm")
    t(d, (px + pw / 2, ty + 342), "berlaku Shift 1 · 06.00–14.00 · Line 9", 13, GREY, False, "mm")
    sy = ty + 372
    steps = [("1", "Absensi", "AKTIF · wajib dulu", TEAL, True),
             ("2", "Isi divisi", "terkunci", LGREY, False),
             ("3", "Review & kirim", "terkunci", LGREY, False)]
    for num, lbl, st, col, on in steps:
        rr(d, (px + 18, sy, px + pw - 18, sy + 44), 8,
           fill=(0xE8, 0xF3, 0xF2) if on else SOFT, line=col, w=2 if on else 1)
        d.ellipse((px + 30, sy + 12, px + 50, sy + 32), fill=col)
        t(d, (px + 40, sy + 22), num, 13, WHITE, True, "mm")
        t(d, (px + 62, sy + 22), lbl, 16, INK if on else GREY, True, "lm")
        t(d, (px + pw - 30, sy + 22), st, 12, col, True, "rm")
        sy += 48
    btn(d, (px + 18, sy + 6, px + pw - 18, sy + 58), "KONFIRMASI KEHADIRAN", TEAL, 18)
    wrap(d, (px + 18, sy + 70), "Isian divisi terbuka setelah kehadiran dikonfirmasi (R-81). "
         "Supervisor/DH dapat membuka bila tertunda, dengan alasan tercatat.", pw - 36, 12, GREY)
    im.save(f"{OUT}/tv_absen.png")


def tv_qr():
    """Sesi dibuka: QR satu pintu + urutan langkah (R-82)."""
    im, _ = canvas()
    im, inner = device_tablet(im, (44, 44, 1556, 912))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = inner
    tv_head(d, inner, "SESI DMS DIBUKA", NAVY, WHITE, "MULAI DARI SINI")
    fy = tv_foot(d, inner, 1, src="EXCEL", extra="Sesi belum dikonfirmasi")
    ty = y0 + 88
    lx, lw = x0 + 24, 620
    px = lx + lw + 28
    pw = x1 - 24 - px
    rr(d, (lx, ty, lx + lw, fy - 16), 14, fill=WHITE, line=RULE, w=2)
    t(d, (lx + lw / 2, ty + 34), "PINDAI UNTUK MULAI DMS", 24, NAVY, True, "mm")
    qs = 330
    qr_pattern(d, lx + (lw - qs) / 2, ty + 62, qs)
    t(d, (lx + lw / 2, ty + 412), "dms.contoh.id/s/9f2c-s1", 18, TEAL, True, "mm")
    t(d, (lx + lw / 2, ty + 442), "QR berputar setiap shift · dapat dicabut Admin", 14, GREY, False, "mm")
    t(d, (lx + lw / 2, ty + 468), "menulis tetap wajib login/SSO", 14, GREY, False, "mm")

    rr(d, (px, ty, px + pw, fy - 16), 14, fill=SOFT2, line=RULE, w=2)
    t(d, (px + 22, ty + 22), "SATU PINTU UNTUK SEMUA PERAN", 20, NAVY, True)
    t(d, (px + 22, ty + 52), "Absensi · isian divisi · PICA · review — satu tautan sesi, bukan aplikasi terpisah", 14, GREY)
    steps = [("1", "ABSENSI", "Leader menandai yang tidak hadir lalu konfirmasi. Wajib selesai lebih dulu.", TEAL, "WAJIB DULU"),
             ("2", "ISI DIVISI", "SHE · Quality · Produksi · Delivery · Teknik. Kolom mengikuti Excel.", NAVY, "TERBUKA SETELAH 1"),
             ("3", "REVIEW & KIRIM", "Cek sebab, tindakan, PIC, tenggat; kirim bagian divisi sendiri.", GOLD_D, "TERKUNCI"),
             ("4", "SESI TERKUNCI", "TV pindah dari Absensi ke rotasi divisi; laporan ikut terbarui.", GREY, "OTOMATIS")]
    sy = ty + 88
    for num, ttl, desc, col, tag in steps:
        rr(d, (px + 22, sy, px + pw - 22, sy + 100), 10, fill=WHITE, line=RULE, w=2)
        d.rectangle((px + 22, sy, px + 28, sy + 100), fill=col)
        d.ellipse((px + 44, sy + 18, px + 78, sy + 52), fill=col)
        t(d, (px + 61, sy + 35), num, 18, WHITE, True, "mm")
        t(d, (px + 94, sy + 20), ttl, 19, INK, True)
        pill(d, px + 94 + tw(d, ttl, 19, True) + 14, sy + 18, tag, col, 11, 24, False)
        wrap(d, (px + 94, sy + 50), desc, pw - 140, 14, GREY)
        sy += 112
    im.save(f"{OUT}/tv_qr.png")


def dasbor():
    im, _ = canvas()
    im, inner = device_laptop(im)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = inner
    y = appbar(d, inner, "Dasbor L2 · Supervisor", [("3 Nov 2026", TEAL)], sub="Snack · Line 9 · shift 1")

    nx = sidebar(d, inner, y, [("Hari ini", "grid", ""), ("Kasus terbuka", "doc", "8"),
                               ("Tren pekan", "chart", ""), ("Perbandingan plant", "chart", ""),
                               ("Laporan & KPI", "doc", ""), ("Pengaturan", "gear", "")],
                 "Hari ini")

    # toolbar
    d.rectangle((nx, y, x1, y + 58), fill=WHITE)
    d.line((nx, y + 58, x1, y + 58), fill=RULE, width=2)
    rr(d, (nx + 20, y + 12, nx + 250, y + 46), 8, fill=SOFT, line=RULE, w=1)
    t(d, (nx + 36, y + 20), "Cari line, kasus, PIC…", 14, LGREY)
    for i, (nm, on) in enumerate([("Hari ini", True), ("7 hari", False), ("30 hari", False)]):
        w = 30 + tw(d, nm, 14, True)
        bx = nx + 300 + i * (w + 8)
        if on:
            pill(d, bx, y + 14, nm, NAVY, 14, 30)
        else:
            pill(d, bx, y + 14, nm, LGREY, 14, 30, solid=False)
    btn(d, (x1 - 150, y + 12, x1 - 20, y + 46), "Ekspor", TEAL, 15, ghost=True, radius=8)
    y += 58

    # KPI
    kpis = [("Kasus hari ini", "96", "+12 vs kemarin", NAVY, [3, 4, 3, 5, 6, 5, 7]),
            ("Close lengkap", "74%", "+6 poin", TEAL, [4, 5, 5, 6, 6, 7, 7]),
            ("Lewat tenggat", "8", "−3 vs kemarin", RED, [7, 6, 6, 5, 5, 4, 4]),
            ("Pola berulang", "5", "2 tanpa tindakan", GOLD, [3, 3, 4, 3, 4, 5, 5])]
    x = nx + 20
    for name, val, delta, col, spark in kpis:
        box = (x, y + 16, x + 236, y + 130)
        card(d, box)
        d.rectangle((box[0], box[1] + 1, box[0] + 5, box[3] - 1), fill=col)
        t(d, (box[0] + 20, box[1] + 12), name, 14, GREY)
        t(d, (box[0] + 20, box[1] + 34), val, 38, col, True)
        t(d, (box[0] + 20, box[1] + 82), delta, 12, GREY)
        sparkline(d, (box[0] + 130, box[1] + 40, box[2] - 18, box[1] + 80), spark, col)
        x += 248

    # grafik pilar
    gy = y + 146
    card(d, (nx + 20, gy, nx + 470, gy + 250), "Kasus per pilar · 7 hari", "gelap = 7 hari · terang = hari ini")
    base = gy + 214
    for i, (nm, a, b, col) in enumerate([("SHE", 62, 9, NAVY), ("QC", 90, 14, TEAL),
                                        ("Prod", 78, 12, GOLD), ("Del", 24, 4, TEAL)]):
        bx = nx + 60 + i * 100
        d.rectangle((bx, base - a * 1.45, bx + 34, base), fill=col)
        d.rectangle((bx + 40, base - b * 1.45, bx + 74, base), fill=(0xE1, 0xE7, 0xF0))
        t(d, (bx + 17, base - a * 1.45 - 20), str(a), 12, col, True, "ma")
        t(d, (bx + 17, base + 12), nm, 13, GREY, False, "ma")
    d.line((nx + 40, base, nx + 450, base), fill=RULE, width=2)

    # temuan terbuka
    card(d, (nx + 486, gy, x1 - 20, gy + 250), "Temuan terbuka · 3 teratas", right="urut dampak")
    items = [("I-02 · LEWAT TENGGAT", "Downtime WS L02", "menunggu bukti", "6 HARI", RED),
             ("I-03 · BERULANG", "BCT WS L04 P02", "sebab sama 134×", "BERULANG", GOLD_D),
             ("I-10 · MENUMPUK", "Checklist line 3", "kosong 3 hari", "HARI INI", TEAL)]
    yy = gy + 58
    for code, title, sub, badge, col in items:
        card(d, (nx + 502, yy, x1 - 36, yy + 58), fill=SOFT2)
        d.rectangle((nx + 502, yy + 1, nx + 507, yy + 57), fill=col)
        t(d, (nx + 520, yy + 7), code, 10, LGREY, True)
        t(d, (nx + 520, yy + 24), title, 16, INK, True)
        t(d, (nx + 716, yy + 27), sub, 12, GREY)
        pill(d, x1 - 52, yy + 15, badge, col, 10, 24, True, "r")
        yy += 64

    # tabel kasus
    ty2 = gy + 264
    card(d, (nx + 20, ty2, x1 - 20, y1 - 16), "Kasus lewat tenggat", right="lihat semua 8 kasus  →")
    cols = [(nx + 40, "KODE", "l"), (nx + 150, "LINE / MESIN", "l"), (nx + 360, "SEBAB", "l"),
            (nx + 640, "PIC", "l"), (nx + 800, "UMUR", "l"), (x1 - 44, "STATUS", "r")]
    hy = table_head(d, nx + 32, x1 - 32, ty2 + 52, cols, 32)
    rows = [("SN-DT-0912", "WS L02", "belt aus", "Dhani", "6 hari", "LEWAT", RED),
            ("SN-QC-0441", "packing 3", "film roll", "Sigit", "4 hari", "LEWAT", RED),
            ("SN-PR-0087", "line 3", "tunggu material", "Rani", "4 hari", "DITINJAU", GOLD_D)]
    ry = hy
    for i, (kode, line, sebab, pic, umur, st, col) in enumerate(rows):
        if i % 2:
            d.rectangle((nx + 32, ry, x1 - 32, ry + 33), fill=SOFT2)
        t(d, (nx + 40, ry + 9), kode, 13, NAVY, True)
        t(d, (nx + 150, ry + 9), line, 13, INK)
        t(d, (nx + 360, ry + 9), sebab, 13, GREY)
        avatar(d, nx + 660, ry + 16, pic[0], TEAL, 11, 9)
        t(d, (nx + 676, ry + 9), pic, 13, INK)
        t(d, (nx + 800, ry + 9), umur, 13, col, True)
        pill(d, x1 - 52, ry + 5, st, col, 10, 22, True, "r")
        ry += 33
    im.save(f"{OUT}/dasbor.png")


# ------------------------------------------------------------------ admin
def admin():
    im, _ = canvas()
    im, inner = device_laptop(im, (150, 70, 1450, 830))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = inner
    y = appbar(d, inner, "Halaman admin", [("Admin plant", GOLD)], sub="Snack · hak ubah aturan")

    nx = sidebar(d, inner, y, [("Beranda", "grid", ""), ("Pengguna", "users", ""),
                               ("Target & KPI", "chart", ""), ("Layar TV", "tv", ""),
                               ("Kunci periode", "doc", ""), ("Jejak audit", "check", "")],
                 "Target & KPI", foot="ADMIN PLANT · SNACK", w=232)

    tabs = ["Pengguna", "Target & KPI", "Layar TV", "Kunci periode", "Audit"]
    tx = nx + 24
    for name in tabs:
        on = name == "Target & KPI"
        t(d, (tx, y + 22), name, 17, NAVY if on else GREY, on)
        if on:
            d.rectangle((tx, y + 52, tx + tw(d, name, 17, True), y + 56), fill=GOLD)
        tx += tw(d, name, 17, True) + 40
    y += 74

    # kartu target
    card(d, (nx + 24, y, nx + 470, y + 330), "Target & bobot KPI · versi",
         "versi 2 · berlaku Nov 2026 – Jan 2027")
    pilar = [("SHE", "zero accident", "30%", "V/O", RED, 100),
             ("Quality", "defect per line", "30%", "V/O", GOLD, 92),
             ("Produksi", "OEE", "25%", "V/O", NAVY, 78),
             ("Delivery", "plan vs real", "15%", "V/O", TEAL, 88)]
    yy = y + 78
    for name, sub, bobot, jenis, col, ach in pilar:
        card(d, (nx + 40, yy, nx + 454, yy + 46), fill=SOFT2)
        d.rectangle((nx + 40, yy + 1, nx + 45, yy + 45), fill=col)
        t(d, (nx + 56, yy + 6), name, 14, INK, True)
        t(d, (nx + 56, yy + 25), sub, 11, GREY)
        t(d, (nx + 220, yy + 14), f"bobot {bobot}", 12, GREY)
        pill(d, nx + 300, yy + 10, jenis, col, 11, 24)
        d.rectangle((nx + 352, yy + 18, nx + 444, yy + 26), fill=(0xE3, 0xE8, 0xF0))
        d.rectangle((nx + 352, yy + 18, nx + 352 + 92 * ach / 100, yy + 26), fill=col)
        yy += 52
    btn(d, (nx + 40, y + 288, nx + 210, y + 322), "Simpan versi baru", NAVY, 13, radius=8)
    t(d, (nx + 222, y + 296), "simulasi dampak wajib dilihat", 11, LGREY)

    # kartu TV
    card(d, (nx + 486, y, x1 - 24, y + 330), "Profil layar TV", right="3 layar aktif")
    tv_rows = [("SN-L09-TV1", "TV lantai 1 · Snack", "divisi + absensi awal", "aktif", OK),
               ("SN-L09-TV2", "TV lantai 2 · Snack", "rotasi 7 halaman", "aktif", OK),
               ("DR-L01-TV1", "TV Dairy", "belum dipasang", "menunggu", LGREY)]
    yy = y + 66
    for kode, name, mode, st, col in tv_rows:
        card(d, (nx + 502, yy, x1 - 40, yy + 62), fill=SOFT2)
        icon(d, nx + 516, yy + 18, 24, "tv", GREY)
        t(d, (nx + 550, yy + 10), name, 16, INK, True)
        t(d, (nx + 550, yy + 32), f"{kode} · {mode}", 13, GREY)
        pill(d, x1 - 56, yy + 18, st.upper(), col, 12, 26, True, "r")
        yy += 70
    t(d, (nx + 502, y + 288), "Rotasi 20 detik · pilar yang tampil bisa dipilih per layar",
      13, LGREY)

    # kunci periode + audit
    ry = y + 346
    rr(d, (nx + 24, ry, nx + 470, y1 - 20), 12, fill=(0xFD, 0xF6, 0xE8), line=(0xE0, 0xC9, 0x8C), w=2)
    t(d, (nx + 40, ry + 16), "KUNCI PERIODE", 13, GOLD_D, True)
    t(d, (nx + 40, ry + 40), "Oktober 2026 sudah dilaporkan", 19, INK, True)
    t(d, (nx + 40, ry + 70), "Periode terkunci tidak dapat diubah;", 14, GREY)
    t(d, (nx + 40, ry + 92), "koreksi dicatat sebagai versi baru.", 14, GREY)
    btn(d, (nx + 40, ry + 120, nx + 220, ry + 154), "Buka kunci", NAVY, 14, ghost=True, radius=8)
    t(d, (nx + 40, ry + 164), "wajib alasan · tercatat di audit", 12, LGREY)

    card(d, (nx + 486, ry, x1 - 24, y1 - 20), "Jejak audit", right="terbaru")
    log = [("07.04", "Dhani", "menutup DT-0912 · bukti 1 berkas", OK),
           ("07.06", "Sigit", "mengubah target QC line 4", GOLD_D),
           ("07.11", "Admin", "menambah layar TV SN-L09-TV2", TEAL)]
    yy = ry + 54
    for jam, who, what, col in log:
        d.ellipse((nx + 502, yy + 8, nx + 512, yy + 18), fill=col)
        t(d, (nx + 522, yy + 2), jam, 12, LGREY, True)
        t(d, (nx + 570, yy), who, 14, INK, True)
        t(d, (nx + 570, yy + 21), what, 12, GREY)
        yy += 40
    im.save(f"{OUT}/admin.png")


# ------------------------------------------------------------------ kasus
def kasus():
    im, _ = canvas()
    im, inner = device_laptop(im, (150, 60, 1450, 830))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = inner
    y = appbar(d, inner, "Kasus · SN-DT-0912", [("LEWAT TENGGAT", RED)], sub="menunggu bukti penutupan")
    nx = sidebar(d, inner, y, [("Hari ini", "grid", ""), ("Kasus terbuka", "doc", "8"),
                               ("Tren pekan", "chart", ""), ("Perbandingan plant", "chart", ""),
                               ("Laporan & KPI", "doc", ""), ("Pengaturan", "gear", "")],
                 "Kasus terbuka")

    # header kasus
    card(d, (nx + 20, y + 16, x1 - 20, y + 136))
    d.rectangle((nx + 20, y + 17, nx + 26, y + 135), fill=RED)
    t(d, (nx + 40, y + 28), "SN-DT-0912 · Downtime WS L02", 23, INK, True)
    t(d, (nx + 40, y + 60), "Snack · Line 9 · dilaporkan 28 Okt 07.04 oleh Rani (leader shift 1)",
      14, GREY)
    pill(d, x1 - 296, y + 28, "DAMPAK A", NAVY, 11, 24)
    pill(d, x1 - 192, y + 28, "LEWAT 6 HARI", RED, 11, 24)
    t(d, (x1 - 40, y + 68), "Tenggat 29 Okt 16.00", 13, GREY, anchor="ra")
    t(d, (x1 - 40, y + 90), "Eskalasi L2 · supervisor", 13, RED, True, "ra")

    # riwayat kasus
    ty = y + 152
    card(d, (nx + 20, ty, nx + 470, ty + 258), "Riwayat kasus")
    steps = [("Dilaporkan", "28 Okt 07.04 · Rani", OK, True),
             ("Diagnosis Teknik", "28 Okt 09.20 · WO EP-TK-0031", OK, True),
             ("Perbaikan", "28 Okt 14.05 · belt diganti", OK, True),
             ("Verifikasi", "29 Okt 07.10 · menunggu bukti", GOLD_D, True),
             ("Penutupan", "belum · 2 kolom wajib kosong", LGREY, False)]
    yy = ty + 50
    for i, (name, sub, col, done) in enumerate(steps):
        d.ellipse((nx + 40, yy + 4, nx + 54, yy + 18), fill=col if done else WHITE,
                  outline=col, width=2)
        if i < len(steps) - 1:
            d.line((nx + 47, yy + 18, nx + 47, yy + 42), fill=RULE, width=3)
        t(d, (nx + 68, yy), name, 15, INK, True)
        t(d, (nx + 68, yy + 21), sub, 12, GREY)
        yy += 42

    # kolom wajib
    card(d, (nx + 486, ty, x1 - 20, ty + 258), "Empat kolom wajib sebelum kasus ditutup")
    fields = [("Sebab", "belt aus karena umur pakai", True, OK),
              ("Tindakan", "ganti belt + cek line 9", True, OK),
              ("Bukti", "0 berkas", False, RED),
              ("PIC", "Dhani", True, OK)]
    fy = ty + 50
    for name, val, filled, col in fields:
        t(d, (nx + 504, fy + 8), name, 12, LGREY, True)
        rr(d, (nx + 580, fy, x1 - 210, fy + 30), 8,
           fill=(0xFD, 0xF3, 0xF3) if not filled else SOFT2,
           line=(0xD9, 0x9C, 0x9C) if not filled else RULE, w=2)
        t(d, (nx + 594, fy + 6), val, 13, col if not filled else INK, not filled)
        if not filled:
            pill(d, x1 - 196, fy + 2, "WAJIB", RED, 10, 24)
        fy += 40
    btn(d, (nx + 504, ty + 208, nx + 690, ty + 240), "Ajukan penutupan", LGREY, 13, radius=8)
    t(d, (nx + 700, ty + 214), "aktif setelah bukti dilampirkan", 11, GREY)

    # PICA
    py = ty + 274
    card(d, (nx + 20, py, nx + 690, y1 - 22), "PICA · empat pertanyaan", right="5 why")
    cols = [(nx + 40, "TAHAP", "l"), (nx + 170, "PERTANYAAN", "l"), (nx + 520, "TEMUAN", "l")]
    hy = table_head(d, nx + 32, nx + 678, py + 46, cols, 24)
    whys = [("Why 1", "kenapa line berhenti?", "belt putus"),
            ("Why 2", "kenapa belt putus?", "umur pakai > 4.000 jam"),
            ("Why 3", "kenapa lewat umur?", "PM tertunda 2 periode"),
            ("Why 4", "kenapa PM tertunda?", "jadwal PM belum di sistem")]
    ry = hy
    for i, (a, b, c_) in enumerate(whys):
        if i % 2:
            d.rectangle((nx + 32, ry, nx + 678, ry + 23), fill=SOFT2)
        t(d, (nx + 40, ry + 5), a, 11, NAVY, True)
        t(d, (nx + 170, ry + 5), b, 12, INK)
        t(d, (nx + 520, ry + 5), c_, 12, GREY)
        ry += 23
    rr(d, (nx + 40, ry + 8, nx + 670, ry + 36), 8, fill=(0xFD, 0xF6, 0xE8))
    t(d, (nx + 54, ry + 15), "Pencegahan: jadwal PM masuk sistem, pengingat H-3 sebelum jatuh tempo",
      11, GOLD_D, True)

    # lampiran + dampak
    card(d, (nx + 706, py, x1 - 20, py + 116), "Lampiran", right="1 dari 3")
    for i in range(3):
        bx = nx + 722 + i * 96
        rr(d, (bx, py + 42, bx + 84, py + 104), 8,
           fill=(0xD8, 0xE4, 0xDD) if i == 0 else SOFT, line=RULE, w=2)
        t(d, (bx + 42, py + 68), "foto" if i == 0 else "+", 12, GREY, False, "mm")

    card(d, (nx + 706, py + 128, x1 - 20, y1 - 22), "Dampak tercatat")
    dampak = [("48 mnt", "line berhenti", RED), ("420 pcs", "output hilang", GOLD_D),
              ("134×", "berulang 90 hari", NAVY)]
    yy = py + 168
    for val, lbl, col in dampak:
        t(d, (nx + 722, yy), val, 17, col, True)
        t(d, (nx + 812, yy + 2), lbl, 12, GREY)
        yy += 32
    im.save(f"{OUT}/kasus.png")


# ------------------------------------------------------------------ laporan
def laporan():
    im, _ = canvas()
    im, inner = device_laptop(im, (150, 60, 1450, 830))
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = inner
    y = appbar(d, inner, "Laporan & skor KPI", [("Oktober 2026", TEAL)],
               sub="Snack · periode terkunci")
    nx = sidebar(d, inner, y, [("Hari ini", "grid", ""), ("Kasus terbuka", "doc", ""),
                               ("Tren pekan", "chart", ""), ("Perbandingan plant", "chart", ""),
                               ("Laporan & KPI", "doc", ""), ("Pengaturan", "gear", "")],
                 "Laporan & KPI")

    # filter
    d.rectangle((nx, y, x1, y + 58), fill=WHITE)
    d.line((nx, y + 58, x1, y + 58), fill=RULE, width=2)
    for i, (nm, val) in enumerate([("Plant", "Snack"), ("Periode", "Okt 2026"), ("Shift", "Semua")]):
        bx = nx + 20 + i * 190
        t(d, (bx, y + 12), nm.upper(), 11, LGREY, True)
        rr(d, (bx, y + 28, bx + 170, y + 48), 6, fill=SOFT, line=RULE, w=1)
        t(d, (bx + 10, y + 31), val, 13, INK)
    btn(d, (x1 - 300, y + 12, x1 - 160, y + 46), "Unduh", TEAL, 14, ghost=True, radius=8)
    btn(d, (x1 - 150, y + 12, x1 - 20, y + 46), "Kirim ke Group", NAVY, 14, radius=8)
    y += 58

    # skor
    scores = [("Skor proses", "92", "kelengkapan & ketepatan waktu", TEAL, 92),
              ("Skor hasil", "74", "pencapaian target pilar", NAVY, 74),
              ("KPI tercapai", "18/24", "V/O biner · 6 belum", GOLD_D, 75)]
    x = nx + 20
    for name, val, sub, col, pct in scores:
        card(d, (x, y + 16, x + 290, y + 150))
        t(d, (x + 20, y + 30), name, 14, GREY)
        t(d, (x + 20, y + 52), val, 40, col, True)
        t(d, (x + 20, y + 104), sub, 12, GREY)
        d.rectangle((x + 20, y + 128, x + 270, y + 136), fill=SOFT)
        d.rectangle((x + 20, y + 128, x + 20 + 250 * pct / 100, y + 136), fill=col)
        x += 302

    # tren
    gy = y + 166
    card(d, (nx + 20, gy, nx + 520, gy + 250), "Close lengkap · 6 bulan",
         "batang = per bulan · garis = tren")
    base = gy + 200
    vals = [58, 61, 66, 70, 68, 74]
    pts = []
    for i, v in enumerate(vals):
        bx = nx + 70 + i * 68
        d.rectangle((bx, base - v * 1.6, bx + 40, base), fill=(0xE6, 0xEB, 0xF3))
        t(d, (bx + 20, base - v * 1.6 - 20), f"{v}%", 11, GREY, True, "ma")
        t(d, (bx + 20, base + 10), ["Mei", "Jun", "Jul", "Agu", "Sep", "Okt"][i], 11, LGREY, False, "ma")
        pts.append((bx + 20, base - v * 1.6))
    d.line(pts, fill=TEAL, width=4, joint="curve")
    d.line((nx + 50, base, nx + 500, base), fill=RULE, width=2)

    # tabel per line
    card(d, (nx + 536, gy, x1 - 20, gy + 250), "Skor per line", right="20 line")
    cols = [(nx + 556, "LINE", "l"), (nx + 650, "PROSES", "c"), (nx + 740, "HASIL", "c"),
            (nx + 830, "KPI", "c"), (nx + 900, "CATATAN", "l")]
    hy = table_head(d, nx + 546, x1 - 32, gy + 56, cols, 30)
    lines = [("Line 9", "98", "88", "6/6", OK, "terbaik"),
             ("Line 3", "94", "76", "5/6", OK, "QC hold"),
             ("Line 12", "88", "71", "4/6", GOLD_D, "PM tertunda"),
             ("Line 4", "72", "64", "3/6", RED, "pengisian")]
    ry = hy
    for i, (nm, p, h, k, col, note) in enumerate(lines):
        if i % 2:
            d.rectangle((nx + 546, ry, x1 - 32, ry + 36), fill=SOFT2)
        t(d, (nx + 556, ry + 10), nm, 13, INK, True)
        for val, cx in ((p, nx + 650), (h, nx + 740), (k, nx + 830)):
            bg = OK_BG if int(str(val).split("/")[0]) >= 5 else (WARN_BG if int(str(val).split("/")[0]) >= 4 else BAD_BG)
            rr(d, (cx - 24, ry + 7, cx + 24, ry + 31), 6, fill=bg)
            t(d, (cx, ry + 11), val, 12, col, True, "ma")
        t(d, (nx + 900, ry + 11), note, 12, GREY)
        ry += 36

    # catatan metode
    ny = gy + 266
    card(d, (nx + 20, ny, x1 - 20, y1 - 20), "Catatan metode", fill=SOFT)
    notes = [("Skor proses dan hasil dipisah",
              "kelengkapan pengisian dihitung sendiri, tidak digabung dengan pencapaian target pilar"),
             ("KPI V/O biner",
              "tercapai atau tidak; tidak ada nilai antara yang bisa ditawar saat rapat"),
             ("Angka dari catatan, bukan rekap",
              "ringkasan dihitung sistem dari satu catatan kasus, bukan diketik ulang"),
             ("Periode terkunci, koreksi berversi",
              "angka Oktober tidak berubah setelah disahkan; koreksi dicatat sebagai versi baru")]
    x = nx + 40
    for i, (head_, body) in enumerate(notes):
        col = x + (i % 2) * 480
        row = ny + 46 + (i // 2) * 60
        d.ellipse((col, row + 4, col + 10, row + 14), fill=TEAL)
        t(d, (col + 18, row), head_, 13, NAVY, True)
        wrap(d, (col + 18, row + 21), body, 430, 11, GREY, lh=15)
    im.save(f"{OUT}/laporan.png")


def trim(name):
    p = f"{OUT}/{name}.png"
    im = Image.open(p).convert("RGB")
    from PIL import ImageChops
    bg = im.getpixel((2, 2))
    diff = ImageChops.difference(im, Image.new("RGB", im.size, bg))
    bb = diff.getbbox()
    if bb:
        pad = 8
        bb = (max(bb[0] - pad, 0), max(bb[1] - pad, 0),
              min(bb[2] + pad, im.width), min(bb[3] + pad, im.height))
        im.crop(bb).save(p)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    form()
    tv()
    tv_divisi("quality")
    tv_divisi("produksi")
    tv_absen()
    tv_qr()
    dasbor()
    admin()
    kasus()
    laporan()
    for name in ("form", "tv", "tv_quality", "tv_produksi", "tv_absen", "tv_qr",
                 "dasbor", "admin", "kasus", "laporan"):
        trim(name)
        p = f"{OUT}/{name}.png"
        print(p, Image.open(p).size, f"{os.path.getsize(p) / 1024:.0f} KB")
