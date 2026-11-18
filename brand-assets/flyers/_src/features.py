"""Feature close-ups (1080x1080 each): 3D tile illustrations textured with the real mat surface.
python3 features.py && node render.js && python3 post.py
Illustrations, not photos: they show the construction (16 interlocking 0.5 in EVA tiles, wipe-clean top), not test results.
"""
import os, json
from flyers import CSS, BUILD, stripe

EXTRA = """
.f{width:1080px;height:1080px}
.scene{position:absolute;left:0;right:0;top:250px;height:720px;perspective:2200px}
.iso{position:absolute;left:50%;top:50%;width:0;height:0;transform-style:preserve-3d;transform:rotateX(58deg) rotateZ(-36deg)}
.t{position:absolute;transform-style:preserve-3d}
.t i{position:absolute;inset:0;display:block}
.ttl{font-family:Fredoka,sans-serif;font-weight:600;letter-spacing:-.02em;line-height:1.02;font-size:66px}
.sub{font-size:26px;font-weight:700;color:#6B5A4B;line-height:1.4;margin-top:12px}
.co{position:absolute;display:flex;align-items:center;gap:12px;font-weight:900;font-size:22px;color:#3B2A1C;z-index:20}
.co b{background:#fff;border-radius:999px;padding:10px 18px;box-shadow:0 12px 26px -14px rgba(59,42,28,.55);white-space:nowrap}
.co span{display:block;height:3px;background:#3B2A1C;border-radius:2px}
.co .dot{width:14px;height:14px;border-radius:50%;background:#C2573B;border:3px solid #fff;box-shadow:0 0 0 2px #C2573B;flex:none}
"""

MATS = {"ash": ("../img/mat-ash.jpg", "#BDB9B6", "#A9A5A2"), "rb": ("../img/mat-rainboho.jpg", "#DDD5CB", "#C9C0B5")}

def poly(S, d, n=3):
    """Interlocking-tile outline: square S with n tabs and n slots of depth d on every edge, in a (S+2d) box."""
    seg = S / (2 * n)
    pts = []
    def edge(p0, dirv, outv):
        for k in range(2 * n):
            a = (p0[0] + dirv[0] * seg * k, p0[1] + dirv[1] * seg * k)
            b = (p0[0] + dirv[0] * seg * (k + 1), p0[1] + dirv[1] * seg * (k + 1))
            off = d if k % 2 == 0 else -d
            w = seg * 0.12
            pts.append(a)
            pts.append((a[0] + dirv[0] * w + outv[0] * off, a[1] + dirv[1] * w + outv[1] * off))
            pts.append((b[0] - dirv[0] * w + outv[0] * off, b[1] - dirv[1] * w + outv[1] * off))
    edge((d, d), (1, 0), (0, -1))          # top
    edge((d + S, d), (0, 1), (1, 0))       # right
    edge((d + S, d + S), (-1, 0), (0, 1))  # bottom
    edge((d, d + S), (0, -1), (-1, 0))     # left
    return "polygon(" + ",".join(f"{x:.1f}px {y:.1f}px" for x, y in pts) + ")"

def tile(x, y, S, T, mat="ash", z=0, d=None, bgx=0, bgy=0, bgs=None, shadow=True):
    img, side, side2 = MATS[mat]
    d = d if d is not None else S * 0.06
    cp = poly(S, d)
    B = S + 2 * d
    bgs = bgs or B * 4
    layers = "".join(f'<i style="clip-path:{cp};background:{side2 if k < T*0.35 else side};transform:translateZ({k}px)"></i>' for k in range(T))
    top = (f'<i style="clip-path:{cp};background:url({img}) {-bgx}px {-bgy}px/{bgs}px auto;transform:translateZ({T}px);'
           f'box-shadow:inset 0 0 0 1px rgba(255,255,255,.4)"></i>')
    sh = (f'<i style="clip-path:{cp};background:rgba(59,42,28,.28);filter:blur(10px);transform:translate(14px,14px)"></i>' if shadow else "")
    return f'<div class="t" style="left:{x}px;top:{y}px;width:{B:.0f}px;height:{B:.0f}px;transform:translateZ({z}px)">{sh}{layers}{top}</div>'

