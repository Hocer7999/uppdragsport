"""Generera annons-creatives (betting/casino-känsla) via fal.ai gpt-image-2 (quality low).
Brand-färgade bakgrunder UTAN riktiga loggor (varumärkestext läggs som HTML-overlay
i AdBanner.astro). Sparas i public/images/ads/. Kör: python scripts/gen_ad_images.py
"""
import json, sys, time, urllib.request, urllib.error
from io import BytesIO
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
MODEL = "openai/gpt-image-2"
SUBMIT_URL = f"https://queue.fal.run/{MODEL}"

# (filnamn relativt public/, bredd, höjd, prompt)
JOBS = [
    ("images/ads/unibet.webp", 1600, 420,
     "wide horizontal sports betting advertisement creative, deep emerald green gradient background with bright stadium lighting, a glowing football and abstract floating glowing odds figures, energetic premium bookmaker aesthetic, clean negative space on one side, no readable words, no letters, no logos, no watermark"),
    ("images/ads/betsson.webp", 1600, 420,
     "wide horizontal sportsbook advertisement creative, dark charcoal background with vivid orange accent lighting, a football and abstract glowing betting numbers, dynamic premium energetic, clean negative space, no readable words, no letters, no logos, no watermark"),
    ("images/ads/leovegas.webp", 640, 520,
     "square online casino advertisement creative, luxurious gold and black, glowing casino chips and dice with warm rich light, premium gaming aesthetic, clean negative space at top, no readable words, no letters, no logos, no watermark"),
    ("images/ads/comeon.webp", 640, 520,
     "square sports betting advertisement creative, vivid purple and magenta gradient, a glowing football with neon accent light, energetic premium, clean negative space, no readable words, no letters, no logos, no watermark"),
]


def load_fal_key():
    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("FAL_KEY="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    sys.exit("FAIL: FAL_KEY not found in .env")


def fal_size(w, h):
    return "landscape_16_9" if w > h else ("portrait_4_3" if h > w else "square_hd")


def submit(key, prompt, w, h):
    body = json.dumps({"prompt": prompt, "quality": "low", "num_images": 1,
                       "image_size": fal_size(w, h), "output_format": "png"}).encode()
    req = urllib.request.Request(SUBMIT_URL, data=body,
                                 headers={"Authorization": f"Key {key}", "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def poll(key, status_url, response_url, timeout=240):
    deadline = time.time() + timeout
    while time.time() < deadline:
        req = urllib.request.Request(status_url, headers={"Authorization": f"Key {key}"})
        with urllib.request.urlopen(req, timeout=30) as r:
            st = json.loads(r.read().decode())
        s = st.get("status")
        if s == "COMPLETED":
            req = urllib.request.Request(response_url, headers={"Authorization": f"Key {key}"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        if s in ("ERROR", "FAILED"):
            sys.exit(f"FAIL: status={s}: {st}")
        time.sleep(2)
    sys.exit("FAIL: timeout")


def download(url, dest, w, h):
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=120) as r:
        img = Image.open(BytesIO(r.read())).convert("RGB")
    iw, ih = img.size
    tr, cr = w / h, iw / ih
    if cr > tr:
        nw = int(ih * tr); left = (iw - nw) // 2; img = img.crop((left, 0, left + nw, ih))
    else:
        nh = int(iw / tr); top = (ih - nh) // 2; img = img.crop((0, top, iw, top + nh))
    img = img.resize((w, h), Image.LANCZOS)
    img.save(dest, format="WEBP", quality=82, method=6)
    return dest.stat().st_size


def main():
    key = load_fal_key()
    print(f"OK: FAL_KEY len={len(key)} | {len(JOBS)} ad jobs")
    for rel, w, h, prompt in JOBS:
        dest = ROOT / "public" / rel
        print(f"-> {rel} ({w}x{h})")
        try:
            sub = submit(key, prompt, w, h)
        except urllib.error.HTTPError as e:
            print(f"   FAIL HTTP {e.code}: {e.read().decode('utf-8','replace')[:200]}"); continue
        res = poll(key, sub["status_url"], sub["response_url"])
        imgs = res.get("images") or []
        if not imgs:
            print(f"   FAIL no images: {res}"); continue
        iu = imgs[0]["url"] if isinstance(imgs[0], dict) else imgs[0]
        print(f"   saved {rel} ({download(iu, dest, w, h)} bytes)")
    print("DONE")


if __name__ == "__main__":
    main()
