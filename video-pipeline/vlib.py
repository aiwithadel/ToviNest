"""vlib: safe-zone-aware layout library for the Tovi Nest 9:16 videos (IG Reels + TikTok).

Drop-in replacement for the old vlib.py: same names and call signatures (chunks, draw_caption,
hook, endcard, price_sticker, bounce, kenburns, xfade, ...), so v3_videos.py / v03.py / vprod.py
keep working unchanged, but every text layer is now:

  * clamped inside SAFE = (40, 320, 900, 1400): the overlap of IG Reels UI, TikTok UI and the
    IG grid crop (center 1080x1350, y 285-1635). Hard-coded y values from old callers are
    re-mapped into the right band instead of being trusted;
  * wrapped on word boundaries to at most 2 lines and auto-shrunk (floor 56 px for hooks and
    captions, 36 px for disclaimers). It never breaks mid-word and never overflows;
  * animated without overshoot (scale <= 1.0), so the animated box never exceeds the clamped box;
  * logged per frame. Video.close() writes <video>.qa.json and prints any text that left the
    safe box or held for less than 1.5 s.

Captions are grouped by clause (punctuation), merged until each group can be held >= 1.5 s,
and held 0.35 s after the last word. Endcard: logo + tagline + prices + "Always supervise"
inside the 1080x1350 crop, CTA pill in the 1258-1344 band (above the TikTok/IG bottom UI).

Prices are normalised everywhere text is drawn: $39.99 -> $49.99, "2 for $89" -> "2 for $89.99",
"launch price" removed. CTA "Shop on TikTok Shop" -> "DM to order · Ships across the USA".
"""
from lib import *            # noqa: F401,F403  (assets, fonts, colours, Video, helpers)
import lib as _lib
import json, math, os, re, subprocess
from PIL import Image, ImageDraw, ImageFont

# ------------------------------------------------------------------ constants
W, H, FPS = 1080, 1920, 30
SAFE = (40, 320, 900, 1400)                     # x0, y0, x1, y1 (8 px padding already included)
SAFE_W, SAFE_H = SAFE[2] - SAFE[0], SAFE[3] - SAFE[1]
SAFE_CX = (SAFE[0] + SAFE[2]) // 2              # 470: centre of the safe box (not of the frame)
GRID = (0, 285, 1080, 1635)                     # IG profile-grid crop of a 9:16 video
BANDS = {
    "hook": (320, 520),          # hooks / titles
    "caption": (1080, 1340),     # kinetic VO captions
    "end_caption": (930, 1130),  # captions while the endcard is up
    "cta": (1258, 1344),         # endcard CTA pill
    "ai": (1356, 1398),          # baked-in "AI-generated" label
}
MIN_HOLD, TAIL = 1.5, 0.35
MIN_TEXT, MIN_DISCLAIMER, MAX_LINES = 56, 36, 2
PRICE_EACH, PRICE_DUO = "$49.99", "2 for $89.99"
CTA_TEXT = "DM to order · Ships across the USA"
SUPERVISE = "Always supervise children during play."
TAGLINE = "Little explorer. Big heart."
AI_TEXT = "AI-generated"

def _c(name, default):
    return getattr(_lib, name, default)
WHITE_, BROWN_, CORAL_, SAGE_, MUSTARD_ = (_c("WHITE", (255, 255, 255)), _c("BROWN", (110, 74, 43)),
                                           _c("CORAL", (224, 122, 95)), _c("SAGE", (122, 143, 106)), _c("MUSTARD", (233, 176, 65)))
MUSTARD_HL = (233, 176, 65)                     # active-word highlight #E9B041

# ------------------------------------------------------------------ text normalisation
_PRICE_FIX = [(r"\$39\.99", PRICE_EACH), (r"(?i)\s*launch price\s*", " "),
              (r"2\s*for\s*\$89(?!\.\d)", PRICE_DUO), (r"(?i)shop on tiktok shop", CTA_TEXT)]