def frame(title, sub, body):
    return f'''<div class="f"><div class="paper"></div>{stripe(True)}
<img src="../img/logo.png" style="position:absolute;right:56px;top:40px;height:90px">
<div style="position:absolute;left:64px;top:64px;width:760px">
 <div class="eyebrow" style="font-size:18px">Moon Walkers Premium EVA Playmat</div>
 <h1 class="ttl" style="margin-top:8px">{title}</h1><p class="sub">{sub}</p></div>
{body}
<div style="position:absolute;left:0;right:0;bottom:34px;text-align:center;font-weight:800;font-size:22px">16 tiles · 67 × 48 in · CPC/CPSIA tested · <span style="color:#C2573B">tovinest.com</span></div>
{stripe(False)}</div>'''

def callout(dx, dy, text, line=50, side="right"):
    """dx,dy = where the dot sits; label extends to the right or left of it."""
    if side == "right":
        return f'<div class="co" style="left:{dx-7}px;top:{dy-22}px"><span class="dot"></span><span style="width:{line}px"></span><b>{text}</b></div>'
    return f'<div class="co" style="left:{dx+7}px;top:{dy-22}px;flex-direction:row-reverse;transform:translateX(-100%)"><span class="dot"></span><span style="width:{line}px"></span><b>{text}</b></div>'

def p_section():
    S = 470
    body = f'''<div class="scene"><div class="iso">{tile(-S/2 - 30, -S/2 - 30, S, 62, "ash", bgx=420, bgy=330, bgs=2100)}</div></div>
{callout(480, 520, "Printed design on top", 50, "left")}
{callout(360, 665, "Interlocking edges", 50, "left")}
{callout(560, 790, "Dense, closed-cell EVA", 50, "left")}
{callout(850, 650, "0.5 in thick", 24)}'''
    return frame("Built from <em>dense EVA</em>", "Not sponge foam. A firm, springy foam that holds its shape.", body)

def drops():
    def drop(x, y, w, h, r=0):
        return (f'<svg style="position:absolute;left:{x}px;top:{y}px;transform:rotate({r}deg);overflow:visible" width="{w}" height="{h}" viewBox="0 0 100 70">'
                f'<defs><radialGradient id="g{x}{y}" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#FFD58A"/><stop offset=".55" stop-color="#F2A23A" stop-opacity=".92"/>'
                f'<stop offset="1" stop-color="#C96A12" stop-opacity=".95"/></radialGradient></defs>'
                f'<ellipse cx="54" cy="44" rx="46" ry="24" fill="rgba(120,60,10,.22)" filter="blur(3px)"/>'
                f'<path d="M8 38C6 18 28 6 52 6s44 12 42 32-22 26-44 26S10 56 8 38z" fill="url(#g{x}{y})"/>'
                f'<ellipse cx="34" cy="22" rx="14" ry="6" fill="#fff" opacity=".85" transform="rotate(-12 34 22)"/>'
                f'<ellipse cx="70" cy="48" rx="8" ry="3" fill="#fff" opacity=".35"/></svg>')
    D = [(330, 470, 170, 110, 8), (520, 420, 100, 66, -6), (470, 590, 70, 46, 10), (600, 560, 54, 36, 0), (280, 640, 60, 40, -14), (650, 470, 40, 28, 0)]
    return "".join(drop(*a) for a in D)

