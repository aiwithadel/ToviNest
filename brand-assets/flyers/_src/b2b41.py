"""Five audience flyers for the 41-contact B2B outreach (1500x975, same ratio as the old 600x390 email flyers).
python3 b2b41.py && node render.js && python3 post.py
Assets: official Dino/Dima PNGs, real RainBoho / Ash Starlight flat-lays (cropped to the mat), vector props.
No people (no photo of the real mat in use exists yet), no prices, no invented stats.
"""
import os, json
from flyers import CSS, BUILD

W, H = 1500, 975
FOOT = "Moon Walkers Premium EVA Playmat · CPC/CPSIA tested · tovinest.com/catalog"

EXTRA = """
.f{width:1500px;height:975px}
.tagp{display:inline-block;font-weight:900;font-size:19px;letter-spacing:.14em;text-transform:uppercase;border-radius:999px;padding:10px 20px}
.ttl{font-family:Fredoka,sans-serif;font-weight:600;letter-spacing:-.02em;line-height:1.0;color:#3B2A1C}
.sub{font-size:27px;line-height:1.4;font-weight:700;color:#5E4D3E}
.chip{background:#fff;border-radius:999px;padding:10px 18px;font-weight:800;font-size:20px;color:#3B2A1C;box-shadow:0 10px 24px -16px rgba(59,42,28,.5)}
.floor{position:absolute;transform-origin:50% 100%;border-radius:30px;overflow:hidden;
 box-shadow:0 14px 0 #E6DACB,0 60px 80px -30px rgba(59,42,28,.55)}
.floor img{width:100%;height:100%;object-fit:cover;display:block}
.ch{position:absolute;filter:drop-shadow(0 24px 18px rgba(59,42,28,.3))}
.sh{position:absolute;border-radius:50%;background:radial-gradient(closest-side,rgba(59,42,28,.32),transparent)}
.prop{position:absolute;filter:drop-shadow(0 18px 16px rgba(59,42,28,.28))}
.foot{position:absolute;left:0;right:0;bottom:0;height:92px;background:#4E6444;color:#FBF4EA;display:flex;align-items:center;justify-content:center;
 font-weight:800;font-size:27px;letter-spacing:.01em}
.foot b{color:#F3C66B;font-weight:900}
"""

# ---------- vector props ----------
def gift(w, body="#E9A6A1", lid=None, rib="#4E6444", rot=0):
    lid = lid or body
    h = w * 0.86
    return f'''<svg viewBox="0 0 100 86" width="{w}" height="{h:.0f}" style="transform:rotate({rot}deg)">
<path d="M50 20c-6-12-22-16-24-7-2 8 14 9 24 7zM50 20c6-12 22-16 24-7 2 8-14 9-24 7z" fill="none" stroke="{rib}" stroke-width="5" stroke-linejoin="round"/>
<rect x="10" y="34" width="80" height="50" rx="5" fill="{body}"/>
<rect x="10" y="34" width="80" height="8" fill="#000" opacity=".07"/>
<rect x="5" y="20" width="90" height="17" rx="4" fill="{lid}"/>
<rect x="5" y="20" width="90" height="17" rx="4" fill="#fff" opacity=".18"/>
<rect x="44" y="20" width="12" height="64" fill="{rib}"/></svg>'''

def heart(s, c="#E9A6A1"):
    return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M12 21s-8-5-8-11a4.5 4.5 0 0 1 8-2.8A4.5 4.5 0 0 1 20 10c0 6-8 11-8 11z" fill="{c}"/></svg>'

def star(s, c="#E9B041"):
    return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M12 1.5l2.3 7.7 8.2.3-6.6 4.8 2.4 7.9L12 17.4l-6.3 4.8 2.4-7.9L1.5 9.5l8.2-.3z" fill="{c}"/></svg>'

def sparkle(s, c="#E9B041"):
    return f'<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M12 0c1 7 5 11 12 12-7 1-11 5-12 12-1-7-5-11-12-12 7-1 11-5 12-12z" fill="{c}"/></svg>'

def note(s, c="#4E6444", double=False):
    if double:
        return (f'<svg viewBox="0 0 40 40" width="{s}" height="{s}"><path d="M14 30V8l22-5v22" fill="none" stroke="{c}" stroke-width="3.6" stroke-linecap="round"/>'
                f'<path d="M14 8l22-5v6L14 14z" fill="{c}"/><ellipse cx="9.5" cy="30.5" rx="6" ry="4.8" fill="{c}" transform="rotate(-20 9.5 30.5)"/>'
                f'<ellipse cx="31.5" cy="25.5" rx="6" ry="4.8" fill="{c}" transform="rotate(-20 31.5 25.5)"/></svg>')
    return (f'<svg viewBox="0 0 30 40" width="{s*.75:.0f}" height="{s}"><path d="M14 31V4c4 3 11 5 11 13" fill="none" stroke="{c}" stroke-width="3.6" stroke-linecap="round"/>'
            f'<ellipse cx="9" cy="31.5" rx="6.5" ry="5" fill="{c}" transform="rotate(-20 9 31.5)"/></svg>')

