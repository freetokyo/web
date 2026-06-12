#!/usr/bin/env python3
"""sitemap.xml を生成（JA ルート + 生成済みロケール配下の4ページ）。
Trero web/scripts/gen_sitemap.py を Jitsuhiro 用にスラッグ変更したもの。"""
import os

BASE_URL = "https://freetokyo.github.io/web/jitsuhiro"
WEB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGES = ["", "support.html", "privacy.html", "terms.html"]  # "" = index

# 生成済みロケール（web/<lang>/ が存在するもの）を自動検出。ja はルート。
def locales():
    out = ["ja"]
    for name in sorted(os.listdir(WEB)):
        p = os.path.join(WEB, name)
        if os.path.isdir(p) and os.path.exists(os.path.join(p, "index.html")) and name not in ("scripts", "translations"):
            out.append(name)
    return out


def url_for(lang, page):
    if lang == "ja":
        return f"{BASE_URL}/{page}" if page else f"{BASE_URL}/"
    return f"{BASE_URL}/{lang}/{page}" if page else f"{BASE_URL}/{lang}/"


def main():
    rows = []
    for lang in locales():
        for page in PAGES:
            rows.append(f"  <url><loc>{url_for(lang, page)}</loc></url>")
    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    with open(os.path.join(WEB, "sitemap.xml"), "w") as f:
        f.write(xml)
    print("wrote sitemap.xml with", len(rows), "urls")


if __name__ == "__main__":
    main()
