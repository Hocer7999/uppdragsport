"""Test fal.ai gpt-image-2 by generating a small test logo for the Bombus template.

Reads FAL_KEY from astromall/.env, submits a prompt to the fal.ai queue API,
polls until the job completes, then downloads the image to public/test-logo.png.

Run from anywhere:
    python scripts/test_fal_logo.py
"""
import json
import os
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
OUT_PATH = ROOT / "public" / "test-logo.png"

MODEL = "openai/gpt-image-2"
SUBMIT_URL = f"https://queue.fal.run/{MODEL}"
PROMPT = (
    "minimalist flat vector logo of a stylized bumblebee in geometric shapes, "
    "soft black and warm yellow palette, clean modern editorial style, "
    "centered on white background, no text, no letters"
)


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


def poll(key: str, status_url: str, response_url: str, timeout: int = 180) -> dict:
    deadline = time.time() + timeout
    while time.time() < deadline:
        req = urllib.request.Request(
            status_url,
            headers={"Authorization": f"Key {key}"},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            status = json.loads(r.read().decode("utf-8"))
        s = status.get("status")
        print(f"  status={s}")
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


def download(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url, timeout=60) as r:
        dest.write_bytes(r.read())


def main() -> None:
    key = load_fal_key()
    print(f"OK: loaded FAL_KEY (len={len(key)})")
    print(f"-> submitting to {SUBMIT_URL}")
    try:
        submission = submit(key)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        sys.exit(f"FAIL: HTTP {e.code} on submit: {body[:500]}")
    print(f"   submission: {json.dumps(submission, indent=2)[:300]}")

    status_url = submission.get("status_url")
    response_url = submission.get("response_url")
    if not status_url or not response_url:
        sys.exit(f"FAIL: missing status_url/response_url in submission: {submission}")

    print(f"-> polling {status_url}")
    result = poll(key, status_url, response_url)
    print(f"   final result: {json.dumps(result, indent=2)[:500]}")

    images = result.get("images") or result.get("data", {}).get("images") or []
    if not images:
        sys.exit(f"FAIL: no images in result: {result}")
    image_url = images[0].get("url") if isinstance(images[0], dict) else images[0]
    if not image_url:
        sys.exit(f"FAIL: missing image url in {images[0]}")

    print(f"-> downloading {image_url}")
    download(image_url, OUT_PATH)
    print(f"OK: saved {OUT_PATH} ({OUT_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
