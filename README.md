# Astra United Story Scroll Motion

Production-ready Wix embed for a cinematic football academy hero section. The current direction is a grounded 1v1 story: an Astra player wins pressure, flicks the ball up, strikes a controlled side-volley, lands safely, and watches the finish.

## Deliverables

| Path | Purpose |
| --- | --- |
| `astrascroll.html` | Main Wix HTML embed with canvas-based frame scrubbing |
| `wix-scroll-driver.js` | Optional parent-page scroll driver for Wix iframe embeds |
| `frames_story/frame_001.png` to `frame_020.png` | Raw Gemini-generated story keyframes |
| `frames_story_web/frame_001.webp` to `frame_020.webp` | Optimized browser frames used by `astrascroll.html` |
| `dist/astra-story-scroll-motion.mp4` | 8-second H.264 fallback video |
| `dist/astra-story-scroll-motion.webm` | 8-second VP9 fallback video |
| `review/story-contact-sheet.jpg` | Quick visual review sheet for the generated sequence |

## Local Setup

Create and use the repo-local virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create `.env` locally with your Gemini key:

```dotenv
GEMINI_API_KEY=your_key_here
```

The `.env` file is ignored and should not be committed.

## Generate Frames

The story generator uses two local references:

| Reference | Path |
| --- | --- |
| Uniform reference | `assets/uniform-reference.png` |
| Club badge/logo | `logo.png` |

Run:

```powershell
.\.venv\Scripts\python.exe generate_story_motion_frames.py
```

The script writes raw PNGs into `frames_story/`.

## Optimize Frames

Run:

```powershell
$env:ASTRA_SOURCE_DIR='frames_story'
$env:ASTRA_OUTPUT_DIR='frames_story_web'
$env:ASTRA_REVIEW_SHEET='story-contact-sheet.jpg'
.\.venv\Scripts\python.exe postprocess_premium_frames.py
```

This creates the optimized WebP frame sequence in `frames_story_web/` and a contact sheet in `review/`.

## Render Fallback Video

Run:

```powershell
$env:ASTRA_VIDEO_SOURCE_DIR='frames_story_web'
$env:ASTRA_VIDEO_WORK_DIR='video_frames_story'
$env:ASTRA_VIDEO_BASENAME='astra-story-scroll-motion'
.\.venv\Scripts\python.exe render_premium_video.py
```

This renders an 8-second MP4 and WebM into `dist/`. The temporary JPEG frames are ignored.

## Preview

```powershell
.\.venv\Scripts\python.exe -m http.server 5174 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:5174/astrascroll.html
```

## Wix Integration

1. Upload `astrascroll.html` into a Wix HTML embed, or paste its code into a Wix embed block.
2. Upload `assets/logo.png` and all files in `frames_story_web/` to Wix Media Manager.
3. Replace the local paths in `astrascroll.html` with the Wix-hosted asset URLs:

```javascript
framePrefix: "https://static.wixstatic.com/.../frame_",
frameExt: ".webp"
```

4. Set the iframe title or name to `Astra United Motion` so the parent scroll driver can find it.
5. Use the iframe at full viewport height in the hero section.
6. Add `wix-scroll-driver.js` to the parent Wix page using a custom code block when the iframe cannot receive normal page scroll events.

The embed supports both standalone scroll and parent-page scroll messages:

```javascript
{ type: "astra-scroll-progress", progress: 0.0 to 1.0 }
```
