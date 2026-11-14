# Tovi Nest video pipeline (safe-zone rebuild)

`vlib.py` is a drop-in replacement for the old `content-v2/_build/vlib.py`. It keeps the same function
names and signatures, so existing builders keep running. Every text layer it draws is now laid out
for **IG Reels + TikTok**:

| Rule | How vlib enforces it |
|---|---|
| Text safe box **x 40–900, y 320–1400** | `SAFE`; every hook / caption / pill / sticker / CTA / mascot box is clamped (`clamp_xy`, `safe_paste`). Old hard-coded `y=` values are re-mapped into bands, not trusted. |
| Bands | hook 320–520 · captions 1080–1340 · endcard captions 930–1130 · CTA 1258–1344 · AI label 1356–1398 |
| ≤ 2 lines, wrap ≤ 860 px, never mid-word | `fit_lines()`: word wrap, then auto-shrink in 2 px steps down to 56 px (36 px for disclaimers) |
| No overshoot past the clamp | entrance animations scale 0.88 → 1.0 (never above 1.0) |
| Captions readable | grouped by clause (`, . ? ! ; :`), short groups merged, held **≥ 1.5 s** and **0.35 s** after the last word; active word in mustard `#E9B041` |
| Endcard | logo + tagline + `$49.99` sticker + `2 for $89.99` + "Always supervise children during play." inside the 1080×1350 crop; CTA pill **"DM to order · Ships across the USA"** in the CTA band |
| Pricing / CTA | `fix_copy()` runs on every string: `$39.99`→`$49.99`, `2 for $89`→`2 for $89.99`, removes "launch price", "Shop on TikTok Shop"→DM CTA |
| AI label | `ai_label(im)` draws "AI-generated" inside the safe box (not at y=36) |
| Encode spec | `mux()`: 1080×1920, SAR 1:1, H.264 High yuv420p, 30 fps, CRF 19, AAC 48 kHz stereo 192 kbps, `+faststart` |
| Cover | `make_cover(path, title, hero)`: 1080×1920, logo + title inside the 1080×1350 crop |
| Self-check | `Video.close()` writes `<silent>.mp4.qa.json`: any box outside SAFE, any text held < 1.5 s, any text that needed > 2 lines |

## Install
Copy into your build folder next to `lib.py`, replacing the old `vlib.py`:
```bash
cp video-pipeline/vlib.py video-pipeline/v01.py video-pipeline/v02.py video-pipeline/qa_contact.py /workspace/content-v2/_build/
cd /workspace/content-v2/_build
```

## Run
```bash
python3 v01.py      # -> /workspace/content-v2/posts/01/01_dino_got_a_delivery.mp4 + posts/01/cover.jpg
python3 v02.py      # -> /workspace/content-v2/posts/02/02_dinos_new_nest.mp4      + posts/02/cover.jpg
python3 v01.py 2 6.5 13          # preview stills -> /tmp/v01_<t>.jpg (same for v02.py)
python3 qa_contact.py /workspace/content-v2/posts/01/01_dino_got_a_delivery.mp4 --out /workspace/content-v2/_qa/01
```
`qa_contact.py` writes `contact-sheet.png` (frame every 1 s, red safe box, blue IG grid crop, shaded UI zones) and
`contact-sheet-raw.png`, and prints the vlib QA verdict for that video.

## Scripts that were not attached
`v3_videos.py` (01/04/10), `v03.py`, `vprod.py` (09) and `/tmp/build_dino_falls.py` weren't attached, so they aren't in
this folder. The first three import `vlib`, so **just running them against this vlib** already:
moves every `hook(... y=170..300)` into the 320+ band, moves every `draw_caption(... y=1720/1580/470)` into the
1080–1340 band with 1.5 s holds, moves the `endcard()` CTA from y=1420 to the CTA band with the new prices, and pulls
`price_sticker(im, 850, 760, r=150)` (04) back inside x ≤ 900.

What vlib can't move, because those scripts paste these layers directly, needs a one-line change each:

| Script | Change |
|---|---|
| `v03.py` | stamps at y=1450 / "Wipe clean" stamp / thickness card (y 1180–1600): draw text with `safe_text(im, "...", fred(64,600), band="caption")` and paste cards/Dino with `safe_paste(im, layer, x, y)` |
| all | Dino / mascot pastes: `im.alpha_composite(img,(x,y))` → `safe_paste(im, img, x, y, shadow_y=True)` |
| all | captions on the endcard: `endcard(im, tt, 0.0, groups=G, caption_t=t)` instead of skipping `draw_caption` after the endcard starts |
| all | after `mux(...)`: `make_cover('/workspace/content-v2/posts/<id>/cover.jpg', '<title>', hero=<image>)` |
| `build_dino_falls.py` | replace `draw_caption_block(...)` with `safe_text(im, txt, fred(64,600), band="caption", fill=BROWN)` (pill bottom ≤ 1400); replace `make_end_card(...)` with `endcard(im, tt, 0.0)` (keeps $49.99 / 2 for $89.99 + supervise line inside y 320–1400); replace the AI badge at (36, 36) with `ai_label(im)` |

`v01.py` and `v02.py` here are the full rewritten builders (same inputs, outputs and asset names).

## Test without the real assets
`tests/run_mock.py` renders `v01.py` and `v02.py` against `tests/mock/lib.py`, a stand-in for your `lib.py`, using
placeholder assets, then runs `qa_contact.py`. It needs ffmpeg, Pillow, numpy and opencv-python-headless, and fetches
the fonts on first run.
```bash
cd video-pipeline && python3 tests/run_mock.py
```

## Note on VO
VO for 01 says "Tap the shop link…" and VO for 04 says "…on our TikTok shop". The burned-in captions transcribe the
audio as spoken, while the on-screen CTA is the DM line. Re-record those lines if you want audio and CTA to match.
