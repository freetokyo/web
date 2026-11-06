#!/usr/bin/env python3
"""ブランドのロゴ素材を作る（2026-11-06 に「ft」のグラデーションから置き換えた）。

紺地に白の f と橙の点。Play デベロッパー アイコン（Console）と同じ絵で、Play は丸く切り抜く。
座標は 2048 四方。ナビの SVG（chrome.py の NAV_LOGO_SVG）も同じ値なので、形を変えるなら両方直す。

    python3 _brand/make_logo.py        # web/ 直下で。logo.png / favicon.* / apple-touch-icon.png / og-default.png

og-default.png の文字は言語を問わない 1 枚にするため英語だけ。本数は書かない（すぐ古くなる。
旧版は「iOS アプリ 64 本」のまま残っていた）。フォントは macOS の Helvetica Neue に依る。
"""
from PIL import Image, ImageDraw, ImageFont

NAVY, WHITE, ORANGE = (0x14, 0x1C, 0x40), (255, 255, 255), (0xFF, 0x9F, 0x0A)
S = 2048
HELV = "/System/Library/Fonts/HelveticaNeue.ttc"


def mark(bg=NAVY):
    im = Image.new("RGBA", (S, S), bg + (255,) if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    lw, x = 250, 900
    d.line((x, 1640, x, 760), fill=WHITE, width=lw)
    d.arc((x - lw // 2, 420, x - lw // 2 + 760, 1180), start=180, end=300, fill=WHITE, width=lw)
    d.ellipse((x - lw // 2, 1640 - lw // 2, x + lw // 2, 1640 + lw // 2), fill=WHITE)
    d.ellipse((1282 - 125, 579 - 125, 1282 + 125, 579 + 125), fill=WHITE)
    d.line((640, 1000, 1190, 1000), fill=WHITE, width=210)
    for px in (640, 1190):
        d.ellipse((px - 105, 895, px + 105, 1105), fill=WHITE)
    d.ellipse((1330, 1330, 1630, 1630), fill=ORANGE)
    return im


def circle(im):
    m = Image.new("L", (S, S), 0)
    ImageDraw.Draw(m).ellipse((0, 0, S - 1, S - 1), fill=255)
    out = im.copy()
    out.putalpha(m)
    return out


sq = mark()
sq.convert("RGB").resize((512, 512), Image.LANCZOS).save("logo.png")
# iOS は角を自分で丸めるので全面を塗る（透過は黒く潰れる）
sq.convert("RGB").resize((180, 180), Image.LANCZOS).save("apple-touch-icon.png")
circle(sq).resize((256, 256), Image.LANCZOS).save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])

W, H = 1200, 630
og = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(og)
k = mark(None).resize((300, 300), Image.LANCZOS)
og.paste(k, (70, 165), k)
d.text((380, 232), "Freetokyo Labs", font=ImageFont.truetype(HELV, 92, index=1), fill=WHITE)
d.text((384, 346), "Small tools for health, life, money & work",
       font=ImageFont.truetype(HELV, 36, index=0), fill=(0xC9, 0xD1, 0xE8))
og.save("og-default.png", optimize=True)
