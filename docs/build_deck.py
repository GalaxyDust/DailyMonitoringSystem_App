#!/usr/bin/env python3
"""
Deck DMS memakai template_master.pptx (versi terbaru):
  slide 1 template -> cover (panel putih judul)
  slide 2 template -> pola semua halaman isi (judul + area konten)
  slide 3 template -> halaman penutup

Jalankan: python3 docs/build_deck.py
Hasil  : docs/DMS_Digitalisasi_v1.pptx
"""
import copy
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

SRC = "template_master.pptx"
OUT = "docs/DMS_Digitalisasi_v1.pptx"

NAVY = RGBColor(0x1F, 0x33, 0x64)      # biru tua logo/tema
TEAL = RGBColor(0x2E, 0x86, 0x8C)
GOLD = RGBColor(0xC8, 0xA5, 0x2B)
INK = RGBColor(0x22, 0x28, 0x33)
GREY = RGBColor(0x5C, 0x64, 0x72)
LGREY = RGBColor(0x8B, 0x93, 0xA1)
RULE = RGBColor(0xD5, 0xDA, 0xE3)
SOFT = RGBColor(0xF4, 0xF6, 0xFA)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
RED = RGBColor(0xB0, 0x2F, 0x2F)

prs = Presentation(SRC)
COVER_T = prs.slides[0]
BODY_T = prs.slides[1]
CLOSE_T = prs.slides[2]
BODY_L, CLOSE_L, COVER_L = BODY_T.slide_layout, CLOSE_T.slide_layout, COVER_T.slide_layout

sldIdLst = prs.slides._sldIdLst
for sid in list(sldIdLst):
    rId = sid.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")
    prs.part.drop_rel(rId)
    sldIdLst.remove(sid)


# ---------------------------------------------------------------- primitif
def txt(slide, x, y, w, h, lines, size=11, color=INK, bold=False, align=PP_ALIGN.LEFT,
        spacing=1.15, anchor=MSO_ANCHOR.TOP, italic=False):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
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
    return box


def box(slide, x, y, w, h, fill=SOFT, line=RULE, lw=0.9, radius=0.06):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE if radius else MSO_SHAPE.RECTANGLE,
                               Inches(x), Inches(y), Inches(w), Inches(h))
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
    if radius:
        s.adjustments[0] = radius
    return s


def hline(slide, x, y, w, color=RULE, h=0.015):
    box(slide, x, y, w, h, fill=color, line=None, radius=None)


