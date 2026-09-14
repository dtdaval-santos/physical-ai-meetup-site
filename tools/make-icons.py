#!/usr/bin/env python3
"""Regenerate the favicon set from the source logo.

Usage:  python3 tools/make-icons.py
Needs:  pip install pillow

Takes assets/source/Logo no words.png (logo on a solid black background),
knocks the black out to transparency, and writes every icon the site uses.
"""
from PIL import Image
import numpy as np
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "source" / "Logo no words.png"
OUT = ROOT / "assets" / "icons"
OUT.mkdir(parents=True, exist_ok=True)

src = Image.open(SRC).convert("RGBA")
a = np.array(src).astype(np.float32)
rgb = a[..., :3]
lum = rgb.max(axis=2)

# soft ramp across the anti-aliased edge band; true colours preserved
LO, HI = 8.0, 55.0
alpha = np.clip((lum - LO) / (HI - LO), 0, 1)
out = np.zeros_like(a)
out[..., :3] = rgb
out[..., 3] = alpha * 255
logo = Image.fromarray(out.astype(np.uint8), "RGBA")
logo = logo.crop(logo.getbbox())


def square(img, size, pad=0.08, bg=None):
    w, h = img.size
    inner = int(size * (1 - 2 * pad))
    sc = min(inner / w, inner / h)
    small = img.resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.LANCZOS)
    canvas = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))
    canvas.alpha_composite(small, ((size - small.size[0]) // 2, (size - small.size[1]) // 2))
    return canvas


for s in (16, 32, 48, 192, 512):
    square(logo, s).save(OUT / f"favicon-{s}x{s}.png", optimize=True)

square(logo, 256).save(OUT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
square(logo, 180, pad=0.14, bg=(8, 11, 16, 255)).convert("RGB").save(
    OUT / "apple-touch-icon.png", optimize=True)

h = 320
logo.resize((int(logo.size[0] * h / logo.size[1]), h), Image.LANCZOS).save(
    OUT / "logo-mark.png", optimize=True)

print("icons written to", OUT)