def fix_copy(txt):
    """Enforce current pricing / CTA on any string about to be drawn."""
    out = str(txt)
    for pat, rep in _PRICE_FIX:
        out = re.sub(pat, rep, out)
    return re.sub(r"\s{2,}", " ", out).strip()

# ------------------------------------------------------------------ QA log
class _QA:
    def __init__(self):
        self.frame, self.items, self.warn = 0, [], []
    def log(self, kind, txt, box):
        x0, y0, x1, y1 = [float(v) for v in box]
        self.items.append((self.frame, kind, str(txt)[:60], (x0, y0, x1, y1)))
    def report(self, path=None):
        bad = [f"frame {f} ({f/FPS:.2f}s) {k} '{t}' outside safe box {tuple(round(v) for v in b)}"
               for f, k, t, b in self.items
               if b[0] < SAFE[0] - .5 or b[1] < SAFE[1] - .5 or b[2] > SAFE[2] + .5 or b[3] > SAFE[3] + .5]
        runs = {}
        for f, k, t, b in self.items:
            if k in ("caption", "ai"):
                continue                      # captions are checked analytically in caption_schedule
            runs.setdefault((k, t), set()).add(f)
        short = []
        for (k, t), fs in runs.items():
            fs = sorted(fs); s = p = fs[0]
            for f in fs[1:] + [None]:
                if f is None or f != p + 1:
                    if (p - s + 1) / FPS < MIN_HOLD:
                        short.append(f"{k} '{t}' held {(p - s + 1)/FPS:.2f}s at {s/FPS:.2f}s")
                    if f is not None:
                        s = f
                if f is not None:
                    p = f
        rep = {"outside_safe_box": sorted(set(bad))[:200], "short_holds": short, "warnings": self.warn,
               "pass": not bad and not short and not [w for w in self.warn if w.startswith("ERROR")]}
        if path:
            json.dump(rep, open(path, "w"), indent=1)
        print(f"[vlib QA] {'PASS' if rep['pass'] else 'CHECK'}: {len(bad)} out-of-box, {len(short)} short holds, "
              f"{len(self.warn)} warnings" + (f" -> {path}" if path else ""))
        for line in (bad[:10] + short[:10] + self.warn[:10]):
            print("   ", line)
        return rep
QA = _QA()

_BaseVideo = _lib.Video
class Video(_BaseVideo):
    """lib.Video + per-frame QA bookkeeping. Usage is unchanged: Video(path); v.add(img); v.close()."""
    def __init__(self, *a, **k):
        super().__init__(*a, **k)
        self._qa_path = (a[0] if a else k.get("path", "video.mp4")) + ".qa.json"
        global QA
        QA = _QA()
    def add(self, im):
        super().add(im)
        QA.frame += 1
    def close(self):
        super().close()
        QA.report(self._qa_path)

# ------------------------------------------------------------------ measuring / fitting
_MD = ImageDraw.Draw(Image.new("RGBA", (8, 8)))

def font_at(f, size):
    """Same face as `f` at a new size (works for any FreeTypeFont returned by lib.fred/nun)."""
    return ImageFont.truetype(f.path, int(size), index=getattr(f, "index", 0))

def measure(txt, f, stroke=0):
    x0, y0, x1, y1 = _MD.textbbox((0, 0), txt, font=f, stroke_width=stroke)
    return x1 - x0, y1 - y0

def wrap_words(txt, f, maxw, stroke=0):
    """Greedy word wrap. Never splits inside a word."""
    words, lines, cur = txt.split(), [], ""
    for w in words:
        cand = (cur + " " + w).strip()
        if not cur or measure(cand, f, stroke)[0] <= maxw:
            cur = cand
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    return lines

