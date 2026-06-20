#!/usr/bin/env python3
"""Check SVG text for overflow beyond card boundaries.

Industry-facts / supply-profit info cards have a strict 340px usable width
(420px card - 40px padding on each side). This script flags text exceeding that.

Usage: python3 bin/check_svg_overflow.py [SVG files...]
Exit code: 0 = all clear, 1 = overflow found
"""
import sys
import re
import glob

# Chinese char ≈ 1 width unit, ASCII ≈ 0.55
def w(text):
    return sum(1 if ord(c) > 127 else 0.55 for c in text)

# Card text positions and their max pixel widths
# Industry-facts cards: x=130 (left column), x=610 (right column), usable=340
# Supply-profit flow chain: centered x=540 in 740px blocks
CHECKS = [
    # (x, y-min, y-max, max-width, label)
    # Industry-facts cards: left col (card x=90), right col (card x=570)
    # Internal padding 40px each side → usable width = 340px
    (130, 350, 1300, 340, "卡片左列"),
    (610, 350, 1300, 340, "卡片右列"),
]

def check_file(path):
    with open(path) as f:
        content = f.read()

    errors = []
    pat = re.compile(
        r'<text\s[^>]*x="(\d+)"[^>]*y="(\d+)"[^>]*font-size="(\d+)"[^>]*>'
        r'([^<]+)</text>'
    )

    for match in pat.finditer(content):
        x = int(match.group(1))
        y = int(match.group(2))
        fs = int(match.group(3))
        text = match.group(4)

        pw = w(text) * fs

        for cx, ymin, ymax, limit, label in CHECKS:
            if x == cx and ymin <= y <= ymax:
                if pw > limit:
                    errors.append(f"  y={y} fs={fs} +{pw-limit:.0f}px  [{label}]  {text}")

    return errors


def main():
    files = sys.argv[1:]
    if not files:
        files = glob.glob("/Users/ennio/Documents/AI_work/rednote/assets/*.svg")

    has_errors = False
    for path in sorted(files):
        if not path.endswith('.svg'):
            continue
        errors = check_file(path)
        if errors:
            print(f"\033[31m{path.split('/')[-1]}:\033[0m")
            for e in errors:
                print(f"  \033[33m⚠️  {e}\033[0m")
            has_errors = True

    if has_errors:
        print("\n❌ Overflow detected — fix before converting to PNG")
        sys.exit(1)
    else:
        print("✅ All SVG text within bounds")


if __name__ == "__main__":
    main()
