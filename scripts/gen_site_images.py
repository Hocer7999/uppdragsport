"""Batch-generera Stadium Noir-bilder för Uppdragsport via fal.ai openai/gpt-image-2 (quality low).

Cinematisk mörk sport-estetik: dramatiskt riktat ljus, arena/action-stämning,
mörk palett med EN röd ljusaccent. INGA ansikten, INGA logotyper/text i bild.
Sparas som .webp i public/images/. Kör: python scripts/gen_site_images.py
"""
import json
import sys
import time
import urllib.request
import urllib.error
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
MODEL = "openai/gpt-image-2"
SUBMIT_URL = f"https://queue.fal.run/{MODEL}"

# Gemensam stil-svans för visuell konsistens (Stadium Noir).
STYLE = (
    " cinematic dark sports photography, near-black background, dramatic single "
    "directional light, deep shadows, one subtle warm red light accent, "
    "high contrast, moody atmosphere, fine haze in the light beam, no people faces, "
    "no text, no logos, no watermark, wide editorial composition"
)

# (filnamn relativt public/, bredd, höjd, prompt-kärna)
JOBS = [
    ("images/hero.webp", 1536, 1024,
     "empty floodlit stadium at night seen from pitch level, wet grass reflecting "
     "the lights, long shadows, atmospheric mist drifting across the field"),
    ("images/om-oss.webp", 1536, 1024,
     "dark sports arena interior before kickoff, rows of empty seats fading into "
     "shadow, a single shaft of light falling onto the field"),
    ("images/categories/fotboll.webp", 1024, 1280,
     "close-up of a classic round black-and-white soccer ball resting on floodlit "
     "wet green grass at night, dramatic side light, water droplets glistening, "
     "dark blurred stadium stands behind, association football"),
    ("images/categories/hockey.webp", 1024, 1280,
     "empty ice hockey rink under arena spotlights, polished ice reflecting light, "
     "an empty goal net in shadow, cold dark atmosphere"),
    ("images/categories/innebandy.webp", 1024, 1280,
     "indoor sports hall floor with bright court lines, a floorball and stick on the "
     "polished wood, dramatic overhead spotlight, dark rafters above"),
    ("images/categories/friidrott-och-skidor.webp", 1024, 1280,
     "running track lanes at night under stadium lights, sharp white lane markings "
     "curving away, empty and dramatic, dark grandstand behind"),
    ("images/articles/allsvenskan-formkurvor.webp", 1536, 1024,
     "floodlit football pitch at dusk seen at a low angle, long dramatic shadows "
     "stretching across the grass, empty dark stadium stands"),
    ("images/articles/shl-slutspel.webp", 1536, 1024,
     "ice hockey rink lit by arena spotlights, reflections on the ice, an empty "
     "players bench in deep shadow, tense dark atmosphere"),
    ("images/articles/landslaget-kval.webp", 1536, 1024,
     "large empty national stadium at twilight, faint flags lining the upper stands, "
     "a single dramatic light over the dark pitch"),
    ("images/articles/friidrotts-vm.webp", 1536, 1024,
     "athletics running track at night under bright stadium lights, crisp lane lines, "
     "starting blocks in the foreground, empty dark stands behind"),
    ("images/articles/innebandy-ssl.webp", 1536, 1024,
     "indoor floorball arena, glossy court with bright boundary lines, dramatic "
     "ceiling spotlights, dark empty stands surrounding the court"),
]


def load_fal_key() -> str:
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("FAL_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("FAIL: FAL_KEY not found in .env")


def fal_size(w: int, h: int) -> str:
    if w > h:
        return "landscape_16_9"
    if h > w:
        return "portrait_4_3"
    return "square_hd"


def submit(key: str, prompt: str, w: int, h: int) -> dict:
    body = json.dumps({
        "prompt": prompt,
        "quality": "low",
        "num_images": 1,
        "image_size": fal_size(w, h),
        "output_format": "png",
    }).encode("utf-8")
    req = urllib.request.Request(
        SUBMIT_URL, data=body,
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


def poll(key: str, status_url: str, response_url: str, timeout: int = 240) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        req = urllib.request.Request(status_url, headers={"Authorization": f"Key {key}"})
        with urllib.request.urlopen(req, timeout=30) as r:
            status = json.loads(r.read().decode("utf-8"))
        s = status.get("status")
        if s == "COMPLETED":
            req = urllib.request.Request(response_url, headers={"Authorization": f"Key {key}"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode("utf-8"))
        if s in ("ERROR", "FAILED"):
            sys.exit(f"FAIL: job status={s}: {status}")
        time.sleep(2)
    sys.exit(f"FAIL: timeout after {timeout}s")


def download_webp(url: str, dest: Path, w: int, h: int) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as r:
        raw = r.read()
    img = Image.open(BytesIO(raw)).convert("RGB")
    # Center-crop to target aspect, then resize.
    tw, th = w, h
    iw, ih = img.size
    target_ratio = tw / th
    cur_ratio = iw / ih
    if cur_ratio > target_ratio:
        new_w = int(ih * target_ratio)
        left = (iw - new_w) // 2
        img = img.crop((left, 0, left + new_w, ih))
    else:
        new_h = int(iw / target_ratio)
        top = (ih - new_h) // 2
        img = img.crop((0, top, iw, top + new_h))
    img = img.resize((tw, th), Image.LANCZOS)
    img.save(dest, format="WEBP", quality=82, method=6)
    return dest.stat().st_size


def main() -> None:
    only = set(sys.argv[1:])
    key = load_fal_key()
    print(f"OK: FAL_KEY len={len(key)} | {len(JOBS)} jobs")
    for rel, w, h, core in JOBS:
        if only and rel not in only:
            continue
        dest = ROOT / "public" / rel
        prompt = core + STYLE
        print(f"-> {rel} ({w}x{h})")
        try:
            sub = submit(key, prompt, w, h)
        except urllib.error.HTTPError as e:
            print(f"   FAIL submit HTTP {e.code}: {e.read().decode('utf-8','replace')[:300]}")
            continue
        result = poll(key, sub["status_url"], sub["response_url"])
        images = result.get("images") or result.get("data", {}).get("images") or []
        if not images:
            print(f"   FAIL: no images: {result}")
            continue
        iu = images[0].get("url") if isinstance(images[0], dict) else images[0]
        size = download_webp(iu, dest, w, h)
        print(f"   saved {rel} ({size} bytes)")
    print("DONE")


if __name__ == "__main__":
    main()