def fit_lines(txt, f, maxw, max_lines=MAX_LINES, min_size=MIN_TEXT, stroke=0):
    """Shrink until txt wraps into <= max_lines lines no wider than maxw. Returns (font, lines)."""
    size = f.size
    while True:
        ff = font_at(f, size)
        lines = wrap_words(txt, ff, maxw, stroke)
        if len(lines) <= max_lines and all(measure(l, ff, stroke)[0] <= maxw for l in lines):
            return ff, lines
        if size <= min_size:
            QA.warn.append(f"ERROR text needs > {max_lines} lines at {min_size}px: '{txt[:50]}'")
            return ff, lines[:max_lines]
        size -= 2

def clamp_xy(x, y, w, h, area=SAFE):
    """Top-left (x, y) moved so a w x h box sits inside `area`."""
    x = min(max(x, area[0]), area[2] - w)
    y = min(max(y, area[1]), area[3] - h)
    return int(round(x)), int(round(y))

def _ease(k):
    k = max(0.0, min(1.0, k))
    return 1 - (1 - k) ** 3

def _paste_scaled(im, layer, x, y, k, shadow=True):
    """Paste `layer` at its final box (x, y), scaled 0.88->1.0 and faded in by k. Scale stays <= 1,
    so the drawn pixels never leave the final, clamped box."""
    k = _ease(k)
    if k <= 0:
        return
    s = 0.88 + 0.12 * k
    lw, lh = max(1, int(layer.width * s)), max(1, int(layer.height * s))
    L = layer.resize((lw, lh), Image.LANCZOS) if s < 1 else layer
    if k < 1:
        a = L.split()[3].point(lambda v: int(v * k)); L = L.copy(); L.putalpha(a)
    px, py = x + (layer.width - lw) // 2, y + (layer.height - lh) // 2
    if shadow and hasattr(_lib, "shadow_paste"):
        _lib.shadow_paste(im, L, (px, py), blur=12, off=(0, 6), alpha=int(55 * k))
    else:
        im.alpha_composite(L, (int(px), int(py)))

def text_layer(lines, f, fill, stroke=0, stroke_fill=None, line_gap=1.12, colors=None):
    """Tight RGBA layer with centred lines. colors: optional per-line list of (word, rgb) lists."""
    lh = int(f.size * line_gap)
    widths = [measure(l, f, stroke)[0] for l in lines]
    w = max(widths) + 2 * stroke + 4
    h = lh * (len(lines) - 1) + measure("Ag", f, stroke)[1] + int(f.size * .35) + 2 * stroke
    L = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i, line in enumerate(lines):
        y = stroke + i * lh
        if colors:
            x = (w - widths[i]) / 2
            for word, col in colors[i]:
                d.text((x, y), word, font=f, fill=col, stroke_width=stroke, stroke_fill=stroke_fill)
                x += measure(word + " ", f)[0]
        else:
            d.text((w / 2, y), line, font=f, fill=fill, anchor="ma", stroke_width=stroke, stroke_fill=stroke_fill)
    return L