def table(slide, data, widths, x, y, row_h=0.34, head_h=0.32, fs=9.5, head_fs=9.5,
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
    box(slide, x + w / 2 - 0.15, y + h / 2 - 0.34, 0.30, 0.30, fill=WHITE,
        line=RGBColor(0xBE, 0xC7, 0xD6), radius=0.2)
    txt(slide, x + w / 2 - 0.15, y + h / 2 - 0.30, 0.30, 0.24, [("+", 11, True, LGREY)],
        align=PP_ALIGN.CENTER)
    txt(slide, x + 0.10, y + h / 2 + 0.02, w - 0.20, 0.24,
        [(caption.upper(), 8.5, True, LGREY)], align=PP_ALIGN.CENTER)
    txt(slide, x + 0.10, y + h / 2 + 0.22, w - 0.20, 0.44,
        [(note, 7.5, None, RGBColor(0xA9, 0xB2, 0xC0))], align=PP_ALIGN.CENTER, spacing=1.08)


def page(title, kicker, no, note=None):
    """Halaman isi memakai layout slide 2 template."""
    s = prs.slides.add_slide(BODY_L)
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx not in (0, 1):
            ph._element.getparent().remove(ph._element)
    title_ph = s.shapes.title
    if title_ph is not None:
        title_ph.left, title_ph.top = Inches(2.05), Inches(0.24)
        title_ph.width, title_ph.height = Inches(10.10), Inches(0.62)
        tf = title_ph.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_left = tf.margin_right = 0
        tf.margin_top = tf.margin_bottom = 0
        tf.text = title
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        for r in p.runs:
            r.font.size = Pt(23)
            r.font.bold = True
            r.font.name = "Calibri"
            r.font.color.rgb = NAVY
    for ph in list(s.placeholders):
        if ph.placeholder_format.idx == 1 and ph != title_ph:
            ph._element.getparent().remove(ph._element)

    hline(s, 2.05, 0.92, 2.20, GOLD, 0.045)
    txt(s, 4.42, 0.80, 6.0, 0.26, [(kicker.upper(), 9, True, GOLD)])
    txt(s, 12.32, 0.28, 0.42, 0.26, [(str(no), 11, True, LGREY)], align=PP_ALIGN.RIGHT)
    if note:
        txt(s, 0.62, 6.96, 8.4, 0.26, [(note, 8, None, LGREY)])
    return s


# ================================================================ 1 · COVER
cover = prs.slides.add_slide(COVER_L)
for sh in list(cover.shapes):                    # panel putih layout dibiarkan (dari layout)
    if sh.is_placeholder:
        sh._element.getparent().remove(sh._element)

# dua panel FAFAFA seperti pada slide 1 template, menutup poster di belakangnya
panel = box(cover, 5.00, 0.25, 5.75, 3.11, fill=RGBColor(0xFA, 0xFA, 0xFA), line=None, radius=0.03)
box(cover, 10.50, 1.64, 2.75, 1.92, fill=RGBColor(0xFA, 0xFA, 0xFA), line=None, radius=0.03)

txt(cover, 5.26, 0.52, 5.10, 0.26, [("OPERATIONAL REVIEW  ·  GOOD IN ACTIONS", 9, True, GOLD)])
hline(cover, 5.26, 0.80, 1.30, GOLD, 0.04)
txt(cover, 5.26, 0.94, 4.95, 0.98,
    [("Digitalisasi", 25, True, NAVY),
     ("Daily Monitoring System", 25, True, NAVY)], spacing=1.06)
txt(cover, 5.26, 1.98, 4.92, 0.30,
    [("Dari workbook Excel menjadi penilaian yang dapat diaudit", 10.5, None, TEAL)], spacing=1.15)
txt(cover, 5.26, 2.32, 4.92, 0.26,
    [("Berlaku untuk Plant Snack, Dairy, Exist Plant, dan New Plant", 8.5, None, GREY)])
txt(cover, 5.26, 2.66, 4.92, 0.26,
    [("Dasar angka: 5.817 kasus pada workbook DMS 2023–2026", 8.5, True, NAVY)])

txt(cover, 10.68, 1.74, 2.42, 1.72,
    [("OKTOBER", 8.5, True, GOLD),
     ("2026", 26, True, NAVY),
     ("Tim Daily Monitoring System", 8, None, GREY),
     ("Group Manufacturing", 8, None, GREY)], spacing=1.12, anchor=MSO_ANCHOR.MIDDLE)


# ================================================================ 2 · KONDISI
s = page("Penilaian hari ini tidak dapat diaudit", "Bagian 1 · kondisi", 2,
         "Sumber: workbook DMS · Resume SHE, Resume QC, Resume Produksi")
kpis = [("5.817", "kasus diperiksa", "3 sheet resume", NAVY),
        ("973", "tutup tanpa sebab", "16,7% dari total", RED),
        ("94%", "label berulang salah", "849 dari 902", RED),
        ("22", "kasus lewat tenggat", "tertua 1.045 hari", GOLD)]
x = 0.62
for val, lab, note_, col in kpis:
    box(s, x, 1.28, 2.95, 0.96, fill=SOFT, line=RULE, radius=0.07)
    box(s, x + 0.12, 1.40, 0.05, 0.72, fill=col, radius=0.5)
    txt(s, x + 0.28, 1.36, 2.50, 0.44, [(val, 22, True, col)])
    txt(s, x + 0.28, 1.78, 2.50, 0.22, [(lab, 9.5, True, INK)])
    txt(s, x + 0.28, 1.98, 2.50, 0.20, [(note_, 8, None, GREY)])
    x += 3.04

table(s, [
    ["Sheet", "Kasus", "Akar masalah", "Due date", "Bukti", "Catatan"],
    ["Resume SHE", "1.185", "0%", "0%", "0%", "dua tabel ditumpuk"],
    ["Resume QC", "1.520", "79%", "100%", "–", "320 tutup tanpa sebab"],
    ["Resume Produksi", "3.112", "78%", "99%", "–", "653 tutup tanpa sebab"],
    ["IIAA Snack", "120", "duplikat", "–", "–", "tidak dipakai"],
], [2.40, 0.95, 1.45, 1.20, 0.85, 1.95], 0.62, 2.46, row_h=0.36, fs=9.5,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.RIGHT, PP_ALIGN.CENTER, PP_ALIGN.CENTER,
            PP_ALIGN.CENTER, PP_ALIGN.LEFT], bold_first=True)

