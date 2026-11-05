#!/usr/bin/env python3
"""
Deck DMS memakai template_master.pptx (versi terbaru) DAN data tiga workbook:
Snack, Exist Plant, New Plant (angka dibaca dari docs/data_plants.json).

slide 1 template -> cover · slide 2 template -> halaman isi · slide 3 template -> penutup

Jalankan: python3 docs/analyze_workbook.py && python3 docs/make_mockups.py && python3 docs/build_deck.py
Hasil  : docs/DMS_Digitalisasi_v1.pptx

Template tidak disimpan di repo: taruh template_master.pptx di root sebelum build.
Foto papan dan ilustrasi layar sudah tersimpan di docs/assets/ (papan, mockup).
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


def img_strip(slide, x, y, w, h, caption, note):
    """Penyemat gambar bentuk strip (lebar, pendek) untuk potongan tabel/foto."""
    box(slide, x, y, w, h, fill=RGBColor(0xF8, 0xFA, 0xFD), line=RGBColor(0xBE, 0xC7, 0xD6), radius=0.04)
    box(slide, x + 0.10, y + h / 2 - 0.13, 0.26, 0.26, fill=WHITE, line=RGBColor(0xBE, 0xC7, 0xD6), radius=0.2)
    txt(slide, x + 0.10, y + h / 2 - 0.09, 0.26, 0.20, [("+", 10, True, LGREY)], align=PP_ALIGN.CENTER)
    txt(slide, x + 0.44, y + 0.06, w - 0.54, 0.20, [(caption.upper(), 8, True, LGREY)])
    txt(slide, x + 0.44, y + 0.26, w - 0.54, max(0.22, h - 0.32),
        [(note, 7.5, None, RGBColor(0xA9, 0xB2, 0xC0))], spacing=1.12)


def mock_papan(slide, x, y, w, h):
    """Ilustrasi papan monitoring line + buku rekap, menggantikan penyemat foto."""
    box(slide, x, y, w, h, fill=RGBColor(0xF7, 0xF8, 0xFB), line=RULE, radius=0.04)
    bw = w * 0.58
    box(slide, x + 0.14, y + 0.12, bw, h - 0.44, fill=RGBColor(0xE9, 0xF1, 0xEE),
        line=RGBColor(0xB6, 0xC6, 0xC0), radius=0.03)
    txt(slide, x + 0.20, y + 0.16, bw - 0.16, 0.14, [("PAPAN LINE 3", 6.6, True, RGBColor(0x46, 0x57, 0x52))])
    rows = ["Checklist A", "Checklist B", "Defect", "Downtime", "Output"]
    yy = y + 0.33
    for i, r in enumerate(rows):
        txt(slide, x + 0.20, yy, bw - 0.60, 0.13, [(r, 5.4, None, RGBColor(0x5C, 0x64, 0x72))])
        for k in range(3 + (i % 2)):
            box(slide, x + bw - 0.36 + k * 0.10, yy + 0.03, 0.06, 0.06,
                fill=None, line=GOLD, lw=0.7, radius=None)
        yy += 0.175
    box(slide, x + bw - 0.04, y + 0.12, 0.40, 0.34, fill=RGBColor(0xF6, 0xE2, 0xA4), line=None, radius=0.02)
    box(slide, x + bw - 0.04, y + 0.50, 0.40, 0.30, fill=RGBColor(0xD8, 0xE7, 0xD4), line=None, radius=0.02)

    bx = x + bw + 0.24
    bw2 = w - bw - 0.38
    box(slide, bx, y + 0.16, bw2, h - 0.48, fill=WHITE, line=RGBColor(0xC9, 0xD0, 0xDB), radius=0.02)
    box(slide, bx, y + 0.16, 0.05, h - 0.48, fill=NAVY, line=None, radius=None)
    txt(slide, bx + 0.12, y + 0.19, bw2 - 0.20, 0.13, [("BUKU REKAP", 6.2, True, GREY)])
    for i in range(6):
        hline(slide, bx + 0.12, y + 0.34 + i * 0.13, bw2 - 0.22, RGBColor(0xE1, 0xE6, 0xEE), 0.012)
    box(slide, bx + 0.10, y + 0.36, bw2 * 0.55, 0.06, fill=RGBColor(0xAE, 0xC2, 0xD8), line=None, radius=None)
    box(slide, bx + 0.10, y + 0.62, bw2 * 0.38, 0.06, fill=RGBColor(0xAE, 0xC2, 0xD8), line=None, radius=None)
    txt(slide, x + 0.14, y + h - 0.28, w - 0.28, 0.20,
        [("Ilustrasi  ·  satu kejadian dicatat di papan, lalu disalin ke buku rekap", 6.8, None, LGREY)])


def mock_excel(slide, x, y, w, h, rows, head="rekap_dms.xlsx · Sheet1"):
    """Potongan kecil spreadsheet rekap manual."""
    box(slide, x, y, w, h, fill=RGBColor(0xEE, 0xF1, 0xF6), line=RGBColor(0xC2, 0xCB, 0xD9), radius=0.04)
    box(slide, x + 0.06, y + 0.06, w - 0.12, 0.20, fill=RGBColor(0x21, 0x7A, 0x46), line=None, radius=None)
    txt(slide, x + 0.14, y + 0.07, w - 0.28, 0.16, [(head, 6.6, True, WHITE)])
    box(slide, x + 0.06, y + 0.24, w - 0.12, h - 0.30, fill=WHITE, line=None, radius=None)
    cols = ["Bulan", "Kasus", "Diisi tangan", "Selisih"]
    xs = [x + 0.12, x + 1.10, x + 1.95, x + 3.05]
    for c, cx in zip(cols, xs):
        txt(slide, cx, y + 0.28, 0.90, 0.14, [(c, 6.4, True, GREY)])
    hline(slide, x + 0.10, y + 0.41, w - 0.20, RGBColor(0xD5, 0xDA, 0xE3), 0.012)
    yy = y + 0.43
    for i, (bln, kasus, tgn, sel) in enumerate(rows):
        if i % 2:
            box(slide, x + 0.08, yy - 0.01, w - 0.16, 0.14, fill=RGBColor(0xF4, 0xF6, 0xFA), line=None, radius=None)
        txt(slide, xs[0], yy, 0.90, 0.14, [(bln, 6.6, None, INK)])
        txt(slide, xs[1], yy, 0.70, 0.14, [(kasus, 6.6, None, INK)])
        txt(slide, xs[2], yy, 0.95, 0.14, [(tgn, 6.6, None, GREY)])
        txt(slide, xs[3], yy, 0.60, 0.14, [(sel, 6.6, True, RED if sel != "0" else GREY)])
        yy += 0.145


def mock_ditolak(slide, x, y, w, h):
    """Ilustrasi layar penutupan kasus yang ditolak sistem."""
    box(slide, x, y, w, h, fill=WHITE, line=RGBColor(0xC2, 0xCB, 0xD9), radius=0.04)
    box(slide, x, y, w, 0.26, fill=NAVY, line=None, radius=0.04)
    txt(slide, x + 0.14, y + 0.05, w - 0.90, 0.16, [("Tutup kasus · DT-0912", 7.6, True, WHITE)])
    txt(slide, x + w - 0.72, y + 0.06, 0.60, 0.16, [("DRAF", 6.2, True, GOLD)], align=PP_ALIGN.RIGHT)
    fields = [("Sebab", "", True), ("Bukti foto", "0 berkas", True), ("PIC", "Dhani", False)]
    yy = y + 0.34
    for name, val, empty in fields:
        txt(slide, x + 0.14, yy + 0.02, 0.98, 0.15, [(name, 7.2, None, GREY)])
        if empty:
            box(slide, x + 1.10, yy, w - 1.24, 0.19, fill=RGBColor(0xFD, 0xF3, 0xF3),
                line=RGBColor(0xD9, 0x9C, 0x9C), lw=0.9, radius=0.02)
            txt(slide, x + 1.16, yy + 0.03, w - 1.40, 0.14, [(val or "wajib diisi", 6.8, None, RED)])
        else:
            txt(slide, x + 1.14, yy + 0.03, w - 1.36, 0.14, [(val, 7.0, True, INK)])
        yy += 0.215
    box(slide, x + 0.14, y + h - 0.30, 1.36, 0.22, fill=RGBColor(0x8E, 0x99, 0xAC), line=None, radius=0.04)
    txt(slide, x + 0.14, y + h - 0.26, 1.36, 0.16, [("Simpan & tutup", 7.0, True, WHITE)], align=PP_ALIGN.CENTER)
    txt(slide, x + 1.58, y + h - 0.26, w - 1.72, 0.16,
        [("tidak aktif sampai kolom terisi", 6.6, None, GREY)])


def photo(slide, path, x, y, w, h, frame=True):
    """Tempel foto asli, potong otomatis agar tidak gepeng."""
    from PIL import Image as _Img
    iw, ih = _Img.open(path).size
    pic = slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
    ar_img, ar_box = iw / ih, w / h
    if ar_img > ar_box:
        trim = (1 - ar_box / ar_img) / 2
        pic.crop_left = pic.crop_right = trim
    else:
        trim = (1 - ar_img / ar_box) / 2
        pic.crop_top = pic.crop_bottom = trim
    if frame:
        shape(slide, MSO_SHAPE.RECTANGLE, x, y, w, h, fill=None,
              line=RGBColor(0xC2, 0xCB, 0xD9), lw=0.9)
    return pic


def caption(slide, x, y, w, text):
    txt(slide, x, y, w, 0.24, [(text, 8, None, LGREY)], spacing=1.15)


def badge(slide, x, y, w, text, color):
    box(slide, x, y, w, 0.19, fill=color, line=None, radius=0.5)
    txt(slide, x, y + 0.010, w, 0.16, [(text, 6.9, True, WHITE)], align=PP_ALIGN.CENTER)


def mock_screen(slide, x, y, w, h, head, right="", body_fill=WHITE):
    """Bingkai layar TV: bezel gelap, kepala navy, isi putih."""
    box(slide, x, y, w, h, fill=RGBColor(0x16, 0x1D, 0x2A), line=None, radius=0.04)
    box(slide, x + 0.05, y + 0.05, w - 0.10, h - 0.10, fill=body_fill, line=None, radius=0.03)
    box(slide, x + 0.05, y + 0.05, w - 0.10, 0.22, fill=NAVY, line=None, radius=None)
    txt(slide, x + 0.13, y + 0.085, w - 0.85, 0.16, [(head, 7.6, True, WHITE)])
    if right:
        txt(slide, x + w - 0.95, y + 0.085, 0.82, 0.16, [(right, 7, True, GOLD)],
            align=PP_ALIGN.RIGHT)
    return y + 0.31


def mock_card(slide, x, y, w, h, code, title, meta, btext, bcolor, strip=GOLD):
    """Satu kartu temuan di layar lantai."""
    box(slide, x, y, w, h, fill=WHITE, line=RULE, radius=0.04)
    box(slide, x, y, 0.05, h, fill=strip, line=None, radius=0.5)
    txt(slide, x + 0.14, y + 0.04, w - 1.05, 0.16, [(code, 7.2, True, GREY)])
    if btext:
        badge(slide, x + w - 0.86, y + 0.05, 0.74, btext, bcolor)
    txt(slide, x + 0.14, y + 0.20, w - 0.26, 0.16, [(title, 8.3, True, INK)], spacing=1.0)
    if meta:
        txt(slide, x + 0.14, y + h - 0.18, w - 0.26, 0.16,
            [(meta, 6.9, None, GREY)], spacing=1.0)


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
x = 1.10
for head_, body, col in band:
    box(s, x, 4.90, 2.24, 1.34, fill=SOFT, line=RULE, radius=0.05)
    hline(s, x + 0.01, 4.90, 2.22, col, 0.06)
    txt(s, x + 0.15, 5.02, 1.96, 0.24, [(head_.upper(), 9, True, col)])
    txt(s, x + 0.15, 5.26, 1.96, 0.90, [(body, 8.8, None, INK)], spacing=1.2)
    x += 2.40

photo(s, "docs/assets/papan/crop_defect.jpg", 8.72, 4.90, 3.99, 1.30)
caption(s, 8.72, 6.24, 3.80, "Tabel defect di papan: target dan hasil tiap shift ditulis tangan")


# ================================================================ 3 · PAPAN DMS (FOTO ASLI)
s = page("Papan DMS hari ini: empat pilar ditulis tangan setiap pagi",
         "Bagian 2 · kondisi hari ini",
         note="Foto papan DMS B.U.E Factory 10, 3 November 2026 · diisi tangan per shift")

photo(s, "docs/assets/papan/board_ep_full.jpg", 0.62, 1.26, 6.16, 4.10)
caption(s, 1.12, 5.40, 5.66,
        "Satu papan, empat pilar: Safety, Quality, Productivity, Delivery")

box(s, 0.62, 5.66, 6.16, 1.08, fill=SOFT, line=RULE, radius=0.05)
txt(s, 0.80, 5.74, 5.80, 0.26,
    [("Yang ditulis tangan tiap pagi", 9.5, True, NAVY)])
txt(s, 0.80, 6.00, 5.80, 0.70,
    [("Angka per line dan per shift disalin dari papan ke rekap, lalu dibahas di "
      "rapat pagi pukul 08.30.", 9, None, GREY),
     ("Alur kunjungan papan: Before → Observation → Documentation → After → Team orientation.",
      9, None, GREY)], spacing=1.16)

label(s, 7.02, 1.26, "EMPAT PILAR · FOTO POTONGAN PAPAN", 5.6)
pillars = [("docs/assets/papan/tile_safety.jpg", "SAFETY",
            "zero accident, SHE index, KAK terakhir", "SHE · 4.896 kasus", RED),
           ("docs/assets/papan/tile_quality.jpg", "QUALITY",
            "defect per line, critical point, kontaminasi", "QC · 5.123 kasus", GOLD),
           ("docs/assets/papan/tile_prod.jpg", "PRODUCTIVITY",
            "yield RM dan PM per line, OEE", "Prod · 7.182 kasus", NAVY),
           ("docs/assets/papan/tile_delivery.jpg", "DELIVERY",
            "plan vs real PO, achievement harian", "keterlambatan kasus", TEAL)]
y = 1.50
for path, name, body, count, col in pillars:
    box(s, 7.02, y, 5.70, 1.06, fill=WHITE, line=RULE, radius=0.05)
    photo(s, path, 7.12, y + 0.09, 1.30, 0.88, frame=False)
    box(s, 7.02, y, 0.05, 1.06, fill=col, line=None, radius=0.5)
    txt(s, 8.56, y + 0.10, 4.00, 0.22, [(name, 9.5, True, col)])
    txt(s, 8.56, y + 0.34, 4.00, 0.34, [(body, 8.5, None, GREY)], spacing=1.08)
    txt(s, 8.56, y + 0.74, 4.00, 0.22, [(count, 8.5, True, NAVY)])
    y += 1.12

txt(s, 7.02, 6.02, 5.70, 0.44,
    [("Empat pilar ini juga empat kelompok data di workbook: yang ditulis tangan di papan "
      "adalah yang nanti diisi sekali di form.", 9, None, INK)], spacing=1.18)


# ================================================================ 4 · ALUR MANUAL VS SISTEM
s = page("Alur kerja berubah: dari lima langkah tangan ke satu input",
         "Bagian 2 · diagram alir",
         note="Perbandingan putaran harian sekarang dan setelah sistem dipakai")

SW, SG = 2.10, 0.37
xs = [0.62 + i * (SW + SG) for i in range(5)]

label(s, 0.62, 1.24, "ALUR SEKARANG · DIKERJAKAN TANGAN", 7.0)
now = [("Tulis di papan", "leader mencatat manual di papan line, per shift"),
       ("Rekap ke Excel", "angka disalin ulang ke file rekap harian"),
       ("Hitung sendiri", "nilai dihitung dengan kalkulator, hasil bisa berbeda"),
       ("Kirim grup WA", "laporan dikirim ke grup, format tidak seragam"),
       ("Rapat & tindak lanjut", "tindak lanjut dicatat di papan PICA")]
for i, (head_, body) in enumerate(now):
    box(s, xs[i], 1.52, SW, 1.32, fill=WHITE, line=RGBColor(0xD9, 0xBE, 0xBE), radius=0.05)
    box(s, xs[i], 1.52, SW, 0.06, fill=RED, line=None, radius=None)
    txt(s, xs[i] + 0.14, 1.68, SW - 0.28, 0.28, [(head_, 10.5, True, INK)])
    txt(s, xs[i] + 0.14, 1.98, SW - 0.26, 0.82, [(body, 9, None, GREY)], spacing=1.12)
    if i < 4:
        arrow(s, xs[i] + SW + 0.05, 2.06, SG - 0.10, 0.26, "right", RGBColor(0xE6, 0xD3, 0xD3))

txt(s, 0.62, 3.24, 12.09, 0.26,
    [("setiap langkah manual digantikan satu langkah sistem", 9, True, GOLD)])
sysm = [("Isi satu form", "sekali per item checklist, selesai di bawah lima menit"),
        ("Sistem periksa", "kolom kurang dan sebab kosong ditolak sebelum dikirim"),
        ("Sistem simpan & olah", "angka jadi saat data disimpan, tanpa rumus ketik ulang"),
        ("Tayang otomatis", "dasbor L1–L3 dan layar TV membaca catatan yang sama"),
        ("Sistem menagih", "pengingat dan tenggat berjalan sampai kasus ditutup")]
for i, (head_, body) in enumerate(sysm):
    box(s, xs[i], 3.56, SW, 1.32, fill=WHITE, line=RGBColor(0xBF, 0xD8, 0xD9), radius=0.05)
    box(s, xs[i], 3.56, SW, 0.06, fill=TEAL, line=None, radius=None)
    txt(s, xs[i] + 0.14, 3.72, SW - 0.28, 0.28, [(head_, 10.5, True, NAVY)])
    txt(s, xs[i] + 0.14, 4.02, SW - 0.26, 0.82, [(body, 9, None, GREY)], spacing=1.12)
    if i < 4:
        arrow(s, xs[i] + SW + 0.05, 4.10, SG - 0.10, 0.26, "right", RGBColor(0xC9, 0xDE, 0xDF))

# panah pembanding per langkah
for i in range(5):
    arrow(s, xs[i] + SW / 2 - 0.13, 2.90, 0.26, 0.30, "down", GOLD)

label(s, 1.12, 5.08, "YANG BERUBAH BAGI TIM", 10.5)
gains = [("Kerja jadi sekali", "input sehari sekali, tidak ada rekap ulang", TEAL),
         ("Angka tidak berselisih", "semua layar membaca catatan yang sama", NAVY),
         ("Tidak ada yang tertinggal", "sistem yang mengingatkan, bukan orang", GOLD)]
x = 1.10
for head_, body, col in gains:
    box(s, x, 5.36, 3.76, 0.96, fill=SOFT, line=RULE, radius=0.05)
    box(s, x, 5.36, 0.06, 0.96, fill=col, line=None, radius=0.5)
    txt(s, x + 0.18, 5.45, 3.42, 0.24, [(head_, 9.5, True, col)])
    txt(s, x + 0.18, 5.72, 3.42, 0.50, [(body, 9, None, GREY)], spacing=1.15)
    x += 3.92

txt(s, 1.10, 6.38, 11.50, 0.50,
    [("Yang tidak berubah  ·  keputusan tetap di manusia: plant head menetapkan prioritas, "
      "DH menyetujui penutupan kasus, Admin menetapkan target plant.", 9.5, None, GREY)], spacing=1.2)


# ================================================================ 4 · ILUSTRASI LAYAR (4 halaman)
def shot(slide, path, x, y, title, sub, col, maxw=7.05, maxh=4.26):
    """Ilustrasi layar besar: gambar mockup dipaskan ke kotak, keterangan di bawah."""
    from PIL import Image as _I
    iw, ih = _I.open(path).size
    ar = iw / ih
    w = maxw if maxw / maxh <= ar else maxh * ar
    h = w / ar
    px = x + 0.12 + (maxw - w) / 2
    cw = maxw + 0.24
    ch = 0.68 + h + 0.30
    box(slide, x, y, cw, maxh + 0.98, fill=WHITE, line=RULE, radius=0.05)
    hline(slide, x + 0.01, y, cw - 0.02, col, 0.05)
    txt(slide, x + 0.20, y + 0.14, cw - 0.34, 0.26, [(title, 10.5, True, NAVY)])
    txt(slide, x + 0.20, y + 0.40, cw - 0.34, 0.22, [(sub, 9, None, GREY)])
    slide.shapes.add_picture(path, Inches(px), Inches(y + 0.68), Inches(w), Inches(h))
    txt(slide, x + 0.20, y + maxh + 0.72, cw - 0.34, 0.20,
        [("Ilustrasi rancangan layar · bukan tangkapan aplikasi asli", 8, None, LGREY)])


def sides(slide, x, y, w, items, head="APA YANG TERLIHAT DI LAYAR"):
    txt(slide, x, y, w, 0.26, [(head, 10, True, GOLD)])
    yy = y + 0.28
    for head_, body, col in items:
        box(slide, x, yy, w, 1.16, fill=SOFT, line=RULE, radius=0.05)
        box(slide, x, yy, 0.06, 1.16, fill=col, line=None, radius=0.5)
        txt(slide, x + 0.20, yy + 0.12, w - 0.40, 0.26, [(head_, 10, True, col)])
        txt(slide, x + 0.20, yy + 0.42, w - 0.40, 0.66, [(body, 9, None, GREY)], spacing=1.16)
        yy += 1.28


s = page("Ilustrasi layar 1: form harian di tablet line",
         "Bagian 3 · ilustrasi sistem",
         note="Angka contoh di layar memakai ukuran workbook Snack · line 9 · 96,9% kasus ada di line ini")
shot(s, "docs/assets/mockup/form.png", 0.62, 1.46,
     "FORM HARIAN · TABLET DI LINE · SNACK LINE 9",
     "satu layar per shift: item checklist, target, hasil, status, sebab", NAVY)
sides(s, 8.20, 1.46, 4.50, [
    ("Satu isian per item", "Leader hanya mengisi hasil; target sudah menempel pada item checklist.", NAVY),
    ("Sebab tidak bisa kosong", "Bila hasil di bawah target, kolom sebab dan tindakan wajib diisi.", RED),
    ("Selesai di bawah lima menit", "12 dari 15 item, sisa waktu tampil di layar; draf tersimpan otomatis.", TEAL),
    ("Kirim sekali, langsung tayang", "Satu tombol: angka masuk dasbor dan layar lantai, tanpa salin ulang.", GOLD)])


s = page("Ilustrasi layar 2: layar lantai TV tanpa login",
         "Bagian 3 · ilustrasi sistem",
         note="TV membaca catatan yang sama dengan form harian dan dasbor · kartu tertua tampil paling atas")
shot(s, "docs/assets/mockup/tv.png", 0.62, 1.46,
     "LAYAR LANTAI · TV AREA PRODUKSI · EXIST PLANT",
     "tanpa interaksi, berganti tiap 30 detik, dibaca dari jauh", TEAL)
sides(s, 8.20, 1.46, 4.50, [
    ("Tiga kartu per layar", "Kartu paling mendesak di atas; sisanya diputar bergiliran tiap 30 detik.", TEAL),
    ("Angka pemicu ikut tampil", "Umur kasus, jumlah berulang, dan porsi kasus terlihat tanpa membuka dasbor.", RED),
    ("Dibaca dari jauh", "Huruf besar, satu warna per status; tidak perlu login dan tidak bisa diubah.", GOLD),
    ("Tidak pernah hilang", "Kartu tetap tampil sampai kasus ditutup, bukan sekali lalu lewat.", NAVY)])


s = page("Ilustrasi layar 3: dasbor tiga tingkat di laptop",
         "Bagian 3 · ilustrasi sistem",
         note="L1 memantau hari ini, L2 menutup kasus, L3 membandingkan plant · satu angka untuk semua")
shot(s, "docs/assets/mockup/dasbor.png", 0.62, 1.46,
     "DASBOR L2 · SUPERVISOR · LINE 9",
     "kartu angka, tren pilar, temuan terbuka, dan daftar lewat tenggat", NAVY)
sides(s, 8.20, 1.46, 4.50, [
    ("Empat angka harian", "Kasus hari ini, close lengkap, lewat tenggat, pola berulang.", NAVY),
    ("Temuan sudah berperingkat", "Sistem yang memilih tiga temuan teratas, bukan orang yang mencari.", TEAL),
    ("Daftar kerja, bukan laporan", "Setiap baris membawa sebab, PIC, dan sisa hari sebelum tenggat.", RED),
    ("Tinggal pilih tingkat", "L1 hari ini, L2 kasus, L3 antar plant dan antar line.", GOLD)])


s = page("Ilustrasi layar 4: halaman admin penjaga aturan",
         "Bagian 3 · ilustrasi sistem",
         note="Hanya Admin yang mengubah target, layar TV, dan kunci periode · semua perubahan masuk jejak audit")
shot(s, "docs/assets/mockup/admin.png", 0.62, 1.46,
     "HALAMAN ADMIN · ADMIN PLANT SNACK",
     "target per versi, layar TV aktif, kunci periode, jejak audit", GOLD)
sides(s, 8.20, 1.46, 4.50, [
    ("Target per plant, per versi", "Target dan bobot KPI disimpan sebagai versi; periode lama tidak berubah.", GOLD),
    ("Layar TV dikelola dari sini", "Admin memilih line dan pilar yang tampil di tiap TV, tanpa menyalakan ulang.", TEAL),
    ("Periode dikunci", "Periode yang sudah dilaporkan tidak bisa diubah; koreksi dicatat versi baru.", RED),
    ("Jejak audit terbaca", "Siapa, kapan, dan nilai sebelum–sesudah tersimpan untuk pemeriksaan.", NAVY)])


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
     "Pola berulang dikenali, saran pencegahan disiapkan", "Menandai manual di kolom"],
    ["Mengumpulkan angka antar plant", "Group",
     "Dasbor membandingkan plant dengan definisi sama", "Menggabung sheet manual"],
    ["Mencari riwayat perubahan angka", "Audit / DH",
     "Tercatat: siapa, kapan, sebelum–sesudah", "Menanyakan siapa yang mengubah"],
    ["Menyusun laporan bulanan", "Admin plant",
     "Laporan tersedia dari data yang sama, siap diunduh", "Merangkum ulang tiap bulan"],
], [3.45, 1.45, 4.10, 3.09], 0.62, 1.24, row_h=0.405, head_h=0.36, fs=10, head_fs=10,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT], bold_first=False)

box(s, 1.10, 6.06, 11.61, 0.62, fill=SOFT, line=RULE, radius=0.05)
txt(s, 1.30, 6.16, 11.22, 0.44,
    [("Cara membaca  ·  kolom kanan adalah pekerjaan yang hilang dari rutinitas tim, "
      "bukan sekadar dipindahkan ke aplikasi.", 9.5, None, GREY)], spacing=1.2)


# ================================================================ 5 · BEBAN PER BULAN
BULAN = list(DATA["_bulanan_total"].keys())
D12 = BULAN[-12:]
LBL = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]
CATS = [LBL[int(m[5:]) - 1] + " " + m[2:4] for m in D12]


def seri(plant):
    b = DATA[plant]["bulanan"]
    return [b.get(m, 0) for m in D12]


kasus_tahun = sum(DATA["_bulanan_total"][m] for m in D12)
kasus_bulan = round(kasus_tahun / 12)
MENIT_REKAP = 2          # asumsi: cari, salin, hitung, tulis per kasus
MENIT_LAPORAN = 15       # asumsi: menyusun laporan & bahan rapat per plant per hari
HARI_KERJA = 21
jam_rekap = kasus_bulan * MENIT_REKAP / 60
jam_laporan = 3 * HARI_KERJA * MENIT_LAPORAN / 60
jam_total = jam_rekap + jam_laporan
jam_setahun = jam_total * 12
hari_kerja_setara = jam_setahun / 8
puncak = max(DATA["_bulanan_total"][m] for m in D12)
_pk = max(D12, key=lambda m: DATA["_bulanan_total"][m])
puncak_bulan = f"{LBL[int(_pk[5:]) - 1]} {_pk[:4]}"

s = page("Sebagian besar waktu tim habis untuk merekap, bukan memperbaiki",
         "Bagian 2 · beban manual",
         note="Volume dari 12 bulan terakhir workbook; waktu per pekerjaan adalah asumsi yang dapat diubah Admin")
kpi_cards(s, [(n(kasus_tahun), "kasus dalam 12 bulan", f"rata-rata {n(kasus_bulan)} kasus/bulan", NAVY),
              (f"{jam_rekap:.0f} jam", "merekapitulasi kasus", f"{n(kasus_bulan)} kasus × {MENIT_REKAP} menit", GOLD),
              (f"{jam_laporan:.0f} jam", "menyusun laporan harian", f"3 plant × {HARI_KERJA} hari × {MENIT_LAPORAN} menit", GOLD),
              (f"{jam_total:.0f} jam", "per bulan kembali ke tim", f"setara {hari_kerja_setara:.0f} hari kerja per tahun", TEAL)])

label(s, 0.62, 2.44, "KASUS PER BULAN · 12 BULAN TERAKHIR", 7.4)
chart(s, 0.52, 2.62, 7.60, 2.10,
      CATS,
      [("Snack", seri("Snack")), ("Exist Plant", seri("Exist Plant")), ("New Plant", seri("New Plant"))],
      XL_CHART_TYPE.COLUMN_STACKED, [GOLD, TEAL, NAVY], number_format="#,##0",
      legend=True, fs=8, gap=45, label_pos=XL_LABEL_POSITION.CENTER, label_color=WHITE,
      vmax=400)
txt(s, 0.62, 4.74, 7.50, 0.26,
    [(f"Puncak {n(puncak)} kasus ({puncak_bulan}) berarti beban rekap naik "
      f"jadi sekitar {puncak * MENIT_REKAP / 60:.0f} jam pada bulan itu.", 9, None, GREY)])

label(s, 8.42, 2.44, "CARA SISTEM MENGEMBALIKAN WAKTUNYA", 4.3)
steps_ = [("Rekap hilang", "form tersimpan sendiri, tidak ada salin ulang", TEAL),
          ("Hitung hilang", "angka jadi saat data dikirim", TEAL),
          ("Bahan rapat hilang", "kartu temuan tersusun otomatis", NAVY),
          ("Menagih hilang", "pengingat berjalan sendiri", NAVY)]
y = 2.66
for head_, body, col in steps_:
    box(s, 8.42, y, 4.29, 0.62, fill=SOFT, line=RULE, radius=0.05)
    box(s, 8.42, y, 0.06, 0.62, fill=col, line=None, radius=0.5)
    txt(s, 8.60, y + 0.07, 3.95, 0.24, [(head_, 9.5, True, col)])
    txt(s, 8.60, y + 0.31, 3.95, 0.28, [(body, 9, None, GREY)])
    y += 0.68

txt(s, 8.42, 5.42, 4.29, 0.26,
    [("REKAP YANG DISUSUN TANGAN · POTONGAN SPREADSHEET", 9, True, GOLD)])
_ex = []
for m in D12[-4:]:
    tot = DATA["_bulanan_total"][m]
    _ex.append((CATS[D12.index(m)], n(tot), n(tot - 3), str(2 + (len(_ex) % 3))))
mock_excel(s, 8.42, 5.70, 4.29, 0.86, _ex, head="rekap_dms.xlsx · dicocokkan per shift")

txt(s, 1.10, 5.18, 7.10, 0.24, [("YANG TIDAK DIHITUNG DALAM JAM, TETAPI LEBIH MAHAL", 9, True, GOLD)])
mahal = [("3.220", "kasus ditutup tanpa sebab — keputusan diambil tanpa dasar"),
         ("53", "kasus lewat tenggat, tertua 1.182 hari — masalah menua"),
         ("153", "sel error di sheet resume — angka bisa salah tanpa diketahui")]
y = 5.48
for v, body in mahal:
    txt(s, 1.10, y, 0.95, 0.28, [(v, 13, True, RED)])
    txt(s, 2.14, y + 0.02, 6.05, 0.26, [(body, 9.5, None, GREY)])
    y += 0.40


# ================================================================ 5 · ALUR HARIAN
s = page("Alur harian: enam langkah dalam satu putaran",
         "Bagian 2 · diagram alir",
         note="Putaran Senin–Jumat; data hari libur tetap tersimpan sebagai arsip")
W, GAP, H = 3.44, 0.60, 1.46
X1 = 0.62
X2 = X1 + W + GAP
X3 = X2 + W + GAP
TOPY, BOTY = 1.54, 3.64

step(s, X1, TOPY, W, H, 1, "Input harian",
     "Leader line mengisi checklist per item untuk hari berjalan.\nSatu layar per line, selesai di bawah lima menit.", NAVY)
arrow(s, X1 + W + 0.14, TOPY + H / 2 - 0.17, GAP - 0.28, 0.34, "right", PALE)
step(s, X2, TOPY, W, H, 2, "Pemeriksaan otomatis",
     "Item yang belum lengkap ditolak sistem sebelum dikirim.\nSebab wajib diisi bila hasil di bawah target.", NAVY)
arrow(s, X2 + W + 0.14, TOPY + H / 2 - 0.17, GAP - 0.28, 0.34, "right", PALE)
step(s, X3, TOPY, W, H, 3, "Angka langsung jadi",
     "Nilai harian dan capaian dihitung sistem saat data disimpan.\nTidak ada rumus yang diketik ulang.", TEAL)

arrow(s, X3 + W / 2 - 0.17, TOPY + H + 0.08, 0.34, 0.40, "down", PALE)

step(s, X3, BOTY, W, H, 4, "Tampil di kanal",
     "Dasbor L1–L3 dan layar TV membaca catatan yang sama.\nKartu temuan ikut diperbarui.", TEAL)
arrow(s, X3 - GAP + 0.14, BOTY + H / 2 - 0.17, GAP - 0.28, 0.34, "left", PALE)
step(s, X2, BOTY, W, H, 5, "Temuan & pengingat",
     "Sistem memilih temuan lalu menetapkan pemilik dan tenggat.\nPengingat berjalan sampai kasus ditutup.", GOLD)
arrow(s, X2 - GAP + 0.14, BOTY + H / 2 - 0.17, GAP - 0.28, 0.34, "left", PALE)
step(s, X1, BOTY, W, H, 6, "Tindak lanjut",
     "Kasus ditutup setelah sebab, tindakan, bukti, dan PIC lengkap.\nPenutupan disetujui DH atau plant head.", GOLD)

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
txt(s, 1.42, 3.30, 1.90, 0.24, [("Belum", 9, True, GOLD)], align=PP_ALIGN.CENTER)
box(s, 0.52, 3.84, 3.50, 0.94, fill=WHITE, line=GOLD, radius=0.05)
txt(s, 0.72, 3.94, 3.12, 0.76,
    [("Kembali ke PIC", 10.5, True, NAVY),
     ("umur kasus bertambah dan kartunya tetap tampil di layar TV", 9, None, GREY)], spacing=1.2)

mock_ditolak(s, 0.62, 4.92, 3.30, 1.44)

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

photo(s, "docs/assets/papan/crop_pica.jpg", 0.62, 1.30, 3.72, 1.52)
caption(s, 0.62, 2.86, 3.72, "Papan PICA: masalah, akar, tindakan, PIC, tenggat")

label(s, 9.10, 1.30, "KENAPA SISTEM YANG MENAHAN", 3.55)
gates = [(n(TOT["close_tanpa_sebab"]), "kasus Close tanpa sebab di tiga workbook"),
         ("0%", "due date terisi di sheet SHE — tidak ada yang menagih"),
         (n(TOT["overdue"]), "kasus lewat tenggat, tertua 1.182 hari")]
y = 1.74
for v, body in gates:
    txt(s, 9.10, y, 1.35, 0.34, [(v, 15, True, NAVY)])
    txt(s, 10.02, y + 0.02, 2.00, 0.62, [(body, 9, None, GREY)], spacing=1.18)
    y += 0.74

box(s, 9.10, 3.94, 3.55, 1.30, fill=SOFT, line=RULE, radius=0.05)
txt(s, 9.28, 4.06, 3.18, 0.24, [("JEJAK AUDIT", 9, True, GOLD)])
txt(s, 9.28, 4.32, 3.18, 0.84,
    [("Sistem mencatat siapa mengubah apa dan kapan, sehingga penutupan kasus "
      "bisa dipertanggungjawabkan.", 9, None, GREY)], spacing=1.2)


# ================================================================ 7 · SATU SUMBER ANGKA
s = page("Satu catatan dipakai semua layar, tanpa rekap ulang",
         "Bagian 5 · peran sistem",
         note="Dibandingkan: angka ringkasan di dalam sheet versus jumlah baris kasus")
label(s, 0.62, 1.26, "ANGKA RINGKASAN SHEET VS BARIS KASUS", 6.6)
chart(s, 0.52, 1.42, 7.10, 3.16,
      ["QC Snack", "QC Exist", "QC New", "Prod Snack", "Prod Exist", "Prod New"],
      [("Ringkasan sheet", [SN["QC"]["ringkasan_sheet"].get("TOTAL", 0), EP["QC"]["ringkasan_sheet"].get("TOTAL", 0),
                            NP["QC"]["ringkasan_sheet"].get("TOTAL", 0), SN["Prod"]["ringkasan_sheet"].get("TOTAL", 0),
                            EP["Prod"]["ringkasan_sheet"].get("TOTAL", 0), NP["Prod"]["ringkasan_sheet"].get("TOTAL", 0)]),
       ("Baris kasus", [SN["QC"]["kasus"], EP["QC"]["kasus"], NP["QC"]["kasus"],
                        SN["Prod"]["kasus"], EP["Prod"]["kasus"], NP["Prod"]["kasus"]])],
      XL_CHART_TYPE.COLUMN_CLUSTERED, [PALE, NAVY], number_format="#,##0",
      legend=True, fs=8, gap=55, label_pos=XL_LABEL_POSITION.OUTSIDE_END, vmax=3600)
txt(s, 0.62, 4.60, 7.10, 0.24,
    [("Selisih terbesar di Exist Plant: ringkasan QC 993, tabel kasus 2.338 baris.",
      9.5, None, GREY)])

table(s, [
    ["Plant", "QC ringkas", "QC tabel", "Prod ringkas", "Prod tabel"],
    ["Snack", n(SN["QC"]["ringkasan_sheet"].get("TOTAL", 0)), n(SN["QC"]["kasus"]),
     n(SN["Prod"]["ringkasan_sheet"].get("TOTAL", 0)), n(SN["Prod"]["kasus"])],
    ["Exist Plant", n(EP["QC"]["ringkasan_sheet"].get("TOTAL", 0)), n(EP["QC"]["kasus"]),
     n(EP["Prod"]["ringkasan_sheet"].get("TOTAL", 0)), n(EP["Prod"]["kasus"])],
    ["New Plant", n(NP["QC"]["ringkasan_sheet"].get("TOTAL", 0)), n(NP["QC"]["kasus"]),
     n(NP["Prod"]["ringkasan_sheet"].get("TOTAL", 0)), n(NP["Prod"]["kasus"])],
], [1.25, 1.00, 0.90, 1.00, 0.90], 8.00, 1.42, row_h=0.46, head_h=0.36, fs=10.5, head_fs=9, bold_first=True,
    aligns=[PP_ALIGN.LEFT] + [PP_ALIGN.RIGHT] * 4)

box(s, 8.00, 3.72, 4.71, 1.20, fill=SOFT, line=RULE, radius=0.05)
txt(s, 8.18, 3.82, 4.35, 0.24, [("YANG DILAKUKAN SISTEM", 9, True, GOLD)])
txt(s, 8.18, 4.08, 4.35, 0.80,
    [("Satu catatan kasus, satu angka.", 9.5, True, NAVY),
     ("Laporan, dasbor, dan layar TV membaca catatan yang sama — tidak ada sel ringkasan "
      "yang perlu dihitung ulang.", 9, None, GREY)], spacing=1.22)

label(s, 1.10, 4.84, "KEBIASAAN MANUAL YANG IKUT HILANG", 11.5)
pola = [("Ringkasan tanpa tanggal", "blok ringkasan tidak menyimpan periode, jadi tidak bisa dibandingkan antar pekan.", GOLD),
        ("Nilai satu blok 0,6", "Exist Plant punya blok 0,6 sementara blok lain 3,0 — akibat salin manual.", RED),
        ("Kolom PIC berisi tautan foto", "di SHE Exist Plant, kolom PIC memuat URL SharePoint, bukan nama orang.", RED),
        ("Nama line tidak seragam", "ws l02 / WS L02 / Line 2 hidup berdampingan di plant yang sama.", GOLD)]
x = 1.10
for head_, body, col in pola:
    box(s, x, 5.30, 2.81, 1.28, fill=SOFT, line=RULE, radius=0.05)
    txt(s, x + 0.16, 5.38, 2.51, 0.44, [(head_, 10, True, col)], spacing=1.08)
    txt(s, x + 0.16, 5.84, 2.51, 0.68, [(body, 9.2, None, GREY)], spacing=1.16)
    x += 2.93


# ================================================================ 8 · MUTU DATA
s = page("Data yang belum lengkap ditandai sistem, bukan dicari manual",
         "Bagian 4 · data",
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

label(s, 1.10, 4.50, "EMPAT HAL YANG DIAMBIL ALIH SISTEM", 11.5)
findings = [(n(TOT["close_tanpa_sebab"]), "Kasus Close tanpa sebab — sistem menolak menutup tanpa sebab terisi.", GOLD),
            ("0%", "Due date di sheet SHE — sistem mewajibkan tenggat sebelum kasus berjalan.", RED),
            (n(TOT["error_sel_total"]), "Sel error di sheet — sistem tidak menyimpan rumus di sel bebas.", RED),
            (n(TOT["pola_3x"]), "Pola berulang — sistem mengenali dan mengusulkan tindakan pencegahan.", TEAL)]
x = 1.10
for v, body, col in findings:
    box(s, x, 4.80, 2.81, 1.42, fill=SOFT, line=RULE, radius=0.05)
    box(s, x, 4.80, 2.81, 0.06, fill=col, line=None, radius=None)
    txt(s, x + 0.18, 4.92, 2.49, 0.40, [(v, 19, True, col)])
    txt(s, x + 0.18, 5.34, 2.49, 0.80, [(body, 9, None, GREY)], spacing=1.18)
    x += 2.93


# ================================================================ 9 · INSIGHT
s = page("Sistem memilih temuan dan mengingatkan pemiliknya",
         "Bagian 5 · peran sistem",
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
], [0.66, 2.76, 3.86, 1.10], 0.62, 1.24, row_h=0.36, head_h=0.34, fs=9.4,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER])

txt(s, 1.10, 6.02, 7.82, 0.70,
    [("Temuan diurutkan dari dampak terbesar, bukan dari siapa yang mengirim lebih dulu.",
      10, True, NAVY),
     ("Maksimal tiga kartu tampil di layar lantai; sisanya di dasbor supervisor dan admin.",
      9.5, None, GREY)], spacing=1.3)

yc = mock_screen(s, 9.10, 1.24, 3.60, 2.32, "SNACK · LINE 9 · 3 KARTU", "07:10 · TV",
                 body_fill=SOFT)
tv_cards = [("I-02 · LEWAT TENGGAT", "Downtime belum ditutup", "PIC Dhani · 1.182 hari", "OVERDUE", RED, RED),
            ("I-03 · BERULANG", "BCT WS L04 P02 muncul lagi", "PIC Sigit · 134× Exist Plant", "BERULANG", GOLD, GOLD),
            ("I-10 · MENUMPUK", "Satu line menumpuk kasus", "Snack line 9 · 96,9% kasus", "L3", TEAL, TEAL)]
for code, title, meta, btext, bcolor, strip in tv_cards:
    mock_card(s, 9.16, yc, 3.48, 0.58, code, title, meta, btext, bcolor, strip)
    yc += 0.64

box(s, 9.10, 3.66, 3.60, 2.20, fill=SOFT, line=RULE, radius=0.05)
txt(s, 9.28, 3.78, 3.24, 0.24, [("CARA MEMBACA TABEL", 9, True, GOLD)])
txt(s, 9.28, 4.06, 3.24, 1.74,
    [("Kanal menunjukkan siapa penerima kartu: layar lantai, dasbor L1, L2, atau L3.", 9, None, GREY),
     ("Satu kartu memuat satu temuan, bukan satu daftar.", 9, None, GREY),
     ("Angka pemicu memakai tiga workbook: 53, 3.220, 134×, 508.226 menit.", 9, None, GREY),
     ("Kartu yang sama juga muncul di dasbor; tidak ada versi angka kedua.", 9, None, GREY)],
    spacing=1.25)


# ================================================================ 10 · KANAL
s = page("Empat kanal tampilan dan batasannya", "Bagian 6 · tampilan",
         note="Mockup layar adalah ilustrasi rancangan; tangkapan aplikasi asli menyusul saat dibangun")
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
    box(s, x, 1.24, 2.95, 1.66, fill=WHITE, line=RULE, radius=0.05)
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
    ["Jejak audit", "Tercatat: siapa, kapan, sebelum–sesudah"],
], [2.25, 6.35], 0.62, 3.06, row_h=0.42, head_h=0.38, fs=10.5, bold_first=True)

ys = mock_screen(s, 9.30, 3.12, 3.40, 1.92, "TV LANTAI · EXIST PLANT", "TANPA LOGIN")
tv_rows = [("Downtime WS L02", "menunggu foto bukti", "6 HARI", RED),
           ("BCT WS L04 P02", "berulang 134× sebab sama", "BERULANG", GOLD),
           ("Checklist line 3", "kosong 3 hari berturut", "HARI INI", TEAL)]
for title, sub, btext, bcolor in tv_rows:
    box(s, 9.36, ys, 3.28, 0.46, fill=WHITE, line=RULE, radius=0.03)
    box(s, 9.36, ys, 0.05, 0.46, fill=bcolor, line=None, radius=0.5)
    badge(s, 11.86, ys + 0.13, 0.72, btext, bcolor)
    txt(s, 9.50, ys + 0.04, 2.28, 0.16, [(title, 8, True, INK)])
    txt(s, 9.50, ys + 0.23, 2.28, 0.16, [(sub, 6.8, None, GREY)])
    ys += 0.52


txt(s, 9.30, 5.14, 3.45, 0.62,
    [("Kartu tertua tampil paling atas, diperbarui tiap 30 detik, dan tidak hilang "
      "sampai ditutup — layar lantai menjadi daftar kerja, bukan hiasan.", 8.5, None, GREY)],
    spacing=1.18)

label(s, 1.10, 6.02, "YANG TIDAK DIBUAT SEKARANG", 11.60)
box(s, 1.10, 6.22, 11.60, 0.66, fill=SOFT, line=RULE, radius=0.05)
notes = [("Tanpa aplikasi mobile", "form harian berbasis web pada fase 1"),
         ("Tanpa login TV", "layar lantai hanya menampilkan"),
         ("Tanpa angka manual", "isian manual hanya Healthy Check")]
x = 1.32
for head_, body in notes:
    txt(s, x, 6.30, 3.55, 0.22, [(head_, 9, True, NAVY)])
    txt(s, x, 6.50, 3.55, 0.26, [(body, 9, None, GREY)])
    x += 3.78


# ================================================================ 11 · RENCANA
s = page("Rencana 8 pekan: rapikan data dulu, tampilan terakhir",
         "Bagian 7 · rencana",
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
txt(s, 10.62, 0.86, 2.09, 0.22, [("PEKAN PELAKSANAAN", 9, True, GOLD)],
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


# ================================================================ 12 · ALUR WAKTU
s = page("Alur waktu: empat gerbang sebelum sistem dipakai semua plant",
         "Bagian 7 · rencana",
         note="Gerbang diperiksa bersama plant head; bila tidak lulus, pekan berikutnya dipakai untuk memperbaiki")

label(s, 0.62, 1.22, "ENAM TAHAP PENGERJAAN", 6.0)
flow = [("Tahap 0\nFondasi", "pekan 1–2", "master line, mesin, hak akses", NAVY),
        ("Tahap 1\nCapture", "pekan 1–3", "form harian dan form kasus", NAVY),
        ("Tahap 2\nMeasure", "pekan 3–5", "angka otomatis dan dasbor line", TEAL),
        ("Tahap 3\nInsight", "pekan 5–6", "delapan aturan pertama aktif", TEAL),
        ("Tahap 4\nDisplay", "pekan 7", "layar lantai satu area", GOLD),
        ("Tahap 5\nAnalitik", "pekan 7–8", "dasbor plant dan ekspor", GOLD)]
BW, BG = 1.78, 0.28
xs = [0.62 + i * (BW + BG) for i in range(6)]
for i, (name, wk, out, col) in enumerate(flow):
    x = xs[i]
    box(s, x, 1.48, BW, 1.52, fill=WHITE, line=RULE, radius=0.05)
    box(s, x, 1.48, BW, 0.06, fill=col, line=None, radius=None)
    txt(s, x + 0.12, 1.58, BW - 0.24, 0.30, [(name.split("\n")[0], 8.2, True, GREY)])
    txt(s, x + 0.12, 1.80, BW - 0.24, 0.28, [(name.split("\n")[1], 11.5, True, NAVY)])
    txt(s, x + 0.12, 2.10, BW - 0.24, 0.22, [(wk, 8.5, True, col)])
    txt(s, x + 0.12, 2.36, BW - 0.24, 0.56, [(out, 8.4, None, GREY)], spacing=1.14)
    if i < 5:
        arrow(s, x + BW + 0.03, 2.12, BG - 0.06, 0.24, "right", PALE)

# garis gerbang
hline(s, 0.62, 3.22, 12.09, RGBColor(0xD9, 0xDE, 0xE7), 0.014)
gates_at = [(xs[1] - BG / 2, "G1"), (xs[3] - BG / 2, "G2"),
            (xs[4] - BG / 2, "G3"), (xs[5] + BW - 0.55, "G4")]
for gx, g in gates_at:
    shape(s, MSO_SHAPE.DIAMOND, gx - 0.13, 3.06, 0.26, 0.32, fill=GOLD, line=None)
    txt(s, gx - 0.40, 3.40, 0.80, 0.20, [(g, 8.5, True, GOLD)], align=PP_ALIGN.CENTER)

label(s, 1.10, 3.62, "EMPAT GERBANG · LULUS ATAU ULANG", 7.0)
gates = [("G1 · Kesiapan data",
          "master line dan mesin cocok dengan laporan lama; nama line sudah seragam.",
          "bila gagal: rapikan master line dulu, jangan mulai form.", NAVY),
         ("G2 · Angka cocok",
          "total kasus sistem = jumlah baris workbook tiga plant pada bulan uji.",
          "bila gagal: selisih ditelusuri sebelum dasbor dibuka.", TEAL),
         ("G3 · Aturan jalan",
          "delapan aturan pertama memunculkan kartu dengan pemilik dan tenggat.",
          "bila gagal: aturan dipertajam, layar lantai ditunda.", TEAL),
         ("G4 · Siap replikasi",
          "lima ukuran terpenuhi di Snack; template KPI siap dipakai plant lain.",
          "bila gagal: perbaikan satu putaran, replikasi digeser dua pekan.", GOLD)]
x = 1.10
for name, ok, fail, col in gates:
    box(s, x, 3.92, 2.70, 1.66, fill=WHITE, line=RULE, radius=0.05)
    box(s, x, 3.92, 0.05, 1.66, fill=col, line=None, radius=0.5)
    txt(s, x + 0.18, 4.02, 2.40, 0.24, [(name.upper(), 9, True, col)])
    txt(s, x + 0.18, 4.28, 2.38, 0.72, [(ok, 8.6, None, INK)], spacing=1.14)
    txt(s, x + 0.18, 5.06, 2.38, 0.44, [(fail, 8.2, None, GREY)], spacing=1.12)
    x += 2.75

box(s, 1.10, 5.76, 11.61, 0.72, fill=SOFT, line=RULE, radius=0.05)
box(s, 1.10, 5.76, 0.06, 0.72, fill=RED, line=None, radius=0.5)
txt(s, 1.32, 5.86, 11.20, 0.52,
    [("Kalau sebuah gerbang tidak lulus, jadwal digeser — bukan gerbangnya yang diturunkan. "
      "Lima ukuran di halaman sebelumnya adalah alat ujinya.", 9.5, None, INK)], spacing=1.2)


# ================================================================ 13 · ALUR PENYEBARAN
s = page("Alur penyebaran: satu plant jadi contoh, tiga plant menyusul",
         "Bagian 7 · rencana",
         note="Urutan ini mengikuti kesiapan data: Snack paling rapi, Dairy menyusul terakhir")

label(s, 0.62, 1.24, "URUTAN PENYEBARAN", 6.0)
plants = [("SNACK", "pilot · 8 pekan", "data 5.815 kasus, 20 line", NAVY, True),
          ("EXIST PLANT", "replikasi · 4 pekan", "6.774 kasus, 59 line", TEAL, False),
          ("NEW PLANT", "replikasi · 4 pekan", "4.612 kasus, 45 line", TEAL, False),
          ("DAIRY", "replikasi · 4 pekan", "menyusul setelah tiga plant", GOLD, False)]
PW, PG = 2.62, 0.60
px = [0.62 + i * (PW + PG) for i in range(4)]
for i, (name, phase, body, col, first) in enumerate(plants):
    x = px[i]
    box(s, x, 1.54, PW, 1.22, fill=WHITE if not first else SOFT, line=col if first else RULE,
        lw=1.4 if first else 1.0, radius=0.05)
    box(s, x, 1.54, PW, 0.06, fill=col, line=None, radius=None)
    txt(s, x + 0.16, 1.66, PW - 0.32, 0.26, [(name, 11, True, col)])
    txt(s, x + 0.16, 1.94, PW - 0.32, 0.24, [(phase, 8.5, True, INK)])
    txt(s, x + 0.16, 2.22, PW - 0.32, 0.40, [(body, 8.5, None, GREY)], spacing=1.16)
    if i < 3:
        hline(s, x + PW + 0.04, 2.14, PG - 0.08, PALE)
        shape(s, MSO_SHAPE.DIAMOND, x + PW + PG / 2 - 0.11, 2.00, 0.22, 0.28,
              fill=WHITE, line=GOLD, lw=1.2)

for i in range(3):
    txt(s, px[i] + PW + 0.01, 2.32, PG - 0.02, 0.22,
        [("lulus uji", 6.4, True, GOLD)], align=PP_ALIGN.CENTER, spacing=1.0)

label(s, 1.10, 3.14, "YANG DIBAWA SAAT REPLIKASI", 5.6)
bring = [("Master line & mesin", "kode line, mesin, dan pemilik shift", NAVY),
         ("Template KPI versi", "target dan bobot per plant, berlaku per periode", NAVY),
         ("Aturan insight", "dua belas aturan yang sama, pemicu dibaca dari data", TEAL)]
y = 3.44
for head_, body, col in bring:
    box(s, 1.10, y, 5.55, 0.66, fill=WHITE, line=RULE, radius=0.05)
    box(s, 1.10, y, 0.05, 0.66, fill=col, line=None, radius=0.5)
    txt(s, 1.30, y + 0.07, 5.20, 0.22, [(head_, 9, True, col)])
    txt(s, 1.30, y + 0.31, 5.20, 0.28, [(body, 8.5, None, GREY)])
    y += 0.72

label(s, 7.16, 3.14, "YANG TETAP LOKAL DI TIAP PLANT", 5.5)
local = [("Target plant", "ditetapkan plant head, tidak dibawa dari Snack"),
         ("Kalender libur", "hari wajib mengikuti libur daerah masing-masing"),
         ("PIC dan approval", "nama pemilik kasus dan penyetuju lokal")]
y = 3.44
for head_, body in local:
    box(s, 7.16, y, 5.55, 0.66, fill=SOFT, line=RULE, radius=0.05)
    txt(s, 7.34, y + 0.07, 5.20, 0.22, [(head_, 9, True, NAVY)])
    txt(s, 7.34, y + 0.31, 5.20, 0.28, [(body, 8.5, None, GREY)])
    y += 0.72

box(s, 1.10, 5.62, 11.61, 0.52, fill=WHITE, line=RULE, radius=0.05)
box(s, 1.10, 5.62, 0.06, 0.52, fill=GOLD, line=None, radius=0.5)
txt(s, 1.40, 5.84, 3.30, 0.22,
    [("20 pekan · empat plant", 9, True, NAVY)])
txt(s, 5.00, 5.84, 7.50, 0.22,
    [("Gerbang G4 di Snack adalah syarat mulai replikasi pertama.", 9, None, INK)])


# ================================================================ 14 · CONTOH DATA
s = page("Potongan data yang dipakai di deck, semuanya dari tiga workbook",
         "Bagian 7 · data",
         note="Angka diambil langsung dari workbook Snack, Exist Plant, New Plant; tidak ada contoh yang dikarang")

# panel kiri · ringkasan vs isi tabel
box(s, 0.62, 1.24, 6.10, 2.96, fill=WHITE, line=RULE, radius=0.05)
txt(s, 0.82, 1.38, 5.70, 0.24, [("RINGKASAN DI SHEET BERBEDA DENGAN ISI TABEL", 10, True, GOLD)])
table(s, [
    ["Plant", "Ringkasan QC", "Tabel QC", "Ringkasan Prod", "Tabel Prod"],
    ["Snack", "1.018", "1.519", "988", "3.111"],
    ["Exist Plant", "993", "2.338", "977", "2.600"],
    ["New Plant", "999", "1.266", "1.003", "1.471"],
], [1.55, 1.15, 1.10, 1.20, 1.05], 0.82, 1.70, row_h=0.42, head_h=0.38, fs=10, head_fs=9.5,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER],
    bold_first=True)
txt(s, 0.82, 3.40, 5.66, 0.92,
    [("Blok ringkasan dan tabel dihitung terpisah, jadi angkanya berbeda sampai dua kali lipat.",
      9.5, None, GREY),
     ("Sistem membaca isi tabel, bukan ringkasan: satu baris kasus dihitung satu kali.",
      9.5, True, NAVY)], spacing=1.22)

# panel kanan · kolom yang masih kosong
box(s, 6.90, 1.24, 5.81, 3.22, fill=WHITE, line=RULE, radius=0.05)
txt(s, 7.10, 1.38, 5.41, 0.24, [("KOLOM YANG SERING KOSONG ATAU BERISI LAIN", 10, True, GOLD)])
rows_b = [("Due date di sheet SHE", "0%", "tidak ada tenggat, tidak ada yang menagih", RED),
          ("Bukti foto saat kasus ditutup", "4,5 – 22,6%", "sebagian besar tanpa bukti", RED),
          ("Sebab terisi · sheet SHE", "52 – 57%", "hampir separuh kasus tanpa sebab", GOLD),
          ("Sel berisi error (#VALUE!)", "153", "51 sel per plant, tidak terlihat", GOLD)]
yy = 1.70
for i, (name, val, sub, col) in enumerate(rows_b):
    txt(s, 7.10, yy, 3.30, 0.22, [(name, 9.5, None, INK)])
    txt(s, 10.55, yy - 0.04, 1.96, 0.28, [(val, 14, True, col)], align=PP_ALIGN.RIGHT)
    txt(s, 7.10, yy + 0.23, 5.30, 0.20, [(sub, 8.5, None, GREY)])
    if i:
        hline(s, 7.10, yy - 0.07, 5.30, RULE, 0.01)
    yy += 0.62
txt(s, 7.10, 4.06, 5.35, 0.30,
    [("Kolom kosong inilah yang diisi sistem sendiri: tenggat dihitung, bukti diminta, "
      "sel error tidak disimpan.", 9.5, True, NAVY)], spacing=1.2)

# tiga kartu penjelas
cards_d = [("Contoh, bukan angka baru",
            "Semua potongan di halaman ini dan di sepanjang deck berasal dari tiga workbook; "
            "angka lain tidak dipakai.", NAVY),
           ("Foto asli sudah dipakai",
            "Papan DMS di halaman 3, potongan tabel defect di halaman 2, dan papan PICA di "
            "halaman 12 memakai foto asli "
            "Factory 10, bukan gambar contoh.", TEAL),
           ("Cara memperbarui",
            "Jalankan analyze_workbook.py lalu build_deck.py; seluruh angka di deck ikut "
            "menyesuaikan.", GOLD)]
x = 1.10
for head_, body, col in cards_d:
    box(s, x, 4.68, 3.76, 1.50, fill=SOFT, line=RULE, radius=0.05)
    hline(s, x + 0.01, 4.68, 3.74, col, 0.06)
    txt(s, x + 0.20, 4.82, 3.40, 0.24, [(head_.upper(), 10, True, col)])
    txt(s, x + 0.20, 5.10, 3.40, 1.00, [(body, 9.8, None, INK)], spacing=1.22)
    x += 3.92


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
box(s, 8.42, 1.58, 4.28, 2.30, fill=None, line=RULE, radius=0.05)
txt(s, 8.64, 1.70, 3.90, 2.10,
    [("1. Tiga keputusan di atas diputuskan pada rapat ini.", 9.5, None, INK),
     ("2. Angka halaman 20 diambil ulang dari workbook sebelum rapat.", 9.5, None, INK),
     ("3. Pilot Snack, lalu Exist Plant dan New Plant dengan pola yang sama.", 9.5, None, INK),
     ("4. Evaluasi pekan ke-8 memakai lima ukuran keberhasilan.", 9.5, None, INK),
     ("5. Hasil keputusan dicatat pada berita acara dan disosialisasikan ke tiap plant.",
      9.5, None, INK)], spacing=1.42)

box(s, 8.42, 3.98, 4.28, 0.62, fill=SOFT, line=RULE, radius=0.05)
box(s, 8.42, 3.98, 0.06, 0.62, fill=GOLD, line=None, radius=0.5)
txt(s, 8.60, 4.06, 3.96, 0.48,
    [("Pemilik langkah: plant head tiap plant, diperiksa Group Manufacturing "
      "pada evaluasi pekan ke-8.", 8.5, None, GREY)], spacing=1.15)

hline(s, 0.62, 4.80, 12.09, RULE)
bx = 0.62
for title_, name_, date_ in [("Disusun oleh", "Tim Daily Monitoring System", "Tanggal: ..............."),
                             ("Diperiksa oleh", "Plant Head / Dept Head", "Tanggal: ..............."),
                             ("Disetujui oleh", "Group Manufacturing", "Tanggal: ...............")]:
    box(s, bx, 5.10, 3.86, 1.06, fill=SOFT, line=RULE, radius=0.05)
    txt(s, bx + 0.20, 5.20, 3.46, 0.24, [(title_.upper(), 9.5, True, NAVY)])
    txt(s, bx + 0.20, 5.48, 3.46, 0.26, [(name_, 11, True, INK)])
    txt(s, bx + 0.20, 5.86, 3.46, 0.24, [(date_, 9, None, GREY)])
    bx += 4.11


# ================================================================ 14 · TERIMA KASIH
close = prs.slides.add_slide(CLOSE_L)
for ph in list(close.placeholders):
    ph._element.getparent().remove(ph._element)

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides._sldIdLst))
