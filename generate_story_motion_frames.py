#!/usr/bin/env python3
"""Generate a more believable Astra United scroll-motion story.

This version avoids the old two-player airborne duel because that prompt creates
impossible body mechanics and duplicate-ball artifacts. The story is a grounded
1v1 that becomes one controlled side-volley strike.
"""
from __future__ import annotations

import io
import json
import mimetypes
import os
import time
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image


ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = ROOT / "frames_story"
REFERENCE_DIR = ROOT / "assets"
MODEL = os.getenv("GEMINI_IMAGE_MODEL", "gemini-2.5-flash-image")
ASPECT_RATIO = "16:9"
FRAME_DELAY_SECONDS = float(os.getenv("ASTRA_FRAME_DELAY", "2.0"))

REFERENCE_IMAGES = [
    REFERENCE_DIR / "uniform-reference.png",
    ROOT / "logo.png",
]


@dataclass(frozen=True)
class Shot:
    num: int
    beat: str
    camera: str
    action: str
    ball: str
    focus: str


MASTER_BRIEF = """
Create a premium cinematic scroll-motion sequence for Astra United Football Academy.

References provided:
- Reference A: exact Astra United navy kit, red accents, player styling, badge placement.
- Reference B: Astra United badge/logo. The badge must appear on the LEFT CHEST of the main player.

Story title: THE BREAKTHROUGH STRIKE
Story logic:
- One main Astra United academy player wins a realistic 1v1, flicks the ball up, strikes a controlled side-volley, lands safely, and watches the shot.
- A second player can appear as a defender/training partner only during the pressure/cutback beats. The defender stays grounded and at least two meters away from the striking leg.
- The hero action belongs to ONE player. Never make two players kick the same airborne ball.

World and style:
- Night training ground under floodlights, damp grass, slight mist, dark navy sky, subtle red accent light.
- Photorealistic sports-commercial photography, 8k detail, cinematic color grade, shallow depth of field, anamorphic lens flare.
- Same main player across all frames: athletic young adult male, dark hair, focused expression, navy Astra kit, white/grey boots.

Critical continuity rules:
1. EXACTLY ONE football visible in each frame.
2. The ball must follow a believable path: grass -> dribble -> flick upward -> side-volley strike -> ball flight.
3. The main player must obey real football body mechanics: planted foot before strike, controlled torso rotation, safe landing.
4. No floating bodies, no impossible horizontal hovering, no mirrored airborne duel, no two balls.
5. Keep the Astra badge visible when the chest faces camera, but do not add any watermark or floating logo.
6. Use subtle dew/turf flecks only. No huge grass explosion, no confetti, no magical particles.
""".strip()


NEGATIVE_GUARDRAILS = """
Avoid: two footballs, duplicate ball, ball in two places, second player kicking the ball, two players airborne,
boot hitting another player, tangled legs, impossible knees, floating player, bicycle-kick duel, player kicking a leg,
extra limbs, detached feet, deformed hands, red-vs-blue kit mismatch, missing chest badge, watermark, random text,
large floating logo, cartoon, illustration, CGI render, video game look, grass avalanche, sparks, star watermark.
""".strip()


