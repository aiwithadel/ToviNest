"""Consumer flyer for sharing in community / parent groups.
python3 community.py && node render.js && python3 post.py
Ordering is online only: tovinest.com (QR). No DM/WhatsApp ordering, no invented promos.
"""
import os, json, segno
from flyers import CSS, ICON, icon, stripe, specs_grid, BUILD
ICON["truck"] = '<path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3v3h-7z"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/>'

QR = segno.make("https://tovinest.com", error="m").svg_inline(scale=10, dark="#3B2A1C", light=None, border=0)
QR = QR.replace("<svg ", '<svg style="width:100%;height:100%" ', 1)

EXTRA = """
.price{font-family:Fredoka,sans-serif;font-weight:700;letter-spacing:-.02em}
.step{display:flex;gap:16px;align-items:flex-start}
.step b.n{flex:none;width:46px;height:46px;border-radius:50%;background:#C2573B;color:#fff;display:grid;place-items:center;
 font-family:Fredoka,sans-serif;font-weight:600;font-size:25px}
.step .t{font-family:Fredoka,sans-serif;font-weight:600;font-size:27px;line-height:1.15}
.step .s{font-size:19px;font-weight:600;color:#6B5A4B;margin-top:2px}
"""

def price_band():
    return f'''<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px">
 <div style="background:#fff;border-radius:28px;padding:20px 26px;box-shadow:0 18px 40px -28px rgba(59,42,28,.5)">
  <div class="eyebrow" style="font-size:16px;color:#4E6444">One playmat</div>
  <div style="display:flex;align-items:baseline;gap:12px;margin-top:2px"><span class="price" style="font-size:62px">$49.99</span>
   <s style="font-size:26px;font-weight:700;color:#A0907F">$79.99</s></div>
  <div style="font-size:18px;font-weight:700;color:#6B5A4B">RainBoho or Ash Starlight</div>
 </div>
 <div style="background:#4E6444;color:#FBF4EA;border-radius:28px;padding:20px 26px;position:relative">
  <span style="position:absolute;top:-14px;right:20px;background:#E9B041;color:#3B2A1C;font-weight:900;font-size:15px;letter-spacing:.1em;
   text-transform:uppercase;border-radius:999px;padding:6px 14px">Best value</span>
  <div class="eyebrow" style="font-size:16px;color:#F3C66B">2-Pack</div>
  <div class="price" style="font-size:62px;margin-top:2px">$89.99</div>
  <div style="font-size:18px;font-weight:700;color:#DCE5D3">Two RainBoho · Two Ash Starlight · or Mix</div>
 </div>
</div>'''

def steps():
    S = [("Scan the code or visit <span style='color:#C2573B'>tovinest.com</span>", "Opens our online store"),
         ("Pick your design", "RainBoho, Ash Starlight, or a 2-pack"),
         ("Check out online", "Ships across the USA")]
    return "".join(f'<div class="step"><b class="n">{i+1}</b><div><div class="t">{t}</div><div class="s">{s}</div></div></div>'
                   for i, (t, s) in enumerate(S))

def how_to_order(qr=210):
    return f'''<div style="background:#fff;border-radius:34px;padding:28px 30px;display:flex;gap:30px;align-items:center;
 box-shadow:0 26px 50px -30px rgba(59,42,28,.5)">
 <div style="flex:1;display:flex;flex-direction:column;gap:16px">
  <div class="disp" style="font-size:36px">How to order</div>{steps()}
 </div>
 <div style="flex:none;text-align:center">
  <div style="width:{qr}px;height:{qr}px;padding:14px;border-radius:24px;background:#FBF4EA;border:3px solid #E9B041">{QR}</div>
  <div style="font-weight:900;font-size:16px;letter-spacing:.12em;text-transform:uppercase;color:#C2573B;margin-top:10px">Scan to shop</div>
 </div>
</div>'''

def mats(top, w, h, gap_left, right_left):
    return f'''<div class="card" style="left:{gap_left}px;top:{top+24}px;width:{w}px;height:{h}px;transform:rotate(-4deg)"><img src="../img/flatlay-rainboho.jpg"><span class="lbl">RainBoho</span></div>
<div class="card" style="left:{right_left}px;top:{top}px;width:{w}px;height:{h}px;transform:rotate(3.5deg)"><img src="../img/flatlay-ash-starlight.jpg"><span class="lbl">Ash Starlight</span></div>'''

