"""Offline generator that produced the committed entry.png. Requires Pillow and Noto fonts available on the build machine, not the grader."""

from PIL import Image, ImageDraw, ImageFont
import os

W = H = 1024
PAPER = "#f6f1e7"
INK = "#14202e"
NAVY = "#10243e"
GOLD = "#e8b64c"
RED = "#c0392b"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"
BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
BLACK = "/usr/share/fonts/truetype/noto/NotoSans-Black.ttf"

im = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(im)

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(text, f, max_width):
    words = text.split()
    lines, line = [], ""
    for word in words:
        trial = word if not line else line + " " + word
        if d.textbbox((0, 0), trial, font=f)[2] <= max_width:
            line = trial
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines

def fit_lines(text, path, size, min_size, width, max_lines):
    while size >= min_size:
        f = font(path, size)
        lines = wrap(text, f, width)
        if len(lines) <= max_lines:
            return f, lines
        size -= 1
    f = font(path, min_size)
    return f, wrap(text, f, width)[:max_lines]

def draw_lines(lines, f, x, y, fill, leading):
    for line in lines:
        d.text((x, y), line, font=f, fill=fill)
        y += leading
    return y

# Masthead
d.rectangle((0, 0, W, 168), fill=NAVY)
d.text((30, 13), "THE WORLD IN ONE DAY", font=font(BOLD, 19), fill=GOLD)
d.text((28, 37), "19 NOVEMBER 2026", font=font(BLACK, 76), fill="#ffffff")
d.text((31, 127), "Thursday · The day's world news in a single picture", font=font(REG, 20), fill="#ffffff")
d.rectangle((0, 168, W, 174), fill=RED)

# Lead story
d.rectangle((0, 174, W, 406), fill="#7c2128")
d.rectangle((0, 403, W, 405), fill=GOLD)
d.text((30, 191), "SUMMIT · SHENZHEN", font=font(BOLD, 18), fill=GOLD)
hero_title = "Trump, Xi & Putin Hold First Three-Way Summit"
hf, hl = fit_lines(hero_title, BOLD, 44, 37, 680, 2)
draw_lines(hl, hf, 30, 221, "#ffffff", int(hf.size * 1.13))
detail = "Joint peace declaration denounces nuclear war and pledges dialogue on nuclear risk."
df, dl = fit_lines(detail, REG, 24, 21, 680, 2)
draw_lines(dl, df, 30, 329, "#ffffff", int(df.size * 1.27))

# Flat national flags, vertically centred in the hero panel.
flag_y, flag_w, flag_h = 244, 64, 92
# USA: thirteen red and white stripes with a navy canton.
for stripe in range(13):
    sy = flag_y + stripe * flag_h // 13
    ey = flag_y + (stripe+1) * flag_h // 13 - 1
    d.rectangle((748, sy, 811, ey), fill="#c0392b" if stripe % 2 == 0 else "#ffffff")
d.rectangle((748, flag_y, 776, flag_y+49), fill="#10243e")
# China: red field and small abstract gold stars/dots.
d.rectangle((832, flag_y, 895, flag_y+91), fill="#c0392b")
for sx, sy, radius in ((840, 254, 3), (851, 250, 2), (856, 260, 2), (851, 271, 2)):
    d.ellipse((sx-radius, sy-radius, sx+radius, sy+radius), fill="#e8b64c")
# Russia: three horizontal bands.
for stripe, color in enumerate(("#ffffff", "#35658d", "#c0392b")):
    d.rectangle((916, flag_y+stripe*31, 979, flag_y+(stripe+1)*31-1), fill=color)
for flag_x in (748, 832, 916):
    d.rectangle((flag_x, flag_y, flag_x+flag_w-1, flag_y+flag_h-1), outline="#ffffff", width=1)

# Story grid
cards = [
    ("JUSTICE · THE HAGUE", "#a87918", "World Court Rules Myanmar Committed Genocide", "The ICJ finds Myanmar responsible for genocide against the Rohingya minority.", "justice"),
    ("MARKETS · NEW YORK", "#2f8057", "Anthropic Prices Record $81 Billion IPO", "Shares priced at $83 — yet US stocks still slide as the AI sell-off deepens.", "market"),
    ("CONFLICT · HORMUZ", "#d65c38", "Tankers Hit Mines in the Strait of Hormuz", "Three tankers set ablaze; 11 crew injured and one sailor missing.", "conflict"),
    ("SPACE", "#5962a8", "Voyager 1 Is Now One Light-Day From Earth", "NASA's 1977 probe reaches a distance light itself takes 24 hours to cross.", "space"),
    ("GAMES", "#8052a0", "GTA VI Finally Launches After 13-Year Wait", "Rockstar's blockbuster lands to rave reviews from critics and fans.", "games"),
    ("TRAGEDY · SENEGAL", "#54728a", "Migrant Boat Capsizes Off Senegal", "A wooden boat carrying about 100 people struck rocks overnight; dozens are missing.", "sea"),
]
left, right, gap = 28, 520, 24
cw, ch = 476, 174
ys = [420, 603, 786]