txt(s, 1.05, 4.34, 7.9, 0.24, [("AKIBAT LANGSUNG PADA PENILAIAN", 9, True, GOLD)])
txt(s, 1.05, 4.62, 7.90, 1.70,
    [("• Status Close diisi karena kolomnya berisi, bukan karena masalahnya selesai.", 9.5, None, INK),
     ("• Prioritas High muncul pada hampir 100% kasus, sehingga tidak lagi membedakan.", 9.5, None, INK),
     ("• 99,7% PIC kasus adalah fungsi Teknik, padahal skornya dinilai ke leader line.", 9.5, None, INK),
     ("• 184 pola berulang (≥3×) mencakup 816 kasus atau 26,2% seluruh kasus.", 9.5, None, INK)],
    spacing=1.45)

img_slot(s, 9.72, 2.46, 2.98, 2.50, "Screenshot Resume QC",
         "tampilkan header kolom + blok kosong root cause")
txt(s, 9.72, 5.06, 2.98, 0.70,
    [("Angka diambil langsung dari ketiga sheet resume; kolom kosong dihitung "
      "sebagai tidak terisi.", 8, None, GREY)], spacing=1.2)


# ================================================================ 3 · CACAT LOGIKA
s = page("Sembilan cacat logika pada rumus penilaian", "Bagian 1 · logika", 3,
         "Sumber: sheet Template Penilaian dan Sheet1")
table(s, [
    ["#", "Cacat", "Bukti di workbook", "Pengganti di aplikasi"],
    ["1", "AVERAGEIF mengabaikan sel kosong", "1 hari terisi → Ach 125% → skor 5", "Penyebut = hari kerja − hari libur"],
    ["2", "Skor objektif dinilai manusia", "on-time & kelengkapan = 30 bobot", "Dihitung sistem"],
    ["3", "Enam item diringkas jadi satu", "hanya nilai total tersimpan", "Skor disimpan per item"],
    ["4", "Healthy Check bernilai tetap", "0,8 ÷ 0,8 selalu 0,6", "Parameter dapat diubah Admin"],
    ["5", "Berulang diisi manual", "849 dari 902 label keliru", "Deteksi otomatis"],
    ["6", "Penutupan tanpa bukti", "973 kasus", "Gate: sebab + tindakan + bukti"],
    ["7", "Kasus tidak terhubung checklist", "item PICA dinilai manual", "Skor item 5–6 dari data kasus"],
    ["8", "Tidak ada dimensi waktu", "tidak ada aging / tren", "Aging, tren, pengingat"],
    ["9", "Ambang tanpa pembulatan", "0,88 ÷ 0,80 = 1,0999 → skor 3", "Bandingkan 2 desimal → skor 4"],
], [0.42, 2.80, 2.90, 2.86], 0.62, 1.28, row_h=0.335, fs=9,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])

