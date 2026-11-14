"""Generate HTML for the Tovi Nest carousels. Run: python3 gen.py  -> build/*.html
Then: node render.js  -> ../A..D/*.png
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")
BA = "../../.."  # brand-assets/ relative to build/
MASCOT = f"{BA}/tovinest-mascot.png"
BADGE = f"{BA}/tovinest-badge-tn.png"
BOX_RB = "../img/box-rainboho.jpg"
BOX_AS = "../img/box-ashstarlight.jpg"

# ---------------------------------------------------------------- icons
ICONS = {
    "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6z"/><path d="M8.6 12.2l2.4 2.4 4.4-4.8"/>',
    "drop": '<path d="M12 3.2c3 4 6 7.4 6 10.9a6 6 0 0 1-12 0c0-3.5 3-6.9 6-10.9z"/><path d="M9.2 14.6a2.9 2.9 0 0 0 2.6 2.6"/>',
    "puzzle": '<path d="M4 7.5h3.6a2.4 2.4 0 1 1 4.8 0H16v3.6a2.4 2.4 0 1 1 0 4.8v3.6h-3.6a2.4 2.4 0 1 0-4.8 0H4v-3.6a2.4 2.4 0 1 0 0-4.8z"/>',
    "feet": '<path d="M7.6 20.5c-2 0-3-1.8-2.7-4.3.3-2.6 1.2-5.2 3.3-5.2s2.4 2.6 2.1 5.3c-.3 2.4-.9 4.2-2.7 4.2z"/><path d="M16.4 15.5c-1.8 0-2.4-1.8-2.7-4.2-.3-2.7 0-5.3 2.1-5.3s3 2.6 3.3 5.2c.3 2.5-.7 4.3-2.7 4.3z"/>',
    "ruler": '<rect x="2.5" y="8" width="19" height="8" rx="1.6"/><path d="M6.2 8v3M9.4 8v4.2M12.6 8v3M15.8 8v4.2M19 8v3"/>',
    "layers": '<path d="M12 4l9 4.8-9 4.8-9-4.8z"/><path d="M3 13.6l9 4.8 9-4.8"/>',
    "leaf": '<path d="M5 19.5C5 11 10 5.5 19.5 4.5 19.5 14 14 19.5 5 19.5z"/><path d="M5 19.5l8.5-8.5"/>',
    "box": '<path d="M3.5 7.5L12 3.6l8.5 3.9v9L12 20.4l-8.5-3.9z"/><path d="M3.5 7.5L12 11.4l8.5-3.9M12 11.4v9"/>',
    "heart": '<path d="M12 20s-7.5-4.6-7.5-10.2A4.1 4.1 0 0 1 12 7.4a4.1 4.1 0 0 1 7.5 2.4C19.5 15.4 12 20 12 20z"/>',
    "check": '<path d="M5 12.6l4.4 4.4L19 7.4"/>',
    "home": '<path d="M4 11l8-6.8 8 6.8v9H4z"/><path d="M10 20v-5.2h4V20"/>',
    "sponge": '<rect x="3.5" y="9.5" width="17" height="9.5" rx="3"/><path d="M7 6.2c1-1.1 2 1.1 3 0s2 1.1 3 0 2 1.1 3 0"/><circle cx="8.5" cy="13.5" r=".6"/><circle cx="12.5" cy="15.3" r=".6"/><circle cx="15.8" cy="12.8" r=".6"/>',
    "baby": '<circle cx="12" cy="12.5" r="8"/><path d="M9.2 14.4c1.6 1.4 4 1.4 5.6 0"/><path d="M12 4.5c-.8-1.4.6-2.4 1.6-1.6"/><circle cx="9.3" cy="11.3" r=".7" fill="currentColor"/><circle cx="14.7" cy="11.3" r=".7" fill="currentColor"/>',
    "timer": '<circle cx="12" cy="13.2" r="7.4"/><path d="M12 9.4v3.8l2.8 1.8M9.8 3.2h4.4"/>',
    "crib": '<rect x="3" y="7" width="18" height="10.5" rx="1.6"/><path d="M7.2 7v10.5M11.4 7v10.5M15.6 7v10.5M3.5 17.5v2.5M20.5 17.5v2.5"/>',
    "tag": '<path d="M3.5 12.2V4.5a1 1 0 0 1 1-1h7.7l8.3 8.3a1.4 1.4 0 0 1 0 2l-6.6 6.6a1.4 1.4 0 0 1-2 0z"/><circle cx="8" cy="8" r="1.4"/>',
    "bag": '<path d="M5 8h14l-1.2 12H6.2z"/><path d="M9 8V6.5a3 3 0 0 1 6 0V8"/>',
    "star": '<path d="M12 3.6l2.5 5.2 5.7.8-4.1 4 1 5.6-5.1-2.7-5.1 2.7 1-5.6-4.1-4 5.7-.8z"/>',
    "moon": '<path d="M19.5 14.5A8 8 0 1 1 9.5 4.5a6.4 6.4 0 0 0 10 10z"/>',
    "rainbow": '<path d="M3 17a9 9 0 0 1 18 0"/><path d="M6.5 17a5.5 5.5 0 0 1 11 0"/><path d="M10 17a2 2 0 0 1 4 0"/>',
    "volume": '<path d="M4 9.5h3.5L12 5.5v13l-4.5-4H4z"/><path d="M15.5 9.5c1.2 1.4 1.2 3.6 0 5"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2.8v2.4M12 18.8v2.4M2.8 12h2.4M18.8 12h2.4M5.5 5.5l1.7 1.7M16.8 16.8l1.7 1.7M5.5 18.5l1.7-1.7M16.8 7.2l1.7-1.7"/>',
    "gift": '<rect x="3.5" y="8.5" width="17" height="4" rx="1"/><path d="M5 12.5v8h14v-8M12 8.5v12"/><path d="M12 8.5c-1.5-3.5-5.5-3.5-5-1s5 1 5 1zm0 0c1.5-3.5 5.5-3.5 5-1s-5 1-5 1z"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "expand": '<path d="M4 9V4h5M20 15v5h-5M4 4l6 6M20 20l-6-6"/>',
}

def icon(name, sw=2.1, fill=False):
    f = 'fill="currentColor" stroke="none"' if fill else f'fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'
    return f'<svg viewBox="0 0 24 24" {f}>{ICONS[name]}</svg>'

HEART_SVG = '<svg viewBox="0 0 24 24"><path fill="#E9A6A1" d="M12 21s-9-5.6-9-12.2A5 5 0 0 1 12 6a5 5 0 0 1 9 2.8C21 15.4 12 21 12 21z"/></svg>'

def wordmark(size=44):
    L = [("T", "#7A8F6A"), ("o", "#7AA3BD"), ("v", "#E07A5F"), ("i", "#E9B041"), (" ", ""),
         ("N", "#E9B041"), ("e", "#7AA3BD"), ("s", "#E9A6A1"), ("t", "#7A8F6A")]
    out = []
    for ch, c in L:
        if ch == " ":
            out.append('<span class="gap"></span>')
        elif ch == "i":
            out.append(f'<span class="i" style="color:{c}">ı{HEART_SVG}</span>')
        else:
            out.append(f'<span style="color:{c}">{ch}</span>')
    return f'<div class="wm" style="font-size:{size}px">{"".join(out)}</div>'

def sprig(x, y, size=200, rot=0, color="#7A8F6A", op=.55, flip=False):
    sx = -1 if flip else 1
    leaves = "".join(
        f'<ellipse cx="{cx}" cy="{cy}" rx="15" ry="7" transform="rotate({r} {cx} {cy})" fill="{color}"/>'
        for cx, cy, r in [(58, 34, -40), (82, 52, 30), (60, 66, -35), (88, 86, 35), (64, 98, -30), (92, 122, 40), (70, 134, -25)])
    return (f'<svg class="sprig" style="left:{x}px;top:{y}px;width:{size}px;height:{size}px;opacity:{op};'
            f'transform:rotate({rot}deg) scaleX({sx})" viewBox="0 0 160 160">'
            f'<path d="M48 20 C70 60 78 110 76 150" stroke="{color}" stroke-width="3" fill="none" stroke-linecap="round"/>{leaves}</svg>')

def spark(x, y, s=34, color="#E9B041", op=.85):
    return (f'<svg class="spark" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;opacity:{op}" viewBox="0 0 24 24">'
            f'<path fill="{color}" d="M12 1c.8 6 3.4 8.6 11 11-7.6 2.4-10.2 5-11 11-.8-6-3.4-8.6-11-11 7.6-2.4 10.2-5 11-11z"/></svg>')

# ---------------------------------------------------------------- mat renders
def _puzzle_lines(w, h, cols, rows, color):
    """Interlocking seams drawn as square-wave lines."""
    paths = []
    t, step = 6, 22
    for c in range(1, cols):
        x = w * c / cols
        d, y, k = f"M{x:.1f},0", 0, 0
        while y < h:
            off = t if k % 2 else -t
            y2 = min(h, y + step)
            d += f" L{x+off:.1f},{y:.1f} L{x+off:.1f},{y2:.1f}"
            y, k = y2, k + 1
        paths.append(d)
    for r in range(1, rows):
        y = h * r / rows
        d, x, k = f"M0,{y:.1f}", 0, 0
        while x < w:
            off = t if k % 2 else -t
            x2 = min(w, x + step)
            d += f" L{x:.1f},{y+off:.1f} L{x2:.1f},{y+off:.1f}"
            x, k = x2, k + 1
        paths.append(d)
    return "".join(f'<path d="{p}" fill="none" stroke="{color}" stroke-width="2.2" stroke-linejoin="round"/>' for p in paths)

def rainboho_pattern(pid):
    return f'''<pattern id="{pid}" width="200" height="200" patternUnits="userSpaceOnUse">
 <rect width="200" height="200" fill="#E8D9C6"/>
 <g fill="none" stroke-linecap="round">
  <path d="M22 78a32 32 0 0 1 64 0" stroke="#C3A386" stroke-width="8"/>
  <path d="M32 78a22 22 0 0 1 44 0" stroke="#F6EEE4" stroke-width="7"/>
  <path d="M42 78a12 12 0 0 1 24 0" stroke="#D6B9A0" stroke-width="7"/>
  <path d="M122 178a32 32 0 0 1 64 0" stroke="#C3A386" stroke-width="8"/>
  <path d="M132 178a22 22 0 0 1 44 0" stroke="#F6EEE4" stroke-width="7"/>
  <path d="M142 178a12 12 0 0 1 24 0" stroke="#D6B9A0" stroke-width="7"/>
 </g>
 <g fill="#F7F0E7"><circle cx="134" cy="40" r="11"/><circle cx="148" cy="34" r="14"/><circle cx="163" cy="41" r="10"/><rect x="128" y="40" width="42" height="11" rx="5.5"/></g>
 <g fill="#F7F0E7"><circle cx="34" cy="140" r="9"/><circle cx="46" cy="134" r="12"/><circle cx="59" cy="141" r="8"/><rect x="28" y="140" width="38" height="9" rx="4.5"/></g>
 <path fill="#D2AE98" d="M150 112s-11-6.8-11-14.8a6 6 0 0 1 11-3.4 6 6 0 0 1 11 3.4c0 8-11 14.8-11 14.8z"/>
 <path fill="#C3A386" d="M98 128a12 12 0 1 1-6-16 9.6 9.6 0 0 0 6 16z"/>
 <path fill="#F7F0E7" d="M100 20l2 5.2 5.2 2-5.2 2-2 5.2-2-5.2-5.2-2 5.2-2z"/>
 <path fill="#F7F0E7" d="M182 92l1.5 3.8 3.8 1.5-3.8 1.5-1.5 3.8-1.5-3.8-3.8-1.5 3.8-1.5z"/>
 <g fill="#CDB096"><circle cx="18" cy="190" r="2.6"/><circle cx="108" cy="72" r="2.6"/><circle cx="192" cy="10" r="2.6"/><circle cx="72" cy="104" r="2.2"/></g>
</pattern>'''

def ash_pattern(pid):
    star = lambda cx, cy, r: (f'<path fill="#F4F1EC" transform="translate({cx} {cy}) scale({r/10})" '
                              'd="M0-10l2.9 6 6.6.9-4.8 4.6 1.2 6.5L0 4.9-5.9 8l1.2-6.5-4.8-4.6 6.6-.9z"/>')
    return f'''<pattern id="{pid}" width="190" height="190" patternUnits="userSpaceOnUse">
 <rect width="190" height="190" fill="#ADA7A0"/>
 <path fill="#F4F1EC" d="M58 54a20 20 0 1 1-12-30 16 16 0 0 0 12 30z"/>
 <path fill="#F4F1EC" d="M156 150a16 16 0 1 1-9.6-24 12.8 12.8 0 0 0 9.6 24z"/>
 {star(140, 40, 11)}{star(40, 140, 9)}{star(100, 100, 6)}
 <g fill="none" stroke="#E6E1DA" stroke-width="2.2"><path d="M100 12l10 12-10 12-10-12z"/><path d="M14 80l8 10-8 10-8-10z"/><path d="M178 84l8 10-8 10-8-10z"/></g>
 <g fill="#E6E1DA"><circle cx="78" cy="160" r="2.6"/><circle cx="92" cy="160" r="2.6"/><circle cx="106" cy="160" r="2.6"/><circle cx="170" cy="20" r="2.2"/><circle cx="20" cy="22" r="2.2"/><circle cx="130" cy="78" r="2"/></g>
 <path fill="#F4F1EC" d="M64 96l1.6 4 4 1.6-4 1.6-1.6 4-1.6-4-4-1.6 4-1.6z"/>
</pattern>'''

_uid = [0]
def mat_svg(design="rb", W=670, H=480, grid=True, scale=1.0):
    _uid[0] += 1
    pid = f"p{_uid[0]}"
    pat = rainboho_pattern(pid) if design == "rb" else ash_pattern(pid)
    seam = "rgba(120,92,66,.30)" if design == "rb" else "rgba(70,66,62,.32)"
    lines = _puzzle_lines(W, H, 4, 4, seam) if grid else ""
    return (f'<svg viewBox="0 0 {W} {H}" preserveAspectRatio="none"><defs>{pat}</defs>'
            f'<rect width="{W}" height="{H}" fill="url(#{pid})" transform="scale(1)"/>'
            f'<g transform="scale(1)">{lines}</g>'
            f'<rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="8" fill="none" stroke="rgba(255,255,255,.35)" stroke-width="3"/></svg>')

def mat3d(design="rb", width=760, rx=56, rz=-14, mt=0):
    h = round(width * 48 / 67)
    cls = "mat3d ash" if design == "as" else "mat3d"
    return (f'<div class="mat3d-wrap" style="margin-top:{mt}px"><div class="{cls}" style="width:{width}px;height:{h}px;'
            f'transform:rotateX({rx}deg) rotateZ({rz}deg)">'
            f'<div class="layer edge"></div><div class="layer top">{mat_svg(design)}</div></div></div>')

def mat_flat(design="rb", width=640, extra=""):
    h = round(width * 48 / 67)
    return (f'<div style="width:{width}px;height:{h}px;border-radius:12px;overflow:hidden;'
            f'box-shadow:0 12px 0 {"#CDBBA6" if design=="rb" else "#8E8882"},0 40px 50px -20px rgba(80,60,40,.45);{extra}">{mat_svg(design)}</div>')

# ---------------------------------------------------------------- shell
def dino(right=None, left=None, bottom=None, top=None, w=260, bubble=None, bpos="tl", bstyle=""):
    pos = ";".join(f"{k}:{v}px" for k, v in [("right", right), ("left", left), ("bottom", bottom), ("top", top)] if v is not None)
    b = f'<div class="bubble {bpos}" style="{bstyle}">{bubble}</div>' if bubble else ""
    anchor = "t" if top is not None else "b"
    return f'<div class="dino {anchor}" style="{pos};width:{w}px">{b}<img src="{MASCOT}"></div>'

def page(n, total, tag, body, bgx=""):
    dots = "".join(f'<i class="{"on" if i == n else ""}"></i>' for i in range(1, total + 1))
    last = n == total
    right = ('<div class="swipe" style="color:var(--coral)">Shop now ' + icon("bag", 2.4) + '</div>') if last else \
            ('<div class="swipe">Swipe ' + icon("arrow", 2.6) + '</div>')
    bg = ('<div class="bg"><div class="blob b1"></div><div class="blob b2"></div><div class="blob b3"></div>'
          + sprig(-40, 1080, 200, -20, '#7A8F6A', .4) + sprig(900, 980, 240, 160, "#7A8F6A", .45)
          + spark(930, 150, 38) + spark(60, 1180, 28, "#E07A5F", .6) + spark(990, 640, 24, "#7AA3BD", .7) + bgx + '</div>')
    return f'''{bg}
<header><div class="lockup"><img src="{BADGE}">{wordmark(46)}</div><div class="tag">{tag}</div></header>
<main>{body}</main>
<footer><div class="handle">{icon("bag", 2.4).replace("<svg", '<svg style="width:30px;height:30px;color:#7A8F6A"')}<span><b>@tovinest</b> · Ships across the USA</span></div>
<div class="dots">{dots}</div>{right}</footer>'''

def doc(inner, ratio):
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../style.css"></head>
<body><div class="slide {ratio}">{inner}</div></body></html>'''

# ---------------------------------------------------------------- price block
def price_block(center=True, duo=True):
    duo_html = ('<div class="card price duo"><div class="lbl">Bundle deal</div><div class="now">2 for $89.99</div>'
                '<div class="note">Mix &amp; match · save $9.99</div></div>') if duo else ""
    return (f'<div class="price-row" style="justify-content:{"center" if center else "flex-start"}">'
            '<div class="card price"><div class="lbl">Each</div><div class="now">$49.99</div></div>'
            f'{duo_html}</div>')

def cta_block(text="DM to order", supervise=True):
    note = '<div class="note-sm" style="margin-top:10px">Always supervise children during play.</div>' if supervise else ""
    return (f'<div style="display:flex;flex-direction:column;align-items:center;margin-top:30px">'
            f'<div class="cta">{icon("bag", 2.4)}{text}</div>'
            f'<div class="handle-big">Ships across the USA · <span>@tovinest</span></div>{note}</div>')

# ================================================================ SLIDES
def photo(src, w, h, rot=0, extra=""):
    return f'<div class="photo" style="width:{w}px;height:{h}px;transform:rotate({rot}deg);{extra}"><img src="{src}"></div>'

def dims(w_px, h_px, inner, top_label="67 in", top_small="170 cm", side_label="48 in", side_small="122 cm"):
    """inner (mat) of size w_px x h_px placed with dimension lines above and left."""
    return f'''<div style="position:relative;width:{w_px+150}px;height:{h_px+130}px;margin:0 auto">
 <div style="position:absolute;left:150px;top:130px">{inner}</div>
 <div class="dim h" style="left:150px;top:52px;width:{w_px}px"><div class="t">{top_label}<small>{top_small}</small></div></div>
 <div class="dim v" style="left:62px;top:130px;height:{h_px}px"><div class="t">{side_label}<small>{side_small}</small></div></div>
</div>'''

def feat(ic, col, title, text):
    return f'<div class="card feat"><div class="ico i-{col}">{icon(ic)}</div><div><h3>{title}</h3><p>{text}</p></div></div>'

def tile(ic, col, title, text):
    return f'<div class="card tile"><div class="ico i-{col}">{icon(ic)}</div><h3>{title}</h3><p>{text}</p></div>'

def pills(items, gap=16, center=True):
    return (f'<div style="display:flex;flex-wrap:wrap;gap:{gap}px;justify-content:{"center" if center else "flex-start"}">'
            + "".join(f'<div class="pill p-{c}">{icon(i)}{t}</div>' for i, c, t in items) + '</div>')

# ---------------- A: What's in the box
def A():
    T, tag = 6, "Unboxing"
    s = []
    s.append(("cover", page(1, T, tag, f'''
<div class="center" style="display:flex;flex-direction:column;align-items:center">
 <div class="kicker">Unboxing the playmat</div>
 <h1>What's in<br>the <em>box?</em></h1>
 <div class="sub">The <b>Moon Walkers Premium EVA Playmat</b> · $49.99</div>
 <div style="position:relative;width:936px;height:600px;margin-top:44px">
  <div style="position:absolute;left:430px;top:30px">{photo(BOX_AS, 360, 470, 7)}</div>
  <div style="position:absolute;left:170px;top:10px">{photo(BOX_RB, 400, 530, -4)}</div>
  <div style="position:absolute;right:-6px;top:-10px;width:210px;height:210px;border-radius:50%;background:var(--coral);color:#fff;
   display:flex;flex-direction:column;align-items:center;justify-content:center;transform:rotate(10deg);font-family:Fredoka;box-shadow:0 18px 30px -12px rgba(224,122,95,.7)">
   <div style="font-size:24px;letter-spacing:2px;font-weight:500">2 FOR</div><div style="font-size:58px;font-weight:600;line-height:1">$89.99</div>
   <div style="font-size:20px;opacity:.9;font-weight:500">mix &amp; match</div></div>
 </div>
</div>
{dino(left=-10, bottom=-20, w=250, bubble="Let's open it!", bpos="tl", bstyle="left:120px;top:-70px")}''')))

    tiles = "".join(f'<div style="width:150px;height:108px;border-radius:10px;overflow:hidden;transform:rotate({r}deg) translateY({ty}px);'
                    f'box-shadow:0 8px 0 #CDBBA6,0 20px 26px -12px rgba(80,60,40,.45)">{mat_svg("rb", 268, 192, grid=False)}</div>'
                    for r, ty in [(-3,0),(2,8),(-1,-4),(4,6),(2,-6),(-4,4),(1,0),(-2,8),(-1,6),(3,-4),(-3,2),(2,0),(4,-2),(-2,6),(1,-6),(-4,0)])
    s.append(("16-tiles", page(2, T, tag, f'''
<div class="kicker">Inside the box</div>
<h1><em>16</em> interlocking<br>foam tiles</h1>
<div class="sub">Soft EVA pieces that snap together in minutes. <b>No tools needed.</b></div>
<div style="display:grid;grid-template-columns:repeat(4,150px);gap:22px 26px;margin:44px 0 0 10px">{tiles}</div>
<div style="margin-top:44px">{pills([("puzzle","sage","Interlocking edges"),("timer","mustard","Quick setup"),("layers","sky","Soft EVA")], center=False)}</div>
{dino(right=-20, bottom=130, w=220, bubble="Like a puzzle!", bpos="tr", bstyle="right:60px;top:-74px")}''')))

    s.append(("assembled-size", page(3, T, tag, f'''
<div class="center" style="display:flex;flex-direction:column;align-items:center">
 <div class="kicker">All snapped together</div>
 <h1 class="md">A big <em>5.6 × 4 ft</em><br>play space</h1>
 <div class="sub">Room for tummy time, toys and you.</div>
 <div style="margin-top:46px">{dims(700, 502, mat_flat("rb", 700))}</div>
</div>
{dino(right=-20, bottom=10, w=240, bubble="Room to roll!", bpos="tr", bstyle="right:70px;top:-74px")}''')))

    s.append(("box-features", page(4, T, tag, f'''
<div class="kicker">The box</div>
<h1 class="md">Everything's on<br>the <em>label</em></h1>
<div style="position:relative;width:936px;height:760px;margin-top:40px">
 <div style="position:absolute;left:250px;top:0">{photo(BOX_RB, 436, 560)}</div>
 <div class="callout" style="left:0;top:220px"><span class="n">1</span>Premium EVA foam</div>
 <div class="callout" style="right:0;top:340px"><span class="n">2</span>16 tiles · 5.6 × 4 ft</div>
 <div class="callout" style="left:0;top:440px"><span class="n">3</span>0.5 in / 1.2 cm thick</div>
 <div class="callout" style="right:0;top:520px"><span class="n">4</span>Design name on every box</div>
 <div style="position:absolute;left:0;right:0;top:620px">{pills([("shield","sage","CPSIA tested"),("check","coral","CPC certified"),("drop","sky","Waterproof")])}</div>
</div>''')))

    def design_card(src, name, ic, col, desc):
        return (f'<div style="display:flex;flex-direction:column;align-items:center;gap:22px">{photo(src, 400, 520)}'
                f'<div class="pill p-{col}" style="font-size:36px;font-weight:600">{icon(ic)}{name}</div>'
                f'<div style="font-size:27px;font-weight:700;color:var(--muted)">{desc}</div></div>')
    s.append(("two-designs", page(5, T, tag, f'''
<div class="center" style="display:flex;flex-direction:column;align-items:center">
 <div class="kicker">Pick your box</div>
 <h1 class="md">Two designs,<br><em>one</em> great mat</h1>
 <div style="display:flex;gap:48px;margin-top:50px">
  {design_card(BOX_RB, "RainBoho", "rainbow", "coral", "Boho rainbows")}
  {design_card(BOX_AS, "Ash Starlight", "moon", "sky", "Stars &amp; moons")}
 </div>
</div>''')))

    s.append(("shop", page(6, T, tag, f'''
<div class="center" style="display:flex;flex-direction:column;align-items:center">
 <h1>Unbox <em>yours</em></h1>
 <div class="sub">A soft, cozy play corner, all in one box.</div>
 {mat3d("rb", 640, mt=10)}
 <div style="margin-top:34px">{price_block()}</div>
 {cta_block()}
</div>
{dino(right=-30, top=300, w=180, bubble="See you there!", bpos="tr", bstyle="right:40px;top:-66px")}''')))
    return s

# ---------------- B: Specs & size guide
def B():
    T, tag = 5, "Size guide"
    s = []
    s.append(("cover", page(1, T, tag, f'''
<div class="kicker">Specs &amp; size guide</div>
<h1>Will it <em>fit?</em><br>Let's measure.</h1>
<div class="sub" style="max-width:640px">Size, thickness and what fits on the <b>Moon Walkers Premium EVA Playmat</b>.</div>
{mat3d("rb", 780, mt=60)}
{dino(right=-10, top=150, w=230, bubble="I measured!", bpos="tr", bstyle="right:60px;top:-70px")}''')))

    s.append(("dimensions", page(2, T, tag, f'''
<div class="center" style="display:flex;flex-direction:column;align-items:center">
 <div class="kicker">Assembled size</div>
 <h1 class="md"><em>5.6 × 4 ft</em><br>of play space</h1>
 <div style="margin-top:40px">{dims(720, 516, mat_flat("as", 720))}</div>
 <div style="margin-top:46px">{pills([("ruler","sage","67 × 48 in"),("expand","sky","170 × 122 cm"),("puzzle","mustard","16 tiles")])}</div>
</div>''')))

    slab = f'''<div style="position:relative;width:860px;height:220px;margin:30px auto 0">
 <div style="position:absolute;left:150px;top:0;width:680px;height:120px;transform:skewX(-40deg);transform-origin:bottom left;border-radius:8px 8px 0 0;overflow:hidden">{mat_svg("rb", 680, 120, grid=False)}</div>
 <div style="position:absolute;left:150px;top:120px;width:680px;height:72px;background:linear-gradient(#DCC9B3,#C8B198);border-radius:0 0 12px 12px;
  box-shadow:0 34px 40px -20px rgba(80,60,40,.5)"></div>
 <div class="dim v" style="left:110px;top:120px;height:72px"><div class="t" style="position:absolute;right:26px;text-align:right">0.5 in<small>1.2 cm</small></div></div>
</div>'''
    s.append(("thickness", page(3, T, tag, f'''
<div class="kicker">Thickness</div>
<h1 class="md"><em>0.5 in</em> of soft<br>EVA cushion</h1>
{slab}
<div class="note-sm" style="text-align:center;margin-top:-6px">Illustration, edge enlarged to show thickness</div>
<div class="grid2 tight" style="margin-top:24px">
 {tile("heart","pink","Soft cushioned landing","For wobbly sitters &amp; new walkers")}
 {tile("baby","mustard","Comfy for knees","Crawling and kneeling feel softer")}
 {tile("volume","sky","Quieter play","Softens the thud of toys &amp; feet")}
 {tile("home","sage","Cozy floor zone","A soft layer over hard floors")}
</div>''')))

    PX = 3.6  # px per inch for mini diagrams
    def fit(title, size, note, w_in, h_in, ic, col, label):
        mw, mh = round(67*PX), round(48*PX)
        ow, oh = round(w_in*PX), round(h_in*PX)
        return f'''<div class="card" style="display:flex;align-items:center;gap:36px;padding:26px 34px">
 <div style="position:relative;width:{mw}px;height:{mh}px;border-radius:8px;overflow:hidden;flex:none;box-shadow:0 6px 0 #8E8882">{mat_svg("as", mw, mh, grid=False)}
  <div style="position:absolute;left:{(mw-ow)//2}px;top:{(mh-oh)//2}px;width:{ow}px;height:{oh}px;border:3px dashed #fff;background:rgba(255,255,255,.55);border-radius:6px;
   display:grid;place-items:center;color:var(--ink);font-family:Fredoka;font-weight:600;font-size:20px">{label}</div></div>
 <div><div class="pill p-{col}" style="font-size:24px;padding:8px 18px">{icon(ic)}{size}</div>
  <h3 style="font-family:Fredoka;font-weight:600;font-size:40px;margin-top:12px;line-height:1.05">{title}</h3>
  <p style="font-size:25px;color:var(--muted);font-weight:700;margin-top:6px">{note}</p></div></div>'''
    s.append(("what-fits", page(4, T, tag, f'''
<div class="kicker">What fits on it?</div>
<h1 class="sm">Drawn to scale on<br>the <em>67 × 48 in</em> mat</h1>
<div style="display:flex;flex-direction:column;gap:18px;margin-top:32px">
 {fit("Standard crib", "52 × 28 in", "Fits, with room to spare", 52, 28, "crib", "sage", "crib")}
 {fit("Play yard", "40 × 28 in", "Fits, with space for toys", 40, 28, "check", "sky", "play yard")}
 {fit("Toddler, stretched out", "~3 ft tall", "Plenty of room to roll", 36, 14, "baby", "mustard", "toddler")}
</div>
<div class="note-sm" style="margin-top:20px">Typical US sizes. Check your own crib or play yard before buying.</div>''')))

    rows = [("layers","Material","Soft EVA foam"),("puzzle","Tiles","16 interlocking"),("ruler","Size","5.6 × 4 ft (67 × 48 in)"),
            ("expand","Metric","170 × 122 cm"),("layers","Thickness","0.5 in (1.2 cm)"),("drop","Surface","Waterproof, wipe clean"),
            ("feet","Grip","Non-slip"),("shield","Testing","CPC / CPSIA tested"),("star","Designs","RainBoho · Ash Starlight")]
    tr = "".join(f'<tr><td>{icon(i)}{k}</td><td>{v}</td></tr>' for i, k, v in rows)
    s.append(("spec-sheet", page(5, T, tag, f'''
<div class="kicker">Save this</div>
<h1 class="sm">The <em>spec</em> sheet</h1>
<div class="card spec-tight" style="margin-top:26px;padding:6px 6px"><table class="spec">{tr}</table></div>
<div style="display:flex;align-items:center;justify-content:space-between;margin-top:26px">
 <div><div style="font-family:Fredoka;font-weight:600;font-size:66px;color:var(--coral);line-height:1">$49.99 <span style="font-size:32px;color:var(--muted)">each</span></div>
 <div style="font-size:30px;font-weight:800;color:var(--ink);margin-top:8px">2 for $89.99 · mix &amp; match</div></div>
 <div class="cta" style="font-size:32px;padding:22px 36px">{icon("bag",2.4)}DM to order</div>
</div>''')))
    return s

# ---------------- C: Why parents love it
def C():
    T, tag = 6, "Why parents love it"
    s = []
    s.append(("cover", page(1, T, tag, f'''
<div class="kicker">5 reasons</div>
<h1>Soft. Cozy.<br><em>Seriously</em> cute.</h1>
<div class="sub">Why the <b>Moon Walkers playmat</b> belongs in your home.</div>
{mat3d("as", 760, mt=70)}
{dino(left=-14, bottom=-30, w=250, bubble="Made with love!", bpos="tl", bstyle="left:140px;top:-74px")}''')))

    s.append(("safety", page(2, T, tag, f'''
<div class="kicker">01 · Tested</div>
<h1 class="md">Tested for<br><em>little ones</em></h1>
<div class="sub">CPSIA tested and backed by a <b>Children's Product Certificate (CPC)</b>.</div>
<div style="display:flex;gap:30px;justify-content:center;margin-top:56px">
 <div class="badge-cert">{icon("shield").replace("<svg",'<svg style="width:54px;height:54px;margin-bottom:6px"')}<b>CPSIA</b><span>Tested</span></div>
 <div class="badge-cert" style="border-color:var(--coral);color:#C65E43">{icon("check",2.6).replace("<svg",'<svg style="width:54px;height:54px;margin-bottom:6px"')}<b>CPC</b><span>Certified</span></div>
 <div class="badge-cert" style="border-color:var(--sky);color:#4D7A98">{icon("leaf").replace("<svg",'<svg style="width:54px;height:54px;margin-bottom:6px"')}<b>Non-toxic</b><span>EVA foam</span></div>
</div>
<div class="feats" style="margin-top:56px;max-width:720px">
 {feat("baby","mustard","Tummy time to first steps","A soft, clean surface for every stage")}
</div>
{dino(right=-20, bottom=40, w=200)}''')))

    drops = "".join(f'<svg style="position:absolute;left:{x}px;top:{y}px;width:{w}px" viewBox="0 0 24 30"><path fill="rgba(122,163,189,.92)" d="M12 1c4 5.5 9 10.5 9 16a9 9 0 0 1-18 0c0-5.5 5-10.5 9-16z"/><ellipse cx="8.5" cy="17" rx="2" ry="3.4" fill="rgba(255,255,255,.7)"/></svg>'
                    for x, y, w in [(150, 90, 54), (250, 170, 36), (420, 110, 44), (560, 200, 30)])
    s.append(("wipe-clean", page(3, T, tag, f'''
<div class="kicker">02 · Waterproof</div>
<h1>Spills? <em class="s">Wipe.</em><br>Done.</h1>
<div class="sub">Juice, milk or messy snacks wipe right off with a damp cloth.</div>
<div style="position:relative;width:640px;margin:40px auto 0">{mat_flat("rb", 640)}{drops}
 <div class="card" style="position:absolute;right:-50px;bottom:-40px;padding:24px 30px;display:flex;align-items:center;gap:18px">
  <div class="ico i-sky">{icon("sponge")}</div><div style="font-family:Fredoka;font-weight:600;font-size:32px;line-height:1.1">Damp cloth.<br><span style="color:var(--sky)">That's it.</span></div></div>
</div>
<div style="margin-top:70px">{pills([("drop","sky","Waterproof"),("sponge","sage","Easy to clean"),("check","mustard","Back to play")])}</div>''')))

    s.append(("non-slip", page(4, T, tag, f'''
<div class="kicker">03 · Non-slip</div>
<h1 class="md">Stays put while<br>they <em>play</em></h1>
<div class="sub">Non-slip surface + locking tiles = one steady play area.</div>
{mat3d("as", 600, rx=58, rz=10, mt=0)}
<div class="feats" style="margin-top:20px">
 {feat("feet","coral","Non-slip surface","Helps the mat stay in place during play")}
 {feat("puzzle","sage","Tiles lock together","One solid space, no gaps to trip on")}
</div>''')))

    s.append(("soft-easy", page(5, T, tag, f'''
<div class="kicker">04 · Comfort &amp; setup</div>
<h1 class="md">Soft &amp; cushioned,<br><em>easy</em> setup</h1>
<div class="grid2" style="margin-top:50px">
 {tile("layers","sage","0.5 in cushion","Thick, soft EVA for crawling &amp; play")}
 {tile("timer","mustard","Sets up in minutes","16 tiles click together, no tools")}
 {tile("puzzle","sky","Rearrange anytime","Fit a corner, a nursery or a playroom")}
 {tile("volume","pink","Quieter play","Softens the thud of toys &amp; feet")}
</div>
{dino(right=0, top=40, w=200, bubble="So comfy!", bpos="tr", bstyle="right:50px;top:-66px")}''')))

    s.append(("style-shop", page(6, T, tag, f'''
<div class="center" style="display:flex;flex-direction:column;align-items:center">
 <div class="kicker">05 · Looks good too</div>
 <h1 class="md">Made for your<br><em>living room</em></h1>
 <div style="display:flex;gap:34px;margin-top:40px">
  <div style="transform:rotate(-3deg)">{mat_flat("rb", 410)}</div><div style="transform:rotate(3deg)">{mat_flat("as", 410)}</div></div>
 <div style="margin-top:48px">{price_block()}</div>
 {cta_block()}
</div>''')))
    return s

# ---------------- D: RainBoho vs Ash Starlight
def D():
    T, tag = 5, "Pick your vibe"
    s = []
    s.append(("cover", page(1, T, tag, f'''
<div class="center" style="display:flex;flex-direction:column;align-items:center">
 <div class="kicker">Which one is you?</div>
 <h1><em class="c">RainBoho</em><br><span style="font-size:60px;color:var(--muted)">vs</span><br><em>Ash Starlight</em></h1>
 <div style="display:flex;gap:30px;margin-top:50px;align-items:flex-start">
  <div style="display:flex;flex-direction:column;align-items:center;gap:24px;transform:rotate(-3deg)">{mat_flat("rb", 420)}<div class="pill p-coral">{icon("rainbow")}Boho rainbows</div></div>
  <div style="display:flex;flex-direction:column;align-items:center;gap:24px;transform:rotate(3deg)">{mat_flat("as", 420)}<div class="pill p-sky">{icon("moon")}Stars &amp; moons</div></div>
 </div>
</div>
{dino(right=10, top=170, w=180, bubble="Swipe to compare", bpos="tr", bstyle="right:40px;top:-66px")}''')))

    def design(n, name_html, sub, d, box, pl, sw):
        swatches = "".join(f'<i style="width:54px;height:54px;border-radius:50%;background:{c};display:block;border:4px solid #fff;box-shadow:0 6px 12px -6px rgba(0,0,0,.3)"></i>' for c in sw)
        return page(n, T, tag, f'''
<div class="kicker">Design 0{n-1}</div>
<h1>{name_html}</h1>
<div class="sub">{sub}</div>
<div style="position:relative;margin-top:20px">{mat3d(d, 680, mt=10)}
 <div style="position:absolute;right:-20px;top:30px">{photo(box, 220, 286, 6)}</div></div>
<div style="display:flex;gap:12px;margin-top:36px;align-items:center"><span style="font-family:Fredoka;font-weight:500;font-size:26px;letter-spacing:2px;color:var(--muted);margin-right:10px">PALETTE</span>{swatches}</div>
<div style="margin-top:30px">{pills(pl, center=False)}</div>''')
    s.append(("rainboho", design(2, 'Rain<em class="c">Boho</em>', "Boho rainbows, clouds &amp; hearts in <b>warm sand tones</b>.", "rb", BOX_RB,
                                  [("sun","mustard","Warm &amp; cheerful"),("home","coral","Wood &amp; beige rooms")],
                                  ["#E8D9C6","#C3A386","#D2AE98","#F7F0E7"])))
    s.append(("ash-starlight", design(3, 'Ash <em class="s">Starlight</em>', "Stars &amp; crescent moons on <b>soft ash grey</b>.", "as", BOX_AS,
                                       [("moon","sky","Calm &amp; dreamy"),("home","sage","Grey &amp; white rooms")],
                                       ["#ADA7A0","#8E8882","#E6E1DA","#F4F1EC"])))

    rows = [("Vibe","Warm &amp; cheerful","Calm &amp; dreamy"),("Motifs","Rainbows, clouds, hearts","Stars, moons"),
            ("Tones","Sand, cream, blush","Ash grey, white"),("Best with","Wood &amp; beige decor","Grey &amp; white decor"),
            ("Size","5.6 × 4 ft","5.6 × 4 ft"),("Thickness","0.5 in","0.5 in"),("Testing","CPC / CPSIA","CPC / CPSIA")]
    tr = "".join(f'<div style="display:contents"><div style="padding:13px 0;color:var(--muted);font-weight:800;font-size:25px;border-top:2px dashed var(--line)">{a}</div>'
                 f'<div style="padding:13px 0;font-family:Fredoka;font-weight:500;font-size:29px;border-top:2px dashed var(--line)">{b}</div>'
                 f'<div style="padding:13px 0;font-family:Fredoka;font-weight:500;font-size:29px;border-top:2px dashed var(--line)">{c}</div></div>' for a, b, c in rows)
    s.append(("compare", page(4, T, tag, f'''
<div class="kicker">Side by side</div>
<h1 class="sm">Same mat.<br><em>Different</em> vibe.</h1>
<div class="card" style="margin-top:28px;padding:28px 36px;display:grid;grid-template-columns:200px 1fr 1fr;column-gap:24px">
 <div></div>
 <div style="padding-bottom:20px"><div style="width:100%;height:90px;border-radius:14px;overflow:hidden">{mat_svg("rb", 330, 90, grid=False)}</div>
  <div style="font-family:Fredoka;font-weight:600;font-size:36px;color:var(--coral);margin-top:14px">RainBoho</div></div>
 <div style="padding-bottom:20px"><div style="width:100%;height:90px;border-radius:14px;overflow:hidden">{mat_svg("as", 330, 90, grid=False)}</div>
  <div style="font-family:Fredoka;font-weight:600;font-size:36px;color:var(--sky);margin-top:14px">Ash Starlight</div></div>
 {tr}
</div>
<div class="sub" style="text-align:center;margin:20px auto 0;font-size:30px">Can't pick? <b>You don't have to.</b></div>''')))

    s.append(("bundle", page(5, T, tag, f'''
<div class="center" style="display:flex;flex-direction:column;align-items:center">
 <h1>Can't decide?<br>Get <em class="m">both.</em></h1>
 <div class="sub">One for the nursery, one for the living room (or Grandma's).</div>
 <div style="position:relative;width:900px;height:440px;margin-top:40px">
  <div style="position:absolute;left:20px;top:40px;transform:rotate(-6deg)">{mat_flat("rb", 460)}</div>
  <div style="position:absolute;right:20px;top:90px;transform:rotate(5deg)">{mat_flat("as", 460)}</div>
  <div style="position:absolute;left:50%;top:150px;transform:translateX(-50%) rotate(-4deg);width:300px;height:300px;border-radius:50%;background:var(--mustard);color:#fff;
   display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:Fredoka;box-shadow:0 26px 40px -16px rgba(169,118,27,.75);border:8px solid #fff">
   <div style="font-size:30px;font-weight:500;letter-spacing:2px">2 FOR</div><div style="font-size:84px;font-weight:600;line-height:.95">$89.99</div>
   <div style="font-size:23px;font-weight:500">mix &amp; match</div></div>
 </div>
 <div style="font-size:28px;font-weight:700;color:var(--muted);margin-top:30px">Single mat <b style="color:var(--coral)">$49.99</b> · the 2-pack saves $9.99</div>
 {cta_block("DM to get the bundle")}
</div>
{dino(right=-40, bottom=210, w=190, bubble="Best deal!", bpos="tr", bstyle="right:40px;top:-66px")}''')))
    return s

if __name__ == "__main__":
    os.makedirs(BUILD, exist_ok=True)
    for f in os.listdir(BUILD):
        os.remove(os.path.join(BUILD, f))
    manifest = []
    import more
    for key, fn in [("A", A), ("B", B), ("C", C), ("D", D)] + more.ALL:
        for i, (slug, inner) in enumerate(fn(), 1):
            # 4:5 is rendered from HTML; the 1080x1920 version is composited by story.py so every
            # word sits inside the IG Reels / TikTok safe box (x 40-900, y 320-1400)
            for ratio, size in [("r45", "1080x1350")]:
                name = f"{key}{i:02d}-{slug}"
                path = os.path.join(BUILD, f"{name}.{ratio}.html")
                open(path, "w").write(doc(inner, ratio))
                manifest.append({"html": path, "out": f"{key}/{name}_{size}.png", "h": 1350 if ratio == "r45" else 1920})
    json.dump(manifest, open(os.path.join(BUILD, "manifest.json"), "w"), indent=1)
    print(len(manifest), "pages")
