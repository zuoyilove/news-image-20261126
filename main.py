#!/usr/bin/env python3
"""news-image-20261126: draw a one-page newspaper front page for
Thursday 26 November 2026 and write it to /output/entry.png.

Everything is drawn with Pillow from the story list baked into this
file: masthead, a drawn market-crash hero chart, the lead markets
story, a 2x2 grid of the day's other big stories, and a navy ticker
band. No network, no outside files. Output is a deterministic
1024x1024 palette PNG under 1 MiB.
"""

import os
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 20
CONTENT_W = W - 2 * MARGIN

PAPER = (248, 244, 236)
INK = (18, 18, 18)
RULE = (120, 110, 95)
RED = (178, 34, 28)
NAVY = (16, 35, 63)
NAVY_DARK = (10, 24, 46)
MUTED = (90, 84, 72)
WHITE = (255, 255, 255)
HERO_BG_TOP = (22, 42, 74)
HERO_BG_BOTTOM = (10, 22, 44)

DATE_LINE = "THURSDAY 26 NOVEMBER 2026"
MASTHEAD = "THE WORLD TODAY"

LEAD_KICKER = "MARKETS"
LEAD_HEADLINE = "WALL STREET TUMBLES ON TARIFF THREAT"
LEAD_DECK = (
    "Nasdaq -3.1%, S&P 500 -2.5%, Nvidia -8.7% -- Washington proposes "
    "Section 301 tariffs on 14 trade partners, up to 45% on some "
    "Chinese goods."
)

STORIES = [
    (
        "satellite",
        "SPACEX CLEARED FOR A MILLION SATELLITES",
        "The FCC approves SpaceX's Starmind constellation, an orbital "
        "AI data-centre network and a first for the United States.",
    ),
    (
        "station",
        "PAKISTAN'S FIRST ASTRONAUT REACHES TIANGONG",
        "Shenzhou-24 docks with China's space station. Zeeshan Ali is "
        "the first foreign astronaut aboard Tiangong.",
    ),
    (
        "flame",
        "CAIRO TANKER FIRE KILLS 31",
        "A fuel tanker overturns and catches fire on the Ring Road. "
        "Twenty-one people are injured.",
    ),
    (
        "islands",
        "AUSTRALIA SIGNS SOLOMONS SECURITY PACT",
        "Canberra seals a security deal with Solomon Islands, seen as "
        "a check on China's influence in the Pacific.",
    ),
]

TICKER = (
    "COLOMBIA FREES 25 HOSTAGES  |  US JOBLESS CLAIMS 189,000  |  EU "
    "FINES PERFUME CARTEL EUR 471.9M  |  N. KOREA EXPELS SWISS DIPLOMAT "
    " |  BANGLADESH PAY UP 36%  |  US THANKSGIVING TRAVEL CHAOS"
)

FONT_PATHS = {
    "serif_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    ],
    "sans_bold": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ],
    "sans": [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    ],
}


def load_font(kind, size):
    """First usable font file wins; fall back to Pillow's built-in font."""
    for path in FONT_PATHS[kind]:
        try:
            return ImageFont.truetype(path, size)
        except (OSError, IOError):
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def text_width(font, text):
    return font.getlength(text)


def wrap_text(draw, text, font, max_width):
    """Greedy word wrap; returns a list of lines that fit max_width."""
    lines, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if text_width(font, trial) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_centered(draw, cx, y, text, font, fill):
    w = text_width(font, text)
    draw.text((cx - w / 2, y), text, font=font, fill=fill)
    return font.getbbox(text)[3]