# ------------------------------------------------------------------ public helpers (old names kept)
def safe_text(im, txt, f, cx=SAFE_CX, top=None, cy=None, fill=None, stroke=0, stroke_fill=None,
              max_lines=MAX_LINES, min_size=MIN_TEXT, maxw=SAFE_W, k=1.0, kind="text", band=None):
    """Draw wrapped, clamped text. Position by `top` or `cy` (centre) or `band`. Returns the box."""
    txt = fix_copy(txt)
    ff, lines = fit_lines(txt, f, min(maxw, SAFE_W) - 2 * stroke, max_lines, min_size, stroke)
    L = text_layer(lines, ff, fill or BROWN_, stroke, stroke_fill)
    if band:
        b0, b1 = BANDS[band]; top = b0 + max(0, (b1 - b0 - L.height) // 2)
    if top is None:
        top = (cy if cy is not None else SAFE[1]) - L.height // 2
    x, y = clamp_xy(cx - L.width / 2, top, L.width, L.height)
    _paste_scaled(im, L, x, y, k, shadow=False)
    QA.log(kind, txt, (x, y, x + L.width, y + L.height))
    return (x, y, x + L.width, y + L.height)

def text(im, xy, txt, font, fill=None, anchor="la", **kw):
    """Old lib.text signature, clamped: draws `txt` so its box stays in SAFE (single line,
    auto-shrunk to fit). Prefer safe_text() for anything that may wrap."""
    txt = fix_copy(txt)
    ff = font
    while measure(txt, ff)[0] > SAFE_W and ff.size > MIN_DISCLAIMER:
        ff = font_at(ff, ff.size - 2)
    d = ImageDraw.Draw(im)
    x0, y0, x1, y1 = d.textbbox(xy, txt, font=ff, anchor=anchor, stroke_width=kw.get("stroke_width", 0))
    dx = (SAFE[0] - x0) if x0 < SAFE[0] else ((SAFE[2] - x1) if x1 > SAFE[2] else 0)
    dy = (SAFE[1] - y0) if y0 < SAFE[1] else ((SAFE[3] - y1) if y1 > SAFE[3] else 0)
    d.text((xy[0] + dx, xy[1] + dy), txt, font=ff, fill=fill if fill is not None else BROWN_, anchor=anchor,
           **{k: v for k, v in kw.items() if k in ("stroke_width", "stroke_fill", "align", "spacing")})
    QA.log("text", txt, (x0 + dx, y0 + dy, x1 + dx, y1 + dy))
    return (x0 + dx, y0 + dy, x1 + dx, y1 + dy)

def pill(im, cx, cy, txt, font, bg=None, fg=None, pad=(36, 16), k=1.0, maxw=SAFE_W, kind="pill"):
    """Rounded pill, auto-shrunk to fit maxw (single line) and clamped into SAFE."""
    txt = fix_copy(txt)
    ff = font
    while measure(txt, ff)[0] + 2 * pad[0] > maxw and ff.size > MIN_DISCLAIMER:
        ff = font_at(ff, ff.size - 2)
    tw, th = measure(txt, ff)
    w, h = tw + 2 * pad[0], int(ff.size * 1.25) + 2 * pad[1]
    L = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=bg or SAGE_)
    d.text((w / 2, h / 2), txt, font=ff, fill=fg or WHITE_, anchor="mm")
    x, y = clamp_xy(cx - w / 2, cy - h / 2, w, h)
    _paste_scaled(im, L, x, y, k)
    QA.log(kind, txt, (x, y, x + w, y + h))
    return (x, y, x + w, y + h)

def chip(im, cx, cy, txt, bg, t=1.0, t0=0.0, size=50):
    """Feature chip (pill) that pops in at t0."""
    if t < t0:
        return None
    return pill(im, cx, cy, txt, fred(size, 600), bg=bg, k=(t - t0) / .3, pad=(34, 14), kind="chip")

