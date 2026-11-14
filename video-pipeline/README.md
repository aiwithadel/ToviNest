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
Copy into your build folder next to `lib.py`, replacing the old `vlib.py` and builders:
```bash
cp video-pipeline/{vlib.py,v01.py,v02.py,v03.py,v04.py,vprod.py,qa_contact.py} /workspace/content-v2/_build/
cp video-pipeline/build_dino_falls.py /tmp/build_dino_falls.py
cd /workspace/content-v2/_build
```

## Run
| Script | Command | Output (same paths as before) |
|---|---|---|
| 01 | `python3 v01.py` | `posts/01/01_dino_got_a_delivery.mp4` + `posts/01/cover.jpg` |
| 02 | `python3 v02.py` | `posts/02/02_dinos_new_nest.mp4` + `cover.jpg` |
| 03 | `python3 v03.py` | `posts/03/03_dino_crawl_test.mp4` + `cover.jpg` |
| 04 | `python3 v04.py` | `posts/04/04_dino_holiday_gift.mp4` + `cover.jpg` |
| 09 | `python3 vprod.py 09` | `posts/09/09_ash_starlight_showcase.mp4` + `cover.jpg` |
| 10 | `python3 vprod.py 10` | `posts/10/10_rainboho_pov.mp4` + `cover.jpg` |
| dino-falls-01 | `python3 /tmp/build_dino_falls.py` | `posts/dino-falls-01/dino_tumbles_ep01_9x16.mp4` + `cover.jpg`, `episodes.md`, `calendar.csv` |

Preview stills: `python3 v03.py 2 5 7.5 11` (same for v01-v04) or `python3 vprod.py 09 1.5 4 13` → `/tmp/<id>_<t>.jpg`.
QA: `python3 qa_contact.py /workspace/content-v2/posts/03/03_dino_crawl_test.mp4 --out /workspace/content-v2/_qa/03`
(each vlib run also prints `[vlib QA] PASS/CHECK` and writes `/tmp/<id>_silent.mp4.qa.json`; dino-falls prints `[QA]`).

dino-falls uses its own fonts: if yours aren't at the `/usr/share/fonts/truetype/sand-box/google/...` paths, set
`TOVI_FREDOKA=... TOVI_NUNITO=...`. Set `TOVI_LOGO=/path/to/tovinest-primary-logo.png` to put the logo on its cover.

## What changed per script
| Script | Fixes |
|---|---|
| `v01.py` | Hooks into the 320+ band; feature chips under the hook (no caption overlap) and re-timed so the last one holds 2.4 s; captions in the 1080–1340 band and continued on the endcard; crawling Dino clamped; AI label inside the box |
| `v02.py` | Whole floor scene lifted 330 px (`lift_bg`) so Dino's feet are ≤ 1400; endcard tada Dino moved off the right rail into the box |
| `v03.py` | Captions moved from y=1720 to the caption band; "Dino tested it all!" stamped over the checklist (was y=1450); thickness card 640–1040 (was 1180–1600); "Wipe clean · Waterproof" moved up and re-timed (1.6 s); "APPROVED BY DINO" from 10.6 s (1.6 s); tada + crawling Dino clamped; stamps no longer start at 1.8× scale |
| `v04.py` | Hook out of the top UI; captions from y=470 to the caption band; price sticker (was x≈700–1000) clamped to x ≤ 900 and reads "2 MATS FOR $89.99"; Santa / Dino-with-box scaled so feet are ≤ 1400 with no overshoot; endcard Santa inside the box |
| `vprod.py` | Hooks via the safe band, ≤ 2 lines; 'card' photos fitted below the hook inside the safe box; AI label; covers |
| `build_dino_falls.py` | Caption pill in the caption band (was 1477–1608); AI badge into the box (was (36,36)); end card rebuilt inside y 320–1400 with **$49.99 each · 2 for $89.99** (the script had $39.99 / "2 for $89") + DM CTA; `episodes.md` / calendar copy updated to the same prices and the Sterling pickup line replaced with the DM / ships CTA; emoji removed from burned-in text (Fredoka has no emoji glyphs, so they rendered as boxes) but kept in post captions; 48 kHz / 192 kbps audio, SAR 1:1; fixed a latent buffer overflow in `chime()` that crashed the audio step |

## Test without the real assets
`tests/run_mock.py` renders all seven videos against `tests/mock/lib.py`, a stand-in for your `lib.py`, using
placeholder assets, then runs `qa_contact.py`. It needs ffmpeg, Pillow, numpy and opencv-python-headless, and fetches
the fonts on first run.
```bash
cd video-pipeline && python3 tests/run_mock.py            # or: python3 tests/run_mock.py v03 dino
```

## Note on VO
VO for 01 says "Tap the shop link…" and VO for 04 says "…on our TikTok shop". The burned-in captions transcribe the
audio as spoken, while the on-screen CTA is the DM line. Re-record those lines if you want audio and CTA to match.
