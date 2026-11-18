"""Gift-a-Mat program: B2B outreach flyer + banner for practices, and a printable gift card (front/back).
python3 gift.py && node render.js && python3 post.py
Model: the practice buys gift cards; families redeem at tovinest.com checkout (Shopify gift card code), shipped across the USA.
No prices for volume (ask us), no invented stats or testimonials.
"""
import os, json, segno
from flyers import CSS, ICON, icon, stripe, BUILD

ICON.update({
    "tooth": '<path d="M7 3.5c-2.6 0-4 2-4 4.6 0 2.4 1.2 3.6 1.7 6 .5 2.6.9 6.4 2.6 6.4 1.6 0 1.6-4.6 3-4.6h3.4c1.4 0 1.4 4.6 3 4.6 1.7 0 2.1-3.8 2.6-6.4.5-2.4 1.7-3.6 1.7-6 0-2.6-1.4-4.6-4-4.6-2 0-3 1.2-5 1.2s-3-1.2-5-1.2z"/>',
    "baby": '<circle cx="12" cy="8" r="4.5"/><path d="M5 21c.6-4 3.4-6.5 7-6.5s6.4 2.5 7 6.5"/><path d="M10.4 8.6h.01M13.6 8.6h.01"/>',
    "steth": '<path d="M5 3.5v5a4 4 0 0 0 8 0v-5"/><path d="M9 12.5v2.5a5 5 0 0 0 10 0v-2"/><circle cx="19" cy="11" r="2"/>',
    "star": '<path d="M12 3.5l2.6 5.4 5.9.8-4.3 4.1 1 5.8L12 16.9 6.8 19.6l1-5.8L3.5 9.7l5.9-.8z"/>',
    "heart": '<path d="M12 20s-7.5-4.6-7.5-10A4.3 4.3 0 0 1 12 7.4 4.3 4.3 0 0 1 19.5 10c0 5.4-7.5 10-7.5 10z"/>',
    "truck": '<path d="M2.5 6.5h11v9h-11z"/><path d="M13.5 9.5h4l3 3v3h-7z"/><circle cx="6.5" cy="17" r="1.8"/><circle cx="17" cy="17" r="1.8"/>',
})

QR = segno.make("https://tovinest.com", error="m").svg_inline(scale=10, dark="#3B2A1C", light=None, border=0).replace("<svg ", '<svg style="width:100%;height:100%" ', 1)

EXTRA = """
.uc{background:#fff;border-radius:28px;padding:24px 24px 22px;box-shadow:0 22px 44px -30px rgba(59,42,28,.5)}
.uc .ic{width:60px;height:60px;border-radius:18px;display:grid;place-items:center}
.uc h3{font-family:Fredoka,sans-serif;font-weight:600;font-size:27px;line-height:1.1;margin-top:14px}
.uc p{font-size:18px;font-weight:600;color:#6B5A4B;line-height:1.35;margin-top:6px}
.who{font-weight:900;font-size:14px;letter-spacing:.14em;text-transform:uppercase;margin-top:12px}
.st{display:flex;gap:14px;align-items:flex-start}
.st b{flex:none;width:44px;height:44px;border-radius:50%;background:#E9B041;color:#3B2A1C;display:grid;place-items:center;font-family:Fredoka,sans-serif;font-weight:600;font-size:23px}
.st .t{font-family:Fredoka,sans-serif;font-weight:600;font-size:24px;line-height:1.15}
.st .s{font-size:17px;font-weight:600;color:#DCE5D3;margin-top:2px}
.gc{position:absolute;border-radius:26px;overflow:hidden;background:#FBF4EA;box-shadow:0 40px 70px -30px rgba(59,42,28,.6)}
"""

USE = [
    ("baby", "#F7DEDA", "#A9544B", "Pediatricians", "New-family welcome gift", "A warm hello for newborns joining your practice."),
    ("tooth", "#DDE9F1", "#3F6A85", "Pediatric dentists", "First-visit reward", "Turn a first check-up into a happy memory."),
    ("heart", "#E3E9DA", "#4E6444", "OB/GYN &amp; birth centers", "Going-home baby gift", "Something soft for the first weeks at home."),
    ("star", "#F6E7C2", "#94681A", "Therapy &amp; childcare", "Milestone &amp; graduation gift", "Celebrate progress with OT, PT, speech or daycare families."),
]

