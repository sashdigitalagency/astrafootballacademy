#!/usr/bin/env python3
"""Generate cinematic frames for Astra United scroll animation."""
import os
import time
import requests
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed

OUTPUT_DIR = "frames"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FRAMES = [
    # Frame 01 — Establishing shot
    "Cinematic wide shot of an empty professional football stadium at dusk, floodlights illuminating vibrant green pitch, dramatic dark clouds, deep blue and orange sky, photorealistic, 8k, film grain, anamorphic lens",
    # Frame 02 — Players enter
    "Wide shot of three football players in dark navy blue and red kits on green pitch at dusk, one player dribbling ball forward, teammates sprinting ahead, stadium floodlights casting long shadows, cinematic motion blur, photorealistic",
    # Frame 03 — Dribbling
    "Medium shot of football midfielder in navy and red kit dribbling ball on green pitch, determined posture, stadium lights in background, cinematic shallow depth of field, dust particles in air, photorealistic",
    # Frame 04 — Looking up
    "Close medium shot of football player in navy and red kit looking up while running with ball, scanning for pass, dramatic side lighting from stadium floodlights, green pitch below, photorealistic, cinematic",
    # Frame 05 — The pass
    "Wide shot of football player in navy and red kit making a powerful pass, ball just leaving foot, teammates running into space, stadium floodlights, green pitch, motion blur on ball, photorealistic, cinematic",
    # Frame 06 — Ball in air
    "Cinematic shot of football in mid-air traveling across green pitch at dusk, stadium floodlights creating lens flares, motion blur trail, grass particles flying, dramatic lighting, photorealistic",
    # Frame 07 — Wing control
    "Medium shot of winger in navy and red kit controlling ball on the wing, body angled toward goal, defender in background, stadium lights, green pitch, cinematic motion, photorealistic",
    # Frame 08 — Cut inside
    "Dynamic shot of winger in navy and red kit cutting inside with ball, sharp turn, defender sliding, grass kicking up, stadium floodlights, dramatic action, photorealistic, cinematic",
    # Frame 09 — The cross
    "Wide shot of winger in navy and red kit crossing ball into penalty box, ball arcing through air, striker waiting in box, goalkeeper preparing, stadium lights, green pitch, photorealistic, cinematic",
    # Frame 10 — Ball arcs
    "Cinematic shot of football arcing through air toward goal, spinning ball, stadium floodlights creating bokeh, green pitch below, dramatic dusk sky, motion blur, photorealistic",
    # Frame 11 — The leap
    "Dramatic shot of striker in navy and red kit leaping high for header, arms outstretched, eyes focused on ball, stadium floodlights backlighting, green pitch below, peak athletic moment, photorealistic, cinematic",
    # Frame 12 — Header connection
    "Intense moment of striker in navy and red kit connecting with header, ball compressing against forehead, muscles tense, stadium lights, green pitch, freeze frame action, photorealistic, cinematic",
    # Frame 13 — Goal!
    "Dramatic shot of football smashing into goal net, net bulging and stretching, fragments of grass flying, stadium floodlights, goalpost visible, peak action moment, photorealistic, cinematic",
    # Frame 14 — Celebration
    "Wide shot of three football players in navy and red kits celebrating goal, arms raised, running toward camera, stadium floodlights, green pitch, joy and triumph, photorealistic, cinematic, red lighting",
    # Frame 15 — Cinematic logo moment
    "Cinematic dark background with deep navy and red tones, subtle stadium lights in distance, glowing red light flare, atmospheric dust particles, dramatic film grain, abstract football atmosphere, photorealistic",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def generate_frame(idx, prompt):
    num = f"{idx + 1:03d}"
    out_path = os.path.join(OUTPUT_DIR, f"frame_{num}.png")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
        print(f"  Frame {num} already exists, skipping.")
        return True

    # Use a seed based on frame index for some variety but controlled
    seed = 100 + idx
    url = (
        "https://image.pollinations.ai/prompt/"
        + urllib.parse.quote(prompt)
        + f"?width=1280&height=720&seed={seed}&nologo=true&negative_prompt=blurry,deformed,hands"
    )

    try:
        r = requests.get(url, headers=HEADERS, timeout=120)
        if r.status_code == 200 and len(r.content) > 1000:
            with open(out_path, "wb") as f:
                f.write(r.content)
            print(f"  ✓ Frame {num} generated ({len(r.content)} bytes)")
            return True
        else:
            print(f"  ✗ Frame {num} failed: HTTP {r.status_code}, size {len(r.content)}")
            return False
    except Exception as e:
        print(f"  ✗ Frame {num} error: {e}")
        return False

def main():
    print(f"Generating {len(FRAMES)} frames for Astra United scroll animation...\n")
    success = 0
    for i, prompt in enumerate(FRAMES):
        print(f"[{i+1}/{len(FRAMES)}] Generating frame_{i+1:03d}.png...")
        if generate_frame(i, prompt):
            success += 1
        # Small delay to be respectful to the API
        time.sleep(1.5)
    print(f"\nDone! {success}/{len(FRAMES)} frames generated successfully.")
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()
