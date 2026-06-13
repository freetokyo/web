#!/usr/bin/env python3
"""ケイヒバ OGP 画像（1200×630）。ブランド配色（ティール）+ レシート/チェックモチーフ + タイトル。"""
import os
from PIL import Image, ImageDraw, ImageFont

TEAL = (0x2C, 0x7A, 0x78)
NAVY = (0x14, 0x3C, 0x3A)
WHITE = (0xFF, 0xFF, 0xFF)
INK = (0xD8, 0xE8, 0xE6)
W, H = 1200, 630
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "og-image.png")

FONT_CANDIDATES = [
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
]


def font(size):
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def make():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)
    d.polygon([(0, 0), (W, 0), (W, H)], fill=TEAL)

    # 左側にレシートモチーフ（白・下辺ギザギザ）。
    rx0, ry0, rx1, ry1 = 110, 130, 360, 470
    d.rounded_rectangle([rx0, ry0, rx1, ry1 - 26], radius=18, fill=WHITE)
    teeth = 7
    tw = (rx1 - rx0) / teeth
    base = ry1 - 26
    for i in range(teeth):
        x = rx0 + i * tw
        d.polygon([(x, base), (x + tw, base), (x + tw / 2, base + 26)], fill=WHITE)
    for i, y in enumerate(range(ry0 + 50, base - 36, 46)):
        w = rx1 - 40 if i % 2 == 0 else rx1 - 96
        d.rounded_rectangle([rx0 + 30, y, w, y + 12], radius=6, fill=INK)
    # チェックバッジ
    cx, cy, r = 350, 430, 70
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=TEAL, outline=WHITE, width=10)
    d.line([(cx - 30, cy + 2), (cx - 6, cy + 26), (cx + 34, cy - 26)], fill=WHITE, width=18, joint="curve")

    # 右側にタイトル。
    tx = 470
    d.text((tx, 200), "ケイヒバ", font=font(96), fill=WHITE)
    d.text((tx, 330), "経費レシート整理", font=font(46), fill=WHITE)
    d.text((tx, 410), "撮るだけ・端末内完結・買い切り", font=font(28), fill=INK)

    img.save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    make()
