# Tovi Nest — Motion videos (9:16, 1080x1920, 30 fps, H.264 MP4)

| File | Length | What |
|---|---|---|
| `tovinest-01-whats-in-the-box.mp4` | 17s | Unboxing explainer: title → box label callouts → 16 tiles fly in and count up → assembled mat with dimension lines → price + CTA |
| `tovinest-02-specs-size-guide.mp4` | 19.5s | Kinetic size guide: "Will it fit?" → 67 × 48 in counters drawing on the mat → 0.5 in thickness → crib / play yard / toddler drawn to scale → spec chips + price |
| `tovinest-03-rainboho-vs-ash-starlight.mp4` | 18s | Design reveal: RainBoho vs Ash Starlight → each design → "Same mat. Different vibe." → 2 for $89 CTA |

- Audio: a silent stereo AAC track (no music), so you can add a trending sound in TikTok/CapCut.
- Text stays out of the top ~230px and bottom ~330px, where TikTok's UI and captions sit.

## Editing
```bash
cd _src
python3 gen_motion.py   # writes build/*.html (open one in Chrome to watch it live)
node render.js          # renders ../*.mp4   (node render.js 02 renders just one)
```
Timings, copy and prices are in `_src/gen_motion.py`; animations are in `_src/motion.css`.
It reuses the carousel kit in `../carousels/_src/` (icons, mat renders, fonts, styles).