SHOTS = [
    Shot(1, "cold open", "low field-level wide shot, negative space on left", "the ball rests on wet grass under floodlights, the main player approaches from the distance", "one ball on grass in foreground", "quiet anticipation, academy training ground"),
    Shot(2, "first touch", "low sideline tracking shot", "main Astra player enters frame dribbling calmly from left to right", "one ball close to his right boot on the ground", "kit and badge readable, defender distant"),
    Shot(3, "pressure arrives", "medium-wide at waist height", "a defender/training partner closes from the front, main player lowers his shoulder", "one ball rolling between main player's feet", "real 1v1 tension, both players grounded"),
    Shot(4, "scan", "medium close-up, slight dolly push", "main player glances up while shielding the ball with his body", "one ball partly in foreground at his feet", "focused face, badge visible"),
    Shot(5, "drag back", "low dynamic angle near grass", "main player drags the ball back with the sole of his right boot while the defender oversteps safely", "EXACTLY ONE ball, pinned under the main player's sole on the turf; no ball in the air, no second ball anywhere", "clear separation, no contact"),
    Shot(6, "cut inside", "wide low-angle tracking shot", "main player cuts inside past the defender, defender is behind and off balance but still grounded", "one ball moving with the main player's left foot", "clean football mechanics"),
    Shot(7, "separation", "medium-wide, floodlights behind", "main player has created space, plants his left foot and opens his hips", "one ball directly in front of him on grass", "defender two meters behind, out of striking lane"),
    Shot(8, "flick", "low 50mm sports lens", "main player flicks the ball up with the top of his right boot", "one ball just leaving the boot at shin height", "beginning of a believable volley setup"),
    Shot(9, "ball rising", "medium shot, slight slow-motion feel", "main player watches the ball rise and bends his knees to load the strike", "one ball at knee-to-waist height, centered", "left foot planted, torso turning"),
    Shot(10, "coil", "cinematic medium-wide", "main player rotates his torso and lifts his right leg for a controlled side-volley", "one ball at waist height, one meter in front of striking foot", "defender blurred far behind, no danger"),
    Shot(11, "strike", "hero action frame, low sideline angle", "main player executes a realistic side-volley, right boot contacting the single ball, left leg planted or just leaving turf", "one ball at boot contact with slight compression", "anatomically plausible peak action"),
    Shot(12, "release", "same direction, stronger motion energy, keep action inside the center 60 percent of the frame", "the ball leaves the boot and travels forward but remains visible near the center-right safe area, player begins to descend", "EXACTLY ONE ball clearly separated from the boot but not near the frame edge", "clean follow-through, no second ball, mobile-safe composition"),
    Shot(13, "follow through", "wide frame, camera continues tracking", "main player's striking leg follows through across his body, arms balancing", "one ball traveling away through light haze", "body weight moving naturally"),
    Shot(14, "landing", "low sideline shot, turf foreground", "main player lands safely and braces with one hand near the grass", "one ball farther away in the air, smaller", "small turf flecks only"),
    Shot(15, "watch the shot", "medium shot from front three-quarter", "main player rises from the landing and watches the shot's path", "one ball visible high in the background", "badge visible, breathing hard"),
    Shot(16, "ball flight", "telephoto shot toward goal lights", "the ball arcs through floodlight beams toward the training goal", "one ball in the upper third, goal blurred behind", "cinematic depth, no players near ball"),
    Shot(17, "goal moment", "behind-goal low angle, no players inside the goal", "the ball hits the inside side-netting of the small training goal; show the net ripple and the ball only", "EXACTLY ONE ball in the net, no player, no goalkeeper, no second ball", "satisfying story payoff, clean net impact"),
    Shot(18, "recovery", "wide field-level frame", "main player stands, defender behind him, both looking toward the goal", "one ball settled in or near the goal net in the distance", "sportsmanship, academy intensity"),
    Shot(19, "hero calm", "medium-wide, negative space for headline", "main player walks back toward camera with controlled confidence", "one ball carried or resting far behind near goal", "Astra kit, badge, cinematic lighting"),
    Shot(20, "end card frame", "wide cinematic hero composition", "main player stands under floodlights, training goal behind, defender out of focus", "one ball on grass near player's boot", "clean final website hero image"),
]


def load_reference_parts() -> list[types.Part]:
    parts: list[types.Part] = []
    for path in REFERENCE_IMAGES:
        if not path.exists():
            print(f"Reference missing, skipping: {path}")
            continue
        mime_type = mimetypes.guess_type(path.name)[0] or "image/png"
        parts.append(types.Part.from_bytes(data=path.read_bytes(), mime_type=mime_type))
    return parts