def price_sticker(im, x, y, r=125, new=PRICE_EACH, sub="EACH", old=None, bg=None, k=1.0, **kw):
    """Round price sticker; centre clamped so the whole circle (and its border) stays in SAFE."""
    new = fix_copy(new)
    r = min(r, SAFE_W // 2 - 8)
    D = 2 * r + 12
    L = Image.new("RGBA", (D, D), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse((0, 0, D - 1, D - 1), fill=WHITE_); d.ellipse((6, 6, D - 7, D - 7), fill=bg or CORAL_)
    f = fred(int(r * .62), 600)
    while measure(new, f)[0] > 1.6 * r and f.size > 24:
        f = font_at(f, f.size - 2)
    d.text((D / 2, D / 2 - (r * .1 if sub else 0)), new, font=f, fill=WHITE_, anchor="mm")
    if sub:
        d.text((D / 2, D / 2 + r * .42), sub, font=nun(max(22, int(r * .2)), 800), fill=WHITE_, anchor="mm")
    px, py = clamp_xy(x - D / 2, y - D / 2, D, D)
    _paste_scaled(im, L, px, py, k)
    QA.log("sticker", new, (px, py, px + D, py + D))
    return (px, py, px + D, py + D)

def safe_paste(im, layer, x, y, kind="mascot", shadow_y=None):
    """Paste a mascot / sticker image clamped into SAFE (no limb leaves the box). Returns (x, y)."""
    px, py = clamp_xy(x, y, layer.width, layer.height)
    if shadow_y is not None and hasattr(_lib, "ground_shadow"):
        _lib.ground_shadow(im, px + layer.width / 2, py + layer.height - 5, layer.width * .65, alpha=60)
    im.alpha_composite(layer, (px, py))
    QA.log(kind, kind, (px, py, px + layer.width, py + layer.height))
    return px, py

def ai_label(im, txt=AI_TEXT):
    """Small baked-in AI disclosure inside the safe box (bottom-left, AI band)."""
    f = nun(MIN_DISCLAIMER, 800)
    w, h = measure(txt, f, 3)
    x, y = SAFE[0] + 6, BANDS["ai"][0] + (BANDS["ai"][1] - BANDS["ai"][0] - h) // 2
    ImageDraw.Draw(im).text((x, y), txt, font=f, fill=WHITE_, stroke_width=3, stroke_fill=BROWN_)
    QA.log("ai", txt, (x, y, x + w, y + h))

# ------------------------------------------------------------------ hooks
def hook(im, txt, t, t0=0.0, y=None, size=70, bg=None, fg=None, maxw=900, band="hook"):
    """Banner hook. Old callers pass y=150..300: that is ignored below the band top (320).
    Wraps to <= 2 lines, shrinks to >= 56 px, centred on the safe box, never overshoots."""
    if t < t0:
        return None
    txt = fix_copy(txt)
    padx, pady = 36, 22
    f = fred(max(size, MIN_TEXT), 600)
    ff, lines = fit_lines(txt, f, min(maxw, SAFE_W) - 2 * padx)
    T = text_layer(lines, ff, fg or BROWN_)
    Wb, Hb = T.width + 2 * padx, T.height + 2 * pady
    L = Image.new("RGBA", (Wb, Hb), (0, 0, 0, 0))
    ImageDraw.Draw(L).rounded_rectangle((0, 0, Wb - 1, Hb - 1), 36, fill=bg or WHITE_)
    L.alpha_composite(T, (padx, pady))
    top = BANDS[band][0] if y is None else max(BANDS[band][0], y)
    x, yy = clamp_xy(SAFE_CX - Wb / 2, top, Wb, Hb)
    _paste_scaled(im, L, x, yy, (t - t0) / .35)
    QA.log("hook", txt, (x, yy, x + Wb, yy + Hb))
    return (x, yy, x + Wb, yy + Hb)

# ------------------------------------------------------------------ captions
WORDS_PATH = f"{B}/audio/words.json"
WORDS = json.load(open(WORDS_PATH)) if os.path.exists(WORDS_PATH) else {}
FIX = {'Moonwalkers': 'Moon Walkers', 'moonwalkers': 'Moon Walkers', 'dyno': 'Dino', 'white': 'wipe', 'Ranboho': 'RainBoho'}
CAPTION_SIZE = 74
_CLAUSE_END = ".?!,;:"

def _normalise(key, offset):
    ws = []
    for w, s, e in WORDS[key]:
        w = FIX.get(w, w)
        if w.lower().startswith('moonwalkers'):
            w = 'Moon Walkers' + w[11:]
        if w.startswith('dyno'):
            w = 'Dino' + w[4:]
        ws.append([w, s + offset, e + offset])
    out, i = [], 0                                   # "non" "-toxic," -> "non-toxic,"
    while i < len(ws):
        if ws[i][0] == 'non' and i + 1 < len(ws) and ws[i+1][0].startswith('-'):
            out.append([ws[i][0] + ws[i+1][0], ws[i][1], ws[i+1][2]]); i += 2
        else:
            out.append(ws[i]); i += 1
    ws, out, i = out, [], 0                          # "play mat" -> "playmat"
    while i < len(ws):
        if ws[i][0] == 'play' and i + 1 < len(ws) and ws[i+1][0].startswith('mat'):
            out.append(['playmat' + ws[i+1][0][3:], ws[i][1], ws[i+1][2]]); i += 2
        else:
            out.append(ws[i]); i += 1
    for i, w in enumerate(out):
        if w[0] == 'tummy':
            w[0] = 'Tummy'
        if w[0] == 'at' and i > 0 and out[i-1][0] == 'tested':
            w[0] = 'it'
        if w[0] == 'all,' and i > 1 and out[i-2][0] == 'tested':
            w[0] = 'all!'
    return out

def _fits(words, size=MIN_TEXT):
    f = fred(size, 600)
    return len(wrap_words(" ".join(words), f, SAFE_W - 40, 9)) <= MAX_LINES

def chunks(key, offset=0.3, maxw=3):
    """VO words -> caption groups ([[word, start, end], ...] per group, same shape as before).
    `maxw` is kept for compatibility but no longer caps a group at 3 words: groups end on clause
    punctuation (or when 2 lines are full), then short groups are merged with the next one until
    each can be held >= 1.5 s."""
    ws = _normalise(key, offset)
    groups, cur = [], []
    for w in ws:
        if cur and not _fits([x[0] for x in cur + [w]], CAPTION_SIZE):
            groups.append(cur); cur = []
        cur.append(w)
        if w[0][-1] in _CLAUSE_END:
            groups.append(cur); cur = []
    if cur:
        groups.append(cur)
    merged = []
    for g in groups:
        if merged:
            prev = merged[-1]
            hold = g[0][1] - prev[0][1]                 # time until this group would replace prev
            if hold < MIN_HOLD and _fits([x[0] for x in prev + g]):
                merged[-1] = prev + g
                continue
        merged.append(list(g))
    if len(merged) > 1:                                 # a too-short last group joins its predecessor
        last, prev = merged[-1], merged[-2]
        if last[-1][2] + TAIL - last[0][1] < MIN_HOLD and (last[0][1] - prev[0][1]) < MIN_HOLD \
                and _fits([x[0] for x in prev + last]):
            merged[-2:] = [prev + last]
    return merged

_SCHED = {}
def caption_schedule(groups):
    """[(start, end, group)]: hold = max(last word + 0.35 s, start + 1.5 s), never overlapping the
    next group. Groups that still cannot reach 1.5 s are reported in the QA log."""
    key = id(groups)
    if key in _SCHED:
        return _SCHED[key]
    out = []
    for i, g in enumerate(groups):
        s = g[0][1]
        e = max(g[-1][2] + TAIL, s + MIN_HOLD)
        if i + 1 < len(groups):
            e = min(e, groups[i+1][0][1])
        if e - s < MIN_HOLD - 1e-6:
            QA.warn.append(f"caption '{' '.join(w[0] for w in g)}' can only hold {e - s:.2f}s "
                           f"(next phrase starts at {groups[i+1][0][1]:.2f}s)")
        out.append((s, e, g))
    _SCHED[key] = out
    return out

def draw_caption(im, groups, t, y=None, size=CAPTION_SIZE, band="caption"):
    """Kinetic caption for time t. `y` from old callers is ignored: captions live in the caption
    band (1080-1340) or, with band='end_caption', in the endcard slot. Active word = mustard."""
    for s, e, g in caption_schedule(groups):
        if s <= t <= e:
            words = [fix_copy(w[0]) for w in g]
            f = fred(max(size, MIN_TEXT), 600)
            ff, lines = fit_lines(" ".join(words), f, SAFE_W - 40, stroke=9)
            colors, wi = [], 0
            for line in lines:
                row = []
                for w in line.split(" "):
                    ws_, we_ = g[min(wi, len(g) - 1)][1:3]
                    row.append((w, MUSTARD_HL if ws_ <= t <= we_ + 0.05 else WHITE_)); wi += 1
                colors.append(row)
            L = text_layer(lines, ff, WHITE_, 9, BROWN_, colors=colors)
            b0, b1 = BANDS[band]
            x, yy = clamp_xy(SAFE_CX - L.width / 2, b0 + max(0, (b1 - b0 - L.height) // 2), L.width, L.height)
            _paste_scaled(im, L, x, yy, (t - s) / .15, shadow=False)
            QA.log("caption", " ".join(words), (x, yy, x + L.width, yy + L.height))
            return (x, yy, x + L.width, yy + L.height)
    return None

# ------------------------------------------------------------------ endcard
def endcard(im, t, t0, price=True, line2=CTA_TEXT, tag=TAGLINE, mascot=None, groups=None, ai=False, caption_t=None):
    """Endcard laid out inside the safe box AND the 1080x1350 grid crop:
       logo 330-560 · tagline ~600 · prices 680-900 · (captions 930-1130) · supervise ~1190 ·
       CTA pill 1258-1344 · AI label 1356-1398.
    line2: anything other than a shop CTA (e.g. 'Follow for episode 2') is shown as a sub-line;
    the CTA pill is always the DM line.
    groups + caption_t: keep the VO captions running in the endcard slot (caption_t = absolute
    video time, because callers usually pass t relative to the endcard start)."""
    tt = t - t0
    k = (tt) / .5
    logo = getattr(_lib, "LOGO", None)
    lcx = SAFE_CX - (110 if mascot is not None else 0)
    if logo is not None:
        lg = fit_h(logo, 230)
        if lg.width > 520:
            lg = fit_w(lg, 520)
        lx, ly = clamp_xy(lcx - lg.width / 2, 330, lg.width, lg.height)
        _paste_scaled(im, lg, lx, ly, k, shadow=False)
        QA.log("logo", "logo", (lx, ly, lx + lg.width, ly + lg.height))
    if mascot is not None and tt > .4:
        m = fit_h(mascot, 240)
        safe_paste(im, m, SAFE[2] - m.width - 10, 330, kind="mascot")
    sub = None if (line2 is None or "shop" in line2.lower() or line2 == CTA_TEXT) else line2
    if tt > .3:
        safe_text(im, tag, fred(60, 600), top=578, fill=BROWN_, max_lines=1, kind="tagline")
    if price and tt > .5:
        price_sticker(im, SAFE[0] + 130, 790, r=105, new=PRICE_EACH, sub="EACH", k=(tt - .5) / .3)
        text(im, (SAFE[0] + 270, 712), PRICE_DUO, fred(66, 600), fill=CORAL_, anchor="la")
        text(im, (SAFE[0] + 274, 806), "RainBoho · Ash Starlight", nun(34, 800), fill=BROWN_, anchor="la")
    elif sub and tt > .5:
        safe_text(im, sub, fred(60, 600), top=740, fill=CORAL_, max_lines=1, kind="subline")
    if sub and price and tt > .5:
        safe_text(im, sub, nun(40, 800), top=880, fill=CORAL_, max_lines=1, min_size=MIN_DISCLAIMER, kind="subline")
    if groups is not None:
        draw_caption(im, groups, t if caption_t is None else caption_t, band="end_caption")
    if tt > .6:
        safe_text(im, SUPERVISE, nun(MIN_DISCLAIMER, 700), top=1170, fill=BROWN_, max_lines=1,
                  min_size=MIN_DISCLAIMER, kind="disclaimer")
    if tt > .7:
        b0, b1 = BANDS["cta"]
        pill(im, SAFE_CX, (b0 + b1) // 2, CTA_TEXT, fred(44, 600), bg=SAGE_, pad=(34, 12), maxw=SAFE_W - 20,
             k=(tt - .7) / .3, kind="cta")
    if ai:
        ai_label(im)

# ------------------------------------------------------------------ covers
def make_cover(path, title, hero=None, bg=None, seed=21):
    """1080x1920 cover whose logo + title sit inside the 1080x1350 grid crop and the safe box."""
    global QA
    saved, QA = QA, _QA()
    im = bg.copy() if bg is not None else deco_bg(W, H, seed=seed)
    logo = getattr(_lib, "LOGO", None)
    if logo is not None:
        lg = fit_h(logo, 300)
        if lg.width > 560:
            lg = fit_w(lg, 560)
        im.alpha_composite(lg, clamp_xy(SAFE_CX - lg.width / 2, 340, lg.width, lg.height))
    box = safe_text(im, title, fred(104, 600), top=680, fill=BROWN_, kind="cover-title")
    if hero is not None:
        h = fit_h(hero, max(80, 1380 - box[3] - 40))
        if h.width > SAFE_W - 40:
            h = fit_w(h, SAFE_W - 40)
        safe_paste(im, h, SAFE_CX - h.width // 2, box[3] + 30, kind="hero")
    im.convert("RGB").save(path, quality=92)
    QA = saved
    return path

# ------------------------------------------------------------------ audio / encode
def mux(silent, out, vo=None, music=None, music_vol=0.2, vo_delay=0.3):
    """Final encode to platform spec: 1080x1920 SAR 1:1, H.264 High yuv420p 30 fps CRF 19,
    AAC 48 kHz stereo 192 kbps, +faststart. VO delayed by vo_delay; music looped + ducked."""
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "default=nw=1:nk=1", silent]).strip())
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", silent]
    filt, n = [], 1
    if vo:
        cmd += ["-i", vo]
        d = int(vo_delay * 1000); filt.append(f"[{n}:a]aresample=48000,adelay={d}|{d},apad[vo]"); n += 1
    if music:
        cmd += ["-stream_loop", "-1", "-i", music]
        filt.append(f"[{n}:a]aresample=48000,volume={music_vol},afade=t=out:st={max(0, dur - 1.2)}:d=1.2[mu]"); n += 1
    if not vo and not music:
        cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
        filt.append("[1:a]anull[aout]")
    elif vo and music:
        filt.append("[vo][mu]amix=inputs=2:duration=longest:normalize=0[aout]")
    else:
        filt.append(f"[{'vo' if vo else 'mu'}]anull[aout]")
    cmd += ["-filter_complex", ";".join(filt), "-map", "0:v", "-map", "[aout]",
            "-vf", "scale=1080:1920,setsar=1", "-c:v", "libx264", "-preset", "slow", "-crf", "19",
            "-pix_fmt", "yuv420p", "-profile:v", "high", "-r", "30",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-t", f"{dur:.3f}",
            "-movflags", "+faststart", out]
    subprocess.check_call(cmd)
    return out

# ------------------------------------------------------------------ unchanged motion helpers
def bounce(t, amp=18, freq=2.2):
    return -abs(math.sin(t * math.pi * freq)) * amp

def kenburns(img, W, H, t, dur, z0=1.0, z1=1.12, dx=0, dy=0):
    k = ease_io(t / dur); z = z0 + (z1 - z0) * k
    s = max(W / img.width, H / img.height) * z
    im = img.resize((int(img.width * s), int(img.height * s)), Image.BILINEAR)
    cx = (im.width - W) / 2 + dx * k; cy = (im.height - H) / 2 + dy * k
    return im.crop((int(cx), int(cy), int(cx) + W, int(cy) + H))

def xfade(a, b, k):
    return Image.blend(a.convert('RGB'), b.convert('RGB'), max(0, min(1, k))).convert('RGBA')

def lift_bg(img, dy):
    """Shift a full-frame background up by dy px (to raise a floor line into the safe box),
    filling the bottom with the stretched last rows."""
    out = Image.new("RGBA", img.size)
    out.alpha_composite(img.crop((0, dy, img.width, img.height)).convert("RGBA"), (0, 0))
    strip = img.crop((0, img.height - 8, img.width, img.height)).resize((img.width, dy)).convert("RGBA")
    out.alpha_composite(strip, (0, img.height - dy))
    return out
