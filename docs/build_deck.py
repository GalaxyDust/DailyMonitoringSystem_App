#!/usr/bin/env python3
# Jalankan dari root repo: python3 docs/build_deck.py  ->  menghasilkan docs/DMS_Digitalisasi_v1.pptx
# Build DMS deck on top of the user's template_master.pptx (GarudaFood theme)
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import copy

SRC = "template_master.pptx"
OUT = "docs/DMS_Digitalisasi_v1.pptx"

NAVY   = RGBColor(0x07, 0x1B, 0x56)
NAVY2  = RGBColor(0x00, 0x20, 0x60)
GOLD   = RGBColor(0xC3, 0x9E, 0x1A)
TEAL   = RGBColor(0x40, 0xC0, 0xBF)
GREY   = RGBColor(0x59, 0x59, 0x59)
LGREY  = RGBColor(0x7F, 0x7F, 0x7F)
LIGHT  = RGBColor(0xEE, 0xF1, 0xF7)
LIGHT2 = RGBColor(0xF7, 0xF8, 0xFB)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
RED    = RGBColor(0xC0, 0x00, 0x00)
AMBER  = RGBColor(0xD9, 0x7A, 0x1E)
GREEN  = RGBColor(0x4F, 0x7B, 0x2F)
BORDER = RGBColor(0xC8, 0xCF, 0xDD)

prs = Presentation(SRC)
# remove all existing slides, keep masters/layouts/theme
xml_slides = prs.slides._sldIdLst
for sldId in list(xml_slides):
    rId = sldId.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
    prs.part.drop_rel(rId)
    xml_slides.remove(sldId)

L_CONTENT = prs.slide_layouts[4]   # 1_Title and Content (light bg)
L_COVER   = prs.slide_layouts[1]   # Title Slide (eagle)
L_CLOSING = prs.slide_layouts[5]   # 2_Title Slide (Thank You)

def clear_placeholders(slide, keep=None):
    for sh in list(slide.shapes):
        if sh.is_placeholder and (keep is None or sh.placeholder_format.idx not in keep):
            sh._element.getparent().remove(sh._element)

def tb(slide, x, y, w, h, text, size=12, bold=False, color=NAVY, align=PP_ALIGN.LEFT,
       font="Calibri", anchor=MSO_ANCHOR.TOP, spacing=None, line=None, wrap=True):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0; tf.margin_right = 0; tf.margin_top = 0; tf.margin_bottom = 0
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if spacing: p.space_after = Pt(spacing)
        if line: p.line_spacing = line
        r = p.add_run(); r.text = ln
        r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = font
    return box

def rect(slide, x, y, w, h, fill=None, line_color=None, line_w=1.0, shape=MSO_SHAPE.RECTANGLE, radius=None):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        s.fill.background()
    else:
        s.fill.solid(); s.fill.fore_color.rgb = fill
    if line_color is None:
        s.line.fill.background()
    else:
        s.line.color.rgb = line_color; s.line.width = Pt(line_w)
    s.shadow.inherit = False
    if radius is not None and shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        s.adjustments[0] = radius
    return s

def header(slide, title, kicker=None):
    rect(slide, 0, 0.08, 13.33, 0.56, fill=NAVY2)
    rect(slide, 0, 0.64, 13.33, 0.035, fill=GOLD)
    tb(slide, 0.30, 0.16, 12.6, 0.36, title, size=22, bold=True, color=WHITE)
    if kicker:
        tb(slide, 0.30, 0.78, 12.7, 0.28, kicker, size=11, bold=True, color=GOLD)

def footer(slide, n, note="Digitalisasi DMS · Pilot Snack · v1"):
    tb(slide, 0.30, 7.06, 8.0, 0.24, note, size=8.5, color=LGREY)
    tb(slide, 11.9, 7.06, 1.1, 0.24, str(n), size=8.5, color=LGREY, align=PP_ALIGN.RIGHT)

