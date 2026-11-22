"""Render entry.png: a one-page front page for Sunday 22 November 2026.

Run with Pillow installed:  python3 draw_entry.py
Everything is drawn with plain PIL shapes and DejaVu fonts; no network.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (245, 238, 222)
INK = (24, 22, 20)
GREY = (92, 88, 82)
RED = (196, 30, 36)
NIGHT = (30, 32, 44)
GOLD = (214, 190, 120)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SANS_B = FONT_DIR + "DejaVuSans-Bold.ttf"
SANS = FONT_DIR + "DejaVuSans.ttf"
SERIF_B = FONT_DIR + "DejaVuSerif-Bold.ttf"

HERE = os.path.dirname(os.path.abspath(__file__))


def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(d, s, f):
    b = d.textbbox((0, 0), s, font=f)
    return b[2] - b[0]


def wrap(d, s, f, max_w):
    lines, cur = [], ""
    for word in s.split():
        trial = (cur + " " + word).strip()
        if text_w(d, trial, f) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def fit(d, s, path, max_w, max_lines, start, smallest):
    """Largest size (<= start) where s wraps into max_lines within max_w."""
    for size in range(start, smallest - 1, -1):
        f = font(path, size)
        lines = wrap(d, s, f, max_w)
        if len(lines) <= max_lines and all(text_w(d, l, f) <= max_w for l in lines):
            return f, lines
    raise SystemExit("does not fit: " + s)


def block(d, x, y, lines, f, fill, gap=1.12):
    asc, desc = f.getmetrics()
    step = int((asc + desc) * gap)
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += step
    return y


# ---------------------------------------------------------------- pictograms

def cop_panel(d, x0, y0, x1, y1):
    """Dawn over Antalya: globe, rising sun, 06:00 GMT clock, caption strip."""
    d.rectangle((x0, y0, x1, y1), fill=NIGHT)
    w, h = x1 - x0, y1 - y0
    # stars
    for sx, sy in ((0.12, 0.10), (0.30, 0.06), (0.55, 0.12), (0.78, 0.07),
                   (0.88, 0.20), (0.06, 0.28), (0.42, 0.16)):
        d.ellipse((x0 + sx * w - 2, y0 + sy * h - 2,
                   x0 + sx * w + 2, y0 + sy * h + 2), fill=PAPER)
    # rising sun with rays, low on the horizon
    sun_cx, sun_cy, sun_r = x0 + w * 0.50, y0 + h * 0.72, 52
    for k in range(9):
        a = math.pi * (1 + k / 8.0)
        d.line((sun_cx + (sun_r + 10) * math.cos(a), sun_cy + (sun_r + 10) * math.sin(a),
                sun_cx + (sun_r + 34) * math.cos(a), sun_cy + (sun_r + 34) * math.sin(a)),
               fill=GOLD, width=5)
    d.pieslice((sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r),
               180, 360, fill=RED)
    d.line((x0, sun_cy, x1, sun_cy), fill=GOLD, width=3)
    # globe above the sun
    gx, gy, gr = x0 + w * 0.50, y0 + h * 0.30, 88
    d.ellipse((gx - gr, gy - gr, gx + gr, gy + gr), outline=PAPER, width=4)
    d.ellipse((gx - gr * 0.45, gy - gr, gx + gr * 0.45, gy + gr), outline=PAPER, width=3)
    d.line((gx - gr, gy, gx + gr, gy), fill=PAPER, width=3)
    d.line((gx - gr * 0.85, gy - gr * 0.45, gx + gr * 0.85, gy - gr * 0.45), fill=PAPER, width=2)
    d.line((gx - gr * 0.85, gy + gr * 0.45, gx + gr * 0.85, gy + gr * 0.45), fill=PAPER, width=2)
    # clock: 06:00, hands at 12 and 6
    ccx, ccy, cr = x0 + w * 0.84, y0 + h * 0.30, 34
    d.ellipse((ccx - cr, ccy - cr, ccx + cr, ccy + cr), fill=PAPER, outline=INK, width=3)
    d.line((ccx, ccy, ccx, ccy - cr * 0.72), fill=INK, width=4)
    d.line((ccx, ccy, ccx, ccy + cr * 0.55), fill=RED, width=4)
    d.ellipse((ccx - 4, ccy - 4, ccx + 4, ccy + 4), fill=INK)
    fclock = font(SANS_B, 20)
    clock_label = "06:00 GMT"
    d.text((ccx - text_w(d, clock_label, fclock) // 2, ccy + cr + 8),
           clock_label, font=fclock, fill=PAPER)
    # caption strip
    d.rectangle((x0, y1 - 40, x1, y1), fill=INK)
    fcap = font(SANS_B, 20)
    cap = "FINAL TEXT TABLED OVERNIGHT"
    d.text((x0 + (w - text_w(d, cap, fcap)) // 2, y1 - 34), cap, font=fcap, fill=PAPER)


def cricket_icon(d, x, y, s):
    """Pant's 128: the score over a tilted bat, ball and stumps."""
    a = math.radians(-32)

    def rot(px, py):
        return (x + s * 0.62 + px * math.cos(a) - py * math.sin(a),
                y + s * 0.78 + px * math.sin(a) + py * math.cos(a))
    blade = [rot(-16, -12), rot(16, -12), rot(18, 78), rot(-18, 78)]
    handle = [rot(-6, -62), rot(6, -62), rot(6, -12), rot(-6, -12)]
    d.polygon(blade, fill=(214, 182, 120), outline=INK)
    d.polygon(handle, fill=INK)
    # score drawn last so the bat handle never cuts through a digit
    f = font(SERIF_B, int(s * 0.62))
    d.text((x + s * 0.10, y - s * 0.08), "128", font=f, fill=RED)
    # stumps
    sx = x + s * 1.28
    for i in range(3):
        d.rectangle((sx + i * 16, y + s * 0.55, sx + i * 16 + 9, y + s * 1.05), fill=INK)
    d.rectangle((sx + 2, y + s * 0.50, sx + 20, y + s * 0.55), fill=INK)
    d.rectangle((sx + 26, y + s * 0.50, sx + 44, y + s * 0.55), fill=INK)
    # red ball
    bx, by = x + s * 1.30, y + s * 1.28
    d.ellipse((bx - 14, by - 14, bx + 14, by + 14), fill=RED)


