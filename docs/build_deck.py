#!/usr/bin/env python3
"""
Deck DMS memakai template_master.pptx (versi terbaru) DAN data tiga workbook:
Snack, Exist Plant, New Plant (angka dibaca dari docs/data_plants.json).

slide 1 template -> cover · slide 2 template -> halaman isi · slide 3 template -> penutup

Jalankan: python3 docs/analyze_workbook.py && python3 docs/build_deck.py
Hasil  : docs/DMS_Digitalisasi_v1.pptx
"""
import json

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

SRC = "template_master.pptx"
OUT = "docs/DMS_Digitalisasi_v1.pptx"
DATA = json.load(open("docs/data_plants.json", encoding="utf-8"))

SN, EP, NP = DATA["Snack"], DATA["Exist Plant"], DATA["New Plant"]
TOT = DATA["_total"]

NAVY = RGBColor(0x1F, 0x33, 0x64)
TEAL = RGBColor(0x2E, 0x86, 0x8C)
GOLD = RGBColor(0xC8, 0xA5, 0x2B)
RED = RGBColor(0xB0, 0x2F, 0x2F)
INK = RGBColor(0x22, 0x28, 0x33)
GREY = RGBColor(0x5C, 0x64, 0x72)
LGREY = RGBColor(0x8B, 0x93, 0xA1)
RULE = RGBColor(0xD5, 0xDA, 0xE3)
SOFT = RGBColor(0xF4, 0xF6, 0xFA)
PALE = RGBColor(0xD9, 0xDE, 0xE7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)


def n(v):
    """Format angka Indonesia: 17201 -> 17.201"""
    return f"{int(round(v)):,}".replace(",", ".")


def pc(v, dec=0):
    s = f"{v:.{dec}f}".replace(".", ",")
    return s + "%"


prs = Presentation(SRC)
COVER_T, BODY_T, CLOSE_T = prs.slides[0], prs.slides[1], prs.slides[2]
BODY_L, CLOSE_L, COVER_L = BODY_T.slide_layout, CLOSE_T.slide_layout, COVER_T.slide_layout

sldIdLst = prs.slides._sldIdLst
for sid in list(sldIdLst):
    rId = sid.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
    prs.part.drop_rel(rId)
    sldIdLst.remove(sid)


# ---------------------------------------------------------------- primitif
def txt(slide, x, y, w, h, lines, size=11, color=INK, bold=False, align=PP_ALIGN.LEFT,
        spacing=1.18, anchor=MSO_ANCHOR.TOP, italic=False):
    box_ = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box_.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = Inches(0.02)
    tf.margin_top = tf.margin_bottom = 0
    if isinstance(lines, str):
        lines = [(lines, size, bold, color)]
    first = tf.paragraphs[0]
    for i, item in enumerate(lines):
        t, sz, bd, col = (tuple(item) + (None, None, None))[:4]
        p = first if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        r = p.add_run()
        r.text = t
        r.font.size = Pt(sz or size)
        r.font.bold = bold if bd is None else bd
        r.font.italic = italic
        r.font.name = "Calibri"
        r.font.color.rgb = col or color
    return box_


def shape(slide, kind, x, y, w, h, fill=SOFT, line=RULE, lw=1.0, adj=None):
    s = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid()
        s.fill.fore_color.rgb = fill
    if line is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line
        s.line.width = Pt(lw)
    s.shadow.inherit = False
    if adj is not None:
        s.adjustments[0] = adj
    return s


def box(slide, x, y, w, h, fill=SOFT, line=RULE, lw=1.0, radius=0.05):
    return shape(slide, MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                 x, y, w, h, fill, line, lw, radius)


def hline(slide, x, y, w, color=RULE, h=0.015):
    box(slide, x, y, w, h, fill=color, line=None, radius=None)


def arrow(slide, x, y, w, h, direction="right", color=LGREY):
    kinds = {"right": MSO_SHAPE.RIGHT_ARROW, "left": MSO_SHAPE.LEFT_ARROW,
             "down": MSO_SHAPE.DOWN_ARROW, "up": MSO_SHAPE.UP_ARROW}
    return shape(slide, kinds[direction], x, y, w, h, fill=color, line=None)


def table(slide, data, widths, x, y, row_h=0.36, head_h=0.36, fs=10.5, head_fs=10.5,
          aligns=None, bold_first=False):
    rows, cols = len(data), len(data[0])
    gf = slide.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(sum(widths)),
                                Inches(head_h + row_h * (rows - 1)))
    t = gf.table
    t.first_row = True
    t.horz_banding = False
    for i, w in enumerate(widths):
        t.columns[i].width = Inches(w)
    for r in range(rows):
        t.rows[r].height = Inches(head_h if r == 0 else row_h)
        for c in range(cols):
            cell = t.cell(r, c)
            cell.margin_left = Inches(0.07)
            cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if r == 0 else (WHITE if r % 2 else SOFT)
            p = cell.text_frame.paragraphs[0]
            p.alignment = aligns[c] if aligns else PP_ALIGN.LEFT
            run = p.add_run()
            run.text = str(data[r][c])
            run.font.size = Pt(head_fs if r == 0 else fs)
            run.font.name = "Calibri"
            run.font.bold = (r == 0) or (bold_first and c == 0)
            run.font.color.rgb = WHITE if r == 0 else INK
    return gf


def img_slot(slide, x, y, w, h, caption, note):
    box(slide, x, y, w, h, fill=RGBColor(0xF8, 0xFA, 0xFD), line=RGBColor(0xBE, 0xC7, 0xD6), radius=0.04)
    box(slide, x + w / 2 - 0.16, y + h / 2 - 0.36, 0.32, 0.32, fill=WHITE,
        line=RGBColor(0xBE, 0xC7, 0xD6), radius=0.2)
    txt(slide, x + w / 2 - 0.16, y + h / 2 - 0.32, 0.32, 0.26, [("+", 12, True, LGREY)],
        align=PP_ALIGN.CENTER)
    txt(slide, x + 0.10, y + h / 2 + 0.04, w - 0.20, 0.24,
        [(caption.upper(), 9, True, LGREY)], align=PP_ALIGN.CENTER)
    txt(slide, x + 0.12, y + h / 2 + 0.26, w - 0.24, 0.50,
        [(note, 8, None, RGBColor(0xA9, 0xB2, 0xC0))], align=PP_ALIGN.CENTER, spacing=1.1)