def est_lines(text, w, size, bold=False):
    em = 0.545 if bold else 0.500
    cw = em * size / 72.0
    cpl = max(int(w / cw), 10)
    return max(1, -(-len(text) // cpl))

def bullets(slide, x, y, w, items, size=13, color=NAVY, gap=8, bullet_color=GOLD, line=None):
    top = y
    tw = w - 0.22
    for it in items:
        if isinstance(it, tuple):
            head, sub = it
        else:
            head, sub = it, None
        hl = est_lines(head, tw, size, True)
        hh = hl * size * 1.24 / 72.0
        rect(slide, x, top + 0.075, 0.075, 0.075, fill=bullet_color)
        tb(slide, x + 0.22, top, tw, hh, head, size=size, bold=True, color=color, line=1.15)
        top += hh + 0.03
        if sub:
            ss = size - 2
            sl = est_lines(sub, tw, ss, False)
            sh = sl * ss * 1.26 / 72.0
            tb(slide, x + 0.22, top, tw, sh, sub, size=ss, color=GREY, line=1.2)
            top += sh
        top += gap / 72.0
    return top

def table(slide, data, col_w, x=0.42, y=1.18, row_h=0.30, font=10, head_font=10,
          head_fill=NAVY2, zebra=True, first_col_bold=False, aligns=None):
    rows, cols = len(data), len(data[0])
    shape = slide.shapes.add_table(rows, cols, Inches(x), Inches(y),
                                   Inches(sum(col_w)), Inches(row_h * rows))
    tbl = shape.table
    tbl.first_row = True
    tbl.horz_banding = False
    for i, w in enumerate(col_w):
        tbl.columns[i].width = Inches(w)
    for r in range(rows):
        tbl.rows[r].height = Inches(row_h)
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left = Inches(0.06); cell.margin_right = Inches(0.06)
            cell.margin_top = Inches(0.02); cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r == 0:
                cell.fill.fore_color.rgb = head_fill
            elif zebra and r % 2 == 0:
                cell.fill.fore_color.rgb = LIGHT2
            else:
                cell.fill.fore_color.rgb = WHITE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = (aligns[c] if aligns else (PP_ALIGN.LEFT if c == 0 else PP_ALIGN.LEFT))
            run = p.add_run(); run.text = str(data[r][c])
            run.font.size = Pt(head_font if r == 0 else font)
            run.font.bold = (r == 0) or (first_col_bold and c == 0)
            run.font.name = "Calibri"
            run.font.color.rgb = WHITE if r == 0 else NAVY
    return shape

def code_box(slide, x, y, w, h, text, size=None, mono_w=0.555):
    rect(slide, x, y, w, h, fill=RGBColor(0xF4, 0xF6, 0xFA), line_color=BORDER, line_w=0.75)
    rect(slide, x, y, 0.06, h, fill=GOLD)
    lines = text.split("\n")
    nlines = len(lines)
    maxlen = max(len(l) for l in lines)
    if size is None:
        by_h = (h - 0.22) * 72.0 / (nlines * 1.16)
        by_w = (w - 0.38) * 72.0 / (maxlen * mono_w)
        size = min(by_h, by_w, 13.0)
    b = tb(slide, x + 0.20, y + 0.11, w - 0.32, h - 0.20, text, size=size, font="Consolas",
           color=RGBColor(0x1F, 0x2A, 0x44), line=1.06)
    return b


def panel(lines, seps=()):
    W = max(len(l) for l in lines) + 2
    out = ["┌" + "─" * W + "┐"]
    for i, l in enumerate(lines):
        out.append("│ " + l.ljust(W - 2) + " │")
        if i in seps:
            out.append("├" + "─" * W + "┤")
    out.append("└" + "─" * W + "┘")
    return out

def two_col(left, right, gap=3):
    W1 = max(len(l) for l in left)
    n = max(len(left), len(right))
    out = []
    for i in range(n):
        a = left[i] if i < len(left) else ""
        b = right[i] if i < len(right) else ""
        out.append(a.ljust(W1) + " " * gap + b)
    return out


def reason_bar(slide, alasan, jawaban, y=6.44, h=0.54):
    """Blok wajib pada setiap slide: ALASAN (dasar data) dan JAWABAN (keputusan)."""
    rect(slide, 0.42, y, 6.10, h, fill=RGBColor(0xFB, 0xF6, 0xE6),
         line_color=RGBColor(0xE6, 0xD6, 0xA2), line_w=0.75)
    rect(slide, 0.42, y, 0.06, h, fill=GOLD)
    tb(slide, 0.58, y + 0.04, 1.2, 0.14, "ALASAN", size=7.5, bold=True, color=GOLD)
    tb(slide, 0.58, y + 0.20, 5.80, h - 0.24, alasan, size=8.5,
       color=RGBColor(0x3A, 0x33, 0x18), line=1.15)

    rect(slide, 6.72, y, 6.10, h, fill=RGBColor(0xEA, 0xF6, 0xF6),
         line_color=RGBColor(0xA9, 0xDC, 0xDB), line_w=0.75)
    rect(slide, 6.72, y, 0.06, h, fill=TEAL)
    tb(slide, 6.88, y + 0.04, 1.2, 0.14, "JAWABAN", size=7.5, bold=True,
       color=RGBColor(0x1E, 0x7A, 0x79))
    tb(slide, 6.88, y + 0.20, 5.80, h - 0.24, jawaban, size=8.5,
       color=RGBColor(0x12, 0x3A, 0x40), line=1.15)


# ---------------------------------------------------------------- 1. COVER
s = prs.slides.add_slide(L_COVER)
clear_placeholders(s)
rect(s, 0.00, 0.00, 13.333, 7.5, fill=WHITE)
s.shapes.add_picture("docs/assets/gf_cover_band.jpg", Inches(0), Inches(5.92), Inches(13.333), Inches(1.58))
rect(s, 0.85, 1.05, 0.11, 0.78, fill=GOLD)
tb(s, 1.15, 0.72, 7.6, 0.28, "DAILY MONITORING SYSTEM   ·   PLANT SNACK", size=12, bold=True, color=GOLD)
tb(s, 1.15, 1.04, 8.4, 1.10,
   "DIGITALISASI DMS: DARI EXCEL KE INSIGHT", size=31, bold=True, color=NAVY, line=1.05)

rect(s, 1.15, 2.34, 8.30, 1.10, fill=RGBColor(0xFB, 0xF6, 0xE6),
     line_color=RGBColor(0xE6, 0xD6, 0xA2), line_w=0.75)
rect(s, 1.15, 2.34, 0.07, 1.10, fill=GOLD)
tb(s, 1.38, 2.44, 1.6, 0.20, "ALASAN", size=9, bold=True, color=GOLD)
tb(s, 1.38, 2.64, 7.85, 0.78,
   "Angka DMS dipakai untuk laporan manajemen, tetapi di dalam workbook: 973 kasus ditutup "
   "tanpa akar masalah, 94% kasus berulang tidak terdeteksi, dan 99,7% penyebabnya berada "
   "di luar kendali leader line.",
   size=10, color=RGBColor(0x3A, 0x33, 0x18), line=1.22)

rect(s, 1.15, 3.62, 8.30, 1.10, fill=RGBColor(0xEA, 0xF6, 0xF6),
     line_color=RGBColor(0xA9, 0xDC, 0xDB), line_w=0.75)
rect(s, 1.15, 3.62, 0.07, 1.10, fill=TEAL)
tb(s, 1.38, 3.72, 1.8, 0.20, "JAWABAN", size=9, bold=True, color=RGBColor(0x1E, 0x7A, 0x79))
tb(s, 1.38, 3.92, 7.85, 0.78,
   "Satu aplikasi dua lapis: form meeting 5 menit, dashboard tiga level, dan display TV lantai "
   "produksi — ditopang 14 aturan insight yang mengubah angka menjadi tindakan berpemilik "
   "dan bertenggat.",
   size=10, color=RGBColor(0x12, 0x3A, 0x40), line=1.22)

rect(s, 1.15, 5.02, 3.10, 0.03, fill=BORDER)
tb(s, 1.15, 5.16, 9.6, 0.26,
   "Dokumen: Logic & Design v1   ·   Oktober 2026   ·   Status: draft diskusi — belum implementasi",
   size=9, color=LGREY)

# ---------------------------------------------------------------- 2. AGENDA
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "AGENDA PEMAPARAN", "Tujuh bagian: dari kondisi hari ini menuju aplikasi yang memberi insight")
items = [
    ("01  Kondisi saat ini", "Apa yang terjadi di workbook DMS — dan mengapa angka tidak bisa dipercaya"),
    ("02  Baseline data", "5.817 kasus historis, kualitas data per sheet, pola masalah berulang"),
    ("03  Cacat logika Excel", "Sembilan titik yang membuat monitoring berhenti menjadi monitoring"),
    ("04  Logika aplikasi", "Rumus final, arsitektur informasi, peran, dan hierarki plant"),
    ("05  Mesin insight", "14 aturan deteksi otomatis + format baku rekomendasi"),
    ("06  Rancangan tampilan", "Form 5 menit · Dashboard 3 level · Display TV lantai produksi"),
    ("07  Roadmap & keputusan", "Pilot Snack 8 pekan + hal yang masih perlu diputuskan"),
]
y = 1.24
for i, (h, sub) in enumerate(items):
    if i % 2 == 0:
        rect(s, 0.42, y - 0.04, 12.45, 0.68, fill=LIGHT2)
    tb(s, 0.60, y, 3.35, 0.30, h, size=12.5, bold=True, color=NAVY)
    tb(s, 4.00, y + 0.02, 8.6, 0.60, sub, size=11, color=GREY)
    y += 0.70
reason_bar(s, 'Pemaparan disusun berurutan dari bukti, logika, lalu keputusan \— bukan dari fitur ke fitur.',
              'Tujuh bagian; yang diminta hari ini adalah jawaban atas keputusan yang masih terbuka.')
footer(s, 2)

# ---------------------------------------------------------------- 3. KONDISI SAAT INI
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "KONDISI SAAT INI", "Monitoring berjalan — tetapi angkanya tidak dapat dipertanggungjawabkan")
cards = [
    ("973", "kasus ditutup\ntanpa root cause", "Close berarti kolom terisi,\nbukan masalah selesai", RED),
    ("94%", "kasus berulang tetap\ndilabeli 'Occurrence'", "Recurrence tercatat 4%,\nfaktanya 26%", AMBER),
    ("99,7%", "kasus PIC-nya\nTeknik / Tekpro", "Yang dinilai leader,\npenyebabnya di pihak lain", RED),
]
x = 0.42
for big, lab, note, col in cards:
    rect(s, x, 1.25, 4.02, 2.05, fill=WHITE, line_color=BORDER, line_w=1)
    rect(s, x, 1.25, 4.02, 0.07, fill=col)
    tb(s, x + 0.22, 1.42, 3.6, 0.62, big, size=34, bold=True, color=col)
    tb(s, x + 0.22, 2.06, 3.6, 0.52, lab, size=11.5, bold=True, color=NAVY, line=1.15)
    tb(s, x + 0.22, 2.66, 3.6, 0.52, note, size=10, color=GREY, line=1.15)
    x += 4.14