def draw_tracked(draw, cx, y, text, font, fill, tracking):
    """Draw text with extra space between letters, centred on cx."""
    widths = [font.getlength(ch) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = cx - total / 2
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += w + tracking
    return font.getbbox(text)[3]


def draw_rule(draw, x0, x1, y, fill=RULE, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_hero(draw, x, y, w, h):
    """Stylised market-crash chart: dark panel, falling red candles."""
    for i in range(h):
        t = i / max(h - 1, 1)
        r = int(HERO_BG_TOP[0] + (HERO_BG_BOTTOM[0] - HERO_BG_TOP[0]) * t)
        g = int(HERO_BG_TOP[1] + (HERO_BG_BOTTOM[1] - HERO_BG_TOP[1]) * t)
        b = int(HERO_BG_TOP[2] + (HERO_BG_BOTTOM[2] - HERO_BG_TOP[2]) * t)
        draw.line([(x, y + i), (x + w, y + i)], fill=(r, g, b))
    for gy in range(y + 30, y + h - 10, 42):
        draw.line([(x + 8, gy), (x + w - 8, gy)], fill=(58, 82, 120), width=1)
    rng = random.Random(20261126)
    n = 26
    step = (w - 60) / n
    tops = []
    for i in range(n):
        cx = x + 30 + i * step + step / 2
        price = 0.06 + (i / (n - 1)) * 0.62 + rng.uniform(-0.03, 0.03)
        price = max(0.05, min(0.92, price))
        top = y + 22 + price * (h - 70)
        body_h = rng.uniform(14, 34)
        wick_top = top - rng.uniform(4, 14)
        wick_bot = top + body_h + rng.uniform(4, 14)
        draw.line([(cx, wick_top), (cx, wick_bot)], fill=(150, 60, 50), width=2)
        draw.rectangle(
            [cx - step * 0.28, top, cx + step * 0.28, top + body_h],
            fill=(214, 61, 42),
        )
        tops.append((cx, top))
    draw.line(tops, fill=(255, 92, 74), width=4)
    ex, ey = tops[-1]
    draw.polygon(
        [(ex, ey + 12), (ex - 16, ey - 4), (ex + 2, ey - 2)],
        fill=(255, 92, 74),
    )
    draw.rectangle([x, y, x + w - 1, y + h - 1], outline=(8, 18, 38), width=2)


def draw_satellite(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY_DARK)
    rng = random.Random(7)
    for _ in range(26):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, h - 4)
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=WHITE)
    draw.rectangle([x + 18, y + 62, x + 58, y + 88], fill=(46, 92, 158))
    draw.rectangle([x + 66, y + 58, x + 94, y + 92], fill=(198, 202, 208))
    draw.rectangle([x + 102, y + 62, x + 142, y + 88], fill=(46, 92, 158))
    draw.line([(x + 80, y + 58), (x + 80, y + 34)], fill=(198, 202, 208), width=3)
    draw.ellipse([x + 74, y + 26, x + 86, y + 38], outline=(255, 205, 80), width=3)


def draw_station(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=NAVY_DARK)
    rng = random.Random(11)
    for _ in range(22):
        sx = x + rng.randint(4, w - 4)
        sy = y + rng.randint(4, h - 40)
        draw.ellipse([sx, sy, sx + 2, sy + 2], fill=WHITE)
    draw.ellipse([x - 55, y + 78, x + 205, y + 250], fill=(38, 92, 148))
    draw.ellipse([x - 55, y + 78, x + 205, y + 250], outline=(120, 180, 230), width=2)
    draw.rectangle([x + 52, y + 46, x + 98, y + 62], fill=(210, 214, 220))
    draw.rectangle([x + 18, y + 50, x + 52, y + 58], fill=(46, 92, 158))
    draw.rectangle([x + 98, y + 50, x + 132, y + 58], fill=(46, 92, 158))
    draw.ellipse([x + 68, y + 30, x + 82, y + 44], fill=(255, 205, 80))


def draw_flame(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(26, 20, 18))
    draw.rectangle([x + 22, y + 118, x + 128, y + 132], fill=(70, 70, 74))
    draw.ellipse([x + 34, y + 110, x + 46, y + 122], fill=(40, 40, 44))
    draw.ellipse([x + 104, y + 110, x + 116, y + 122], fill=(40, 40, 44))
    cx = x + w / 2
    draw.polygon(
        [
            (cx - 42, y + 118),
            (cx - 34, y + 66),
            (cx - 12, y + 88),
            (cx - 4, y + 34),
            (cx + 12, y + 72),
            (cx + 34, y + 52),
            (cx + 42, y + 118),
        ],
        fill=(232, 96, 24),
    )
    draw.polygon(
        [
            (cx - 22, y + 118),
            (cx - 16, y + 84),
            (cx - 2, y + 66),
            (cx + 12, y + 88),
            (cx + 22, y + 118),
        ],
        fill=(255, 196, 60),
    )


def draw_islands(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(28, 96, 150))
    draw.polygon(
        [(x + 22, y + 108), (x + 44, y + 66), (x + 66, y + 96), (x + 58, y + 122),
         (x + 34, y + 126)],
        fill=(66, 150, 90),
    )
    draw.polygon(
        [(x + 96, y + 52), (x + 118, y + 28), (x + 136, y + 48), (x + 128, y + 74),
         (x + 104, y + 72)],
        fill=(66, 150, 90),
    )
    for t in range(0, 101, 8):
        u = t / 100
        px = x + 52 + u * 62
        py = y + 108 - 52 * (4 * u * (1 - u)) - 18 * u
        draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=WHITE)
    draw.line([(x + 52, y + 108), (x + 52, y + 96)], fill=WHITE, width=2)
    draw.line([(x + 114, y + 52), (x + 114, y + 40)], fill=WHITE, width=2)


