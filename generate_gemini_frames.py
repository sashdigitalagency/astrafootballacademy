#!/usr/bin/env python3
"""Generate cinematic frames for Astra United using Gemini image generation."""
import os
import io
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image

load_dotenv()
client = genai.Client()

OUTPUT_DIR = "frames"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Cinematic style prefix applied to all prompts
STYLE_PREFIX = (
    "Cinematic photorealistic football scene, stadium floodlights, "
    "dramatic lighting, green pitch, professional sports photography, "
    "8k quality, film grain, anamorphic lens, motion energy, "
    "anatomically correct players, navy blue and red kits. "
)

FRAMES = [
    # Frame 01 — Establishing shot
    "Wide establishing shot of empty professional football stadium at dusk, "
    "vibrant green pitch, dramatic dark clouds with orange sunset glow, "
    "floodlights creating beams of light, photorealistic, 16:9",
    
    # Frame 02 — Players enter
    "Wide shot of three football players in dark navy blue and red striped kits "
    "on green pitch at dusk, one player dribbling ball forward, teammates sprinting ahead, "
    "stadium floodlights casting long shadows, cinematic motion blur, photorealistic",
    
    # Frame 03 — Dribbling
    "Medium shot of football midfielder in navy blue and red kit dribbling ball on green pitch, "
    "determined focused posture, stadium lights in background, shallow depth of field, "
    "dust particles in air, photorealistic",
    
    # Frame 04 — Looking up
    "Close medium shot of football player in navy and red kit looking up while running with ball, "
    "scanning for pass, dramatic side lighting from stadium floodlights, green pitch below, "
    "intense concentration, photorealistic",
    
    # Frame 05 — The pass
    "Wide shot of football player in navy and red kit making a powerful pass with right foot, "
    "ball just leaving foot, teammates running into space ahead, stadium floodlights, "
    "green pitch, motion blur on ball, photorealistic",
    
    # Frame 06 — Ball in air
    "Cinematic shot of football in mid-air traveling across green pitch at dusk, "
    "stadium floodlights creating lens flares, motion blur trail behind ball, "
    "grass particles flying, dramatic lighting, photorealistic",
    
    # Frame 07 — Wing control
    "Medium shot of winger in navy and red kit controlling ball on the right wing, "
    "body angled toward goal, defender in background, stadium lights, green pitch, "
    "cinematic action, photorealistic",
    
    # Frame 08 — Cut inside
    "Dynamic action shot of winger in navy and red kit cutting inside with ball, "
    "sharp turn, defender sliding tackle, grass kicking up, stadium floodlights, "
    "dramatic sports action, photorealistic",
    
    # Frame 09 — The cross
    "Wide shot of winger in navy and red kit crossing ball into penalty box with left foot, "
    "ball arcing through air, striker waiting in box, goalkeeper preparing, "
    "stadium lights, green pitch, photorealistic",
    
    # Frame 10 — Ball arcs
    "Cinematic shot of football arcing through air toward goal area, spinning ball, "
    "stadium floodlights creating bokeh, green pitch below, dramatic dusk sky, "
    "motion blur, photorealistic",
    
    # Frame 11 — The leap
    "Dramatic shot of striker in navy and red kit leaping high for powerful header, "
    "arms outstretched, eyes focused on ball, stadium floodlights backlighting silhouette, "
    "green pitch below, peak athletic moment, photorealistic",
    
    # Frame 12 — Header connection
    "Intense freeze-frame of striker in navy and red kit connecting with header, "
    "ball compressing against forehead, muscles tense, stadium lights, green pitch, "
    "peak action moment, photorealistic",
    
    # Frame 13 — Goal!
    "Dramatic shot of football smashing into goal net from close range, net bulging and stretching, "
    "fragments of grass flying, stadium floodlights, goalpost visible, peak action moment, "
    "photorealistic",
    
    # Frame 14 — Celebration
    "Wide shot of three football players in navy and red kits celebrating goal together, "
    "arms raised in triumph, running toward camera, stadium floodlights, green pitch, "
    "joy and excitement, photorealistic, red lighting",
    
    # Frame 15 — Cinematic logo moment
    "Cinematic abstract football atmosphere, deep navy blue and red tones, "
    "subtle stadium lights in distance, glowing red light flare, atmospheric dust particles, "
    "dramatic film grain, moody and powerful, photorealistic",
]


def generate_frame(idx, prompt):
    num = f"{idx + 1:03d}"
    out_path = os.path.join(OUTPUT_DIR, f"frame_{num}.png")
    if os.path.exists(out_path) and os.path.getsize(out_path) > 10000:
        print(f"  Frame {num} already exists, skipping.")
        return True

    full_prompt = STYLE_PREFIX + prompt
    print(f"  Generating frame {num}...")
    
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
                # Convert to RGB if needed and save
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(out_path, 'PNG')
                print(f"  ✓ Frame {num} saved ({os.path.getsize(out_path)} bytes)")
                return True
        
        print(f"  ✗ Frame {num}: No image in response")
        return False
        
    except Exception as e:
        print(f"  ✗ Frame {num} error: {type(e).__name__}: {str(e)[:200]}")
        return False


def main():
    print(f"Generating {len(FRAMES)} frames using Gemini image generation...\n")
    success = 0
    for i, prompt in enumerate(FRAMES):
        print(f"[{i+1}/{len(FRAMES)}] frame_{i+1:03d}.png")
        if generate_frame(i, prompt):
            success += 1
        # Small delay to respect rate limits
        time.sleep(2)
    
    print(f"\n{'='*50}")
    print(f"Done! {success}/{len(FRAMES)} frames generated successfully.")
    print(f"Output directory: {os.path.abspath(OUTPUT_DIR)}")


if __name__ == "__main__":
    main()