tb(s, 0.42, 3.52, 12.5, 0.26, "AKAR MASALAHNYA BUKAN PADA ORANG — TETAPI PADA LOGIKA FILE", size=11.5, bold=True, color=GOLD)
bullets(s, 0.42, 3.88, 12.4, [
    ("Skor dinilai manual, padahal bisa dihitung sistem", "Item on-time dan kelengkapan file = 30 dari 100 bobot, semuanya input manusia"),
    ("Tidak mengisi lebih menguntungkan daripada mengisi jelek", "AVERAGEIF mengabaikan sel kosong: 1 hari sempurna = Ach 125% = skor 5"),
    ("Kasus dan checklist tidak saling terhubung", "Item PICA dan follow-up dinilai manual, padahal buktinya ada di 5.817 baris kasus"),
    ("Tidak ada dimensi waktu", "Tidak ada aging, tren, maupun peringatan sebelum masalah membesar"),
], size=12.5, gap=10)
reason_bar(s, 'Tiga angka pada slide ini dihitung langsung dari 5.817 baris workbook, bukan perkiraan.',
              'Akar masalahnya logika file, bukan orangnya. Perbaikannya harus di sistem, bukan imbauan.')
footer(s, 3)

# ---------------------------------------------------------------- 4. BASELINE DATA
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "BASELINE DATA", "Hasil audit workbook: 5.817 kasus, 12 sheet, 3 tahun")
data = [
    ["Sumber", "Kasus", "Rentang", "Kondisi data"],
    ["Resume SHE", "1.185", "Jan 2023 – Des 2025", "Dua tabel ditumpuk; root cause & due date 0%"],
    ["Resume QC", "1.520", "Agu 2023 – Okt 2026", "Relatif lengkap; 320 close tanpa root cause"],
    ["Resume Prod", "3.112", "Agu 2023 – Okt 2026", "Relatif lengkap; 653 close tanpa root cause"],
    ["IIAA Snack", "120", "2024 – 2026", "Duplikat, 100% Close — tidak dimigrasi"],
    ["TOTAL", "5.817", "", "973 kasus ditutup tanpa akar masalah"],
]
table(s, data, [2.35, 1.35, 3.05, 5.65], y=1.28, row_h=0.40, font=10.5)
for r in range(1, 5):
    pass

tb(s, 0.42, 3.90, 4.35, 0.26, "POLA MASALAH (PRODUKTIVITAS)", size=11, bold=True, color=GOLD)
data2 = [
    ["Pola berulang", "Frekuensi"],
    ["M03 BCAT", "15×"],
    ["SVB13 BCAT", "14×"],
    ["MHM39 LSTR", "13×"],
    ["SVB19 LSTR", "13×"],
]
table(s, data2, [2.55, 1.55], x=0.42, y=4.22, row_h=0.30, font=10)

tb(s, 5.05, 3.90, 7.8, 0.26, "184 POLA BERULANG MENCAPAI 26,2% DARI SELURUH KASUS", size=11, bold=True, color=GOLD)
bullets(s, 5.05, 4.28, 7.8, [
    ("Semua di Pilus L1 / Line 9", "3.014 dari 3.112 kasus produktivitas berasal dari satu line"),
    ("Prefix mesin: MHM 26,8% · BCAT 14,1%", "Downtime median 50 menit per kasus — total 208.848 menit"),
    ("Standardisasi hampir tidak pernah dijalankan", "OPL / PM / AM / CRMO dominan 'O' (88–98%) = tidak sesuai"),
], size=11.5, gap=6)
reason_bar(s, 'Sheet1 terbukti 100% ISO, dan 184 pola berulang mencakup 26,2% kasus produktivitas.',
              '5.817 kasus layak jadi baseline; 120 baris IIAA dibuang karena duplikat dan 100% Close.')
footer(s, 4)

# ---------------------------------------------------------------- 5. KUALITAS DATA
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "KUALITAS DATA", "Tanpa perbaikan ini, aplikasi hanya memindahkan masalah lama ke tempat baru")
data = [
    ["Field wajib", "SHE", "QC", "Prod", "Dampak bila dibiarkan"],
    ["Root cause", "0%", "79%", "78%", "Recurrence tidak bisa dianalisis"],
    ["Due date", "0%", "100%", "99%", "Tidak ada dasar aging & eskalasi"],
    ["Action plan", "28%", "100%", "100%", "Kasus open tanpa rencana penyelesaian"],
    ["Bukti / picture", "0%", "–", "–", "Close tidak dapat diverifikasi"],
    ["Case category", "16%", "100%", "100%", "Recurrence mustahil dihitung"],
    ["Prioritas", "~100% High", "~100% High", "~100% High", "Tidak lagi berfungsi sebagai triase"],
]
table(s, data, [2.20, 1.55, 1.35, 1.30, 6.00], y=1.30, row_h=0.42, font=10.5,
      aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT])

rect(s, 0.42, 4.72, 12.40, 1.45, fill=WHITE, line_color=GOLD, line_w=1.25)
rect(s, 0.42, 4.72, 0.08, 1.45, fill=GOLD)
tb(s, 0.68, 4.88, 11.9, 0.28, "TEMUAN PALING MAHAL", size=11, bold=True, color=GOLD)
tb(s, 0.68, 5.16, 11.9, 0.90,
   "Status \"Close\" diisi ketika kolomnya sudah berisi — bukan ketika masalahnya selesai. "
   "973 kasus ditutup tanpa akar masalah, dan 22 kasus masih Open dengan due date terlampaui "
   "hingga 1.045 hari. Sistem monitoring yang tidak bisa menutup loop akan terus menghasilkan angka 75%.",
   size=11.5, color=NAVY, line=1.30)
reason_bar(s, 'Status Close diisi saat kolom terisi, bukan saat masalah selesai: 973 kasus tanpa akar masalah.',
              'Gate close diberlakukan: root cause + action + bukti + approval.')
footer(s, 5)

# ---------------------------------------------------------------- 6. CACAT LOGIKA
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "SEMBILAN CACAT LOGIKA EXCEL", "Ini yang membuat monitoring berhenti menjadi monitoring")
data = [
    ["#", "Cacat logika", "Bukti di file", "Perbaikan di aplikasi"],
    ["1", "AVERAGEIF mengabaikan sel kosong", "1 hari diisi → Ach 125% → skor 5", "Penyebut = hari kerja − hari libur"],
    ["2", "Skor objektif dinilai manusia", "On-time & kelengkapan = 30 bobot", "Dihitung sistem (tombol Start/End)"],
    ["3", "Enam item diringkas jadi satu angka", "Hanya nilai total yang tersimpan", "Simpan skor per item"],
    ["4", "Healthy Check bernilai konstan", "0,8 / 0,8 → selalu 0,6", "Parameter editable + simulasi"],
    ["5", "Recurrence diisi manual", "849 dari 902 salah label", "Deteksi otomatis by signature"],
    ["6", "Close tanpa bukti", "973 kasus", "Gate: root cause + action + bukti"],
    ["7", "Kasus tidak terhubung checklist", "Item PICA dinilai manual", "Skor item 5 & 6 dari data kasus"],
    ["8", "Tidak ada dimensi waktu", "Tidak ada aging / tren", "Aging, tren, lead indicator"],
    ["9", "Ambang batas tanpa pembulatan", "0,88/0,8 = 1,0999 → skor 3", "Bandingkan pada 2 desimal"],
]
table(s, data, [0.55, 4.05, 4.05, 3.75], y=1.22, row_h=0.50, font=9.5, head_font=10,
      aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])
reason_bar(s, 'Sembilan cacat ini terbukti dari rumus aslinya, misalnya 0,88/0,8 = 1,0999 yang jatuh ke skor 3.',
              'Semuanya ditambal di aplikasi; tidak ada satu pun yang dibiarkan karena warisan Excel.')
footer(s, 6)

