#!/usr/bin/env python3
"""Post-process generated frames: color grade, logo overlay, effects."""
import os
import io
from PIL import Image, ImageEnhance, ImageFilter, ImageDraw
import numpy as np

FRAMES_DIR = "frames"
LOGO_PATH = "logo.png"
OUTPUT_DIR = "frames"

# Astra United color palette
TEAL_NAVY = (10, 14, 23)
DEEP_RED = (220, 38, 38)
WARM_WHITE = (255, 248, 240)


def load_logo(size=120):
    if not os.path.exists(LOGO_PATH):
        return None
    logo = Image.open(LOGO_PATH).convert("RGBA")
    # Maintain aspect ratio
    ratio = size / max(logo.size)
    new_size = (int(logo.size[0] * ratio), int(logo.size[1] * ratio))
    logo = logo.resize(new_size, Image.LANCZOS)
    return logo


def apply_cinematic_grade(img):
    """Apply cinematic color grading: deepen shadows, warm highlights, enhance contrast."""
    # Convert to RGB if needed
    img = img.convert("RGB")
    
    # Enhance contrast
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.15)
    
    # Enhance color saturation slightly
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.1)
    
    # Slight warmth
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)
    
    # Apply subtle color tint using overlay
    arr = np.array(img).astype(np.float32)
    
    # Deepen shadows with navy tint
    shadow_mask = 1 - (arr.mean(axis=2, keepdims=True) / 255)
    arr[:, :, 0] = np.clip(arr[:, :, 0] + shadow_mask.squeeze() * 8, 0, 255)
    arr[:, :, 1] = np.clip(arr[:, :, 1] + shadow_mask.squeeze() * 4, 0, 255)
    arr[:, :, 2] = np.clip(arr[:, :, 2] + shadow_mask.squeeze() * 12, 0, 255)
    
    # Warm highlights
    highlight_mask = arr.mean(axis=2, keepdims=True) / 255
    arr[:, :, 0] = np.clip(arr[:, :, 0] + highlight_mask.squeeze() * 10, 0, 255)
    arr[:, :, 1] = np.clip(arr[:, :, 1] + highlight_mask.squeeze() * 5, 0, 255)
    
    img = Image.fromarray(arr.astype(np.uint8))
    return img


def add_vignette(img, strength=0.25):
    """Add cinematic vignette."""
    width, height = img.size
    # Create radial gradient mask
    x = np.linspace(-1, 1, width)
    y = np.linspace(-1, 1, height)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    mask = 1 - np.clip(R / np.sqrt(2), 0, 1) * strength
    mask = (mask * 255).astype(np.uint8)
    mask_img = Image.fromarray(mask).convert("L")
    
    # Apply mask
    img = img.convert("RGB")
    dark = Image.new("RGB", (width, height), (0, 0, 0))
    img = Image.composite(img, dark, mask_img)
    return img


def add_logo_overlay(img, logo, position="bottom-right", opacity=0.85):
    """Add subtle logo watermark."""
    if logo is None:
        return img
    img = img.convert("RGBA")
    logo_copy = logo.copy()
    
    # Adjust logo opacity
    alpha = logo_copy.split()[3]
    alpha = alpha.point(lambda p: int(p * opacity))
    logo_copy.putalpha(alpha)
    
    # Position
    padding = 25
    if position == "bottom-right":
        x = img.width - logo_copy.width - padding
        y = img.height - logo_copy.height - padding
    elif position == "bottom-center":
        x = (img.width - logo_copy.width) // 2
        y = img.height - logo_copy.height - padding
    else:
        x = padding
        y = padding
    
    img.paste(logo_copy, (x, y), logo_copy)
    return img


def process_frame(frame_path, idx, total, logo):
    """Process a single frame."""
    try:
        img = Image.open(frame_path)
    except Exception as e:
        print(f"  ✗ Could not open {frame_path}: {e}")
        return False
    
    # Resize to consistent 1280x720
    img = img.resize((1280, 720), Image.LANCZOS)
    
    # Cinematic color grade
    img = apply_cinematic_grade(img)
    
    # Vignette
    img = add_vignette(img, strength=0.3)
    
    # Logo overlay on all frames (subtle)
    img = add_logo_overlay(img, logo, position="bottom-right", opacity=0.6)
    
    # Final frames (13-15) get stronger logo and effects
    if idx >= 12:
        img = add_logo_overlay(img, logo, position="bottom-center", opacity=0.9)
    
    # Save
    img = img.convert("RGB")
    img.save(frame_path, "PNG", optimize=True)
    print(f"  ✓ Processed frame_{idx+1:03d}.png")
    return True


def main():
    print("Loading logo...")
    logo = load_logo(size=100)
    if logo:
        print(f"  Logo loaded: {logo.size}")
    else:
        print("  No logo found, skipping overlay.")
    
    frame_files = sorted([
        f for f in os.listdir(FRAMES_DIR)
        if f.startswith("frame_") and f.endswith(".png")
    ])
    
    if not frame_files:
        print(f"No frames found in {FRAMES_DIR}")
        return
    
    print(f"\nPost-processing {len(frame_files)} frames...\n")
    success = 0
    for i, fname in enumerate(frame_files):
        path = os.path.join(FRAMES_DIR, fname)
        if process_frame(path, i, len(frame_files), logo):
            success += 1
    
    print(f"\nDone! {success}/{len(frame_files)} frames processed.")

if __name__ == "__main__":
    main()
