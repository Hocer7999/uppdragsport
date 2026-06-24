"""Generate a hero background video via fal.ai bytedance/seedance-2.0/text-to-video.

Edit the PROMPT constant below before running. Output is saved to
public/hero.mp4. Recommend also generating a poster image (public/hero.webp)
via gen_images.py so the Hero component can show a static frame while the
video loads and as fallback for prefers-reduced-motion.

Run: python scripts/gen_hero_video.py

Video jobs take significantly longer than image jobs (60–300s typically).
The polling timeout is set generously to avoid premature failure.
"""
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"

MODEL = "bytedance/seedance-2.0/text-to-video"
SUBMIT_URL = f"https://queue.fal.run/{MODEL}"

OUTPUT = ROOT / "public" / "hero.mp4"

# ===== EDIT THIS FOR EACH BUILD =======================================
# Hero video prompt. Describe the SCENE, not the brand. Keep it under 80
# words. The scene should LOOP-friendly: avoid hard cuts, dramatic camera
# moves, or content that ends — favor slow drifts, ambient motion, focus
# pulls, dust particles in light, etc.
#
# Nisch-tips:
#   Tandvård     → calm dental clinic interior, soft daylight panning slowly
#   Juridik      → city skyline at golden hour, slow drift
#   Hantverk     → close-up of a hand working on wood, soft natural light
#   Skönhet/spa  → water droplet rippling in slow motion, soft pastel
#   Finans       → abstract data flow, blurred bokeh of city at night
# ----------------------------------------------------------------------
PROMPT = (
    "[SCENE DESCRIPTION — e.g. calm scandinavian dental clinic interior, "
    "soft natural daylight from large windows, gentle slow camera pan from "
    "left to right, dental chair partially visible, warm wood and white "
    "tones, no people, no text, no logos, cinematic editorial photography]"
)

# Video parameters — adjust if needed. 720p is the sweet spot for web hero;
# 1080p quadruples filesize. 5s is enough for a seamless loop with most prompts.
RESOLUTION = "720p"      # "480p" | "720p" | "1080p"
ASPECT_RATIO = "16:9"    # "16:9" | "9:16" | "1:1"
DURATION = 5             # seconds; typically 5 or 10
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
        "resolution": RESOLUTION,
        "aspect_ratio": ASPECT_RATIO,
        "duration": DURATION,
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


def poll(key: str, status_url: str, response_url: str, timeout: int = 900) -> dict:
    """Poll up to 15 min — video jobs commonly take 60–300s."""
    deadline = time.time() + timeout
    last_status = None
    while time.time() < deadline:
        req = urllib.request.Request(
            status_url,
            headers={"Authorization": f"Key {key}"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            status = json.loads(r.read().decode("utf-8"))
        s = status.get("status")
        if s != last_status:
            print(f"  status={s}")
            last_status = s
        if s == "COMPLETED":
            req = urllib.request.Request(
                response_url,
                headers={"Authorization": f"Key {key}"},
            )
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        if s in ("ERROR", "FAILED"):
            sys.exit(f"FAIL: job ended with status={s}: {status}")
        time.sleep(5)
    sys.exit(f"FAIL: timeout after {timeout}s")


def download(url: str, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as r:
        dest.write_bytes(r.read())
    return dest.stat().st_size


def extract_video_url(result: dict) -> str:
    # fal video models can return video under a few different keys.
    for key in ("video", "videos", "output", "data"):
        v = result.get(key)
        if not v:
            continue
        if isinstance(v, dict) and v.get("url"):
            return v["url"]
        if isinstance(v, list) and v:
            first = v[0]
            if isinstance(first, dict) and first.get("url"):
                return first["url"]
            if isinstance(first, str):
                return first
        if isinstance(v, str) and v.startswith("http"):
            return v
        if isinstance(v, dict):
            inner = v.get("video") or v.get("videos")
            if isinstance(inner, dict) and inner.get("url"):
                return inner["url"]
    sys.exit(f"FAIL: could not find video URL in result: {json.dumps(result)[:500]}")


def main() -> None:
    if "[SCENE DESCRIPTION" in PROMPT:
        sys.exit(
            "FAIL: PROMPT still has placeholder text — edit gen_hero_video.py "
            "to describe the niche-specific scene before running."
        )
    key = load_fal_key()
    print(f"OK: loaded FAL_KEY (len={len(key)})")
    print(f"-> {OUTPUT} ({RESOLUTION} {ASPECT_RATIO} {DURATION}s)")
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
    video_url = extract_video_url(result)
    size = download(video_url, OUTPUT)
    print(f"   saved {OUTPUT} ({size / 1024 / 1024:.1f} MB)")


if __name__ == "__main__":
    main()
