"""Generate a transparent-background logo for the project via fal.ai openai/gpt-image-2.

The subagent running the `new-site` skill SHOULD edit the PROMPT constant below
to match the niche before running, then execute:

    python scripts/gen_logo.py

Result is saved to public/logo.png (PNG with alpha). After generation the logo
is automatically cleaned with fal.ai birefnet/v2 — this removes the outer
background AND the inner gaps that gpt-image-2 sometimes leaves as solid white
pixels (e.g. spaces between concentric rings). Always use the model and quality
combination already set here — do NOT switch to Flux.
"""
import json
import sys
import time
import urllib.request
import urllib.error
from io import BytesIO
from pathlib import Path

from PIL import Image

# Import bg-removal from sibling script
sys.path.insert(0, str(Path(__file__).resolve().parent))
from remove_bg_fal import main as clean_bg

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"

MODEL = "openai/gpt-image-2"
SUBMIT_URL = f"https://queue.fal.run/{MODEL}"

OUTPUT = ROOT / "public" / "logo.png"

# ===== EDIT THIS FOR EACH BUILD =======================================
# Niche-specific symbol + primary-color hex (from ui-ux-pro-max output).
# Keep the boilerplate ("clean modern vector style ... no text ... isolated
# centered symbol") — change only the symbol description and the hex.
# See SKILL.md Steg 6a for the symbol table per niche.
# ----------------------------------------------------------------------
PROMPT = (
    "minimalist logo symbol for a Swedish sports news brand, "
    "bold abstract forward chevron mark suggesting speed and momentum, "
    "two sharp angular arrows pointing right stacked into a dynamic motion glyph, "
    "single solid color #f33736, "
    "clean modern vector style, geometric, balanced composition, generous "
    "white space around the symbol, transparent background, professional, "
    "no text, no shadows, no gradients, no extra elements, isolated centered "
    "symbol"
)
# ======================================================================


def load_fal_key() -> str:
    if not ENV_PATH.exists():
        sys.exit(f"FAIL: no .env at {ENV_PATH}")
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("FAL_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("FAIL: FAL_KEY not found in .env")


def submit(key: str) -> dict:
    body = json.dumps({
        "prompt": PROMPT,
        "quality": "low",
        "num_images": 1,
        "image_size": "square_hd",
        "background": "transparent",
        "output_format": "png",
    }).encode("utf-8")
    req = urllib.request.Request(
        SUBMIT_URL,
        data=body,
        headers={
            "Authorization": f"Key {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def poll(key: str, status_url: str, response_url: str, timeout: int = 240) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        req = urllib.request.Request(
            status_url,
            headers={"Authorization": f"Key {key}"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            status = json.loads(r.read().decode("utf-8"))
        s = status.get("status")
        if s == "COMPLETED":
            req = urllib.request.Request(
                response_url,
                headers={"Authorization": f"Key {key}"},
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        if s in ("ERROR", "FAILED"):
            sys.exit(f"FAIL: job ended with status={s}: {status}")
        time.sleep(2)
    sys.exit(f"FAIL: timeout after {timeout}s")


def download_png(url: str, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as r:
        raw = r.read()
    img = Image.open(BytesIO(raw))
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    img.save(dest, format="PNG", optimize=True)
    return dest.stat().st_size


def main() -> None:
    if "[BRAND/NICHE]" in PROMPT or "[PRIMARY HEX" in PROMPT or "[SYMBOL" in PROMPT:
        sys.exit(
            "FAIL: PROMPT still has placeholder text — edit gen_logo.py to "
            "fill in the niche-specific values before running."
        )
    key = load_fal_key()
    print(f"OK: loaded FAL_KEY (len={len(key)})")
    print(f"-> {OUTPUT}")
    try:
        submission = submit(key)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"FAIL: HTTP {e.code} on submit: {body[:500]}")
    status_url = submission.get("status_url")
    response_url = submission.get("response_url")
    if not status_url or not response_url:
        sys.exit(f"FAIL: missing url in submission: {submission}")

    result = poll(key, status_url, response_url)
    images = result.get("images") or result.get("data", {}).get("images") or []
    if not images:
        sys.exit(f"FAIL: no images: {result}")
    image_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    if not image_url:
        sys.exit(f"FAIL: no URL in image[0]: {images[0]}")

    size = download_png(image_url, OUTPUT)
    print(f"   saved {OUTPUT} ({size} bytes)")

    print("Cleaning background via fal birefnet...")
    clean_bg(str(OUTPUT), str(OUTPUT))


if __name__ == "__main__":
    main()