def response_parts(response):
    if getattr(response, "parts", None):
        yield from response.parts
    for candidate in getattr(response, "candidates", []) or []:
        content = getattr(candidate, "content", None)
        for part in getattr(content, "parts", []) or []:
            yield part


def prompt_for(shot: Shot) -> str:
    return f"""
{MASTER_BRIEF}

Frame {shot.num:03d} of {len(SHOTS):03d}
Beat: {shot.beat}
Camera: {shot.camera}
Action: {shot.action}
Ball continuity: {shot.ball}
Primary focus: {shot.focus}

Composition requirements:
- 16:9 widescreen website hero frame.
- Main player should occupy a consistent hero scale across action frames.
- Keep the camera believable: sports photographer at field level, not impossible drone angles.
- The sequence must read as a single continuous football action when scrubbed by scroll.
- No typography in the generated image.

{NEGATIVE_GUARDRAILS}
""".strip()


def save_image_from_response(response, out_path: Path) -> bool:
    for part in response_parts(response):
        inline_data = getattr(part, "inline_data", None)
        if not inline_data:
            continue
        image = Image.open(io.BytesIO(inline_data.data))
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(out_path, "PNG")
        return True
    return False


def generate_frame(client: genai.Client, shot: Shot, reference_parts: list[types.Part]) -> bool:
    out_path = OUTPUT_DIR / f"frame_{shot.num:03d}.png"
    force = os.getenv("ASTRA_FORCE", "0") == "1"
    if not force and out_path.exists() and out_path.stat().st_size > 20_000:
        print(f"[{shot.num:03d}] exists, skipping")
        return True

    contents = [prompt_for(shot), *reference_parts]
    print(f"[{shot.num:03d}/{len(SHOTS):03d}] generating {out_path.name}")
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(aspect_ratio=ASPECT_RATIO),
            ),
        )
    except Exception as exc:
        print(f"[{shot.num:03d}] error: {type(exc).__name__}: {str(exc)[:500]}")
        return False

    ok = save_image_from_response(response, out_path)
    if ok:
        print(f"[{shot.num:03d}] saved {out_path.stat().st_size / 1024:.0f} KB")
    else:
        print(f"[{shot.num:03d}] no image data returned")
    return ok


def write_manifest() -> None:
    manifest = {
        "project": "Astra United story scroll motion",
        "model": MODEL,
        "aspect_ratio": ASPECT_RATIO,
        "frame_count": len(SHOTS),
        "duration_seconds": 8,
        "scenario": "The Breakthrough Strike",
        "frames": [
            {
                "file": f"frame_{shot.num:03d}.png",
                "beat": shot.beat,
                "camera": shot.camera,
                "action": shot.action,
                "ball": shot.ball,
            }
            for shot in SHOTS
        ],
    }
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main() -> int:
    load_dotenv(ROOT / ".env")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if not os.getenv("GEMINI_API_KEY"):
        print("Missing GEMINI_API_KEY in .env")
        return 1

    reference_parts = load_reference_parts()
    if len(reference_parts) < 2:
        print("Warning: fewer than two reference images loaded. Consistency may be lower.")

    client = genai.Client()
    only_frames_raw = os.getenv("ASTRA_ONLY_FRAMES", "").strip()
    only_frames = None
    if only_frames_raw:
        only_frames = {int(value.strip()) for value in only_frames_raw.split(",") if value.strip()}
    success = 0
    selected_shots = [shot for shot in SHOTS if only_frames is None or shot.num in only_frames]
    for shot in selected_shots:
        if generate_frame(client, shot, reference_parts):
            success += 1
        time.sleep(FRAME_DELAY_SECONDS)

    write_manifest()
    print(f"Done: {success}/{len(selected_shots)} frames in {OUTPUT_DIR}")
    return 0 if success == len(selected_shots) else 2


if __name__ == "__main__":
    raise SystemExit(main())
