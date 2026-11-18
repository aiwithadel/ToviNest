"""Inline-email comparison: interlocking EVA tiles (Moon Walkers) vs a typical folding foam mat.
python3 compare.py && node render.js && python3 post.py
Category-level and fair: no claims about any specific competitor brand, and the folding mat gets its real advantages.
"""
import os, json
from flyers import CSS, BUILD, stripe, icon

EXTRA = """
.row{display:grid;grid-template-columns:250px 1fr 1fr;border-top:2px solid rgba(59,42,28,.08)}
.row>div{padding:18px 22px;font-size:21px;font-weight:700;line-height:1.35;display:flex;gap:12px;align-items:flex-start}
.row .k{font-weight:900;font-size:17px;letter-spacing:.1em;text-transform:uppercase;color:#8C7A6B;align-items:center}
.row .us{background:rgba(227,233,218,.55);color:#3B2A1C}
.row .them{color:#6B5A4B}
.ok,.mid{flex:none;width:30px;height:30px;border-radius:50%;display:grid;place-items:center;margin-top:1px}
.ok{background:#4E6444;color:#fff}.mid{background:#EADFD2;color:#8C7A6B}
.why{background:#fff;border-radius:26px;padding:22px 24px;box-shadow:0 18px 40px -28px rgba(59,42,28,.5)}
.why h3{font-family:Fredoka,sans-serif;font-weight:600;font-size:27px;margin-top:10px;line-height:1.1}
.why p{font-size:18px;font-weight:600;color:#6B5A4B;line-height:1.4;margin-top:6px}
"""
CHECK = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>'
DOT = '<svg viewBox="0 0 24 24" width="16" height="16"><circle cx="12" cy="12" r="4" fill="currentColor"/></svg>'

ROWS = [
    ("Material", "EVA foam: dense, closed-cell, bounces back", "Varies by brand (often XPE or PE foam). Check the label", 1, 0),
    ("Thickness", "0.5 in cushion across every tile", "Varies by brand. Ask for the spec", 1, 0),
    ("If one spot wears out", "Swap out just that tile", "The whole mat is one piece", 1, 0),
    ("Size &amp; shape", "16 tiles · 67 × 48 in. Rearrange or link mats for a bigger area", "One fixed size", 1, 0),
    ("Cleaning", "Wipe-clean surface", "Wipe-clean surface", 1, 1),
    ("Storage", "Tiles stack flat", "Folds up quickly", 1, 1),
    ("Safety testing", "CPC / CPSIA tested · 0+", "Ask the seller for a CPC", 1, 0),
]

WHY = [("drop", "#DDE9F1", "#3F6A85", "Not sponge foam", "Closed-cell EVA doesn't soak up spills the way open-cell sponge foam does. Just wipe it."),
       ("tiles", "#E3E9DA", "#4E6444", "Built to be fixed", "Interlocking tiles mean a worn or damaged spot is a one-tile fix, not a new mat."),
       ("layers", "#F6E7C2", "#94681A", "Grows with the room", "Reshape it for circle time, a reading nook or a baby corner. Add a second mat for more space.")]

def page():
    rows = "".join(f'''<div class="row"><div class="k">{k}</div>
<div class="us"><span class="ok">{CHECK}</span>{us}</div>
<div class="them"><span class="{'ok' if tg else 'mid'}">{CHECK if tg else DOT}</span>{them}</div></div>''' for k, us, them, ug, tg in ROWS)
    why = "".join(f'<div class="why"><span style="width:56px;height:56px;border-radius:18px;display:grid;place-items:center;background:{bg};color:{ink}">{icon(ic,30)}</span><h3>{t}</h3><p>{d}</p></div>' for ic, bg, ink, t, d in WHY)
    return f'''<div class="f" style="width:1200px;height:1550px"><div class="paper"></div>{stripe(True)}
<img src="../img/logo.png" style="position:absolute;left:70px;top:50px;height:104px">
<span class="tag" style="position:absolute;right:70px;top:80px;font-size:16px">For classrooms &amp; childcare</span>
<div style="position:absolute;left:70px;top:190px;width:660px">
 <div class="eyebrow" style="font-size:18px">Moon Walkers Premium EVA Playmat</div>
 <h1 style="font-size:62px;line-height:1.04;margin-top:10px">Why we chose <em>interlocking EVA</em> tiles</h1>
 <p style="font-size:23px;font-weight:600;color:#6B5A4B;line-height:1.45;margin-top:14px">Not all foam mats are the same. Here's how our tiles compare with a typical folding foam mat.</p>
</div>
<div class="card" style="left:800px;top:180px;width:330px;height:260px;transform:rotate(4deg);border-width:8px"><img src="../img/flatlay-ash-starlight.jpg"></div>
<img class="char" src="../img/dino.png" style="left:745px;top:330px;width:120px">
<div style="position:absolute;left:60px;right:60px;top:500px;background:#fff;border-radius:30px;overflow:hidden;box-shadow:0 26px 50px -30px rgba(59,42,28,.5)">
 <div class="row" style="border-top:0"><div></div>
  <div style="background:#4E6444;color:#FBF4EA;font-family:Fredoka,sans-serif;font-weight:600;font-size:25px">Tovi Nest interlocking EVA</div>
  <div style="background:#F1E9DF;font-family:Fredoka,sans-serif;font-weight:600;font-size:25px;color:#6B5A4B">Typical folding foam mat</div></div>
 {rows}
</div>
<div style="position:absolute;left:60px;right:60px;top:1165px;display:grid;grid-template-columns:repeat(3,1fr);gap:18px">{why}</div>
<div style="position:absolute;left:70px;right:70px;bottom:34px;display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:20px">
 <span style="display:flex;gap:24px"><span style="display:flex;gap:8px;align-items:center">{icon("mail",24)}hello@tovinest.com</span><span style="display:flex;gap:8px;align-items:center">{icon("globe",24)}tovinest.com/catalog</span></span>
 <span style="font-size:15px;font-weight:700;color:#8C7A6B">Always supervise children during play.</span></div>
{stripe(False)}</div>'''

if __name__ == "__main__":
    jobs = [j for j in json.load(open(os.path.join(BUILD, "jobs.json"))) if "compare" not in j["name"]]
    p = os.path.join(BUILD, "compare-eva.html")
    open(p, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS + EXTRA}</style></head><body>{page()}</body></html>')
    jobs.append({"html": p, "name": "tovinest-compare-eva-vs-folding", "w": 1200, "h": 1550})
    json.dump(jobs, open(os.path.join(BUILD, "jobs.json"), "w"), indent=1)
    print("ok")
