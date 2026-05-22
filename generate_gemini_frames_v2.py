#!/usr/bin/env python3
"""
Generate cinematic frames for Astra United scroll animation — V2
Focus: consistency, logo on kits, same players, same stadium
"""
import os
import io
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
client = genai.Client()

OUTPUT_DIR = "frames_v2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ===================================================================
#  MASTER DIRECTOR'S BRIEF — This context prepends every frame
# ===================================================================
MASTER_CONTEXT = """You are generating frames for a professional football club promotional film.

THE CLUB:
- Name: Astra United Football Club
- Logo: A shield-shaped badge with "ASTRA UNITED" in bold white letters, a star-patterned football, red wings. The badge MUST appear on the left chest of every player's kit.

THE PLAYERS (same three men in every frame):
- PLAYER A — Midfielder, #8. Dark brown short hair, light stubble beard, athletic build, Caucasian, age 26. Navy blue kit with red vertical stripes, white socks with red trim.
- PLAYER B — Winger, #11. Light brown/blonde short hair, clean shaven, lean athletic build, Caucasian, age 24. Same kit.
- PLAYER C — Striker, #9. Very short black hair, no beard, muscular build, Caucasian, age 28. Same kit.

THE STADIUM (identical in every frame):
- Astra United home ground: modern 30,000-seat stadium
- Red and navy blue seats visible in stands
- Four tall LED floodlight pylons at each corner
- Green grass pitch with white line markings
- Slight dampness on grass (evening dew)
- Crowd visible but blurred in background

THE BALL:
- Standard white pentagon/black hexagon classic football
- Slightly scuffed match ball

LIGHTING & ATMOSPHERE:
- Friday evening match, kickoff 8pm
- Overcast dusk sky, deep blue and orange gradient
- Stadium floodlights on, creating dramatic beams and slight haze
- Cinematic film look, slight lens flare, subtle film grain
- Anamorphic lens characteristics

CRITICAL RULES:
1. ALL THREE PLAYERS must wear the Astra United badge on their LEFT CHEST.
2. Player faces should remain recognizably consistent across all frames.
3. The stadium architecture must remain consistent.
4. The ball must always be the classic black and white pattern.
5. Photorealistic, 8k, sports photography, no cartoon or illustration style.
"""

