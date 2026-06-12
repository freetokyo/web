#!/usr/bin/env python3
"""ジツヒロ OGP 画像（1200×630）。ブランド配色 + アイコンモチーフ + タイトル。"""
import os
from PIL import Image, ImageDraw, ImageFont

BLUEPRINT = (0x22, 0x57, 0xA5)
NAVY = (0x16, 0x36, 0x5C)
PILLAR_RED = (0xE5, 0x48, 0x4D)
WHITE = (0xFF, 0xFF, 0xFF)
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
    # 右下に向かう斜めグラデーション風の帯。
    d.rectangle([0, 0, W, H], fill=NAVY)
    d.polygon([(0, 0), (W, 0), (W, H)], fill=BLUEPRINT)

    # 左側にアイコンモチーフ（部屋コーナー + 柱 + 寸法線）。
    ox, oy, t = 90, 150, 46
    x1, y1 = 90 + 320, 150 + 320
    d.rectangle([ox, oy, x1, oy + t], fill=WHITE)
    d.rectangle([ox, oy, ox + t, y1], fill=WHITE)
    d.rectangle([ox + t, oy + t, ox + t + 130, oy + t + 130], fill=PILLAR_RED)
    # 寸法線
    ly = 150 + 360
    d.rectangle([ox, ly - 6, x1, ly + 6], fill=WHITE)
    d.rectangle([ox, ly - 26, ox + 12, ly + 26], fill=WHITE)
    d.rectangle([x1 - 12, ly - 26, x1, ly + 26], fill=WHITE)

    # 右側にタイトル。
    tx = 520
    d.text((tx, 210), "ジツヒロ", font=font(96), fill=WHITE)
    d.text((tx, 330), "間取り図の本当の広さ", font=font(46), fill=WHITE)
    d.text((tx, 396), "チェッカー", font=font(46), fill=WHITE)
    d.text((tx, 470), "柱を引いた純・有効面積と帖数差／動線検証", font=font(28), fill=(0xD8, 0xE4, 0xF2))

    img.save(OUT, "PNG")
    print("wrote", OUT)


if __name__ == "__main__":
    make()
