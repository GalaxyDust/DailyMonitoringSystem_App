"""Renderer verifikasi visual (tanpa LibreOffice).

Menggambar ulang slide dari XML: gambar latar, shape (kotak, panah, diamond),
tabel, grafik batang (column/bar, bertumpuk), dan teks dengan bold/regular.

Pemakaian: python3 docs/render_deck.py [file.pptx] -> /tmp/prev/sNN.png
"""
from pptx import Presentation
from PIL import Image, ImageDraw, ImageFont
import textwrap, os, io, sys
from pptx.enum.chart import XL_CHART_TYPE

p = Presentation(sys.argv[1] if len(sys.argv) > 1 else 'docs/DMS_Digitalisasi_v1.pptx')
W, H = 1280, 720
os.makedirs('/tmp/prev', exist_ok=True)
EMU = 914400


def font(sz, bold=False):
    pa = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(pa, max(int(sz * 96 / 72), 6)) if os.path.exists(pa) else ImageFont.load_default()


def rgb(c, default=(120, 120, 120)):
    try:
        if c is None or c.type is None:
            return default
        return tuple(c.rgb)
    except Exception:
        return default


def geometry(sh):
    return ((sh.left or 0) / EMU * 96, (sh.top or 0) / EMU * 96,
            (sh.width or 0) / EMU * 96, (sh.height or 0) / EMU * 96)


def draw_bg(img, slide):
    shapes = []
    try:
        shapes += list(slide.slide_master.shapes)
    except Exception:
        pass
    shapes += list(slide.slide_layout.shapes)
    for sh in shapes:
        if sh.shape_type == 13:
            try:
                x, y, w, h = geometry(sh)
                im = Image.open(io.BytesIO(sh.image.blob)).convert('RGB')
                iw, ih = im.size
                l, r = sh.crop_left or 0, sh.crop_right or 0
                t, b = sh.crop_top or 0, sh.crop_bottom or 0
                bb = (int(l * iw), int(t * ih), int(iw - r * iw), int(ih - b * ih))
                if bb[2] > bb[0] and bb[3] > bb[1]:
                    im = im.crop(bb)
                img.paste(im.resize((max(int(w), 1), max(int(h), 1))), (int(x), int(y)))
            except Exception:
                pass


def shape_kind(sh):
    try:
        return str(sh.auto_shape_type)
    except Exception:
        return ''


def draw_shape(d, sh, x, y, w, h, fill, lc):
    kind = shape_kind(sh)
    if 'DIAMOND' in kind:
        d.polygon([(x + w / 2, y), (x + w, y + h / 2), (x + w / 2, y + h), (x, y + h / 2)],
                  fill=fill, outline=lc)
    elif 'RIGHT_ARROW' in kind:
        sh_h = h / 2
        d.polygon([(x, y + h * .25), (x + w - sh_h, y + h * .25), (x + w - sh_h, y),
                   (x + w, y + h / 2), (x + w - sh_h, y + h), (x + w - sh_h, y + h * .75),
                   (x, y + h * .75)], fill=fill, outline=lc)
    elif 'LEFT_ARROW' in kind:
        sh_h = h / 2
        d.polygon([(x + w, y + h * .25), (x + sh_h, y + h * .25), (x + sh_h, y),
                   (x, y + h / 2), (x + sh_h, y + h), (x + sh_h, y + h * .75),
                   (x + w, y + h * .75)], fill=fill, outline=lc)
    elif 'DOWN_ARROW' in kind:
        sw = w / 2
        d.polygon([(x + w * .25, y), (x + w * .75, y), (x + w * .75, y + h - sw),
                   (x + w, y + h - sw), (x + w / 2, y + h), (x, y + h - sw),
                   (x + w * .25, y + h - sw)], fill=fill, outline=lc)
    elif 'ROUNDED_RECTANGLE' in kind:
        r = min(w, h) * 0.16
        d.rounded_rectangle([x, y, x + w, y + h], radius=r, fill=fill, outline=lc)
    else:
        d.rectangle([x, y, x + w, y + h], fill=fill, outline=lc)


def para_lines(para, width):
    runs = list(para.runs)
    sz = runs[0].font.size.pt if runs and runs[0].font.size else 12
    txt = ''.join(r.text for r in runs)
    out = []
    for seg in txt.split('\n'):
        out += textwrap.wrap(seg, width=max(int(width / (sz * 0.667)), 6)) or ['']
    return out, sz


def text_height(tf, width):
    total = 0.0
    for para in tf.paragraphs:
        lines, sz = para_lines(para, width)
        total += len(lines) * sz * 96 / 72 * (para.line_spacing or 1.15) * 1.02
    return total