txt(s, 1.05, 4.78, 7.85, 0.24, [("DUA CONTOH YANG DAPAT DIHITUNG ULANG", 9, True, GOLD)])
txt(s, 1.05, 5.08, 7.80, 1.50,
    [("Skenario A · 5 hari wajib, 1 hari terisi: Excel memberi ACh 125% dan skor 5; "
      "dengan penyebut hari kerja hasilnya 20% dan skor 1.", 9.5, None, INK),
     ("Skenario B · 0,88 ÷ 0,80 = 1,0999: Excel membaca 109% dan memberi skor 3; "
      "dengan pembulatan dua desimal menjadi 110% dan skor 4.", 9.5, None, INK),
     ("Keduanya adalah sumber selisih hasil antara workbook dan aplikasi.", 9.5, True, NAVY)],
    spacing=1.35)

img_slot(s, 10.02, 1.28, 2.68, 1.95, "Screenshot Template Penilaian",
         "sorot formula AVERAGEIF dan band skor")


# ================================================================ 4 · RUMUS FINAL
s = page("Rumus final: tiga koreksi, satu arti baru", "Bagian 2 · rumus", 4,
         "Bobot dan band mengikuti workbook; hanya penyebut dan pembulatan yang diubah")
table(s, [
    ["Komponen", "Rumus / nilai", "Keterangan"],
    ["Nilai harian", "Σ (skor item ÷ 10 × bobot) ÷ 100", "bobot 10/20/10/20/20/20 = 100"],
    ["Ach KPI", "V ÷ (V + O)", "harian bersifat biner Valid / Open"],
    ["Ach checklist", "Σ nilai harian ÷ (hari kerja × 0,8)", "target 0,8 per hari"],
    ["Band skor", "≥120% = 5 · ≥110% = 4 · ≥100% = 3 · ≥90% = 2 · <90% = 1", "bandingkan 2 desimal"],
    ["DMS Index", "0,4 × KPI + 0,4 × checklist + 0,2 × healthy", "target 3,00 dari maksimum 5"],
], [1.45, 4.10, 3.30], 0.62, 1.28, row_h=0.44, fs=9.5, bold_first=True)

txt(s, 0.62, 4.02, 8.3, 0.24, [("TIGA KOREKSI DAN DAMPAKNYA", 9, True, GOLD)])
table(s, [
    ["Koreksi", "Sebelum", "Sesudah"],
    ["Penyebut memakai hari kerja", "1 hari isi = Ach 125%", "1 dari 5 hari = Ach 20%"],
    ["Ambang dibandingkan 2 desimal", "1,0999 → skor 3", "110% → skor 4"],
    ["Healthy Check jadi parameter", "tetap 0,8", "dapat diubah Admin, bertanggal"],
], [3.35, 2.45, 2.35], 0.62, 4.36, row_h=0.33, fs=9,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.LEFT])

img_slot(s, 10.02, 1.28, 2.68, 2.10, "Screenshot Sheet1",
         "sorot kolom ISO week sebagai dasar pekan")
txt(s, 10.02, 3.56, 2.68, 1.10,
    [("Pekan memakai ISO week. Hari wajib Senin–Jumat dikurangi hari libur, "
      "sehingga jumlah hari penilaian sama untuk semua line.", 8, None, GREY)],
    spacing=1.2)

txt(s, 0.62, 5.82, 9.40, 0.24, [("AKIBATNYA PADA PENILAIAN KPI", 9, True, GOLD)])
imp = [("Skor lebih jujur",
        "SHE yang kini 0% root cause menjadi terukur; 973 kasus Close tidak lagi dihitung selesai."),
       ("Tidak bisa diakali",
        "On-time dan kelengkapan dinilai sistem, bukan skor manual yang bisa diisi 30 poin."),
       ("Bisa diaudit",
        "Perubahan skor tercatat siapa dan kapan; periode yang sudah dilaporkan dikunci.")]