# ---------------------------------------------------------------- 7. LAPORAN VS INSIGHT
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "DARI LAPORAN MENJADI INSIGHT", "Output aplikasi bukan angka — tetapi tindakan")
# left
rect(s, 0.42, 1.22, 6.05, 4.55, fill=WHITE, line_color=BORDER, line_w=1)
rect(s, 0.42, 1.22, 6.05, 0.08, fill=LGREY)
tb(s, 0.68, 1.42, 5.6, 0.30, "LAPORAN BIASA (EXCEL)", size=12, bold=True, color=LGREY)
data = [
    ["Yang disampaikan", "Isi"],
    ["Capaian", "Ach 83,7%"],
    ["Recurrence", "5,3%"],
    ["Status", "Ada 142 kasus open"],
    ["Kesimpulan", "Diserahkan ke pembaca"],
]
table(s, data, [1.85, 3.90], x=0.68, y=1.86, row_h=0.42, font=10, head_fill=LGREY)
tb(s, 0.68, 4.50, 5.5, 0.62, "Angka tanpa sebab → rapat berhenti pada\n\"kenapa bisa begitu?\"", size=10.5, color=GREY, line=1.2)

# right
rect(s, 6.78, 1.22, 6.05, 4.55, fill=WHITE, line_color=GOLD, line_w=1.5)
rect(s, 6.78, 1.22, 6.05, 0.08, fill=GOLD)
tb(s, 7.04, 1.42, 5.6, 0.30, "INSIGHT APLIKASI", size=12, bold=True, color=GOLD)
rows = [
    ("TEMUAN", "83,7% — di bawah target 90% (PICA Safety)"),
    ("BUKTI", "142 dari 536 kasus masih Open; 37 lewat due date"),
    ("SEBAB", "Fokus pada Correction, bukan Preventive; OPL/PM 88–98% tidak terisi"),
    ("DAMPAK", "Index turun ke 3,00 — tepat di batas target"),
    ("REKOMENDASI", "Wajibkan Preventive Action untuk pola ≥3× di Pilus L1"),
    ("PEMILIK", "Teknik — bukan leader line"),
]
y = 1.84
for k, v in rows:
    tb(s, 7.04, y, 1.42, 0.26, k, size=8.5, bold=True, color=GOLD)
    tb(s, 8.52, y - 0.02, 4.05, 0.50, v, size=9.5, color=NAVY, line=1.12)
    y += 0.58
reason_bar(s, 'Ach 83,7% tidak menjelaskan apa pun, sehingga rapat berhenti pada pertanyaan kenapa.',
              'Output aplikasi = temuan + bukti + sebab + dampak + rekomendasi + pemilik.')
footer(s, 7)

# ---------------------------------------------------------------- 8. ARSITEKTUR
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "ARSITEKTUR INFORMASI", "Empat lapis lokasi · dua peran · satu sumber angka")
tb(s, 0.42, 1.25, 5.9, 0.26, "HIERARKI LOKASI", size=11, bold=True, color=GOLD)
levels = [
    ("GROUP", "template core · konsolidasi · benchmarking"),
    ("PLANT", "Dairy · Exist · New · Snack — KPI & target khas plant"),
    ("FACTORY / BU", "Factory 10 (QC+Prod) · Factory 30 (SHE)"),
    ("LINE / AREA", "Pilus L1 (9) · Pellet L1 (10) · Line A–F"),
]
y = 1.60
for i, (h, sub) in enumerate(levels):
    w = 5.55 - i * 0.42
    rect(s, 0.42 + i * 0.21, y, w, 0.72, fill=NAVY if i == 0 else (WHITE if i % 2 else LIGHT2),
         line_color=BORDER, line_w=0.75)
    tb(s, 0.60 + i * 0.21, y + 0.10, w - 0.3, 0.26, h, size=10.5, bold=True,
       color=WHITE if i == 0 else NAVY)
    tb(s, 0.60 + i * 0.21, y + 0.36, w - 0.3, 0.32, sub, size=8.5,
       color=RGBColor(0xD9, 0xE2, 0xF3) if i == 0 else GREY, line=1.1)
    y += 0.80
tb(s, 0.42, 4.92, 5.9, 0.55,
   "Kode stabil: PLT-SNK, PLT-DRY, PLT-EX1, PLT-NW1.\nNama tampilan boleh berubah — kode tidak.", size=9.5, color=GREY, line=1.25)

tb(s, 6.95, 1.25, 5.9, 0.26, "PERAN & AKSES", size=11, bold=True, color=GOLD)
data = [
    ["Kemampuan", "User", "Admin", "TV"],
    ["Isi form meeting", "✓", "✓", "—"],
    ["Buat / update kasus", "miliknya", "semua", "—"],
    ["Close kasus", "ajukan", "approve", "—"],
    ["Dashboard", "plant", "semua plant", "—"],
    ["Ubah bobot & target", "—", "✓", "—"],
    ["Kelola profil TV", "—", "✓", "tampil"],
]
table(s, data, [2.72, 1.05, 1.13, 0.90], x=6.95, y=1.60, row_h=0.36, font=9.5, head_font=9.5,
      aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER])

rect(s, 6.95, 4.42, 5.85, 1.05, fill=LIGHT2, line_color=BORDER, line_w=0.75)
rect(s, 6.95, 4.42, 0.07, 1.05, fill=RED)
tb(s, 7.18, 4.56, 5.5, 0.80,
   "Aturan keras: setiap query wajib ter-filter plant_id.\nIni pencegahan kebocoran data antar plant yang paling sering terlewat.",
   size=9.5, color=NAVY, line=1.25)
reason_bar(s, 'Satu plant Snack sudah punya dua factory, dan data Dairy sudah bocor 1 entri ke sheet Snack.',
              'plant_id wajib di semua transaksi, dan nama plant diganti kode stabil (PLT-SNK, PLT-DRY).')
footer(s, 8)

# ---------------------------------------------------------------- 9. ALUR APLIKASI
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "ALUR APLIKASI", "Lima tahap loop tertutup — berhenti di satu tahap berarti kembali ke Excel")
steps = [
    ("1", "CAPTURE", "Meeting harian +\nkasus baru", "Form 5 menit\nsaat rapat"),
    ("2", "DETECT", "Aging, recurrence,\nlonjakan, breach", "Rule engine\notomatis"),
    ("3", "EXPLAIN", "Setiap angka bisa\ndi-drill sampai kasus", "Traceability"),
    ("4", "RECOMMEND", "Usulkan tindakan dari\nriwayat penanganan", "Bukan tebakan"),
    ("5", "ACT & VERIFY", "PIC, due date, cek\nkambuh atau tidak", "Loop tertutup"),
]
x = 0.42
for num, title, body, note in steps:
    w = 2.38
    rect(s, x, 1.35, w, 2.35, fill=WHITE, line_color=BORDER, line_w=1)
    rect(s, x, 1.35, w, 0.07, fill=TEAL)
    rect(s, x + 0.18, 1.55, 0.44, 0.44, fill=NAVY, shape=MSO_SHAPE.OVAL)
    tb(s, x + 0.18, 1.63, 0.44, 0.28, num, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    tb(s, x + 0.72, 1.62, w - 0.85, 0.30, title, size=10.5, bold=True, color=NAVY)
    tb(s, x + 0.18, 2.18, w - 0.36, 0.70, body, size=9.5, color=NAVY, line=1.2)
    tb(s, x + 0.18, 3.16, w - 0.36, 0.40, note, size=8.5, color=LGREY, line=1.15)
    if num != "5":
        tb(s, x + w + 0.02, 2.30, 0.30, 0.30, "›", size=20, bold=True, color=GOLD)
    x += w + 0.19

rect(s, 0.42, 4.05, 12.40, 2.05, fill=LIGHT2, line_color=BORDER, line_w=0.75)
tb(s, 0.68, 4.20, 11.9, 0.28, "YANG MEMBEDAKAN DENGAN DASHBOARD BIASA", size=11, bold=True, color=GOLD)
comps = [
    ("Output", "bukan angka, tetapi tindakan dengan pemilik dan tenggat"),
    ("Penjelasan", "setiap skor dapat ditelusuri sampai ke kasus penyebabnya"),
    ("Prediksi", "pola berulang terdeteksi sebelum menjadi kegagalan besar"),
    ("Verifikasi", "sistem menanyakan kembali: apakah kasus ini kambuh?"),
]
y = 4.56
for k, v in comps:
    tb(s, 0.68, y, 1.55, 0.26, k, size=10, bold=True, color=NAVY)
    tb(s, 2.30, y, 10.3, 0.26, v, size=10, color=GREY)
    y += 0.36
reason_bar(s, 'Excel sekarang berhenti di tahap capture dan detect; tidak ada explain, recommend, maupun verifikasi.',
              'Loop ditutup di ACT & VERIFY: setiap kasus dicek kembali kambuh atau tidak.')
footer(s, 9)

# ---------------------------------------------------------------- 10. FORM MEETING
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "RANCANGAN FORM MEETING HARIAN", "Dipakai berdiri, sambil rapat berjalan — target selesai di bawah 5 menit")
wf = "\n".join(panel([
    "Meeting Harian  ·  29 Okt 2026  ·  Pilus L1",
    "Leader: [dropdown]    Mulai 07:00    Selesai 07:08    [OK] ON-TIME",
    "A. CHECKLIST — 6 item",
    "1  On time ......................... otomatis  · bobot 10",
    "2  Kelengkapan form ................ otomatis  · bobot 20",
    "3  Peserta aktif ............ [0] [5] [8] [10]   (note)*",
    "4  Leader menjalankan tugas . [0] [5] [8] [10]   (note)*",
    "5  PICA lengkap ............. [0] [5] [8] [10]   (note)*",
    "6  Action direview .......... [0] [5] [8] [10]   (note)*",
    "    *) catatan wajib diisi bila skor < 8",
    "B. KPI — 15 item, tombol besar V / O / N-A",
    "Safety        KAK           [V][O][NA]    PICA Safety   [V][O][NA]",
    "Quality       Defect Pack   [V][O][NA]    PICA Quality  [V][O][NA]",
    "Productivity  OEE           [V][O][NA]    Yield RM      [V][O][NA]",
    "Energy        Gas Engine    [V][O][NA]    Electrical    [V][O][NA]",
    "  [ + MASALAH BARU ]                                  [ SIMPAN ]",
], seps=(1, 9, 14)))
code_box(s, 0.42, 1.25, 8.55, 4.55, wf)

