#!/usr/bin/env python3
"""Render an 8-second MP4/WebM fallback from the premium frame sequence."""
from __future__ import annotations

import shutil
import subprocess
import os
from pathlib import Path

from PIL import Image, ImageEnhance


ROOT = Path(__file__).resolve().parent
SOURCE_DIR = ROOT / os.getenv("ASTRA_VIDEO_SOURCE_DIR", "frames_premium_web")
WORK_DIR = ROOT / os.getenv("ASTRA_VIDEO_WORK_DIR", "video_frames_premium")
DIST_DIR = ROOT / os.getenv("ASTRA_VIDEO_DIST_DIR", "dist")
VIDEO_BASENAME = os.getenv("ASTRA_VIDEO_BASENAME", "astra-premium-scroll-motion")
WIDTH = 1600
HEIGHT = 900
FPS = 24
DURATION_SECONDS = 8
TOTAL_VIDEO_FRAMES = FPS * DURATION_SECONDS


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3 - 2 * value)


def gaussian(value: float, center: float, width: float) -> float:
    return pow(2.718281828, -((value - center) / width) ** 2)


def cover_zoom(img: Image.Image, progress: float, impact: float) -> Image.Image:
    zoom = 1.015 + progress * 0.07 + impact * 0.025
    crop_w = int(WIDTH / zoom)
    crop_h = int(HEIGHT / zoom)
    pan_x = int((progress - 0.5) * WIDTH * 0.035)
    pan_y = int((0.5 - progress) * HEIGHT * 0.018 - impact * HEIGHT * 0.01)
    left = (WIDTH - crop_w) // 2 + pan_x
    top = (HEIGHT - crop_h) // 2 + pan_y
    left = max(0, min(WIDTH - crop_w, left))
    top = max(0, min(HEIGHT - crop_h, top))
    cropped = img.crop((left, top, left + crop_w, top + crop_h))
    return cropped.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def prepare_work_dir() -> None:
    if WORK_DIR.exists():
        shutil.rmtree(WORK_DIR)
    WORK_DIR.mkdir(parents=True)
    DIST_DIR.mkdir(parents=True, exist_ok=True)


def render_intermediate_frames(frames: list[Image.Image]) -> None:
    last_index = len(frames) - 1
    for i in range(TOTAL_VIDEO_FRAMES):
        p = i / (TOTAL_VIDEO_FRAMES - 1)
        story = smoothstep(p)
        exact = story * last_index
        action_frames = 0.18 < p < 0.82
        index = round(exact) if action_frames else int(exact)
        next_index = index if action_frames else min(index + 1, last_index)
        blend = 0.0 if action_frames else smoothstep(exact - index)
        impact = gaussian(p, 0.42, 0.09)

        current = cover_zoom(frames[index], p, impact)
        if next_index != index and blend > 0.01:
            nxt = cover_zoom(frames[next_index], p, impact)
            current = Image.blend(current, nxt, blend)

        if impact > 0.02:
            current = ImageEnhance.Contrast(current).enhance(1 + impact * 0.08)
            current = ImageEnhance.Brightness(current).enhance(1 + impact * 0.035)

        current.save(WORK_DIR / f"frame_{i + 1:04d}.jpg", "JPEG", quality=91, optimize=True)
        if (i + 1) % 24 == 0:
            print(f"rendered {i + 1}/{TOTAL_VIDEO_FRAMES}")


def run_ffmpeg(args: list[str]) -> None:
    subprocess.run(args, cwd=ROOT, check=True)


def encode_video() -> None:
    input_pattern = str(WORK_DIR / "frame_%04d.jpg")
    mp4_out = str(DIST_DIR / f"{VIDEO_BASENAME}.mp4")
    webm_out = str(DIST_DIR / f"{VIDEO_BASENAME}.webm")

    run_ffmpeg([
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", input_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        "-crf", "18",
        mp4_out,
    ])
    run_ffmpeg([
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", input_pattern,
        "-c:v", "libvpx-vp9",
        "-pix_fmt", "yuv420p",
        "-b:v", "0",
        "-crf", "30",
        webm_out,
    ])


def main() -> int:
    frame_paths = sorted(SOURCE_DIR.glob("frame_*.webp"))
    if not frame_paths:
        print(f"No optimized frames found in {SOURCE_DIR}")
        return 1

    prepare_work_dir()
    frames = [Image.open(path).convert("RGB").resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS) for path in frame_paths]
    render_intermediate_frames(frames)
    encode_video()
    print(f"video written to {DIST_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
