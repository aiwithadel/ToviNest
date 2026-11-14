"""Tovi Nest motion videos, v2: IG Reels + TikTok safe-zone layout.

Every text layer, pill, badge, CTA and mascot sits inside the SAFE box (x 40-900, y 320-1400),
which is the overlap of the IG Reels UI, the TikTok UI and the IG grid crop (y 285-1635).
Bands (absolute y): hook 320-520 · middle visual 540-1240 · chips/captions 1080-1340 ·
CTA 1258-1344 · brand footer 1352-1400.
Text appears with whole-element fades/scales (never a mid-glyph wipe) and every text layer
holds >= 1.5 s. render.js --qa checks both.

python3 gen_motion.py   -> build/*.html, build/*-cover.html, build/videos.json
node render.js          -> ../tovinest-*.mp4 + ../tovinest-*-cover.jpg
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "carousels", "_src"))
import gen as G  # noqa: E402
from gen import icon, wordmark, sprig, spark, mat_svg, mat3d, mat_flat, MASCOT, BADGE  # noqa: E402

SAFE = (40, 320, 900, 1400)          # x0, y0, x1, y1 (absolute px)
SW, SH = SAFE[2] - SAFE[0], SAFE[3] - SAFE[1]   # 860 x 1080
BOX_RB = "../../../carousels/_src/img/box-rainboho.jpg"
BOX_AS = "../../../carousels/_src/img/box-ashstarlight.jpg"
LOGO = "../../../tovinest-primary-logo.png"
EASE = "cubic-bezier(.2,.8,.2,1)"
SOFT = "cubic-bezier(.2,.9,.3,1)"     # no overshoot: nothing grows past its final box
PRICE_EACH, PRICE_DUO = "$49.99", "2 for $89.99"
CTA_TEXT = "DM to order · Ships across the USA"
SUPERVISE = "Always supervise children during play."

IO = []
def inout(start, end, fade=.35):
    """One animation that fades/scales in at `start` and out at `end` (a single keyframe track, so the
    'both' fill of a later fade-out can never override the fade-in)."""
    i, d = len(IO), end - start
    p1, p2 = fade / d * 100, (d - fade) / d * 100
    IO.append(f"@keyframes io{i} {{ 0% {{ opacity:0; transform:scale(.8) }} {p1:.2f}% {{ opacity:1; transform:none }} "
              f"{p2:.2f}% {{ opacity:1; transform:none }} 100% {{ opacity:0; transform:none }} }}")
    return f"io{i} {d}s linear {start}s both"

def a(name, start, dur=.45, ease=EASE, it="1"):
    return f"{name} {dur}s {ease} {start}s {it} both"

def at(top, html, *anims, h=None, left=0, width=SW, style="", cls=""):
    """Absolutely positioned block inside the safe box. top/left are relative to the box."""
    an = f"animation:{', '.join(anims)};" if anims else ""
    hh = f"height:{h}px;" if h else ""
    return (f'<div class="{cls}" style="position:absolute;left:{left}px;top:{top}px;width:{width}px;{hh}'
            f'display:flex;flex-direction:column;align-items:center;justify-content:center;{an}{style}">{html}</div>')

def photo(src, w, h, rot=0):
    return f'<div class="photo" style="width:{w}px;height:{h}px;transform:rotate({rot}deg)"><img src="{src}"></div>'

def hook(lines, start, size=104, colors=None, top=0):
    """Hook text in the 320-520 band (max 2 lines). Whole words fade/rise in, 0.1 s stagger."""
    html, k = [], 0
    for li, line in enumerate(lines):
        ws = []
        for wi, w in enumerate(line.split(" ")):
            c = colors.get(w) if colors else None
            ws.append(f'<span class="w qa-t" style="{"color:"+c+";" if c else ""}animation:{a("rise", start + k*.08, .4)}">{w}</span>')
            k += 1
        html.append(" ".join(ws))
    if len(lines) > 1:
        size = min(size, 100)          # 2 lines x ~1.03em must fit the 220 px hook slot
    return at(top, f'<div class="big" style="font-size:{size}px;line-height:1.02">{"<br>".join(html)}</div>', h=220,
              style="justify-content:flex-start;padding-top:4px")

def chip(ic, col, text, size=40):
    return f'<div class="pill p-{col} qa-t" style="font-size:{size}px;padding:16px 28px">{icon(ic)}{text}</div>'

def dino(start, w, left, top, bubble=None, bstart=None, bside="l", wave=False):
    """Mascot + optional bubble. left/top relative to the safe box; the bubble sits beside the head."""
    b = ""
    if bubble:
        side = "right:100%;margin-right:-30px" if bside == "l" else "left:100%;margin-left:-30px"
        b = (f'<div class="bubble qa-t" style="position:absolute;top:-10px;{side};font-size:40px;'
             f'animation:{a("popIn", bstart if bstart is not None else start+.4, .4, SOFT)}">{bubble}</div>')
    inner = a("wave", start+.6, 1.2, "ease-in-out", "infinite") if wave else a("bob", start+.6, 2.4, "ease-in-out", "infinite")
    return (f'<div class="qa-m" style="position:absolute;left:{left}px;top:{top}px;width:{w}px;animation:{a("rise", start, .5)}">{b}'
            f'<img src="{MASCOT}" style="width:100%;display:block;filter:drop-shadow(0 16px 18px rgba(80,60,40,.22));'
            f'transform-origin:50% 90%;animation:{inner}"></div>')

COUNTS = set()
def cnt(n, start, dur=1.0):
    COUNTS.add(n)
    return f'<span class="count" style="animation:count{n} {dur}s {EASE} {start}s both"></span>'

def price_row(start, top):
    return at(top, f'''<div style="display:flex;gap:20px;justify-content:center">
 <div class="card price qa-t" style="padding:24px 34px;animation:{a("popIn", start, .4, SOFT)}"><div class="lbl">Each</div><div class="now" style="font-size:84px">{PRICE_EACH}</div></div>
 <div class="card price duo qa-t" style="padding:24px 34px;animation:{a("popIn", start+.15, .4, SOFT)}"><div class="lbl">Bundle</div><div class="now" style="font-size:84px">{PRICE_DUO}</div></div>
</div>''', h=200)

def cta(start, top=SH - 142):
    # absolute 1258-1344: the endcard CTA band, above the TikTok/IG bottom UI
    return at(top, f'<div class="cta qa-t" style="font-size:38px;padding:20px 34px;gap:12px">{icon("bag", 2.4)}{CTA_TEXT}</div>',
              a("popIn", start, .4, SOFT), h=86)

def supervise(start, top):
    return at(top, f'<div class="qa-t" style="font-size:36px;font-weight:700;color:var(--muted)">{SUPERVISE}</div>', a("fadeIn", start, .4), h=46)


class Video:
    def __init__(self, name, total, tag):
        self.name, self.total, self.tag, self.scenes, self.kf = name, total, tag, [], []

    def scene(self, start, end, inner, fade=.3):
        i, d = len(self.scenes), end - start
        p1, p2 = fade / d * 100, (d - fade) / d * 100
        first, last = start == 0, end >= self.total
        self.kf.append(f"@keyframes sc{i} {{ 0% {{ opacity:{1 if first else 0} }} {p1:.2f}% {{ opacity:1 }} "
                       f"{p2:.2f}% {{ opacity:1 }} 100% {{ opacity:{1 if last else 0} }} }}")
        self.scenes.append(f'<div class="scene2" style="animation:sc{i} {d}s linear {start}s both">{inner}</div>')

    def html(self):
        counts = "".join(f"@keyframes count{n} {{ from {{ --n: 0 }} to {{ --n: {n} }} }}" for n in sorted(COUNTS))
        bg = ('<div class="bg"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>'
              + sprig(-60, 1500, 260, -20, '#7A8F6A', .4) + sprig(900, 1560, 240, 160, "#7A8F6A", .4)
              + spark(960, 260, 40) + spark(70, 1700, 30, "#E07A5F", .6) + spark(980, 1000, 26, "#7AA3BD", .7) + '</div>')
        foot = (f'<div class="foot" style="animation:{a("fadeIn", .1, .4)}"><div class="lockup qa-t"><img src="{BADGE}">{wordmark(34)}</div>'
                f'<div class="tag qa-t" style="font-size:20px;padding:6px 16px">{self.tag}</div></div>')
        return f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../../../carousels/_src/style.css"><link rel="stylesheet" href="../motion.css">
<style>{" ".join(self.kf)} {" ".join(IO)} {counts}</style></head>
<body><div class="stage slide r916" style="padding:0">{bg}<div class="safe">{"".join(self.scenes)}{foot}</div></div></body></html>'''

    def cover(self, title_lines, visual):
        title = "<br>".join(title_lines)
        return f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../../../carousels/_src/style.css"><link rel="stylesheet" href="../motion.css"></head>
<body><div class="stage slide r916" style="padding:0">
<div class="bg"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>{sprig(-60, 1500, 260, -20, '#7A8F6A', .4)}{spark(960, 260, 40)}</div>
<div class="safe">
 {at(10, f'<img src="{LOGO}" style="height:300px">', h=310)}
 {at(330, f'<div class="big" style="font-size:96px;line-height:1.02">{title}</div>', h=210)}
 {at(560, visual, h=420)}
 {at(1000, f'<div class="tag" style="font-size:26px">Play mats &amp; more for babies + kids</div>', h=60)}
</div></div></body></html>'''


# ====================================================================== 1. What's in the box
def v1():
    v = Video("01-whats-in-the-box", 20.0, "Unboxing")
    G_ = {"box?": "#7A8F6A"}
    v.scene(0, 3.8, hook(["What's in", "the box?"], .2, 116, G_) +
            at(226, '<div class="sub qa-t" style="margin:0;font-size:40px">The <b>Moon Walkers Premium EVA Playmat</b></div>', a("fadeIn", .6), h=60) +
            at(330, f'<div style="display:flex;gap:26px;align-items:flex-end">'
                    f'<div style="animation:{a("rise", .5, .5)}">{photo(BOX_RB, 330, 440, -4)}</div></div>', h=470) +
            dino(1.0, 230, 600, 560, "Let's open it!", 1.4, "l"))
    co = [("Premium EVA foam", 0, 4.3), ("16 tiles", 1, 4.6), ("67 × 48 in", 0, 4.9), ("0.5 in thick", 1, 5.2)]
    calls = "".join(
        f'<div class="callout qa-t" style="position:absolute;{"left:0" if side == 0 else "right:0"};top:{260 + i*120}px;font-size:36px;'
        f'animation:{a("popIn", t, .4, SOFT)}"><span class="n">{i+1}</span>{txt}</div>' for i, (txt, side, t) in enumerate(co))
    v.scene(3.8, 8.4, hook(["Everything's on", "the label"], 4.0, 100, {"label": "#7A8F6A"}) +
            at(220, f'<div style="animation:{a("rise", 4.0, .5)}">{photo(BOX_RB, 400, 540)}</div>', h=560) + calls +
            at(790, G.pills([("shield", "sage", "CPC / CPSIA tested")]).replace('class="pill', 'class="pill qa-t'), a("popIn", 5.6, .4, SOFT), h=90))
    import random
    random.seed(4)
    tiles = []
    for i in range(16):
        dx, dy = random.randint(-260, 260), random.randint(-300, 300)
        r, r2 = random.randint(-90, 90), random.choice([-3, -2, -1, 1, 2, 3])
        tiles.append(f'<div style="--dx:{dx}px;--dy:{dy}px;--r:{r}deg;--r2:{r2}deg;width:170px;height:122px;border-radius:12px;overflow:hidden;'
                     f'box-shadow:0 8px 0 #CDBBA6,0 18px 24px -12px rgba(80,60,40,.45);animation:{a("fly2", 8.8 + i*.08, .5, SOFT)}">'
                     f'{mat_svg("rb", 268, 192, grid=False)}</div>')
    v.scene(8.4, 12.6,
            at(10, f'<div class="big qa-t" style="font-size:140px;color:var(--sage);line-height:1">{cnt(16, 8.6, 1.4)}</div>', a("popIn", 8.5, .4, SOFT), h=180) +
            at(195, '<div class="big qa-t" style="font-size:80px">interlocking tiles</div>', a("rise", 8.7, .4), h=100) +
            at(280, f'<div style="display:grid;grid-template-columns:repeat(4,170px);gap:14px">{"".join(tiles)}</div>', h=540, style="top:305px") +
            at(860, '<div style="display:flex;gap:16px">' + chip("timer", "mustard", "Snaps together") + chip("puzzle", "sage", "No tools") + '</div>',
               a("popIn", 9.2, .4, SOFT), h=90))
    W_, H_ = 600, 430
    v.scene(12.6, 16.2, hook(["A big 5.6 × 4 ft", "play space"], 12.8, 100, {"5.6": "#7A8F6A", "×": "#7A8F6A", "4": "#7A8F6A", "ft": "#7A8F6A"}) +
            f'''<div style="position:absolute;left:30px;top:240px;width:{W_+140}px;height:{H_+140}px">
 <div style="position:absolute;left:140px;top:120px;animation:{a("fadeIn", 12.9, .5)}">{mat_flat("rb", W_)}</div>
 <div class="dim h" style="left:140px;top:50px;width:{W_}px;transform-origin:left;animation:{a("drawX", 13.2, .6)}"><div class="t qa-t" style="font-size:48px;animation:{a("popIn", 13.3, .4, SOFT)}">{cnt(67, 13.3, .9)} in<small>170 cm</small></div></div>
 <div class="dim v" style="left:58px;top:120px;height:{H_}px;transform-origin:top;animation:{a("drawY", 13.4, .6)}"><div class="t qa-t" style="font-size:48px;animation:{a("popIn", 13.5, .4, SOFT)}">{cnt(48, 13.5, .9)} in<small>122 cm</small></div></div>
</div>''' + dino(13.2, 170, 660, 740, "Room to roll!", 13.6, "l"))
    v.scene(16.2, 20.0, hook(["Unbox yours"], 16.4, 120, {"yours": "#7A8F6A"}) +
            at(150, f'<div style="animation:{a("rise", 16.5, .5)}">{mat3d("rb", 560)}</div>', h=420) +
            dino(16.8, 150, 690, 190, wave=True) +
            price_row(16.9, 580) + supervise(17.3, 830) + cta(17.4))
    title, visual = ["What's in", "the box?"], photo(BOX_RB, 300, 400, -3)
    return v, (title, visual)

# ====================================================================== 2. Specs & size guide
def v2():
    v = Video("02-specs-size-guide", 21.0, "Size guide")
    v.scene(0, 3.6, hook(["Will it fit?"], .2, 140, {"fit?": "#7A8F6A"}) +
            at(170, '<div class="big qa-t" style="font-size:84px;color:var(--coral)">Let\'s measure.</div>', a("rise", .6, .4), h=100) +
            dino(1.0, 300, 280, 420, "I measured!", 1.4, "r"))
    W_, H_ = 620, 444
    v.scene(3.6, 8.4, hook(["67 × 48 in"], 3.8, 120, {"67": "#7A8F6A", "48": "#7A8F6A", "in": "#7A8F6A"}) +
            at(150, '<div class="sub qa-t" style="margin:0;font-size:44px">Assembled size · 5.6 × 4 ft</div>', a("fadeIn", 4.0), h=60) +
            f'''<div style="position:absolute;left:40px;top:260px;width:{W_+140}px;height:{H_+140}px">
 <div style="position:absolute;left:140px;top:120px;animation:{a("reveal", 4.1, .5)}">{mat_flat("as", W_)}</div>
 <div class="dim h" style="left:140px;top:50px;width:{W_}px;transform-origin:left;animation:{a("drawX", 4.7, .6)}"><div class="t qa-t" style="font-size:56px;animation:{a("popIn", 4.8, .4, SOFT)}">{cnt(67, 4.8, 1.0)} in<small style="font-size:28px">170 cm</small></div></div>
 <div class="dim v" style="left:58px;top:120px;height:{H_}px;transform-origin:top;animation:{a("drawY", 5.3, .6)}"><div class="t qa-t" style="font-size:56px;animation:{a("popIn", 5.4, .4, SOFT)}">{cnt(48, 5.4, 1.0)} in<small style="font-size:28px">122 cm</small></div></div>
</div>''')
    v.scene(8.4, 12.2,
            at(0, f'<div class="big qa-t" style="font-size:180px;color:var(--sage);line-height:1">0.5<span style="font-size:96px"> in</span></div>', a("popIn", 8.6, .4, SOFT), h=190) +
            at(200, '<div class="big qa-t" style="font-size:72px">of soft EVA foam</div>', a("rise", 8.8, .4), h=90) +
            f'''<div style="position:absolute;left:0;top:360px;width:{SW}px;height:260px">
 <div style="position:absolute;left:150px;top:20px;width:600px;height:130px;transform:skewX(-36deg);transform-origin:bottom left;border-radius:10px 10px 0 0;overflow:hidden;animation:{a("fadeIn", 9.0, .5)}">{mat_svg("as", 600, 130, grid=False)}</div>
 <div style="position:absolute;left:150px;top:150px;width:600px;height:0;background:linear-gradient(#A8A29B,#8E8882);border-radius:0 0 14px 14px;box-shadow:0 30px 36px -20px rgba(80,60,40,.5);animation:grow .5s {EASE} 9.3s both"></div>
 <div class="dim v" style="left:100px;top:150px;height:80px;transform-origin:top;animation:{a("drawY", 9.6, .4)}"><div class="t qa-t" style="position:absolute;left:24px;font-size:40px;white-space:nowrap;animation:{a("fadeIn", 9.7)}">1.2 cm</div></div>
</div>''' +
            at(700, '<div style="display:flex;flex-direction:column;gap:16px;align-items:center">' + chip("heart", "pink", "Soft cushioned landing") +
               chip("baby", "mustard", "Comfy for crawling knees") + '</div>', a("popIn", 9.9, .4, SOFT), h=190))
    v.kf.append("@keyframes grow { from { height: 0 } to { height: 80px } }")
    PX = 8.4
    mw, mh = round(67*PX), round(48*PX)
    def obj(label, w_in, h_in, t0, t1):
        ow, oh = round(w_in*PX), round(h_in*PX)
        return (f'<div class="qa-t" style="position:absolute;left:{(mw-ow)//2}px;top:{(mh-oh)//2}px;width:{ow}px;height:{oh}px;border:5px dashed #fff;'
                f'background:rgba(255,255,255,.62);border-radius:10px;display:grid;place-items:center;font-family:Fredoka;font-weight:600;font-size:40px;color:var(--ink);'
                f'animation:{inout(t0, t1)}">{label}</div>')
    rows = [("Standard crib", "52 × 28 in", 12.6, 14.6), ("Play yard", "40 × 28 in", 14.6, 16.6), ("Toddler stretched out", "about 3 ft", 16.6, 18.6)]
    objs = obj("crib", 52, 28, 12.6, 14.6) + obj("play yard", 40, 28, 14.6, 16.6) + obj("toddler", 36, 14, 16.6, 18.6)
    labels = "".join(f'<div class="card qa-t" style="position:absolute;left:80px;right:80px;top:0;display:flex;align-items:center;gap:20px;padding:18px 28px;'
                     f'animation:{inout(t0, t1)}">'
                     f'<div class="ico i-sage" style="width:72px;height:72px;border-radius:22px">{icon("check", 2.8)}</div>'
                     f'<div style="text-align:left"><div style="font-family:Fredoka;font-weight:600;font-size:48px;line-height:1.05">{n}</div>'
                     f'<div style="font-size:34px;font-weight:700;color:var(--muted)">{s} · fits</div></div></div>' for n, s, t0, t1 in rows)
    v.scene(12.2, 18.8, hook(["What fits on it?"], 12.3, 96, {"fits": "#7A8F6A"}) +
            at(140, '<div class="sub qa-t" style="margin:0;font-size:40px">Drawn to scale on the 67 × 48 in mat</div>', a("fadeIn", 12.4), h=60) +
            f'<div style="position:absolute;left:{(SW-mw)//2}px;top:240px;width:{mw}px;height:{mh}px;border-radius:12px;overflow:hidden;'
            f'box-shadow:0 12px 0 #8E8882,0 36px 46px -20px rgba(80,60,40,.45);animation:{a("popIn", 12.4, .4, SOFT)}">{mat_svg("as", mw, mh, grid=False)}{objs}</div>' +
            f'<div style="position:absolute;left:0;right:0;top:{240+mh+50}px;height:140px">{labels}</div>')
    chips = [("puzzle", "sage", "16 tiles"), ("ruler", "mustard", "5.6 × 4 ft"), ("layers", "sky", "0.5 in thick"),
             ("drop", "sky", "Wipe-clean top"), ("shield", "sage", "CPC / CPSIA tested")]
    ch = "".join(f'<div style="animation:{a("popIn", 19.0 + i*.1, .35, SOFT)}">{chip(ic, c, t, 38)}</div>' for i, (ic, c, t) in enumerate(chips))
    v.scene(18.8, 21.0 + 1.8, hook(["The specs"], 18.9, 110, {"specs": "#7A8F6A"}) +
            at(150, f'<div style="display:flex;flex-wrap:wrap;gap:14px;justify-content:center;width:820px">{ch}</div>', h=300) +
            price_row(19.4, 480) + supervise(19.7, 730) + cta(19.8))
    v.total = 22.8
    title = ["Will it fit?", "Size guide"]
    visual = f'<div style="transform:scale(.9)">{mat_flat("as", 520)}</div>'
    return v, (title, visual)

# ====================================================================== 3. RainBoho vs Ash Starlight
def v3():
    v = Video("03-rainboho-vs-ash-starlight", 20.0, "Pick your vibe")
    # whole words scale/fade in (<= 0.4 s); nothing is ever shown half-wiped
    v.scene(0, 3.8,
            at(0, '<div class="big qa-t" style="font-size:112px;color:var(--coral)">RainBoho</div>', a("popIn", .15, .3, SOFT), h=120) +
            at(118, '<div class="big qa-t" style="font-size:64px;color:var(--muted)">vs</div>', a("popIn", .25, .3, SOFT), h=70) +
            at(190, '<div class="big qa-t" style="font-size:104px;color:var(--sage)">Ash Starlight</div>', a("popIn", .3, .3, SOFT), h=120) +
            at(380, f'<div style="display:flex;gap:24px"><div style="transform:rotate(-4deg)"><div style="animation:{a("rise", .9, .5)}">{mat_flat("rb", 400)}</div></div>'
                    f'<div style="transform:rotate(4deg)"><div style="animation:{a("rise", 1.05, .5)}">{mat_flat("as", 400)}</div></div></div>', h=360) +
            at(800, '<div style="display:flex;gap:16px">' + chip("rainbow", "coral", "Boho rainbows") + chip("moon", "sky", "Stars &amp; moons") + '</div>',
               a("popIn", 1.4, .4, SOFT), h=90))

    def design(s, e, n, name_html, sub, d, box, tags, sw):
        sws = "".join(f'<i style="width:62px;height:62px;border-radius:50%;background:{c};display:block;border:5px solid #fff;'
                      f'box-shadow:0 8px 14px -6px rgba(0,0,0,.3)"></i>' for c in sw)
        tg = "".join(chip(ic, c, t, 38) for ic, c, t in tags)
        v.scene(s, e,
                at(0, f'<div class="kicker qa-t" style="font-size:30px;margin:0">Design 0{n}</div>', a("fadeIn", s+.1), h=44) +
                at(44, f'<div class="big qa-t" style="font-size:118px">{name_html}</div>', a("popIn", s+.15, .35, SOFT), h=130) +
                at(180, f'<div class="sub qa-t" style="margin:0;font-size:40px">{sub}</div>', a("fadeIn", s+.4), h=60) +
                at(270, f'<div style="animation:{a("rise", s+.4, .5)}">{mat3d(d, 640)}</div>', h=420) +
                f'<div style="position:absolute;right:20px;top:250px;animation:{a("popIn", s+.7, .4, SOFT)}">{photo(box, 190, 250, 6)}</div>' +
                at(720, f'<div style="display:flex;gap:14px">{sws}</div>', a("fadeIn", s+.8), h=80) +
                at(820, f'<div style="display:flex;gap:14px;flex-wrap:wrap;justify-content:center">{tg}</div>', a("popIn", s+.9, .4, SOFT), h=90))
    design(3.8, 8.0, 1, 'Rain<span style="color:var(--coral)">Boho</span>', "Boho rainbows, clouds &amp; hearts", "rb", BOX_RB,
           [("sun", "mustard", "Warm &amp; cheerful"), ("home", "coral", "Wood &amp; beige rooms")], ["#E8D9C6", "#C3A386", "#D2AE98", "#F7F0E7"])
    design(8.0, 12.2, 2, 'Ash <span style="color:var(--sky)">Starlight</span>', "Stars &amp; crescent moons on soft grey", "as", BOX_AS,
           [("moon", "sky", "Calm &amp; dreamy"), ("home", "sage", "Grey &amp; white rooms")], ["#ADA7A0", "#8E8882", "#E6E1DA", "#F4F1EC"])
    same = [("ruler", "sage", "Same 5.6 × 4 ft"), ("layers", "sky", "Same 0.5 in cushion"), ("shield", "coral", "Same CPC / CPSIA testing")]
    sm = "".join(f'<div style="animation:{a("popIn", 13.0 + i*.15, .35, SOFT)}">{chip(ic, c, t, 40)}</div>' for i, (ic, c, t) in enumerate(same))
    v.scene(12.2, 15.8, hook(["Same mat.", "Different vibe."], 12.4, 104, {"Different": "#7A8F6A"}) +
            at(230, f'<div style="display:flex;gap:22px"><div style="transform:rotate(-3deg)"><div style="animation:{a("rise", 12.6, .5)}">{mat_flat("rb", 400)}</div></div>'
                    f'<div style="transform:rotate(3deg)"><div style="animation:{a("rise", 12.75, .5)}">{mat_flat("as", 400)}</div></div></div>', h=340) +
            at(620, f'<div style="display:flex;flex-direction:column;gap:14px;align-items:center">{sm}</div>', h=300))
    v.scene(15.8, 20.0, hook(["Can't decide?", "Get both."], 16.0, 104, {"both.": "#E9B041"}) +
            f'''<div style="position:absolute;left:0;top:220px;width:{SW}px;height:360px">
 <div style="position:absolute;left:30px;top:20px;transform:rotate(-6deg)"><div style="animation:{a("rise", 16.2, .5)}">{mat_flat("rb", 400)}</div></div>
 <div style="position:absolute;right:30px;top:70px;transform:rotate(5deg)"><div style="animation:{a("rise", 16.3, .5)}">{mat_flat("as", 400)}</div></div>
 <div class="qa-t" style="position:absolute;left:50%;top:40px;margin-left:-150px;width:300px;height:300px;border-radius:50%;background:var(--mustard);color:#fff;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Fredoka;box-shadow:0 26px 40px -16px rgba(169,118,27,.75);border:9px solid #fff;
  animation:{a("popIn", 16.5, .45, SOFT)}">
  <div style="font-size:40px;font-weight:500;letter-spacing:3px">2 FOR</div><div style="font-size:100px;font-weight:600;line-height:.95">$89.99</div>
  <div style="font-size:26px;font-weight:500">mix &amp; match</div>
  <i style="position:absolute;top:0;bottom:0;left:0;width:40%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.45),transparent);animation:{a("shine", 17.3, .9, "ease-in-out")}"></i></div>
</div>''' +
            at(600, f'<div class="qa-t" style="font-family:Fredoka;font-weight:600;font-size:56px;color:var(--ink)">{PRICE_EACH} <span style="color:var(--muted);font-size:40px">each</span></div>',
               a("fadeIn", 16.7), h=80) +
            supervise(16.9, 720) + dino(16.8, 150, 690, 760, wave=True) + cta(17.0))
    title = ["RainBoho vs", "Ash Starlight"]
    visual = (f'<div style="display:flex;gap:20px"><div style="transform:rotate(-4deg)">{mat_flat("rb", 380)}</div>'
              f'<div style="transform:rotate(4deg)">{mat_flat("as", 380)}</div></div>')
    return v, (title, visual)


if __name__ == "__main__":
    B = os.path.join(HERE, "build")
    os.makedirs(B, exist_ok=True)
    out = []
    for i, fn in enumerate((v1, v2, v3)):
        vid, (title, visual) = fn()
        p = os.path.join(B, vid.name + ".html")
        open(p, "w").write(vid.html())
        c = os.path.join(B, vid.name + "-cover.html")
        open(c, "w").write(vid.cover(title, visual))
        out.append({"html": p, "cover": c, "name": vid.name, "dur": vid.total, "music": i})
    json.dump(out, open(os.path.join(B, "videos.json"), "w"), indent=1)
    print(json.dumps([(o["name"], o["dur"]) for o in out]))