reason_bar(s, "30 dari 100 bobot dinilai manusia, padahal dua item itu dapat dihitung sistem.",
           "Item 1 dan 2 otomatis, autosave per field, dan catatan wajib bila skor di bawah 8.")

tb(s, 9.20, 1.25, 3.7, 0.26, "KEPUTUSAN DESAIN", size=11, bold=True, color=GOLD)
bullets(s, 9.20, 1.60, 3.65, [
    ("Dua item jadi otomatis", "Bobot 30 dari 100 tidak lagi dinilai manusia"),
    ("Autosave per field", "Sinyal area produksi tidak andal"),
    ("Catatan wajib bila < 8", "Skor tidak bisa diberikan tanpa alasan"),
    ("Tombol besar", "Diisi di HP maupun tablet"),
    ("Satu layar", "Bukan wizard bertahap"),
], size=10.5, gap=8)
tb(s, 9.20, 5.20, 3.65, 0.80,
   "Hari wajib = Senin–Jumat dikurangi\nhari libur nasional.\nTarget waktu: di bawah 5 menit.", size=9.5, color=GREY, line=1.25)
footer(s, 10)

# ---------------------------------------------------------------- 11. FORM KASUS
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "RANCANGAN FORM KASUS & HALAMAN USER", "Masalah dicatat saat itu juga — bukan direkap di akhir bulan")
left = "\n".join(panel([
    "FORM KASUS  (30 detik)",
    "Problem*      ________________________",
    "Kategori*     [Machine v]",
    "Prioritas*    [Medium v]   (default, bukan High)",
    "LBN / Mesin*  [dropdown]  + kode mesin",
    "Root cause*   ________________________",
    "Action*       ________________________",
    "PIC*          [dropdown]",
    "Due date*     [ 29/10/2026 ]",
    "Bukti         [ foto / kamera ]",
    "",
    "  [ SIMPAN & LANJUT 5-WHY ]",
]))
right = "\n".join(panel([
    "KASUS SAYA (12)",
    "C-081  M03 BCAT    ! +2 hari",
    "C-079  MHM39 LSTR    7 hari",
    "C-076  MHM38 LSTR    3 hari",
    "C-072  PICA Safety   0 hari",
    "",
    "Detail:",
    "  5-Why · Action · Bukti",
    "  Riwayat · Ajukan Close",
    "",
    "  [ AJUKAN CLOSE ]",
]))
code_box(s, 0.42, 1.25, 5.05, 2.72, left)
code_box(s, 5.60, 1.25, 3.40, 2.72, right)

tb(s, 0.42, 4.22, 8.6, 0.26, "ALUR DARI MASALAH KE VERIFIKASI", size=10.5, bold=True, color=GOLD)
steps = ["Masalah\ndicatat", "PIC &\ndue date", "5-Why\nlengkap", "Action\ndijalankan", "Close\ndisetujui", "Cek\nkambuh?"]
x = 0.42
for i, st in enumerate(steps):
    rect(s, x, 4.54, 1.30, 0.78, fill=WHITE, line_color=BORDER, line_w=0.75)
    rect(s, x, 4.54, 1.30, 0.05, fill=TEAL if i < 5 else GOLD)
    tb(s, x + 0.08, 4.68, 1.16, 0.52, st, size=8.5, bold=True, color=NAVY, align=PP_ALIGN.CENTER, line=1.15)
    if i < 5:
        tb(s, x + 1.30, 4.74, 0.14, 0.26, "›", size=14, bold=True, color=GOLD)
    x += 1.44

rect(s, 0.42, 5.56, 8.58, 0.72, fill=LIGHT2, line_color=BORDER, line_w=0.75)
rect(s, 0.42, 5.56, 0.07, 0.72, fill=GOLD)
tb(s, 0.70, 5.66, 8.1, 0.56,
   "Enam tahap ini adalah state machine kasus. Sistem tidak mengizinkan lompat tahap:\n"
   "kasus tidak dapat masuk \"Cek kambuh\" sebelum close disetujui dengan bukti lengkap.",
   size=9.5, color=NAVY, line=1.25)

tb(s, 9.20, 1.25, 3.7, 0.26, "ATURAN INPUT", size=11, bold=True, color=GOLD)
bullets(s, 9.20, 1.60, 3.65, [
    ("Wajib saat itu", "Problem · PIC · due date — tiga field yang dipakai mesin insight"),
    ("5-Why menyusul", "Boleh dilengkapi, tetapi tidak boleh close sebelum lengkap"),
    ("Default Medium", "Prioritas ~100% High membuat triase mati"),
    ("Bukti dari HP", "Sesuatu yang Excel tidak pernah bisa minta"),
], size=10.5, gap=9)
reason_bar(s, 'Kasus tanpa PIC dan due date tidak bisa menua dan tidak bisa dieskalasi.',
              'Problem + PIC + due date wajib saat input; 5-Why boleh menyusul, tetapi close tidak.')
footer(s, 11)

# ---------------------------------------------------------------- 12. ADMIN
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "RANCANGAN HALAMAN ADMIN", "Menyetujui, mengonfigurasi, dan menjaga kualitas angka")
b1 = panel([
    "REVIEW & APPROVE",
    "Menunggu close: 5    Ditolak: 1    Perlu bukti: 3",
    "C-076  M03 BCAT    root cause OK  action OK  bukti --",
    "       > [ Minta bukti ]  [ Tolak ]  [ Setujui ]",
    "C-072  MHM38 LSTR  root cause OK  action OK  bukti OK",
    "       ! recurrence ke-7 — wajib Preventive Action",
    "       > [ Setujui dengan syarat ]  [ Tolak ]",
], seps=(1,))
b2 = panel([
    "PENGATURAN PENILAIAN — versioned · effective_date",
    "Bobot checklist   [10][20][10][20][20][20]      Total = 100",
    "Band skor         >=120%->5  >=110%->4  >=100%->3  >=90%->2",
    "Healthy Check     nilai [0,8]   bobot [0,2]   mode [konstan]",
    "Bobot index       KPI [0,4]   Checklist [0,4]   Healthy [0,2]",
    "Hari wajib        [Sen][Sel][Rab][Kam][Jum]   Libur [+ tanggal]",
    "Simulasi: index 3,40 -> 3,20",
    "                         [ BATAL ]    [ SIMPAN VERSI ]",
], seps=(0,))
wf = "\n".join(b1) + "\n" + "\n".join(b2)
code_box(s, 0.42, 1.22, 8.55, 4.42, wf)