def toothbrush(w, rot=-32):
    return f'''<svg viewBox="0 0 300 60" width="{w}" height="{w*.2:.0f}" style="transform:rotate({rot}deg)">
<rect x="0" y="22" width="215" height="22" rx="11" fill="#E9B041"/><rect x="18" y="26" width="120" height="6" rx="3" fill="#fff" opacity=".45"/>
<rect x="205" y="26" width="90" height="16" rx="8" fill="#7AA3BD"/>
<g fill="#fff" stroke="#BFD3E0" stroke-width="2">{"".join(f'<rect x="{212+i*13}" y="2" width="10" height="26" rx="4"/>' for i in range(6))}</g>
<path d="M210 6c20-10 60-10 82 0" fill="none" stroke="#9FD0E8" stroke-width="5" stroke-linecap="round" opacity=".7"/></svg>'''

def tooth(s):
    return f'''<svg viewBox="0 0 24 24" width="{s}" height="{s}"><path d="M7 3c-2.6 0-4 2-4 4.6 0 2.4 1.2 3.6 1.7 6 .5 2.6.9 6.4 2.6 6.4 1.6 0 1.6-4.6 3-4.6h3.4c1.4 0 1.4 4.6 3 4.6 1.7 0 2.1-3.8 2.6-6.4.5-2.4 1.7-3.6 1.7-6C21 5 19.6 3 17 3c-2 0-3 1.2-5 1.2S9 3 7 3z" fill="#fff" stroke="#7AA3BD" stroke-width="1.4"/>
<path d="M8.5 7.5c1-1 2.5-1 3.3-.4" fill="none" stroke="#9FD0E8" stroke-width="1.4" stroke-linecap="round"/></svg>'''

def drum(w, body="#E9A6A1", rim="#F3C66B"):
    return f'''<svg viewBox="0 0 100 90" width="{w}" height="{w*.9:.0f}">
<path d="M8 22v44c0 10 19 18 42 18s42-8 42-18V22" fill="{body}"/>
<path d="M8 66c0 10 19 18 42 18s42-8 42-18v-6c0 10-19 18-42 18S8 70 8 60z" fill="{rim}"/>
<path d="M12 30l13 46 13-48 12 50 12-50 13 48 13-46" fill="none" stroke="#fff" stroke-width="3" stroke-linejoin="round" opacity=".9"/>
<ellipse cx="50" cy="22" rx="42" ry="14" fill="#FBF4EA" stroke="{rim}" stroke-width="6"/></svg>'''

def tambourine(w, rot=-18):
    jingles = "".join(f'<g transform="rotate({a} 50 50)"><rect x="44" y="4" width="12" height="9" rx="2" fill="#4E6444"/><circle cx="50" cy="8.5" r="5" fill="#F3C66B" stroke="#C89530" stroke-width="1.5"/></g>' for a in range(0, 360, 45))
    return f'''<svg viewBox="0 0 100 100" width="{w}" height="{w}" style="transform:rotate({rot}deg)">
<circle cx="50" cy="50" r="42" fill="#FBF4EA"/><circle cx="50" cy="50" r="42" fill="none" stroke="#4E6444" stroke-width="10"/>
<circle cx="50" cy="50" r="30" fill="none" stroke="#E9A6A1" stroke-width="2" stroke-dasharray="3 5"/>{jingles}</svg>'''

def block(s, c, letter):
    return f'''<div class="prop" style="width:{s}px;height:{s}px;border-radius:{s*.18:.0f}px;background:{c};display:grid;place-items:center;
 font-family:Fredoka,sans-serif;font-weight:600;font-size:{s*.6:.0f}px;color:#fff;box-shadow:inset 0 -{s*.12:.0f}px 0 rgba(0,0,0,.12)">{letter}</div>'''

def arc(x, y, w, rot, c="#E9B041"):
    return (f'<svg style="position:absolute;left:{x}px;top:{y}px;transform:rotate({rot}deg)" width="{w}" height="{w*.5:.0f}" viewBox="0 0 100 50">'
            f'<path d="M5 45C20 5 80 5 95 45" fill="none" stroke="{c}" stroke-width="4" stroke-linecap="round" stroke-dasharray="2 10"/></svg>')