def protest_icon(d, x, y, s):
    """Crowd with placards: one reads 82,500, one reads 25."""
    # placards on sticks, spaced so no board covers another's text
    boards = [
        (x + s * 0.00, 76, 58, RED, "82,500", PAPER, 17),
        (x + s * 0.72, 66, 58, INK, "25", PAPER, 26),
        (x + s * 1.36, 66, 58, (120, 112, 100), "", PAPER, 19),
    ]
    for bx, bw, bh, fill, label, tfill, tsize in boards:
        top = y + s * 0.04
        d.line((bx + bw // 2, top + bh, bx + bw // 2, y + s * 0.78), fill=INK, width=4)
        d.rectangle((bx, top, bx + bw, top + bh), fill=fill, outline=INK, width=2)
        if label:
            fl = font(SANS_B, tsize)
            d.text((bx + (bw - text_w(d, label, fl)) // 2, top + (bh - tsize) // 2 - 2),
                   label, font=fl, fill=tfill)
    # crowd: heads and shoulders
    base = y + s * 1.02
    for i, hx in enumerate((0.08, 0.38, 0.68, 0.98, 1.28)):
        cx = x + s * hx
        d.ellipse((cx - 15, base - 52, cx + 15, base - 22), fill=INK)
        d.pieslice((cx - 26, base - 26, cx + 26, base + 26), 180, 360, fill=INK)
    d.line((x, base + 4, x + s * 1.55, base + 4), fill=INK, width=3)


# ---------------------------------------------------------------- page

def story(d, x, y, w, tag, head, deck, head_size, head_lines, deck_size, limit):
    """Tag, headline and deck; the headline shrinks until the block fits above limit."""
    ft = font(SANS_B, 16)
    for size in range(head_size, 19, -1):
        fh, lines = fit(d, head, SANS_B, w, head_lines, size, 20)
        asc, desc = fh.getmetrics()
        hy = y + 24 + len(lines) * int((asc + desc) * 1.05) + 6
        fd, dl = fit(d, deck, SANS, w, 2, deck_size, 15)
        a2, d2 = fd.getmetrics()
        end = hy + len(dl) * int((a2 + d2) * 1.12)
        if end <= limit:
            break
    else:
        raise SystemExit("overflow: " + head)
    d.text((x, y), tag, font=ft, fill=RED)
    block(d, x, y + 24, lines, fh, INK, 1.05)
    return block(d, x, hy, dl, fd, GREY, 1.12)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28

    # masthead
    fm, _ = fit(d, "THE WORLD IN ONE DAY", SERIF_B, W - 2 * M, 1, 76, 40)
    mw = text_w(d, "THE WORLD IN ONE DAY", fm)
    d.text(((W - mw) // 2, 14), "THE WORLD IN ONE DAY", font=fm, fill=INK)
    d.line((M, 104, W - M, 104), fill=INK, width=3)
    # date band
    d.rectangle((M, 112, W - M, 166), fill=RED)
    fdte = font(SANS_B, 40)
    date = "SUNDAY, 22 NOVEMBER 2026"
    d.text(((W - text_w(d, date, fdte)) // 2, 116), date, font=fdte, fill=PAPER)

    # lead story: about 40% of the page
    top, bottom = 180, 556
    cop_panel(d, M, top, M + 450, bottom)
    tx = M + 472
    tw = W - M - tx
    y = story(d, tx, top + 20, tw, "LEAD · CLIMATE · ANTALYA",
              "COP31 NEARS DEAL AT DAWN",
              "Final text tabled overnight; delegates vote Sunday morning",
              62, 3, 23, bottom - 70)
    fx = font(SANS_B, 20)
    extra = wrap(d, "Plenary reconvenes 06:00 GMT after talks ran past Friday's deadline",
                 fx, tw)
    d.line((tx, y + 8, tx + 60, y + 8), fill=RED, width=3)
    block(d, tx, y + 16, extra, fx, INK, 1.1)
    d.line((M, bottom + 12, W - M, bottom + 12), fill=INK, width=2)

    # row one: cricket, full width
    ry, row_end = 580, 772
    cricket_icon(d, M + 4, ry + 6, 120)
    story(d, M + 250, ry + 6, W - M - (M + 250), "SPORT · WELLINGTON",
          "PANT TON PUTS INDIA ON TOP",
          "Pant's 128 takes India past 600 — a record total in New Zealand",
          44, 2, 19, row_end)
    d.line((M, row_end + 12, W - M, row_end + 12), fill=INK, width=2)

    # row two: protests, full width
    ry2 = row_end + 24
    protest_icon(d, M + 4, ry2 + 2, 118)
    story(d, M + 250, ry2 + 2, W - M - (M + 250), "EUROPE",
          "STREETS STAY FULL INTO SUNDAY",
          "Youth protests over living costs roll into Sunday across 25 nations",
          44, 2, 19, H - 44)

    ff = font(SANS, 15)
    foot = "Events reported on Sunday 22 November 2026  ·  Sources: Reuters, CNN, Al Jazeera"
    d.line((M, H - 34, W - M, H - 34), fill=INK, width=1)
    d.text(((W - text_w(d, foot, ff)) // 2, H - 28), foot, font=ff, fill=GREY)

    img.save(os.path.join(HERE, "entry.png"), optimize=True)


if __name__ == "__main__":
    main()
