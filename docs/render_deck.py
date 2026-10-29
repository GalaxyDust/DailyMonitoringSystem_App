from pptx import Presentation
from PIL import Image, ImageDraw, ImageFont
import textwrap, os, io, sys

p = Presentation(sys.argv[1] if len(sys.argv) > 1 else 'docs/DMS_Digitalisasi_v1.pptx')
W, H = 1280, 720
os.makedirs('/tmp/prev', exist_ok=True)


def font(sz, bold=False):
    pa = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(pa, max(int(sz * 96 / 72), 6)) if os.path.exists(pa) else ImageFont.load_default()


def rgb(c):
    try:
        return tuple(c.rgb)
    except Exception:
        return (120, 120, 120)


def draw_bg(img, slide):
    shapes = []
    try:
        for sh in slide.slide_master.shapes:
            shapes.append(sh)
    except Exception:
        pass
    for sh in slide.slide_layout.shapes:
        shapes.append(sh)
    for sh in shapes:
        if sh.shape_type == 13:
            try:
                x = sh.left / 914400 * 96; y = sh.top / 914400 * 96
                w = (sh.width or 0) / 914400 * 96; h = (sh.height or 0) / 914400 * 96
                im = Image.open(io.BytesIO(sh.image.blob)).convert('RGB')
                iw, ih = im.size
                l = sh.crop_left or 0; r = sh.crop_right or 0
                t = sh.crop_top or 0; b = sh.crop_bottom or 0
                box = (int(l * iw), int(t * ih), int(iw - r * iw), int(ih - b * ih))
                if box[2] > box[0] and box[3] > box[1]:
                    im = im.crop(box)
                img.paste(im.resize((max(int(w), 1), max(int(h), 1))), (int(x), int(y)))
            except Exception:
                pass


for i, s in enumerate(p.slides, 1):
    img = Image.new('RGB', (W, H), (250, 250, 252))
    draw_bg(img, s)
    d = ImageDraw.Draw(img)
    for sh in s.shapes:
        try:
            x = (sh.left or 0) / 914400 * 96; y = (sh.top or 0) / 914400 * 96
            w = (sh.width or 0) / 914400 * 96; h = (sh.height or 0) / 914400 * 96
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
        if st == 9:  # connector
            try:
                d.line([(x, y), (x + w, y + h)], fill=rgb(sh.line.color), width=2)
            except Exception:
                pass
            continue
        if sh.has_table if hasattr(sh, 'has_table') else False:
            tb = sh.table
            cy = y
            rowh = h / max(len(tb.rows), 1)
            for r_i, row in enumerate(tb.rows):
                cx = x
                colw = [c.width / 914400 * 96 for c in tb.columns]
                for c_i, cell in enumerate(row.cells):
                    try:
                        fill = rgb(cell.fill.fore_color)
                    except Exception:
                        fill = (255, 255, 255)
                    d.rectangle([cx, cy, cx + colw[c_i], cy + rowh], fill=fill,
                                outline=(210, 214, 222))
                    txt = cell.text
                    if txt:
                        f = font(8.5, bold=(r_i == 0))
                        lines = textwrap.wrap(txt, width=max(int(colw[c_i] / 5.0), 6))
                        ty = cy + 3
                        for ln in lines[:4]:
                            d.text((cx + 5, ty), ln, font=f,
                                   fill=(255, 255, 255) if r_i == 0 else (31, 41, 55))
                            ty += 11
                    cx += colw[c_i]
                cy += rowh
            continue
        # shapes / textboxes
        try:
            fill = rgb(sh.fill.fore_color) if sh.fill.type == 1 else None
        except Exception:
            fill = None
        try:
            lc = rgb(sh.line.color) if sh.line.fill.type == 1 else None
        except Exception:
            lc = None
        if fill or lc:
            d.rectangle([x, y, x + w, y + h], fill=fill, outline=lc)
        if sh.has_text_frame and sh.text_frame.text.strip():
            ty = y + 1
            for para in sh.text_frame.paragraphs:
                txt = ''.join(r.text for r in para.runs)
                if not txt:
                    ty += 6
                    continue
                sz = para.runs[0].font.size.pt if para.runs[0].font.size else 12
                bold = bool(para.runs[0].font.bold)
                col = rgb(para.runs[0].font.color) if para.runs[0].font.color and para.runs[0].font.color.type is not None else (31, 41, 55)
                f = font(min(sz, 30), bold)
                lines = []
                for seg in txt.split('\n'):
                    lines += textwrap.wrap(seg, width=max(int((w / 96) * 96 / (sz * 0.52)), 6)) or ['']
                for ln in lines:
                    d.text((x, ty), ln, font=f, fill=col)
                    ty += sz * 96 / 72 * (para.line_spacing or 1.15) * 0.86
    img.save(f'/tmp/prev/s{i:02d}.png')
print('ok', len(p.slides))
