"""Generate a clean square monogram favicon set for a site that has no usable
square brand mark.

Renders the site's initial(s) in white on its brand colour, then writes the
full favicon set (PNGs + multi-res .ico + self-contained SVG) into public/.

Usage:
    python scripts/gen_monogram_favicon.py <site_dir> <monogram> <color>

  <color> is either #RRGGBB or oklch(L C H)  (L may be 0..1 or a percent).

This avoids the two classic failure modes:
  - external-image favicon.svg (blank in browsers' sandbox)
  - squashing a wide wordmark logo into a square (illegible).
"""
import base64
import io
import math
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

FONT = "C:/Windows/Fonts/segoeuib.ttf"  # Segoe UI Bold


def _srgb(c: float) -> float:
    c = max(0.0, min(1.0, c))
    return 12.92 * c if c <= 0.0031308 else 1.055 * (c ** (1 / 2.4)) - 0.055


def oklch_to_rgb(L: float, C: float, H: float) -> tuple[int, int, int]:
    """OKLCH (L 0..1, C, H degrees) -> sRGB 0..255."""
    h = math.radians(H)
    a, b = C * math.cos(h), C * math.sin(h)
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    r = 4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_
    g = -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_
    bl = -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_
    return tuple(round(_srgb(x) * 255) for x in (r, g, bl))


def parse_color(spec: str) -> tuple[int, int, int]:
    spec = spec.strip()
    if spec.startswith("#"):
        h = spec.lstrip("#")
        return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
    m = re.match(r"oklch\(\s*([\d.]+%?)\s+([\d.]+)\s+([\d.]+)", spec)
    if not m:
        raise ValueError(f"unparseable color: {spec!r}")
    L = float(m.group(1).rstrip("%")) / (100 if "%" in m.group(1) else 1)
    return oklch_to_rgb(L, float(m.group(2)), float(m.group(3)))


SIZES = [
    ("favicon-16x16.png", 16),
    ("favicon-32x32.png", 32),
    ("apple-touch-icon.png", 180),
    ("android-chrome-192x192.png", 192),
    ("android-chrome-512x512.png", 512),
]


def render(text: str, bg: tuple[int, int, int], size: int = 512) -> Image.Image:
    img = Image.new("RGB", (size, size), bg)
    d = ImageDraw.Draw(img)
    # fit the text to ~62% of the box
    target = size * 0.62
    fs = size
    while fs > 4:
        font = ImageFont.truetype(FONT, fs)
        l, t, r, b = d.textbbox((0, 0), text, font=font)
        if (r - l) <= target and (b - t) <= target:
            break
        fs -= 2
    l, t, r, b = d.textbbox((0, 0), text, font=font)
    x = (size - (r - l)) / 2 - l
    y = (size - (b - t)) / 2 - t
    d.text((x, y), text, font=font, fill=(255, 255, 255))
    return img


def main() -> None:
    site, mono, color = sys.argv[1], sys.argv[2], sys.argv[3]
    pub = Path(site) / "public"
    if not pub.is_dir():
        raise SystemExit(f"FAIL: {pub} missing")
    bg = parse_color(color)
    master = render(mono, bg, 512)
    print(f"{site}: '{mono}' on rgb{bg}")

    for name, sz in SIZES:
        master.resize((sz, sz), Image.LANCZOS).save(pub / name, format="PNG", optimize=True)
    master.save(pub / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])

    buf = io.BytesIO()
    master.resize((256, 256), Image.LANCZOS).save(buf, format="PNG", optimize=True)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">'
        f'<image href="data:image/png;base64,{b64}" width="256" height="256"/>'
        "</svg>"
    )
    (pub / "favicon.svg").write_text(svg, encoding="utf-8")
    print(f"   wrote favicon set ({', '.join(n for n, _ in SIZES)}, favicon.ico, favicon.svg)")


if __name__ == "__main__":
    main()
