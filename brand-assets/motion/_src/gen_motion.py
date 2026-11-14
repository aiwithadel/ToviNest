"""Build the Tovi Nest motion videos as HTML/CSS animations.
python3 gen_motion.py  -> build/*.html (+ build/videos.json)
node render.js         -> ../*.mp4
Reuses the carousel components (icons, wordmark, mat renders) from ../../carousels/_src/gen.py.
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "carousels", "_src"))
import gen as G  # noqa: E402
from gen import icon, wordmark, sprig, spark, mat_svg, mat3d, mat_flat, MASCOT, BADGE  # noqa: E402

BOX_RB = "../../../carousels/_src/img/box-rainboho.jpg"
BOX_AS = "../../../carousels/_src/img/box-ashstarlight.jpg"
EASE = "cubic-bezier(.2,.8,.2,1)"
BOUNCE = "cubic-bezier(.34,1.56,.64,1)"

def a(name, start, dur=.6, ease=EASE, it="1"):
    return f"{name} {dur}s {ease} {start}s {it} both"

def el(html, *anims, style="", cls=""):
    an = f"animation:{', '.join(anims)};" if anims else ""
    return f'<div class="{cls}" style="{an}{style}">{html}</div>'

def photo(src, w, h, rot=0):
    return f'<div class="photo" style="width:{w}px;height:{h}px;transform:rotate({rot}deg)"><img src="{src}"></div>'

def words(text, start, step=.12, cls="w", anim="up", dur=.55, colors=None):
    out = []
    for i, w in enumerate(text.split(" ")):
        c = f"color:{colors[i]};" if colors and colors[i] else ""
        out.append(f'<span class="{cls}" style="{c}animation:{a(anim, start+i*step, dur)}">{w}</span>')
    return "&nbsp;".join(out)

def dino(start, w=300, bubble=None, bstart=None, pos="", bpos="tl", bstyle="", wave=False):
    b = ""
    if bubble:
        b = f'<div class="bubble {bpos}" style="{bstyle};animation:{a("pop", bstart if bstart is not None else start+.4, .5, BOUNCE)}">{bubble}</div>'
    inner_anim = a("wave", start+.6, 1.2, "ease-in-out", "infinite") if wave else a("bob", start+.6, 2.2, "ease-in-out", "infinite")
    return (f'<div class="dino" style="{pos};width:{w}px;animation:{a("up", start, .7, BOUNCE)}">{b}'
            f'<img src="{MASCOT}" style="transform-origin:50% 90%;animation:{inner_anim}"></div>')

def counter(n, start, dur=1.2):
    return f'<span class="count" style="animation:count{n} {dur}s {EASE} {start}s both"></span>'

COUNTS = set()
def cnt(n, start, dur=1.2):
    COUNTS.add(n)
    return counter(n, start, dur)

class Video:
    def __init__(self, name, total):
        self.name, self.total, self.scenes, self.kf = name, total, [], []

    def scene(self, start, end, inner, style="", fade=.35):
        i = len(self.scenes)
        d = end - start
        p1, p2 = fade / d * 100, (d - fade) / d * 100
        first = start == 0
        self.kf.append(f"@keyframes sc{i} {{ 0% {{ opacity:{1 if first else 0}; transform: {'none' if first else 'translateY(30px)'} }} "
                       f"{p1:.2f}% {{ opacity:1; transform:none }} {p2:.2f}% {{ opacity:1; transform:none }} "
                       f"100% {{ opacity:{1 if end >= self.total else 0}; transform:{'none' if end >= self.total else 'translateY(-30px)'} }} }}")
        self.scenes.append(f'<div class="scene" style="animation:sc{i} {d}s linear {start}s both;{style}">{inner}</div>')

    def html(self, tag):
        counts = "".join(f"@keyframes count{n} {{ from {{ --n: 0 }} to {{ --n: {n} }} }}" for n in sorted(COUNTS))
        bg = ('<div class="bg"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>'
              + sprig(-40, 1300, 240, -20, '#7A8F6A', .4) + sprig(880, 1460, 260, 160, "#7A8F6A", .45)
              + spark(930, 330, 40) + spark(70, 1640, 30, "#E07A5F", .6) + spark(980, 900, 26, "#7AA3BD", .7) + '</div>')
        top = (f'<div class="topbar" style="animation:{a("down", .1, .6)}"><div class="lockup"><img src="{BADGE}">{wordmark(46)}</div>'
               f'<div class="tag">{tag}</div></div>')
        return f'''<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="../../../carousels/_src/style.css"><link rel="stylesheet" href="../motion.css">
<style>{" ".join(self.kf)} {counts}</style></head>
<body><div class="stage slide r916" style="padding:0">{bg}{top}{"".join(self.scenes)}</div></body></html>'''

def handle_bar(start):
    return el(f'<div class="cta" style="font-size:40px">{icon("bag", 2.4)}Shop on TikTok Shop</div>'
              f'<div class="handle-big" style="font-size:38px">Search <span>@tovinest</span></div>',
              a("up", start, .6), style="display:flex;flex-direction:column;align-items:center;margin-top:40px")

# ====================================================================== 1. Unboxing
def v1():
    v = Video("01-whats-in-the-box", 17.0)
    # S1 0 - 3.4
    v.scene(0, 3.4, f'''
<div class="kicker" style="animation:{a("fadeIn", .3, .5)}">Unboxing the playmat</div>
<div class="big" style="font-size:150px">{words("What's in", .45)}<br>{words("the box?", .75, colors=[None, "#7A8F6A"])}</div>
<div class="sub" style="animation:{a("up", 1.3)}">The <b>Moon Walkers Premium EVA Playmat</b></div>
{dino(1.5, 340, "Let's open it!", 2.1, "left:50%;margin-left:-170px;bottom:300px;position:absolute", "tl", "left:210px;top:-80px")}''', style="justify-content:flex-start;padding-top:440px")
    # S2 3.4 - 7.4 box features
    co = [("Premium EVA foam", "left:-10px;top:300px", 4.4), ("16 tiles", "right:-10px;top:450px", 4.85),
          ("5.6 × 4 ft · 67 × 48 in", "left:-10px;top:620px", 5.3), ("0.5 in / 1.2 cm thick", "right:-10px;top:780px", 5.75)]
    calls = "".join(f'<div class="callout" style="{p};font-size:34px;animation:{a("pop", t, .5, BOUNCE)}"><span class="n">{i+1}</span>{txt}</div>'
                    for i, (txt, p, t) in enumerate(co))
    v.scene(3.4, 7.4, f'''
<div class="kicker" style="animation:{a("fadeIn", 3.6)}">The box</div>
<div class="big" style="font-size:110px">{words("Everything's on", 3.65)}<br>{words("the label", 3.9, colors=[None, "#7A8F6A"])}</div>
<div style="position:relative;width:936px;height:980px;margin-top:40px">
 <div style="position:absolute;left:218px;top:40px;animation:{a("swingIn", 3.9, .8, BOUNCE)}">{photo(BOX_RB, 500, 680)}</div>
 {calls}
 <div style="position:absolute;left:0;right:0;top:860px;animation:{a("up", 6.2)}">{G.pills([("shield","sage","CPSIA tested"),("check","coral","CPC certified")])}</div>
</div>''')
    # S3 7.4 - 11.2 tiles fly in
    import random
    random.seed(4)
    tiles = []
    for i in range(16):
        dx, dy = random.randint(-500, 500), random.randint(-700, 700)
        r, r2 = random.randint(-120, 120), random.choice([-3, -2, -1, 1, 2, 3])
        t = 8.0 + i * .1
        tiles.append(f'<div style="--dx:{dx}px;--dy:{dy}px;--r:{r}deg;--r2:{r2}deg;width:200px;height:143px;border-radius:12px;overflow:hidden;'
                     f'box-shadow:0 9px 0 #CDBBA6,0 22px 28px -12px rgba(80,60,40,.45);animation:{a("fly", t, .55, BOUNCE)}, {a("snap", 10.0, .35)}">'
                     f'{mat_svg("rb", 268, 192, grid=False)}</div>')
    v.scene(7.4, 11.2, f'''
<div class="kicker" style="animation:{a("fadeIn", 7.6)}">Inside the box</div>
<div class="big" style="font-size:150px"><span style="color:var(--sage)">{cnt(16, 7.9, 1.8)}</span></div>
<div class="big" style="font-size:96px">{words("interlocking tiles", 8.1)}</div>
<div style="display:grid;grid-template-columns:repeat(4,200px);gap:18px;margin-top:60px">{"".join(tiles)}</div>
<div style="margin-top:56px;animation:{a("up", 10.1)}">{G.pills([("timer","mustard","Snaps together in minutes"),("puzzle","sage","No tools")])}</div>''')
    # S4 11.2 - 14.2 assembled + dims
    W, H = 760, 545
    v.scene(11.2, 14.2, f'''
<div class="big" style="font-size:104px">{words("A big", 11.4)}&nbsp;<span class="w" style="color:var(--sage);animation:{a("pop", 11.7, .6, BOUNCE)}">5.6 × 4 ft</span><br>{words("play space", 11.9)}</div>
<div style="position:relative;width:{W+150}px;height:{H+150}px;margin-top:70px">
 <div style="position:absolute;left:150px;top:140px;animation:{a("zoomOut", 11.4, 1.2)}, {a("fadeIn", 11.4, .5)}">{mat_flat("rb", W)}</div>
 <div class="dim h" style="left:150px;top:60px;width:{W}px;transform-origin:left;animation:{a("drawX", 12.2, .7)}"><div class="t" style="animation:{a("pop", 12.7, .5, BOUNCE)}">{cnt(67, 12.3, .9)} in<small>170 cm</small></div></div>
 <div class="dim v" style="left:62px;top:140px;height:{H}px;transform-origin:top;animation:{a("drawY", 12.6, .7)}"><div class="t" style="animation:{a("pop", 13.1, .5, BOUNCE)}">{cnt(48, 12.7, .9)} in<small>122 cm</small></div></div>
</div>
{dino(12.4, 250, "Room to roll!", 13.0, "right:40px;bottom:330px;position:absolute", "tr", "right:80px;top:-80px")}''')
    # S5 14.2 - 17 CTA
    v.scene(14.2, 17.0, f'''
<div class="big" style="font-size:136px">{words("Unbox", 14.4)}&nbsp;<span class="w" style="color:var(--sage);animation:{a("up", 14.55, .55)}">yours</span></div>
<div style="margin-top:50px;animation:{a("up", 14.8)}">{mat3d("rb", 700)}</div>
<div class="price-row" style="margin-top:50px;justify-content:center">
 <div class="card price" style="animation:{a("pop", 15.2, .5, BOUNCE)}"><div class="lbl">Launch price</div>
  <div class="old" style="position:relative;text-decoration:none">$49.99<i style="position:absolute;left:-4px;right:-4px;top:52%;height:4px;background:#A99684;transform-origin:left;animation:{a("drawX", 15.6, .35)}"></i></div>
  <div class="now">$39.99</div></div>
 <div class="card price duo" style="animation:{a("pop", 15.5, .5, BOUNCE)}"><div class="lbl">Bundle deal</div><div class="now">2 for $89</div><div class="note">Mix &amp; match</div></div>
</div>
<div style="animation:{a("pulse", 16.4, 1, "ease-in-out", "infinite")}">{handle_bar(15.8)}</div>
{dino(15.0, 210, None, None, "left:0px;bottom:250px;position:absolute", wave=True)}''')
    return v, "Unboxing"

# ====================================================================== 2. Specs
def v2():
    v = Video("02-specs-size-guide", 17.5)
    v.scene(0, 3.0, f'''
<div class="big" style="font-size:190px">{words("Will it", .3, .18)}<br><span class="w" style="color:var(--sage);animation:{a("pop", .75, .6, BOUNCE)}">fit?</span></div>
<div class="big" style="font-size:96px;margin-top:40px;color:var(--coral)">{words("Let's measure.", 1.3, .2)}</div>
{dino(1.6, 320, "I measured!", 2.1, "left:50%;margin-left:-160px;bottom:300px;position:absolute", "tl", "left:200px;top:-80px")}''', style="justify-content:flex-start;padding-top:400px")
    W, H = 800, 573
    v.scene(3.0, 8.0, f'''
<div class="kicker" style="animation:{a("fadeIn", 3.2)}">Assembled size</div>
<div class="big" style="font-size:104px">{words("67 × 48 in", 3.3, .15, colors=["#7A8F6A", None, "#7A8F6A", "#7A8F6A"])}</div>
<div style="position:relative;width:{W+140}px;height:{H+170}px;margin-top:70px">
 <div style="position:absolute;left:140px;top:150px;animation:{a("reveal", 3.6, 1.0)}">{mat_flat("as", W)}</div>
 <div class="dim h" style="left:140px;top:60px;width:{W}px;transform-origin:left;animation:{a("drawX", 4.6, .9)}">
  <div class="t" style="font-size:64px;animation:{a("pop", 4.9, .5, BOUNCE)}">{cnt(67, 4.9, 1.2)} in<small style="font-size:30px;animation:{a("fadeIn", 6.0)}">170 cm · 5.6 ft</small></div></div>
 <div class="dim v" style="left:52px;top:150px;height:{H}px;transform-origin:top;animation:{a("drawY", 5.7, .9)}">
  <div class="t" style="font-size:64px;animation:{a("pop", 6.0, .5, BOUNCE)}">{cnt(48, 6.0, 1.2)} in<small style="font-size:30px;animation:{a("fadeIn", 7.0)}">122 cm · 4 ft</small></div></div>
</div>''')
    # thickness
    v.scene(8.0, 11.2, f'''
<div class="kicker" style="animation:{a("fadeIn", 8.2)}">Thickness</div>
<div class="big" style="font-size:260px;color:var(--sage)"><span class="w" style="animation:{a("pop", 8.3, .6, BOUNCE)}">0.5</span><span class="w" style="font-size:130px;animation:{a("fromR", 8.6)}">in</span></div>
<div class="big" style="font-size:80px">{words("of soft EVA cushion", 8.8, .12)}</div>
<div style="position:relative;width:900px;height:300px;margin-top:80px">
 <div style="position:absolute;left:170px;top:30px;width:700px;height:150px;transform:skewX(-40deg);transform-origin:bottom left;border-radius:10px 10px 0 0;overflow:hidden;animation:{a("reveal", 9.2, .8)}">{mat_svg("as", 700, 150, grid=False)}</div>
 <div style="position:absolute;left:170px;top:180px;width:700px;height:0;background:linear-gradient(#A8A29B,#8E8882);border-radius:0 0 14px 14px;
  box-shadow:0 34px 40px -20px rgba(80,60,40,.5);animation:grow 0.6s {EASE} 9.8s both"></div>
 <div class="dim v" style="left:120px;top:180px;height:90px;transform-origin:top;animation:{a("drawY", 10.2, .4)}"><div class="t" style="position:absolute;right:26px;font-size:40px;text-align:right;animation:{a("fadeIn", 10.4)}">1.2 cm</div></div>
</div>
<div style="margin-top:30px;animation:{a("up", 10.4)}">{G.pills([("heart","pink","Soft landings"),("baby","mustard","Comfy for knees")])}</div>''')
    v.kf.append("@keyframes grow { from { height: 0 } to { height: 90px } }")
    # what fits
    PX = 9.0
    mw, mh = round(67*PX), round(48*PX)
    def obj(label, w_in, h_in, t, color):
        ow, oh = round(w_in*PX), round(h_in*PX)
        return (f'<div style="position:absolute;left:{(mw-ow)//2}px;top:{(mh-oh)//2}px;width:{ow}px;height:{oh}px;border:5px dashed #fff;'
                f'background:{color};border-radius:10px;display:grid;place-items:center;font-family:Fredoka;font-weight:600;font-size:34px;color:var(--ink);'
                f'animation:{a("pop", t, .5, BOUNCE)}, {a("fadeOut", t+1.05, .3)}">{label}</div>')
    v.kf.append("@keyframes fadeOut { from { opacity: 1 } to { opacity: 0 } }")
    rows = [("Standard crib", "52 × 28 in", 11.9), ("Play yard", "40 × 28 in", 13.2), ("Toddler, stretched out", "~3 ft tall", 14.5)]
    labels = "".join(f'<div class="card" style="display:flex;align-items:center;gap:20px;padding:20px 30px;animation:{a("fromL", t+.15)}">'
                     f'<div class="ico i-sage" style="width:70px;height:70px;border-radius:22px">{icon("check", 2.8)}</div>'
                     f'<div style="text-align:left"><div style="font-family:Fredoka;font-weight:600;font-size:40px">{n}</div>'
                     f'<div style="font-size:28px;font-weight:700;color:var(--muted)">{s} · fits</div></div></div>' for n, s, t in rows)
    v.scene(11.2, 15.6, f'''
<div class="kicker" style="animation:{a("fadeIn", 11.3)}">What fits on it?</div>
<div class="big" style="font-size:96px">{words("Drawn to scale", 11.4, .14)}</div>
<div style="position:relative;width:{mw}px;height:{mh}px;margin-top:56px;border-radius:12px;overflow:hidden;box-shadow:0 12px 0 #8E8882,0 40px 50px -20px rgba(80,60,40,.45);animation:{a("pop", 11.5, .6)}">
 {mat_svg("as", mw, mh, grid=False)}
 {obj("crib", 52, 28, 11.9, "rgba(255,255,255,.6)")}{obj("play yard", 40, 28, 13.2, "rgba(255,255,255,.6)")}{obj("toddler", 36, 14, 14.5, "rgba(255,255,255,.6)")}
</div>
<div style="display:flex;flex-direction:column;gap:16px;margin-top:50px;width:760px">{labels}</div>''')
    # summary
    chips = [("puzzle","sage","16 tiles"),("ruler","mustard","5.6 × 4 ft"),("layers","sky","0.5 in thick"),
             ("drop","sky","Waterproof"),("feet","coral","Non-slip"),("shield","sage","CPSIA · CPC")]
    ch = "".join(f'<div class="pill p-{c}" style="font-size:38px;padding:20px 32px;animation:{a("pop", 16.0+i*.12, .45, BOUNCE)}">{icon(ic)}{t}</div>'
                 for i, (ic, c, t) in enumerate(chips))
    v.scene(15.6, 17.5 + 2.0, f'''
<div class="kicker" style="animation:{a("fadeIn", 15.8)}">Save this</div>
<div class="big" style="font-size:120px">{words("The specs", 15.8)}</div>
<div style="display:flex;flex-wrap:wrap;gap:20px;justify-content:center;margin-top:60px;width:900px">{ch}</div>
<div class="big" style="font-size:150px;color:var(--coral);margin-top:70px;animation:{a("pop", 16.9, .5, BOUNCE)}">$39.99</div>
<div style="font-size:34px;font-weight:700;color:var(--muted);animation:{a("fadeIn", 17.1)}">launch price · reg. <s>$49.99</s></div>
{handle_bar(17.2)}''')
    v.total = 19.5
    return v, "Size guide"

# ====================================================================== 3. RainBoho vs Ash Starlight
def v3():
    v = Video("03-rainboho-vs-ash-starlight", 18.0)
    v.scene(0, 3.4, f'''
<div class="kicker" style="animation:{a("fadeIn", .3)}">Which one is you?</div>
<div class="big" style="font-size:150px;color:var(--coral);animation:{a("fromL", .4, .7)}">RainBoho</div>
<div class="big" style="font-size:80px;color:var(--muted);margin:16px 0;animation:{a("pop", .9, .5, BOUNCE)}">vs</div>
<div class="big" style="font-size:140px;color:var(--sage);animation:{a("fromR", 1.1, .7)}">Ash Starlight</div>
<div style="display:flex;gap:30px;margin-top:80px">
 <div style="transform:rotate(-4deg)"><div style="animation:{a("fromL", 1.6, .7)}">{mat_flat("rb", 440)}</div></div>
 <div style="transform:rotate(4deg)"><div style="animation:{a("fromR", 1.8, .7)}">{mat_flat("as", 440)}</div></div>
</div>''')
    def design(s, e, n, name_parts, sub, d, box, tags, sw):
        sws = "".join(f'<i style="width:70px;height:70px;border-radius:50%;background:{c};display:block;border:5px solid #fff;'
                      f'box-shadow:0 8px 14px -6px rgba(0,0,0,.3);animation:{a("pop", s+1.9+i*.1, .4, BOUNCE)}"></i>' for i, c in enumerate(sw))
        tg = "".join(f'<div class="pill p-{c}" style="font-size:36px;animation:{a("pop", s+2.3+i*.15, .45, BOUNCE)}">{icon(ic)}{t}</div>' for i, (ic, c, t) in enumerate(tags))
        letters = "".join(f'<span class="w" style="color:{col};animation:{a("up", s+.3+i*.05, .45, BOUNCE)}">{ch}</span>' if ch != " " else "&nbsp;"
                          for i, (ch, col) in enumerate(name_parts))
        v.scene(s, e, f'''
<div class="kicker" style="animation:{a("fadeIn", s+.2)}">Design 0{n}</div>
<div class="big" style="font-size:150px">{letters}</div>
<div class="sub" style="animation:{a("up", s+.9)}">{sub}</div>
<div style="position:relative;margin-top:60px">
 <div style="animation:{a("swingIn", s+.8, .9, BOUNCE)}">{mat3d(d, 820)}</div>
 <div style="position:absolute;right:-30px;top:-60px;animation:{a("pop", s+1.5, .5, BOUNCE)}">{photo(box, 230, 300, 6)}</div>
</div>
<div style="display:flex;gap:16px;margin-top:70px;align-items:center">{sws}</div>
<div style="display:flex;gap:16px;margin-top:36px;flex-wrap:wrap;justify-content:center">{tg}</div>''')
    rb = [(c, "#4A3422") for c in "Rain"] + [(c, "#E07A5F") for c in "Boho"]
    asl = [(c, "#4A3422") for c in "Ash"] + [(" ", "")] + [(c, "#7AA3BD") for c in "Starlight"]
    design(3.4, 7.2, 1, rb, "Boho rainbows, clouds &amp; hearts in <b>warm sand tones</b>", "rb", BOX_RB,
           [("sun","mustard","Warm &amp; cheerful"),("home","coral","Wood &amp; beige rooms")], ["#E8D9C6","#C3A386","#D2AE98","#F7F0E7"])
    design(7.2, 11.0, 2, asl, "Stars &amp; crescent moons on <b>soft ash grey</b>", "as", BOX_AS,
           [("moon","sky","Calm &amp; dreamy"),("home","sage","Grey &amp; white rooms")], ["#ADA7A0","#8E8882","#E6E1DA","#F4F1EC"])
    same = [("ruler","sage","Same 5.6 × 4 ft"),("layers","sky","Same 0.5 in cushion"),("shield","coral","Same CPSIA · CPC")]
    sm = "".join(f'<div class="pill p-{c}" style="font-size:38px;animation:{a("fromL", 12.4+i*.18, .5)}">{icon(ic)}{t}</div>' for i, (ic, c, t) in enumerate(same))
    v.scene(11.0, 14.0, f'''
<div class="big" style="font-size:130px">{words("Same mat.", 11.2, .15)}<br><span class="w" style="color:var(--sage);animation:{a("pop", 11.6, .5, BOUNCE)}">Different</span>&nbsp;{words("vibe.", 11.8)}</div>
<div style="display:flex;gap:26px;margin-top:70px">
 <div style="transform:rotate(-3deg)"><div style="animation:{a("up", 11.9, .6)}">{mat_flat("rb", 450)}</div></div>
 <div style="transform:rotate(3deg)"><div style="animation:{a("up", 12.1, .6)}">{mat_flat("as", 450)}</div></div>
</div>
<div style="display:flex;flex-direction:column;gap:18px;margin-top:70px;align-items:center">{sm}</div>''')
    v.scene(14.0, 18.0, f'''
<div class="big" style="font-size:130px">{words("Can't decide?", 14.2, .15)}</div>
<div class="big" style="font-size:150px;margin-top:10px">{words("Get", 14.6)}&nbsp;<span class="w" style="color:var(--mustard);animation:{a("pop", 14.75, .55, BOUNCE)}">both.</span></div>
<div style="position:relative;width:940px;height:560px;margin-top:60px">
 <div style="position:absolute;left:10px;top:40px;transform:rotate(-6deg)"><div style="animation:{a("fromL", 14.9, .6)}">{mat_flat("rb", 500)}</div></div>
 <div style="position:absolute;right:10px;top:110px;transform:rotate(5deg)"><div style="animation:{a("fromR", 15.0, .6)}">{mat_flat("as", 500)}</div></div>
 <div style="position:absolute;left:50%;top:170px;margin-left:-180px;width:360px;height:360px;border-radius:50%;background:var(--mustard);color:#fff;overflow:hidden;
  display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Fredoka;box-shadow:0 26px 40px -16px rgba(169,118,27,.75);border:10px solid #fff;
  animation:{a("spinPop", 15.4, .8, BOUNCE)}">
  <div style="font-size:38px;font-weight:500;letter-spacing:3px">2 FOR</div><div style="font-size:150px;font-weight:600;line-height:.9">$89</div>
  <div style="font-size:28px;font-weight:500">mix &amp; match</div>
  <i style="position:absolute;top:0;bottom:0;left:0;width:40%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.45),transparent);animation:{a("shine", 16.3, .9, "ease-in-out")}"></i></div>
</div>
<div style="font-size:34px;font-weight:700;color:var(--muted);margin-top:20px;animation:{a("fadeIn", 16.0)}">Single mat <b style="color:var(--coral)">$39.99</b> launch price <s>$49.99</s></div>
<div style="animation:{a("pulse", 17.0, 1, "ease-in-out", "infinite")}">{handle_bar(16.2)}</div>
{dino(15.8, 200, "Best deal!", 16.3, "right:30px;bottom:520px;position:absolute", "tr", "right:60px;top:-76px")}''')
    return v, "Pick your vibe"

if __name__ == "__main__":
    B = os.path.join(HERE, "build")
    os.makedirs(B, exist_ok=True)
    out = []
    for fn in (v1, v2, v3):
        vid, tag = fn()
        p = os.path.join(B, vid.name + ".html")
        open(p, "w").write(vid.html(tag))
        out.append({"html": p, "name": vid.name, "dur": vid.total})
    json.dump(out, open(os.path.join(B, "videos.json"), "w"), indent=1)
    print(out)
