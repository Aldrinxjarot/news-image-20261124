#!/usr/bin/env python3
"""Draw the front page for Tuesday, 24 November 2026.

Build-time only: running this program renders entry.png, the image
the entry submits. Everything on the page -- masthead, headlines,
standfirst, panels, the markets chart and the ticker -- is drawn
here with Pillow; no photograph or outside artwork is used.

Every story was checked against wire-style coverage dated Tuesday
24 November 2026 before it was drawn; NOTES.md keeps the source and
dateline for each one, and the list of stories checked and dropped
as earlier days' news.
"""

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024
MARGIN = 48
CONTENT_W = W - 2 * MARGIN

PAPER = (248, 244, 233)
INK = (24, 22, 20)
MUTED = (96, 90, 82)
ACCENT = (163, 22, 33)
RULE = (60, 56, 50)
DOWN = (176, 44, 32)
UP = (24, 122, 66)
BAND = (24, 22, 20)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_ITALIC = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit(draw, text, path, size, max_w):
    """Largest size at or below `size` that keeps `text` in `max_w`."""
    while size > 10:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_w:
            return f
        size -= 1
    return font(path, size)


def wrap(draw, text, f, max_w):
    """Split `text` into lines that fit `max_w` in font `f`."""
    lines = []
    current = ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if draw.textlength(trial, font=f) <= max_w:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_wrapped(draw, text, f, x, y, max_w, leading, fill=INK):
    for line in wrap(draw, text, f, max_w):
        draw.text((x, y), line, font=f, fill=fill)
        y += leading
    return y


def centered(draw, text, f, y, fill=INK):
    w = draw.textlength(text, font=f)
    draw.text(((W - w) / 2, y), text, font=f, fill=fill)


def rule(draw, y, weight=2):
    draw.line([(MARGIN, y), (W - MARGIN, y)], fill=RULE, width=weight)


def panel(draw, x, y, w, kicker, headline, body):
    """One news panel: kicker, headline, body. Returns bottom y."""
    kf = font(SANS_BOLD, 17)
    draw.text((x, y), kicker, font=kf, fill=ACCENT)
    y += 26
    hf = fit(draw, headline, SERIF_BOLD, 27, w)
    draw.text((x, y), headline, font=hf, fill=INK)
    y += 38
    bf = font(SERIF, 19)
    y = draw_wrapped(draw, body, bf, x, y, w, 25)
    return y


