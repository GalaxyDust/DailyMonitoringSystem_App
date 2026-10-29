#!/usr/bin/env python3
"""
Generator deck: Digitalisasi DMS (Plant Snack)
Jalankan dari root repo:  python3 docs/build_deck.py

Prinsip desain
- Background memakai layout asli template_master.pptx (bukan dibuat baru).
- Tipografi: Calibri. Warna: navy #071B56, aksen gold #C39E1A, netral abu.
- Gaya konsultasi: judul = kesimpulan, isi ringkas, bukan dekorasi.
- Semua slide memiliki blok ALASAN dan JAWABAN.
- Rancangan tampilan aplikasi (form/dashboard/TV) sengaja dikosongkan (placeholder),
  karena desain UI akan dibuat terpisah.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

SRC = "template_master.pptx"
OUT = "docs/DMS_Digitalisasi_v1.pptx"
LOGO = "docs/assets/gf_logo.png"

NAVY   = RGBColor(0x0B, 0x1F, 0x4E)
GOLD   = RGBColor(0xC3, 0x9E, 0x1A)
GOLD_L = RGBColor(0xF6, 0xF1, 0xE0)
TEAL   = RGBColor(0x2C, 0x7F, 0x8A)
TEAL_L = RGBColor(0xEA, 0xF3, 0xF4)
INK    = RGBColor(0x1F, 0x29, 0x37)
GREY   = RGBColor(0x6B, 0x72, 0x80)
LGREY  = RGBColor(0x9C, 0xA3, 0xAF)
RULE   = RGBColor(0xD8, 0xDD, 0xE5)
BG     = RGBColor(0xF6, 0xF7, 0xFA)
WHITE  = RGBColor(0xFF, 0xFF, 0xFF)
RED    = RGBColor(0xA6, 0x2B, 0x2B)
AMBER  = RGBColor(0xB2, 0x7A, 0x12)
GREEN  = RGBColor(0x3B, 0x6B, 0x3B)

prs = Presentation(SRC)

# --- kosongkan slide lama, master/layout/theme dipertahankan
sld = prs.slides._sldIdLst
for sid in list(sld):
    rId = sid.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
    prs.part.drop_rel(rId)
    sld.remove(sid)

L_CONTENT = prs.slide_layouts[4]   # "1_Title and Content"  (background putih + logo)
L_TITLE   = prs.slide_layouts[1]   # "Title Slide"          (cover: eagle + navy)
L_END     = prs.slide_layouts[5]   # "2_Title Slide"        (Thank you)


# ------------------------------------------------------------------ primitif
def clean(slide, keep=()):
    for sh in list(slide.shapes):
        if sh.is_placeholder and sh.placeholder_format.idx not in keep:
            sh._element.getparent().remove(sh._element)


def text(slide, x, y, w, h, s, size=12, bold=False, color=INK, align=PP_ALIGN.LEFT,
         italic=False, spacing=1.15, space_after=0, font="Calibri", anchor=MSO_ANCHOR.TOP):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, ln in enumerate(s.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.line_spacing = spacing
        p.space_after = Pt(space_after)
        r = p.add_run()
        r.text = ln
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.name = font
        r.font.color.rgb = color
    return box


def block(slide, x, y, w, h, fill=None, line=None, lw=0.75, radius=None):
    shape = MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE
    sh = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        sh.fill.background()
    else:
        sh.fill.solid()
        sh.fill.fore_color.rgb = fill
    if line is None:
        sh.line.fill.background()
    else:
        sh.line.color.rgb = line
        sh.line.width = Pt(lw)
    sh.shadow.inherit = False
    if radius:
        sh.adjustments[0] = radius
    return sh


def hrule(slide, x, y, w, color=RULE, h=0.012):
    block(slide, x, y, w, h, fill=color)


def head(slide, title, sub=None, kicker=None):
    """Kanvas bersih di atas master template: bar navy + logo, judul di area putih."""
    block(slide, 0, 0, 13.333, 7.5, fill=WHITE)
    block(slide, 0, 0, 13.333, 0.82, fill=RGBColor(0x07, 0x18, 0x45))
    slide.shapes.add_picture(LOGO, Inches(0.46), Inches(0.15), height=Inches(0.50))
    text(slide, 3.05, 0.30, 6.9, 0.22, "DAILY MONITORING SYSTEM  ·  PLANT SNACK",
         size=8.5, bold=True, color=GOLD)
    text(slide, 9.90, 0.30, 2.70, 0.22, "DIGITALISASI DMS", size=8.5,
         color=RGBColor(0x8E, 0x9C, 0xB8), align=PP_ALIGN.RIGHT)

    y = 1.06
    if kicker:
        text(slide, 0.86, y, 9.0, 0.20, kicker.upper(), size=8.5, bold=True, color=GOLD)
        y += 0.22
    text(slide, 0.86, y, 11.5, 0.50, title, size=21, bold=True, color=NAVY, spacing=1.02)
    y += 0.50
    if sub:
        text(slide, 0.86, y, 11.5, 0.26, sub, size=10, color=GREY)
        y += 0.28
    hrule(slide, 0.86, y + 0.02, 11.58, GOLD, 0.022)
    return y + 0.26


def foot(slide, n, note="Digitalisasi DMS · Plant Snack · draft diskusi"):
    text(slide, 0.86, 7.06, 8.0, 0.22, note, size=8, color=LGREY)
    text(slide, 11.85, 7.06, 0.60, 0.22, str(n), size=8, color=LGREY, align=PP_ALIGN.RIGHT)


def reason(slide, alasan, jawaban, y=6.46):
    """Blok tetap ALASAN / JAWABAN — pembeda utama deck ini."""
    w, h = 5.86, 0.54
    block(slide, 0.86, y, w, h, fill=GOLD_L)
    block(slide, 0.86, y, 0.045, h, fill=GOLD)
    text(slide, 1.06, y + 0.055, 1.0, 0.14, "ALASAN", size=6.5, bold=True, color=GOLD)
    text(slide, 2.00, y + 0.05, 4.55, 0.44, alasan, size=8, color=RGBColor(0x3E, 0x35, 0x1A), spacing=1.12)

    x2 = 0.86 + w + 0.14
    block(slide, x2, y, w, h, fill=TEAL_L)
    block(slide, x2, y, 0.045, h, fill=TEAL)
    text(slide, x2 + 0.20, y + 0.055, 1.0, 0.14, "JAWABAN", size=6.5, bold=True, color=TEAL)
    text(slide, x2 + 1.18, y + 0.05, 4.42, 0.44, jawaban, size=8, color=RGBColor(0x14, 0x36, 0x3B), spacing=1.12)


def table(slide, data, widths, x=0.86, y=1.55, row_h=0.34, size=9.5, head_size=9,
          first_bold=False, aligns=None, head_fill=NAVY):
    rows, cols = len(data), len(data[0])
    shp = slide.shapes.add_table(rows, cols, Inches(x), Inches(y),
                                 Inches(sum(widths)), Inches(row_h * rows))
    t = shp.table
    t.first_row = True
    t.horz_banding = False
    for i, w in enumerate(widths):
        t.columns[i].width = Inches(w)
    for r in range(rows):
        t.rows[r].height = Inches(row_h)
        for c in range(cols):
            cell = t.cell(r, c)
            cell.margin_left = Inches(0.07)
            cell.margin_right = Inches(0.07)
            cell.margin_top = Inches(0.02)
            cell.margin_bottom = Inches(0.02)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            cell.fill.fore_color.rgb = head_fill if r == 0 else (WHITE if r % 2 else BG)
            p = cell.text_frame.paragraphs[0]
            p.alignment = aligns[c] if aligns else PP_ALIGN.LEFT
            run = p.add_run()
            run.text = str(data[r][c])
            run.font.size = Pt(head_size if r == 0 else size)
            run.font.bold = (r == 0) or (first_bold and c == 0)
            run.font.name = "Calibri"
            run.font.color.rgb = WHITE if r == 0 else INK
    return shp


def kpi_strip(slide, items, y=1.62, h=1.02):
    """Tiga angka besar tanpa dekorasi berlebih."""
    w = 3.85
    gap = 0.19
    x = 0.70
    for big, label, note, col in items:
        block(slide, x, y, w, h, fill=BG, line=RULE)
        block(slide, x, y, 0.045, h, fill=col)
        text(slide, x + 0.22, y + 0.13, 1.9, 0.44, big, size=25, bold=True, color=col)
        text(slide, x + 0.22, y + 0.56, w - 0.40, 0.22, label, size=9.5, bold=True, color=INK)
        text(slide, x + 0.22, y + 0.76, w - 0.40, 0.20, note, size=8, color=GREY)
        x += w + gap


def rows_list(slide, x, y, w, items, size=10.5, gap=0.30, bullet=GOLD):
    """Daftar dengan penanda persegi kecil (bukan bullet bawaan)."""
    cy = y
    for head_, body in items:
        block(slide, x, cy + 0.075, 0.07, 0.07, fill=bullet)
        text(slide, x + 0.20, cy, w - 0.20, 0.22, head_, size=size, bold=True, color=INK)
        cy += 0.235
        if body:
            cpl = max(int((w - 0.24) * 15.2), 24)
            lines = -(-len(body) // cpl)
            text(slide, x + 0.20, cy, w - 0.20, 0.20 * lines + 0.04, body,
                 size=size - 1.5, color=GREY, spacing=1.15)
            cy += 0.20 * lines
        cy += gap
    return cy


def placeholder(slide, x, y, w, h, label, note=None):
    """Bidang kosong bertanda untuk rancangan tampilan (desain UI menyusul)."""
    block(slide, x, y, w, h, fill=RGBColor(0xF7, 0xF8, 0xFA))
    hrule(slide, x, y, w, RGBColor(0xC9, 0xD0, 0xDB))
    hrule(slide, x, y + h, w, RGBColor(0xC9, 0xD0, 0xDB))
    box = block(slide, x, y, 0.02, h, fill=RGBColor(0xC9, 0xD0, 0xDB))
    box = block(slide, x + w - 0.02, y, 0.02, h, fill=RGBColor(0xC9, 0xD0, 0xDB))
    text(slide, x + 0.16, y + h / 2 - 0.24, w - 0.32, 0.22, label.upper(), size=9,
         bold=True, color=RGBColor(0x8A, 0x93, 0xA5), align=PP_ALIGN.CENTER)
    if note:
        text(slide, x + 0.16, y + h / 2 + 0.02, w - 0.32, 0.24, note, size=8.5,
             color=RGBColor(0xA6, 0xAE, 0xBC), align=PP_ALIGN.CENTER)


# ============================================================ 01 · COVER
s = prs.slides.add_slide(L_TITLE)
clean(s)
# Layout asli dibiarkan utuh: pita putih + logo GarudaFood di atas,
# judul diletakkan di bidang navy di bawahnya.
s.shapes.add_picture(LOGO, Inches(0.94), Inches(1.18), height=Inches(0.92))
text(s, 0.86, 3.12, 10.0, 0.24, "DAILY MONITORING SYSTEM  ·  PLANT SNACK", size=10, bold=True, color=GOLD)
text(s, 0.86, 3.40, 11.4, 0.92, "Digitalisasi DMS: Dari Excel ke Insight",
     size=30, bold=True, color=WHITE, spacing=1.06)
hrule(s, 0.86, 4.36, 2.60, GOLD, 0.03)
text(s, 0.86, 4.52, 10.4, 0.28,
     "Kerangka penilaian, alur kerja, dan mesin insight untuk menggantikan workbook DMS.",
     size=10, color=RGBColor(0xC3, 0xCC, 0xDD))
text(s, 0.86, 4.86, 9.4, 0.24, "Logic & Design v1   ·   Oktober 2026   ·   draft diskusi, belum implementasi",
     size=8.5, color=RGBColor(0x93, 0xA1, 0xBB))

w, h = 5.86, 0.86
block(s, 0.86, 5.16, w, h, fill=WHITE)
block(s, 0.86, 5.16, 0.05, h, fill=GOLD)
text(s, 1.08, 5.26, 0.90, 0.16, "ALASAN", size=7, bold=True, color=GOLD)
text(s, 1.08, 5.46, 5.42, 0.48,
     "973 kasus ditutup tanpa akar masalah dan 94% kasus berulang tidak terdeteksi, "
     "padahal angkanya dipakai untuk laporan manajemen.", size=8.5,
     color=RGBColor(0x33, 0x2C, 0x14), spacing=1.2)

x2 = 0.86 + w + 0.14
block(s, x2, 5.16, w, h, fill=WHITE)
block(s, x2, 5.16, 0.05, h, fill=TEAL)
text(s, x2 + 0.22, 5.26, 1.00, 0.16, "JAWABAN", size=7, bold=True, color=TEAL)
text(s, x2 + 0.22, 5.46, 5.42, 0.48,
     "Kerangka aplikasi: form harian, dashboard tiga level, display TV, "
     "dan 14 aturan insight.", size=8.5, color=RGBColor(0x14, 0x36, 0x3B), spacing=1.2)


# ============================================================ 02 · AGENDA
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Agenda", "Bukti lebih dulu, keputusan di akhir", kicker="Alur pemaparan")
items = [
    ("01", "Kondisi & data", "Apa yang terjadi di workbook — dan mengapa angkanya tidak dapat dipercaya"),
    ("02", "Logika penilaian", "Sembilan cacat rumus Excel dan penggantinya di aplikasi"),
    ("03", "Kerangka aplikasi", "Hierarki plant, peran, alur loop tertutup, dan konfigurasi"),
    ("04", "Mesin insight", "14 aturan deteksi otomatis beserta format rekomendasinya"),
    ("05", "Tampilan", "Struktur halaman — desain antarmuka menyusul terpisah"),
    ("06", "Rencana & keputusan", "Pilot Snack 8 pekan dan hal yang masih terbuka"),
]
row_y = y + 0.06
for i, (no, name, desc) in enumerate(items):
    text(s, 0.86, row_y + 0.09, 0.55, 0.24, no, size=13, bold=True, color=GOLD)
    text(s, 1.32, row_y + 0.07, 2.55, 0.26, name, size=12, bold=True, color=NAVY)
    text(s, 3.95, row_y + 0.09, 8.55, 0.26, desc, size=10.5, color=GREY)
    if i < len(items) - 1:
        hrule(s, 0.86, row_y + 0.48, 11.58)
    row_y += 0.56
reason(s, "Enam bagian disusun dari bukti menuju keputusan, bukan dari daftar fitur.",
       "Setiap bagian ditutup dengan keputusan yang diusulkan, bukan hanya temuan.")
foot(s, 2)


# ============================================================ 03 · KONDISI
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Monitoring berjalan, tetapi angkanya tidak dapat dipertanggungjawabkan",
         "Tiga angka ini dihitung langsung dari 5.817 baris data di dalam workbook",
         kicker="Kondisi saat ini")
kpi_strip(s, [
    ("973", "kasus ditutup tanpa root cause", "dari 5.817 kasus", RED),
    ("94%", "kasus berulang tidak terdeteksi", "849 dari 902 kasus", AMBER),
    ("99,7%", "penyebab berada di luar kendali leader", "3.102 dari 3.112 kasus", NAVY),
], y=y + 0.02, h=0.94)
text(s, 0.86, 3.40, 11.55, 0.22, "AKAR MASALAHNYA ADA PADA LOGIKA FILE, BUKAN PADA ORANGNYA",
     size=9, bold=True, color=GOLD)
rows_list(s, 0.86, 3.72, 11.55, [
    ("Skor dinilai manual padahal bisa dihitung sistem",
     "30 dari 100 bobot dinilai manual: on-time dan kelengkapan file."),
    ("Tidak mengisi lebih menguntungkan daripada mengisi jelek",
     "AVERAGEIF mengabaikan sel kosong; satu hari sempurna = Ach 125%, skor 5."),
    ("Kasus tidak terhubung dengan checklist",
     "Item PICA dinilai manual, padahal buktinya ada di 5.817 kasus."),
    ("Tidak ada dimensi waktu",
     "Tidak ada aging, tren, atau peringatan sebelum masalah membesar."),
], size=9.5, gap=0.16)
reason(s, "Ketiga angka berasal dari workbook, bukan asumsi: status, label kasus, dan kolom PIC.",
       "Perbaikan diarahkan ke sistem — denominator, gate penutupan, dan deteksi otomatis.")
foot(s, 3)


# ============================================================ 04 · BASELINE
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Baseline data: 5.817 kasus, dua belas sheet, tiga tahun",
         "Audit workbook sebelum merancang — termasuk bagian yang tidak boleh dimigrasi",
         kicker="Data")
table(s, [
    ["Sumber", "Kasus", "Rentang", "Kondisi data"],
    ["Resume SHE", "1.185", "Jan 2023 – Des 2025", "Dua tabel ditumpuk; root cause & due date 0%"],
    ["Resume QC", "1.520", "Agu 2023 – Okt 2026", "320 kasus ditutup tanpa root cause"],
    ["Resume Prod", "3.112", "Agu 2023 – Okt 2026", "653 kasus ditutup tanpa root cause"],
    ["IIAA Snack", "120", "2024 – 2026", "Duplikat, 100% Close — tidak dimigrasi"],
], [2.30, 1.25, 3.05, 5.35], y=y + 0.02, row_h=0.34, size=9.5,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])

text(s, 0.86, 4.14, 5.4, 0.22, "POLA BERULANG TERBESAR", size=9, bold=True, color=GOLD)
table(s, [
    ["Pola", "Frekuensi"],
    ["M03 BCAT", "15×"],
    ["SVB13 BCAT", "14×"],
    ["MHM39 LSTR", "13×"],
    ["SVB19 LSTR", "13×"],
], [2.55, 1.35], x=0.86, y=4.44, row_h=0.27, size=9,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT])

text(s, 5.40, 4.14, 7.0, 0.22, "184 POLA BERULANG MENCAPAI 26,2% SELURUH KASUS", size=9, bold=True, color=GOLD)
rows_list(s, 5.40, 4.44, 7.04, [
    ("Terpusat di satu line", "3.014 dari 3.112 kasus produktivitas berasal dari Pilus L1."),
    ("Prefix mesin: MHM 26,8% · BCAT 14,1%", "Downtime median 50 menit; total 208.848 menit."),
    ("Standardisasi hampir tidak dijalankan", "OPL, PM, AM, CRMO dominan 'O' pada 88–98% kasus."),
], size=9.5, gap=0.10)
reason(s, "Sheet1 terbukti 100% konsisten ISO, dan 184 pola berulang mencakup 26,2% kasus.",
       "5.817 kasus dipakai sebagai baseline; 120 baris IIAA dibuang karena duplikat.")
foot(s, 4)


# ============================================================ 05 · KUALITAS DATA
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Kualitas data belum memadai untuk monitoring",
         "Tanpa perbaikan ini, aplikasi hanya memindahkan masalah lama ke tempat baru",
         kicker="Data")
table(s, [
    ["Field wajib", "SHE", "QC", "Prod", "Dampak bila dibiarkan"],
    ["Root cause", "0%", "79%", "78%", "Recurrence tidak dapat dianalisis"],
    ["Due date", "0%", "100%", "99%", "Tidak ada dasar aging dan eskalasi"],
    ["Action plan", "28%", "100%", "100%", "Kasus terbuka tanpa rencana penyelesaian"],
    ["Bukti / picture", "0%", "–", "–", "Penutupan tidak dapat diverifikasi"],
    ["Case category", "16%", "100%", "100%", "Recurrence mustahil dihitung"],
    ["Prioritas", "~100% High", "~100% High", "~100% High", "Tidak lagi berfungsi sebagai triase"],
], [2.35, 1.55, 1.35, 1.35, 5.35], y=y + 0.02, row_h=0.335, size=9.5, first_bold=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT])

block(s, 0.86, 4.86, 11.58, 0.86, fill=BG, line=RULE)
block(s, 0.86, 4.86, 0.045, 0.86, fill=GOLD)
text(s, 0.94, 4.96, 11.4, 0.20, "TEMUAN YANG PALING MAHAL", size=8.5, bold=True, color=GOLD)
text(s, 0.94, 5.18, 11.36, 0.46,
     "Status “Close” diisi ketika kolomnya sudah berisi, bukan ketika masalahnya selesai. "
     "973 kasus ditutup tanpa akar masalah, dan 22 kasus masih terbuka dengan due date terlampaui "
     "hingga 1.045 hari.", size=10, color=INK, spacing=1.25)
reason(s, "Diperiksa per field pada ketiga sheet; angka pada tabel adalah persentase keterisian.",
       "Empat field dijadikan wajib, dan kasus lama diberi penanda agar tidak membanjiri insight.")
foot(s, 5)


# ============================================================ 06 · CACAT LOGIKA
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Sembilan cacat logika pada workbook",
         "Setiap baris dapat ditunjukkan langsung dari rumus dan data aslinya",
         kicker="Logika penilaian")
table(s, [
    ["#", "Cacat", "Bukti di file", "Penggantinya di aplikasi"],
    ["1", "AVERAGEIF mengabaikan sel kosong", "1 hari diisi → Ach 125% → skor 5", "Penyebut = hari kerja − hari libur"],
    ["2", "Skor objektif dinilai manusia", "On-time & kelengkapan = 30 bobot", "Dihitung sistem"],
    ["3", "Enam item diringkas menjadi satu", "Hanya nilai total tersimpan", "Skor disimpan per item"],
    ["4", "Healthy Check bernilai konstan", "0,8 / 0,8 → selalu 0,6", "Parameter editable + simulasi"],
    ["5", "Recurrence diisi manual", "849 dari 902 salah label", "Deteksi otomatis"],
    ["6", "Penutupan tanpa bukti", "973 kasus", "Gate: root cause + action + bukti"],
    ["7", "Kasus tidak terhubung checklist", "Item PICA dinilai manual", "Skor item 5–6 dari data kasus"],
    ["8", "Tidak ada dimensi waktu", "Tidak ada aging / tren", "Aging, tren, lead indicator"],
    ["9", "Ambang batas tanpa pembulatan", "0,88 / 0,8 = 1,0999 → skor 3", "Bandingkan pada 2 desimal"],
], [0.50, 4.10, 4.00, 3.33], y=y + 0.02, row_h=0.40, size=9,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])
reason(s, "Semua cacat terverifikasi dari rumus asli, termasuk kasus 0,88/0,8 = 1,0999.",
       "Tidak ada satu pun yang dipertahankan hanya karena sudah dipakai bertahun-tahun.")
foot(s, 6)


# ============================================================ 07 · LAPORAN vs INSIGHT
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Keluaran aplikasi adalah tindakan, bukan angka",
         "Perbedaan antara laporan bulanan dan mesin insight", kicker="Nilai yang diusulkan")

block(s, 0.86, y + 0.02, 5.75, 3.90, fill=BG, line=RULE)
text(s, 0.96, y + 0.20, 5.2, 0.22, "LAPORAN SEKARANG", size=9.5, bold=True, color=GREY)
for i, (k, v) in enumerate([("Capaian", "Ach 83,7%"), ("Recurrence", "5,3%"),
                            ("Status", "142 kasus terbuka"), ("Kesimpulan", "diserahkan ke pembaca")]):
    yy = y + 0.58 + i * 0.52
    text(s, 0.96, yy, 1.55, 0.22, k, size=9, color=GREY)
    text(s, 2.60, yy, 3.6, 0.22, v, size=10.5, bold=True, color=INK)
    hrule(s, 0.96, yy + 0.34, 5.20)
text(s, 0.96, y + 2.92, 5.2, 0.60,
     "Angka tanpa sebab: rapat berhenti pada pertanyaan “kenapa bisa begitu?”",
     size=9.5, italic=True, color=GREY, spacing=1.2)

block(s, 6.88, y + 0.02, 5.75, 3.90, fill=WHITE, line=NAVY, lw=1.0)
block(s, 6.88, y + 0.02, 5.75, 0.05, fill=NAVY)
text(s, 7.14, y + 0.20, 5.2, 0.22, "KELUARAN YANG DIUSULKAN", size=9.5, bold=True, color=NAVY)
rows = [
    ("TEMUAN", "PICA Safety 83,7% — di bawah target 90%"),
    ("BUKTI", "142 dari 536 kasus terbuka; 37 lewat due date"),
    ("SEBAB", "Fokus pada Correction; OPL/PM 88–98% tidak terisi"),
    ("DAMPAK", "Index 3,00 — tepat di batas target"),
    ("REKOMENDASI", "Wajibkan Preventive Action untuk pola ≥3×"),
    ("PEMILIK", "Teknik, bukan leader line"),
]
for i, (k, v) in enumerate(rows):
    yy = y + 0.58 + i * 0.52
    text(s, 7.14, yy, 1.42, 0.22, k, size=8, bold=True, color=GOLD)
    text(s, 8.66, yy, 3.85, 0.42, v, size=9.5, color=INK, spacing=1.15)
reason(s, "Satu angka tidak menjelaskan penyebab; itu sebabnya rapat berulang membahas hal yang sama.",
       "Setiap insight wajib membawa bukti, sebab, dampak, rekomendasi, dan pemilik.")
foot(s, 7)


# ============================================================ 08 · ARSITEKTUR
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Struktur data mengikuti hierarki pabrik",
         "Empat lapis lokasi, satu tabel kasus, dan cakupan akses yang tegas",
         kicker="Kerangka aplikasi")

text(s, 0.86, y + 0.02, 5.4, 0.22, "HIERARKI LOKASI", size=9.5, bold=True, color=GOLD)
levels = [
    ("GROUP", "template core · konsolidasi · benchmarking"),
    ("PLANT", "Dairy · Exist · New · Snack — KPI & target khas plant"),
    ("FACTORY / BU", "Factory 10 (QC + Prod) · Factory 30 (SHE)"),
    ("LINE / AREA", "Pilus L1 (9) · Pellet L1 (10) · Line A–F"),
]
yy = y + 0.34
for i, (name, desc) in enumerate(levels):
    x = 0.70 + i * 0.28
    w = 5.40 - i * 0.28
    fill = NAVY if i == 0 else (WHITE if i % 2 else BG)
    block(s, x, yy, w, 0.62, fill=fill, line=RULE)
    text(s, x + 0.16, yy + 0.09, w - 0.3, 0.22, name, size=9.5, bold=True,
         color=WHITE if i == 0 else NAVY)
    text(s, x + 0.16, yy + 0.32, w - 0.3, 0.24, desc, size=8,
         color=RGBColor(0xC7, 0xD1, 0xE4) if i == 0 else GREY)
    yy += 0.70
text(s, 0.86, yy + 0.06, 5.4, 0.50,
     "Kode stabil: PLT-SNK, PLT-DRY, PLT-EX1, PLT-NW1.\nNama tampilan boleh berubah; kode tidak.",
     size=8.5, color=GREY, spacing=1.25)

text(s, 6.55, y + 0.02, 6.0, 0.22, "PERAN & CAKUPAN", size=9.5, bold=True, color=GOLD)
table(s, [
    ["Kemampuan", "User", "Admin", "TV"],
    ["Isi form meeting", "Ya", "Ya", "–"],
    ["Buat / perbarui kasus", "miliknya", "semua", "–"],
    ["Menutup kasus", "mengajukan", "menyetujui", "–"],
    ["Dashboard", "plant sendiri", "semua plant", "–"],
    ["Ubah bobot & target", "–", "Ya", "–"],
    ["Profil display", "–", "Ya", "tampil"],
], [2.75, 1.15, 1.15, 0.85], x=6.55, y=y + 0.34, row_h=0.34, size=9,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.CENTER])

block(s, 6.55, y + 2.90, 6.03, 0.78, fill=BG, line=RULE)
block(s, 6.55, y + 2.90, 0.045, 0.78, fill=RED)
text(s, 6.78, y + 3.00, 5.6, 0.60,
     "Setiap kueri wajib terfilter plant_id. Ini pencegahan kebocoran data antar plant "
     "yang paling sering terlewat.", size=9, color=INK, spacing=1.25)
reason(s, "Satu plant Snack sudah memiliki dua factory, dan satu entri Dairy sudah masuk ke sheet Snack.",
       "plant_id wajib pada semua transaksi; nama plant diganti kode stabil.")
foot(s, 8)


# ============================================================ 09 · ALUR
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Excel berhenti di dua tahap pertama",
         "Alur kerja diusulkan sebagai satu loop tertutup, bukan laporan satu arah",
         kicker="Kerangka aplikasi")
steps = [
    ("1", "Capture", "Meeting harian dan\nkasus baru"),
    ("2", "Detect", "Aging, recurrence,\nlonjakan, breach"),
    ("3", "Explain", "Skor dapat ditelusuri\nsampai kasus"),
    ("4", "Recommend", "Usulan tindakan dari\nriwayat penanganan"),
    ("5", "Act & verify", "PIC, tenggat, dan\npengecekan kambuh"),
]
bw, gap = 2.22, 0.20
x = 0.70
for i, (no, name, desc) in enumerate(steps):
    active = i < 2
    block(s, x, y + 0.06, bw, 1.42, fill=BG if active else WHITE, line=RULE)
    block(s, x, y + 0.06, bw, 0.045, fill=LGREY if active else GOLD)
    text(s, x + 0.16, y + 0.20, 0.3, 0.22, no, size=10, bold=True, color=LGREY if active else GOLD)
    text(s, x + 0.46, y + 0.20, bw - 0.6, 0.22, name.upper(), size=9, bold=True,
         color=GREY if active else NAVY)
    text(s, x + 0.16, y + 0.56, bw - 0.32, 0.62, desc, size=8.5,
         color=GREY if active else INK, spacing=1.2)
    text(s, x + 0.16, y + 1.16, bw - 0.32, 0.20, "sudah ada di Excel" if active else "belum ada",
         size=7.5, italic=True, color=LGREY)
    x += bw + gap

text(s, 0.86, y + 1.78, 11.55, 0.22, "YANG MEMBEDAKAN DENGAN DASHBOARD BIASA", size=9.5, bold=True, color=GOLD)
rows_list(s, 0.86, y + 2.08, 11.55, [
    ("Keluaran berupa tindakan", "Setiap temuan membawa pemilik dan tenggat, bukan hanya angka."),
    ("Dapat dijelaskan", "Setiap skor dapat ditelusuri sampai item dan kasus penyebabnya."),
    ("Menutup loop", "Sistem menanyakan kembali apakah kasus yang ditutup kambuh lagi."),
], size=10, gap=0.10)
reason(s, "Hanya capture dan detect yang berjalan saat ini; tidak ada penelusuran maupun verifikasi.",
       "Tiga tahap terakhir ditambahkan agar monitoring berhenti menjadi pelaporan.")
foot(s, 9)


# ============================================================ 10 · TAMPILAN (kosong)
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Struktur tampilan: empat kanal, satu sumber angka",
         "Kerangka halaman di bawah ini masih kosong — desain antarmuka dibuat terpisah",
         kicker="Tampilan")
canals = [
    ("FORM HARIAN", "Leader / DH\nsaat rapat berjalan", "Satu layar, target di bawah 5 menit"),
    ("DASHBOARD L1–L3", "Supervisor, admin,\nplant head", "Tiga level dengan audiens berbeda"),
    ("DISPLAY TV", "Lantai produksi\n(jarak 3–10 meter)", "Tanpa interaksi, rotasi otomatis"),
    ("HALAMAN ADMIN", "Admin plant\n& group", "Persetujuan, konfigurasi, audit"),
]
cw, cg = 2.86, 0.17
x = 0.70
for name, who, note in canals:
    placeholder(s, x, y + 0.06, cw, 2.05, name, "rancangan menyusul")
    text(s, x, y + 2.24, cw, 0.44, who, size=8.5, bold=True, color=NAVY, spacing=1.2)
    text(s, x, y + 2.72, cw, 0.40, note, size=8, color=GREY, spacing=1.2)
    x += cw + cg
text(s, 0.86, y + 3.28, 11.58, 0.52,
     "Catatan: seluruh gambar rancangan aplikasi (form, dashboard, TV) belum disertakan pada versi ini. "
     "Pembahasan hari ini difokuskan pada logika penilaian, alur kerja, dan mesin insight.",
     size=9, italic=True, color=GREY, spacing=1.25)
reason(s, "Desain antarmuka perlu dibahas dengan pengguna lapangan sebelum digambar.",
       "Deck ini hanya menetapkan struktur kanal dan batasannya, bukan tampilan visualnya.")
foot(s, 10)


# ============================================================ 11 · ADMIN (kosong)
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Kontrol admin: tiga hal yang harus dijaga",
         "Persetujuan penutupan, konfigurasi penilaian, dan jejak audit",
         kicker="Tampilan")
placeholder(s, 0.86, y + 0.06, 7.60, 3.05, "Rancangan halaman admin", "menyusul")
rows_list(s, 8.55, y + 0.08, 4.08, [
    ("Persetujuan", "Penutupan kasus disetujui pihak lain, bukan pengisi."),
    ("Konfigurasi", "Bobot, band skor, target, dan kalender libur memiliki tanggal berlaku."),
    ("Audit", "Setiap perubahan tercatat: siapa, kapan, sebelum–sesudah, alasan."),
], size=9.5, gap=0.26)
block(s, 0.86, y + 3.28, 7.60, 0.62, fill=BG, line=RULE)
block(s, 0.86, y + 3.28, 0.045, 0.62, fill=RED)
text(s, 0.92, y + 3.42, 7.2, 0.46,
     "Admin tidak dapat mengubah skor pada periode yang sudah dikunci; koreksi hanya melalui "
     "penyesuaian beralasan.", size=9, color=INK, spacing=1.25)
reason(s, "Mengubah bobot hari ini tanpa versioning berarti mengubah skor periode yang telah dilaporkan.",
       "Config memakai effective_date dan period lock.")
foot(s, 11)


# ============================================================ 12 · INSIGHT
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Mesin insight: 14 aturan, tiga kanal",
         "Setiap temuan wajib membawa bukti, sebab, dampak, rekomendasi, dan pemilik",
         kicker="Mesin insight")
table(s, [
    ["Kode", "Pemicu", "Contoh keluaran", "Kanal"],
    ["I-01", "Hari kerja tanpa meeting", "Line 10 tidak DMS tiga hari berturut", "L1 · TV"],
    ["I-02", "Due date lewat, status terbuka", "22 kasus terlambat; tertua 1.045 hari", "TV · L1"],
    ["I-03", "Signature sama ≥3× per 90 hari", "M03 BCAT 15× di Pilus L1", "TV · L2"],
    ["I-04", "Recurrence dengan root cause identik", "Correction sama 4× — naikkan ke Preventive", "L2"],
    ["I-05", "Tutup, tetapi OPL/PM/AM/CRMO = O", "88–98% kasus tidak pernah distandarkan", "L2 · L3"],
    ["I-06", "Tutup tanpa root cause atau bukti", "973 kasus ditutup tanpa akar masalah", "Admin"],
    ["I-07", "Prioritas High di atas 80%", "Field prioritas tidak lagi membedakan", "Admin"],
    ["I-08", "Ach dalam 1% di bawah band", "Rawan salah hitung — perlu pembulatan", "Admin"],
    ["I-09", "Tiga periode menurun berturut", "Checklist turun 4% per pekan", "L2 · L3"],
    ["I-10", "Satu line atau mesin di atas 20%", "Pilus L1 = 90% kasus; MHM 26,8%", "L3"],
    ["I-11", "Downtime besar dan sering", "MHM38 tujuh kali, median 50 menit", "L2"],
    ["I-12", "PICA lemah dan kasus baru naik", "Prediksi lonjakan pekan berikutnya", "L3"],
    ["I-13", "Field wajib kosong di atas 10%", "Kelengkapan data line ini 78%", "Admin"],
    ["I-14", "KPI non-controllable dinilai ke leader", "99,7% PIC kasus adalah Teknik", "Admin"],
], [0.72, 3.55, 6.05, 1.61], y=y + 0.02, row_h=0.262, size=8,
    head_size=8,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER])
reason(s, "849 dari 902 kasus berulang tetap dilabeli Occurrence, sehingga deteksi manual tidak mungkin.",
       "Peringkat prioritas menentukan maksimal tiga insight yang tampil di TV dan L1.")
foot(s, 12)


# ============================================================ 13 · RUMUS
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Logika penilaian final: tiga perbaikan kecil, satu arti baru",
         "Rumus dipakai apa adanya dari workbook, dengan tiga koreksi", kicker="Logika penilaian")

rules = [
    ("Nilai harian", "Σ (skor item ÷ 10 × bobot item) ÷ 100", "bobot 10/20/10/20/20/20 = 100"),
    ("Ach pekan", "Σ nilai harian ÷ (hari kerja − hari libur) ÷ target", "target 0,8"),
    ("Band skor", "≥120% → 5 · ≥110% → 4 · ≥100% → 3 · ≥90% → 2 · <90% → 1", "dibandingkan 2 desimal"),
    ("Nilai parameter", "skor × bobot parameter", "KPI 0,4 · Checklist 0,4 · Healthy 0,2"),
    ("DMS Index", "jumlah nilai parameter", "target 3 dari maksimum 5"),
]
yy = y + 0.04
for i, (name, formula, note) in enumerate(rules):
    block(s, 0.86, yy, 7.55, 0.60, fill=BG if i % 2 == 0 else WHITE, line=RULE)
    text(s, 0.88, yy + 0.08, 1.85, 0.22, name, size=9.5, bold=True, color=NAVY)
    text(s, 2.78, yy + 0.08, 3.60, 0.22, formula, size=9, color=INK)
    text(s, 2.78, yy + 0.32, 5.30, 0.20, note, size=8, color=GREY)
    yy += 0.66

text(s, 8.55, y + 0.02, 4.08, 0.22, "PERUBAHAN DAN DAMPAKNYA", size=9.5, bold=True, color=GOLD)
table(s, [
    ["Skenario", "Excel", "Aplikasi"],
    ["5 hari wajib, 1 terisi", "skor 5", "skor 1"],
    ["0,88 ÷ 0,80", "skor 3", "skor 4"],
    ["0,89 ÷ 0,80", "skor 4", "skor 4"],
], [1.85, 1.05, 1.18], x=8.55, y=y + 0.34, row_h=0.42, size=9,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER])
rows_list(s, 8.55, y + 2.08, 4.08, [
    ("Sel kosong dihitung nol", "Tidak mengisi tidak lagi lebih menguntungkan."),
    ("Ambang dibulatkan", "Selisih 1% tidak menjatuhkan satu band."),
    ("Healthy Check jadi parameter", "Dapat diubah Admin per tanggal berlaku."),
], size=9, gap=0.10)
reason(s, "Denominator dan ambang batas adalah dua sumber selisih hasil antara Excel dan aplikasi.",
       "Penyebut memakai hari kerja, dan perbandingan band memakai dua desimal.")
foot(s, 13)


# ============================================================ 14 · RENCANA
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Pilot Snack: delapan pekan, lima ukuran keberhasilan",
         "Keberhasilan diukur dari pemakaian, bukan dari aplikasi selesai dibangun",
         kicker="Rencana")
phases = [
    ("0", "Fondasi", "2 pekan", "Master data bersih, config versioned, akses"),
    ("1", "Capture", "3 pekan", "Form meeting, form kasus, persetujuan"),
    ("2", "Measure", "2 pekan", "Engine skor dan dashboard L1"),
    ("3", "Insight", "2 pekan", "Delapan aturan pertama"),
    ("4", "Display", "1 pekan", "Display TV satu area"),
    ("5", "Analitik", "2 pekan", "Dashboard L2–L3 dan ekspor"),
]
yy = y + 0.04
for i, (no, name, dur, desc) in enumerate(phases):
    block(s, 0.86, yy, 7.35, 0.52, fill=WHITE, line=RULE)
    text(s, 0.86, yy + 0.15, 0.30, 0.22, no, size=10, bold=True, color=GOLD)
    text(s, 1.22, yy + 0.15, 1.55, 0.22, name.upper(), size=9, bold=True, color=NAVY)
    text(s, 2.85, yy + 0.15, 0.85, 0.22, dur, size=8.5, color=GOLD)
    text(s, 3.78, yy + 0.15, 4.10, 0.30, desc, size=8.5, color=GREY)
    yy += 0.58

text(s, 8.45, y + 0.02, 4.18, 0.22, "UKURAN KEBERHASILAN (8 PEKAN)", size=9.5, bold=True, color=GOLD)
table(s, [
    ["Ukuran", "Target"],
    ["Kepatuhan isi form", "≥ 90%"],
    ["Kelengkapan root cause", "≥ 95%"],
    ["Kasus terlambat", "turun 50%"],
    ["Pola ≥3× punya action", "100%"],
    ["Insight ditindaklanjuti", "≥ 70%"],
], [2.95, 1.23], x=8.45, y=y + 0.34, row_h=0.38, size=9,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER])
block(s, 8.45, y + 2.86, 4.18, 0.94, fill=BG, line=RULE)
block(s, 8.45, y + 2.86, 0.045, 0.94, fill=GOLD)
text(s, 8.66, y + 2.95, 3.85, 0.20, "SETELAH PILOT STABIL", size=8, bold=True, color=GOLD)
text(s, 8.66, y + 3.16, 3.85, 0.58,
     "Generalisasi template plant, lalu Exist Plant → Dairy → New Plant.",
     size=8.5, color=INK, spacing=1.2)
reason(s, "Snack dipilih karena template dan data historisnya sudah tersedia untuk validasi.",
       "Delapan pekan, dengan lima ukuran pemakaian yang dapat diperiksa tiap pekan.")
foot(s, 14)


# ============================================================ 15 · KEPUTUSAN
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Empat belas keputusan dikunci, tiga masih terbuka",
         "Yang diminta pada sesi ini adalah jawaban atas tiga hal di kanan",
         kicker="Keputusan")
table(s, [
    ["#", "Keputusan"],
    ["1", "Dua peran: User dan Admin, plus kanal display"],
    ["2", "Hierarki Group → Plant → Factory → Line"],
    ["3", "Template core ditambah KPI khas plant"],
    ["4", "Skor proses untuk KPI, skor hasil untuk monitoring"],
    ["5", "Pekan memakai ISO"],
    ["6", "Hari wajib Senin–Jumat dikurangi hari libur"],
    ["7", "KPI harian bersifat V/O"],
    ["8", "Recurrence dideteksi otomatis"],
    ["9", "Penutupan wajib: root cause, action, bukti"],
    ["10", "Healthy Check dapat diubah per tanggal"],
    ["11", "Display TV memakai profil yang diatur Admin"],
    ["12", "Pilot dimulai dari plant Snack"],
    ["13", "Skala audit menengah (laporan manajemen)"],
    ["14", "Sheet duplikat dan kosong dipensiunkan"],
], [0.48, 5.47], y=y + 0.02, row_h=0.266, size=8.5, head_size=8.5,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT])

pending = [
    ("Kalender libur", "Master tahunan yang diisi sekali, atau input per tanggal?"),
    ("Status N/A pada KPI", "Item yang tidak relevan keluar dari penyebut?"),
    ("Impor data historis", "5.817 kasus dengan penanda legacy, atau mulai bersih?"),
]
yy = y + 0.04
for name, q in pending:
    block(s, 7.05, yy, 5.43, 0.86, fill=WHITE, line=RULE)
    block(s, 7.05, yy, 0.045, 0.86, fill=AMBER)
    text(s, 7.27, yy + 0.12, 5.00, 0.22, name, size=10, bold=True, color=NAVY)
    text(s, 7.27, yy + 0.38, 5.00, 0.42, q, size=9, color=GREY, spacing=1.2)
    yy += 0.96
text(s, 7.05, yy + 0.06, 5.43, 0.62,
     "Dua hal lain menyusul: akun untuk Teknik (99,7% kasus milik mereka) dan kebijakan retensi data.",
     size=8.5, italic=True, color=GREY, spacing=1.2)
reason(s, "Tiga hal ini tidak dapat disimpulkan dari file: kalender libur, status N/A, dan kebijakan impor.",
       "Mohon arahan pada sesi ini agar ruang lingkup pilot dapat dikunci.")
foot(s, 15)


# ============================================================ 16 · PENUTUP
s = prs.slides.add_slide(L_CONTENT)
clean(s)
block(s, 0, 0, 13.333, 7.5, fill=WHITE)
block(s, 0, 0, 13.333, 0.82, fill=RGBColor(0x07, 0x18, 0x45))
s.shapes.add_picture(LOGO, Inches(0.46), Inches(0.15), height=Inches(0.50))
text(s, 3.05, 0.30, 6.9, 0.22, "DAILY MONITORING SYSTEM  ·  PLANT SNACK",
     size=8.5, bold=True, color=GOLD)
text(s, 9.90, 0.30, 2.70, 0.22, "DIGITALISASI DMS", size=8.5,
     color=RGBColor(0x8E, 0x9C, 0xB8), align=PP_ALIGN.RIGHT)

text(s, 0.86, 1.86, 11.0, 0.28, "PENUTUP", size=8.5, bold=True, color=GOLD)
text(s, 0.86, 2.18, 11.4, 0.80, "Tiga keputusan menunggu arahan Bapak/Ibu", size=30, bold=True, color=NAVY)
hrule(s, 0.86, 3.06, 11.58, GOLD, 0.022)
text(s, 0.86, 3.24, 11.3, 0.60,
     "Kalender libur  ·  status N/A pada KPI  ·  kebijakan impor 5.817 kasus historis",
     size=13, color=INK)
text(s, 0.86, 3.94, 10.6, 0.80,
     "Setelah ketiganya ditetapkan, ruang lingkup pilot Snack dapat dikunci dan jadwal delapan pekan "
     "bisa disusun. Dokumen logika dan desain menyertai deck ini sebagai lampiran.",
     size=10, color=GREY, spacing=1.35)
text(s, 0.86, 4.92, 11.0, 0.30, "Terima kasih.", size=15, bold=True, color=NAVY)

text(s, 0.86, 6.72, 8.0, 0.22, "Logic & Design v1  ·  Plant Snack  ·  Oktober 2026", size=8.5, color=LGREY)
reason(s, "Ketiganya adalah kebijakan, bukan angka: tidak dapat disimpulkan dari workbook.",
       "Arahan pada sesi ini mengunci lingkup pilot dan tanggal mulai.")
text(s, 11.85, 7.06, 0.60, 0.22, "16", size=8, color=LGREY, align=PP_ALIGN.RIGHT)


prs.save(OUT)
print("saved", OUT)
