#!/usr/bin/env python3
"""
Generator deck: Digitalisasi DMS — versi umum, kerangka SGA (8 langkah).
Jalankan dari root repo:  python3 docs/build_deck.py

Prinsip
- Background & layout memakai template_master.pptx apa adanya.
- Kerangka poin mengikuti deck SGA Akatsuki: 1A-1E, 2A-2D, 3A-3B, 4A-4C,
  5A-5B, 6A-6B, 7, 8 — sehingga tiap slide menjawab satu pertanyaan baku.
- Isi dibuat umum (berlaku untuk semua plant); angka workbook dipakai sebagai
  sampel/ilustrasi, bukan patokan plant tertentu.
- Setiap slide punya blok ALASAN & JAWABAN. Judul slide = kesimpulan.
- Rancangan tampilan aplikasi dikosongkan (desain UI menyusul).
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

SRC = "template_master.pptx"
OUT = "docs/DMS_Digitalisasi_v1.pptx"
LOGO = "docs/assets/gf_logo.png"

NAVY   = RGBColor(0x0B, 0x1F, 0x4E)
NAVY_D = RGBColor(0x07, 0x18, 0x45)
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

L_CONTENT = prs.slide_layouts[4]   # "1_Title and Content"
L_TITLE   = prs.slide_layouts[1]   # "Title Slide" (cover)


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


def block(slide, x, y, w, h, fill=None, line=None, lw=0.75, radius=None, dash=None):
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
        if dash:
            from pptx.enum.dml import MSO_LINE_DASH_STYLE
            sh.line.dash_style = MSO_LINE_DASH_STYLE.DASH
    sh.shadow.inherit = False
    if radius:
        sh.adjustments[0] = min(radius, 0.5)
    return sh


def card(slide, x, y, w, h, fill=WHITE, line=RULE, radius=0.07, lw=0.9):
    """Panel bersudut membulat — pengganti kotak tajam."""
    return block(slide, x, y, w, h, fill=fill, line=line, lw=lw, radius=radius)


def hrule(slide, x, y, w, color=RULE, h=0.012):
    block(slide, x, y, w, h, fill=color)


def line(slide, x1, y1, x2, y2, color=RULE, w=1.0):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                   Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(w)
    return c


def head(slide, title, sub=None, code=None, stage=None):
    """Kanvas bersih di atas master template: bar navy + logo, judul di area putih."""
    block(slide, 0, 0, 13.333, 7.5, fill=WHITE)
    block(slide, 0, 0, 13.333, 0.82, fill=NAVY_D)
    slide.shapes.add_picture(LOGO, Inches(0.46), Inches(0.15), height=Inches(0.50))
    text(slide, 3.05, 0.29, 6.6, 0.24, "DAILY MONITORING SYSTEM  ·  SEMUA PLANT",
         size=9.5, bold=True, color=GOLD)
    text(slide, 9.20, 0.29, 3.40, 0.24, "PENILAIAN & INSIGHT HARIAN", size=9,
         color=RGBColor(0x8E, 0x9C, 0xB8), align=PP_ALIGN.RIGHT)

    y = 1.04
    if code or stage:
        if stage:
            text(slide, 0.86, y, 3.0, 0.22, stage.upper(), size=8, bold=True,
                 color=LGREY)
        if code:
            text(slide, 3.10, y, 9.4, 0.22, code.upper(), size=9.5, bold=True, color=GOLD)
        y += 0.24
    text(slide, 0.86, y, 11.5, 0.50, title, size=22, bold=True, color=NAVY, spacing=1.02)
    y += 0.50
    if sub:
        text(slide, 0.86, y, 11.5, 0.28, sub, size=10.5, color=GREY, spacing=1.2)
        y += 0.30
    hrule(slide, 0.86, y + 0.03, 11.58, GOLD, 0.022)
    return y + 0.24


def foot(slide, n):
    text(slide, 0.86, 7.05, 8.0, 0.24, "Digitalisasi DMS · semua plant · draft diskusi",
         size=8.5, color=LGREY)
    text(slide, 11.85, 7.05, 0.60, 0.24, str(n), size=8.5, color=LGREY, align=PP_ALIGN.RIGHT)


def reason(slide, alasan, jawaban, y=6.36):
    """Dua panel membulat ALASAN / JAWABAN — ukuran teks dibuat nyaman dibaca."""
    w, h = 5.80, 0.66
    card(slide, 0.86, y, w, h, fill=GOLD_L, line=RGBColor(0xE6, 0xD9, 0xB2), radius=0.12)
    block(slide, 1.02, y + 0.13, 0.05, h - 0.26, fill=GOLD, radius=0.5)
    text(slide, 1.18, y + 0.10, 1.20, 0.18, "ALASAN", size=8, bold=True, color=GOLD)
    text(slide, 1.18, y + 0.29, w - 0.46, 0.34, alasan, size=9.5,
         color=RGBColor(0x3E, 0x35, 0x1A), spacing=1.15)

    x2 = 0.86 + w + 0.18
    card(slide, x2, y, w, h, fill=TEAL_L, line=RGBColor(0xBF, 0xD8, 0xDB), radius=0.12)
    block(slide, x2 + 0.16, y + 0.13, 0.05, h - 0.26, fill=TEAL, radius=0.5)
    text(slide, x2 + 0.32, y + 0.10, 1.30, 0.18, "JAWABAN", size=8, bold=True, color=TEAL)
    text(slide, x2 + 0.32, y + 0.29, w - 0.46, 0.34, jawaban, size=9.5,
         color=RGBColor(0x14, 0x36, 0x3B), spacing=1.15)


def table(slide, data, widths, x=0.86, y=1.55, row_h=0.38, size=10, head_size=9.5,
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


def kpi_strip(slide, items, y=1.62, h=1.04):
    w, gap, x = 3.85, 0.19, 0.86
    for big, label, note, col in items:
        card(slide, x, y, w, h, fill=BG, line=RULE, radius=0.09)
        block(slide, x + 0.14, y + 0.14, 0.05, h - 0.28, fill=col, radius=0.5)
        text(slide, x + 0.30, y + 0.12, 2.0, 0.42, big, size=24, bold=True, color=col)
        text(slide, x + 0.30, y + 0.56, w - 0.52, 0.24, label, size=9.5, bold=True, color=INK)
        text(slide, x + 0.30, y + 0.80, w - 0.52, 0.24, note, size=9, color=GREY)
        x += w + gap


def rows_list(slide, x, y, w, items, size=10.5, gap=0.26, bullet=GOLD):
    cy = y
    for head_, body in items:
        block(slide, x, cy + 0.075, 0.07, 0.07, fill=bullet)
        text(slide, x + 0.20, cy, w - 0.20, 0.22, head_, size=size, bold=True, color=INK)
        cy += 0.225
        if body:
            cpl = max(int((w - 0.24) * 15.2), 24)
            lines = -(-len(body) // cpl)
            text(slide, x + 0.20, cy, w - 0.20, 0.20 * lines + 0.04, body,
                 size=size - 1, color=GREY, spacing=1.14)
            cy += 0.19 * lines
        cy += gap
    return cy


def placeholder(slide, x, y, w, h, label, note=None):
    """Panel membulat bertanda untuk rancangan tampilan (desain UI menyusul)."""
    card(slide, x, y, w, h, fill=RGBColor(0xF7, 0xF8, 0xFA),
         line=RGBColor(0xC2, 0xCA, 0xD6), radius=0.06, lw=1.0)
    text(slide, x + 0.16, y + h / 2 - 0.26, w - 0.32, 0.24, label.upper(), size=10.5,
         bold=True, color=RGBColor(0x86, 0x90, 0xA0), align=PP_ALIGN.CENTER)
    if note:
        text(slide, x + 0.16, y + h / 2 + 0.00, w - 0.32, 0.24, note, size=9,
             color=RGBColor(0xA3, 0xAB, 0xB9), align=PP_ALIGN.CENTER)


def img_slot(slide, x, y, w, h, caption, note="sisipkan foto atau gambar di sini"):
    """Kotak gambar berbingkai putus-putus: tinggal diganti foto/diagram nanti."""
    card(slide, x, y, w, h, fill=RGBColor(0xFA, 0xFB, 0xFD),
         line=RGBColor(0xBF, 0xC7, 0xD4), radius=0.05, lw=1.15)
    ic = 0.30
    cx, cy = x + w / 2, y + h / 2 - 0.20
    card(slide, cx - ic / 2, cy - ic / 2, ic, ic, fill=WHITE,
         line=RGBColor(0xC2, 0xCA, 0xD6), radius=0.18, lw=1.0)
    text(slide, cx - ic / 2, cy - 0.11, ic, 0.22, "+", size=13, bold=True,
         color=RGBColor(0xA3, 0xAB, 0xB9), align=PP_ALIGN.CENTER)
    text(slide, x + 0.18, y + h / 2 + 0.14, w - 0.36, 0.24, caption.upper(), size=9.5,
         bold=True, color=RGBColor(0x86, 0x90, 0xA0), align=PP_ALIGN.CENTER)
    text(slide, x + 0.18, y + h / 2 + 0.36, w - 0.36, 0.24, note, size=8.5,
         color=RGBColor(0xA9, 0xB1, 0xBE), align=PP_ALIGN.CENTER)



def bars(slide, items, y, x=0.86, label_w=3.35, max_w=7.40, row_h=0.56):
    """Batang horizontal sederhana untuk kontribusi (%) tanpa dekorasi."""
    for label, pct, col in items:
        text(slide, x, y + 0.04, label_w - 0.15, 0.24, label, size=10, color=INK)
        bw = max_w * pct / 100.0
        block(slide, x + label_w, y + 0.05, max_w, 0.24, fill=RGBColor(0xEE, 0xF0, 0xF4), radius=0.5)
        block(slide, x + label_w, y + 0.05, bw, 0.24, fill=col, radius=0.5)
        text(slide, x + label_w + max_w + 0.12, y + 0.04, 0.70, 0.24,
             f"{pct}%", size=10, bold=True, color=col)
        y += row_h
    return y


# ============================================================ 01 · COVER
s = prs.slides.add_slide(L_TITLE)
clean(s)
s.shapes.add_picture(LOGO, Inches(0.94), Inches(1.16), height=Inches(0.90))
text(s, 0.86, 3.08, 10.0, 0.24, "DAILY MONITORING SYSTEM  ·  DAIRY · EXIST · NEW PLANT · SNACK",
     size=9.5, bold=True, color=GOLD)
text(s, 0.86, 3.34, 11.6, 1.00, "Menutup Celah Monitoring Harian:\nNol Penilaian Manual",
     size=28, bold=True, color=WHITE, spacing=1.06)
hrule(s, 0.86, 4.34, 2.60, GOLD, 0.03)
text(s, 0.86, 4.50, 10.6, 0.28,
     "Satu kerangka penilaian, satu alur tindakan, satu mesin insight untuk seluruh plant.",
     size=10, color=RGBColor(0xC3, 0xCC, 0xDD))
text(s, 0.86, 4.82, 9.6, 0.24, "Usulan rancangan   ·   Oktober 2026   ·   draft diskusi, belum implementasi",
     size=8.5, color=RGBColor(0x93, 0xA1, 0xBB))

w, h = 5.80, 0.92
card(s, 0.86, 5.12, w, h, fill=WHITE, line=RGBColor(0xE6, 0xD9, 0xB2), radius=0.10)
block(s, 1.02, 5.28, 0.05, h - 0.32, fill=GOLD, radius=0.5)
text(s, 1.18, 5.24, 1.10, 0.18, "ALASAN", size=8, bold=True, color=GOLD)
text(s, 1.18, 5.44, w - 0.48, 0.52,
     "Monitoring berjalan di semua plant, tetapi skornya masih dinilai manusia dan "
     "penutupan kasus tidak diverifikasi.", size=9.5,
     color=RGBColor(0x33, 0x2C, 0x14), spacing=1.18)

x2 = 0.86 + w + 0.18
card(s, x2, 5.12, w, h, fill=WHITE, line=RGBColor(0xBF, 0xD8, 0xDB), radius=0.10)
block(s, x2 + 0.16, 5.28, 0.05, h - 0.32, fill=TEAL, radius=0.5)
text(s, x2 + 0.32, 5.24, 1.15, 0.18, "JAWABAN", size=8, bold=True, color=TEAL)
text(s, x2 + 0.32, 5.44, w - 0.48, 0.52,
     "Delapan langkah perbaikan: masalah, sebab, tindakan, ukuran, standar — "
     "berlaku untuk plant mana pun.", size=9.5, color=RGBColor(0x14, 0x36, 0x3B), spacing=1.2)


# ============================================================ 02 · PETA 8 LANGKAH
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Delapan langkah: masalah, sebab, tindakan, lalu standar",
         "Setiap langkah menjawab satu pertanyaan baku — sama untuk semua plant",
         code="Peta penyajian", stage="Kerangka")
steps = [
    ("1", "Identifikasi masalah", "Apa yang salah, seberapa besar, mau ke mana?", "1A – 1E"),
    ("2", "Analisis akar masalah", "Mengapa hal itu terjadi?", "2A – 2D"),
    ("3", "Penyebab dominan", "Mana yang paling menentukan?", "3A – 3B"),
    ("4", "Rencana perbaikan", "Apa yang dikerjakan, oleh siapa, kapan?", "4A – 4C"),
    ("5", "Pelaksanaan", "Apa yang dibangun dan diuji?", "5A – 5B"),
    ("6", "Monitoring & evaluasi", "Apakah hasilnya sesuai target?", "6A – 6B"),
    ("7", "Standarisasi", "Bagaimana caranya agar tidak kembali?", "7A – 7D"),
    ("8", "Tema berikutnya", "Apa langkah setelah ini?", "8A – 8B"),
]
cy = y + 0.06
for no, name, q, rng in steps:
    text(s, 0.86, cy + 0.02, 0.40, 0.24, no, size=13, bold=True, color=GOLD)
    text(s, 1.28, cy, 3.05, 0.24, name.upper(), size=10, bold=True, color=NAVY)
    text(s, 4.55, cy + 0.02, 6.55, 0.24, q, size=9.5, color=GREY)
    text(s, 11.10, cy + 0.02, 1.30, 0.24, rng, size=8.5, color=LGREY, align=PP_ALIGN.RIGHT)
    hrule(s, 0.86, cy + 0.34, 11.58)
    cy += 0.44
reason(s, "Kerangka delapan langkah adalah bahasa baku perbaikan di perusahaan, bukan struktur baru.",
       "Pembaca mana pun dapat menilai kelengkapan usulan tanpa mengenal istilah DMS lebih dulu.")
foot(s, 2)


# ============================================================ 03 · 1A
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Masalahnya penilaian yang manual, bukan orangnya",
         "Diuji pada satu plant; polanya berlaku untuk semua plant",
         code="1A · Penentuan masalah", stage="Langkah 1")
kpi_strip(s, [
    ("5.817", "baris kasus diperiksa", "seluruh sheet resume", NAVY),
    ("973", "kasus ditutup tanpa akar masalah", "16,7% dari total", RED),
    ("94%", "kasus berulang salah label", "849 dari 902 kasus", AMBER),
], y=y + 0.02, h=0.94)
rows_list(s, 0.86, 3.52, 7.35, [
    ("Skor dinilai manusia", "Sebagian bobot diisi manual, sehingga hasilnya bergantung pada ingatan."),
    ("Penutupan tidak diverifikasi", "Status selesai diisi saat kolomnya berisi, bukan saat masalahnya tuntas."),
    ("Tidak ada dimensi waktu", "Belum ada aging, tren, atau peringatan sebelum masalah membesar."),
], size=10, gap=0.26)
img_slot(s, 8.45, 3.46, 3.99, 2.20, "Bukti kondisi saat ini",
         "salinan tangkapan layar workbook atau foto rapat")
reason(s, "Ketiga gejala muncul di semua sheet, sehingga bukan kebiasaan satu plant atau satu orang.",
       "Masalah utama dirumuskan pada mekanisme penilaian dan penutupan kasus.")
foot(s, 3)


# ============================================================ 04 · 1B
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Data cukup untuk mendiagnosis, belum cukup untuk menilai",
         "Sumber data diseragamkan di semua plant; angka di bawah adalah contoh satu plant",
         code="1B · Pengumpulan data", stage="Langkah 1")
table(s, [
    ["Sumber", "Kasus", "Rentang", "Kelengkapan akar masalah", "Status pakai"],
    ["Resume SHE", "1.185", "2023 – 2025", "0%", "Dipakai"],
    ["Resume QC", "1.520", "2023 – 2026", "79%", "Dipakai"],
    ["Resume Produksi", "3.112", "2023 – 2026", "78%", "Dipakai"],
    ["IIAA Snack", "120", "2024 – 2026", "duplikat", "Tidak dipakai"],
], [2.55, 1.05, 1.85, 2.60, 2.10], y=y + 0.02, row_h=0.38, size=9.5,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT])
text(s, 0.86, 4.28, 11.5, 0.22, "EMPAT KOLOM YANG WAJIB LENGKAP SEBELUM DATA DIPAKAI",
     size=9, bold=True, color=GOLD)
rows_list(s, 0.86, 4.58, 5.55, [
    ("Identitas kasus", "Plant, line, mesin, tanggal, kategori."),
    ("Sebab dan tindakan", "Root cause, action plan, PIC, due date."),
], size=9.5, gap=0.16)
rows_list(s, 5.95, 4.58, 6.45, [
    ("Bukti penutupan", "Dokumen atau foto, plus penyetuju."),
    ("Label status", "Open, Close, dan tanda berulang."),
], size=9.5, gap=0.16)
reason(s, "Tanpa empat kolom itu, analisis berulang dan aging mustahil dihitung.",
       "Template pengumpulan dibuat sama; tiap plant mengisi angkanya sendiri.")
foot(s, 4)


# ============================================================ 05 · 1C
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Tema: satu cara menilai, dipakai semua plant",
         "Tema dipilih karena dampaknya besar, berada dalam kendali tim, dan berulang setiap hari",
         code="1C · Penentuan tema", stage="Langkah 1")
card(s, 0.86, y + 0.02, 11.58, 1.02, fill=BG, line=RULE, radius=0.09)
block(s, 0.86, y + 0.02, 0.045, 1.02, fill=NAVY)
text(s, 1.10, y + 0.12, 11.0, 0.22, "TEMA YANG DIUSULKAN", size=9, bold=True, color=GOLD)
text(s, 1.10, y + 0.36, 11.0, 0.56,
     "Menghapus penilaian manual pada monitoring harian, sehingga setiap angka dapat ditelusuri "
     "sampai kasus dan setiap kasus ditutup dengan bukti.", size=11, color=INK, spacing=1.2)
table(s, [
    ["Kriteria pemilihan tema", "Penilaian", "Alasan"],
    ["Dampak", "Tinggi", "Angka dipakai untuk penilaian KPI dan laporan manajemen"],
    ["Dalam kendali tim", "Ya", "Mekanisme penilaian dan penutupan ada di proses sendiri"],
    ["Keterulangan", "Harian", "Muncul setiap hari kerja di semua plant"],
    ["Kelayakan", "Tinggi", "Tidak menuntut investasi mesin; cukup aturan dan sistem"],
], [3.05, 1.60, 6.93], y=y + 1.16, row_h=0.345, size=9.5, first_bold=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT])
card(s, 0.86, 5.30, 11.58, 0.86, fill=BG, line=RULE, radius=0.09)
block(s, 1.02, 5.44, 0.05, 0.58, fill=NAVY, radius=0.5)
text(s, 1.20, 5.40, 10.9, 0.20, "CATATAN RUANG LINGKUP", size=8.5, bold=True, color=NAVY)
text(s, 1.20, 5.62, 10.9, 0.46,
     "Yang diperbaiki adalah cara menilai dan menutup kasus, bukan mesin atau proses produksinya. "
     "Karena itu perbaikan ini dapat diterapkan di plant mana pun tanpa investasi peralatan.",
     size=9.5, color=INK, spacing=1.2)
reason(s, "Tema dipilih dengan empat kriteria yang sama seperti pemilihan tema perbaikan lain.",
       "Ruang lingkupnya proses penilaian dan pelaporan, bukan proyek perangkat keras.")
foot(s, 5)


# ============================================================ 06 · 1D
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Target delapan pekan: nol penilaian manual, nol penutupan tanpa bukti",
         "Semua target dapat diukur pekanan dan berlaku sama di setiap plant",
         code="1D · Penetapan target", stage="Langkah 1")
table(s, [
    ["Indikator", "Sekarang (sampel)", "Target", "Cara ukur"],
    ["Skor yang dinilai manual", "30% bobot", "0%", "Semua item dihitung sistem"],
    ["Kasus ditutup tanpa akar masalah", "973 kasus", "0 kasus", "Gate penutupan menolak simpan"],
    ["Kasus berulang terdeteksi", "6% (53 dari 902)", "100%", "Deteksi otomatis per pola"],
    ["Kepatuhan mengisi form", "belum terukur", "≥ 90%", "Hari wajib terisi ÷ hari wajib"],
    ["Insight yang ditindaklanjuti", "belum ada", "≥ 70%", "Tindakan tercatat atas temuan"],
    ["Waktu menyusun laporan harian", "manual, jam-an", "≤ 5 menit", "Waktu respons dasbor"],
], [3.55, 2.35, 1.75, 3.93], y=y + 0.02, row_h=0.42, size=9.5, first_bold=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.CENTER, PP_ALIGN.LEFT])
text(s, 0.86, 5.66, 11.5, 0.44,
     "Target dipasang pada mekanisme, bukan pada orang: selama skor masih manual, "
     "perbaikan perilaku tidak dapat dibuktikan.",
     size=9.5, italic=True, color=GREY, spacing=1.2)
reason(s, "Enam indikator ini sudah dihitung dari data yang ada, tanpa perlu sistem baru.",
       "Setelah sistem berjalan, angka yang sama dipakai sebagai kriteria go/no-go pilot.")
foot(s, 6)


# ============================================================ 07 · 1E
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Dampaknya terasa di empat sisi, bukan hanya di laporan",
         "Analisis dampak sebelum perbaikan, memakai kerangka PQCD",
         code="1E · Analisis dampak", stage="Langkah 1")
table(s, [
    ["Aspek", "Sebelum perbaikan", "Sesudah perbaikan (target)"],
    ["Productivity", "Laporan disusun manual; leader menghabiskan waktu di rekap, bukan di tindakan",
     "Rekap otomatis; waktu leader pindah ke verifikasi dan tindakan"],
    ["Quality", "973 kasus ditutup tanpa akar masalah; kelengkapan bukti 0–28%",
     "Penutupan wajib berisi akar masalah, tindakan, dan bukti"],
    ["Cost", "Pola berulang tidak terlihat; kasus yang sama dikerjakan berulang",
     "Pola berulang terdeteksi; perbaikan diarahkan ke penyebab, bukan gejalanya"],
    ["Delivery", "Eskalasi bergantung pada ingatan; 22 kasus terlambat hingga 1.045 hari",
     "Aging dan eskalasi otomatis sejak hari pertama keterlambatan"],
], [1.55, 5.05, 4.98], y=y + 0.02, row_h=0.74, size=9.5, first_bold=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])
reason(s, "PQCD adalah empat sisi yang dipakai menilai dampak pada setiap perbaikan.",
       "Karena itu usulan ini dinilai dari empat sisi tersebut, bukan dari jumlah fitur.")
foot(s, 7)


# ============================================================ 08 · 2A
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Excel berhenti di dua tahap pertama",
         "Urutan proses yang sama berlaku di semua plant: lima tahap, satu putaran tertutup",
         code="2A · Penggambaran urutan proses", stage="Langkah 2")
stages = [
    ("1", "CAPTURE", "Meeting harian dan kasus baru tercatat", "sudah ada"),
    ("2", "DETECT", "Aging, pengulangan, lonjakan", "sudah ada"),
    ("3", "EXPLAIN", "Skor dapat ditelusuri sampai kasus", "belum ada"),
    ("4", "RECOMMEND", "Usulan tindakan dari riwayat", "belum ada"),
    ("5", "ACT & VERIFY", "PIC, tenggat, dan pengecekan ulang", "belum ada"),
]
cw, gap = 2.18, 0.20
x = 0.86
for no, name, desc, tag in stages:
    card(s, x, y + 0.04, cw, 1.62, fill=WHITE, line=RULE, radius=0.08)
    hrule(s, x, y + 0.04, cw, NAVY if tag == "sudah ada" else GOLD, 0.05)
    text(s, x + 0.14, y + 0.16, 0.30, 0.22, no, size=11, bold=True, color=GOLD)
    text(s, x + 0.46, y + 0.17, cw - 0.60, 0.22, name, size=9, bold=True, color=NAVY)
    text(s, x + 0.14, y + 0.52, cw - 0.28, 0.74, desc, size=9, color=GREY, spacing=1.2)
    text(s, x + 0.14, y + 1.30, cw - 0.28, 0.22, tag, size=8.5, color=LGREY)
    x += cw + gap
text(s, 0.86, 4.06, 11.5, 0.24,
     "YANG MEMBEDAKAN DENGAN DASBOR BIASA", size=9, bold=True, color=GOLD)
rows_list(s, 0.86, 4.38, 11.58, [
    ("Keluaran berupa tindakan", "Setiap temuan membawa pemilik dan tenggat, bukan hanya angka."),
    ("Dapat dijelaskan", "Skor dapat ditelusuri sampai item penilaian dan kasus penyebabnya."),
    ("Menutup loop", "Sistem menanyakan kembali apakah kasus yang ditutup kambuh lagi."),
], size=9.5, gap=0.20)
reason(s, "Saat ini hanya tahap capture dan detect yang berjalan; tidak ada penelusuran maupun verifikasi.",
       "Tiga tahap terakhir ditambahkan agar monitoring berhenti menjadi laporan.")
foot(s, 8)


# ============================================================ 09 · 2B
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Delapan penyebab potensial, semuanya di metode dan alat",
         "Dikumpulkan dari bukti yang tercatat, bukan dari dugaan",
         code="2B · Brainstorming penyebab potensial", stage="Langkah 2")
table(s, [
    ["No", "Penyebab potensial", "Sumber bukti"],
    ["1", "Rumus rata-rata mengabaikan sel kosong", "Ach 125% dari satu hari terisi"],
    ["2", "Skor objektif dinilai manusia", "On-time & kelengkapan = 30% bobot"],
    ["3", "Enam item diringkas menjadi satu angka", "Hanya nilai total tersimpan"],
    ["4", "Parameter mutu bernilai konstan", "0,8 ÷ 0,8 selalu terbaca 0,6"],
    ["5", "Label kasus berulang diisi manual", "849 dari 902 salah label"],
    ["6", "Penutupan tidak mensyaratkan bukti", "973 kasus tanpa akar masalah"],
    ["7", "Kasus tidak terhubung ke checklist", "Item tindakan dinilai manual"],
    ["8", "Tidak ada dimensi waktu", "Tidak ada aging, tren, atau pengingat"],
], [0.62, 6.05, 4.91], y=y + 0.02, row_h=0.345, size=9, head_size=9,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT])
reason(s, "Setiap penyebab punya bukti yang dapat dibuka kembali di file aslinya.",
       "Delapan penyebab ini disaring pada langkah berikutnya untuk dicari yang dominan.")
foot(s, 9)


# ============================================================ 10 · 2C
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Tiga penyebab terbukti lewat 5G, bukan dugaan",
         "Setiap dugaan diuji langsung di tempat kerja, lalu dibandingkan dengan standar dan teori",
         code="2C · Analisis 5G", stage="Langkah 2")
table(s, [
    ["Penyebab potensial", "Genba (aktivitas)", "Genbutsu (objek)", "Genjitsu (temuan)",
     "Gensoku (standar)", "Genri (teori)", "Kesimpulan"],
    ["Skor dinilai manusia", "Menelusuri pengisian skor harian",
     "Kolom on-time & kelengkapan", "30% bobot berasal dari isian manual",
     "Penilaian seharusnya dari data", "Data tercatat lebih andal daripada ingatan", "TERBUKTI"],
    ["Penutupan tanpa bukti", "Memeriksa kasus berstatus Close",
     "Kolom akar masalah & bukti", "973 kasus Close tanpa akar masalah",
     "Penutupan wajib bukti", "Tanpa sebab, kasus yang sama akan berulang", "TERBUKTI"],
    ["Pengulangan diisi manual", "Membandingkan label dengan riwayat",
     "Kolom status berulang", "849 dari 902 label keliru",
     "Deteksi berbasis data", "Pola hanya terlihat bila dihitung mesin", "TERBUKTI"],
], [1.95, 1.60, 1.45, 2.15, 1.50, 1.75, 1.18], y=y + 0.02, row_h=0.80, size=8.5,
    head_size=8.5, first_bold=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT,
            PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER])
reason(s, "5G memisahkan pengamatan nyata dari asumsi, sehingga kesimpulan tidak bisa dibantah dengan opini.",
       "Ketiga penyebab dinyatakan terbukti dan dibawa ke penetapan penyebab dominan.")
foot(s, 10)


# ============================================================ 11 · 2D FISHBONE
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Sebabnya menyebar di lima kategori, akarnya tetap metode",
         "Diagram sebab-akibat: dari gejala di lapangan menuju satu masalah utama ",
         code="2D · Fishbone analysis", stage="Langkah 2")
spine_y = 4.42
line(s, 1.00, spine_y, 9.60, spine_y, NAVY, 2.0)
block(s, 9.62, spine_y - 0.50, 2.82, 1.00, fill=NAVY)
text(s, 9.76, spine_y - 0.36, 2.56, 0.76,
     "Penilaian harian tidak dapat dipertanggungjawabkan", size=8, bold=True,
     color=WHITE, spacing=1.15)

up = [
    (2.30, "MANUSIA", ["Pengisian bergantung ingatan", "Tidak ada verifikasi atasan", "Beban rekap manual"]),
    (4.85, "SISTEM / ALAT", ["Excel tanpa gate penutupan", "Tidak ada jejak audit", "Tidak ada notifikasi"]),
    (7.40, "PENGUKURAN", ["Rumus abaikan sel kosong", "Ambang tanpa pembulatan", "Parameter konstan"]),
]
down = [
    (3.55, "METODE", ["Penilaian 30% manual", "Enam item jadi satu angka", "Berulang dinilai manual"]),
    (6.10, "DATA", ["Akar masalah 0–79%", "Bukti penutupan kosong", "Kategori kasus 16%"]),
]
for bx, name, causes in up:
    text(s, bx - 0.55, 2.30, 2.25, 0.22, name, size=9.5, bold=True, color=NAVY)
    cy = 2.60
    for c in causes:
        block(s, bx - 0.62, cy + 0.07, 0.06, 0.06, fill=GOLD)
        text(s, bx - 0.46, cy, 2.05, 0.22, c, size=8.5, color=GREY, spacing=1.1)
        cy += 0.28
    line(s, bx, spine_y, bx - 0.42, cy - 0.10, NAVY, 1.25)

for bx, name, causes in down:
    line(s, bx, spine_y, bx - 0.42, spine_y + 0.44, NAVY, 1.25)
    text(s, bx - 0.55, spine_y + 0.48, 2.25, 0.22, name, size=9.5, bold=True, color=NAVY)
    cy = spine_y + 0.76
    for c in causes:
        block(s, bx - 0.62, cy + 0.07, 0.06, 0.06, fill=GOLD)
        text(s, bx - 0.46, cy, 2.05, 0.22, c, size=8.5, color=GREY, spacing=1.1)
        cy += 0.28
reason(s, "Gejala yang tampak berbeda (angka, kelengkapan, keterlambatan) mengarah ke satu akar yang sama.",
       "Perbaikan tidak menyasar orang per orang, melainkan aturan penilaian dan verifikasinya.")
foot(s, 11)


# ============================================================ 12 · 3A
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Empat akar penyebab menjelaskan hampir seluruh masalah",
         "Akar penyebab beserta bukti, bobot kontribusi, dan dampaknya bila dibiarkan",
         code="3A · Daftar akar penyebab", stage="Langkah 3")
table(s, [
    ["#", "Akar penyebab", "Bukti", "Kontribusi", "Dampak bila dibiarkan"],
    ["1", "Penilaian 30% bobot masih manual", "On-time & kelengkapan diisi manusia", "35%",
     "Skor tidak konsisten antarline"],
    ["2", "Penutupan tanpa gate dan bukti", "973 kasus Close tanpa akar masalah", "30%",
     "Kasus yang sama dikerjakan berulang"],
    ["3", "Pengulangan dideteksi manual", "849 dari 902 label keliru", "20%",
     "Pola besar tidak terlihat"],
    ["4", "Tidak ada dimensi waktu", "22 kasus terlambat hingga 1.045 hari", "15%",
     "Eskalasi terlambat, masalah membesar"],
], [0.52, 3.45, 3.55, 1.20, 2.86], y=y + 0.02, row_h=0.56, size=9.5,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT])
text(s, 0.86, 4.98, 11.5, 0.24, "URUTAN PRIORITAS PENANGANAN", size=9, bold=True, color=GOLD)
rows_list(s, 0.86, 5.24, 11.58, [
    ("Pertama: hitung otomatis dan gate penutupan", "Dua akar teratas menyumbang 65% masalah."),
    ("Kedua: deteksi berulang dan dimensi waktu", "Sisanya 35%, bergantung pada data yang sudah bersih."),
], size=9.5, gap=0.10)
reason(s, "Kontribusi dihitung dari jumlah kasus yang terpengaruh tiap akar, bukan dari perkiraan.",
       "Urutan penanganan mengikuti besaran kontribusi, agar hasil cepat terlihat.")
foot(s, 12)


# ============================================================ 13 · 3B
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Dua akar teratas menyumbang 65% masalah",
         "Visualisasi kontribusi: dasar penetapan prioritas",
         code="3B · Visualisasi", stage="Langkah 3")
bars(s, [
    ("Penilaian manual", 35, NAVY),
    ("Tanpa gate penutupan", 30, NAVY),
    ("Pengulangan manual", 20, TEAL),
    ("Tanpa dimensi waktu", 15, TEAL),
], y=y + 0.18)
card(s, 0.86, 4.48, 6.90, 1.24, fill=BG, line=RULE, radius=0.08)
block(s, 1.02, 4.66, 0.05, 0.88, fill=GOLD, radius=0.5)
text(s, 1.20, 4.58, 6.0, 0.20, "CARA MEMBACA", size=8.5, bold=True, color=GOLD)
text(s, 1.20, 4.80, 6.34, 0.78,
     "Dua batang pertama berada di mekanisme penilaian dan penutupan kasus — keduanya dapat "
     "diperbaiki tanpa menambah orang. Dua batang berikutnya baru bermakna setelah data bersih.",
     size=9.5, color=INK, spacing=1.25)
img_slot(s, 8.05, 4.48, 4.39, 1.24, "Grafik pendukung", "tempel pareto atau tren di sini")
reason(s, "Bila keempat akar dikerjakan bersamaan, hasilnya sulit dibedakan mana yang bekerja.",
       "Pilot mengerjakan dua akar teratas lebih dulu, dua sisanya menyusul pada fase berikutnya.")
foot(s, 13)


# ============================================================ 14 · 4A
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Dua solusi menang: hitung otomatis dan gate penutupan",
         "Setiap alternatif dinilai dengan ukuran yang sama: dampak, biaya, risiko, dan kompleksitas",
         code="4A · Analisis alternatif solusi", stage="Langkah 4")
table(s, [
    ["No", "Alternatif solusi", "Dampak 40%", "Biaya 10%", "Risiko 30%", "Kompleksitas 20%", "Skor", "Prioritas"],
    ["1", "Ganti penilaian manual dengan perhitungan sistem", "5", "4", "4", "4", "4,4", "2"],
    ["2", "Gate penutupan: akar masalah + tindakan + bukti + persetujuan", "5", "5", "4", "5", "4,7", "1"],
    ["3", "Deteksi berulang otomatis berbasis riwayat kasus", "4", "5", "4", "3", "3,9", "3"],
    ["4", "Penegasan disiplin tanpa mengubah sistem", "2", "4", "3", "5", "3,1", "—"],
], [0.52, 4.55, 0.95, 0.95, 0.95, 1.30, 0.80, 1.06], y=y + 0.28, row_h=0.46, size=9,
    head_size=8.5,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT] + [PP_ALIGN.CENTER] * 6)
text(s, 0.86, y - 0.02, 11.5, 0.22,
     "SKALA 1–5 · SKOR = DAMPAK×0,4 + BIAYA×0,1 + RISIKO×0,3 + KOMPLEKSITAS×0,2",
     size=8.5, bold=True, color=GOLD)
card(s, 0.86, 4.98, 7.10, 1.20, fill=BG, line=RULE, radius=0.08)
block(s, 1.02, 5.12, 0.05, 0.92, fill=GOLD, radius=0.5)
text(s, 1.20, 5.08, 6.5, 0.20, "CATATAN PEMILIHAN", size=8.5, bold=True, color=GOLD)
text(s, 1.20, 5.30, 6.50, 0.80,
     "Solusi nomor 4 sengaja dicantumkan sebagai pembanding: menambah penekanan pada orang "
     "tidak menyelesaikan sebabnya. Skor dihitung dengan bobot yang sama untuk semua usulan.",
     size=9.5, color=INK, spacing=1.22)
img_slot(s, 8.16, 4.98, 4.28, 1.20, "Matriks scoring", "tempel hasil perhitungan tim")
reason(s, "Matriks ini memaksa setiap usulan dibandingkan pada ukuran yang sama, bukan pada selera.",
       "Dua solusi teratas dikerjakan lebih dulu; keduanya saling menguatkan.")
foot(s, 14)


# ============================================================ 15 · 4B WORKPLAN
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Rencana kerja: tiga paket, tiga pemilik, satu jadwal",
         "Setiap paket ditulis lengkap: apa, mengapa, bagaimana, siapa, kapan, di mana, berapa",
         code="4B · Workplan 5W1H", stage="Langkah 4")
table(s, [
    ["What (rencana)", "Why (ukuran berhasil)", "How (uraian)", "Who", "When", "Where", "How much"],
    ["Hitung skor otomatis", "0% skor dinilai manual", "Item dinilai dari data; skor disimpan per item",
     "Tim DMS + IT", "Pekan 3–5", "Semua plant", "Internal"],
    ["Gate penutupan kasus", "0 kasus tanpa akar masalah", "Form menolak simpan tanpa sebab, tindakan, bukti",
     "Pemilik proses", "Pekan 3–6", "Semua plant", "Internal"],
    ["Deteksi berulang", "100% pola ≥3× terdeteksi", "Aturan otomatis atas riwayat kasus",
     "Tim DMS", "Pekan 6–7", "Semua plant", "Internal"],
], [2.30, 2.10, 3.35, 1.40, 0.95, 1.00, 0.88], y=y + 0.02, row_h=0.80, size=8.5,
    head_size=8.5, first_bold=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT,
            PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.CENTER])
text(s, 0.86, 5.58, 11.58, 0.44,
     "Ketiga paket dijalankan berurutan: perhitungan skor menjadi dasar gate penutupan, "
     "dan deteksi berulang baru berjalan setelah data penutupan lengkap.",
     size=9.5, italic=True, color=GREY, spacing=1.22)
reason(s, "Paket tanpa pemilik dan tanggal tidak akan berjalan, sebaik apa pun idenya.",
       "Ketiga paket memakai pemilik proses yang sudah ada; tidak perlu organisasi baru.")
foot(s, 15)


# ============================================================ 16 · 4C TIMELINE
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Delapan pekan: fondasi dulu, tampilan paling akhir",
         "Urutan fase mengikuti kesiapan data, bukan kemudahan membuat tampilan",
         code="4C · Timeline perbaikan", stage="Langkah 4")
phases = [
    ("0", "Fondasi", "2 pekan", "Master data bersih, aturan penilaian, hak akses"),
    ("1", "Capture", "3 pekan", "Form meeting harian, form kasus, persetujuan"),
    ("2", "Measure", "2 pekan", "Perhitungan skor dan dasbor tingkat line"),
    ("3", "Insight", "2 pekan", "Delapan aturan deteksi pertama"),
    ("4", "Display", "1 pekan", "Tampilan lantai produksi satu area"),
    ("5", "Analitik", "2 pekan", "Dasbor level plant dan ekspor"),
]
cw, gap, x = 1.86, 0.14, 0.86
for i, (no, name, dur, desc) in enumerate(phases):
    card(s, x, y + 0.10, cw, 2.16, fill=WHITE, line=RULE, radius=0.07)
    hrule(s, x, y + 0.10, cw, GOLD, 0.05)
    text(s, x + 0.12, y + 0.22, 0.30, 0.22, no, size=11, bold=True, color=GOLD)
    text(s, x + 0.12, y + 0.50, cw - 0.24, 0.22, name.upper(), size=9, bold=True, color=NAVY)
    text(s, x + 0.12, y + 0.74, cw - 0.24, 0.20, dur, size=8, color=GOLD)
    text(s, x + 0.12, y + 0.98, cw - 0.24, 1.12, desc, size=8.5, color=GREY, spacing=1.2)
    x += cw + gap
text(s, 0.86, 4.58, 11.5, 0.24, "ATURAN URUTAN", size=9, bold=True, color=GOLD)
rows_list(s, 0.86, 4.88, 11.58, [
    ("Tidak ada layar sebelum aturan penilaian disepakati", "Tampilan tanpa aturan hanya memindahkan selisih hitung."),
    ("Tidak ada dasbor sebelum data wajib terisi", "Dasbor di atas data bolong menghasilkan kesimpulan keliru."),
], size=9.5, gap=0.10)
reason(s, "Sebagian besar proyek sejenis gagal karena memulai dari tampilan, bukan dari definisi angka.",
       "Fase 0 dan 1 dikunci lebih dulu; tampilan dikerjakan setelah angkanya dapat dipercaya.")
foot(s, 16)


# ============================================================ 17 · 5A TAMPILAN (kosong)
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Tampilan mengikuti peran, bukan sebaliknya",
         "Kerangka empat kanal di bawah ini masih kosong — desain antarmuka dibuat terpisah",
         code="5A · Pelaksanaan — rancangan tampilan", stage="Langkah 5")
cw, gap, x = 2.80, 0.18, 0.86
for label, who, desc in [
    ("Form harian", "Leader & DH", "Satu layar, target di bawah 5 menit"),
    ("Dasbor L1–L3", "Supervisor, admin", "Tiga tingkat dengan audiens berbeda"),
    ("Tampilan lantai", "Lantai produksi", "Tanpa interaksi, rotasi otomatis"),
    ("Halaman admin", "Admin plant & group", "Persetujuan, konfigurasi, audit"),
]:
    img_slot(s, x, y + 0.02, cw, 1.94, label, "mockup atau foto layar")
    text(s, x, 4.24, cw, 0.22, who, size=9.5, bold=True, color=NAVY)
    text(s, x, 4.48, cw, 0.44, desc, size=9, color=GREY, spacing=1.2)
    x += cw + gap
text(s, 0.86, 5.10, 11.5, 0.44,
     "Catatan: rancangan aplikasi (form, dasbor, TV) sengaja dikosongkan. "
     "Pembahasan hari ini difokuskan pada logika penilaian, alur kerja, dan mesin insight.",
     size=9.5, color=GREY, spacing=1.25)
reason(s, "Desain antarmuka perlu dibahas dengan pengguna lapangan sebelum digambar.",
       "Deck ini menetapkan struktur kanal dan batasannya, bukan tampilan visualnya.")
foot(s, 17)


# ============================================================ 18 · 5B ADMIN (kosong)
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Angka tidak boleh bisa diubah diam-diam",
         "Tiga hal yang dijaga pada halaman admin — gambarnya menyusul",
         code="5B · Pelaksanaan — kontrol admin", stage="Langkah 5")
img_slot(s, 0.86, y + 0.02, 7.30, 2.66, "Rancangan halaman admin", "mockup atau foto layar")
rows_list(s, 8.45, y + 0.06, 3.99, [
    ("Persetujuan", "Penutupan kasus disetujui pihak lain, bukan pengisi."),
    ("Konfigurasi", "Bobot, ambang skor, target, dan kalender libur bertanggal berlaku."),
    ("Audit", "Setiap perubahan tercatat: siapa, kapan, sebelum–sesudah."),
], size=9.5, gap=0.20)
card(s, 0.86, y + 2.84, 11.58, 0.66, fill=BG, line=RULE, radius=0.10)
block(s, 1.02, y + 2.96, 0.05, 0.42, fill=RED, radius=0.5)
text(s, 1.20, y + 2.94, 11.0, 0.48,
     "Admin tidak dapat mengubah skor periode yang sudah dikunci; koreksi hanya melalui "
     "penyesuaian beralasan yang tercatat.", size=9, color=INK, spacing=1.2)
reason(s, "Mengubah bobot hari ini tanpa versioning berarti mengubah skor periode yang sudah dilaporkan.",
       "Konfigurasi memakai tanggal berlaku dan kunci periode.")
foot(s, 18)


# ============================================================ 19 · 6A
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Capaian diukur pekanan dengan enam indikator yang sama",
         "Tabel monitoring dipakai seragam, sehingga hasil antarplant dapat dibandingkan",
         code="6A · Monitoring capaian terhadap target", stage="Langkah 6")
table(s, [
    ["Indikator", "Cara ukur", "Frekuensi", "Ambang eskalasi"],
    ["Kepatuhan mengisi form", "Hari wajib terisi ÷ hari wajib", "Pekanan", "< 90% → plant head"],
    ["Kelengkapan akar masalah", "Kasus dengan sebab ÷ kasus ditutup", "Pekanan", "< 95% → pemilik proses"],
    ["Kasus terlambat", "Jumlah due date lewat", "Harian", "Naik 2 pekan → group"],
    ["Pola berulang ditangani", "Pola ≥3× yang punya tindakan", "Bulanan", "< 100% → admin"],
    ["Insight ditindaklanjuti", "Temuan bertindak ÷ temuan tampil", "Pekanan", "< 70% → supervisor"],
    ["Skor dinilai manual", "Item manual ÷ seluruh item", "Bulanan", "> 0% → dianggap belum jadi"],
], [3.30, 3.90, 1.55, 2.83], y=y + 0.02, row_h=0.44, size=9.5, first_bold=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT])
text(s, 0.86, 5.66, 11.5, 0.48,
     "Ambang eskalasi ditulis sejak awal agar kenaikan masalah tidak bergantung pada siapa "
     "yang memeriksa laporan.", size=9, italic=True, color=GREY, spacing=1.2)
reason(s, "Tanpa ambang yang disepakati, setiap plant akan menilai capaiannya dengan ukurannya sendiri.",
       "Pekan pertama pilot dipakai mengukur dasar, pekan berikutnya menilai perbaikan.")
foot(s, 19)


# ============================================================ 20 · 6B
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Evaluasi dinilai dari empat dampak, bukan dari aplikasi selesai",
         "Perbandingan sebelum dan sesudah delapan pekan, memakai kerangka yang sama dengan poin 1E",
         code="6B · Evaluasi hasil", stage="Langkah 6")
table(s, [
    ["Aspek", "Sebelum", "Sesudah (target)", "Kriteria lanjut"],
    ["Productivity", "Rekap manual, berjam-jam", "Rekap otomatis ≤ 5 menit", "Leader memakai data, bukan menyusunnya"],
    ["Quality", "0–28% kelengkapan bukti", "≥ 95% kasus berakar masalah", "Penutupan dapat diaudit"],
    ["Cost", "Pola berulang tidak terlihat", "Pola ≥3× punya tindakan", "Perbaikan mengarah ke penyebab"],
    ["Delivery", "Keterlambatan 1.045 hari", "Tidak ada kasus lewat tenggat tanpa eskalasi", "Eskalasi berjalan otomatis"],
], [1.55, 3.65, 3.35, 3.03], y=y + 0.02, row_h=0.56, size=9.5, first_bold=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])
card(s, 0.86, 5.28, 11.58, 0.86, fill=BG, line=RULE, radius=0.09)
block(s, 0.86, 5.28, 0.045, 0.86, fill=GREEN)
text(s, 1.08, 5.38, 11.0, 0.20, "KRITERIA GO / NO-GO", size=8, bold=True, color=GREEN)
text(s, 1.08, 5.60, 11.1, 0.44,
     "Lanjut ke plant lain bila empat dari enam indikator tercapai; bila tidak, pilot diperpanjang "
     "dua pekan sebelum diputuskan.", size=9.5, color=INK, spacing=1.2)
reason(s, "Evaluasi yang hanya melihat aplikasi selesai tidak menjawab apakah masalahnya berkurang.",
       "Keputusan lanjut atau berhenti memakai ambang yang sudah disepakati di awal.")
foot(s, 20)


# ============================================================ 21 · 7
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Hasil bertahan karena standar, bukan karena pengawasan",
         "Empat standar yang cukup disusun sekali dan dipakai semua plant",
         code="7 · Standarisasi", stage="Langkah 7")
table(s, [
    ["Standar", "Isi", "Bentuk dokumen"],
    ["7A · Hasil", "Rumus penilaian, ambang band skor, target per parameter", "Satu lembar acuan penilaian"],
    ["7B · Proses", "Gate penutupan, hari wajib, kalender libur, alur persetujuan", "SOP dan WI monitoring harian"],
    ["7C · Sistem", "Template inti, tambahan KPI per plant, konfigurasi bertanggal", "Dokumen konfigurasi berversi"],
    ["7D · Audit", "Jejak perubahan, kunci periode, koreksi beralasan", "Prosedur audit dan contoh laporan"],
], [1.85, 5.55, 4.18], y=y + 0.02, row_h=0.54, size=9.5, first_bold=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])
text(s, 0.86, 4.74, 11.5, 0.22, "YANG BERUBAH SETELAH STANDAR BERLAKU", size=9, bold=True, color=GOLD)
rows_list(s, 0.86, 5.04, 11.58, [
    ("Tidak ada lagi versi file per orang", "Satu acuan, satu versi, satu tanggal berlaku."),
    ("Masalah lama tidak kembali", "Kasus yang kambuh otomatis muncul sebagai temuan."),
], size=9.5, gap=0.10)
reason(s, "Perbaikan tanpa standar akan kembali ke kebiasaan lama begitu perhatian berkurang.",
       "Empat standar ini yang membuat hasil tidak bergantung pada satu orang.")
foot(s, 21)


# ============================================================ 22 · 8
s = prs.slides.add_slide(L_CONTENT)
clean(s)
y = head(s, "Setelah satu plant stabil, kerangka yang sama dipakai plant lain",
         "Tema berikutnya dan urutan penyebaran ke plant lain",
         code="8 · Tema berikutnya", stage="Langkah 8")
card(s, 0.86, y + 0.02, 11.58, 1.00, fill=BG, line=RULE, radius=0.09)
block(s, 1.02, y + 0.16, 0.05, 0.72, fill=GOLD, radius=0.5)
text(s, 1.20, y + 0.12, 11.0, 0.20, "TEMA BERIKUTNYA", size=8.5, bold=True, color=GOLD)
text(s, 1.20, y + 0.34, 10.9, 0.56,
     "Menyebarkan kerangka penilaian yang sama ke seluruh plant, dengan tambahan KPI khas "
     "masing-masing plant.", size=11, color=INK, spacing=1.2)
table(s, [
    ["Urutan", "Plant", "Yang disiapkan", "Perkiraan"],
    ["1", "Snack", "Pilot penuh delapan pekan", "Pekan 1–8"],
    ["2", "Exist Plant", "Salin template, sesuaikan KPI dan kalender", "Pekan 9–12"],
    ["3", "Dairy", "KPI proses dan mutu khas dairy", "Pekan 13–16"],
    ["4", "New Plant", "Ikut sejak awal operasi", "Saat plant berjalan"],
], [0.70, 1.90, 4.35, 2.00], y=y + 1.18, row_h=0.42, size=9.5,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])
img_slot(s, 9.30, y + 1.18, 3.14, 2.10, "Peta sebaran plant", "sisipkan foto atau diagram")
reason(s, "KPI khas plant berbeda, tetapi cara menilai, menutup kasus, dan membaca insight tetap sama.",
       "Penyebaran dilakukan setelah satu plant terbukti, agar kesalahannya tidak berlipat.")
foot(s, 22)


# ============================================================ 23 · PENUTUP
s = prs.slides.add_slide(L_CONTENT)
clean(s)
block(s, 0, 0, 13.333, 7.5, fill=WHITE)
block(s, 0, 0, 13.333, 0.82, fill=NAVY_D)
s.shapes.add_picture(LOGO, Inches(0.46), Inches(0.15), height=Inches(0.50))
text(s, 3.05, 0.30, 6.6, 0.22, "DAILY MONITORING SYSTEM  ·  SEMUA PLANT",
     size=8.5, bold=True, color=GOLD)
text(s, 9.40, 0.30, 3.20, 0.22, "PENILAIAN & INSIGHT HARIAN", size=8.5,
     color=RGBColor(0x8E, 0x9C, 0xB8), align=PP_ALIGN.RIGHT)

text(s, 0.86, 1.84, 11.0, 0.24, "PENUTUP", size=8.5, bold=True, color=GOLD)
text(s, 0.86, 2.12, 11.4, 0.62, "Tiga keputusan menunggu arahan", size=30, bold=True, color=NAVY)
hrule(s, 0.86, 2.92, 11.58, GOLD, 0.022)
table(s, [
    ["Keputusan", "Pilihan yang tersedia"],
    ["Kalender hari libur", "Master tahunan diisi sekali, atau input per tanggal"],
    ["Status N/A pada KPI", "Item tidak relevan keluar dari penyebut, atau dihitung nol"],
    ["Data historis", "5.817 kasus dibawa dengan penanda lama, atau mulai bersih"],
], [3.05, 5.05], y=3.14, row_h=0.52, size=9.5, first_bold=True)
text(s, 0.86, 5.42, 11.58, 0.50,
     "Dua hal menyusul setelah ketiganya: akun untuk fungsi Teknik (mayoritas kasus milik mereka) "
     "dan kebijakan retensi data.", size=9, italic=True, color=GREY, spacing=1.2)
text(s, 0.86, 5.92, 11.0, 0.32, "Terima kasih.", size=13.5, bold=True, color=NAVY)
reason(s, "Ketiganya kebijakan, bukan angka: tidak dapat disimpulkan dari workbook mana pun.",
       "Arahan pada sesi ini mengunci lingkup pilot dan tanggal mulai.")
text(s, 11.85, 7.06, 0.60, 0.22, "23", size=8, color=LGREY, align=PP_ALIGN.RIGHT)

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides.__iter__.__self__._sldIdLst))