def chart(draw, x, y, w):
    """Tuesday's closing moves as horizontal bars (Reuters)."""
    rows = [
        ("DOW", 0.9),
        ("S&P 500", -0.5),
        ("NASDAQ", -1.5),
        ("NVIDIA", -6.0),
    ]
    draw.rectangle([x, y, x + w, y + 196], outline=RULE, width=2)
    tf = font(SANS_BOLD, 17)
    draw.text((x + 14, y + 10), "TUESDAY'S CLOSE", font=tf, fill=INK)
    zero_x = x + 180
    scale = 15  # pixels per percentage point
    draw.line([(zero_x, y + 42), (zero_x, y + 178)], fill=MUTED, width=1)
    lf = font(SANS_BOLD, 16)
    vf = font(SANS, 16)
    row_y = y + 48
    for name, pct in rows:
        draw.text((x + 14, row_y), name, font=lf, fill=INK)
        x2 = zero_x + pct * scale
        colour = UP if pct > 0 else DOWN
        draw.rectangle([min(zero_x, x2), row_y + 2, max(zero_x, x2), row_y + 15],
                       fill=colour)
        label = "%+.1f%%" % pct
        # Positive values sit past the bar's end; negative ones sit
        # just right of the zero line, clear of both bar and name.
        lx = x2 + 8 if pct > 0 else zero_x + 8
        draw.text((lx, row_y), label, font=vf, fill=INK)
        row_y += 33
    return y + 196


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # Masthead
    rule(draw, 30, 3)
    rule(draw, 38, 1)
    mf = fit(draw, "THE WORLD IN ONE DAY", SERIF_BOLD, 63, CONTENT_W)
    centered(draw, "THE WORLD IN ONE DAY", mf, 52)
    df = font(SANS_BOLD, 27)
    centered(draw, "Tuesday, 24 November 2026", df, 132)
    rule(draw, 172, 2)

    # Hero: Nvidia
    y = 188
    kf = font(SANS_BOLD, 18)
    draw.text((MARGIN, y), "MARKETS  ·  THE DAY AFTER THE SHOCK RETURN", font=kf,
              fill=ACCENT)
    y += 32
    hf = font(SERIF_BOLD, 55)
    for line in ("NVIDIA BOUNCE FADES", "AS HUANG RALLY COOLS"):
        f = fit(draw, line, SERIF_BOLD, 55, CONTENT_W)
        draw.text((MARGIN, y), line, font=f, fill=INK)
        y += 64
    y += 6
    standfirst = (
        "The relief rally over Jensen Huang's return as Nvidia's chief "
        "executive ran out of steam on Tuesday: the chipmaker slid 6% "
        "and the Nasdaq fell 1.5%, while Congress prepared to question "
        "the boss who quit on 12 November and was brought back after "
        "President Trump intervened."
    )
    sf = font(SERIF_ITALIC, 23)
    text_w = 580
    draw_wrapped(draw, standfirst, sf, MARGIN, y, text_w, 30)
    chart(draw, MARGIN + text_w + 28, y, CONTENT_W - text_w - 28)
    y += 196 + 10

    rule(draw, y, 2)
    y += 18

    # Panels, row 1
    col_w = (CONTENT_W - 28) // 2
    x2 = MARGIN + col_w + 28
    panel(draw, MARGIN, y, col_w, "CHINA  ·  COURTS",
          "HUAWEI CONVICTED IN U.S. TRIAL",
          "A federal jury on Tuesday convicted the Chinese tech giant "
          "of deceiving banks about its business in Iran and of "
          "stealing trade secrets from U.S. companies, in a sprawling "
          "criminal case years in the making. (Reuters)")
    panel(draw, x2, y, col_w, "BUSINESS  ·  PHARMA",
          "SANOFI BUYS INSMED FOR $41BN",
          "France's Sanofi said in Paris on Tuesday it will buy the "
          "U.S. biotech for $175 a share in cash -- the year's biggest "
          "pharma deal -- gaining two first-in-disease respiratory "
          "medicines and a phase 3 pipeline.")
    y += 205

    # Panels, row 2
    panel(draw, MARGIN, y, col_w, "ISRAEL  ·  POLITICS",
          "EISENKOT SEALS FIRST PACT",
          "Former military chief Gadi Eisenkot's Yashar party signed "
          "its first coalition agreement on Tuesday, with Lieberman's "
          "Israel Our Home. He has until 6 December to form a "
          "government. (Reuters)")
    panel(draw, x2, y, col_w, "UKRAINE  ·  WAR",
          "OVERNIGHT HIT ON ZAPORIZHZHIA",
          "An overnight Russian attack killed two people and wounded "
          "dozens -- among them four children -- striking an apartment "
          "building, the regional governor said on Tuesday.")

    # Ticker
    band_y = 970
    draw.rectangle([0, band_y, W, H], fill=BAND)
    tf = font(SANS_BOLD, 16)
    draw.text((MARGIN, band_y + 9), "ALSO TODAY", font=tf, fill=(255, 214, 120))
    ticker = (
        "U.S. consumer confidence hits 103.3, a near two-year high  ·  "
        "Israeli strikes kill at least six in Gaza  ·  Bangladesh "
        "garment workers clash with police  ·  175 migrants missing "
        "off Senegal"
    )
    bf = font(SANS, 16)
    draw_wrapped(draw, ticker, bf, MARGIN + 130, band_y + 9,
                 CONTENT_W - 130, 20, fill=(245, 242, 235))

    img.save("entry.png", optimize=True)
    print("wrote entry.png")


if __name__ == "__main__":
    main()