def at(x, y, inner, z=1, extra=""):
    return f'<div style="position:absolute;left:{x}px;top:{y}px;z-index:{z};{extra}">{inner}</div>'

def floor(mat, left=700, top=300, w=780, h=540, rx=54):
    return (f'<div class="floor" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px;transform:perspective(1300px) rotateX({rx}deg)">'
            f'<img src="../img/{mat}"></div>')

def char(name, x, y, w, rot=0, z=3, shadow=True, sy=None):
    h = w * (1100 / (798 if name == "dino" else 697))
    sh = ""
    if shadow:
        sy = sy if sy is not None else y + h - 22
        sh = f'<div class="sh" style="left:{x + w*.12:.0f}px;top:{sy:.0f}px;width:{w*.76:.0f}px;height:{w*.16:.0f}px;z-index:{z-1}"></div>'
    return sh + f'<img class="ch" src="../img/{name}.png" style="left:{x}px;top:{y}px;width:{w}px;transform:rotate({rot}deg);z-index:{z}">'

# ---------- scenes ----------
def scene_hospital():
    tag = ('<div style="position:absolute;left:1188px;top:452px;z-index:6;transform:rotate(6deg)">'
           '<svg width="80" height="70" style="position:absolute;left:-58px;top:-44px"><path d="M4 4C30 10 50 30 72 58" fill="none" stroke="#4E6444" stroke-width="3"/></svg>'
           '<div style="background:#fff;border-radius:16px;padding:14px 22px 14px 30px;box-shadow:0 18px 30px -18px rgba(59,42,28,.6);position:relative;'
           'font-family:Fredoka,sans-serif;font-weight:600;font-size:30px;color:#3B2A1C;line-height:1.05;white-space:nowrap">'
           '<span style="position:absolute;left:10px;top:50%;width:10px;height:10px;margin-top:-5px;border-radius:50%;background:#E9A6A1"></span>'
           'Welcome,<br><span style="color:#C2573B">little one</span> ♡</div></div>')
    return (floor("mat-rainboho.jpg")
            + char("dima", 760, 330, 300)
            + at(1070, 470, gift(280, "#E9A6A1", "#F2B9B4", "#4E6444"), 4) + tag
            + at(1110, 150, heart(54), 2) + at(1220, 220, heart(34, "#F2B9B4"), 2) + at(1010, 210, sparkle(34), 2)
            + at(1380, 330, sparkle(26, "#7AA3BD"), 2))

def scene_foundation():
    return (floor("mat-ash.jpg")
            + at(1150, 560, gift(230, "#E9B041", "#F3C66B", "#4E6444"), 4)
            + at(1290, 470, gift(170, "#7AA3BD", "#9CBDD1", "#FBF4EA", rot=8), 3)
            + at(1210, 400, gift(150, "#E9A6A1", "#F2B9B4", "#4E6444", rot=-6), 2)
            + at(1360, 640, gift(110, "#4E6444", "#62794F", "#F3C66B", rot=4), 5)
            + char("dino", 760, 300, 330)
            + at(840, 560, gift(170, "#E9A6A1", "#F2B9B4", "#4E6444", rot=-8), 6)
            + at(1100, 170, star(46), 2) + at(1250, 250, sparkle(36, "#E9A6A1"), 2) + at(1390, 190, star(30, "#7AA3BD"), 2)
            + at(1000, 230, heart(30), 2))

def scene_dentist():
    badge = ('<div style="position:absolute;left:1180px;top:170px;z-index:6;transform:rotate(8deg);width:200px;height:200px;border-radius:50%;'
             'background:#fff;box-shadow:0 22px 40px -20px rgba(59,42,28,.6);display:grid;place-items:center;text-align:center;border:6px dashed #E9B041">'
             f'<div>{tooth(70)}<div style="font-family:Fredoka,sans-serif;font-weight:600;font-size:30px;color:#3B2A1C;line-height:1;margin-top:4px">Brave<br>smile!</div></div></div>')
    return (floor("mat-ash.jpg")
            + char("dino", 800, 300, 340)
            + at(690, 590, toothbrush(400, -24), 5)
            + at(1170, 560, gift(190, "#E9B041", "#F3C66B", "#4E6444", rot=6), 4)
            + badge + at(1120, 420, sparkle(40, "#7AA3BD"), 6) + at(1400, 430, sparkle(28), 6) + at(770, 230, sparkle(34, "#7AA3BD"), 2))