def head(h1size):
    return f'''<div style="position:absolute;left:64px;right:64px;top:44px;display:flex;justify-content:space-between;align-items:center">
 <img src="../img/logo.png" style="height:104px">
 <span class="tag" style="font-size:16px;padding:9px 18px">{icon("truck",22)} Ships across the USA</span>
</div>
<div style="position:absolute;left:64px;right:64px;top:176px;text-align:center">
 <div class="eyebrow" style="font-size:18px">Moon Walkers Premium EVA Playmat</div>
 <h1 style="font-size:{h1size}px;line-height:1.02;margin-top:10px">A soft, beautiful<br>play space <em>for little ones</em></h1>
</div>'''

def foot():
    return f'''<div style="position:absolute;left:64px;right:64px;bottom:30px;display:flex;justify-content:space-between;align-items:center;
 font-weight:800;font-size:19px">
 <span style="display:flex;gap:18px"><span style="display:flex;gap:8px;align-items:center">{icon("globe",22)}tovinest.com</span>
 <span style="display:flex;gap:8px;align-items:center">{icon("mail",22)}hello@tovinest.com</span></span>
 <span style="font-size:15px;font-weight:700;color:#8C7A6B">Always supervise children during play.</span>
</div>'''

def feed():  # 1080x1350
    return f'''<div class="f" style="width:1080px;height:1350px"><div class="paper"></div>{stripe(True)}
{head(64).replace('top:176px','top:160px')}
<div style="position:absolute;left:0;right:0;top:350px;height:330px">
 {mats(0, 400, 300, 120, 560)}
 <img class="char" src="../img/dino.png" style="left:8px;top:136px;width:146px">
 <img class="char" src="../img/dima.png" style="right:8px;top:132px;width:128px">
</div>
<div style="position:absolute;left:64px;right:64px;top:700px">
 <div style="display:flex;justify-content:center;gap:10px;flex-wrap:wrap;font-weight:800;font-size:17px">
  {"".join(f'<span style="background:rgba(255,255,255,.7);border-radius:999px;padding:7px 14px">{t}</span>' for t in
   ["16 tiles", "67 × 48 in (5.6 × 4 ft)", "0.5 in soft EVA", "Wipe-clean", "Non-slip", "CPC / CPSIA tested"])}
 </div>
 <div style="margin-top:22px">{price_band()}</div>
 <div style="margin-top:20px">{how_to_order(188)}</div>
</div>
{foot()}{stripe(False)}</div>'''

def story():  # 1080x1920
    return f'''<div class="f" style="width:1080px;height:1920px"><div class="paper"></div>{stripe(True)}
<div style="position:absolute;inset:0;top:90px">{head(80)}</div>
<div style="position:absolute;left:0;right:0;top:520px;height:440px">
 {mats(0, 470, 360, 90, 520)}
 <img class="char" src="../img/dino.png" style="left:4px;top:210px;width:180px">
 <img class="char" src="../img/dima.png" style="right:6px;top:222px;width:160px">
</div>
<div style="position:absolute;left:64px;right:64px;top:1040px">{specs_grid(3, 20)}</div>
<div style="position:absolute;left:64px;right:64px;top:1220px">{price_band()}</div>
<div style="position:absolute;left:64px;right:64px;top:1450px">{how_to_order(210)}</div>
<div style="position:absolute;left:0;right:0;bottom:60px">{foot().replace("bottom:30px","bottom:0")}</div>
{stripe(False)}</div>'''

if __name__ == "__main__":
    css = CSS + EXTRA
    jobs = json.load(open(os.path.join(BUILD, "jobs.json")))
    jobs = [j for j in jobs if "community" not in j["name"]]
    for name, fn, w, h in [("feed", feed, 1080, 1350), ("story", story, 1080, 1920)]:
        p = os.path.join(BUILD, f"community-{name}.html")
        open(p, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{fn()}</body></html>')
        jobs.append({"html": p, "name": f"tovinest-community-{name}", "w": w, "h": h})
    json.dump(jobs, open(os.path.join(BUILD, "jobs.json"), "w"), indent=1)
    print("ok")
