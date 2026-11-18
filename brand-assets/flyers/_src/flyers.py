"""Tovi Nest B2B email flyers (classrooms / pediatric waiting rooms).

python3 flyers.py  -> build/*.html ;  node render.js  -> ../*.png / *.jpg

Two layouts per audience:
  tall    1200x1600 CSS px (email body or attachment), rendered at 2x = 2400x3200
  banner  1200x780  CSS px (same ratio as the old 600x390 email flyers), rendered at 2x
Facts only from the brief: 16 tiles, 67 x 48 in (5.6 x 4 ft), 0.5 in EVA, wipe-clean, non-slip,
CPC/CPSIA tested, RainBoho / Ash Starlight, local to Sterling VA with a free visit & room measuring.
No prices, no injury/safety claims, no carton photos, no "AI-generated".
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build")

ICON = {
    "tiles": '<rect x="3.5" y="3.5" width="7.5" height="7.5" rx="1.5"/><rect x="13" y="3.5" width="7.5" height="7.5" rx="1.5"/><rect x="3.5" y="13" width="7.5" height="7.5" rx="1.5"/><rect x="13" y="13" width="7.5" height="7.5" rx="1.5"/>',
    "ruler": '<rect x="2.5" y="8" width="19" height="8" rx="1.6"/><path d="M6.2 8v3M9.4 8v4.2M12.6 8v3M15.8 8v4.2M19 8v3"/>',
    "layers": '<path d="M12 4l9 4.8-9 4.8-9-4.8z"/><path d="M3 13.6l9 4.8 9-4.8"/>',
    "drop": '<path d="M12 3.2c3 4 6 7.4 6 10.9a6 6 0 0 1-12 0c0-3.5 3-6.9 6-10.9z"/>',
    "shield": '<path d="M12 3l7 3v6c0 4.5-3 7.6-7 9-4-1.4-7-4.5-7-9V6z"/><path d="M8.6 12.2l2.4 2.4 4.4-4.8"/>',
    "grip": '<path d="M4 17h16"/><path d="M6 13l2 4M10 13l2 4M14 13l2 4"/><rect x="4" y="6" width="16" height="7" rx="2"/>',
    "pin": '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z"/><circle cx="12" cy="10" r="2.3"/>',
    "mail": '<rect x="3" y="5.5" width="18" height="13" rx="2.5"/><path d="M3.5 7l8.5 6 8.5-6"/>',
    "globe": '<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.6 2.6 2.6 14.4 0 17M12 3.5c-2.6 2.6-2.6 14.4 0 17"/>',
    "gift": '<rect x="3.5" y="8.5" width="17" height="4" rx="1"/><path d="M5 12.5v8h14v-8M12 8.5v12"/><path d="M12 8.5c-1.5-3.5-5.5-3.5-5-1s5 1 5 1zm0 0c1.5-3.5 5.5-3.5 5-1s-5 1-5 1z"/>',
    "ruler2": '<path d="M4 20L20 4"/><path d="M7 17l2 2M10 14l1.5 1.5M13 11l2 2M16 8l1.5 1.5"/>',
}

def icon(n, size=34, color="currentColor", sw=1.9):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[n]}</svg>')

SPECS = [("tiles", "16 interlocking tiles"), ("ruler", "67 × 48 in · 5.6 × 4 ft"), ("layers", "0.5 in soft EVA"),
         ("drop", "Wipe-clean top"), ("grip", "Non-slip"), ("shield", "CPC / CPSIA tested")]

AUD = {
    "classroom": {
        "tag": "For classrooms &amp; childcare",
        "h1": 'A soft play corner<br>for every <em>classroom</em>',
        "sub": "Cushioned, wipe-clean floor space for circle time, quiet corners and waiting areas, in two calm designs that look good in any room.",
        "offer_top": "Local to Sterling, VA",
        "offer": "Free visit &amp; room measuring",
        "offer_sub": "We'll measure your space and bring both designs to see in person.",
        "extra": None,
        "banner_h1": 'Soft play space for <em>classrooms</em>',
        "banner_sub": "&amp; waiting rooms",
    },
    "clinic": {
        "tag": "For pediatric waiting rooms",
        "h1": 'A softer waiting room<br>for <em>little patients</em>',
        "sub": "A cushioned, wipe-clean play space that turns the wait into play time, in two calm designs that suit a clinic.",
        "offer_top": "Local to Sterling, VA",
        "offer": "Free visit &amp; room measuring",
        "offer_sub": "We'll measure your waiting room and bring both designs to see in person.",
        "extra": ("gift", "Gift-a-Mat", "Ask about our Gift-a-Mat program for young patients."),
        "banner_h1": 'Soft play space for <em>waiting rooms</em>',
        "banner_sub": "and a Gift-a-Mat program for young patients",
    },
}

CSS = """
@font-face{font-family:"Fredoka";src:url("../fonts/Fredoka.woff2") format("woff2");font-weight:300 700}
@font-face{font-family:"Nunito";src:url("../fonts/Nunito.woff2") format("woff2");font-weight:200 1000}
*{box-sizing:border-box;margin:0;padding:0}
html,body{background:#FBF4EA}
.f{position:relative;overflow:hidden;font-family:Nunito,sans-serif;color:#3B2A1C;background:#FBF4EA}
.f h1,.f h2,.f .disp{font-family:Fredoka,sans-serif;font-weight:600;letter-spacing:-.015em}
.f em{font-style:normal;color:#62794F}
.blob{position:absolute;border-radius:50%;filter:blur(2px)}
.paper{position:absolute;inset:0;background:
 radial-gradient(900px 700px at -10% -10%,rgba(233,166,161,.28),transparent 60%),
 radial-gradient(900px 800px at 110% 110%,rgba(122,143,106,.24),transparent 60%),
 radial-gradient(600px 500px at 105% 20%,rgba(233,176,65,.14),transparent 60%)}
.tag{display:inline-flex;align-items:center;gap:10px;font-weight:800;font-size:19px;letter-spacing:.14em;text-transform:uppercase;color:#4E6444;
 border:2px solid rgba(78,100,68,.35);border-radius:999px;padding:10px 22px;background:rgba(255,255,255,.55)}
.eyebrow{font-weight:800;font-size:19px;letter-spacing:.16em;text-transform:uppercase;color:#C2573B}
.card{position:absolute;border-radius:34px;overflow:hidden;background:#fff;border:10px solid #fff;box-shadow:0 40px 70px -34px rgba(59,42,28,.55)}
.card img{width:100%;height:100%;object-fit:cover;display:block;border-radius:24px}
.lbl{position:absolute;left:50%;bottom:26px;transform:translateX(-50%);background:rgba(255,255,255,.95);border-radius:999px;padding:10px 24px;
 font-family:Fredoka,sans-serif;font-weight:600;font-size:26px;white-space:nowrap;box-shadow:0 12px 24px -12px rgba(59,42,28,.45)}
.char{position:absolute;filter:drop-shadow(0 26px 22px rgba(59,42,28,.28))}
.spec{display:flex;align-items:center;gap:14px;font-weight:800;font-size:23px;color:#3B2A1C}
.spec .i{width:58px;height:58px;border-radius:18px;display:grid;place-items:center;flex:none}
.rule{height:2px;background:linear-gradient(90deg,transparent,rgba(59,42,28,.18),transparent)}
.stripe{position:absolute;left:0;right:0;height:12px;display:flex}
.stripe i{flex:1}
"""

def stripe(top):
    pos = "top:0" if top else "bottom:0"
    return (f'<div class="stripe" style="{pos}"><i style="background:#7A8F6A"></i><i style="background:#E9B041"></i>'
            f'<i style="background:#E9A6A1"></i><i style="background:#7AA3BD"></i><i style="background:#7A8F6A"></i></div>')

TINTS = ["#E3E9DA", "#F6E7C2", "#F7DEDA", "#DDE9F1", "#E3E9DA", "#F6E7C2"]
INK = ["#4E6444", "#94681A", "#A9544B", "#3F6A85", "#4E6444", "#94681A"]

def specs_grid(cols=3, size=23):
    cells = "".join(f'<div class="spec" style="font-size:{size}px"><span class="i" style="background:{TINTS[i]};color:{INK[i]}">{icon(n, 30)}</span>{t}</div>'
                    for i, (n, t) in enumerate(SPECS))
    return f'<div style="display:grid;grid-template-columns:repeat({cols},minmax(0,1fr));gap:22px 26px">{cells}</div>'

def contact_row(color="#3B2A1C", size=24):
    return (f'<div style="display:flex;gap:34px;align-items:center;flex-wrap:wrap;font-weight:800;font-size:{size}px;color:{color}">'
            f'<span style="display:flex;gap:10px;align-items:center">{icon("mail", 28)}hello@tovinest.com</span>'
            f'<span style="display:flex;gap:10px;align-items:center">{icon("globe", 28)}tovinest.com</span></div>')

def tall(a):
    A = AUD[a]
    extra = ""
    if A["extra"]:
        ic, t, s = A["extra"]
        extra = (f'<div style="display:flex;gap:18px;align-items:center;background:#FFFFFF;border-radius:26px;padding:20px 26px;margin-top:22px;'
                 f'box-shadow:0 18px 40px -26px rgba(59,42,28,.45)"><span class="i" style="width:64px;height:64px;border-radius:20px;display:grid;place-items:center;'
                 f'background:#F7DEDA;color:#A9544B;flex:none">{icon(ic, 34)}</span><div><div class="disp" style="font-size:30px">{t}</div>'
                 f'<div style="font-size:22px;font-weight:600;color:#6B5A4B">{s}</div></div></div>')
    return f'''<div class="f" style="width:1200px;height:1600px">
<div class="paper"></div>{stripe(True)}
<div style="position:absolute;left:80px;right:80px;top:58px;display:flex;justify-content:space-between;align-items:center">
 <img src="../img/logo.png" style="height:118px">
 <span class="tag">{A["tag"]}</span>
</div>
<div style="position:absolute;left:80px;right:80px;top:236px">
 <div class="eyebrow">Moon Walkers Premium EVA Playmat</div>
 <h1 style="font-size:88px;line-height:1.0;margin-top:14px">{A["h1"]}</h1>
 <p style="font-size:27px;line-height:1.45;color:#6B5A4B;font-weight:600;margin-top:22px;max-width:900px">{A["sub"]}</p>
</div>
<div style="position:absolute;left:0;right:0;top:610px;height:520px">
 <div class="card" style="left:110px;top:30px;width:520px;height:440px;transform:rotate(-4deg)"><img src="../img/flatlay-rainboho.jpg"><span class="lbl">RainBoho</span></div>
 <div class="card" style="left:570px;top:0;width:520px;height:440px;transform:rotate(3.5deg)"><img src="../img/flatlay-ash-starlight.jpg"><span class="lbl">Ash Starlight</span></div>
 <img class="char" src="../img/dino.png" style="left:6px;top:228px;width:205px">
 <img class="char" src="../img/dima.png" style="right:14px;top:250px;width:178px">
</div>
<div style="position:absolute;left:80px;right:80px;top:1156px">{specs_grid(3, 22)}</div>
<div style="position:absolute;left:60px;right:60px;top:1310px;height:190px;border-radius:36px;background:#4E6444;color:#FBF4EA;display:flex;align-items:center;gap:34px;padding:0 44px">
 <span style="width:92px;height:92px;border-radius:28px;background:rgba(251,244,234,.14);display:grid;place-items:center;flex:none;color:#F3C66B">{icon("pin", 50)}</span>
 <div style="flex:1;min-width:0">
  <div style="font-weight:800;font-size:19px;letter-spacing:.16em;text-transform:uppercase;color:#F3C66B">{A["offer_top"]}</div>
  <div class="disp" style="font-size:46px;line-height:1.05;margin-top:4px">{A["offer"]}</div>
  <div style="font-size:20px;font-weight:600;color:#DCE5D3;margin-top:6px">{A["offer_sub"]}</div>
 </div>
</div>
{"" if not A["extra"] else ""}
<div style="position:absolute;left:80px;right:80px;bottom:30px;display:flex;justify-content:space-between;align-items:center">
 {contact_row("#3B2A1C", 22)}
 <span style="font-size:17px;font-weight:700;color:#8C7A6B">Always supervise children during play.</span>
</div>
{stripe(False)}
</div>''' if not A["extra"] else tall_clinic(A)

def tall_clinic(A):
    ic, t, s = A["extra"]
    return f'''<div class="f" style="width:1200px;height:1600px">
<div class="paper"></div>{stripe(True)}
<div style="position:absolute;left:80px;right:80px;top:58px;display:flex;justify-content:space-between;align-items:center">
 <img src="../img/logo.png" style="height:118px">
 <span class="tag">{A["tag"]}</span>
</div>
<div style="position:absolute;left:80px;right:80px;top:236px">
 <div class="eyebrow">Moon Walkers Premium EVA Playmat</div>
 <h1 style="font-size:88px;line-height:1.0;margin-top:14px">{A["h1"]}</h1>
 <p style="font-size:27px;line-height:1.45;color:#6B5A4B;font-weight:600;margin-top:22px;max-width:900px">{A["sub"]}</p>
</div>
<div style="position:absolute;left:0;right:0;top:600px;height:500px">
 <div class="card" style="left:110px;top:30px;width:500px;height:420px;transform:rotate(-4deg)"><img src="../img/flatlay-rainboho.jpg"><span class="lbl">RainBoho</span></div>
 <div class="card" style="left:590px;top:0;width:500px;height:420px;transform:rotate(3.5deg)"><img src="../img/flatlay-ash-starlight.jpg"><span class="lbl">Ash Starlight</span></div>
 <img class="char" src="../img/dino.png" style="left:6px;top:214px;width:195px">
 <img class="char" src="../img/dima.png" style="right:14px;top:236px;width:170px">
</div>
<div style="position:absolute;left:80px;right:80px;top:1118px">{specs_grid(3, 22)}</div>
<div style="position:absolute;left:60px;right:60px;top:1272px;height:230px;display:grid;grid-template-columns:1.25fr 1fr;gap:20px">
 <div style="border-radius:34px;background:#4E6444;color:#FBF4EA;display:flex;align-items:center;gap:26px;padding:0 34px">
  <span style="width:84px;height:84px;border-radius:26px;background:rgba(251,244,234,.14);display:grid;place-items:center;flex:none;color:#F3C66B">{icon("pin", 46)}</span>
  <div><div style="font-weight:800;font-size:18px;letter-spacing:.16em;text-transform:uppercase;color:#F3C66B">{A["offer_top"]}</div>
   <div class="disp" style="font-size:40px;line-height:1.05;margin-top:4px">{A["offer"]}</div>
   <div style="font-size:19px;font-weight:600;color:#DCE5D3;margin-top:6px">{A["offer_sub"]}</div></div>
 </div>
 <div style="border-radius:34px;background:#F4D8D2;display:flex;flex-direction:column;justify-content:center;gap:10px;padding:0 32px">
  <div style="display:flex;gap:14px;align-items:center;color:#A9544B">{icon(ic, 46)}<span class="disp" style="font-size:40px;color:#3B2A1C">{t}</span></div>
  <div style="font-size:21px;font-weight:700;color:#6B4A43;line-height:1.35">{s}</div>
 </div>
</div>
<div style="position:absolute;left:80px;right:80px;bottom:30px;display:flex;justify-content:space-between;align-items:center">
 {contact_row("#3B2A1C", 22)}
 <span style="font-size:17px;font-weight:700;color:#8C7A6B">Always supervise children during play.</span>
</div>
{stripe(False)}
</div>'''

def banner(a):
    A = AUD[a]
    chips = "".join(f'<span style="display:inline-flex;align-items:center;gap:8px;padding:8px 16px;border-radius:999px;background:{TINTS[i]};color:{INK[i]};'
                    f'font-weight:800;font-size:19px">{icon(n, 22)}{t}</span>'
                    for i, (n, t) in enumerate([SPECS[0], SPECS[1], SPECS[3], SPECS[4]]))
    extra = " · Gift-a-Mat" if A["extra"] else ""
    return f'''<div class="f" style="width:1200px;height:780px">
<div class="paper"></div>{stripe(True)}
<div style="position:absolute;left:56px;top:46px;right:56px;display:flex;justify-content:space-between;align-items:center">
 <img src="../img/logo.png" style="height:84px"><span class="tag" style="font-size:16px;padding:8px 18px">{A["tag"]}</span>
</div>
<div style="position:absolute;left:0;right:0;top:150px;text-align:center">
 <h1 style="font-size:60px;line-height:1.05">{A["banner_h1"]}</h1>
 <p style="font-size:25px;font-weight:700;color:#6B5A4B;margin-top:8px">{A["banner_sub"]}</p>
</div>
<div class="card" style="left:262px;top:300px;width:330px;height:280px;transform:rotate(-3deg);border-width:8px;border-radius:28px"><img src="../img/flatlay-rainboho.jpg"><span class="lbl" style="font-size:20px;bottom:16px;padding:7px 18px">RainBoho</span></div>
<div class="card" style="left:608px;top:292px;width:330px;height:280px;transform:rotate(3deg);border-width:8px;border-radius:28px"><img src="../img/flatlay-ash-starlight.jpg"><span class="lbl" style="font-size:20px;bottom:16px;padding:7px 18px">Ash Starlight</span></div>
<img class="char" src="../img/dino.png" style="left:56px;top:330px;width:190px">
<img class="char" src="../img/dima.png" style="right:58px;top:342px;width:168px">
<div style="position:absolute;left:0;right:0;top:612px;display:flex;justify-content:center;gap:12px;flex-wrap:wrap">{chips}</div>
<div style="position:absolute;left:0;right:0;bottom:30px;display:flex;justify-content:center;gap:22px;align-items:center;font-weight:800;font-size:21px;color:#3B2A1C">
 <span style="display:flex;gap:8px;align-items:center;color:#4E6444">{icon("pin", 24)}Local to Sterling, VA · free visit &amp; room measuring{extra}</span>
 <span style="color:#C2573B">tovinest.com</span>
</div>
{stripe(False)}
</div>'''

if __name__ == "__main__":
    os.makedirs(BUILD, exist_ok=True)
    jobs = []
    for a in AUD:
        for kind, fn, w, h in [("flyer", tall, 1200, 1600), ("banner", banner, 1200, 780)]:
            p = os.path.join(BUILD, f"{a}-{kind}.html")
            open(p, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{fn(a)}</body></html>')
            jobs.append({"html": p, "name": f"tovinest-{a}-{kind}", "w": w, "h": h})
    json.dump(jobs, open(os.path.join(BUILD, "jobs.json"), "w"), indent=1)
    print(len(jobs), "pages")