def chart(slide, x, y, w, h, cats, series, kind, colors, number_format="0", legend=False,
          fs=9, gap=60, overlap=None, label_pos=None, label_color=INK, vmax=None,
          point_colors=None):
    data = CategoryChartData()
    data.categories = cats
    for name, vals in series:
        data.add_series(name, vals)
    gf = slide.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), data)
    ch = gf.chart
    ch.has_title = False
    ch.has_legend = legend
    ch.font.size = Pt(fs)
    ch.font.name = "Calibri"
    ch.font.color.rgb = GREY
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP
        ch.legend.include_in_layout = False
        ch.legend.font.size = Pt(fs)
        ch.legend.font.color.rgb = GREY
    plot = ch.plots[0]
    plot.gap_width = gap
    if overlap is not None:
        plot.overlap = overlap
    plot.has_data_labels = True
    dl = plot.data_labels
    dl.font.size = Pt(fs)
    dl.font.bold = True
    dl.font.color.rgb = label_color
    dl.number_format = number_format
    dl.number_format_is_linked = False
    if label_pos is not None:
        dl.position = label_pos
    for i, s in enumerate(ch.series):
        s.format.fill.solid()
        s.format.fill.fore_color.rgb = colors[i % len(colors)]
        s.format.line.fill.background()
    if point_colors:
        for i, col in enumerate(point_colors):
            pt = ch.series[0].points[i]
            pt.format.fill.solid()
            pt.format.fill.fore_color.rgb = col
            pt.format.line.fill.background()
    va = ch.value_axis
    va.has_major_gridlines = True
    va.major_gridlines.format.line.color.rgb = RGBColor(0xE7, 0xEA, 0xF0)
    va.format.line.fill.background()
    va.tick_labels.font.size = Pt(fs - 1)
    va.tick_labels.font.color.rgb = LGREY
    if vmax is not None:
        va.maximum_scale = vmax
    ca = ch.category_axis
    ca.format.line.color.rgb = RULE
    ca.tick_labels.font.size = Pt(fs)
    ca.tick_labels.font.color.rgb = INK
    ca.has_major_gridlines = False
    return gf


PAGE = [1]


def page(title, kicker, no=None, note=None):
    """Halaman isi memakai layout slide 2 template. Nomor halaman otomatis."""
    PAGE[0] += 1
    s = prs.slides.add_slide(BODY_L)
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx not in (0, 1):
            ph._element.getparent().remove(ph._element)
    title_ph = s.shapes.title
    size = 24 if len(title) <= 46 else (22.5 if len(title) <= 56 else 20.5)
    if title_ph is not None:
        title_ph.left, title_ph.top = Inches(2.05), Inches(0.20)
        title_ph.width, title_ph.height = Inches(10.05), Inches(0.68)
        tf = title_ph.text_frame
        tf.word_wrap = False
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = 0
        tf.margin_top = tf.margin_bottom = 0
        tf.text = title
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        for r in p.runs:
            r.font.size = Pt(size)
            r.font.bold = True
            r.font.name = "Calibri"
            r.font.color.rgb = NAVY
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx == 1 and ph != title_ph:
            ph._element.getparent().remove(ph._element)

    hline(s, 2.05, 0.94, 2.20, GOLD, 0.05)
    txt(s, 4.45, 0.82, 6.00, 0.28, [(kicker.upper(), 10, True, GOLD)])
    txt(s, 12.28, 0.26, 0.46, 0.28, [(str(PAGE[0]), 12, True, LGREY)], align=PP_ALIGN.RIGHT)
    if note:
        txt(s, 0.62, 6.98, 9.40, 0.26, [(note, 9, None, LGREY)])
    return s


def kpi_cards(s, items, y=1.24, h=1.06):
    count = len(items)
    gap = 0.10
    w = (12.09 - gap * (count - 1)) / count
    x = 0.62
    for val, lab, note_, col in items:
        box(s, x, y, w, h, fill=SOFT, line=RULE, radius=0.07)
        box(s, x + 0.14, y + 0.14, 0.06, h - 0.28, fill=col, radius=0.5)
        txt(s, x + 0.32, y + 0.06, w - 0.46, 0.50, [(val, 26, True, col)])
        txt(s, x + 0.32, y + 0.56, w - 0.46, 0.24, [(lab, 11, True, INK)])
        txt(s, x + 0.32, y + 0.80, w - 0.46, 0.22, [(note_, 9, None, GREY)])
        x += w + gap


def step(s, x, y, w, h, no, title, body, col=NAVY):
    box(s, x, y, w, h, fill=WHITE, line=RULE, radius=0.05)
    box(s, x, y, 0.50, h, fill=col, line=None, radius=0.05)
    txt(s, x, y + h / 2 - 0.18, 0.50, 0.36, [(str(no), 15, True, WHITE)],
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x + 0.64, y + 0.18, w - 0.80, 0.30, [(title, 12.5, True, NAVY)])
    txt(s, x + 0.64, y + 0.54, w - 0.80, h - 0.66, [(body, 10, None, GREY)], spacing=1.25)


def label(s, x, y, text, w=6.0):
    txt(s, x, y, w, 0.26, [(text.upper(), 10, True, GOLD)])


# ================================================================ 1 · COVER
cover = prs.slides.add_slide(COVER_L)
for sh in list(cover.shapes):
    if sh.is_placeholder:
        sh._element.getparent().remove(sh._element)

box(cover, 5.00, 0.25, 5.75, 3.11, fill=RGBColor(0xFA, 0xFA, 0xFA), line=None, radius=0.03)
box(cover, 10.50, 1.64, 2.75, 1.92, fill=RGBColor(0xFA, 0xFA, 0xFA), line=None, radius=0.03)

txt(cover, 5.26, 0.50, 5.10, 0.26, [("OPERATIONAL REVIEW  ·  GOOD IN ACTIONS", 10, True, GOLD)])
hline(cover, 5.26, 0.80, 1.30, GOLD, 0.045)
txt(cover, 5.26, 0.92, 4.95, 1.00,
    [("Digitalisasi", 27, True, NAVY),
     ("Daily Monitoring System", 27, True, NAVY)], spacing=1.06)
txt(cover, 5.26, 1.96, 4.92, 0.34,
    [("Sistem yang mencatat, menghitung, dan mengingatkan — bukan tim", 11, None, TEAL)],
    spacing=1.15)
txt(cover, 5.26, 2.30, 4.92, 0.26,
    [("Berlaku untuk Plant Snack, Exist Plant, New Plant, dan Dairy", 9.5, None, GREY)])
txt(cover, 5.26, 2.62, 4.92, 0.26,
    [(f"Dasar angka: {n(TOT['total_kasus'])} kasus dari 3 workbook DMS", 9.5, True, NAVY)])

txt(cover, 10.68, 1.74, 2.42, 1.72,
    [("NOVEMBER", 9.5, True, GOLD),
     ("2026", 27, True, NAVY),
     ("Tim Daily Monitoring System", 8.5, None, GREY),
     ("Group Manufacturing", 8.5, None, GREY)], spacing=1.12, anchor=MSO_ANCHOR.MIDDLE)


# ================================================================ 2 · BEBAN MANUAL
s = page("Hari ini banyak pekerjaan rutin masih dikerjakan tangan",
         "Bagian 1 · kondisi hari ini",
         note="Sumber: workbook DMS Snack, Exist Plant, New Plant · sheet Resume SHE, QC, Prod")
kpi_cards(s, [(n(TOT["total_kasus"]), "baris kasus", "3 workbook · 9 sheet", NAVY),
              (n(TOT["close_tanpa_sebab"]), "close tanpa sebab",
               pc(100 * TOT["close_tanpa_sebab"] / TOT["total_kasus"], 1) + " dari total", GOLD),
              (n(TOT["pola_3x"]), "pola berulang ≥3×",
               f"{n(TOT['kasus_dalam_pola'])} kasus di dalamnya", GOLD),
              (n(TOT["overdue"]), "kasus lewat tenggat", "tertua 1.182 hari", RED)])

