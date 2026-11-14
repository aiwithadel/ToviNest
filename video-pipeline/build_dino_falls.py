#!/usr/bin/env python3
"""Build Dino Tumbles Ep.1 video, episode scripts, and calendar weave (safe-zone rebuild).

Changes vs. the original /tmp/build_dino_falls.py:
  * captions: cream pill was placed at y = 1920-280-box_h (~1477-1608, under the IG/TikTok bottom
    UI). It now sits in the caption band 1080-1340, centred on the safe box (x 40-900), wrapped to
    <= 2 lines (auto-shrunk to >= 56 px), sub-line >= 36 px. Emoji were removed from the burned-in
    text because Fredoka/Nunito have no emoji glyphs (they rendered as boxes); they stay in the
    post captions and calendar copy;
  * AI badge moved from (36,36) (under the top UI) to the AI band inside the safe box (y 1356-1398);
  * end card: packshot and price card were at y 180 / y 1280-1820. Everything now sits inside
    x 40-900 / y 320-1400: packshot 330-760, card 780-1215 ($49.99 each · 2 for $89.99 ·
    Always supervise), CTA pill "DM to order · Ships across the USA" in 1258-1344. No end-card zoom,
    so nothing drifts out of the box;
  * pricing everywhere (end card, episodes.md, calendar): $49.99 each · 2 for $89.99 (was
    $39.99 launch · 2 for $89); Ep.8 "Sterling pickup" line replaced by the DM / ships CTA;
  * audio 48 kHz, AAC 192 kbps stereo; video SAR 1:1; cover.jpg (title + logo inside the 1080x1350 crop);
  * a QA report (safe box + 1.5 s holds) is printed after the frames are built.
Fonts: override with env TOVI_FREDOKA / TOVI_NUNITO if your paths differ.
"""
from __future__ import annotations

import csv
import math
import shutil
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path("/workspace/content-v2")
OUT = ROOT / "posts" / "dino-falls-01"
CAL = ROOT / "calendar.csv"
W, H, FPS = 1080, 1920, 30
DURATION = 14.0  # seconds
NFRAMES = int(DURATION * FPS)

import os
FREDOKA = os.environ.get("TOVI_FREDOKA", "/usr/share/fonts/truetype/sand-box/google/Fredoka/Fredoka-VariableFont_wdth,wght.ttf")
NUNITO = os.environ.get("TOVI_NUNITO", "/usr/share/fonts/truetype/sand-box/google/Nunito/Nunito-VariableFont_wght.ttf")
LOGO = Path(os.environ.get("TOVI_LOGO", "/workspace/brand/tovinest-primary-logo.png"))   # optional, for the cover

# ---- safe zone (same rules as video-pipeline/vlib.py) ----
SAFE = (40, 320, 900, 1400)            # x0, y0, x1, y1: overlap of IG Reels UI, TikTok UI and the IG grid crop
SAFE_W = SAFE[2] - SAFE[0]
SAFE_CX = (SAFE[0] + SAFE[2]) // 2     # 470
CAPTION_BAND = (1080, 1340)
CTA_BAND = (1258, 1344)
AI_BAND = (1356, 1398)
MIN_TEXT, MIN_SMALL, MIN_HOLD = 56, 36, 1.5
PRICE_EACH, PRICE_DUO = "$49.99", "2 for $89.99"
CTA_TEXT = "DM to order · Ships across the USA"
SUPERVISE = "Always supervise your little one."
QA_LOG = []                            # (frame, kind, text, box)
_FRAME = [0]

SAGE = (106, 137, 107)
BROWN = (92, 64, 45)
CREAM = (250, 244, 232)
CORAL = (224, 122, 95)
MUSTARD = (233, 176, 65)
WHITE = (255, 255, 255)


def font(path, size, style=b"Bold"):
    f = ImageFont.truetype(path, size)
    try:
        f.set_variation_by_name(style)
    except Exception:
        try:
            if "Fredoka" in path:
                f.set_variation_by_axes([700, 100])
            else:
                f.set_variation_by_axes([700])
        except Exception:
            pass
    return f


def fit_cover(im: Image.Image, tw=W, th=H) -> Image.Image:
    im = im.convert("RGB")
    scale = max(tw / im.width, th / im.height)
    nw, nh = int(im.width * scale + 0.5), int(im.height * scale + 0.5)
    im = im.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return im.crop((left, top, left + tw, top + th))


def kenburns(base: Image.Image, t: float, t0: float, t1: float, z0=1.0, z1=1.08, pan=(0, 0)):
    """t relative progress 0-1 over the clip, zoom from z0 to z1, optional pan in px of the oversized canvas."""
    p = 0 if t1 == t0 else max(0.0, min(1.0, (t - t0) / (t1 - t0)))
    # ease in-out
    p = p * p * (3 - 2 * p)
    z = z0 + (z1 - z0) * p
    # render from a slightly larger crop
    src_w, src_h = base.size
    cw, ch = int(src_w / z), int(src_h / z)
    # keep odd-pixel safe
    cw, ch = max(2, cw), max(2, ch)
    px = (src_w - cw) / 2 + pan[0] * p
    py = (src_h - ch) / 2 + pan[1] * p
    px = max(0, min(src_w - cw, px))
    py = max(0, min(src_h - ch, py))
    crop = base.crop((int(px), int(py), int(px) + cw, int(py) + ch))
    return crop.resize((W, H), Image.Resampling.LANCZOS)