def usecases():
    return "".join(f'''<div class="uc"><span class="ic" style="background:{bg};color:{ink}">{icon(ic,32)}</span>
<div class="who" style="color:{ink}">{who}</div><h3>{t}</h3><p>{s}</p></div>''' for ic, bg, ink, who, t, s in USE)

def mini_card(w):
    """Small gift-card mockup used inside the flyer (scaled front)."""
    s = w / 700
    return f'''<div style="width:700px;height:440px;transform:scale({s});transform-origin:0 0;position:relative">
<div class="gc" style="inset:0;position:absolute">{card_front_inner(700, 440, small=True)}</div></div>'''

def card_front_inner(W, H, small=False, practice="Your Practice Name"):
    k = W / 1400
    def px(v): return f"{v*k:.0f}px"
    return f'''<div class="paper"></div>
<div style="position:absolute;left:0;right:0;top:0;height:{px(16)};display:flex"><i style="flex:1;background:#7A8F6A"></i><i style="flex:1;background:#E9B041"></i><i style="flex:1;background:#E9A6A1"></i><i style="flex:1;background:#7AA3BD"></i></div>
<img src="../img/logo.png" style="position:absolute;left:{px(70)};top:{px(60)};height:{px(130)}">
<div style="position:absolute;right:{px(70)};top:{px(80)};font-weight:900;font-size:{px(22)};letter-spacing:.16em;text-transform:uppercase;color:#C2573B;
 border:{px(3)} solid rgba(194,87,59,.4);border-radius:999px;padding:{px(10)} {px(24)}">Gift card</div>
<div style="position:absolute;left:{px(70)};top:{px(250)};width:{px(700)}">
 <div style="font-family:Fredoka,sans-serif;font-weight:600;font-size:{px(104)};line-height:.98;letter-spacing:-.02em">A little gift<br><span style="color:#62794F">for you</span></div>
 <div style="font-size:{px(30)};font-weight:700;color:#6B5A4B;margin-top:{px(26)}">With love from</div>
 <div style="font-family:Fredoka,sans-serif;font-weight:600;font-size:{px(46)};color:#3B2A1C;margin-top:{px(4)};border-bottom:{px(3)} dashed rgba(59,42,28,.3);padding-bottom:{px(8)}">{practice}</div>
 <div style="font-size:{px(26)};font-weight:700;color:#6B5A4B;margin-top:{px(28)};line-height:1.35">Good for one <b style="color:#3B2A1C">Moon Walkers Premium Playmat</b><br>in RainBoho or Ash Starlight</div>
</div>
<div class="card" style="left:{px(830)};top:{px(270)};width:{px(470)};height:{px(360)};transform:rotate(4deg);border-width:{px(10)};border-radius:{px(30)}"><img src="../img/flatlay-rainboho.jpg" style="border-radius:{px(20)}"></div>
<div class="card" style="left:{px(880)};top:{px(560)};width:{px(400)};height:{px(300)};transform:rotate(-5deg);border-width:{px(10)};border-radius:{px(30)}"><img src="../img/flatlay-ash-starlight.jpg" style="border-radius:{px(20)}"></div>
<img class="char" src="../img/dino.png" style="left:{px(760)};top:{px(640)};width:{px(190)}">
<img class="char" src="../img/dima.png" style="left:{px(1215)};top:{px(170)};width:{px(150)}">
<div style="position:absolute;left:{px(70)};bottom:{px(54)};font-weight:800;font-size:{px(24)};color:#4E6444;display:flex;gap:{px(10)};align-items:center">{icon("truck", 30*k)} Ships across the USA · tovinest.com</div>'''

def card_front():
    return f'<div class="f gc" style="position:relative;width:1400px;height:1000px;border-radius:0">{card_front_inner(1400,1000)}</div>'