x = 0.62
for head, body in imp:
    box(s, x, 6.08, 3.00, 0.72, fill=SOFT, line=RULE, radius=0.05)
    txt(s, x + 0.14, 6.16, 2.72, 0.20, [(head, 8.5, True, NAVY)])
    txt(s, x + 0.14, 6.38, 2.72, 0.38, [(body, 7.5, None, GREY)], spacing=1.14)
    x += 3.16


# ================================================================ 5 · INSIGHT
s = page("Mesin insight: 12 aturan yang siap dipakai", "Bagian 3 · insight", 5,
         "Setiap temuan membawa bukti, sebab, dampak, rekomendasi, dan pemilik")
table(s, [
    ["Kode", "Pemicu", "Contoh keluaran", "Kanal"],
    ["I-01", "Hari kerja tanpa meeting", "Line tidak DMS 3 hari berturut", "L1 · TV"],
    ["I-02", "Tenggat lewat, status terbuka", "22 kasus; tertua 1.045 hari", "TV · L1"],
    ["I-03", "Signature sama ≥3× per 90 hari", "M03 BCAT 15× di Pilus L1", "TV · L2"],
    ["I-04", "Berulang dengan sebab identik", "Correction sama 4× → Preventive", "L2"],
    ["I-05", "Tutup, tetapi OPL/PM/AM/CRMO = O", "88–98% kasus tidak distandarkan", "L2 · L3"],
    ["I-06", "Tutup tanpa sebab atau bukti", "973 kasus", "Admin"],
    ["I-07", "Prioritas High di atas 80%", "prioritas tidak membedakan", "Admin"],
    ["I-08", "Ach dalam 1% di bawah band", "rawan salah hitung", "Admin"],
    ["I-09", "Tiga periode menurun", "checklist turun 4% per pekan", "L2 · L3"],
    ["I-10", "Satu line atau mesin di atas 20%", "Pilus L1 = 90% kasus", "L3"],
    ["I-11", "Downtime besar dan sering", "MHM 26,8% · BCAT 14,1%", "L2"],
    ["I-12", "PICA lemah, kasus baru naik", "prediksi lonjakan pekan depan", "L3"],
], [0.62, 2.95, 4.03, 1.16], 0.62, 1.26, row_h=0.355, fs=8.5,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER])

txt(s, 0.62, 5.90, 8.2, 0.90,
    [("Peringkat = dampak × volume × kebaruan × (controllable ? 1 : 0,5).", 9, None, INK),
     ("Maksimal tiga kartu tampil di layar lantai; sisanya di dasbor supervisor dan admin.",
      9, None, GREY)], spacing=1.3)

img_slot(s, 10.02, 1.26, 2.68, 2.10, "Mockup 3 kartu TV",
         "satu kartu = satu temuan + pemilik + tenggat")

box(s, 10.02, 3.56, 2.68, 2.28, fill=SOFT, line=RULE, radius=0.05)
txt(s, 10.18, 3.70, 2.40, 0.22, [("CARA MEMBACA TABEL", 8.5, True, GOLD)])
txt(s, 10.18, 3.96, 2.40, 1.78,
    [("Kanal menunjukkan siapa yang menerima kartu: layar lantai, dasbor L1, L2, atau L3.", 8.5, None, GREY),
     ("Setiap kartu memuat satu temuan, bukan satu daftar.", 8.5, None, GREY),
     ("Angka pemicu memakai contoh workbook: 22, 973, 26,8%, 14,1%.", 8.5, None, GREY)],
    spacing=1.22)


# ================================================================ 6 · RENCANA
s = page("Rencana 8 pekan: fondasi dulu, tampilan terakhir", "Bagian 4 · rencana", 6,
         "Pilot Plant Snack, lalu Exist Plant, Dairy, dan New Plant")
