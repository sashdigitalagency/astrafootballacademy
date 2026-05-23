#!/usr/bin/env python3
"""Optimize and review premium Astra keyframes for Wix/browser playback."""
from __future__ import annotations

import math
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / os.getenv("ASTRA_SOURCE_DIR", "frames_premium")
OUTPUT_DIR = ROOT / os.getenv("ASTRA_OUTPUT_DIR", "frames_premium_web")
REVIEW_DIR = ROOT / os.getenv("ASTRA_REVIEW_DIR", "review")
REVIEW_SHEET = os.getenv("ASTRA_REVIEW_SHEET", "premium-contact-sheet.jpg")
TARGET_SIZE = (1600, 900)


def cover_resize(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    return ImageOps.fit(img.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))


def cinematic_grade(img: Image.Image) -> Image.Image:
    img = ImageEnhance.Contrast(img).enhance(1.12)
    img = ImageEnhance.Color(img).enhance(1.06)
    img = ImageEnhance.Sharpness(img).enhance(1.08)

    arr = np.asarray(img).astype(np.float32)
    luminance = arr.mean(axis=2, keepdims=True) / 255.0
    shadow = 1.0 - luminance
    highlight = luminance

    # Deep navy shadows and restrained warm highlights.
    arr[:, :, 0] += shadow[:, :, 0] * 2 + highlight[:, :, 0] * 7
    arr[:, :, 1] += shadow[:, :, 0] * 4 + highlight[:, :, 0] * 3
    arr[:, :, 2] += shadow[:, :, 0] * 12
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return Image.fromarray(arr, "RGB")


def add_vignette(img: Image.Image, strength: float = 0.34) -> Image.Image:
    width, height = img.size
    y, x = np.ogrid[-1:1:height * 1j, -1:1:width * 1j]
    radius = np.sqrt((x * 0.92) ** 2 + (y * 1.05) ** 2)
    mask = 1 - np.clip((radius - 0.28) / 0.95, 0, 1) * strength
    mask_img = Image.fromarray(np.uint8(mask * 255), "L").filter(ImageFilter.GaussianBlur(14))
    dark = Image.new("RGB", img.size, (0, 0, 0))
    return Image.composite(img, dark, mask_img)


def add_subtle_grain(img: Image.Image, amount: float = 0.018) -> Image.Image:
    arr = np.asarray(img).astype(np.float32)
    noise = np.random.default_rng(42).normal(0, 255 * amount, arr.shape[:2])
    arr[:, :, 0] += noise
    arr[:, :, 1] += noise
    arr[:, :, 2] += noise
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8), "RGB")


def process_frame(path: Path) -> Path:
    img = Image.open(path)
    img = cover_resize(img, TARGET_SIZE)
    img = cinematic_grade(img)
    img = add_vignette(img)
    img = add_subtle_grain(img)
    out = OUTPUT_DIR / path.with_suffix(".webp").name
    img.save(out, "WEBP", quality=86, method=6)
    return out


def make_contact_sheet(paths: list[Path]) -> Path:
    thumbs = []
    for path in paths:
        img = Image.open(path).convert("RGB")
        img.thumbnail((320, 180), Image.Resampling.LANCZOS)
        tile = Image.new("RGB", (320, 210), (8, 12, 20))
        tile.paste(img, (0, 0))
        draw = ImageDraw.Draw(tile)
        draw.text((12, 186), path.stem.replace("frame_", "Frame "), fill=(240, 248, 255))
        thumbs.append(tile)

    cols = 4
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * 320, rows * 210), (4, 8, 16))
    for idx, tile in enumerate(thumbs):
        sheet.paste(tile, ((idx % cols) * 320, (idx // cols) * 210))

    out = REVIEW_DIR / REVIEW_SHEET
    sheet.save(out, "JPEG", quality=90)
    return out


def main() -> int:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    frames = sorted(SOURCE_DIR.glob("frame_*.png"))
    if not frames:
        print(f"No frames found in {SOURCE_DIR}")
        return 1

    outputs = []
    for frame in frames:
        out = process_frame(frame)
        outputs.append(out)
        print(f"saved {out.relative_to(ROOT)}")

    sheet = make_contact_sheet(outputs)
    print(f"contact sheet: {sheet}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