def card_back():
    steps = [("Visit tovinest.com", "or scan the code"), ("Choose your design", "RainBoho or Ash Starlight"), ("Enter your gift code at checkout", "We ship it to your door, anywhere in the USA")]
    st = "".join(f'<div class="st"><b style="width:58px;height:58px;font-size:30px">{i+1}</b><div><div class="t" style="font-size:36px">{t}</div><div class="s" style="font-size:24px;color:#6B5A4B">{s}</div></div></div>' for i,(t,s) in enumerate(steps))
    return f'''<div class="f" style="width:1400px;height:1000px"><div class="paper"></div>{stripe(True)}
<div style="position:absolute;left:90px;top:110px;width:800px">
 <div class="eyebrow" style="font-size:22px">How to redeem</div>
 <div style="display:flex;flex-direction:column;gap:30px;margin-top:30px">{st}</div>
 <div style="margin-top:46px;font-weight:900;font-size:20px;letter-spacing:.16em;text-transform:uppercase;color:#4E6444">Your gift code</div>
 <div style="margin-top:10px;display:inline-block;background:#fff;border:3px dashed #E9B041;border-radius:22px;padding:18px 34px;
  font-family:ui-monospace,Menlo,monospace;font-weight:700;font-size:44px;letter-spacing:.12em;color:#3B2A1C">XXXX-XXXX-XXXX-XXXX</div>
 <div style="font-size:22px;font-weight:700;color:#6B5A4B;margin-top:22px;line-height:1.45">Good for one Moon Walkers Premium Playmat at tovinest.com.<br>Ships across the USA.</div>
</div>
<div style="position:absolute;right:100px;top:120px;text-align:center">
 <div style="width:330px;height:330px;padding:22px;background:#fff;border-radius:32px;border:4px solid #E9B041">{QR}</div>
 <div style="font-weight:900;font-size:20px;letter-spacing:.14em;text-transform:uppercase;color:#C2573B;margin-top:16px">Scan to redeem</div>
 <img class="char" src="../img/dino.png" style="position:relative;width:200px;margin-top:30px">
</div>
<div style="position:absolute;left:90px;right:90px;bottom:50px;display:flex;justify-content:space-between;font-weight:700;font-size:20px;color:#8C7A6B">
 <span>Questions? hello@tovinest.com</span><span>Always supervise children during play.</span></div>
{stripe(False)}</div>'''

def flyer():  # 1200x1600 email/attachment
    steps = [("Tell us how many gifts you need", "Pick RainBoho, Ash Starlight, or let families choose"),
             ("We make gift cards with your practice name", "Ready to hand out at the front desk"),
             ("Families redeem online at tovinest.com", "We ship the mat to their home, anywhere in the USA")]
    st = "".join(f'<div class="st"><b>{i+1}</b><div><div class="t">{t}</div><div class="s">{s}</div></div></div>' for i,(t,s) in enumerate(steps))
    return f'''<div class="f" style="width:1200px;height:1600px"><div class="paper"></div>{stripe(True)}
<div style="position:absolute;left:70px;right:70px;top:52px;display:flex;justify-content:space-between;align-items:center">
 <img src="../img/logo.png" style="height:108px"><span class="tag" style="font-size:16px">For pediatric, dental &amp; family practices</span></div>
<div style="position:absolute;left:70px;top:200px;width:640px">
 <div class="eyebrow" style="font-size:18px">The Tovi Nest Gift-a-Mat program</div>
 <h1 style="font-size:64px;line-height:1.02;margin-top:12px">A patient gift<br>families <em>actually use</em></h1>
 <p style="font-size:23px;line-height:1.45;color:#6B5A4B;font-weight:600;margin-top:18px">Give young patients a soft Moon Walkers playmat. It's a thank-you that goes home with them and gets used every day.</p>
</div>
<div style="position:absolute;left:690px;top:230px;transform:rotate(4deg)">{mini_card(460)}</div>
<div style="position:absolute;left:70px;right:70px;top:600px">
 <div class="eyebrow" style="font-size:17px;color:#4E6444">Who it's for</div>
 <div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px;margin-top:14px">{usecases()}</div>
</div>
<div style="position:absolute;left:60px;right:60px;top:985px;border-radius:36px;background:#4E6444;color:#FBF4EA;padding:34px 40px;display:grid;grid-template-columns:1.35fr 1fr;gap:34px;align-items:center">
 <div><div class="disp" style="font-size:36px">How it works</div><div style="display:flex;flex-direction:column;gap:18px;margin-top:20px">{st}</div></div>
 <div style="background:rgba(251,244,234,.1);border-radius:26px;padding:24px 26px">
  <div style="font-weight:800;font-size:16px;letter-spacing:.16em;text-transform:uppercase;color:#F3C66B">What each family gets</div>
  <div style="font-size:19px;font-weight:700;line-height:1.6;margin-top:10px;color:#FBF4EA">
   One Moon Walkers playmat<br>16 tiles · 67 × 48 in · 0.5 in soft EVA<br>Wipe-clean · Non-slip<br>CPC / CPSIA tested</div>
 </div>
</div>
<div style="position:absolute;left:60px;right:60px;top:1365px;height:112px;border-radius:30px;background:#F7DEDA;display:flex;align-items:center;gap:22px;padding:0 34px">
 <span style="width:64px;height:64px;border-radius:20px;background:#fff;color:#A9544B;display:grid;place-items:center;flex:none">{icon("gift",34)}</span>
 <div><div class="disp" style="font-size:30px;color:#3B2A1C">Volume pricing for practices</div>
 <div style="font-size:19px;font-weight:700;color:#6B4A43">Reply to this email or write to hello@tovinest.com, and we'll put together a quote.</div></div>
</div>
<div style="position:absolute;left:70px;right:70px;bottom:30px;display:flex;justify-content:space-between;align-items:center;font-weight:800;font-size:20px">
 <span style="display:flex;gap:26px"><span style="display:flex;gap:8px;align-items:center">{icon("mail",24)}hello@tovinest.com</span><span style="display:flex;gap:8px;align-items:center">{icon("globe",24)}tovinest.com</span></span>
 <span style="font-size:15px;font-weight:700;color:#8C7A6B">Always supervise children during play.</span></div>
{stripe(False)}</div>'''