table(s, [
    ["Fase", "Pekan", "Keluaran", "Prasyarat"],
    ["0 · Fondasi", "1–2", "Master data, aturan skor, hak akses", "Daftar line & mesin"],
    ["1 · Capture", "1–3", "Form meeting harian dan form kasus", "Aturan penilaian disetujui"],
    ["2 · Measure", "3–5", "Perhitungan skor dan dasbor line", "Data wajib terisi"],
    ["3 · Insight", "5–6", "Delapan aturan pertama aktif", "Riwayat kasus 12 bulan"],
    ["4 · Display", "7", "Layar lantai satu area", "Kartu temuan disepakati"],
    ["5 · Analitik", "7–8", "Dasbor plant dan ekspor", "Skor stabil dua pekan"],
], [1.95, 0.95, 4.00, 2.20], 0.62, 1.28, row_h=0.40, fs=9.5, bold_first=True,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT])

txt(s, 0.62, 4.28, 8.3, 0.24, [("UKURAN KEBERHASILAN YANG DIPERIKSA PEKANAN", 9, True, GOLD)])
table(s, [
    ["Ukuran", "Baseline", "Target"],
    ["Kepatuhan mengisi form", "belum terukur", "≥ 90%"],
    ["Kelengkapan root cause", "0% SHE · 79% QC", "≥ 95%"],
    ["Kasus lewat tenggat", "22 kasus", "turun 50%"],
    ["Pola ≥3× punya tindakan", "belum ada", "100%"],
    ["Insight ditindaklanjuti", "belum ada", "≥ 70%"],
], [3.55, 2.35, 1.60], 0.62, 4.58, row_h=0.34, fs=9,
    aligns=[PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER])

img_slot(s, 10.02, 1.28, 2.68, 2.05, "Gantt pilot 8 pekan", "tempel jadwal papan proyek")
txt(s, 10.02, 3.50, 2.68, 1.50,
    [("Empat dari lima ukuran sudah punya baseline hari ini, sehingga progres dapat "
      "dinilai sejak pekan pertama tanpa menunggu aplikasi selesai.", 8, None, GREY)],
    spacing=1.2)


# ================================================================ 7 · KANAL
s = page("Empat kanal tampilan dan batasannya", "Bagian 5 · tampilan", 7,
         "Struktur final; gambar antarmuka menyusul")
cards = [("Form harian", "Leader & DH", "satu layar, di bawah 5 menit",
          "Isi harian per line: item checklist, status, sebab bila tidak memenuhi target.", NAVY),
         ("Dasbor L1–L3", "Supervisor, plant head", "tiga tingkat dengan audiens berbeda",
          "L1 memantau hari ini, L2 menutup kasus, L3 membandingkan plant.", TEAL),
         ("Layar lantai (TV)", "Area produksi", "tanpa interaksi, rotasi 30 detik",
          "Kartu temuan terbuka: sebab, PIC, tenggat hitung mundur, foto bukti.", TEAL),
         ("Halaman admin", "Admin plant & group", "persetujuan, konfigurasi, audit",
          "Kelola pengguna, KPI plant, Healthy Check, dan tata letak kartu TV.", GOLD)]
x = 0.62
for name, who, desc, body, col in cards:
    box(s, x, 1.26, 2.95, 1.86, fill=WHITE, line=RULE, radius=0.05)
    hline(s, x + 0.01, 1.26, 2.93, col, 0.05)
    txt(s, x + 0.16, 1.44, 2.62, 0.24, [(name.upper(), 10, True, NAVY)])
    txt(s, x + 0.16, 1.72, 2.62, 0.22, [(who, 8.5, None, GREY)])
    txt(s, x + 0.16, 1.98, 2.62, 0.24, [(desc, 8.5, True, col)])
    txt(s, x + 0.16, 2.26, 2.62, 0.78, [(body, 8.5, None, INK)], spacing=1.22)
    x += 3.04

table(s, [
    ["Aturan tetap", "Isi"],
    ["Dua peran", "User dan Admin; layar TV tidak punya login"],
    ["Satu sumber angka", "Semua kanal membaca dari perhitungan yang sama"],
    ["Empat kolom wajib", "Sebab, tindakan, bukti, dan PIC sebelum kasus ditutup"],
    ["Kunci periode", "Skor periode yang sudah dilaporkan tidak dapat diubah"],
    ["Jejak audit", "Setiap perubahan tercatat: siapa, kapan, sebelum–sesudah"],
], [2.20, 6.35], 0.62, 3.32, row_h=0.365, fs=9.5, bold_first=True)