tb(s, 9.20, 1.22, 3.7, 0.26, "PRINSIP ADMIN", size=11, bold=True, color=GOLD)
bullets(s, 9.20, 1.58, 3.65, [
    ("Config punya tanggal berlaku", "Ubah bobot hari ini tidak boleh mengubah skor tahun lalu"),
    ("Simulasi sebelum simpan", "Admin melihat dampak, bukan angka tersembunyi"),
    ("Approval bukan formalitas", "Syarat close: root cause + action + bukti"),
    ("Semua perubahan tercatat", "Siapa, kapan, sebelum → sesudah, alasan"),
], size=10.5, gap=9)
rect(s, 0.42, 5.76, 8.55, 0.50, fill=LIGHT2, line_color=BORDER, line_w=0.75)
rect(s, 0.42, 5.76, 0.07, 0.50, fill=RED)
tb(s, 0.70, 5.84, 8.2, 0.38,
   "Batasan Admin: tidak dapat mengubah skor pada periode yang sudah dikunci.\n"
   "Koreksi hanya melalui penyesuaian beralasan yang tercatat di audit log.",
   size=9, color=NAVY, line=1.2)
reason_bar(s, 'Mengubah bobot hari ini tanpa versioning berarti mengubah skor periode yang sudah dilaporkan.',
              'Config memakai effective_date + period lock; koreksi hanya lewat penyesuaian beralasan.')
footer(s, 12)

# ---------------------------------------------------------------- 13. DASHBOARD
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "DASHBOARD TIGA LEVEL", "Satu dashboard untuk semua orang berarti tidak berguna untuk siapa pun")
levels = [
    ("L1 · OPERASIONAL", "Leader · Supervisor", ["Status meeting hari ini", "DMS Index vs target", "Kasus open & aging", "Insight 3 teratas"], "real-time · sedikit angka", "3 line belum DMS\nindex 3,40 vs target 3,00"),
    ("L2 · ANALITIK", "Admin · Manager", ["Tren pekan & bulan", "Recurrence & Pareto", "Per line / per PIC", "Drill-down penuh"], "semua bisa diklik", "recurrence 26,2%\ntercatat hanya 4,0%"),
    ("L3 · EKSEKUTIF", "Plant Head", ["1 angka index", "3 kartu insight", "Tren 12 pekan", "Tanpa scroll"], "satu layar", "index 3,40\n2 parameter di bawah target"),
]
x = 0.42
for title, who, items, note, contoh in levels:
    rect(s, x, 1.28, 4.02, 3.90, fill=WHITE, line_color=BORDER, line_w=1)
    rect(s, x, 1.28, 4.02, 0.62, fill=NAVY)
    tb(s, x + 0.20, 1.38, 3.6, 0.26, title, size=11, bold=True, color=WHITE)
    tb(s, x + 0.20, 1.66, 3.6, 0.22, who, size=8.5, color=RGBColor(0xC9, 0xD5, 0xEE))
    y = 2.08
    for it in items:
        rect(s, x + 0.22, y + 0.09, 0.06, 0.06, fill=GOLD)
        tb(s, x + 0.40, y, 3.4, 0.26, it, size=10, color=NAVY)
        y += 0.34
    rect(s, x + 0.22, 3.62, 3.58, 0.68, fill=LIGHT2, line_color=BORDER, line_w=0.75)
    tb(s, x + 0.34, 3.70, 3.35, 0.20, "CONTOH TAMPILAN", size=7.5, bold=True, color=GOLD)
    tb(s, x + 0.34, 3.90, 3.35, 0.36, contoh, size=9, color=NAVY, line=1.15)
    tb(s, x + 0.22, 4.55, 3.6, 0.26, note, size=8.5, color=LGREY)
    x += 4.14

rect(s, 0.42, 5.26, 12.40, 0.96, fill=LIGHT2, line_color=BORDER, line_w=0.75)
rect(s, 0.42, 5.26, 0.07, 0.96, fill=TEAL)
tb(s, 0.68, 5.36, 12.0, 0.24, "ATURAN YANG TIDAK BOLEH DILANGGAR", size=10.5, bold=True, color=GOLD)
tb(s, 0.68, 5.60, 12.0, 0.56,
   "Setiap angka harus bisa ditelusuri: index → parameter → hari → item checklist → kasus penyebabnya.   "
   "Setiap insight harus punya PIC dan due date — jika tidak, ia berhenti menjadi insight dan berubah menjadi keluhan.",
   size=10.5, color=NAVY, line=1.30)
reason_bar(s, 'Satu dashboard untuk semua orang berakhir tidak berguna untuk siapa pun.',
              'Tiga level dengan audiens jelas; setiap angka dapat di-drill sampai kasus penyebabnya.')
footer(s, 13)

# ---------------------------------------------------------------- 14. TV
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "DISPLAY TV LANTAI PRODUKSI", "Bukan dashboard yang diperbesar — tata letak sendiri untuk jarak 3–10 meter")
wf = "\n".join(panel([
    "DMS FACTORY 10 — PILUS L1          Kam, 29 Okt 2026  14:32:10",
    "DMS INDEX HARI INI      |  STATUS MEETING HARI INI",
    "       3,40  ^          |  [OK] Line 9    selesai 07:12",
    "    TARGET 3,00         |  [  ] Line 10   belum mulai",
    "  ##########.... (gauge)|  [!]  Frying     telat 25 menit",
    "KASUS TERBUKA 142    AGING >30 HARI 37    RECURRENCE 5,3%",
    "PERLU TINDAKAN                          (rotasi 20 detik)",
    "!  MHM38 BCAT — 7x dalam 60 hari — PIC Teknik — sisa 4 hari",
    "!  PICA Safety 75,4% < 90% — 37 kasus lewat due date",
    "!  Checklist \"PICA\" skor < 8 tiga hari berturut-turut",
], seps=(0, 4, 5)))
code_box(s, 0.42, 1.28, 8.55, 3.28, wf)

tb(s, 9.20, 1.28, 3.7, 0.26, "ATURAN TEKNIS", size=11, bold=True, color=GOLD)
bullets(s, 9.20, 1.62, 3.65, [
    ("Font ≥ 40 px", "Angka hero ≥ 120 px — uji baca 5 meter"),
    ("Refresh 30–60 detik", "Bukan websocket — lebih tahan sinyal"),
    ("Hanya 3 warna status", "Tanpa gradasi; pabrik terang & buta warna"),
    ("Fallback snapshot", "Jangan pernah menampilkan layar kosong"),
    ("Tanpa interaksi", "Tidak ada tombol sama sekali"),
], size=10, gap=7)
tb(s, 0.42, 5.00, 8.6, 0.26, "ROTASI OTOMATIS ZONA BAWAH", size=10.5, bold=True, color=GOLD)
rota = ["Perlu tindakan\n(3 teratas)", "Status meeting\nper line", "Pareto masalah\nminggu ini", "Recurrence\nteratas", "Pengingat\ntarget"]
x = 0.42
for i, r in enumerate(rota):
    rect(s, x, 5.34, 1.64, 0.62, fill=WHITE, line_color=BORDER, line_w=0.75)
    tb(s, x + 0.06, 5.42, 1.52, 0.50, r, size=8, color=NAVY, align=PP_ALIGN.CENTER, line=1.1)
    x += 1.72
