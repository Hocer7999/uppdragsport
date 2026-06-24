"""Remove background via fal.ai birefnet (state-of-the-art segmentation).

Usage:
  python remove_bg_fal.py input.png output.png

Requires FAL_KEY in environment or .env file.
"""
import os
import sys
from pathlib import Path
from urllib.request import urlretrieve

import fal_client


def load_env():
    env_path = Path(".env")
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ.setdefault(key.strip(), val.strip())


def main(input_path: str, output_path: str) -> None:
    src = Path(input_path)
    if not src.exists():
        print(f"ERROR: input file not found: {src}")
        sys.exit(1)

    load_env()
    if not os.environ.get("FAL_KEY"):
        print("ERROR: FAL_KEY not set in env or .env")
        sys.exit(1)

    print(f"Uploading {src}...")
    url = fal_client.upload_file(str(src))

    print("Running fal-ai/birefnet/v2...")
    result = fal_client.subscribe(
        "fal-ai/birefnet/v2",
        arguments={"image_url": url},
        with_logs=False,
    )

    out_url = result["image"]["url"]
    print(f"Downloading result from {out_url}")
    urlretrieve(out_url, output_path)
    size = Path(output_path).stat().st_size
    print(f"OK: {output_path} ({size} bytes)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python remove_bg_fal.py <input.png> <output.png>")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