img_slot(s, 9.90, 3.32, 2.80, 1.82, "Mockup layar TV", "tangkapan layar atau desain akhir")

txt(s, 0.62, 5.60, 12.09, 0.24, [("YANG TIDAK DIBUAT SEKARANG", 9, True, GOLD)])
notes = [("Tanpa aplikasi mobile", "Form harian cukup berbasis web; tidak ada versi ponsel pada fase 1."),
         ("Tanpa login TV", "Layar lantai hanya menampilkan; hak ubah tetap di User dan Admin."),
         ("Tanpa angka manual", "Semua kanal membaca satu perhitungan; isian manual hanya Healthy Check.")]
x = 0.62
for head, body in notes:
    box(s, x, 5.88, 3.90, 0.86, fill=SOFT, line=RULE, radius=0.05)
    txt(s, x + 0.16, 5.98, 3.60, 0.22, [(head, 9, True, NAVY)])
    txt(s, x + 0.16, 6.22, 3.60, 0.44, [(body, 8, None, GREY)], spacing=1.18)
    x += 4.09


# ================================================================ 8 · BAHAN GAMBAR
s = page("Daftar bahan gambar yang harus di-screenshot", "Bagian 5 · bahan", 8,
         "Dikumpulkan sebelum deck dipresentasikan; semua bersumber dari workbook dan lantai")
table(s, [
    ["#", "Yang di-screenshot / difoto", "Diambil dari", "Untuk halaman", "Sorotan"],
    ["1", "Sheet Resume SHE", "workbook · sheet Resume SHE", "2, 3", "kolom root cause, due date, bukti 0%"],
    ["2", "Sheet Resume QC", "workbook · sheet Resume QC", "2", "320 baris Close tanpa sebab"],
    ["3", "Sheet Resume Produksi", "workbook · sheet Resume Produksi", "2", "653 baris Close tanpa sebab"],
    ["4", "Sheet Template Penilaian", "workbook · Template Penilaian", "3, 4", "formula AVERAGEIF dan band skor"],
    ["5", "Sheet Sheet1", "workbook · Sheet1", "4", "kolom ISO week"],
    ["6", "Sheet IIAA Snack", "workbook · IIAA Snack", "2", "baris duplikat"],
    ["7", "Papan monitoring line", "lantai produksi", "2, 8", "checklist yang diisi tangan"],
    ["8", "Form checklist terisi", "line · dokumen cetak", "3", "item yang dinilai persepsi"],
    ["9", "Foto rapat pagi", "area meeting line", "5", "tahap capture berjalan"],
    ["10", "Foto mesin / area", "Pilus L1 (contoh)", "5", "sumber 90% kasus produktivitas"],
    ["11", "Screenshot laporan harian", "WhatsApp atau email group", "2", "alur laporan sekarang"],
    ["12", "Screenshot layar TV (bila ada)", "area produksi", "7", "pembanding tampilan baru"],
], [0.45, 3.30, 3.60, 1.55, 3.45], 0.62, 1.26, row_h=0.355, fs=8.5, head_fs=9,
    aligns=[PP_ALIGN.CENTER, PP_ALIGN.LEFT, PP_ALIGN.LEFT, PP_ALIGN.CENTER, PP_ALIGN.LEFT])

txt(s, 1.05, 6.02, 8.30, 0.90,
    [("Cara mengambil: tampilkan nama sheet, header kolom, dan 5–10 baris contoh; "
      "blok kolom yang kosong agar terlihat. Foto lapangan landscape, minimal 1600 px, "
      "dan diberi keterangan tanggal.", 8.5, None, GREY)], spacing=1.25)


