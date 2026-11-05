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
    # kamera depan
    d.ellipse((790, 82, 810, 102), fill=(0x3A, 0x42, 0x52))
    rr(d, (82, 116, 1518, 916), 12, fill=WHITE)

    # kepala
    d.rectangle((82, 116, 1518, 186), fill=NAVY)
    t(d, (112, 138), "FORM HARIAN  ·  SNACK  ·  LINE 9", 26, WHITE, True)
    t(d, (1488, 140), "Sen, 3 Nov 2026 · Shift 1", 21, (0xC9, 0xD3, 0xE6), anchor="ra")

    # sub kepala
    t(d, (112, 202), "Isi harian", 24, NAVY, True)
    t(d, (300, 206), "12 dari 15 item terisi · sisa 4 menit", 20, GREY)
    chip(d, 1300, 198, 196, 36, "DRAF TERSIMPAN", PALE, 15, GREY)

    # tabel
    cols = [(112, 620), (620, 790), (790, 960), (960, 1230), (1230, 1490)]
    head = ["ITEM CHECKLIST", "TARGET", "HASIL", "STATUS", "SEBAB / BUKTI"]
    d.rectangle((112, 250, 1490, 292), fill=SOFT)
    for (x0, x1), h_ in zip(cols, head):
        t(d, (x0 + 12, 264), h_, 17, LGREY, True)

    rows = [("Checklist A · critical point", "100%", "100%", "SESUAI", "", TEAL),
            ("Checklist B · suhu ruang", "≤ 18 °C", "16 °C", "SESUAI", "", TEAL),
            ("Defect visual · packing", "≤ 0,6%", "0,9%", "DI ATAS TARGET", "film roll WS L02", RED),
            ("Downtime mesin", "≤ 20 mnt", "48 mnt", "LEWAT BATAS", "belt aus · 1 foto", RED),
            ("Output shift", "8.400 pcs", "8.120 pcs", "DI BAWAH TARGET", "tunggu material", GOLD)]
    y = 292
    for i, (item, tg, hs, st, sb, col) in enumerate(rows):
        if i % 2:
            d.rectangle((112, y, 1490, y + 78), fill=(0xFA, 0xFB, 0xFD))
        d.line((112, y + 78, 1490, y + 78), fill=RULE, width=1)
        t(d, (124, y + 26), item, 22, INK)
        t(d, (632, y + 26), tg, 22, GREY)
        t(d, (802, y + 26), hs, 22, INK, True)
        cw = 26 + len(st) * 11
        chip(d, 968, y + 22, cw, 34, st, col, 15)
        t(d, (1243, y + 26), sb if sb else "—", 18, GREY)
        y += 78

    # kolom sebab + bukti + tombol
    rr(d, (112, 700, 780, 884), 12, fill=(0xFD, 0xF3, 0xF3), line=(0xD9, 0x9C, 0x9C), w=2)
    t(d, (132, 716), "SEBAB WAJIB DIISI", 16, RED, True)
    t(d, (132, 748), "Belt WS L02 aus, diganti", 24, INK)
    t(d, (132, 786), "Tindakan: ganti belt, cek sebelum shift 2", 19, GREY)
    t(d, (132, 816), "PIC: Dhani  ·  tenggat 3 Nov 16.00", 19, GREY)

    rr(d, (798, 700, 1230, 884), 12, fill=SOFT, line=RULE, w=2)
    t(d, (818, 716), "BUKTI FOTO · 1 BERKAS", 16, LGREY, True)
    for i in range(3):
        x0 = 818 + i * 136
        rr(d, (x0, 748, x0 + 120, 832), 8,
           fill=(0xE3, 0xE8, 0xF0) if i else (0xD8, 0xE4, 0xDD),
           line=(0xC2, 0xCB, 0xD9), w=2)
        t(d, (x0 + 60, 790), "foto" if i == 0 else "+", 18, GREY, False, "mm")

    rr(d, (1252, 700, 1490, 776), 12, fill=NAVY)
    t(d, (1371, 738), "Kirim ke dasbor", 23, WHITE, True, "mm")
    t(d, (1252, 796), "angka langsung jadi", 18, GREY)
    t(d, (1252, 822), "di dasbor & TV", 18, GREY)

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
def tv():
    im, d = canvas()
    shadow(im, (60, 60, 1540, 900))
    d = ImageDraw.Draw(im)
    rr(d, (54, 54, 1546, 906), 16, fill=DARK)
    rr(d, (78, 78, 1522, 882), 6, fill=WHITE)

    d.rectangle((78, 78, 1522, 156), fill=NAVY)
    t(d, (108, 104), "LAYAR LANTAI  ·  EXIST PLANT  ·  LINE WS L02", 27, WHITE, True)
    t(d, (1492, 106), "07.10  ·  TANPA LOGIN", 19, GOLD, True, "ra")

    t(d, (108, 178), "Kartu tertua tampil paling atas · berganti tiap 30 detik", 20, GREY)

    cards = [("I-02 · LEWAT TENGGAT", "Downtime WS L02", "montir sudah ditunjuk", "6 HARI", RED, "6 hari"),
             ("I-03 · BERULANG", "BCT WS L04 P02", "sebab sama 134× di plant ini", "BERULANG", GOLD, "134×"),
             ("I-10 · MENUMPUK", "Satu line menumpuk kasus", "96,9% kasus ada di line 9", "L3", TEAL, "96,9%")]
    y = 224
    for code, title, sub, badge, col, big in cards:
        rr(d, (108, y, 1492, y + 186), 10, fill=(0xFA, 0xFB, 0xFD), line=RULE, w=2)
        d.rectangle((108, y, 120, y + 186), fill=col)
        t(d, (140, y + 20), code, 17, GREY, True)
        t(d, (140, y + 50), title, 34, INK, True)
        t(d, (140, y + 100), sub, 21, GREY)
        chip(d, 1226, y + 24, 226, 42, badge, col, 18)
        t(d, (1492 - 26, y + 96), big, 46, col, True, "ra")
        t(d, (1492 - 26, y + 150), "angka pemicu", 16, LGREY, anchor="ra")
        y += 202

    t(d, (108, 842), "Sumber: satu catatan kasus, sama dengan dasbor dan form harian", 18, LGREY)
    im.save(f"{OUT}/tv.png")


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
    admin()
    for name in ("form", "dasbor", "tv", "admin"):
        trim(name)
        p = f"{OUT}/{name}.png"
        print(p, Image.open(p).size, f"{os.path.getsize(p) / 1024:.0f} KB")
