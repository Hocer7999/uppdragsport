"""Generate the favicon set from public/logo.png at multiple sizes.

Apple touch icon is composited on a solid background (defaults to the
project's --color-primary). Override APPLE_BG_HEX below if your primary
differs significantly from the default teal.

Run: python scripts/gen_favicons.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "public" / "logo.png"
PUB = ROOT / "public"

# ===== EDIT IF YOUR PRIMARY DIFFERS ==================================
# Match this to the --color-primary in your DaisyUI theme (see SKILL.md
# Steg 3.5). The Apple touch icon background uses this color.
APPLE_BG_HEX = "#000000"
# =====================================================================


def hex_to_rgba(h: str) -> tuple[int, int, int, int]:
    h = h.lstrip("#")
    if len(h) != 6:
        raise ValueError(f"expected #RRGGBB, got {h!r}")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)


SIZES = [
    ("favicon-16x16.png", 16, None),
    ("favicon-32x32.png", 32, None),
    ("apple-touch-icon.png", 180, hex_to_rgba(APPLE_BG_HEX)),
    ("android-chrome-192x192.png", 192, None),
    ("android-chrome-512x512.png", 512, None),
]


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"FAIL: source {SRC} missing — run gen_logo.py first")
    base = Image.open(SRC).convert("RGBA")
    print(f"OK: source {base.size}")

    for name, size, bg in SIZES:
        out = PUB / name
        if bg is None:
            img = base.resize((size, size), Image.LANCZOS)
        else:
            # Composite logo on solid bg with 12% padding (Apple HIG-friendly)
            canvas = Image.new("RGBA", (size, size), bg)
            inner = int(size * 0.76)
            logo = base.resize((inner, inner), Image.LANCZOS)
            off = (size - inner) // 2
            canvas.paste(logo, (off, off), logo)
            img = canvas.convert("RGB")
        img.save(out, format="PNG", optimize=True)
        print(f"   wrote {name} ({out.stat().st_size} bytes)")

    # Self-contained SVG with the icon embedded as a base64 PNG data-URI.
    # NOTE: a favicon SVG must NOT reference an external <image href="/logo.png">
    # — browsers render favicons sandboxed and refuse to fetch external assets,
    # which renders the favicon blank. Embed the bytes instead.
    import base64, io

    buf = io.BytesIO()
    base.resize((256, 256), Image.LANCZOS).save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">'
        f'<image href="data:image/png;base64,{b64}" width="256" height="256"/>'
        "</svg>"
    )
    (PUB / "favicon.svg").write_text(svg, encoding="utf-8")
    print(f"   wrote favicon.svg (self-contained, {len(svg)} bytes)")

    # Real multi-resolution favicon.ico from the logo. Without this the stale
    # boilerplate default favicon.ico survives a generator run and browsers may
    # still auto-fetch /favicon.ico and show the wrong icon.
    ico = PUB / "favicon.ico"
    base.save(
        ico,
        format="ICO",
        sizes=[(16, 16), (32, 32), (48, 48), (64, 64)],
    )
    print(f"   wrote favicon.ico ({ico.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