def rounded_rect(draw, xy, r, fill, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def wrap_text(text, fnt, max_w, draw):
    """Word wrap (never splits a word)."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), trial, font=fnt)
        if bbox[2] - bbox[0] <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


_DUMMY = ImageDraw.Draw(Image.new("RGB", (10, 10)))


def fit_lines(text, path, size, max_w, style=b"SemiBold", max_lines=2, min_size=MIN_TEXT):
    """Shrink until text wraps into <= max_lines lines no wider than max_w."""
    while True:
        f = font(path, size, style)
        lines = wrap_text(text, f, max_w, _DUMMY)
        widest = max(_DUMMY.textbbox((0, 0), ln, font=f)[2] for ln in lines)
        if (len(lines) <= max_lines and widest <= max_w) or size <= min_size:
            if len(lines) > max_lines:
                print(f"WARNING: '{text}' needs {len(lines)} lines at {size}px")
            return f, lines[:max_lines]
        size -= 2


def clamp_xy(x, y, w, h):
    return int(min(max(x, SAFE[0]), SAFE[2] - w)), int(min(max(y, SAFE[1]), SAFE[3] - h))


def qa(kind, text, box):
    QA_LOG.append((_FRAME[0], kind, text, tuple(int(v) for v in box)))


def draw_caption_block(img, text, y=None, sub=None, max_w=None):
    """Cream pill caption inside the caption band (1080-1340), centred on the safe box.
    `y` / `max_w` from old callers are ignored on purpose: the pill always lands in the band."""
    pad_x, pad_y = 36, 24
    title_f, lines = fit_lines(text, FREDOKA, 64, SAFE_W - 2 * pad_x)
    line_h = int(title_f.size * 1.15)
    sub_f, sub_lines = (fit_lines(sub, NUNITO, 38, SAFE_W - 2 * pad_x, max_lines=1, min_size=MIN_SMALL) if sub else (None, []))
    sub_h = int(sub_f.size * 1.3) if sub else 0
    widths = [_DUMMY.textbbox((0, 0), ln, font=title_f)[2] for ln in lines]
    widths += [_DUMMY.textbbox((0, 0), ln, font=sub_f)[2] for ln in sub_lines]
    box_w = min(SAFE_W, max(widths) + pad_x * 2)
    box_h = pad_y * 2 + line_h * len(lines) + sub_h
    b0, b1 = CAPTION_BAND
    x, y = clamp_xy(SAFE_CX - box_w / 2, b0 + max(0, (b1 - b0 - box_h) // 2), box_w, box_h)
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    rounded_rect(ImageDraw.Draw(shadow), (x + 4, y + 8, x + box_w + 4, y + box_h + 8), 36, (40, 30, 20, 60))
    overlay = Image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(10)), overlay)
    d = ImageDraw.Draw(overlay)
    rounded_rect(d, (x, y, x + box_w, y + box_h), 36, (250, 244, 232, 235))
    ty = y + pad_y - 4
    for ln in lines:
        tw = d.textbbox((0, 0), ln, font=title_f)[2]
        d.text((SAFE_CX - tw // 2, ty), ln, font=title_f, fill=BROWN)
        ty += line_h
    for ln in sub_lines:
        tw = d.textbbox((0, 0), ln, font=sub_f)[2]
        d.text((SAFE_CX - tw // 2, ty + 2), ln, font=sub_f, fill=SAGE)
    qa("caption", text, (x, y, x + box_w, y + box_h))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def draw_ai_badge(img):
    """'AI' label inside the safe box (bottom-left AI band), not at (36, 36)."""
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    f = font(NUNITO, MIN_SMALL, b"Bold")
    label = "AI-generated"
    bb = d.textbbox((0, 0), label, font=f)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 6
    x, y = SAFE[0] + 4, AI_BAND[0] + (AI_BAND[1] - AI_BAND[0] - th - 2 * pad) // 2
    rounded_rect(d, (x, y, x + tw + pad * 2 + 8, y + th + pad * 2), 12, (40, 30, 20, 170))
    d.text((x + pad + 4, y + pad - bb[1]), label, font=f, fill=WHITE)
    qa("ai", label, (x, y, x + tw + pad * 2 + 8, y + th + pad * 2))
    return Image.alpha_composite(img.convert("RGBA"), overlay)


def center_text(draw, text, y, fnt, fill, kind="endcard"):
    bb = draw.textbbox((0, 0), text, font=fnt)
    tw = bb[2] - bb[0]
    x, yy = clamp_xy(SAFE_CX - tw / 2, y, tw, bb[3])
    draw.text((x, yy), text, font=fnt, fill=fill)
    qa(kind, text, (x, yy, x + tw, yy + bb[3]))


def make_end_card(packshot_path: Path) -> Image.Image:
    """End card laid out inside the safe box and the 1080x1350 grid crop."""
    base = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(base)
    for i in range(220):                       # subtle top sage wash
        a = 18 * (1 - i / 220)
        d.line([(0, i), (W, i)], fill=tuple(int(c * (a / 255) + CREAM[k] * (1 - a / 255)) for k, c in enumerate(SAGE)))
    box = Image.open(packshot_path).convert("RGBA")
    box.thumbnail((560, 430), Image.Resampling.LANCZOS)          # packshot inside y 330-760
    bx, by = clamp_xy(SAFE_CX - box.width / 2, 330, box.width, box.height)
    sh = Image.new("RGBA", base.size, (0, 0, 0, 0))
    sh.paste((40, 30, 20, 150), (bx + 14, by + 22, bx + 14 + box.width, by + 22 + box.height), Image.new("L", box.size, 150))
    canvas = Image.alpha_composite(base.convert("RGBA"), sh.filter(ImageFilter.GaussianBlur(22)))
    canvas.paste(box, (bx, by), box)
    qa("packshot", "packshot", (bx, by, bx + box.width, by + box.height))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    card_y0, card_y1 = 780, 1220
    rounded_rect(ImageDraw.Draw(overlay), (SAFE[0] + 20, card_y0, SAFE[2] - 20, card_y1), 40, (255, 255, 255, 235))
    canvas = Image.alpha_composite(canvas, overlay)
    d2 = ImageDraw.Draw(canvas)
    center_text(d2, "Perfect gift for moms", card_y0 + 26, font(FREDOKA, 58, b"SemiBold"), BROWN)
    center_text(d2, f"{PRICE_EACH} each", card_y0 + 104, font(FREDOKA, 92, b"Bold"), CORAL)
    center_text(d2, PRICE_DUO, card_y0 + 224, font(FREDOKA, 72, b"Bold"), BROWN)
    center_text(d2, "Peace of mind while they learn.", card_y0 + 322, font(NUNITO, 38, b"SemiBold"), BROWN)
    center_text(d2, SUPERVISE, card_y0 + 372, font(NUNITO, 36, b"SemiBold"), SAGE)
    # CTA pill in the CTA band
    f = font(FREDOKA, 44, b"SemiBold")
    while d2.textbbox((0, 0), CTA_TEXT, font=f)[2] + 68 > SAFE_W - 20 and f.size > MIN_SMALL:
        f = font(FREDOKA, f.size - 2, b"SemiBold")
    tw = d2.textbbox((0, 0), CTA_TEXT, font=f)[2]
    pw, ph = tw + 68, CTA_BAND[1] - CTA_BAND[0]
    px, py = clamp_xy(SAFE_CX - pw / 2, CTA_BAND[0], pw, ph)
    rounded_rect(d2, (px, py, px + pw, py + ph), ph // 2, SAGE)
    d2.text((SAFE_CX, py + ph / 2), CTA_TEXT, font=f, fill=WHITE, anchor="mm")
    qa("cta", CTA_TEXT, (px, py, px + pw, py + ph))
    return canvas.convert("RGB")


def make_cover(packshot_path: Path, dest: Path, title="Who here never bumped their head as a baby?"):
    """1080x1920 cover: logo (if TOVI_LOGO exists) + title + packshot inside the 1080x1350 crop."""
    im = Image.new("RGBA", (W, H), CREAM + (255,))
    y = 340
    if LOGO.exists():
        lg = Image.open(LOGO).convert("RGBA"); lg.thumbnail((520, 260), Image.Resampling.LANCZOS)
        im.alpha_composite(lg, clamp_xy(SAFE_CX - lg.width / 2, y, lg.width, lg.height)); y += lg.height + 30
    f, lines = fit_lines(title, FREDOKA, 92, SAFE_W - 40)
    d = ImageDraw.Draw(im)
    for ln in lines:
        tw = d.textbbox((0, 0), ln, font=f)[2]
        d.text((SAFE_CX - tw // 2, y), ln, font=f, fill=BROWN); y += int(f.size * 1.12)
    box = Image.open(packshot_path).convert("RGBA"); box.thumbnail((620, max(120, 1380 - y - 30)), Image.Resampling.LANCZOS)
    im.alpha_composite(box, clamp_xy(SAFE_CX - box.width / 2, y + 30, box.width, box.height))
    im.convert("RGB").save(dest, quality=92)


def qa_report():
    bad = [r for r in QA_LOG if r[3][0] < SAFE[0] or r[3][1] < SAFE[1] or r[3][2] > SAFE[2] or r[3][3] > SAFE[3]]
    runs = {}
    for fr, kind, text, box in QA_LOG:
        if kind in ("ai", "packshot"):
            continue
        runs.setdefault(text, []).append(fr)
    short = []
    for text, frs in runs.items():
        frs = sorted(set(frs)); s0 = p = frs[0]
        for f in frs[1:] + [None]:
            if f is None or f != p + 1:
                if (p - s0 + 1) / FPS < MIN_HOLD:
                    short.append(f"'{text}' held {(p - s0 + 1) / FPS:.2f}s at {s0 / FPS:.2f}s")
                if f is not None:
                    s0 = f
            if f is not None:
                p = f
    print(f"[QA] {'PASS' if not bad and not short else 'CHECK'}: {len(bad)} outside safe box, {len(short)} short holds")
    for b in bad[:10]:
        print("   outside:", b)
    for x in short[:10]:
        print("   short:", x)


# ---------- audio ----------
def tone(freq, dur, sr, vol=0.2, attack=0.01, release=0.08):
    n = int(sr * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    env = np.ones_like(t)
    a = int(sr * attack)
    r = int(sr * release)
    if a > 0:
        env[:a] = np.linspace(0, 1, a)
    if r > 0:
        env[-r:] = np.linspace(1, 0, r)
    # soft triangle + sine
    wave = 0.7 * np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(2 * np.pi * freq * 2 * t) * 0.3
    return (wave * env * vol).astype(np.float64)


def pluck(freq, dur, sr, vol=0.22):
    n = int(sr * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    env = np.exp(-t * 5.5)
    # slight chorus
    sig = np.sin(2 * np.pi * freq * t) + 0.35 * np.sin(2 * np.pi * freq * 2 * t) * env
    sig += 0.12 * np.sin(2 * np.pi * (freq * 1.003) * t)
    return (sig * env * vol).astype(np.float64)


def boing(sr, vol=0.28):
    dur = 0.45
    n = int(sr * dur)
    t = np.linspace(0, dur, n, endpoint=False)
    freq = 420 * np.exp(-t * 4.2) + 160
    env = np.exp(-t * 6)
    sig = np.sin(2 * np.pi * freq * t) * env
    # soft thud under
    thud = np.sin(2 * np.pi * 70 * t) * np.exp(-t * 14) * 0.4
    return ((sig + thud) * vol).astype(np.float64)


def chime(sr, vol=0.2):
    parts = []
    for f, d in [(784, 0.35), (987, 0.4), (1174, 0.55)]:
        parts.append(pluck(f, d, sr, vol=vol))
    offs = [0, int(0.06 * sr), int(0.12 * sr)]
    out = np.zeros(max(o + p.size for o, p in zip(offs, parts)))   # was sized to the longest note only -> overflow
    for o, p, g in zip(offs, parts, (1.0, 0.8, 0.7)):
        out[o : o + p.size] += p * g
    return out


def make_music(path: Path, seconds=DURATION, sr=48000):
    n = int(sr * seconds)
    mix = np.zeros(n, dtype=np.float64)
    # C major pentatonic-ish playful ostinato
    # C4 D4 E4 G4 A4 C5
    scale = [261.63, 293.66, 329.63, 392.00, 440.00, 523.25, 392.00, 329.63]
    bpm = 108
    beat = 60 / bpm
    t0 = 0.0
    i = 0
    while t0 < seconds - 0.2:
        f = scale[i % len(scale)]
        # bass every 2 beats
        start = int(t0 * sr)
        pl = pluck(f, 0.55, sr, vol=0.16)
        end = min(n, start + pl.size)
        mix[start:end] += pl[: end - start]
        if i % 2 == 0:
            bass = pluck(f / 2, 0.7, sr, vol=0.11)
            endb = min(n, start + bass.size)
            mix[start:endb] += bass[: endb - start]
        t0 += beat
        i += 1
    # soft pad (very quiet sine fifths)
    t = np.linspace(0, seconds, n, endpoint=False)
    pad = 0.03 * np.sin(2 * np.pi * 196 * t) + 0.02 * np.sin(2 * np.pi * 261.63 * t)
    fade = np.ones_like(t)
    fade[: int(sr * 0.4)] = np.linspace(0, 1, int(sr * 0.4))
    fade[-int(sr * 0.8) :] = np.linspace(1, 0, int(sr * 0.8))
    mix += pad * fade

    # SFX: boing at tumble ~2.55s, chime at laugh ~5.2s, little chime at end card ~10.3s
    def add_at(sig, tsec):
        s = int(tsec * sr)
        e = min(n, s + sig.size)
        mix[s:e] += sig[: e - s]

    add_at(boing(sr, vol=0.32), 2.55)
    add_at(chime(sr, vol=0.18), 5.15)
    add_at(chime(sr, vol=0.16), 10.35)

    # soft limiter
    peak = np.max(np.abs(mix)) or 1.0
    mix = mix / peak * 0.85
    # fade out last 0.6s already partly
    pcm = (mix * 32767).astype(np.int16)
    # stereo
    stereo = np.column_stack([pcm, pcm])
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(stereo.tobytes())


# ---------- frames ----------
def blend(a: Image.Image, b: Image.Image, alpha: float) -> Image.Image:
    return Image.blend(a.convert("RGB"), b.convert("RGB"), max(0, min(1, alpha)))


def build_frames():
    wobble = fit_cover(Image.open(OUT / "01_wobble_9x16.jpg"))
    tumble = fit_cover(Image.open(OUT / "02_tumble_9x16.jpg"))
    laugh = fit_cover(Image.open(OUT / "03_laugh_9x16.jpg"))
    situp = fit_cover(Image.open(OUT / "04_situp_9x16.jpg"))
    end = make_end_card(OUT / "05_packshot_box_9x16.png")
    end_card_ref = [end]
    make_cover(OUT / "05_packshot_box_9x16.png", OUT / "cover.jpg")
    end.save(OUT / "06_endcard_9x16.png")

    # also save key frames with captions for Adel
    k1 = draw_ai_badge(draw_caption_block(kenburns(wobble, 0.4, 0, 1, 1.0, 1.08, (0, -20)).convert("RGBA"),
                                          "Who here never bumped their head as a baby?"))
    k1.convert("RGB").save(OUT / "keyframe_hook.jpg", quality=92)
    k2 = draw_ai_badge(draw_caption_block(kenburns(laugh, 0.4, 0, 1, 1.0, 1.06, (0, 10)).convert("RGBA"),
                                          "Soft cushioned landing",
                                          sub="Always supervise your little one."))
    k2.convert("RGB").save(OUT / "keyframe_landing.jpg", quality=92)

    clips = [
        # t0, t1, image, z0,z1, pan, caption, sub
        (0.00, 2.70, wobble, 1.00, 1.10, (0, -30), "Who here never bumped their head as a baby?", None),
        (2.50, 5.30, tumble, 1.02, 1.12, (0, 20), "When they start moving…", None),
        (5.10, 8.20, laugh, 1.00, 1.08, (0, 16), "little tumbles happen.", None),
        (8.00, 10.50, situp, 1.00, 1.07, (0, -10), "Soft cushioned landing", SUPERVISE),
        (10.30, 14.00, end, 1.00, 1.00, (0, 0), None, None),   # no zoom: the end card is laid out to the pixel
    ]

    frames_dir = OUT / "_frames"
    if frames_dir.exists():
        shutil.rmtree(frames_dir)
    frames_dir.mkdir()

    def clip_frame(clip, t):
        t0, t1, im, z0, z1, pan, cap, sub = clip
        fr = kenburns(im, t, t0, t1, z0, z1, pan)
        if cap:
            fr = draw_caption_block(fr.convert("RGBA"), cap, sub=sub)
        elif im is end_card_ref[0]:
            qa("endcard", "end card", (SAFE[0] + 20, 330, SAFE[2] - 20, CTA_BAND[1]))
        else:
            fr = fr.convert("RGBA")
        return fr

    QA_LOG.clear()                     # keyframe stills above are not part of the video
    for i in range(NFRAMES):
        t = i / FPS
        _FRAME[0] = i
        # find active clips
        active = [c for c in clips if c[0] <= t <= c[1]]
        if not active:
            active = [clips[-1] if t >= clips[-1][0] else clips[0]]
        if len(active) == 1:
            fr = clip_frame(active[0], t)
        else:
            a, b = active[0], active[1]
            # crossfade over overlap
            overlap = min(a[1], b[1]) - max(a[0], b[0])
            alpha = 0 if overlap <= 0 else (t - b[0]) / overlap
            fa = clip_frame(a, t)
            fb = clip_frame(b, t)
            fr = blend(fa, fb, alpha).convert("RGBA")
        fr = draw_ai_badge(fr)
        fr.convert("RGB").save(frames_dir / f"f{i:04d}.jpg", quality=90, subsampling=1)
        if i % 60 == 0:
            print(f"frame {i}/{NFRAMES}", flush=True)
    print("frames done", NFRAMES)
    qa_report()
    return frames_dir


def encode(frames_dir: Path, audio_path: Path, dest: Path):
    import subprocess
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(FPS),
        "-i", str(frames_dir / "f%04d.jpg"),
        "-i", str(audio_path),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-profile:v", "high", "-crf", "18", "-preset", "medium",
        "-vf", "scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p",
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-shortest", "-movflags", "+faststart",
        "-r", str(FPS),
        str(dest),
    ]
    print("ffmpeg", " ".join(cmd), flush=True)
    subprocess.check_call(cmd)
    print("wrote", dest, dest.stat().st_size)


def update_calendar():
    rows = list(csv.DictReader(CAL.open()))
    fields = list(rows[0].keys())

    episodes = {
        ("2026-11-14", "19:00"): dict(
            format="AI video (cartoon series)",
            concept="Dino Tumbles Ep.1 – The Hook: Who here never bumped their head as a baby?",
            caption="Who here never bumped their head as a baby? 😅 When they start moving, little tumbles happen. Soft cushioned landing 💛 Perfect gift for moms. $49.99 · 2 for $89.99. Always supervise your little one. #tovinest #moonwalkers #playmat #babygift #momtok #dinosnest",
            asset_path_or_to_generate="posts/dino-falls-01/dino_tumbles_ep01_9x16.mp4",
        ),
        ("2026-11-16", "19:00"): dict(
            format="AI video (cartoon series)",
            concept="Dino Tumbles Ep.2 – Crawl school: first scoot, little tumble, laugh",
            caption="Crawl school is in session 🦕 First scoot… little tumble… then a laugh. Cushions little tumbles. Peace of mind while they learn. $49.99 · 2 for $89.99. Always supervise your little one. #tovinest #tummytime #playmat #momtok #dinosnest",
            asset_path_or_to_generate="TO GENERATE: Dino Tumbles Ep.2 (same pipeline as posts/dino-falls-01)",
        ),
        ("2026-11-21", "19:00"): dict(
            format="AI video (cartoon series)",
            concept="Dino Tumbles Ep.3 – Hardwood vs the mat (Dino scoots back to a soft cushioned landing)",
            caption="Hardwood is… a choice 😅 Dino votes for a soft cushioned landing. Perfect gift for moms. $49.99 · 2 for $89.99. Always supervise your little one. #tovinest #playmat #momtok #dinosnest #babygift",
            asset_path_or_to_generate="TO GENERATE: Dino Tumbles Ep.3 (same pipeline as posts/dino-falls-01)",
        ),
        ("2026-11-23", "19:00"): dict(
            format="AI video (cartoon series)",
            concept="Dino Tumbles Ep.4 – Wobbly first steps (tip, land, giggle)",
            caption="Those first wobbly steps 💛 Tip, soft cushioned landing, giggle, try again. Peace of mind while they learn. $49.99 · 2 for $89.99. Always supervise your little one. #tovinest #firststeps #playmat #momtok #dinosnest",
            asset_path_or_to_generate="TO GENERATE: Dino Tumbles Ep.4 (same pipeline as posts/dino-falls-01)",
        ),
        ("2026-11-26", "13:00"): dict(
            format="AI video (cartoon series)",
            concept="Dino Tumbles Ep.5 – Thankful for cushioned landings (Thanksgiving, 1pm)",
            caption="This year we're thankful for soft cushioned landings 🦃💛 Perfect gift for moms. $49.99 · 2 for $89.99. Always supervise your little one. #tovinest #thanksgiving #playmat #babygift #dinosnest",
            asset_path_or_to_generate="TO GENERATE: Dino Tumbles Ep.5 (same pipeline as posts/dino-falls-01)",
        ),
        ("2026-12-06", "19:00"): dict(
            format="AI video (cartoon series)",
            concept="Dino Tumbles Ep.6 – Dance-party wobbles (they start moving!)",
            caption="When the music starts, the wobbles start 🕺🦕 Little tumbles happen. Soft cushioned landing. $49.99 · 2 for $89.99. Always supervise your little one. #tovinest #playmat #momtok #dinosnest",
            asset_path_or_to_generate="TO GENERATE: Dino Tumbles Ep.6 (same pipeline as posts/dino-falls-01)",
        ),
        ("2026-12-11", "13:00"): dict(
            format="AI video (cartoon series)",
            concept="Dino Tumbles Ep.7 – Perfect gift for moms (holiday, 1pm)",
            caption="The gift moms actually want 🎁 Peace of mind while they learn to move. Soft cushioned landing. $49.99 · 2 for $89.99. Always supervise your little one. #tovinest #babygift #giftguide #playmat #dinosnest",
            asset_path_or_to_generate="TO GENERATE: Dino Tumbles Ep.7 (same pipeline as posts/dino-falls-01)",
        ),
        ("2026-12-20", "19:00"): dict(
            format="AI video (cartoon series)",
            concept="Dino Tumbles Ep.8 – For your baby's first crawling steps (series closer)",
            caption="For your baby's first crawling steps 💌 Soft cushioned landing. Peace of mind. Perfect gift for moms. DM to order · Ships across the USA. $49.99 · 2 for $89.99. Always supervise your little one. #tovinest #milestones #babygift #playmat #dinosnest",
            asset_path_or_to_generate="TO GENERATE: Dino Tumbles Ep.8 (same pipeline as posts/dino-falls-01)",
        ),
    }
    n = 0
    for r in rows:
        key = (r["date"], r["time"][:5])
        if key in episodes:
            r["platform"] = "TikTok + Instagram Reels"
            r.update(episodes[key])
            n += 1
    if n != 8:
        raise SystemExit(f"expected 8 calendar updates, got {n}")
    with CAL.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print("calendar updated", n, "slots")


EPISODES_MD = r'''# Dino Tumbles — 8-episode series
Tone: gentle comedy. Dino (sage-green plush, rust-orange bandana) learns to crawl, walk, and wobble, tumbles onto the Moon Walkers mat, and bounces back laughing.
Hook line: "Who here never bumped their head as a baby? 😅"
Theme: babies start moving and little accidents happen, so the mat gives a soft cushioned landing. Perfect gift for moms. Peace of mind.
Compliance (every episode):
- SAY: soft cushioned landing, cushions little tumbles, peace of mind.
- NEVER claim it prevents injuries, protects the head, or is safety-certified for falls.
- ALWAYS: "Always supervise your little one."
- AI label ON.
Offers: $49.99 each · 2 for $89.99. CTA: DM to order · Ships across the USA.
'''


def write_episodes_md():
    text = '''# Dino Tumbles — 8-episode series

Tone: gentle comedy. Dino (sage-green plush dinosaur, rust-orange bandana) learns to crawl, walk, and wobble, keeps tumbling onto the Moon Walkers RainBoho mat, and bounces back laughing.

Series hook: "Who here never bumped their head as a baby? 😅"

Theme: babies start moving and little tumbles happen. The mat gives a soft cushioned landing. Perfect gift for moms. Peace of mind while they learn.

Compliance (every episode):
- Allowed phrases: "soft cushioned landing", "cushions little tumbles", "peace of mind".
- Never claim the mat prevents injuries, protects the head, or is safety-certified for falls.
- Always include: "Always supervise your little one."
- AI label ON.

Offers: $49.99 each · 2 for $89.99. CTA: "DM to order · Ships across the USA".

Calendar weave (Nov 14–Dec 20): Ep.1, 2, 3, 4, 6, 8 at 7:00 PM ET; Ep.5 and Ep.7 at 1:00 PM ET.

---

## Episode 1 — The Hook
Slot: Fri Nov 14, 7:00 PM ET. Asset: posts/dino-falls-01/dino_tumbles_ep01_9x16.mp4 (finished).

Hook: Who here never bumped their head as a baby? 😅

Script / shots (14s, 9:16):
1. 0–2.6s — Dino standing wobbly on the RainBoho mat, arms out, "uh-oh" face.
2. 2.5–5.3s — Comic mid-tumble toward the mat (gentle, not scary).
3. 5.1–8.2s — Dino on his back on the mat, laughing.
4. 8.0–10.5s — Dino sits up, wink and grin.
5. 10.3–14.0s — Real RainBoho box packshot + price end card.

On-screen text:
- "Who here never bumped their head as a baby? 😅"
- "When they start moving…"
- "little tumbles happen."
- "Soft cushioned landing 💛" / "Always supervise your little one."
- End card: "Perfect gift for moms" · "$49.99 each" · "2 for $89.99" · "Peace of mind while they learn." · "Always supervise your little one." · "DM to order · Ships across the USA"
- AI badge, full duration.

Caption: Who here never bumped their head as a baby? 😅 When they start moving, little tumbles happen. Soft cushioned landing 💛 Perfect gift for moms. $49.99 · 2 for $89.99. Always supervise your little one.

Hashtags: #tovinest #moonwalkers #playmat #babygift #momtok #dinosnest

---

## Episode 2 — Crawl school
Slot: Sun Nov 16, 7:00 PM ET.

Hook: First day of crawl school. How did yours go? 😅

Script / shots:
1. Dino on tummy, determined, chin on hands.
2. First scoot — one wobbly push.
3. Tips sideways onto the mat.
4. Pops up laughing, tries again.
5. Packshot + $49.99 / 2 for $89.99.

On-screen text:
- "Crawl school is in session."
- "First scoot…"
- "Little tumble."
- "Cushions little tumbles 💛"
- "Always supervise your little one."

Caption: Crawl school is in session 🦕 First scoot… little tumble… then a laugh. Cushions little tumbles. Peace of mind while they learn. $49.99 · 2 for $89.99. Always supervise your little one.

Hashtags: #tovinest #tummytime #playmat #momtok #dinosnest

---

## Episode 3 — Hardwood vs the mat
Slot: Sat Nov 21, 7:00 PM ET.

Hook: Hardwood is a choice. Dino would like a word. 😅

Script / shots:
1. Dino peeks at the bare wood floor at the edge of the mat, pats it, shakes his head.
2. One tiny step toward the edge… no thanks.
3. Scoots backward onto the RainBoho tiles and flops, happy.
4. Stretch and sigh on the mat.
5. Packshot + offer.

On-screen text:
- "Hardwood is… a choice."
- "Dino votes mat."
- "Soft cushioned landing 💛"
- "Peace of mind while they learn."
- "Always supervise your little one."

Caption: Hardwood is… a choice 😅 Dino votes for a soft cushioned landing. Perfect gift for moms. $49.99 · 2 for $89.99. Always supervise your little one.

Hashtags: #tovinest #playmat #momtok #dinosnest #babygift

---

## Episode 4 — Wobbly first steps
Slot: Mon Nov 23, 7:00 PM ET.

Hook: The wobbly-step era has entered the chat. 💛

Script / shots:
1. Dino pulls up to standing on the mat, knees shaking (comedy, not fear).
2. Two proud steps.
3. Tips, sits down with a bounce, laughs.
4. Gets up and tries again.
5. Packshot + offer.

On-screen text:
- "Those first wobbly steps."
- "Tip…"
- "Soft cushioned landing 💛"
- "Giggle. Try again."
- "Always supervise your little one."

Caption: Those first wobbly steps 💛 Tip, soft cushioned landing, giggle, try again. Peace of mind while they learn. $49.99 · 2 for $89.99. Always supervise your little one.

Hashtags: #tovinest #firststeps #playmat #momtok #dinosnest

---

## Episode 5 — Thankful for cushioned landings
Slot: Thu Nov 26, 1:00 PM ET (Thanksgiving).

Hook: This year we're thankful for soft landings. 🦃

Script / shots:
1. Mini Thanksgiving setup on the mat (tiny hat or leaf, playful).
2. Dino waddles toward a "feast," wobbles.
3. Tumbles, lands laughing.
4. Holds a little thankful sign or hugs the mat.
5. Packshot + offer. Perfect gift for moms heading into the holidays.

On-screen text:
- "Thankful for…"
- "soft cushioned landings 💛"
- "Peace of mind while they learn."
- "Always supervise your little one."

Caption: This year we're thankful for soft cushioned landings 🦃💛 Perfect gift for moms. $49.99 · 2 for $89.99. Always supervise your little one.

Hashtags: #tovinest #thanksgiving #playmat #babygift #dinosnest

---

## Episode 6 — Dance-party wobbles
Slot: Sun Dec 6, 7:00 PM ET.

Hook: When the music starts, the wobbles start. 🕺

Script / shots:
1. Dino boogies on the mat, bandana bouncing.
2. Big flourish, loses balance (comic).
3. Tumbles, bounces back laughing, keeps dancing.
4. Freeze-frame smile.
5. Packshot + offer.

On-screen text:
- "When they start moving…"
- "the wobbles start."
- "Little tumbles happen."
- "Soft cushioned landing 💛"
- "Always supervise your little one."

Caption: When the music starts, the wobbles start 🕺🦕 Little tumbles happen. Soft cushioned landing. $49.99 · 2 for $89.99. Always supervise your little one.

Hashtags: #tovinest #playmat #momtok #dinosnest

---

## Episode 7 — Perfect gift for moms
Slot: Fri Dec 11, 1:00 PM ET.

Hook: The gift moms actually want isn't another mug. 🎁

Script / shots:
1. Gift-ready RainBoho box, Dino peeks over the top.
2. Quick recap: wobble, tumble, laugh (1-second flashes).
3. Dino places the "first crawling steps" card on the box.
4. Warm smile to camera.
5. Packshot + $49.99 / 2 for $89.99 (one for home, one for Grandma).

On-screen text:
- "Perfect gift for moms."
- "Peace of mind while they learn."
- "Soft cushioned landing 💛"
- "Always supervise your little one."
- End card prices.

Caption: The gift moms actually want 🎁 Peace of mind while they learn to move. Soft cushioned landing. $49.99 · 2 for $89.99. Always supervise your little one.

Hashtags: #tovinest #babygift #giftguide #playmat #dinosnest

---

## Episode 8 — For your baby's first crawling steps
Slot: Sun Dec 20, 7:00 PM ET (series closer).

Hook: For first crawls, first wobbles, first soft landings. 💌

Script / shots:
1. Dino crawls across the mat, a little more confident, still comedic.
2. One last friendly tumble, laughs, sits up.
3. "First crawling steps" card lands in frame.
4. "DM to order · Ships across the USA" reminder, without crowding the joke.
5. Packshot + offer. Wave goodbye.

On-screen text:
- "For your baby's first crawling steps."
- "Soft cushioned landing 💛"
- "Peace of mind."
- "Always supervise your little one."
- "DM to order · Ships across the USA."

Caption: For your baby's first crawling steps 💌 Soft cushioned landing. Peace of mind. Perfect gift for moms. DM to order · Ships across the USA. $49.99 · 2 for $89.99. Always supervise your little one.

Hashtags: #tovinest #milestones #babygift #playmat #dinosnest
'''
    (OUT / "episodes.md").write_text(text)
    print("wrote", OUT / "episodes.md")


def main():
    write_episodes_md()
    update_calendar()
    audio = OUT / "ep01_audio.wav"
    print("making audio")
    make_music(audio)
    print("making frames")
    frames = build_frames()
    dest = OUT / "dino_tumbles_ep01_9x16.mp4"
    encode(frames, audio, dest)
    # keep frames for now? clean to save space but keep key stills
    shutil.rmtree(frames)
    print("DONE", dest)


if __name__ == "__main__":
    main()