def scene_gym():
    return (floor("mat-rainboho.jpg")
            + char("dino", 770, 170, 290, rot=-12, sy=680) + char("dima", 1130, 120, 250, rot=14, sy=700)
            + arc(760, 120, 260, -10) + arc(1110, 70, 240, 12, "#E9A6A1")
            + at(990, 650, block(90, "#E9B041", "A"), 4) + at(1080, 690, block(76, "#7AA3BD", "B"), 4) + at(1370, 640, block(84, "#E9A6A1", "C"), 4)
            + at(1050, 330, star(40), 2) + at(1400, 330, sparkle(32, "#7AA3BD"), 2) + at(720, 400, sparkle(28), 2))

def scene_music():
    return (floor("mat-ash.jpg")
            + char("dima", 820, 300, 290)
            + at(990, 470, tambourine(170, -20), 5)
            + at(1170, 560, drum(170, "#E9A6A1", "#F3C66B"), 4) + at(1330, 520, drum(130, "#7AA3BD", "#FBF4EA"), 4)
            + at(730, 620, drum(120, "#E9B041", "#4E6444"), 4)
            + at(1110, 190, note(70, "#4E6444", True), 2) + at(1290, 300, note(60, "#C2573B"), 2) + at(760, 220, note(54, "#7AA3BD"), 2)
            + at(1380, 160, note(48, "#E9B041", True), 2) + at(1010, 120, sparkle(30), 2))

FLYERS = [
    ("hospitals", "Hospitals &amp; maternity units", "#F7DEDA", "#A9544B",
     "A Welcome Gift<br>for Every <em>New Family</em>", "Send every family home with a soft, beautiful playmat for baby’s first months.",
     scene_hospital),
    ("foundations", "Hospital foundations &amp; auxiliaries", "#F6E7C2", "#94681A",
     "Give Every Newborn<br>a Safe Place <em>to Play</em>", "Sponsor playmats for the families your hospital serves, one gift at a time.",
     scene_foundation),
    ("dentists", "Pediatric dentists", "#DDE9F1", "#3F6A85",
     "Brave Smiles<br>Deserve <em>a Reward</em>", "A gift kids remember long after the check-up, and a soft corner for your waiting room.",
     scene_dentist),
    ("kids-gyms", "Kids gyms &amp; play spaces", "#E3E9DA", "#4E6444",
     "Soft Landings<br>for Big <em>Adventures</em>", "Cushioned 0.5 in EVA floor for crawling, tumbling and play.",
     scene_gym),
    ("music-classes", "Kids music classes", "#F7DEDA", "#A9544B",
     "Where Little<br>Musicians <em>Gather</em>", "A soft, wipe-clean floor for circle time, songs and shakers.",
     scene_music),
]

def page(key, tag, tint, ink, title, sub, scene):
    fs = 70 if len(title) > 50 else 76
    blob = (f'<div style="position:absolute;left:640px;top:-120px;width:1000px;height:1000px;border-radius:50%;'
            f'background:radial-gradient(closest-side,{tint},rgba(251,244,234,0))"></div>')
    chips = "".join(f'<span class="chip">{t}</span>' for t in ["16 tiles · 67 × 48 in", "0.5 in soft EVA", "Wipe-clean"])
    return f'''<div class="f"><div class="paper"></div>{blob}
<img src="../img/logo.png" style="position:absolute;left:70px;top:44px;height:112px">
<div style="position:absolute;left:70px;top:200px;width:720px;z-index:8">
 <span class="tagp" style="background:{tint};color:{ink}">{tag}</span>
 <h1 class="ttl" style="font-size:{fs}px;margin-top:22px">{title}</h1>
 <p class="sub" style="margin-top:22px">{sub}</p>
 <div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:30px">{chips}</div>
</div>
<div style="position:absolute;inset:0;transform:scale(.93);transform-origin:100% 88%">{scene()}</div>
<div class="foot" style="z-index:9">Moon Walkers Premium EVA Playmat<span style="opacity:.5;margin:0 16px">·</span>CPC/CPSIA tested<span style="opacity:.5;margin:0 16px">·</span><b>tovinest.com/catalog</b></div>
</div>'''

if __name__ == "__main__":
    css = CSS + EXTRA
    jobs = [j for j in json.load(open(os.path.join(BUILD, "jobs.json"))) if "b2b-" not in j["name"]]
    for i, f in enumerate(FLYERS, 1):
        p = os.path.join(BUILD, f"b2b-{i}-{f[0]}.html")
        open(p, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{page(*f)}</body></html>')
        jobs.append({"html": p, "name": f"tovinest-b2b-{i}-{f[0]}", "w": W, "h": H})
    json.dump(jobs, open(os.path.join(BUILD, "jobs.json"), "w"), indent=1)
    print("ok")
