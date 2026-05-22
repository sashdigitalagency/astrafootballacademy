# Astra United — Scroll Motion Frame-by-Frame Animation

## Overview
A production-grade, Wix-compatible scroll-driven frame-by-frame animation that tells the story of "The Breakaway" — a 6-second cinematic football sequence featuring three Astra United players executing a counter-attack that ends in a dramatic goal and celebration.

## Deliverables
| File | Description |
|------|-------------|
| `astrascroll.html` | Main Wix embed file — drop this into a Wix HTML iframe |
| `frames/frame_001.png` … `frame_015.png` | 15 cinematic keyframes (post-processed) |
| `assets/logo.png` | Astra United club logo |
| `css/astrascroll.css` | Stylesheet (also inlined in HTML) |
| `js/scroll-engine.js` | Scroll engine (also inlined in HTML) |

## Scenario: "The Breakaway"
1. **Frame 01** — Empty stadium at dusk, floodlights on
2. **Frame 02** — Three players enter, attack begins
3. **Frame 03** — Midfielder dribbling forward
4. **Frame 04** — Player looks up, scanning for pass
5. **Frame 05** — The pass is made
6. **Frame 06** — Ball travels through air
7. **Frame 07** — Winger controls ball on the flank
8. **Frame 08** — Winger cuts inside past defender
9. **Frame 09** — Cross into the penalty box
10. **Frame 10** — Ball arcs toward goal area
11. **Frame 11** — Striker leaps for header
12. **Frame 12** — Header connection moment
13. **Frame 13** — GOAL! Ball hits the net
14. **Frame 14** — Players celebrate together
15. **Frame 15** — Cinematic logo reveal

## Features
- **Canvas-based renderer** for zero-lag frame scrubbing
- **Preloader** with progress bar and animated logo
- **Smooth scroll interpolation** (lerp) for fluid motion between frames
- **Mobile touch support** with momentum scrolling
- **Cinematic overlays** — vignette, film grain, color grading
- **Particle system** — subtle dust and light particles
- **Logo reveal animation** — scales in with tagline on final frames
- **Progress indicator** — red line at top tracks scroll position
- **Responsive** — adapts to any screen size

## Wix Integration

### Step 1: Upload Assets
1. In your Wix Editor, go to **Site Assets** or **Media Manager**
2. Upload all `frame_*.png` files to a folder (e.g., `astra-scroll-frames/`)
3. Upload `logo.png` to the same folder

### Step 2: Create HTML Embed
1. Add an **HTML iframe** element to your page
2. Set its size to **100% width × 100vh height** (full viewport)
3. In the HTML settings, choose **Code** mode (not URL)
4. Paste the contents of `astrascroll.html`

### Step 3: Update Paths
Inside the HTML code, update these paths to match your Wix asset URLs:
```javascript
framePrefix: 'https://your-site.wixsite.com/_files/astra-scroll-frames/frame_',
```
And update the logo src:
```html
<img src="https://your-site.wixsite.com/_files/astra-scroll-frames/logo.png" ...>
```

> **Tip:** Right-click on each uploaded image in Wix Media Manager and select **"Copy URL"** to get the direct link.

### Step 4: Page Setup
- Ensure the Wix page is tall enough for scrolling (the HTML sets `600vh` scroll height automatically)
- For best results, set the section containing the HTML embed to **full bleed** (no margins)

## Customization

### Frame Count
To add more frames:
1. Generate additional PNGs following the `frame_XXX.png` naming
2. Update `totalFrames` in the JavaScript config
3. Adjust scroll height if needed

### Colors
The animation uses Astra United's brand colors:
- **Navy**: `#0a0e17`
- **Red**: `#dc2626`
- **Warm White**: `#fff8f0`

Edit the CSS variables in `astrascroll.html` to adjust.

### Scroll Speed
Adjust `CONFIG.lerpFactor` (default `0.12`):
- Lower = smoother but slower response
- Higher = snappier but potentially jittery

## Technical Notes
- **No external dependencies** — everything is self-contained for Wix compatibility
- **Frame preloading** — all frames load before the experience starts
- **Touch optimization** — custom touch handling for mobile devices
- **Performance** — uses `requestAnimationFrame` and hardware-accelerated transforms

## Expanding to Full 144-Frame Sequence
For an even smoother experience, you can expand this to the full 6-second sequence:
1. Generate 144 frames using a video interpolation tool (e.g., RIFE, DAIN)
2. Update `totalFrames` to `144`
3. The scroll engine will automatically adapt

## Credits
- Animation engine: Custom-built for Astra United Football Club
- Frame generation: Pollinations AI + cinematic post-processing
- Club branding: Astra United FC