PANEL_DRAWERS = {
    "satellite": draw_satellite,
    "station": draw_station,
    "flame": draw_flame,
    "islands": draw_islands,
}


def build_image():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    masthead_font = load_font("serif_bold", 62)
    date_font = load_font("sans_bold", 21)
    kicker_font = load_font("sans_bold", 16)
    headline_font = load_font("serif_bold", 38)
    deck_font = load_font("sans", 20)
    story_head_font = load_font("sans_bold", 19)
    story_body_font = load_font("sans", 15)
    ticker_font = load_font("sans_bold", 16)

    y = 14
    draw_centered(draw, W / 2, y, MASTHEAD, masthead_font, INK)
    y += 78
    draw_rule(draw, MARGIN, W - MARGIN, y, fill=INK, width=3)
    y += 10
    draw_tracked(draw, W / 2, y, DATE_LINE, date_font, INK, tracking=4)
    y += 34
    draw_rule(draw, MARGIN, W - MARGIN, y, fill=INK, width=3)
    y += 12

    hero_h = 248
    draw_hero(draw, MARGIN, y, CONTENT_W, hero_h)
    y += hero_h + 16

    draw_centered(draw, W / 2, y, LEAD_KICKER, kicker_font, RED)
    y += 24
    draw_centered(draw, W / 2, y, LEAD_HEADLINE, headline_font, INK)
    y += 50
    deck_lines = wrap_text(draw, LEAD_DECK, deck_font, CONTENT_W)
    for line in deck_lines:
        draw_centered(draw, W / 2, y, line, deck_font, MUTED)
        y += 26
    y += 8
    draw_rule(draw, MARGIN, W - MARGIN, y, fill=INK, width=2)
    y += 14

    cell_w = (CONTENT_W - 16) // 2
    cell_h = 158
    pic_w, pic_h = 150, 150
    for row in range(2):
        for col in range(2):
            kind, head, body = STORIES[row * 2 + col]
            cx = MARGIN + col * (cell_w + 16)
            cy = y + row * (cell_h + 12)
            panel_img = Image.new("RGB", (pic_w, pic_h), PAPER)
            panel_draw = ImageDraw.Draw(panel_img)
            PANEL_DRAWERS[kind](panel_draw, 0, 0, pic_w, pic_h)
            img.paste(panel_img, (cx, cy))
            tx = cx + pic_w + 12
            tw = cell_w - pic_w - 12
            head_lines = wrap_text(draw, head, story_head_font, tw)
            hy = cy + 2
            for line in head_lines:
                draw.text((tx, hy), line, font=story_head_font, fill=INK)
                hy += 23
            body_lines = wrap_text(draw, body, story_body_font, tw)
            by = hy + 4
            for line in body_lines[:4]:
                draw.text((tx, by), line, font=story_body_font, fill=MUTED)
                by += 19
    y += 2 * cell_h + 12 + 8

    band_h = 62
    band_y = H - MARGIN - band_h
    draw.rectangle([MARGIN, band_y, W - MARGIN, band_y + band_h], fill=NAVY)
    ticker_lines = wrap_text(draw, TICKER, ticker_font, CONTENT_W - 24)
    ty = band_y + 8
    for line in ticker_lines[:2]:
        draw_centered(draw, W / 2, ty, line, ticker_font, WHITE)
        ty += 22

    footer_font = load_font("sans", 13)
    draw_centered(
        draw,
        W / 2,
        band_y + band_h + 6,
        "Sources: Reuters, AP, CNN, CNA, Dawn, Xinhua, WSJ, TechCrunch "
        "-- 26 November 2026",
        footer_font,
        MUTED,
    )

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    tmp_path = out_path + ".tmp"

    img = build_image()
    pal = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    pal.save(tmp_path, format="PNG", optimize=True)
    os.replace(tmp_path, out_path)

    with open(out_path, "rb") as fh:
        data = fh.read()
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "not a PNG"
    assert len(data) <= 1048576, "over 1 MiB"
    check = Image.open(out_path)
    assert check.size == (W, H), "wrong dimensions"
    import hashlib

    print(
        "wrote %s (%d bytes, %dx%d, sha256 %s)"
        % (out_path, len(data), W, H, hashlib.sha256(data).hexdigest())
    )


if __name__ == "__main__":
    main()