def draw_text(d, sh, x, y, w, h):
    if not (sh.has_text_frame and sh.text_frame.text.strip()):
        return
    tf = sh.text_frame
    ml = (tf.margin_left or 0) / EMU * 96
    mt = (tf.margin_top or 0) / EMU * 96
    inner = w - ml - 4
    total_h = text_height(tf, inner)
    ty = y + mt + (max(h - total_h, 0) / 2 if 'MIDDLE' in str(tf.vertical_anchor) else 0)
    for para in tf.paragraphs:
        lines, sz = para_lines(para, inner)
        if not ''.join(r.text for r in para.runs):
            ty += 6
            continue
        run = para.runs[0]
        bold = bool(run.font.bold)
        col = rgb(run.font.color, (31, 41, 55))
        f = font(min(sz, 30), bold)
        align = str(para.alignment)
        for ln in lines:
            tw = d.textlength(ln, font=f)
            tx = x + ml
            if 'CENTER' in align:
                tx = x + ml + (inner - tw) / 2
            elif 'RIGHT' in align:
                tx = x + ml + (inner - tw)
            d.text((tx, ty), ln, font=f, fill=col)
            ty += sz * 96 / 72 * (para.line_spacing or 1.15) * 1.02


def fmt(v, nf):
    nf = nf or '0'
    if '%' in nf:
        if '0.0' in nf:
            return f"{v:.1f}%"
        return f"{v:.0f}%"
    if '#,##0' in nf:
        s = f"{v:,.0f}".replace(',', '.')
        return s
    if '0.0' in nf:
        return f"{v:.1f}"
    return f"{v:.0f}"


def draw_chart(d, sh, x, y, w, h):
    ch = sh.chart
    ctype = ch.chart_type
    cats = [str(c) for c in ch.plots[0].categories]
    series = []
    for s in ch.series:
        fill = rgb(s.format.fill.fore_color, (31, 51, 100))
        vals = [v for v in s.values]
        series.append((s.name or '', vals, fill))
    stacked = ctype in (XL_CHART_TYPE.BAR_STACKED_100, XL_CHART_TYPE.COLUMN_STACKED_100,
                        XL_CHART_TYPE.BAR_STACKED, XL_CHART_TYPE.COLUMN_STACKED)
    horizontal = ctype in (XL_CHART_TYPE.BAR_CLUSTERED, XL_CHART_TYPE.BAR_STACKED,
                           XL_CHART_TYPE.BAR_STACKED_100)
    pct = ctype in (XL_CHART_TYPE.BAR_STACKED_100, XL_CHART_TYPE.COLUMN_STACKED_100)
    va = ch.value_axis
    vmax = va.maximum_scale or 1.0
    nf = ch.plots[0].data_labels.number_format

    legend_h = 18 if ch.has_legend else 0
    if ch.has_legend:
        lx = x + 4
        for name, _, col in series:
            d.rectangle([lx, y + 4, lx + 9, y + 13], fill=col)
            d.text((lx + 13, y + 2), name, font=font(8), fill=(92, 100, 114))
            lx += 22 + d.textlength(name, font=font(8))

    padl = 54 if not horizontal else 82
    padt = y + legend_h + 6
    padb = 18 if not horizontal else 26
    plot = (x + padl, padt, x + w - 8, y + h - padb)
    pw, ph = plot[2] - plot[0], plot[3] - plot[1]
    if pw <= 10 or ph <= 10:
        return

    if not horizontal:
        for g in range(5):
            gy = plot[3] - ph * g / 4
            d.line([plot[0], gy, plot[2], gy], fill=(231, 234, 240))
            d.text((x + 4, gy - 6), fmt(vmax * g / 4, nf), font=font(7), fill=(139, 147, 161))
        n = len(cats)
        ns = max(len(series), 1)
        slot = pw / max(n, 1)
        group = slot * 0.68
        bw = group / ns
        for i, cat in enumerate(cats):
            base = plot[0] + slot * i + (slot - group) / 2
            bottom = plot[3]
            for si, (name, vals, col) in enumerate(series):
                v = vals[i]
                hh = ph * (v / vmax)
                top = bottom - hh
                cx = base + si * bw
                d.rectangle([cx, top, cx + bw - 1, bottom], fill=col)
                if not stacked:
                    bottom = plot[3]
                    lbl = fmt(v, nf)
                    d.text((cx + (bw - 1) / 2 - d.textlength(lbl, font=font(7, True)) / 2, top - 12),
                           lbl, font=font(7, True), fill=(31, 51, 100))
                else:
                    lbl = fmt(v, nf)
                    if hh > 14:
                        d.text((cx + (bw - 1) / 2 - d.textlength(lbl, font=font(7, True)) / 2,
                                top + hh / 2 - 6), lbl, font=font(7, True), fill=(255, 255, 255))
                    bottom = top
            lab = cat
            tw = d.textlength(lab, font=font(8))
            d.text((plot[0] + slot * i + slot / 2 - tw / 2, plot[3] + 5), lab, font=font(8), fill=(34, 40, 51))
    else:
        for g in range(5):
            gx = plot[0] + pw * g / 4
            d.line([gx, plot[1], gx, plot[3]], fill=(231, 234, 240))
            d.text((gx - 12, plot[3] + 6), fmt(vmax * g / 4, nf), font=font(7), fill=(139, 147, 161))
        n = len(cats)
        ns = max(len(series), 1)
        slot = ph / max(n, 1)
        group = slot * 0.68
        bh = group / ns
        for i, cat in enumerate(cats):
            base = plot[1] + slot * i + (slot - group) / 2
            left = plot[0]
            for si, (name, vals, col) in enumerate(series):
                v = vals[i]
                bwv = pw * (v / vmax)
                cy = base + si * bh
                d.rectangle([left, cy, left + bwv, cy + bh - 1], fill=col)
                lbl = fmt(v, nf)
                if bwv > 40 and not stacked:
                    d.text((left + bwv / 2 - d.textlength(lbl, font=font(8, True)) / 2,
                            cy + bh / 2 - 7), lbl, font=font(8, True), fill=(255, 255, 255))
                else:
                    d.text((left + bwv + 3, cy + bh / 2 - 7), lbl, font=font(8, True),
                           fill=(31, 51, 100))
                if stacked:
                    left += bwv
            lab = cat
            tw = d.textlength(lab, font=font(8))
            d.text((plot[0] - tw - 6, base + group / 2 - 7), lab, font=font(8), fill=(34, 40, 51))


