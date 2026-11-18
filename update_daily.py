#!/usr/bin/env python3
"""毎朝の星読みJSONを公式HPの daily セクションへ埋め込む。"""
import html, json, re, sys
from datetime import datetime
from zoneinfo import ZoneInfo

SITE = "/home/hatch/workspace/luna-hp-site/index.html"
CARD_DIR = "/home/hatch/workspace/luna-card"
GLYPHS = ["♈","♉","♊","♋","♌","♍","♎","♏","♐","♑","♒","♓"]

def build_block(d):
    rows = []
    for i, s in enumerate(d["signs"]):
        g = GLYPHS[i] if i < len(GLYPHS) else "✦"
        rows.append(
            f'<li><span class="daily-glyph" aria-hidden="true">{g}</span>'
            f'<span class="daily-name">{html.escape(s["name"])}</span>'
            f'<span class="daily-text">{html.escape(s["text"])}</span></li>')
    return (
        f'<p class="daily-date">{html.escape(d["date_label"])}の星読み</p>\n'
        f'<p class="daily-intro">{html.escape(d.get("intro", ""))}</p>\n'
        f'<ul class="daily-list">\n' + "\n".join(rows) + '\n</ul>\n'
        f'<p class="daily-advice"><span>✦ 星の助言</span>{html.escape(d.get("lucky_action", ""))}</p>')

def main():
    day = sys.argv[1] if len(sys.argv) > 1 else datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d")
    try:
        d = json.load(open(f"{CARD_DIR}/{day}.json", encoding="utf-8"))
    except FileNotFoundError:
        print(f"NO_JSON {day}")
        return 1
    src = open(SITE, encoding="utf-8").read()
    block = build_block(d)
    new, n = re.subn(r"<!--DAILY:START-->.*?<!--DAILY:END-->",
                     f"<!--DAILY:START-->\n{block}\n<!--DAILY:END-->", src, flags=re.S)
    if n != 1:
        print("MARKER_NOT_FOUND")
        return 1
    if new != src:
        open(SITE, "w", encoding="utf-8").write(new)
        print(f"UPDATED {day}")
    else:
        print(f"UNCHANGED {day}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