reason_bar(s, 'Layar dilihat dari jarak 3\–10 meter, sambil berdiri, di bawah pencahayaan pabrik.',
              'Font minimum 40 px, refresh 30\–60 detik, tiga warna status, tanpa interaksi, ada fallback.')
footer(s, 14)

# ---------------------------------------------------------------- 15. TV KONFIGURASI
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "TV DIATUR DARI APLIKASI", "Admin mengubah tampilan tanpa deployment")
data = [
    ["Yang diatur Admin", "Contoh default", "Efek"],
    ["Jumlah kartu insight", "3", "Menyesuaikan ukuran & jarak baca layar"],
    ["Jenis insight yang tampil", "I-01 · I-02 · I-03", "Hanya menampilkan yang relevan per area"],
    ["Rotasi antar kartu", "20 detik", "Pesan terbaca sebelum berganti"],
    ["Interval refresh data", "60 detik", "Seimbang antara kesegaran & beban jaringan"],
    ["Line / area yang ditampilkan", "Pilus L1", "Satu TV satu konteks — hindari tampilan semua line"],
    ["Jam aktif", "06:00 – 22:00", "Tidak menampilkan data basi di luar jam kerja"],
    ["Ambang warna", "hijau ≥90% · kuning ≥75%", "Konsisten dengan band skor penilaian"],
    ["Token akses", "per perangkat, dapat dicabut", "TV bukan user — akses read-only & terbatas"],
]
table(s, data, [3.95, 3.75, 4.70], y=1.28, row_h=0.50, font=10, head_font=10.5)

tb(s, 0.42, 5.80, 12.4, 0.20, "YANG TIDAK DITAMPILKAN DI TV", size=10.5, bold=True, color=GOLD)
tb(s, 0.42, 6.04, 12.4, 0.30,
   "Ranking individu/PIC (memicu konflik, bukan perbaikan)  ·  angka mentah panjang  ·  KPI di luar wewenang orang di lantai",
   size=10.5, color=NAVY)
reason_bar(s, 'Kebutuhan tampilan berbeda per area; hardcode berarti setiap perubahan butuh deployment.',
              'TV dirender dari profil: jumlah kartu, jenis insight, rotasi, jam aktif, ambang warna.')
footer(s, 15)

# ---------------------------------------------------------------- 16. INSIGHT ENGINE
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "MESIN INSIGHT · 14 ATURAN", "Setiap temuan wajib membawa bukti, sebab, dampak, rekomendasi, dan pemilik")
data = [
    ["Kode", "Pemicu", "Contoh output", "Kanal"],
    ["I-01", "Hari kerja tanpa meeting", "Line 10 tidak DMS 3 hari berturut", "L1 · TV"],
    ["I-02", "Due date lewat & masih Open", "22 kasus overdue, tertua 1.045 hari", "TV · L1"],
    ["I-03", "Signature sama ≥3× / 90 hari", "M03 BCAT 15× di Pilus L1", "TV · L2"],
    ["I-04", "Recurrence + root cause identik", "Correction sama 4× → naikkan Preventive", "L2"],
    ["I-05", "Close tapi OPL/PM/AM/CRMO = O", "88–98% kasus tidak pernah distandarkan", "L2 · L3"],
    ["I-06", "Close tanpa root cause/bukti", "973 kasus ditutup tanpa akar masalah", "Admin"],
    ["I-07", "Prioritas High > 80%", "Field prioritas tidak lagi membedakan", "Admin"],
    ["I-08", "Ach dalam 1% di bawah band", "Rawan salah hitung — perlu pembulatan", "Admin"],
    ["I-09", "3 periode menurun berturut", "Checklist turun 4%/pekan", "L2 · L3"],
    ["I-10", "Satu line/mesin > 20% kasus", "Pilus L1 = 90% kasus; MHM 26,8%", "L3"],
    ["I-11", "DT besar × frekuensi tinggi", "MHM38 7× dengan median DT 50 menit", "L2"],
    ["I-12", "PICA lemah + kasus baru naik", "Prediksi lonjakan pekan depan", "L3"],
    ["I-13", "Field wajib kosong > 10%", "Kelengkapan data line ini 78%", "Admin"],
    ["I-14", "KPI non-controllable ke leader", "99,7% PIC kasus = Teknik", "Admin"],
]
table(s, data, [0.80, 3.60, 6.45, 1.55], y=1.20, row_h=0.335, font=9, head_font=9.5,
      aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER])
reason_bar(s, '849 dari 902 kasus berulang tetap dilabeli Occurrence, jadi deteksi manual tidak mungkin.',
              '14 aturan otomatis; maksimal 3 tampil di TV dan L1 (dapat diubah), sisanya masuk daftar.')
footer(s, 16)

# ---------------------------------------------------------------- 17. RUMUS
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "LOGIKA PENILAIAN FINAL", "Tiga perbaikan kecil yang mengubah arti seluruh angka")
code = (
"# MEETING HARIAN\n"
"bobot_item   = [10, 20, 10, 20, 20, 20]        # Σ = 100, config\n"
"skor_item    = 0 | 5 | 8 | 10                   # rubric config\n"
"nilai_harian = Σ (skor_item/10 × bobot_item)/100\n"
"\n"
"item_1 = on_time(mulai, selesai, toleransi=10m)  # otomatis\n"
"item_2 = kelengkapan_form(tabel_wajib)           # otomatis\n"
"\n"
"# KPI HARIAN (V/O)\n"
"ach_kpi_harian = V / (V + O)                     # N/A keluar dari penyebut\n"
"\n"
"# PEKAN\n"
"penyebut      = hari_kerja − hari_libur          # BUKAN hari terisi\n"
"ach_checklist = Σ nilai_harian / (penyebut × target)\n"
"ach_kpi       = Σ ach_kpi_harian / (penyebut × target)\n"
"\n"
"# SKOR (band config, bandingkan 2 desimal)\n"
"skor = 5 if ach ≥ 1.20   4 if ach ≥ 1.10   3 if ach ≥ 1.00\n"
"       2 if ach ≥ 0.90   1 if ach <  0.90\n"
"\n"
"# INDEX\n"
"nilai_param = skor × bobot_param                 # 0,4 / 0,4 / 0,2\n"
"DMS Index   = Σ nilai_param                      # target 3, max 5\n"
)
code_box(s, 0.42, 1.22, 7.55, 5.15, code)

tb(s, 8.20, 1.22, 4.7, 0.26, "PERUBAHAN & DAMPAKNYA", size=11, bold=True, color=GOLD)
data = [
    ["Skenario", "Excel", "Aplikasi"],
    ["5 hari wajib,\n1 hari diisi", "skor 5", "skor 1"],
    ["0,88 / 0,80", "skor 3", "skor 4"],
    ["0,89 / 0,80", "skor 4", "skor 4"],
]
table(s, data, [1.85, 1.10, 1.25], x=8.20, y=1.58, row_h=0.52, font=9.5,
      aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER])

bullets(s, 8.20, 3.72, 4.6, [
    ("Tidak mengisi tidak lagi menguntungkan", "Sel kosong dihitung sebagai nol, bukan diabaikan"),
    ("Ambang batas dibulatkan", "Selisih realisasi 1% tidak lagi menjatuhkan satu band penuh"),
    ("Healthy Check jadi parameter", "Nilai & bobot dapat diubah Admin per tanggal berlaku"),
], size=10, gap=8)
reason_bar(s, 'AVERAGEIF mengabaikan sel kosong, dan ambang tanpa pembulatan menjatuhkan satu band penuh.',
              'Penyebut = hari kerja dikurangi hari libur, dan perbandingan band pada 2 desimal.')
footer(s, 17)