for i, s in enumerate(p.slides, 1):
    img = Image.new('RGB', (W, H), (250, 250, 252))
    draw_bg(img, s)
    d = ImageDraw.Draw(img)
    for sh in s.shapes:
        try:
            x, y, w, h = geometry(sh)
        except Exception:
            continue
        st = sh.shape_type
        if st == 13:
            try:
                im = Image.open(io.BytesIO(sh.image.blob)).convert('RGB')
                img.paste(im.resize((max(int(w), 1), max(int(h), 1))), (int(x), int(y)))
            except Exception:
                pass
            continue
        if hasattr(sh, 'has_chart') and sh.has_chart:
            draw_chart(d, sh, x, y, w, h)
            continue
        if hasattr(sh, 'has_table') and sh.has_table:
            tb = sh.table
            widths = [c.width / EMU * 96 for c in tb.columns]
            heights = [r.height / EMU * 96 for r in tb.rows]
            cy = y
            for r_i, row in enumerate(tb.rows):
                cx = x
                for c_i, cell in enumerate(row.cells):
                    try:
                        fill = rgb(cell.fill.fore_color, (255, 255, 255))
                    except Exception:
                        fill = (255, 255, 255)
                    d.rectangle([cx, cy, cx + widths[c_i], cy + heights[r_i]], fill=fill,
                                outline=(213, 218, 227))
                    tf = cell.text_frame
                    runs = tf.paragraphs[0].runs
                    sz = runs[0].font.size.pt if runs and runs[0].font.size else 9
                    bold = (r_i == 0) or bool(runs[0].font.bold) if runs else False
                    col = (255, 255, 255) if r_i == 0 else (34, 40, 51)
                    ml = (tf.margin_left or 0) / EMU * 96
                    inner = widths[c_i] - ml - 4
                    lines = []
                    for seg in cell.text.split('\n'):
                        lines += textwrap.wrap(seg, width=max(int(inner / (sz * 0.64)), 6)) or ['']
                    lh = sz * 96 / 72 * 1.12
                    ty = cy + heights[r_i] / 2 - len(lines) * lh / 2
                    f = font(sz, bold)
                    for ln in lines:
                        tw = d.textlength(ln, font=f)
                        align = str(tf.paragraphs[0].alignment)
                        tx = cx + ml
                        if 'CENTER' in align:
                            tx = cx + ml + (inner - tw) / 2
                        elif 'RIGHT' in align:
                            tx = cx + ml + inner - tw
                        d.text((tx, ty), ln, font=f, fill=col)
                        ty += lh
                    cx += widths[c_i]
                cy += heights[r_i]
            continue
        try:
            fill = rgb(sh.fill.fore_color) if sh.fill.type == 1 else None
        except Exception:
            fill = None
        try:
            lc = rgb(sh.line.color) if sh.line.fill.type == 1 else None
        except Exception:
            lc = None
        if fill or lc:
            draw_shape(d, sh, x, y, w, h, fill, lc)
        draw_text(d, sh, x, y, w, h)
    img.save(f'/tmp/prev/s{i:02d}.png')
print('ok', len(p.slides))
