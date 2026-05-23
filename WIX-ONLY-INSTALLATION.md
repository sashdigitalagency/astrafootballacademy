# Wix-Only Installation

This setup keeps the live motion experience inside Wix. GitHub is only for source control.

## What You Upload To Wix

Upload these files to **Wix Media Manager**:

- `assets/logo.png`
- `frames_story_web/frame_001.webp`
- `frames_story_web/frame_002.webp`
- `frames_story_web/frame_003.webp`
- `frames_story_web/frame_004.webp`
- `frames_story_web/frame_005.webp`
- `frames_story_web/frame_006.webp`
- `frames_story_web/frame_007.webp`
- `frames_story_web/frame_008.webp`
- `frames_story_web/frame_009.webp`
- `frames_story_web/frame_010.webp`
- `frames_story_web/frame_011.webp`
- `frames_story_web/frame_012.webp`
- `frames_story_web/frame_013.webp`
- `frames_story_web/frame_014.webp`
- `frames_story_web/frame_015.webp`
- `frames_story_web/frame_016.webp`
- `frames_story_web/frame_017.webp`
- `frames_story_web/frame_018.webp`
- `frames_story_web/frame_019.webp`
- `frames_story_web/frame_020.webp`

Copy the Wix URL for each uploaded file.

## Update The Embed Code

Open `astrascroll.html` and find this block:

```javascript
var CONFIG = {
  totalFrames: 20,
  logoUrl: "assets/logo.png",
  frameUrls: [],
  framePrefix: "frames_story_web/frame_",
  frameExt: ".webp",
```

Replace `logoUrl` with the Wix logo URL.

Replace `frameUrls: []` with your 20 Wix frame URLs:

```javascript
frameUrls: [
  "https://static.wixstatic.com/media/...frame_001.webp",
  "https://static.wixstatic.com/media/...frame_002.webp",
  "https://static.wixstatic.com/media/...frame_003.webp",
  "https://static.wixstatic.com/media/...frame_004.webp",
  "https://static.wixstatic.com/media/...frame_005.webp",
  "https://static.wixstatic.com/media/...frame_006.webp",
  "https://static.wixstatic.com/media/...frame_007.webp",
  "https://static.wixstatic.com/media/...frame_008.webp",
  "https://static.wixstatic.com/media/...frame_009.webp",
  "https://static.wixstatic.com/media/...frame_010.webp",
  "https://static.wixstatic.com/media/...frame_011.webp",
  "https://static.wixstatic.com/media/...frame_012.webp",
  "https://static.wixstatic.com/media/...frame_013.webp",
  "https://static.wixstatic.com/media/...frame_014.webp",
  "https://static.wixstatic.com/media/...frame_015.webp",
  "https://static.wixstatic.com/media/...frame_016.webp",
  "https://static.wixstatic.com/media/...frame_017.webp",
  "https://static.wixstatic.com/media/...frame_018.webp",
  "https://static.wixstatic.com/media/...frame_019.webp",
  "https://static.wixstatic.com/media/...frame_020.webp"
],
```

Keep the order exactly from `001` to `020`.

## Add The Hero In Wix

1. Open the Wix page.
2. Add a full-height hero section.
3. Add an **HTML iframe / Embed HTML** element.
4. Choose **Code** mode.
5. Paste the full updated contents of `astrascroll.html`.
6. Set the iframe title/name to:

```text
Astra United Motion
```

7. Stretch the iframe to the full hero section:
   - Width: `100%`
   - Height: full viewport / hero height
   - No margins
   - No section padding

## Add The Scroll Driver In Wix

The HTML embed runs inside an iframe, so the parent Wix page must send scroll progress into it.

In Wix **Custom Code**, add a new code snippet on the page that contains the hero.

Paste the full contents of:

```text
wix-scroll-driver.js
```

Place it at **Body - end**.

## Publish And Test

Test on the published Wix site, not only inside the editor.

Checklist:

- The first frame loads in the hero.
- Scrolling the page advances the motion.
- The action section shows one ball, not ghosted duplicate balls.
- The final frame appears near the end of the hero scroll.
- Mobile view does not show iframe scrollbars.
- The iframe is not cropped.

## Troubleshooting

If the motion does not move:

- Confirm `wix-scroll-driver.js` was added to the parent page, not inside the HTML iframe.
- Confirm the iframe title/name contains `Astra United Motion`.
- Confirm the custom code is set to load on the correct page.
- Test after publishing.

If frames do not load:

- Confirm all 20 frame URLs are public Wix media URLs.
- Confirm the order is `001` to `020`.
- Confirm each URL is wrapped in quotes and separated with commas.

If the hero has scrollbars:

- Increase the iframe height.
- Remove padding/margins from the Wix hero section.
- Make the iframe full width and full height.