# ---------------------------------------------------------------- 18. ROADMAP
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "ROADMAP PILOT SNACK", "Delapan pekan untuk membuktikan bahwa aplikasi dipakai — bukan hanya dibangun")
phases = [
    ("0", "FONDASI", "2 pekan", "Master data bersih · config versioned · auth & scope"),
    ("1", "CAPTURE", "3 pekan", "Form meeting + form kasus + approval"),
    ("2", "MEASURE", "2 pekan", "Engine skor + dashboard L1"),
    ("3", "INSIGHT", "2 pekan", "8 aturan pertama (I-01…I-06, I-13, I-14)"),
    ("4", "DISPLAY", "1 pekan", "TV + profil display di area Pilus L1"),
    ("5", "ANALITIK", "2 pekan", "Dashboard L2 & L3 + ekspor laporan"),
]
y = 1.26
for num, name, dur, desc in phases:
    rect(s, 0.42, y, 7.55, 0.62, fill=WHITE, line_color=BORDER, line_w=0.75)
    rect(s, 0.42, y, 0.42, 0.62, fill=NAVY)
    tb(s, 0.42, y + 0.16, 0.42, 0.30, num, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    tb(s, 0.98, y + 0.16, 1.55, 0.30, name, size=10.5, bold=True, color=NAVY)
    tb(s, 2.55, y + 0.18, 1.05, 0.26, dur, size=9, color=GOLD, bold=True)
    tb(s, 3.65, y + 0.12, 4.20, 0.46, desc, size=9.5, color=GREY, line=1.1)
    y += 0.68

tb(s, 8.20, 1.26, 4.7, 0.26, "KRITERIA KEBERHASILAN (8 PEKAN)", size=11, bold=True, color=GOLD)
data = [
    ["Metrik", "Target"],
    ["Kepatuhan isi form", "≥ 90%"],
    ["Kelengkapan root cause", "≥ 95%"],
    ["Kasus overdue", "turun 50%"],
    ["Pola ≥3× punya action", "100%"],
    ["Insight ditindaklanjuti", "≥ 70%"],
]
table(s, data, [3.05, 1.55], x=8.20, y=1.62, row_h=0.40, font=10,
      aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER])

rect(s, 8.20, 4.52, 4.60, 1.80, fill=LIGHT2, line_color=BORDER, line_w=0.75)
rect(s, 8.20, 4.52, 0.07, 1.80, fill=GOLD)
tb(s, 8.44, 4.64, 4.2, 0.28, "SETELAH PILOT STABIL", size=10, bold=True, color=GOLD)
tb(s, 8.44, 4.94, 4.2, 1.26,
   "Generalisasi template plant, lalu rollout berurutan:\n\n"
   "Exist Plant  →  Dairy  →  New Plant\n\n"
   "New Plant dimulai tanpa data lama — paling mudah.",
   size=9.5, color=NAVY, line=1.25)
reason_bar(s, 'Snack dipilih karena template dan 5.817 baris datanya sudah ada, sehingga bisa divalidasi tanpa data baru.',
              'Delapan pekan, dengan lima metrik keberhasilan terukur \— bukan sekadar aplikasi selesai.')
footer(s, 18)

# ---------------------------------------------------------------- 19. KEPUTUSAN
s = prs.slides.add_slide(L_CONTENT); clear_placeholders(s)
header(s, "YANG SUDAH & BELUM DIPUTUSKAN", "Empat belas keputusan sudah dikunci — lima masih menunggu jawaban")
tb(s, 0.42, 1.24, 6.0, 0.26, "SUDAH DIKUNCI", size=11, bold=True, color=GREEN)
data = [
    ["#", "Keputusan"],
    ["1", "2 role (User, Admin) + kanal TV read-only"],
    ["2", "Hierarki Group → Plant → Factory → Line"],
    ["3", "Template core + KPI tambahan per plant"],
    ["4", "Skor proses untuk KPI, skor hasil untuk monitoring"],
    ["5", "Pekan ISO (sudah konsisten di file)"],
    ["6", "Hari wajib Senin–Jumat dikurangi hari libur"],
    ["7", "KPI harian V/O biner"],
    ["8", "Recurrence dideteksi otomatis"],
    ["9", "Gate close: root cause + action + bukti"],
    ["10", "Healthy Check editable per tanggal"],
    ["11", "TV = profil tampilan yang diatur Admin"],
    ["12", "Pilot dimulai dari plant Snack"],
    ["13", "Skala audit menengah (laporan manajemen)"],
    ["14", "Sheet duplikat/kosong dipensiunkan"],
]
table(s, data, [0.55, 5.55], y=1.58, row_h=0.285, font=8.5, head_font=9,
      aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT])

tb(s, 6.95, 1.24, 5.9, 0.26, "MASIH MENUNGGU KEPUTUSAN", size=11, bold=True, color=AMBER)
pending = [
    ("Kalender libur", "Master tahunan yang diisi sekali, atau input manual per tanggal?"),
    ("Status N/A pada KPI", "Item seperti Gas Engine di line tanpa gas engine — keluar dari penyebut?"),
    ("Impor data historis", "5.817 kasus diimpor dengan flag legacy, atau mulai bersih dari go-live?"),
    ("Akun untuk Teknik", "99,7% kasus milik mereka — apakah mereka mendapat akun & KPI sendiri?"),
    ("Retensi data", "Berapa tahun sebelum diarsipkan?"),
]
y = 1.62
for i, (h, sub) in enumerate(pending):
    rect(s, 6.95, y, 5.85, 0.84, fill=WHITE, line_color=BORDER, line_w=0.75)
    rect(s, 6.95, y, 0.06, 0.84, fill=AMBER)
    tb(s, 7.18, y + 0.12, 5.5, 0.26, h, size=10.5, bold=True, color=NAVY)
    tb(s, 7.18, y + 0.38, 5.5, 0.50, sub, size=9, color=GREY, line=1.15)
    y += 1.00
reason_bar(s, 'Tiga hal tidak dapat dijawab dari file: kalender libur, status N/A, dan kebijakan impor data lama.',
              'Yang diminta hari ini bukan persetujuan membangun, melainkan jawaban atas tiga keputusan itu.')
footer(s, 19)

# ---------------------------------------------------------------- 20. CLOSING
s = prs.slides.add_slide(L_CONTENT)
clear_placeholders(s)
rect(s, 0.00, 0.00, 13.333, 7.5, fill=WHITE)
s.shapes.add_picture("docs/assets/gf_cover_band.jpg", Inches(0), Inches(5.90), Inches(13.333), Inches(1.60))
rect(s, 0.85, 1.55, 0.11, 1.10, fill=GOLD)
tb(s, 1.15, 1.55, 7.0, 0.60, "TERIMA KASIH", size=40, bold=True, color=NAVY)
tb(s, 1.15, 2.35, 8.6, 0.80,
   "Yang kami minta bukan persetujuan untuk membangun aplikasi,\nmelainkan persetujuan atas tiga keputusan yang masih terbuka.",
   size=13, color=GREY, line=1.30)
rect(s, 1.15, 3.42, 3.10, 0.03, fill=BORDER)
rows = [("Kalender libur", "master tahunan atau input per tanggal"),
        ("Status N/A pada KPI", "item tidak relevan keluar dari penyebut"),
        ("Impor data historis", "5.817 kasus dengan flag legacy, atau mulai bersih")]
y = 3.62
for k, v in rows:
    tb(s, 1.15, y, 2.55, 0.26, k, size=10.5, bold=True, color=NAVY)
    tb(s, 3.80, y, 7.2, 0.26, v, size=10.5, color=GREY)
    y += 0.36
tb(s, 1.15, 5.50, 8.0, 0.28, "Digitalisasi DMS · Pilot Snack · v1 · Oktober 2026", size=9, color=LGREY)

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides.__iter__.__self__._sldIdLst))
