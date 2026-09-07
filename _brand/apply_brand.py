#!/usr/bin/env python3
"""_brand/brand.json を web/ 配下の全ファイルへ反映する。

brand.json がブランド名・連絡先・サイト URL の唯一の真実源で、このスクリプトはそれを
静的ファイルへ配る係。出力は静的 HTML のままなので、OGP クローラや検索
エンジン（JS を実行しない）にもそのまま届く。

    python3 _brand/apply_brand.py            # 差分を見るだけ（既定・書かない）
    python3 _brand/apply_brand.py --apply    # 書き込む
    python3 _brand/apply_brand.py -v         # ファイルごとの内訳も出す

冪等。--apply を二度流しても二度目は 0 件になる。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BRAND_DIR = Path(__file__).resolve().parent
WEB_ROOT = BRAND_DIR.parent
BRAND_JSON = BRAND_DIR / "brand.json"

# 中身がテキストで、ブランド名や連絡先が載りうるもの。
TARGET_SUFFIXES = {".html", ".htm", ".json", ".js", ".txt", ".py", ".xml", ".css", ".md"}

# 触らない場所。_brand 自身を含めるのは、brand.json の previous_* が
# 置換されて履歴が消えるのを防ぐため。
SKIP_DIRS = {".git", "node_modules", ".github", "_brand"}


class Rule:
    """旧表記 → 現行表記のひとつの置き換え。"""

    def __init__(self, label: str, old: str, new: str, is_regex: bool = False):
        self.label = label
        self.old = old
        self.new = new
        self.is_regex = is_regex
        if is_regex:
            # 正規表現は書いたとおりに当てる。大小を無視すると、置換後の
            # 表記（Freetokyo Labs）に自分で再マッチして冪等性が壊れる。
            self.pattern = re.compile(old)
        else:
            # 文字列は大小の揺れ（Freetokyo Apps / freetokyo apps）も拾って正規化する。
            self.pattern = re.compile(re.escape(old), re.IGNORECASE)

    def apply(self, text: str) -> tuple[str, int]:
        return self.pattern.subn(self.new, text)


def load_rules() -> list[Rule]:
    try:
        cfg = json.loads(BRAND_JSON.read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"brand.json が見つからない: {BRAND_JSON}")
    except json.JSONDecodeError as e:
        sys.exit(f"brand.json が壊れている: {e}")

    rules: list[Rule] = []

    def add(label: str, current: str, olds: list[str], where: str, is_regex: bool = False) -> None:
        for old in olds:
            if is_regex:
                try:
                    re.compile(old)
                except re.error as e:
                    sys.exit(f"brand.json の {where} の正規表現が壊れている: {old!r} — {e}")
                rules.append(Rule(label, old, current, is_regex=True))
                continue
            if old.lower() == current.lower():
                # 自己置換は無限に自分を書き換え続けるので設定ミスとして止める。
                sys.exit(
                    f"brand.json の {where} に現行値 '{current}' が入っている。"
                    " previous_* / from には旧い値だけを入れる。"
                )
            rules.append(Rule(label, old, current))

    # 名前付きセクション。current が空なら設定ミスとして止める。
    for section, current_key, previous_key, label in (
        ("brand", "name", "previous_names", "ブランド名"),
        ("contact", "email", "previous_emails", "連絡先"),
        ("site", "url", "previous_urls", "サイトURL"),
    ):
        block = cfg.get(section, {})
        current = block.get(current_key)
        if not current:
            sys.exit(f"brand.json の {section}.{current_key} が空")
        add(label, current, block.get(previous_key, []), f"{section}.{previous_key}")

    # 名前付きセクションで表せない置き換え（パーセントエンコードされた URL など）。
    for extra in cfg.get("extra_replacements", []):
        if "to" not in extra:
            sys.exit("extra_replacements に to が無い項目がある")
        to = extra["to"]  # 空文字は「その表現を消す」の意味なので許す
        label = extra.get("label", "その他")
        add(label, to, extra.get("from", []), "extra_replacements.from")
        add(label, to, extra.get("from_regex", []), "extra_replacements.from_regex", is_regex=True)

    if not rules:
        sys.exit("置換ルールが 0 件。brand.json の previous_* が空。")

    # 文字列を長い順に当ててから、広く拾う正規表現を最後に回す。
    # 短い値が長い値の一部を食う事故と、正規表現が個別ルールを先取りする事故を防ぐ。
    rules.sort(key=lambda r: (r.is_regex, -len(r.old)))
    return rules


def iter_targets():
    for path in sorted(WEB_ROOT.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in TARGET_SUFFIXES:
            continue
        if SKIP_DIRS & set(path.relative_to(WEB_ROOT).parts):
            continue
        yield path


def main() -> int:
    ap = argparse.ArgumentParser(description="brand.json を web/ 配下へ反映する")
    ap.add_argument("--apply", action="store_true", help="実際に書き込む（既定は確認のみ）")
    ap.add_argument("-v", "--verbose", action="store_true", help="ファイルごとの内訳を出す")
    args = ap.parse_args()

    rules = load_rules()
    print(f"真実源: {BRAND_JSON.relative_to(WEB_ROOT.parent)}")
    for r in rules:
        print(f"  [{r.label}] {r.old!r} → {r.new!r}")
    print()

    changed_files = 0
    scanned = 0
    per_rule: dict[str, int] = {}

    for path in iter_targets():
        scanned += 1
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"  ! UTF-8 で読めないので飛ばす: {path.relative_to(WEB_ROOT)}", file=sys.stderr)
            continue

        text = original
        hits: dict[str, int] = {}
        for rule in rules:
            text, n = rule.apply(text)
            if n:
                hits[rule.old] = hits.get(rule.old, 0) + n
                per_rule[rule.old] = per_rule.get(rule.old, 0) + n

        if text == original:
            continue

        changed_files += 1
        if args.verbose:
            detail = ", ".join(f"{k} ×{v}" for k, v in hits.items())
            print(f"  {path.relative_to(WEB_ROOT)}: {detail}")
        if args.apply:
            path.write_text(text, encoding="utf-8")

    total = sum(per_rule.values())
    print()
    print(f"走査 {scanned} ファイル / 該当 {changed_files} ファイル / 置換 {total} 箇所")
    for old, n in sorted(per_rule.items(), key=lambda kv: -kv[1]):
        print(f"  {old}: {n}")

    if not args.apply:
        print()
        if total:
            print("確認のみ。書き込むには --apply を付ける。")
            return 1
        print("ズレなし。全ファイルが brand.json と一致している。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