# ================================================================ 9 · KEPUTUSAN
s = page("Keputusan yang diminta dan langkah berikutnya", "Penutup · keputusan", 9,
         "Semua keputusan mengacu pada angka workbook; tidak ada tambahan asumsi baru")

txt(s, 0.62, 1.28, 4.15, 0.24, [("TIGA KEPUTUSAN TERBUKA", 9, True, GOLD)])
dec = [("1 · Kalender hari libur",
        "Master tahunan diisi sekali, atau input per tanggal? Penyebut skor bergantung pada jawaban ini."),
       ("2 · Status N/A pada KPI",
        "Item yang tidak relevan keluar dari penyebut, atau tetap dihitung nol?"),
       ("3 · Data historis",
        "5.817 kasus dibawa dengan penanda lama, atau mulai dari nol?")]
y = 1.60
for name, q in dec:
    box(s, 0.62, y, 4.15, 0.86, fill=SOFT, line=RULE, radius=0.05)
    txt(s, 0.78, y + 0.10, 3.85, 0.22, [(name, 10, True, NAVY)])
    txt(s, 0.78, y + 0.34, 3.85, 0.48, [(q, 8.5, None, GREY)], spacing=1.2)
    y += 0.98

txt(s, 5.02, 1.28, 3.20, 0.24, [("ANGKA YANG MENJADI DASAR", 9, True, GOLD)])
nums = [("5.817", "kasus diperiksa"), ("973", "tutup tanpa sebab"),
        ("94%", "label berulang salah"), ("22", "kasus lewat tenggat"),
        ("184", "pola berulang ≥3×")]
y = 1.60
for v, l in nums:
    txt(s, 5.02, y, 1.20, 0.30, [(v, 15, True, NAVY)])
    txt(s, 6.24, y + 0.06, 1.95, 0.24, [(l, 8.5, None, GREY)])
    hline(s, 5.02, y + 0.34, 3.15, RULE)
    y += 0.46

txt(s, 8.42, 1.28, 4.28, 0.24, [("LANGKAH SETELAH SESI", 9, True, GOLD)])
box(s, 8.42, 1.60, 4.28, 2.72, fill=None, line=RULE, radius=0.05)
txt(s, 8.62, 1.74, 3.90, 2.45,
    [("1. Tiga keputusan di atas diputuskan pada rapat ini.", 9, None, INK),
     ("2. Bahan gambar halaman 8 dikumpulkan maksimal tiga hari kerja.", 9, None, INK),
     ("3. Pilot Plant Snack mulai pekan berikutnya, fase 0 dua pekan.", 9, None, INK),
     ("4. Evaluasi pekan ke-8 memakai lima ukuran keberhasilan.", 9, None, INK),
     ("5. Hasil keputusan dicatat pada berita acara rapat dan disosialisasikan ke empat plant.", 9, None, INK)],
    spacing=1.45)

hline(s, 0.62, 4.86, 12.09, RULE)
bx = 0.62
for title_, name_, date_ in [("Disusun oleh", "Tim Daily Monitoring System", "Tanggal: ..............."),
                             ("Diperiksa oleh", "Plant Head / Dept Head", "Tanggal: ..............."),
                             ("Disetujui oleh", "Group Manufacturing", "Tanggal: ...............")]:
    box(s, bx, 5.02, 3.86, 1.30, fill=SOFT, line=RULE, radius=0.05)
    txt(s, bx + 0.18, 5.14, 3.50, 0.24, [(title_.upper(), 9, True, NAVY)])
    txt(s, bx + 0.18, 5.46, 3.50, 0.26, [(name_, 10, True, INK)])
    txt(s, bx + 0.18, 5.86, 3.50, 0.24, [(date_, 8.5, None, GREY)])
    bx += 4.11


# ================================================================ 10 · TERIMA KASIH
close = prs.slides.add_slide(CLOSE_L)
for ph in list(close.placeholders):
    ph._element.getparent().remove(ph._element)

prs.save(OUT)
print("saved", OUT, "slides:", len(prs.slides._sldIdLst))