# ===================================================================
#  SHOT LIST — 15 frames with specific camera directions
# ===================================================================
SHOTS = [
    {
        "num": "001",
        "desc": "EXTREME WIDE establishing shot from behind the goal. Empty green pitch stretching toward the opposite goal. The four floodlight pylons visible. Red and navy seats in stands. Dramatic dusk sky with orange glow on horizon. No players visible yet. Cinematic atmosphere, slight ground mist."
    },
    {
        "num": "002",
        "desc": "WIDE shot from halfway line. PLAYER A (#8, dark hair, stubble) dribbling ball up the center of the pitch. PLAYER B (#11, lighter hair, clean shaven) sprinting ahead to the right. PLAYER C (#9, short black hair) running forward to the left. All three facing away from camera, moving toward the opposite goal. Floodlights creating long shadows behind them."
    },
    {
        "num": "003",
        "desc": "MEDIUM-LOW tracking shot from behind and slightly to the left of PLAYER A (#8). He is dribbling the ball with his right foot, body leaning forward, focused. We can see his face in three-quarter profile — concentrated expression, stubble visible. The Astra United badge clearly on his chest. Green pitch, white lines, stadium lights in background."
    },
    {
        "num": "004",
        "desc": "CLOSE-UP side profile of PLAYER A (#8) as he looks up while running. His eyes are scanning the field ahead. Sweat visible on forehead. Mouth slightly open, breathing hard. Astra United badge on chest. Stadium floodlights creating rim lighting on his face and shoulders. Green pitch below, blurred crowd behind."
    },
    {
        "num": "005",
        "desc": "WIDE shot from 45-degree angle. PLAYER A (#8) making a right-footed pass across the field. His body is twisted in the follow-through motion. The ball has just left his foot and is visible mid-air. PLAYER B (#11) is visible in the distance, raising his hand to signal. PLAYER C (#9) continues his run. Stadium lights, green pitch, crowd in stands."
    },
    {
        "num": "006",
        "desc": "CLOSE-UP tracking shot of the ball traveling through the air. The classic black and white ball is spinning slightly, motion blur trail. Stadium floodlights create a beautiful bokeh in the background. Green pitch far below. The ball is the hero of the shot, filling 30% of the frame. Dramatic dusk sky visible."
    },
    {
        "num": "007",
        "desc": "MEDIUM shot from side. PLAYER B (#11, lighter hair, clean shaven) controlling the ball with his right foot on the right wing. He is looking down at the ball, body angled forward. The Astra United badge visible on his chest. A defender in red kit is visible in the background, approaching. Green pitch, white sideline, stadium lights."
    },
    {
        "num": "008",
        "desc": "DYNAMIC action shot from low angle. PLAYER B (#11) cutting inside sharply, dragging the ball with his left foot. His body is leaning into the turn, left arm out for balance. A defender is sliding on the grass behind him. Grass and mud kicking up from the turf. Astra United badge on chest. Stadium lights, dramatic motion."
    },
    {
        "num": "009",
        "desc": "WIDE shot from behind PLAYER B (#11). He is crossing the ball with his left foot into the penalty box. His body is angled, left leg extended in the follow-through. The ball is visible arcing through the air. PLAYER C (#9, striker) is visible in the penalty box, preparing to jump. Goalkeeper in green visible near goal line. Stadium, floodlights, crowd."
    },
    {
        "num": "010",
        "desc": "CLOSE-UP of the ball arcing through the air toward the goal. The ball is spinning, classic black and white pattern clearly visible. In the blurred background, we can see PLAYER C (#9) leaping and the goalkeeper raising his arms. Stadium floodlights create a halo effect. Green pitch below. Dramatic moment frozen in time."
    },
    {
        "num": "011",
        "desc": "DRAMATIC wide shot. PLAYER C (#9, short black hair, muscular) leaping high for a header. His body is fully extended, arms out for balance, eyes locked on the ball above him. He is 3 feet off the ground. The Astra United badge visible on his chest. Stadium floodlights backlighting him, creating a slight silhouette effect. Green pitch far below. Crowd blurred in stands. Peak athletic moment."
    },
    {
        "num": "012",
        "desc": "INTENSE close-up of PLAYER C (#9) at the exact moment of header connection. His forehead has just struck the ball. Neck muscles tensed, eyes squeezed shut from effort. The ball is compressing against his forehead. Astra United badge on chest. Floodlights illuminating his face from the side. Sweat flying off. Peak action freeze-frame."
    },
    {
        "num": "013",
        "desc": "DRAMATIC shot from behind the goal. The ball has just hit the back of the net. The net is bulging outward, stretching from the impact. Fragments of grass and water droplets flying in the air. The goalpost and crossbar visible. In the background, PLAYER C (#9) is landing from his header, arms beginning to raise. Stadium floodlights, crowd going wild (blurred)."
    },
    {
        "num": "014",
        "desc": "WIDE celebratory shot. All three players running toward the camera in celebration. PLAYER C (#9) in the center, arms raised high, mouth open shouting in triumph. PLAYER A (#8) to his left, also arms raised, big smile. PLAYER B (#11) to his right, jumping slightly, fist pumped. All three Astra United badges visible. Red and navy stadium seats behind them. Floodlights creating a celebratory glow. Joy, energy, triumph."
    },
    {
        "num": "015",
        "desc": "CINEMATIC abstract atmosphere. Deep navy blue and red color palette. The Astra United logo (shield with star football) appears large and glowing in the center of the frame. Behind it, a blurred stadium atmosphere with floodlights creating red and white bokeh. Dust particles floating in light beams. Dramatic film grain. Moody, powerful, iconic. The club badge is the hero."
    },
]


def generate_frame(shot_info):
    num = shot_info["num"]
    desc = shot_info["desc"]
    out_path = os.path.join(OUTPUT_DIR, f"frame_{num}.png")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        print(f"  Frame {num} already exists, skipping.")
        return True

    # Build the full prompt
    full_prompt = (
        f"{MASTER_CONTEXT}\n\n"
        f"CURRENT SHOT TO GENERATE:\n"
        f"Frame {num} — {desc}\n\n"
        f"Technical specs: photorealistic, 8k quality, cinematic sports photography, "
        f"16:9 widescreen, film grain, anamorphic lens look, dramatic lighting."
    )

    print(f"[{num}/15] Generating frame_{num}.png...")
    print(f"  Prompt length: {len(full_prompt)} chars")

    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=['IMAGE'],
                image_config=types.ImageConfig(aspect_ratio='16:9')
            )
        )

        for part in response.parts:
            if part.inline_data:
                image = Image.open(io.BytesIO(part.inline_data.data))
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(out_path, 'PNG')
                size_kb = os.path.getsize(out_path) / 1024
                print(f"  ✓ Frame {num} saved ({size_kb:.0f} KB)")
                return True

        print(f"  ✗ Frame {num}: No image data in response")
        return False

    except Exception as e:
        print(f"  ✗ Frame {num} error: {type(e).__name__}: {str(e)[:300]}")
        return False


def main():
    print("=" * 60)
    print("ASTRA UNITED — Frame Generation V2")
    print("Focus: Consistency, Logo on Kits, Same Players")
    print("=" * 60)
    print(f"\nGenerating {len(SHOTS)} frames...\n")

    success = 0
    for shot in SHOTS:
        if generate_frame(shot):
            success += 1
        time.sleep(2)  # Respect API rate limits

    print(f"\n{'=' * 60}")
    print(f"Done! {success}/{len(SHOTS)} frames generated.")
    print(f"Output: {os.path.abspath(OUTPUT_DIR)}")
    print("=" * 60)


if __name__ == "__main__":
    main()