label(s, 0.62, 2.44, "KASUS PER PLANT DAN PER SHEET", 6.2)
chart(s, 0.52, 2.60, 5.80, 2.06,
      ["Snack", "Exist Plant", "New Plant"],
      [("SHE", [SN["SHE"]["kasus"], EP["SHE"]["kasus"], NP["SHE"]["kasus"]]),
       ("QC", [SN["QC"]["kasus"], EP["QC"]["kasus"], NP["QC"]["kasus"]]),
       ("Prod", [SN["Prod"]["kasus"], EP["Prod"]["kasus"], NP["Prod"]["kasus"]])],
      XL_CHART_TYPE.COLUMN_STACKED, [GOLD, TEAL, NAVY], number_format="#,##0",
      legend=True, fs=8.5, gap=70, label_pos=XL_LABEL_POSITION.CENTER, label_color=WHITE,
      vmax=7000)

label(s, 6.62, 2.44, "PEKERJAAN YANG DIKERJAKAN MANUAL", 6.0)
manual = [("Rekap dari papan dan kertas", "setiap hari, per line, per shift", NAVY),
          ("Memindahkan angka ke beberapa file", "satu kejadian disalin 2–3 kali", NAVY),
          ("Menghitung nilai sendiri", "hasil tiap orang bisa berbeda", GOLD),
          ("Menyusun bahan rapat pagi", "dicari ulang dari sheet berbeda", GOLD),
          ("Menagih tindak lanjut", "lewat pesan pribadi, mudah terlewat", RED)]
y = 2.66
for head_, sub, col in manual:
    box(s, 6.62, y, 5.86, 0.36, fill=SOFT, line=RULE, radius=0.05)
    box(s, 6.62, y, 0.06, 0.36, fill=col, line=None, radius=0.5)
    txt(s, 6.80, y + 0.05, 3.30, 0.26, [(head_, 9.5, True, INK)])
    txt(s, 10.10, y + 0.07, 2.26, 0.24, [(sub, 8.5, None, GREY)])
    y += 0.40

band = [("Beban manual terbesar",
         f"{n(TOT['total_kasus'])} baris tersebar di 9 sheet; setiap rekap harus dibaca ulang per sheet.", NAVY),
        ("Yang paling mahal",
         f"{n(TOT['close_tanpa_sebab'])} kasus berstatus Close tanpa sebab dan {n(TOT['overdue'])} kasus lewat tenggat.", GOLD),
        ("Yang dibutuhkan",
         "Sistem yang mencatat sekali, menghitung sendiri, dan mengingatkan tanpa menambah kerja tim.", TEAL)]
x = 0.62
for head_, body, col in band:
    box(s, x, 4.90, 3.95, 1.54, fill=SOFT, line=RULE, radius=0.05)
    hline(s, x + 0.01, 4.90, 3.93, col, 0.06)
    txt(s, x + 0.20, 5.06, 3.58, 0.26, [(head_.upper(), 10, True, col)])
    txt(s, x + 0.20, 5.38, 3.58, 0.94, [(body, 10, None, INK)], spacing=1.26)
    x += 4.07


# ================================================================ 3 · ALUR MANUAL VS SISTEM
s = page("Alur kerja berubah: dari lima langkah tangan ke satu input",
         "Bagian 2 · diagram alir",
         note="Perbandingan putaran harian sekarang dan setelah sistem dipakai")

SW, SG = 2.10, 0.37
xs = [0.62 + i * (SW + SG) for i in range(5)]

label(s, 0.62, 1.24, "ALUR SEKARANG · DIKERJAKAN TANGAN", 7.0)
now = [("Tulis di papan", "leader mencatat manual"),
       ("Rekap ke Excel", "disalin per shift"),
       ("Hitung sendiri", "hasil bisa berbeda"),
       ("Kirim grup WA", "format tidak seragam"),
       ("Rapat & tindak lanjut", "tidak tercatat siapa-kapan")]
for i, (head_, body) in enumerate(now):
    box(s, xs[i], 1.52, SW, 1.32, fill=WHITE, line=RGBColor(0xD9, 0xBE, 0xBE), radius=0.05)
    box(s, xs[i], 1.52, SW, 0.06, fill=RED, line=None, radius=None)
    txt(s, xs[i] + 0.14, 1.68, SW - 0.28, 0.28, [(head_, 10.5, True, INK)])
    txt(s, xs[i] + 0.14, 2.00, SW - 0.28, 0.76, [(body, 8.5, None, GREY)], spacing=1.15)
    if i < 4:
        arrow(s, xs[i] + SW + 0.05, 2.06, SG - 0.10, 0.26, "right", RGBColor(0xE6, 0xD3, 0xD3))

txt(s, 0.62, 3.24, 12.09, 0.26,
    [("setiap langkah manual digantikan satu langkah sistem", 9, True, GOLD)])
sysm = [("Isi satu form", "sekali, per item checklist"),
        ("Sistem periksa", "kolom kurang ditolak"),
        ("Sistem simpan & olah", "angka langsung jadi"),
        ("Tayang otomatis", "dasbor L1–L3 dan TV"),
        ("Sistem menagih", "pengingat sampai ditutup")]
for i, (head_, body) in enumerate(sysm):
    box(s, xs[i], 3.56, SW, 1.32, fill=WHITE, line=RGBColor(0xBF, 0xD8, 0xD9), radius=0.05)
    box(s, xs[i], 3.56, SW, 0.06, fill=TEAL, line=None, radius=None)
    txt(s, xs[i] + 0.14, 3.72, SW - 0.28, 0.28, [(head_, 10.5, True, NAVY)])
    txt(s, xs[i] + 0.14, 4.04, SW - 0.28, 0.76, [(body, 8.5, None, GREY)], spacing=1.15)
    if i < 4:
        arrow(s, xs[i] + SW + 0.05, 4.10, SG - 0.10, 0.26, "right", RGBColor(0xC9, 0xDE, 0xDF))

# panah pembanding per langkah
for i in range(5):
    arrow(s, xs[i] + SW / 2 - 0.13, 2.90, 0.26, 0.30, "down", GOLD)

label(s, 0.62, 5.10, "YANG BERUBAH BAGI TIM", 11.0)
gains = [("Kerja jadi sekali", "input sehari sekali, tidak ada rekap ulang", TEAL),
         ("Angka tidak berselisih", "semua layar membaca catatan yang sama", NAVY),
         ("Tidak ada yang tertinggal", "sistem yang mengingatkan, bukan orang", GOLD)]
x = 0.62
for head_, body, col in gains:
    box(s, x, 5.40, 3.95, 0.86, fill=SOFT, line=RULE, radius=0.05)
    box(s, x, 5.40, 0.06, 0.86, fill=col, line=None, radius=0.5)
    txt(s, x + 0.18, 5.48, 3.60, 0.24, [(head_, 9.5, True, col)])
    txt(s, x + 0.18, 5.74, 3.60, 0.44, [(body, 8.5, None, GREY)], spacing=1.15)
    x += 4.07

txt(s, 0.62, 6.30, 12.09, 0.50,
    [("Yang tidak berubah  ·  keputusan tetap di manusia: plant head menetapkan prioritas, "
      "DH menyetujui penutupan kasus, Admin menetapkan target plant.", 9.5, None, GREY)], spacing=1.2)