def banner():  # 1200x780 email header
    return f'''<div class="f" style="width:1200px;height:780px"><div class="paper"></div>{stripe(True)}
<img src="../img/logo.png" style="position:absolute;left:60px;top:44px;height:92px">
<div style="position:absolute;left:60px;top:205px;width:580px">
 <div class="eyebrow" style="font-size:17px">Gift-a-Mat program</div>
 <h1 style="font-size:56px;line-height:1.02;margin-top:10px">A patient gift<br>families <em>actually use</em></h1>
 <p style="font-size:22px;font-weight:700;color:#6B5A4B;margin-top:16px;line-height:1.4">Soft playmat gift cards for pediatric, dental and family practices. Families redeem online, and we ship across the USA.</p>
 <div style="display:flex;gap:10px;margin-top:22px;flex-wrap:wrap;font-weight:800;font-size:16px">
  {"".join(f'<span style="background:#fff;border-radius:999px;padding:8px 14px;display:flex;gap:6px;align-items:center;color:{c}">{icon(i,18)}{t}</span>' for i,t,c in [("baby","Pediatricians","#A9544B"),("tooth","Dentists","#3F6A85"),("heart","OB/GYN","#4E6444"),("star","Therapy &amp; childcare","#94681A")])}
 </div>
</div>
<div style="position:absolute;left:660px;top:235px;transform:rotate(4deg)">{mini_card(490)}</div>
<div style="position:absolute;left:0;right:0;bottom:30px;text-align:center;font-weight:800;font-size:20px;color:#3B2A1C">Volume pricing for practices · hello@tovinest.com · <span style="color:#C2573B">tovinest.com</span></div>
{stripe(False)}</div>'''

if __name__ == "__main__":
    css = CSS + EXTRA
    jobs = [j for j in json.load(open(os.path.join(BUILD, "jobs.json"))) if "gift" not in j["name"]]
    for name, fn, w, h in [("gift-program-flyer", flyer, 1200, 1600), ("gift-program-banner", banner, 1200, 780),
                           ("gift-card-front", card_front, 1400, 1000), ("gift-card-back", card_back, 1400, 1000)]:
        p = os.path.join(BUILD, f"{name}.html")
        open(p, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{fn()}</body></html>')
        jobs.append({"html": p, "name": f"tovinest-{name}", "w": w, "h": h})
    json.dump(jobs, open(os.path.join(BUILD, "jobs.json"), "w"), indent=1)
    print("ok")
