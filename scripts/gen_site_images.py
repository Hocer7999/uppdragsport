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

# Gemensam stil-svans för visuell konsistens.
# Ljus, vibrant och välexponerad sport-estetik — energisk men ren. Färgen
# kommer från motivet (grönt gräs, röd bana, vit is), inte från mörker.
STYLE = (
    " vivid high-energy sports photography, bright clean lighting, crisp and sharp, "
    "saturated vibrant colours, bright stadium floodlights, well-exposed with balanced "
    "contrast, dynamic and fresh, no people faces, no text, no logos, no watermark, "
    "wide editorial composition"
)

# (filnamn relativt public/, bredd, höjd, prompt-kärna)
JOBS = [
    ("images/hero.webp", 1536, 1024,
     "a vibrant green floodlit football pitch seen from pitch level, lush bright grass, "
     "crisp clean stadium lights, clear vivid atmosphere, energetic and alive"),
    ("images/om-oss.webp", 1536, 1024,
     "bright modern sports arena interior before kickoff, rows of colourful seats, "
     "daylight and floodlight filling the space, vivid and airy"),
    ("images/categories/fotboll.webp", 1024, 1280,
     "close-up of a classic black-and-white soccer ball on vivid bright green grass, "
     "crisp daylight, sharp detail, fresh dew droplets, bright stadium behind, "
     "association football"),
    ("images/categories/hockey.webp", 1024, 1280,
     "bright ice hockey rink under clean arena lights, gleaming white ice, a goal net, "
     "crisp cold fresh atmosphere, vivid and clear"),
    ("images/categories/innebandy.webp", 1024, 1280,
     "bright indoor sports hall, glossy light wood floor with vivid court lines, a "
     "floorball and stick, clean bright overhead lighting, airy"),
    ("images/categories/friidrott-och-skidor.webp", 1024, 1280,
     "bright running track under stadium lights, vivid red track surface, crisp white "
     "lane markings curving away, clean fresh and energetic"),
    ("images/articles/allsvenskan-formkurvor.webp", 1536, 1024,
     "bright floodlit football pitch at a low angle, vivid lush green grass, crisp "
     "clean lighting, clear bright stadium"),
    ("images/articles/shl-slutspel.webp", 1536, 1024,
     "bright ice hockey rink under arena lights, gleaming white ice with clean "
     "reflections, vivid fresh atmosphere"),
    ("images/articles/landslaget-kval.webp", 1536, 1024,
     "large bright national stadium at golden hour, flags lining the stands, vivid "
     "warm light over a clear green pitch"),
    ("images/articles/friidrotts-vm.webp", 1536, 1024,
     "athletics running track under bright stadium lights, vivid red track, crisp white "
     "lane lines, starting blocks in the foreground, clean bright stands"),
    ("images/articles/innebandy-ssl.webp", 1536, 1024,
     "bright indoor floorball arena, glossy court with vivid boundary lines, clean "
     "ceiling lights, fresh and airy"),
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