# ================================================================ 4 · TABEL AMBIL ALIH
s = page("Sepuluh pekerjaan manual yang diambil alih sistem",
         "Bagian 2 · peran sistem",
         note="Kolom terakhir menunjukkan apa yang berhenti dikerjakan tim")
table(s, [
    ["Pekerjaan manual sekarang", "Siapa", "Yang dilakukan sistem", "Yang berhenti dikerjakan"],
    ["Rekap harian dari papan dan kertas", "Leader line",
     "Form harian tersimpan per item, per line, per tanggal", "Menyalin ke buku rekap"],
    ["Memindahkan angka ke file lain", "Admin plant",
     "Satu catatan dipakai semua laporan dan layar", "Copy–paste antar file"],
    ["Menghitung nilai harian", "Leader & DH",
     "Nilai dihitung saat data disimpan, bukan diketik", "Menghitung dengan kalkulator"],
    ["Mencari kolom yang belum diisi", "Supervisor",
     "Kolom wajib diperiksa sebelum data boleh dikirim", "Menyisir kolom satu per satu"],
    ["Menyusun bahan rapat pagi", "Supervisor",
     "Kartu temuan tersusun otomatis, urut dampak", "Menyiapkan slide/printout"],
    ["Menagih tindak lanjut", "DH / plant head",
     "Pengingat berjalan sampai kasus ditutup dan disetujui", "Menelepon dan chat pribadi"],
    ["Menebak masalah berulang", "Plant head",
     "Pola berulang dikenali, saran tindakan pencegahan disiapkan", "Menandai manual di kolom"],
    ["Mengumpulkan angka antar plant", "Group",
     "Dasbor membandingkan plant dengan definisi sama", "Menggabung sheet manual"],
    ["Mencari riwayat perubahan angka", "Audit / DH",
     "Setiap perubahan tercatat: siapa, kapan, sebelum–sesudah", "Menanyakan siapa yang mengubah"],
    ["Menyusun laporan bulanan", "Admin plant",
     "Laporan tersedia dari data yang sama, siap diunduh", "Merangkum ulang tiap bulan"],
], [3.45, 1.45, 4.10, 3.09], 0.62, 1.24, row_h=0.47, head_h=0.40, fs=9.5, head_fs=10,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT], bold_first=False)

box(s, 0.62, 6.06, 12.09, 0.62, fill=SOFT, line=RULE, radius=0.05)
txt(s, 0.82, 6.16, 11.70, 0.44,
    [("Cara membaca  ·  kolom kanan adalah pekerjaan yang hilang dari rutinitas tim, "
      "bukan sekadar dipindahkan ke aplikasi.", 9.5, None, GREY)], spacing=1.2)


# ================================================================ 5 · ALUR HARIAN
s = page("Alur harian: enam langkah dalam satu putaran",
         "Bagian 2 · diagram alir",
         note="Putaran Senin–Jumat; data hari libur tetap tersimpan sebagai arsip")
W, GAP, H = 3.44, 0.60, 1.64
X1 = 0.62
X2 = X1 + W + GAP
X3 = X2 + W + GAP
TOPY, BOTY = 1.54, 3.74

step(s, X1, TOPY, W, H, 1, "Input harian",
     "Leader line mengisi checklist per item untuk hari berjalan.", NAVY)
arrow(s, X1 + W + 0.14, TOPY + H / 2 - 0.17, GAP - 0.28, 0.34, "right", PALE)
step(s, X2, TOPY, W, H, 2, "Pemeriksaan otomatis",
     "Item yang belum lengkap ditolak sistem sebelum dikirim.", NAVY)
arrow(s, X2 + W + 0.14, TOPY + H / 2 - 0.17, GAP - 0.28, 0.34, "right", PALE)
step(s, X3, TOPY, W, H, 3, "Angka langsung jadi",
     "Nilai harian dan capaian dihitung sistem saat data disimpan.", TEAL)

arrow(s, X3 + W / 2 - 0.17, TOPY + H + 0.08, 0.34, 0.40, "down", PALE)

step(s, X3, BOTY, W, H, 4, "Tampil di kanal",
     "Dasbor L1–L3 dan layar TV membaca catatan yang sama.", TEAL)
arrow(s, X3 - GAP + 0.14, BOTY + H / 2 - 0.17, GAP - 0.28, 0.34, "left", PALE)
step(s, X2, BOTY, W, H, 5, "Temuan & pengingat",
     "Sistem memilih temuan dan menetapkan pemilik serta tenggat.", GOLD)
arrow(s, X2 - GAP + 0.14, BOTY + H / 2 - 0.17, GAP - 0.28, 0.34, "left", PALE)
step(s, X1, BOTY, W, H, 6, "Tindak lanjut",
     "Kasus ditutup setelah sebab, tindakan, bukti, dan PIC lengkap.", GOLD)

box(s, X1 + W / 2 - 0.01, BOTY + H + 0.06, 0.02, 0.18, fill=PALE, line=None, radius=None)
box(s, X1 + W / 2 - 0.01, BOTY + H + 0.22, 8.56, 0.02, fill=PALE, line=None, radius=None)
txt(s, X1 + W / 2 + 0.20, 5.44, 8.30, 0.26,
    [("Data tersimpan otomatis; putaran berikutnya mulai lagi dari langkah 1", 9.5, None, LGREY)])

legend = [("Leader line", "mengisi form harian per item checklist", NAVY),
          ("DH & supervisor", "memverifikasi, menetapkan pemilik dan tenggat", TEAL),
          ("Admin plant", "mengunci periode, mengatur target dan layar TV", GOLD)]
x = 0.62
for head_, body, col in legend:
    box(s, x, 5.86, 3.95, 0.92, fill=SOFT, line=RULE, radius=0.05)
    box(s, x + 0.18, 6.02, 0.12, 0.12, fill=col, radius=0.3)
    txt(s, x + 0.40, 5.96, 3.40, 0.24, [(head_, 10, True, NAVY)])
    txt(s, x + 0.40, 6.24, 3.40, 0.44, [(body, 9, None, GREY)], spacing=1.18)
    x += 4.07


# ================================================================ 6 · GERBANG PENUTUPAN
s = page("Kasus tidak bisa ditutup sebelum buktinya lengkap",
         "Bagian 2 · peran sistem",
         note="Sistem menahan penutupan, bukan mengandalkan kedisiplinan pengisian")

