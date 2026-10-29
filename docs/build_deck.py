#!/usr/bin/env python3
"""
Deck DMS memakai template_master.pptx (versi terbaru):
  slide 1 template -> cover (panel putih judul)
  slide 2 template -> pola semua halaman isi (judul + area konten)
  slide 3 template -> halaman penutup

Isi 13 slide:
  1 cover · 2 kondisi + grafik kolom · 3 diagram alir harian
  4 diagram alir penutupan kasus · 5 struktur data · 6 rumus
  7 dua grafik batang · 8 mesin insight · 9 gantt · 10 kanal
  11 bahan gambar · 12 keputusan · 13 penutup

Jalankan: python3 docs/build_deck.py
Hasil  : docs/DMS_Digitalisasi_v1.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION

SRC = "template_master.pptx"
OUT = "docs/DMS_Digitalisasi_v1.pptx"

NAVY = RGBColor(0x1F, 0x33, 0x64)      # kuat / angka pokok
TEAL = RGBColor(0x2E, 0x86, 0x8C)      # terkendali / sudah baik
GOLD = RGBColor(0xC8, 0xA5, 0x2B)      # perlu perhatian
RED = RGBColor(0xB0, 0x2F, 0x2F)       # risiko / lewat batas
INK = RGBColor(0x22, 0x28, 0x33)
GREY = RGBColor(0x5C, 0x64, 0x72)
LGREY = RGBColor(0x8B, 0x93, 0xA1)
RULE = RGBColor(0xD5, 0xDA, 0xE3)
SOFT = RGBColor(0xF4, 0xF6, 0xFA)
PALE = RGBColor(0xD9, 0xDE, 0xE7)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)

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


def page(title, kicker, no, note=None):
    """Halaman isi memakai layout slide 2 template."""
    s = prs.slides.add_slide(BODY_L)
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx not in (0, 1):
            ph._element.getparent().remove(ph._element)
    title_ph = s.shapes.title
    n = len(title)
    size = 24 if n <= 46 else (22.5 if n <= 56 else 20.5)
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
    txt(s, 12.28, 0.26, 0.46, 0.28, [(str(no), 12, True, LGREY)], align=PP_ALIGN.RIGHT)
    if note:
        txt(s, 0.62, 6.98, 9.40, 0.26, [(note, 9, None, LGREY)])
    return s


def kpi_cards(s, items, y=1.24, h=1.06):
    n = len(items)
    gap = 0.10
    w = (12.09 - gap * (n - 1)) / n
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
txt(cover, 5.26, 1.98, 4.92, 0.30,
    [("Melanjutkan workbook Excel menjadi penilaian yang lebih terukur", 11, None, TEAL)],
    spacing=1.15)
txt(cover, 5.26, 2.32, 4.92, 0.26,
    [("Berlaku untuk Plant Snack, Dairy, Exist Plant, dan New Plant", 9.5, None, GREY)])
txt(cover, 5.26, 2.64, 4.92, 0.26,
    [("Dasar angka: 5.817 kasus pada workbook DMS 2023–2026", 9.5, True, NAVY)])

txt(cover, 10.68, 1.74, 2.42, 1.72,
    [("OKTOBER", 9.5, True, GOLD),
     ("2026", 27, True, NAVY),
     ("Tim Daily Monitoring System", 8.5, None, GREY),
     ("Group Manufacturing", 8.5, None, GREY)], spacing=1.12, anchor=MSO_ANCHOR.MIDDLE)


# ================================================================ 2 · KONDISI
s = page("Praktik hari ini sudah berjalan, angkanya lebih terbaca",
         "Bagian 1 · kondisi hari ini", 2,
         "Sumber: workbook DMS · Resume SHE, Resume QC, Resume Produksi")
kpi_cards(s, [("5.817", "kasus terdata", "tiga sheet resume", NAVY),
              ("973", "close tanpa sebab", "16,7% dari total", GOLD),
              ("94%", "label berulang keliru", "849 dari 902", GOLD),
              ("22", "kasus lewat tenggat", "tertua 1.045 hari", RED)])

label(s, 0.62, 2.44, "KASUS PER SHEET RESUME", 5.3)
chart(s, 0.52, 2.60, 5.40, 2.04,
      ["Resume SHE", "Resume QC", "Resume Produksi"],
      [("Kasus", [1185, 1520, 3112])],
      XL_CHART_TYPE.COLUMN_CLUSTERED, [NAVY], number_format="#,##0",
      fs=9, gap=90, label_pos=XL_LABEL_POSITION.OUTSIDE_END, vmax=3600,
      point_colors=[RGBColor(0x8F, 0xA1, 0xC4), RGBColor(0x4A, 0x5F, 0x94), NAVY])

label(s, 6.20, 2.44, "KELENGKAPAN DOKUMEN DI WORKBOOK", 6.4)
table(s, [
    ["Sheet", "Kasus", "Akar masalah", "Due date", "Bukti"],
    ["Resume SHE", "1.185", "0%", "0%", "0%"],
    ["Resume QC", "1.520", "79%", "100%", "–"],
    ["Resume Produksi", "3.112", "78%", "99%", "–"],
    ["IIAA Snack", "120", "duplikat", "–", "–"],
], [1.95, 1.05, 1.40, 1.15, 1.00], 6.20, 2.60, row_h=0.38, fs=10,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER],
    bold_first=True)
txt(s, 6.22, 4.50, 6.40, 0.28,
    [("Kolom kosong dihitung belum terisi; angka diambil apa adanya dari workbook.", 9, None, GREY)])

band = [("Sudah berjalan baik",
         "Semua plant mencatat harian pada workbook yang sama; 5.817 kasus dapat ditelusuri per sheet.",
         TEAL),
        ("Yang bisa dirapikan",
         "Kelengkapan sebab dan bukti belum merata: SHE 0%, QC 79%, Produksi 78%.",
         GOLD),
        ("Manfaat langsung",
         "Dengan data lebih lengkap, 973 kasus Close dapat diverifikasi tanpa input ulang.",
         NAVY)]
x = 0.62
for head, body, col in band:
    box(s, x, 4.90, 3.95, 1.54, fill=SOFT, line=RULE, radius=0.05)
    hline(s, x + 0.01, 4.90, 3.93, col, 0.06)
    txt(s, x + 0.20, 5.06, 3.58, 0.26, [(head.upper(), 10, True, col)])
    txt(s, x + 0.20, 5.38, 3.58, 0.94, [(body, 10, None, INK)], spacing=1.26)
    x += 4.07


# ================================================================ 3 · ALUR HARIAN
s = page("Alur harian: enam langkah dalam satu putaran",
         "Bagian 2 · diagram alir", 3,
         "Putaran Senin–Jumat; data hari libur tetap tersimpan sebagai arsip")
W, GAP, H = 3.44, 0.60, 1.64
X1 = 0.62
X2 = X1 + W + GAP
X3 = X2 + W + GAP
TOPY, BOTY = 1.54, 3.74

step(s, X1, TOPY, W, H, 1, "Input harian",
     "Leader line mengisi checklist per item untuk hari berjalan.", NAVY)
arrow(s, X1 + W + 0.14, TOPY + H / 2 - 0.17, GAP - 0.28, 0.34, "right", PALE)
step(s, X2, TOPY, W, H, 2, "Verifikasi",
     "DH memeriksa kelengkapan; item kurang dikembalikan hari itu.", NAVY)
arrow(s, X2 + W + 0.14, TOPY + H / 2 - 0.17, GAP - 0.28, 0.34, "right", PALE)
step(s, X3, TOPY, W, H, 3, "Hitung otomatis",
     "Skor item, Ach KPI, dan DMS Index dihitung sistem.", TEAL)

arrow(s, X3 + W / 2 - 0.17, TOPY + H + 0.08, 0.34, 0.40, "down", PALE)

step(s, X3, BOTY, W, H, 4, "Tampil di kanal",
     "Dasbor L1–L3 dan layar TV membaca angka yang sama.", TEAL)
arrow(s, X3 - GAP + 0.14, BOTY + H / 2 - 0.17, GAP - 0.28, 0.34, "left", PALE)
step(s, X2, BOTY, W, H, 5, "Insight & eskalasi",
     "Aturan I-01…I-12 memilih temuan, pemilik, dan tenggat.", GOLD)
arrow(s, X2 - GAP + 0.14, BOTY + H / 2 - 0.17, GAP - 0.28, 0.34, "left", PALE)
step(s, X1, BOTY, W, H, 6, "Tindak lanjut",
     "Kasus ditutup setelah sebab, tindakan, bukti, dan PIC lengkap.", GOLD)

box(s, X1 + W / 2 - 0.01, BOTY + H + 0.06, 0.02, 0.18, fill=PALE, line=None, radius=None)
box(s, X1 + W / 2 - 0.01, BOTY + H + 0.22, 8.56, 0.02, fill=PALE, line=None, radius=None)
txt(s, X1 + W / 2 + 0.20, 5.44, 8.30, 0.26,
    [("Data tersimpan otomatis; putaran berikutnya mulai lagi dari langkah 1", 9.5, None, LGREY)])

legend = [("Leader line", "mengisi form harian per item checklist", NAVY),
          ("DH & supervisor", "memverifikasi, menetapkan pemilik dan tenggat", TEAL),
          ("Admin plant", "mengunci periode, mengatur KPI dan Healthy Check", GOLD)]
x = 0.62
for head, body, col in legend:
    box(s, x, 5.86, 3.95, 0.92, fill=SOFT, line=RULE, radius=0.05)
    box(s, x + 0.18, 6.02, 0.12, 0.12, fill=col, radius=0.3)
    txt(s, x + 0.40, 5.96, 3.40, 0.24, [(head, 10, True, NAVY)])
    txt(s, x + 0.40, 6.24, 3.40, 0.44, [(body, 9, None, GREY)], spacing=1.18)
    x += 4.07


# ================================================================ 4 · ALUR PENUTUPAN
s = page("Penutupan kasus memakai gerbang empat kolom",
         "Bagian 2 · diagram alir", 4,
         "Gerbang inilah yang membuat status Close dapat dipertanggungjawabkan")

CX, CW = 4.86, 3.70
box(s, CX, 1.34, CW, 0.60, fill=NAVY, line=None, radius=0.05)
txt(s, CX, 1.40, CW, 0.48, [("Kasus terbuka · defect · downtime · audit", 10, True, WHITE)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
arrow(s, CX + CW / 2 - 0.17, 1.96, 0.34, 0.22, "down", PALE)

box(s, CX, 2.18, CW, 0.76, fill=WHITE, line=RULE, radius=0.05)
txt(s, CX + 0.18, 2.26, CW - 0.36, 0.60,
    [("Isi sebab · tindakan · bukti · PIC", 10.5, True, NAVY),
     ("minimal satu foto atau dokumen per kasus", 9, None, GREY)], spacing=1.18)
arrow(s, CX + CW / 2 - 0.17, 2.96, 0.34, 0.20, "down", PALE)

shape(s, MSO_SHAPE.DIAMOND, CX + 0.30, 3.16, CW - 0.60, 1.04,
      fill=RGBColor(0xF7, 0xF1, 0xDD), line=GOLD, lw=1.25)
txt(s, CX + 0.56, 3.40, CW - 1.12, 0.56,
    [("Empat kolom lengkap?", 10, True, NAVY)], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

arrow(s, CX - 0.50, 3.52, 0.44, 0.32, "left", GOLD)
txt(s, 1.52, 3.28, 2.10, 0.24, [("Tidak", 9, True, GOLD)], align=PP_ALIGN.CENTER)
box(s, 0.62, 3.84, 3.30, 0.94, fill=WHITE, line=GOLD, radius=0.05)
txt(s, 0.82, 3.94, 2.94, 0.76,
    [("Kembali ke PIC", 10.5, True, NAVY),
     ("aging bertambah; kartu tampil di layar TV sampai dilengkapi", 9, None, GREY)], spacing=1.2)

arrow(s, CX + CW / 2 - 0.17, 4.22, 0.34, 0.20, "down", TEAL)
txt(s, CX + CW / 2 + 0.24, 4.18, 0.80, 0.24, [("Ya", 9, True, TEAL)])

box(s, CX, 4.44, CW, 0.60, fill=WHITE, line=RULE, radius=0.05)
txt(s, CX, 4.50, CW, 0.48, [("Review & persetujuan DH / Plant Head", 10.5, True, NAVY)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
arrow(s, CX + CW / 2 - 0.17, 5.06, 0.34, 0.20, "down", PALE)

shape(s, MSO_SHAPE.DIAMOND, CX + 0.82, 5.28, CW - 1.64, 0.86,
      fill=RGBColor(0xE8, 0xF3, 0xF4), line=TEAL, lw=1.25)
txt(s, CX + 1.02, 5.42, CW - 2.04, 0.56, [("Disetujui?", 10, True, NAVY)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

arrow(s, CX + CW + 0.02, 5.56, 0.34, 0.30, "right", GOLD)
box(s, 8.94, 5.30, 3.78, 0.86, fill=WHITE, line=GOLD, radius=0.05)
txt(s, 9.12, 5.40, 3.44, 0.70,
    [("Revisi bukti atau sebab", 10, True, NAVY),
     ("kasus tetap terbuka dan tetap terhitung dalam aging", 9, None, GREY)], spacing=1.18)
txt(s, 9.02, 6.22, 3.60, 0.24, [("Tidak", 9, True, GOLD)])

arrow(s, CX + CW / 2 - 0.17, 6.16, 0.34, 0.18, "down", TEAL)
box(s, CX - 0.40, 6.38, CW + 0.80, 0.48, fill=TEAL, line=None, radius=0.05)
txt(s, CX - 0.40, 6.44, CW + 0.80, 0.36,
    [("Kasus ditutup, skor periode dikunci", 10, True, WHITE)],
    align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

label(s, 9.00, 1.30, "KENAPA GERBANG INI PERLU", 3.60)
gates = [("973", "kasus berstatus Close tanpa sebab tercatat"),
         ("0%", "bukti foto pada sheet Resume SHE"),
         ("22", "kasus melewati tenggat, tertua 1.045 hari")]
y = 1.62
for v, body in gates:
    txt(s, 9.00, y, 1.15, 0.34, [(v, 15, True, NAVY)])
    txt(s, 10.20, y + 0.02, 2.50, 0.62, [(body, 9, None, GREY)], spacing=1.18)
    y += 0.74

box(s, 9.00, 3.94, 3.60, 1.30, fill=SOFT, line=RULE, radius=0.05)
txt(s, 9.18, 4.06, 3.24, 0.24, [("JEJAK AUDIT", 9, True, GOLD)])
txt(s, 9.18, 4.32, 3.24, 0.84,
    [("Setiap perubahan mencatat siapa, kapan, dan nilai sebelum–sesudah; "
      "periode yang sudah dilaporkan tidak dapat diubah.", 9, None, GREY)], spacing=1.2)


# ================================================================ 5 · STRUKTUR DATA
s = page("Satu kerangka data untuk empat plant",
         "Bagian 2 · struktur data", 5,
         "Nama level mengikuti workbook: Group, Plant, Factory/BU, Line")
levels = [("Group", "Manufacturing", "kebijakan & pembanding antar plant", NAVY),
          ("Plant", "Snack · Dairy · Exist · New", "KPI dan Hari Libur per plant", TEAL),
          ("Factory / BU", "contoh: Snack", "pemilik anggaran perbaikan", TEAL),
          ("Line & mesin", "Pilus L1 · M03 · MHM", "unit penilaian harian", GOLD),
          ("Item harian", "6 item checklist", "titik data terkecil", GOLD)]
x = 0.62
for i, (name, sub, body, col) in enumerate(levels):
    box(s, x, 1.62, 2.26, 1.72, fill=WHITE, line=RULE, radius=0.05)
    hline(s, x + 0.01, 1.62, 2.24, col, 0.06)
    txt(s, x + 0.16, 1.78, 1.94, 0.28, [(name, 12.5, True, NAVY)])
    txt(s, x + 0.16, 2.10, 1.94, 0.40, [(sub, 9, True, col)], spacing=1.12)
    txt(s, x + 0.16, 2.56, 1.94, 0.68, [(body, 9, None, GREY)], spacing=1.2)
    if i < len(levels) - 1:
        arrow(s, x + 2.30, 2.32, 0.26, 0.30, "right", PALE)
    x += 2.56

label(s, 0.62, 3.62, "ATURAN YANG MENJAGA ANGKA TETAP SAMA DI SEMUA PLANT", 12.0)
rules = [("Satu template inti", "Enam item checklist, bobot 10/20/10/20/20/20, dan band skor sama untuk semua plant.", NAVY),
         ("KPI plant berversi", "Setiap plant dapat menambah KPI sendiri; versi dan tanggal berlaku tersimpan.", TEAL),
         ("Skor proses & hasil", "Kepatuhan mengisi dinilai terpisah dari capaian hasil line.", TEAL),
         ("Pekan ISO, Senin–Jumat", "Hari wajib dikurangi hari libur plant agar penyebut setara.", GOLD)]
x = 0.62
for head, body, col in rules:
    box(s, x, 3.92, 2.95, 1.60, fill=SOFT, line=RULE, radius=0.05)
    hline(s, x + 0.01, 3.92, 2.93, col, 0.05)
    txt(s, x + 0.18, 4.06, 2.60, 0.50, [(head, 10.5, True, col)], spacing=1.12)
    txt(s, x + 0.18, 4.62, 2.60, 0.82, [(body, 9.5, None, GREY)], spacing=1.22)
    x += 3.04

box(s, 0.62, 5.72, 12.09, 0.82, fill=WHITE, line=RULE, radius=0.05)
txt(s, 0.82, 5.84, 11.70, 0.62,
    [("Contoh penelusuran  ·  kasus Pilus L1 dapat ditelusuri sampai item checklist, lalu "
      "dibandingkan dengan line lain di plant yang sama tanpa mengubah definisi skor.", 10, None, GREY)],
    spacing=1.25)


# ================================================================ 6 · RUMUS
s = page("Rumus final: tiga penyempurnaan, hasil lebih tepat",
         "Bagian 3 · rumus", 6,
         "Bobot dan band tetap mengikuti workbook; yang disempurnakan penyebut dan pembulatan")
table(s, [
    ["Komponen", "Rumus / nilai", "Keterangan"],
    ["Nilai harian", "Σ (skor item ÷ 10 × bobot) ÷ 100", "bobot 10/20/10/20/20/20 = 100"],
    ["Ach KPI", "V ÷ (V + O)", "harian bersifat biner Valid / Open"],
    ["Ach checklist", "Σ nilai harian ÷ (hari kerja × 0,8)", "target 0,8 per hari"],
    ["Band skor", "≥120% = 5 · ≥110% = 4 · ≥100% = 3 · ≥90% = 2 · <90% = 1", "bandingkan 2 desimal"],
    ["DMS Index", "0,4 × KPI + 0,4 × checklist + 0,2 × healthy", "target 3,00 dari maksimum 5"],
], [1.50, 4.05, 3.25], 0.62, 1.26, row_h=0.46, head_h=0.36, fs=10, bold_first=True)

label(s, 0.62, 4.06, "TIGA PENYEMPURNAAN DAN HASILNYA", 8.4)
table(s, [
    ["Penyempurnaan", "Di workbook", "Di aplikasi"],
    ["Penyebut memakai hari kerja", "1 hari isi = Ach 125%", "1 dari 5 hari = Ach 20%"],
    ["Ambang dibandingkan 2 desimal", "1,0999 → skor 3", "110% → skor 4"],
    ["Healthy Check jadi parameter", "tetap 0,8", "dapat diubah Admin, bertanggal"],
], [3.35, 2.45, 2.35], 0.62, 4.38, row_h=0.40, head_h=0.36, fs=9.5)

img_slot(s, 10.02, 1.26, 2.68, 2.10, "Screenshot Sheet1",
         "sorot kolom ISO week sebagai dasar pekan")
txt(s, 10.02, 3.50, 2.68, 1.00,
    [("Pekan memakai ISO week. Hari wajib Senin–Jumat dikurangi hari libur, "
      "sehingga jumlah hari penilaian sama untuk semua line.", 9, None, GREY)], spacing=1.2)

label(s, 10.02, 4.62, "DAMPAK PADA KPI", 3.0)
imp = [("Capaian lebih adil", "SHE yang tercatat 0% root cause punya jalur perbaikan terukur.", TEAL),
       ("Tidak bisa diisi manual", "On-time dan kelengkapan dihitung sistem, bukan diketik.", NAVY),
       ("Bisa diaudit", "Perubahan skor tercatat siapa dan kapan; periode dikunci.", GOLD)]
y = 4.92
for head, body, col in imp:
    box(s, 10.02, y, 2.68, 0.68, fill=SOFT, line=RULE, radius=0.05)
    box(s, 10.02, y, 0.06, 0.68, fill=col, line=None, radius=0.5)
    txt(s, 10.18, y + 0.06, 2.44, 0.22, [(head, 9, True, col)])
    txt(s, 10.18, y + 0.30, 2.44, 0.34, [(body, 8, None, GREY)], spacing=1.14)
    y += 0.74


# ================================================================ 7 · GRAFIK DATA
s = page("Kelengkapan sebab dan bukti belum merata",
         "Bagian 3 · data", 7,
         "Sumber: Resume SHE, Resume QC, Resume Produksi; downtime dari catatan line")
label(s, 0.62, 1.26, "ROOT CAUSE TERISI PER SHEET (%)", 6.0)
chart(s, 0.52, 1.44, 6.20, 2.66,
      ["Resume SHE", "Resume QC", "Resume Produksi"],
      [("Terisi", [0, 79, 78]), ("Belum terisi", [100, 21, 22])],
      XL_CHART_TYPE.BAR_STACKED_100, [TEAL, PALE], number_format='0"%"',
      legend=True, fs=9, gap=70, label_pos=XL_LABEL_POSITION.CENTER, label_color=WHITE, vmax=1.0)
txt(s, 0.62, 4.16, 6.10, 0.28,
    [("Sheet SHE belum menyimpan sebab; dua sheet lain sudah 78–79%.", 9, None, GREY)])

label(s, 6.86, 1.26, "PANGSA DOWNTIME MESIN · CONTOH PLANT SNACK (%)", 5.9)
chart(s, 6.72, 1.44, 5.99, 2.66,
      ["MHM", "BCAT", "Mesin lain"],
      [("Pangsa", [26.8, 14.1, 59.1])],
      XL_CHART_TYPE.BAR_CLUSTERED, [NAVY], number_format='0.0"%"',
      fs=9, gap=65, label_pos=XL_LABEL_POSITION.OUTSIDE_END, vmax=70,
      point_colors=[RED, GOLD, PALE])
txt(s, 6.88, 4.16, 5.85, 0.28,
    [("Dua mesin menyumbang 40,9% downtime — layak menjadi kartu tetap di layar lantai.",
      9, None, GREY)])

label(s, 0.62, 4.56, "EMPAT ANGKA YANG MENJADI PRIORITAS PERBAIKAN", 12.0)
findings = [("973", "Kasus ditutup tanpa sebab tercatat — 16,7% dari 5.817 kasus.", GOLD),
            ("184", "Pola berulang ≥3× mencakup 816 kasus atau 26,2% seluruh kasus.", GOLD),
            ("849 / 902", "Label berulang diisi manual dan 94% di antaranya keliru.", RED),
            ("22", "Kasus melewati tenggat, tertua 1.045 hari sejak dibuka.", RED)]
x = 0.62
for v, body, col in findings:
    box(s, x, 4.86, 2.95, 1.50, fill=SOFT, line=RULE, radius=0.05)
    box(s, x, 4.86, 2.95, 0.06, fill=col, line=None, radius=None)
    txt(s, x + 0.18, 5.00, 2.60, 0.40, [(v, 20, True, col)])
    txt(s, x + 0.18, 5.44, 2.60, 0.82, [(body, 9, None, GREY)], spacing=1.2)
    x += 3.04


# ================================================================ 8 · INSIGHT
s = page("Mesin insight: 12 aturan siap pakai", "Bagian 4 · insight", 8,
         "Setiap temuan membawa bukti, sebab, dampak, rekomendasi, dan pemilik")
table(s, [
    ["Kode", "Pemicu", "Contoh keluaran", "Kanal"],
    ["I-01", "Hari kerja tanpa meeting", "Line tidak DMS 3 hari berturut", "L1 · TV"],
    ["I-02", "Tenggat lewat, status terbuka", "22 kasus; tertua 1.045 hari", "TV · L1"],
    ["I-03", "Signature sama ≥3× per 90 hari", "M03 BCAT 15× di Pilus L1", "TV · L2"],
    ["I-04", "Berulang dengan sebab identik", "Correction sama 4× → Preventive", "L2"],
    ["I-05", "Tutup, tetapi OPL/PM/AM/CRMO = O", "88–98% kasus belum distandarkan", "L2 · L3"],
    ["I-06", "Tutup tanpa sebab atau bukti", "973 kasus", "Admin"],
    ["I-07", "Prioritas High di atas 80%", "prioritas belum membedakan", "Admin"],
    ["I-08", "Ach dalam 1% di bawah band", "rawan selisih pembulatan", "Admin"],
    ["I-09", "Tiga periode menurun", "checklist turun 4% per pekan", "L2 · L3"],
    ["I-10", "Satu line atau mesin di atas 20%", "Pilus L1 = 90% kasus", "L3"],
    ["I-11", "Downtime besar dan sering", "MHM 26,8% · BCAT 14,1%", "L2"],
    ["I-12", "PICA lemah, kasus baru naik", "prediksi lonjakan pekan depan", "L3"],
], [0.70, 2.86, 3.96, 1.18], 0.62, 1.24, row_h=0.355, head_h=0.34, fs=9,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER])

txt(s, 0.62, 6.10, 8.30, 0.70,
    [("Peringkat = dampak × volume × kebaruan × (controllable ? 1 : 0,5).", 10, True, NAVY),
     ("Maksimal tiga kartu tampil di layar lantai; sisanya di dasbor supervisor dan admin.",
      9.5, None, GREY)], spacing=1.3)

img_slot(s, 10.06, 1.24, 2.64, 2.10, "Mockup 3 kartu TV",
         "satu kartu = satu temuan + pemilik + tenggat")

box(s, 10.06, 3.50, 2.64, 2.36, fill=SOFT, line=RULE, radius=0.05)
txt(s, 10.24, 3.64, 2.28, 0.24, [("CARA MEMBACA TABEL", 9, True, GOLD)])
txt(s, 10.24, 3.92, 2.28, 1.86,
    [("Kanal menunjukkan siapa penerima kartu: layar lantai, dasbor L1, L2, atau L3.", 9, None, GREY),
     ("Satu kartu memuat satu temuan, bukan satu daftar.", 9, None, GREY),
     ("Angka pemicu memakai contoh workbook: 22, 973, 26,8%, 14,1%.", 9, None, GREY)],
    spacing=1.25)


# ================================================================ 9 · RENCANA
s = page("Rencana 8 pekan: fondasi dulu, tampilan terakhir",
         "Bagian 5 · rencana", 9,
         "Pilot Plant Snack, lalu Exist Plant, Dairy, dan New Plant")

phases = [("0 · Fondasi", 1, 2, "master data, aturan skor, hak akses", NAVY),
          ("1 · Capture", 1, 3, "form harian dan form kasus", NAVY),
          ("2 · Measure", 3, 5, "perhitungan skor, dasbor line", TEAL),
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
    ["Ukuran", "Baseline hari ini", "Target pekan ke-8", "Cara ukur"],
    ["Kepatuhan mengisi form", "belum terukur", "≥ 90%", "hari terisi ÷ hari wajib"],
    ["Kelengkapan root cause", "0% SHE · 79% QC · 78% Produksi", "≥ 95%", "kolom sebab terisi"],
    ["Kasus lewat tenggat", "22 kasus", "turun 50%", "aging > tenggat"],
    ["Pola ≥3× punya tindakan", "belum ada", "100%", "pola dengan PICA tertutup"],
    ["Insight ditindaklanjuti", "belum ada", "≥ 70%", "kartu dengan tindak lanjut"],
], [3.05, 3.50, 1.75, 3.79], 0.62, 4.72, row_h=0.36, head_h=0.34, fs=9.5, bold_first=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT])


# ================================================================ 10 · KANAL
s = page("Empat kanal tampilan dan batasannya", "Bagian 5 · tampilan", 10,
         "Struktur final; gambar antarmuka menyusul")
cards = [("Form harian", "Leader & DH", "satu layar, di bawah 5 menit",
          "Isi harian per line: item checklist, status, sebab bila di bawah target.", NAVY),
         ("Dasbor L1–L3", "Supervisor, plant head", "tiga tingkat audiens",
          "L1 memantau hari ini, L2 menutup kasus, L3 membandingkan plant.", TEAL),
         ("Layar lantai (TV)", "Area produksi", "tanpa interaksi, rotasi 30 detik",
          "Kartu temuan terbuka: sebab, PIC, tenggat hitung mundur, foto bukti.", TEAL),
         ("Halaman admin", "Admin plant & group", "persetujuan, konfigurasi, audit",
          "Kelola pengguna, KPI plant, Healthy Check, tata letak kartu TV.", GOLD)]
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
    ["Satu sumber angka", "Semua kanal membaca dari perhitungan yang sama"],
    ["Empat kolom wajib", "Sebab, tindakan, bukti, dan PIC sebelum kasus ditutup"],
    ["Kunci periode", "Skor periode yang sudah dilaporkan tidak dapat diubah"],
    ["Jejak audit", "Setiap perubahan tercatat: siapa, kapan, sebelum–sesudah"],
], [2.25, 6.35], 0.62, 3.42, row_h=0.42, head_h=0.36, fs=10, bold_first=True)

img_slot(s, 9.90, 3.42, 2.80, 1.92, "Mockup layar TV", "tangkapan layar atau desain akhir")

label(s, 0.62, 6.04, "YANG TIDAK DIBUAT SEKARANG", 12.0)
notes = [("Tanpa aplikasi mobile", "form harian cukup berbasis web pada fase 1"),
         ("Tanpa login TV", "layar lantai hanya menampilkan, hak ubah di User & Admin"),
         ("Tanpa angka manual", "semua kanal membaca satu perhitungan; manual hanya Healthy Check")]
x = 0.62
for head, body in notes:
    txt(s, x, 6.34, 3.90, 0.24, [(head, 9.5, True, NAVY)])
    txt(s, x, 6.60, 3.90, 0.28, [(body, 9, None, GREY)])
    x += 4.07


# ================================================================ 11 · BAHAN GAMBAR
s = page("Daftar bahan gambar yang harus di-screenshot", "Bagian 5 · bahan", 11,
         "Dikumpulkan sebelum deck dipresentasikan; semua bersumber dari workbook dan lantai")
table(s, [
    ["#", "Yang di-screenshot / difoto", "Diambil dari", "Halaman", "Sorotan"],
    ["1", "Sheet Resume SHE", "workbook · Resume SHE", "2, 7", "kolom root cause, due date, bukti 0%"],
    ["2", "Sheet Resume QC", "workbook · Resume QC", "2, 7", "320 baris Close tanpa sebab"],
    ["3", "Sheet Resume Produksi", "workbook · Resume Produksi", "2, 7", "653 baris Close tanpa sebab"],
    ["4", "Sheet Template Penilaian", "workbook · Template Penilaian", "6", "formula AVERAGEIF dan band skor"],
    ["5", "Sheet Sheet1", "workbook · Sheet1", "6", "kolom ISO week"],
    ["6", "Sheet IIAA Snack", "workbook · IIAA Snack", "2", "baris duplikat"],
    ["7", "Papan monitoring line", "lantai produksi", "3", "checklist yang diisi tangan"],
    ["8", "Form checklist terisi", "line · dokumen cetak", "3", "item yang dinilai persepsi"],
    ["9", "Foto rapat pagi", "area meeting line", "3", "langkah 1–2 saat berjalan"],
    ["10", "Foto mesin / area", "Pilus L1 dan MHM (contoh)", "7", "sumber downtime terbesar"],
    ["11", "Screenshot laporan harian", "WhatsApp atau email group", "2", "alur laporan sekarang"],
    ["12", "Screenshot layar TV (bila ada)", "area produksi", "10", "pembanding tampilan baru"],
], [0.50, 3.30, 3.45, 1.25, 3.45], 0.62, 1.24, row_h=0.395, head_h=0.36, fs=9.5, head_fs=10,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT])

box(s, 0.62, 6.12, 12.09, 0.72, fill=SOFT, line=RULE, radius=0.05)
txt(s, 0.82, 6.22, 11.70, 0.52,
    [("Cara mengambil  ·  tampilkan nama sheet, header kolom, dan 5–10 baris contoh; blok kolom "
      "yang kosong agar terlihat. Foto lapangan landscape minimal 1600 px dan diberi tanggal.",
      9.5, None, GREY)], spacing=1.22)


# ================================================================ 12 · KEPUTUSAN
s = page("Keputusan yang diminta dan langkah berikutnya", "Penutup · keputusan", 12,
         "Semua keputusan mengacu pada angka workbook; tidak ada tambahan asumsi baru")

label(s, 0.62, 1.26, "TIGA KEPUTUSAN TERBUKA", 4.15)
dec = [("1 · Kalender hari libur",
        "Master tahunan diisi sekali, atau input per tanggal? Penyebut skor bergantung pada jawaban ini."),
       ("2 · Status N/A pada KPI",
        "Item yang tidak relevan keluar dari penyebut, atau tetap dihitung nol?"),
       ("3 · Data historis",
        "5.817 kasus dibawa dengan penanda lama, atau mulai dari nol?")]
y = 1.58
for name, q in dec:
    box(s, 0.62, y, 4.15, 0.98, fill=SOFT, line=RULE, radius=0.05)
    txt(s, 0.80, y + 0.10, 3.80, 0.24, [(name, 10.5, True, NAVY)])
    txt(s, 0.80, y + 0.38, 3.80, 0.54, [(q, 9, None, GREY)], spacing=1.2)
    y += 1.06

label(s, 5.02, 1.26, "ANGKA YANG MENJADI DASAR", 3.20)
nums = [("5.817", "kasus terdata", NAVY), ("973", "close tanpa sebab", GOLD),
        ("94%", "label berulang keliru", RED), ("22", "kasus lewat tenggat", RED),
        ("184", "pola berulang ≥3×", GOLD)]
y = 1.58
for v, l, col in nums:
    txt(s, 5.02, y, 1.25, 0.32, [(v, 16, True, col)])
    txt(s, 6.28, y + 0.06, 1.95, 0.24, [(l, 9, None, GREY)])
    hline(s, 5.02, y + 0.36, 3.20, RULE)
    y += 0.48

label(s, 8.42, 1.26, "LANGKAH SETELAH SESI", 4.28)
box(s, 8.42, 1.58, 4.28, 3.02, fill=None, line=RULE, radius=0.05)
txt(s, 8.64, 1.74, 3.90, 2.74,
    [("1. Tiga keputusan di atas diputuskan pada rapat ini.", 9.5, None, INK),
     ("2. Bahan gambar halaman 11 dikumpulkan maksimal tiga hari kerja.", 9.5, None, INK),
     ("3. Pilot Plant Snack mulai pekan berikutnya, fase 0 dua pekan.", 9.5, None, INK),
     ("4. Evaluasi pekan ke-8 memakai lima ukuran keberhasilan.", 9.5, None, INK),
     ("5. Hasil keputusan dicatat pada berita acara dan disosialisasikan ke empat plant.",
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


# ================================================================ 13 · TERIMA KASIH
close = prs.slides.add_slide(CLOSE_L)
for ph in list(close.placeholders):
    ph._element.getparent().remove(ph._element)

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides._sldIdLst))