def p_spill():
    cloth = ('<svg style="position:absolute;left:650px;top:600px;filter:drop-shadow(0 22px 20px rgba(59,42,28,.35));transform:rotate(-14deg)" width="300" height="240" viewBox="0 0 300 240">'
             '<rect x="20" y="20" width="250" height="190" rx="22" fill="#8FA67D"/>'
             '<path d="M20 60h250M20 100h250M20 140h250M20 180h250" stroke="#9DB38B" stroke-width="3"/>'
             '<path d="M270 130v58a22 22 0 0 1-22 22h-60z" fill="#B7C9A7"/><path d="M270 130l-82 80" stroke="#7E946D" stroke-width="3"/>'
             '<rect x="20" y="20" width="250" height="190" rx="22" fill="none" stroke="#7E946D" stroke-width="4" stroke-dasharray="2 8"/></svg>')
    swipe = '<div style="position:absolute;left:560px;top:540px;width:300px;height:150px;border-radius:80px;background:rgba(255,255,255,.18);transform:rotate(-18deg);filter:blur(6px)"></div>'
    body = f'''<div style="position:absolute;left:90px;right:90px;top:300px;height:600px;border-radius:40px;overflow:hidden;
 box-shadow:0 40px 70px -34px rgba(59,42,28,.6);background:url(../img/mat-ash.jpg) -300px -260px/1500px auto">
 <div style="position:absolute;inset:0;background:linear-gradient(160deg,rgba(255,255,255,.18),transparent 50%,rgba(0,0,0,.08))"></div></div>
<div style="position:absolute;left:0;top:0;width:1080px;height:1080px">{drops()}{swipe}{cloth}</div>
{callout(140, 352, "Spills sit on top", 40)}
{callout(700, 892, "One wipe and it's clean", 40, "left")}'''
    return frame("Spills <em>wipe right off</em>", "Closed-cell EVA doesn't soak up juice or milk the way sponge foam does.", body)

def p_lock():
    S = 330
    arrow = ('<svg style="position:absolute;left:470px;top:600px;z-index:30;transform:rotate(-30deg)" width="140" height="60" viewBox="0 0 140 60">'
             '<path d="M10 30h110M95 10l25 20-25 20" fill="none" stroke="#C2573B" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    body = f'''<div class="scene"><div class="iso">
 {tile(-S - 70, -S/2, S, 40, "ash", bgx=540, bgy=400, bgs=1900, shadow=False)}
 {tile(20, -S/2, S, 40, "ash", bgx=1010, bgy=400, bgs=1900, shadow=False)}
</div></div>{arrow}
{callout(300, 860, "Tabs and slots lock together", 40)}'''
    return frame("Snaps together, <em>lifts apart</em>", "Tiles lock tight for play and come apart for cleaning, moving or rearranging.", body)

def p_grid():
    S, T, gap = 104, 18, 0
    d = S * 0.06
    step = S
    tiles = []
    for r in range(4):
        for c in range(4):
            lift = (r, c) == (1, 2)
            x = -2 * step + c * step - (6 if lift else 0)
            y = -2 * step + r * step
            tiles.append(tile(x, y, S, T, "ash", z=(150 if lift else 0), d=d, bgx=S*0.45 + c * S, bgy=S*0.35 + r * S, bgs=5.2 * S, shadow=not lift))
    body = f'''<div class="scene" style="transform:scale(1.55);transform-origin:50% 55%"><div class="iso">{"".join(tiles)}</div></div>
{callout(700, 430, "Lift out any single tile", 40)}'''
    return frame("16 tiles, <em>one big mat</em>", "67 × 48 in when assembled. Lift any tile out to clean under it or rearrange.", body)

PAGES = [("1-dense-eva", p_section), ("2-wipe-clean", p_spill), ("3-interlocking", p_lock), ("4-sixteen-tiles", p_grid)]

if __name__ == "__main__":
    jobs = [j for j in json.load(open(os.path.join(BUILD, "jobs.json"))) if "feature-" not in j["name"]]
    for name, fn in PAGES:
        p = os.path.join(BUILD, f"feature-{name}.html")
        open(p, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS + EXTRA}</style></head><body>{fn()}</body></html>')
        jobs.append({"html": p, "name": f"tovinest-feature-{name}", "w": 1080, "h": 1080})
    json.dump(jobs, open(os.path.join(BUILD, "jobs.json"), "w"), indent=1)
    print("ok")