CX, CW = 4.86, 3.70
box(s, CX, 1.34, CW, 0.60, fill=NAVY, line=None, radius=0.05)
txt(s, CX, 1.40, CW, 0.48, [("Kasus terbuka · defect · downtime · audit", 10, True, WHITE)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
arrow(s, CX + CW / 2 - 0.17, 1.96, 0.34, 0.22, "down", PALE)

box(s, CX, 2.18, CW, 0.76, fill=WHITE, line=RULE, radius=0.05)
txt(s, CX + 0.18, 2.26, CW - 0.36, 0.60,
    [("Isi sebab · tindakan · bukti · PIC", 10.5, True, NAVY),
     ("satu foto atau dokumen wajib dilampirkan", 9, None, GREY)], spacing=1.18)
arrow(s, CX + CW / 2 - 0.17, 2.96, 0.34, 0.20, "down", PALE)

shape(s, MSO_SHAPE.DIAMOND, CX + 0.30, 3.16, CW - 0.60, 1.04,
      fill=RGBColor(0xF7, 0xF1, 0xDD), line=GOLD, lw=1.25)
txt(s, CX + 0.56, 3.40, CW - 1.12, 0.56,
    [("Sistem menyatakan lengkap?", 10, True, NAVY)], align=PP_ALIGN.CENTER,
    anchor=MSO_ANCHOR.MIDDLE)

arrow(s, CX - 0.50, 3.52, 0.44, 0.32, "left", GOLD)
txt(s, 1.52, 3.28, 2.10, 0.24, [("Belum", 9, True, GOLD)], align=PP_ALIGN.CENTER)
box(s, 0.62, 3.84, 3.30, 0.94, fill=WHITE, line=GOLD, radius=0.05)
txt(s, 0.82, 3.94, 2.94, 0.76,
    [("Kembali ke PIC", 10.5, True, NAVY),
     ("umur kasus bertambah dan kartunya tetap tampil di layar TV", 9, None, GREY)], spacing=1.2)

arrow(s, CX + CW / 2 - 0.17, 4.22, 0.34, 0.20, "down", TEAL)
txt(s, CX + CW / 2 + 0.24, 4.18, 0.80, 0.24, [("Ya", 9, True, TEAL)])

box(s, CX, 4.44, CW, 0.60, fill=WHITE, line=RULE, radius=0.05)
txt(s, CX, 4.50, CW, 0.48, [("Persetujuan DH / Plant Head di layar", 10.5, True, NAVY)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
arrow(s, CX + CW / 2 - 0.17, 5.06, 0.34, 0.20, "down", PALE)

shape(s, MSO_SHAPE.DIAMOND, CX + 0.82, 5.28, CW - 1.64, 0.86,
      fill=RGBColor(0xE8, 0xF3, 0xF4), line=TEAL, lw=1.25)
txt(s, CX + 1.02, 5.42, CW - 2.04, 0.56, [("Disetujui?", 10, True, NAVY)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

arrow(s, CX + CW + 0.02, 5.56, 0.34, 0.30, "right", GOLD)
box(s, 8.94, 5.30, 3.78, 0.86, fill=WHITE, line=GOLD, radius=0.05)
txt(s, 9.12, 5.40, 3.44, 0.70,
    [("Dikembalikan untuk revisi", 10, True, NAVY),
     ("kasus tetap terbuka dan tetap dihitung dalam umur kasus", 9, None, GREY)], spacing=1.18)
txt(s, 9.02, 6.22, 3.60, 0.24, [("Tidak", 9, True, GOLD)])

arrow(s, CX + CW / 2 - 0.17, 6.16, 0.34, 0.18, "down", TEAL)
box(s, CX - 0.40, 6.38, CW + 0.80, 0.48, fill=TEAL, line=None, radius=0.05)
txt(s, CX - 0.40, 6.44, CW + 0.80, 0.36,
    [("Kasus ditutup, periode dikunci", 10, True, WHITE)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

label(s, 9.00, 1.30, "KENAPA SISTEM YANG MENAHAN", 3.60)
gates = [(n(TOT["close_tanpa_sebab"]), "kasus berstatus Close tanpa sebab di tiga workbook"),
         ("0%", "due date terisi pada sheet SHE — tidak ada yang menagih"),
         (n(TOT["overdue"]), "kasus melewati tenggat, tertua 1.182 hari")]
y = 1.62
for v, body in gates:
    txt(s, 9.00, y, 1.35, 0.34, [(v, 15, True, NAVY)])
    txt(s, 10.40, y + 0.02, 2.30, 0.62, [(body, 9, None, GREY)], spacing=1.18)
    y += 0.74

box(s, 9.00, 3.94, 3.60, 1.30, fill=SOFT, line=RULE, radius=0.05)
txt(s, 9.18, 4.06, 3.24, 0.24, [("JEJAK AUDIT", 9, True, GOLD)])
txt(s, 9.18, 4.32, 3.24, 0.84,
    [("Sistem mencatat siapa mengubah apa dan kapan, sehingga penutupan kasus bisa "
      "dipertanggungjawabkan tanpa menelusuri siapa yang mengisi.", 9, None, GREY)], spacing=1.2)


# ================================================================ 7 · SATU SUMBER ANGKA
s = page("Satu catatan dipakai semua layar, tanpa rekap ulang",
         "Bagian 3 · peran sistem",
         note="Dibandingkan: angka ringkasan di dalam sheet versus jumlah baris kasus")
label(s, 0.62, 1.26, "ANGKA RINGKASAN SHEET VS BARIS KASUS", 6.6)
chart(s, 0.52, 1.44, 7.10, 2.66,
      ["QC Snack", "QC Exist", "QC New", "Prod Snack", "Prod Exist", "Prod New"],
      [("Ringkasan sheet", [SN["QC"]["ringkasan_sheet"].get("TOTAL", 0), EP["QC"]["ringkasan_sheet"].get("TOTAL", 0),
                            NP["QC"]["ringkasan_sheet"].get("TOTAL", 0), SN["Prod"]["ringkasan_sheet"].get("TOTAL", 0),
                            EP["Prod"]["ringkasan_sheet"].get("TOTAL", 0), NP["Prod"]["ringkasan_sheet"].get("TOTAL", 0)]),
       ("Baris kasus", [SN["QC"]["kasus"], EP["QC"]["kasus"], NP["QC"]["kasus"],
                        SN["Prod"]["kasus"], EP["Prod"]["kasus"], NP["Prod"]["kasus"]])],
      XL_CHART_TYPE.COLUMN_CLUSTERED, [PALE, NAVY], number_format="#,##0",
      legend=True, fs=8, gap=55, label_pos=XL_LABEL_POSITION.OUTSIDE_END, vmax=3600)
txt(s, 0.62, 4.16, 7.00, 0.28,
    [("Selisih terbesar di Exist Plant: ringkasan QC 993, tabel kasus 2.338 baris.",
      9, None, GREY)])

table(s, [
    ["Plant", "QC ringkasan", "QC tabel", "Prod ringkasan", "Prod tabel"],
    ["Snack", n(SN["QC"]["ringkasan_sheet"].get("TOTAL", 0)), n(SN["QC"]["kasus"]),
     n(SN["Prod"]["ringkasan_sheet"].get("TOTAL", 0)), n(SN["Prod"]["kasus"])],
    ["Exist Plant", n(EP["QC"]["ringkasan_sheet"].get("TOTAL", 0)), n(EP["QC"]["kasus"]),
     n(EP["Prod"]["ringkasan_sheet"].get("TOTAL", 0)), n(EP["Prod"]["kasus"])],
    ["New Plant", n(NP["QC"]["ringkasan_sheet"].get("TOTAL", 0)), n(NP["QC"]["kasus"]),
     n(NP["Prod"]["ringkasan_sheet"].get("TOTAL", 0)), n(NP["Prod"]["kasus"])],
], [1.30, 0.95, 0.85, 0.95, 0.85], 8.00, 1.44, row_h=0.40, fs=9.5, bold_first=True,
    aligns=[PP_ALIGN.LEFT] + [PP_ALIGN.RIGHT] * 4)

box(s, 8.00, 3.56, 4.71, 1.28, fill=SOFT, line=RULE, radius=0.05)
txt(s, 8.18, 3.66, 4.35, 0.24, [("YANG DILAKUKAN SISTEM", 9, True, GOLD)])
txt(s, 8.18, 3.92, 4.35, 0.86,
    [("Satu catatan kasus, satu angka.", 9.5, True, NAVY),
     ("Laporan, dasbor, dan layar TV membaca catatan yang sama — tidak ada sel ringkasan "
      "yang perlu dihitung ulang.", 9, None, GREY)], spacing=1.22)

label(s, 0.62, 4.92, "KEBIASAAN MANUAL YANG IKUT HILANG", 12.0)
pola = [("Ringkasan tanpa tanggal", "blok ringkasan tidak menyimpan periode, jadi tidak bisa dibandingkan antar pekan.", GOLD),
        ("Nilai satu blok 0,6", "Exist Plant punya blok 0,6 sementara blok lain 3,0 — akibat salin manual.", RED),
        ("Kolom PIC berisi tautan foto", "di SHE Exist Plant, kolom PIC memuat URL SharePoint, bukan nama orang.", RED),
        ("Nama line tidak seragam", "ws l02 / WS L02 / Line 2 hidup berdampingan di plant yang sama.", GOLD)]
x = 0.62
for head_, body, col in pola:
    box(s, x, 5.20, 2.95, 1.40, fill=SOFT, line=RULE, radius=0.05)
    txt(s, x + 0.16, 5.30, 2.62, 0.46, [(head_, 9.5, True, col)], spacing=1.1)
    txt(s, x + 0.16, 5.78, 2.62, 0.74, [(body, 8.5, None, GREY)], spacing=1.18)
    x += 3.04


# ================================================================ 8 · MUTU DATA
s = page("Data yang belum lengkap ditandai sistem, bukan dicari manual",
         "Bagian 3 · data",
         note="Sumber: Resume SHE, QC, Prod pada tiga workbook; downtime dari kolom DT (min)")
label(s, 0.62, 1.26, "SEBAB TERISI PER SHEET DAN PLANT (%)", 7.0)
chart(s, 0.52, 1.44, 7.30, 2.64,
      ["Resume SHE", "Resume QC", "Resume Prod"],
      [("Snack", [SN["SHE"]["root_cause_pct"], SN["QC"]["root_cause_pct"], SN["Prod"]["root_cause_pct"]]),
       ("Exist Plant", [EP["SHE"]["root_cause_pct"], EP["QC"]["root_cause_pct"], EP["Prod"]["root_cause_pct"]]),
       ("New Plant", [NP["SHE"]["root_cause_pct"], NP["QC"]["root_cause_pct"], NP["Prod"]["root_cause_pct"]])],
      XL_CHART_TYPE.COLUMN_CLUSTERED, [PALE, TEAL, NAVY], number_format='0"%"',
      legend=True, fs=8.5, gap=60, label_pos=XL_LABEL_POSITION.OUTSIDE_END, vmax=115)
txt(s, 0.62, 4.14, 7.20, 0.28,
    [("Sheet SHE paling rendah di tiga plant (52–57%); New Plant tertinggi di QC dan Produksi.",
      9, None, GREY)])

label(s, 8.02, 1.26, "DOWNTIME TERCATAT (MENIT)", 4.6)
chart(s, 7.92, 1.44, 4.84, 2.64,
      ["Snack", "Exist Plant", "New Plant"],
      [("Menit", [SN["Prod"]["dt_total"], EP["Prod"]["dt_total"], NP["Prod"]["dt_total"]])],
      XL_CHART_TYPE.BAR_CLUSTERED, [NAVY], number_format="#,##0",
      fs=9, gap=65, label_pos=XL_LABEL_POSITION.OUTSIDE_END, vmax=260000)
txt(s, 8.02, 4.14, 4.60, 0.28,
    [("Total 508.226 menit atau 8.470 jam mesin; median 50–60 menit per kasus.", 9, None, GREY)])

label(s, 0.62, 4.56, "EMPAT HAL YANG DIAMBIL ALIH SISTEM DARI PENERIKSAAN MANUAL", 12.0)
findings = [(n(TOT["close_tanpa_sebab"]), "Kasus Close tanpa sebab — sistem menolak menutup tanpa sebab terisi.", GOLD),
            ("0%", "Due date di sheet SHE — sistem mewajibkan tenggat sebelum kasus berjalan.", RED),
            (n(TOT["error_sel_total"]), "Sel error di sheet — sistem tidak menyimpan rumus di sel bebas.", RED),
            (n(TOT["pola_3x"]), "Pola berulang — sistem mengenali dan mengusulkan tindakan pencegahan.", TEAL)]
x = 0.62
for v, body, col in findings:
    box(s, x, 4.86, 2.95, 1.50, fill=SOFT, line=RULE, radius=0.05)
    box(s, x, 4.86, 2.95, 0.06, fill=col, line=None, radius=None)
    txt(s, x + 0.18, 5.00, 2.60, 0.40, [(v, 20, True, col)])
    txt(s, x + 0.18, 5.44, 2.60, 0.82, [(body, 9, None, GREY)], spacing=1.2)
    x += 3.04


# ================================================================ 9 · INSIGHT
s = page("Sistem memilih temuan dan mengingatkan pemiliknya",
         "Bagian 4 · peran sistem",
         note="Setiap temuan membawa bukti, sebab, dampak, rekomendasi, dan pemilik")
table(s, [
    ["Kode", "Yang dipantau sistem", "Contoh keluaran (tiga workbook)", "Kanal"],
    ["I-01", "Hari kerja tanpa pertemuan", "Line tidak DMS 3 hari berturut", "L1 · TV"],
    ["I-02", "Kasus lewat tenggat", f"{n(TOT['overdue'])} kasus; tertua 1.182 hari", "TV · L1"],
    ["I-03", "Masalah sama berulang", "WS L04 P02 BCT 134× di Exist Plant", "TV · L2"],
    ["I-04", "Berulang dengan sebab identik", "Correction sama 4× → Preventive", "L2"],
    ["I-05", "Tutup tanpa standar pencegahan", "88–98% kasus belum distandarkan", "L2 · L3"],
    ["I-06", "Tutup tanpa sebab atau bukti", f"{n(TOT['close_tanpa_sebab'])} kasus (18,7%)", "Admin"],
    ["I-07", "Prioritas tidak membedakan", "High 100% di ketiga plant", "Admin"],
    ["I-08", "Nilai mendekati batas", "rawan selisih antar pencatat", "Admin"],
    ["I-09", "Tiga periode menurun", "checklist turun 4% per pekan", "L2 · L3"],
    ["I-10", "Satu line menumpuk kasus", "Snack line 9 = 96,9% · Exist WS L02 = 22,6%", "L3"],
    ["I-11", "Downtime besar dan sering", "508.226 menit; median 50–60 menit/kasus", "L2"],
    ["I-12", "Tindakan perbaikan lemah", "prediksi lonjakan pekan depan", "L3"],
], [0.70, 2.86, 3.96, 1.18], 0.62, 1.24, row_h=0.355, head_h=0.34, fs=9,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER])

txt(s, 0.62, 6.10, 8.30, 0.70,
    [("Temuan diurutkan dari dampak terbesar, bukan dari siapa yang mengirim lebih dulu.",
      10, True, NAVY),
     ("Maksimal tiga kartu tampil di layar lantai; sisanya di dasbor supervisor dan admin.",
      9.5, None, GREY)], spacing=1.3)

img_slot(s, 10.06, 1.24, 2.64, 2.10, "Mockup 3 kartu TV",
         "satu kartu = satu temuan + pemilik + tenggat")

box(s, 10.06, 3.50, 2.64, 2.36, fill=SOFT, line=RULE, radius=0.05)
txt(s, 10.24, 3.64, 2.28, 0.24, [("CARA MEMBACA TABEL", 9, True, GOLD)])
txt(s, 10.24, 3.92, 2.28, 1.86,
    [("Kanal menunjukkan siapa penerima kartu: layar lantai, dasbor L1, L2, atau L3.", 9, None, GREY),
     ("Satu kartu memuat satu temuan, bukan satu daftar.", 9, None, GREY),
     ("Angka pemicu memakai tiga workbook: 53, 3.220, 134×, 508.226 menit.", 9, None, GREY)],
    spacing=1.25)


# ================================================================ 10 · KANAL
s = page("Empat kanal tampilan dan batasannya", "Bagian 5 · tampilan",
         note="Struktur final; gambar antarmuka menyusul")
cards = [("Form harian", "Leader & DH", "satu layar, di bawah 5 menit",
          "Isi harian per line: item checklist, status, sebab bila di bawah target.", NAVY),
         ("Dasbor L1–L3", "Supervisor, plant head", "tiga tingkat audiens",
          "L1 memantau hari ini, L2 menutup kasus, L3 membandingkan plant.", TEAL),
         ("Layar lantai (TV)", "Area produksi", "tanpa interaksi, rotasi 30 detik",
          "Kartu temuan terbuka: sebab, PIC, tenggat hitung mundur, foto bukti.", TEAL),
         ("Halaman admin", "Admin plant & group", "persetujuan, konfigurasi, audit",
          "Kelola pengguna, target plant, layar TV, dan periode yang dikunci.", GOLD)]
x = 0.62
for name, who, desc, body, col in cards:
    box(s, x, 1.24, 2.95, 1.96, fill=WHITE, line=RULE, radius=0.05)
    hline(s, x + 0.01, 1.24, 2.93, col, 0.06)
    txt(s, x + 0.18, 1.42, 2.60, 0.26, [(name.upper(), 11, True, NAVY)])
    txt(s, x + 0.18, 1.72, 2.60, 0.24, [(who, 9, None, GREY)])
    txt(s, x + 0.18, 1.98, 2.60, 0.26, [(desc, 9, True, col)])
    txt(s, x + 0.18, 2.28, 2.60, 0.82, [(body, 9, None, INK)], spacing=1.22)
    x += 3.04

table(s, [
    ["Aturan tetap", "Isi"],
    ["Dua peran", "User dan Admin; layar TV tidak punya login"],
    ["Satu sumber angka", "Semua kanal membaca dari catatan yang sama"],
    ["Empat kolom wajib", "Sebab, tindakan, bukti, dan PIC sebelum kasus ditutup"],
    ["Kunci periode", "Periode yang sudah dilaporkan tidak dapat diubah"],
    ["Jejak audit", "Setiap perubahan tercatat: siapa, kapan, sebelum–sesudah"],
], [2.25, 6.35], 0.62, 3.42, row_h=0.42, head_h=0.36, fs=10, bold_first=True)

img_slot(s, 9.90, 3.42, 2.80, 1.92, "Mockup layar TV", "tangkapan layar atau desain akhir")

label(s, 0.62, 5.94, "YANG TIDAK DIBUAT SEKARANG", 9.30)
box(s, 0.62, 6.22, 9.30, 0.66, fill=SOFT, line=RULE, radius=0.05)
notes = [("Tanpa aplikasi mobile", "form harian berbasis web pada fase 1"),
         ("Tanpa login TV", "layar lantai hanya menampilkan"),
         ("Tanpa angka manual", "isian manual hanya Healthy Check")]
x = 0.80
for head_, body in notes:
    txt(s, x, 6.30, 2.85, 0.22, [(head_, 9, True, NAVY)])
    txt(s, x, 6.52, 2.85, 0.24, [(body, 8.5, None, GREY)])
    x += 3.02


# ================================================================ 11 · RENCANA
s = page("Rencana 8 pekan: rapikan data dulu, tampilan terakhir",
         "Bagian 5 · rencana",
         note="Mulai Snack, lalu Exist Plant dan New Plant; Dairy menyusul dengan pola yang sama")

phases = [("0 · Fondasi", 1, 2, "master line & mesin, hak akses", NAVY),
          ("1 · Capture", 1, 3, "form harian dan form kasus", NAVY),
          ("2 · Measure", 3, 5, "angka otomatis dan dasbor line", TEAL),
          ("3 · Insight", 5, 6, "delapan aturan pertama aktif", TEAL),
          ("4 · Display", 7, 7, "layar lantai satu area", GOLD),
          ("5 · Analitik", 7, 8, "dasbor plant dan ekspor", GOLD)]
gx, gw = 2.86, 7.60
for wk in range(9):
    hline(s, gx + gw * wk / 8, 1.60, 0.009, RGBColor(0xE3, 0xE7, 0xEE), 1.98)
    if wk < 8:
        txt(s, gx + gw * wk / 8 + gw / 16 - 0.20, 1.26, 0.40, 0.24,
            [(f"P{wk + 1}", 9, True, LGREY)], align=PP_ALIGN.CENTER)
txt(s, gx + gw / 2 - 0.60, 1.00, 1.20, 0.24, [("PEKAN PELAKSANAAN", 9, True, GOLD)],
    align=PP_ALIGN.CENTER)
y = 1.62
for name, start, end, out, col in phases:
    txt(s, 0.62, y + 0.04, 2.10, 0.28, [(name, 10.5, True, NAVY)])
    box(s, gx + gw * (start - 1) / 8, y, gw * (end - start + 1) / 8 - 0.05, 0.34,
        fill=col, line=None, radius=0.04)
    txt(s, gx + gw * (start - 1) / 8 + 0.12, y + 0.07, 2.60, 0.24,
        [(f"pekan {start}–{end}", 8.5, True, WHITE)])
    txt(s, 10.62, y + 0.05, 2.12, 0.28, [(out, 8.5, None, GREY)], spacing=1.05)
    y += 0.46

label(s, 0.62, 4.46, "UKURAN KEBERHASILAN YANG DIPERIKSA PEKANAN", 12.0)
table(s, [
    ["Ukuran", "Kondisi hari ini (3 workbook)", "Target pekan ke-8", "Cara ukur"],
    ["Hari terisi tanpa diingatkan", "belum terukur", "≥ 90%", "hari terisi ÷ hari wajib"],
    ["Kasus dengan sebab lengkap", "SHE 52–57% · QC 79–98% · Prod 79–92%", "≥ 95%", "kolom sebab terisi"],
    ["Tenggat tercatat di sheet SHE", "0% di tiga plant", "≥ 95%", "kolom due date terisi"],
    ["Kasus lewat tenggat", f"{n(TOT['overdue'])} kasus", "turun 50%", "umur kasus > tenggat"],
    ["Pola berulang punya tindakan", f"{n(TOT['pola_3x'])} pola", "100%", "pola dengan tindakan tertutup"],
], [3.05, 3.75, 1.65, 3.64], 0.62, 4.66, row_h=0.34, head_h=0.32, fs=9.5, bold_first=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT])


# ================================================================ 12 · BAHAN GAMBAR
s = page("Daftar bahan gambar yang harus di-screenshot", "Bagian 5 · bahan",
         note="Dikumpulkan sebelum deck dipresentasikan; semua bersumber dari tiga workbook dan lantai")
table(s, [
    ["#", "Yang di-screenshot / difoto", "Diambil dari", "Halaman", "Sorotan"],
    ["1", "Papan monitoring line", "lantai produksi", "2, 3", "pencatatan tangan yang dipakai sekarang"],
    ["2", "Rekap Excel manual", "file rekap per shift", "2, 3", "kolom yang disalin berulang"],
    ["3", "Grup WhatsApp laporan harian", "WhatsApp / email group", "2, 3", "alur laporan sekarang"],
    ["4", "Sheet Resume SHE · tiga plant", "workbook Snack, EP, NP", "6, 8", "kolom due date & bukti kosong"],
    ["5", "Sheet Resume QC · tiga plant", "workbook Snack, EP, NP", "6, 8", "baris Close tanpa sebab"],
    ["6", "Sheet Resume Prod · tiga plant", "workbook Snack, EP, NP", "8", "kolom DT (min) dan sel #VALUE!"],
    ["7", "Blok STATUS PICA tiap sheet", "workbook · dalam sheet resume", "7", "angka ringkasan vs isi tabel"],
    ["8", "Sheet DMS_INDEX", "workbook · DMS_INDEX", "7", "blok 0,6 vs 3,0"],
    ["9", "Form checklist tercetak", "line · dokumen cetak", "3", "penilaian yang masih persepsi"],
    ["10", "Foto rapat pagi", "area meeting line", "5", "langkah 1–2 saat berjalan"],
    ["11", "Foto mesin / area", "Pilus L1, WS L04, WS L11", "8", "sumber downtime terbesar"],
    ["12", "Layar TV area produksi (bila ada)", "area produksi", "10", "pembanding tampilan baru"],
], [0.50, 3.30, 3.45, 1.25, 3.45], 0.62, 1.22, row_h=0.352, head_h=0.34, fs=9, head_fs=9.5,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT])

box(s, 0.62, 6.14, 12.09, 0.68, fill=SOFT, line=RULE, radius=0.05)
txt(s, 0.82, 6.24, 11.70, 0.50,
    [("Cara mengambil  ·  tampilkan nama sheet, header kolom, dan 5–10 baris contoh; blok kolom "
      "yang kosong agar terlihat. Foto lapangan landscape minimal 1600 px dan diberi tanggal.",
      9.5, None, GREY)], spacing=1.22)


# ================================================================ 13 · KEPUTUSAN
s = page("Keputusan yang diminta dan langkah berikutnya", "Penutup · keputusan",
         note="Semua keputusan mengacu pada angka tiga workbook; tidak ada tambahan asumsi baru")

label(s, 0.62, 1.26, "TIGA KEPUTUSAN TERBUKA", 4.15)
dec = [("1 · Kalender hari libur",
        "Daftar libur tahunan diisi sekali, atau per tanggal? Sistem memakainya untuk menentukan hari wajib."),
       ("2 · Item yang tidak relevan",
        "Item yang tidak berlaku di suatu line dikeluarkan, atau tetap dicatat sebagai nol?"),
       ("3 · Data historis tiga plant",
        "17.201 kasus dibawa sebagai arsip dengan penanda lama, atau mulai dari nol per plant?")]
y = 1.58
for name, q in dec:
    box(s, 0.62, y, 4.15, 0.98, fill=SOFT, line=RULE, radius=0.05)
    txt(s, 0.80, y + 0.10, 3.80, 0.24, [(name, 10.5, True, NAVY)])
    txt(s, 0.80, y + 0.38, 3.80, 0.54, [(q, 9, None, GREY)], spacing=1.2)
    y += 1.06

label(s, 5.02, 1.26, "ANGKA YANG MENJADI DASAR", 3.20)
nums = [(n(TOT["total_kasus"]), "kasus tiga plant", NAVY),
        (n(TOT["close_tanpa_sebab"]), "close tanpa sebab", GOLD),
        (n(TOT["pola_3x"]), "pola berulang ≥3×", GOLD),
        (n(TOT["overdue"]), "kasus lewat tenggat", RED),
        (n(TOT["error_sel_total"]), "sel error di sheet", RED)]
y = 1.58
for v, l, col in nums:
    txt(s, 5.02, y, 1.35, 0.32, [(v, 16, True, col)])
    txt(s, 6.40, y + 0.06, 1.85, 0.24, [(l, 9, None, GREY)])
    hline(s, 5.02, y + 0.36, 3.20, RULE)
    y += 0.48

label(s, 8.42, 1.26, "LANGKAH SETELAH SESI", 4.28)
box(s, 8.42, 1.58, 4.28, 3.02, fill=None, line=RULE, radius=0.05)
txt(s, 8.64, 1.74, 3.90, 2.74,
    [("1. Tiga keputusan di atas diputuskan pada rapat ini.", 9.5, None, INK),
     ("2. Bahan gambar halaman 12 dikumpulkan maksimal tiga hari kerja.", 9.5, None, INK),
     ("3. Pilot Snack, lalu Exist Plant dan New Plant dengan pola yang sama.", 9.5, None, INK),
     ("4. Evaluasi pekan ke-8 memakai lima ukuran keberhasilan.", 9.5, None, INK),
     ("5. Hasil keputusan dicatat pada berita acara dan disosialisasikan ke tiap plant.",
      9.5, None, INK)], spacing=1.5)

hline(s, 0.62, 4.90, 12.09, RULE)
bx = 0.62
for title_, name_, date_ in [("Disusun oleh", "Tim Daily Monitoring System", "Tanggal: ..............."),
                             ("Diperiksa oleh", "Plant Head / Dept Head", "Tanggal: ..............."),
                             ("Disetujui oleh", "Group Manufacturing", "Tanggal: ...............")]:
    box(s, bx, 5.06, 3.86, 1.40, fill=SOFT, line=RULE, radius=0.05)
    txt(s, bx + 0.20, 5.20, 3.46, 0.24, [(title_.upper(), 9.5, True, NAVY)])
    txt(s, bx + 0.20, 5.54, 3.46, 0.28, [(name_, 11, True, INK)])
    txt(s, bx + 0.20, 5.96, 3.46, 0.24, [(date_, 9, None, GREY)])
    bx += 4.11


# ================================================================ 14 · TERIMA KASIH
close = prs.slides.add_slide(CLOSE_L)
for ph in list(close.placeholders):
    ph._element.getparent().remove(ph._element)

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides._sldIdLst))