def icon(kind, x, y, color):
    if kind == "justice":
        d.line((x+20,y+3,x+20,y+34), fill=color, width=5)
        d.line((x+4,y+10,x+36,y+10), fill=color, width=4)
        d.line((x+10,y+10,x+7,y+23), fill=color, width=3); d.line((x+30,y+10,x+33,y+23), fill=color, width=3)
        d.polygon([(x+2,y+23),(x+12,y+23),(x+7,y+29)], outline=color)
        d.polygon([(x+28,y+23),(x+38,y+23),(x+33,y+29)], outline=color)
        d.arc((x+1,y+23,x+13,y+31), 0, 180, fill=color, width=3); d.arc((x+27,y+23,x+39,y+31), 0, 180, fill=color, width=3)
        d.line((x+9,y+38,x+31,y+38), fill=color, width=5)
    elif kind == "market":
        d.line((x+2,y+36,x+2,y+4), fill=color, width=4); d.line((x+2,y+36,x+38,y+36), fill=color, width=4)
        d.line((x+6,y+29,x+16,y+21,x+24,y+25,x+36,y+8), fill=color, width=5)
        d.polygon([(x+36,y+8),(x+28,y+10),(x+34,y+16)], fill=color)
    elif kind == "conflict":
        # Simple tanker: hull, rear bridge, deck line, and one flame.
        d.polygon([(x+2,y+24),(x+39,y+24),(x+33,y+34),(x+9,y+34)], fill=color)
        d.rectangle((x+5,y+18,x+12,y+23), fill=color)
        d.line((x+14,y+22,x+37,y+22), fill=color, width=3)
        d.polygon([(x+27,y+20),(x+29,y+12),(x+32,y+17),(x+35,y+11),(x+35,y+20)], fill=color)
    elif kind == "space":
        d.ellipse((x+17,y+18,x+29,y+30), outline=color, width=4)
        d.arc((x+3,y+8,x+29,y+32), 210, 315, fill=color, width=4)
        d.arc((x+1,y+4,x+26,y+30), 220, 300, fill=color, width=4)
        d.arc((x+2,y+0,x+30,y+29), 225, 300, fill=color, width=4)
        d.line((x+3,y+34,x+39,y+4), fill=color, width=4)
        d.polygon([(x+39,y+4),(x+30,y+6),(x+37,y+13)], fill=color)
    elif kind == "games":
        d.rounded_rectangle((x+2,y+13,x+40,y+35), radius=7, outline=color, width=5)
        d.line((x+12,y+20,x+12,y+29), fill=color, width=4); d.line((x+8,y+24,x+16,y+24), fill=color, width=4)
        d.ellipse((x+27,y+20,x+31,y+24), fill=color); d.ellipse((x+33,y+26,x+37,y+30), fill=color)
    else:
        d.polygon([(x+5,y+24),(x+37,y+24),(x+31,y+31),(x+11,y+31)], outline=color)
        d.line((x+21,y+24,x+21,y+8), fill=color, width=4)
        d.polygon([(x+22,y+9),(x+34,y+21),(x+22,y+21)], outline=color)
        d.arc((x+1,y+29,x+20,y+39), 0, 180, fill=color, width=4)
        d.arc((x+20,y+29,x+40,y+39), 0, 180, fill=color, width=4)
        d.arc((x+10,y+31,x+30,y+41), 0, 180, fill=color, width=4)

for i, (chip, accent, headline, desc, kind) in enumerate(cards):
    col, row = i % 2, i // 2
    x = left if col == 0 else right
    y = ys[row]
    d.rounded_rectangle((x, y, x+cw, y+ch), radius=8, fill="#fffefa", outline="#d7d0c4", width=2)
    d.rectangle((x+2, y+12, x+6, y+ch-12), fill=accent)
    chip_font = font(BOLD, 13)
    chip_w = int(d.textbbox((0, 0), chip, font=chip_font)[2]) + 18
    d.rounded_rectangle((x+14, y+10, x+14+chip_w, y+36), radius=5, fill=accent)
    d.text((x+22, y+13), chip, font=chip_font, fill="#ffffff")
    icon(kind, x+cw-53, y+45, accent)
    tx, maxw = x+26, cw-79
    hy = y+43
    hfont = None
    for size in (28, 27, 26, 25, 24, 23, 22):
        candidate = font(BOLD, size)
        lines = wrap(headline, candidate, maxw)
        line_leading = int(size*1.04)
        headline_bottom = hy + max((i*line_leading + d.textbbox((0,0), line, font=candidate)[3]) for i,line in enumerate(lines))
        detail_y = headline_bottom + 7
        if len(lines) <= 3 and detail_y <= y+ch-10:
            hfont, hlines = candidate, lines
            break
    if hfont is None:
        hfont, hlines = fit_lines(headline, BOLD, 22, 22, maxw, 3)
    hy = draw_lines(hlines, hfont, tx, hy, INK, int(hfont.size*1.04))
    line_leading = int(hfont.size*1.04)
    headline_bottom = (y+43) + max((i*line_leading + d.textbbox((0,0), line, font=hfont)[3]) for i,line in enumerate(hlines))
    body_y = headline_bottom + 7
    bfont, blines = None, None
    for size in (22, 21, 20, 19, 18):
        candidate = font(REG, size)
        lines = wrap(desc, candidate, cw-43)
        leading = int(size*1.13)
        text_bottom = body_y + (len(lines)-1)*leading + d.textbbox((0, 0), "Ag", font=candidate)[3]
        if len(lines) <= 3 and text_bottom <= y+ch-10:
            bfont, blines = candidate, lines
            break
    if bfont is None:
        bfont, blines = fit_lines(desc, REG, 18, 18, cw-34, 3)
    draw_lines(blines, bfont, tx, body_y, "#2c3844", int(bfont.size*1.13))

# Footer
d.rectangle((0, 968, W, H), fill=NAVY)
d.text((28, 984), "19 NOVEMBER 2026 — ONE DAY OF WORLD NEWS", font=font(BOLD, 17), fill="#ffffff")
footer = "Compiled from the day's reporting"
fw = d.textbbox((0,0), footer, font=font(REG, 15))[2]
d.text((W-28-fw, 986), footer, font=font(REG, 15), fill="#ffffff")

out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", str(os.path.dirname(os.path.abspath(__file__))))
os.makedirs(out_dir, exist_ok=True)
im.save(os.path.join(out_dir, "entry.png"), format="PNG", optimize=True)
