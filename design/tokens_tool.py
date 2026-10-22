"""Design tokens helper (#7): validate design/tokens.json and export CSS variables.

Usage:
    python design/tokens_tool.py check   # required tokens + WCAG 2.1 contrast pairs
    python design/tokens_tool.py css     # write design/tokens.css (generated, do not edit)

Stdlib only. Exit code 1 if a check fails.
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOKENS = ROOT / "tokens.json"
CSS = ROOT / "tokens.css"

# Semantic names promised to frontend in issue #7, section 5.
REQUIRED = [
    "color.bg", "color.surface", "color.text", "color.risk", "color.opportunity",
    "color.neutral", "color.bank", "color.ai", "color.fact", "color.estimate",
    "color.focus", "color.danger", "radius.card", "space.4", "typography.body",
]

# (foreground, background, min ratio, where it is used). 4.5 = AA text, 3.0 = AA large text / UI.
CONTRAST = [
    ("color.text", "color.bg", 4.5, "основной текст на фоне"),
    ("color.text", "color.surface", 4.5, "основной текст в карточке"),
    ("color.text-secondary", "color.surface", 4.5, "подписи в карточке"),
    ("color.text-secondary", "color.bg", 4.5, "подписи на фоне"),
    ("color.text-tertiary", "color.surface", 4.5, "мета в карточке"),
    ("color.text-tertiary", "color.bg", 4.5, "мета на фоне"),
    ("color.text-tertiary", "color.surface-subtle", 4.5, "мета во вложенном блоке"),
    ("color.text-inverse", "color.action", 4.5, "текст primary-кнопки"),
    ("color.text-inverse", "color.action-hover", 4.5, "primary hover"),
    ("color.text-inverse", "color.surface-inverse", 4.5, "тост / tooltip"),
    ("color.link", "color.surface", 4.5, "ссылка"),
    ("color.risk", "color.risk-subtle", 4.5, "тег «Риск»"),
    ("color.opportunity", "color.opportunity-subtle", 4.5, "тег «Возможность»"),
    ("color.neutral", "color.neutral-subtle", 4.5, "тег «Нейтрально»"),
    ("color.fact", "color.fact-subtle", 4.5, "бейдж «Факт»"),
    ("color.bank", "color.bank-subtle", 4.5, "бейдж «Позиция банка»"),
    ("color.ai", "color.ai-subtle", 4.5, "бейдж «Вывод AI»"),
    ("color.estimate", "color.estimate-subtle", 4.5, "бейдж «Оценка»"),
    ("color.danger", "color.danger-subtle", 4.5, "ошибка"),
    ("color.info", "color.info-subtle", 4.5, "баннер демо-режима"),
    ("color.risk", "color.surface", 4.5, "текст риска в карточке"),
    ("color.opportunity", "color.surface", 4.5, "текст возможности в карточке"),
    ("color.accent", "color.surface", 3.0, "полоса банка, иконки (не текст)"),
    ("color.focus", "color.surface", 3.0, "кольцо фокуса на карточке"),
    ("color.focus", "color.bg", 3.0, "кольцо фокуса на фоне"),
    ("color.border-strong", "color.surface", 3.0, "рамка поля ввода"),
    ("color.meter-fill", "color.meter-track", 3.0, "шкала уверенности"),
]

ALIAS = re.compile(r"^\{([^}]+)\}$")


def flatten(node, path=(), inherited_type=None):
    """Yield (dotted name, token dict, $type) for every token in the tree."""
    group_type = node.get("$type", inherited_type)
    for key, value in node.items():
        if key.startswith("$") or not isinstance(value, dict):
            continue
        if "$value" in value:
            yield ".".join(path + (key,)), value, value.get("$type", group_type)
        else:
            yield from flatten(value, path + (key,), group_type)


def resolve(value, tokens, seen=()):
    if isinstance(value, str):
        match = ALIAS.match(value)
        if not match:
            return value
        name = match.group(1)
        if name in seen or name not in tokens:
            raise ValueError(f"bad alias {value!r}")
        return resolve(tokens[name][0]["$value"], tokens, seen + (name,))
    if isinstance(value, list):
        return [resolve(v, tokens, seen) for v in value]
    if isinstance(value, dict):
        return {k: resolve(v, tokens, seen) for k, v in value.items()}
    return value


def load():
    raw = json.loads(TOKENS.read_text(encoding="utf-8"))
    tokens = {name: (tok, typ) for name, tok, typ in flatten(raw)}
    return {name: (resolve(tok["$value"], tokens), typ) for name, (tok, typ) in tokens.items()}


def rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def luminance(hex_color):
    def channel(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (channel(c) for c in rgb(hex_color))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(fg, bg):
    hi, lo = sorted((luminance(fg), luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def check():
    tokens = load()
    failed = False
    for name in REQUIRED:
        if name not in tokens:
            print(f"MISSING  {name}")
            failed = True
    print(f"{'ratio':>6}  {'min':>4}  pair")
    for fg, bg, minimum, where in CONTRAST:
        value = ratio(tokens[fg][0], tokens[bg][0])
        ok = value >= minimum
        failed |= not ok
        print(f"{value:6.2f}  {minimum:4.1f}  {'ok  ' if ok else 'FAIL'} {fg} on {bg} — {where}")
    print("FAILED" if failed else f"OK: {len(tokens)} tokens, {len(CONTRAST)} contrast pairs")
    return 1 if failed else 0


def css_value(value, typ):
    if typ == "fontFamily":
        return ", ".join(f'"{f}"' if " " in f else f for f in value)
    if typ == "shadow":
        layers = value if isinstance(value, list) else [value]
        return ", ".join(
            f"{s['offsetX']} {s['offsetY']} {s['blur']} {s['spread']} {s['color']}" for s in layers
        )
    if typ == "cubicBezier":
        return "cubic-bezier({})".format(", ".join(str(v) for v in value))
    if typ == "typography":
        family = css_value(value["fontFamily"], "fontFamily")
        return f"{value['fontWeight']} {value['fontSize']}/{value['lineHeight']} {family}"
    return str(value)


def css():
    tokens = load()
    lines = [
        "/* Generated from design/tokens.json by design/tokens_tool.py — do not edit by hand. */",
        ":root {",
    ]
    for name, (value, typ) in tokens.items():
        var = "--" + name.replace(".", "-")
        lines.append(f"  {var}: {css_value(value, typ)};")
        if typ == "typography":
            lines.append(f"  {var}-tracking: {value['letterSpacing']};")
    lines.append("}")
    CSS.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {CSS.relative_to(ROOT.parent)} ({len(tokens)} tokens)")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles default to cp1252
    command = sys.argv[1] if len(sys.argv) > 1 else "check"
    sys.exit({"check": check, "css": css}.get(command, check)())
