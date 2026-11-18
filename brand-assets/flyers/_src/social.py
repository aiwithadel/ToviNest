"""Square (1080x1080) images for Facebook groups / Marketplace, English + Arabic.
python3 social.py && node render.js && python3 post.py
Order online only (tovinest.com). Facts: $49.99 (reg $79.99), 2-pack $89.99, 16 tiles, 67x48 in, 0.5 in EVA,
wipe-clean, non-slip, CPC/CPSIA tested, ships across the USA.
"""
import os, json, segno
from flyers import CSS, BUILD, stripe

QR = segno.make("https://tovinest.com", error="m").svg_inline(scale=10, dark="#3B2A1C", light=None, border=0).replace("<svg ", '<svg style="width:100%;height:100%" ', 1)

EXTRA = """
@font-face{font-family:"Cairo";src:url("../fonts/Cairo-arabic.woff2") format("woff2");font-weight:200 1000;unicode-range:U+0600-06FF,U+0750-077F,U+08A0-08FF,U+FB50-FDFF,U+FE70-FEFF,U+200C-200E}
.f{width:1080px;height:1080px}
.ar{direction:rtl;font-family:Cairo,Nunito,sans-serif}
.ar h1,.ar .disp{font-family:Cairo,Fredoka,sans-serif;font-weight:800;letter-spacing:0}
.ar .eyebrow,.ar .tag{letter-spacing:0;text-transform:none}
.ttl{font-family:Fredoka,sans-serif;font-weight:600;letter-spacing:-.02em;line-height:1.02}
.ar .ttl{font-family:Cairo,sans-serif;font-weight:800;line-height:1.25}
.chip{background:#fff;border-radius:999px;padding:10px 18px;font-weight:800;font-size:22px;box-shadow:0 10px 24px -16px rgba(59,42,28,.5);white-space:nowrap}
.pr{font-family:Fredoka,sans-serif;font-weight:700;letter-spacing:-.02em;direction:ltr;unicode-bidi:isolate}
.ltr{direction:ltr;unicode-bidi:isolate}
"""

T = {
 "en": dict(
   ship="Ships across the USA", h_eyebrow="Moon Walkers Premium EVA Playmat",
   h_title="Soft playmats<br>for <em>little ones</em>", h_sub="Big 67 × 48 in mat · two beautiful designs",
   was="reg.", shop="Shop at", rb_sub="Rainbows, clouds, moons &amp; little dinos in warm sand tones",
   as_sub="Calm grey with soft boho patterns", design="Design",
   chips=["16 tiles · 67 × 48 in", "0.5 in soft EVA", "Wipe-clean", "Non-slip", "CPC / CPSIA tested"],
   o_title="How to order", one="One playmat", two="2-Pack", two_sub="Two RainBoho · Two Ash Starlight · or Mix",
   steps=[("Visit tovinest.com", "or scan the code"), ("Pick your design", "RainBoho, Ash Starlight, or a 2-pack"), ("Check out online", "Ships across the USA")],
   scan="Scan to shop", sup="Always supervise children during play."),
 "ar": dict(
   ship="الشحن لكل أمريكا", h_eyebrow="بلاي مات Moon Walkers من EVA",
   h_title="بلاي مات طرية<br><em>لأطفالك الصغيرين</em>", h_sub="مقاس كبير <span class='ltr'>67 × 48</span> إنش · تصميمين حلوين",
   was="بدل", shop="اطلب من", rb_sub="قوس قزح وسحاب وقمر وديناصورات صغيرة بألوان رملية دافية",
   as_sub="رمادي هادي بنقوش بوهو ناعمة", design="تصميم",
   chips=["16 قطعة · <span class='ltr'>67 × 48</span> إنش", "سُمك نص إنش EVA", "بتتمسح بسهولة", "مش بتتزحلق", "CPC / CPSIA tested"],
   o_title="إزاي تطلب؟", one="بلاي مات واحدة", two="الاتنين مع بعض", two_sub="اتنين RainBoho · اتنين Ash Starlight · أو واحدة من كل تصميم",
   steps=[("ادخل على tovinest.com", "أو امسح الكود"), ("اختار التصميم", "RainBoho أو Ash Starlight أو الاتنين"), ("اطلب وادفع أونلاين", "والشحن لكل أمريكا")],
   scan="امسح واطلب", sup="خلّي عينك على الأطفال دايماً وهم بيلعبوا."),
}

def frame(L, body):
    t = T[L]
    side = "right" if L == "ar" else "left"
    other = "left" if L == "ar" else "right"
    return f'''<div class="f {L}" lang="{L}"><div class="paper"></div>{stripe(True)}
<img src="../img/logo.png" style="position:absolute;{side}:60px;top:40px;height:100px">
<span class="tag" style="position:absolute;{other}:60px;top:66px;font-size:{17 if L=='en' else 21}px;padding:9px 18px">{t["ship"]}</span>
{body}{stripe(False)}</div>'''

def price_line(L, size=64):
    t = T[L]
    return (f'<div style="display:flex;align-items:baseline;gap:14px;justify-content:center">'
            f'<span class="pr" style="font-size:{size}px">$49.99</span>'
            f'<span style="font-size:{size*.4:.0f}px;font-weight:800;color:#A0907F">{t["was"]} <s class="ltr">$79.99</s></span></div>')

def hero(L):
    t = T[L]
    return frame(L, f'''
<div style="position:absolute;left:60px;right:60px;top:170px;text-align:center">
 <div class="eyebrow" style="font-size:{18 if L=='en' else 24}px">{t["h_eyebrow"]}</div>
 <h1 class="ttl" style="font-size:{78 if L=='en' else 72}px;margin-top:8px">{t["h_title"]}</h1>
 <div style="font-size:26px;font-weight:700;color:#6B5A4B;margin-top:10px">{t["h_sub"]}</div>
</div>
<div class="card" style="left:120px;top:500px;width:420px;height:330px;transform:rotate(-4deg)"><img src="../img/flatlay-rainboho.jpg"><span class="lbl">RainBoho</span></div>
<div class="card" style="left:540px;top:480px;width:420px;height:330px;transform:rotate(3.5deg)"><img src="../img/flatlay-ash-starlight.jpg"><span class="lbl">Ash Starlight</span></div>
<img class="char" src="../img/dino.png" style="left:10px;top:660px;width:160px">
<img class="char" src="../img/dima.png" style="right:14px;top:670px;width:142px">
<div style="position:absolute;left:0;right:0;top:880px;text-align:center">{price_line(L, 66)}
 <div style="font-size:26px;font-weight:800;margin-top:4px">{t["shop"]} <span class="ltr" style="color:#C2573B">tovinest.com</span></div></div>''')

def design(L, key):
    t = T[L]
    name, img, sub, ch = ("RainBoho", "flatlay-rainboho.jpg", t["rb_sub"], "dino") if key == "rb" else ("Ash Starlight", "flatlay-ash-starlight.jpg", t["as_sub"], "dima")
    chips = "".join(f'<span class="chip">{c}</span>' for c in t["chips"])
    cside = ("left:20px" if L == "en" else "right:20px") if ch == "dino" else ("right:20px" if L == "en" else "left:20px")
    return frame(L, f'''
<div style="position:absolute;left:60px;right:60px;top:165px;text-align:center">
 <div class="eyebrow" style="font-size:{18 if L=='en' else 24}px">{t["design"]}</div>
 <h1 class="ttl ltr" style="font-size:86px;font-family:Fredoka,sans-serif;font-weight:600">{name}</h1>
 <div style="font-size:26px;font-weight:700;color:#6B5A4B;margin-top:2px">{sub}</div>
</div>
<div class="card" style="left:170px;top:380px;width:740px;height:440px;transform:rotate(-2deg)"><img src="../img/{img}"></div>
<img class="char" src="../img/{ch}.png" style="{cside};top:600px;width:{170 if ch=='dino' else 150}px">
<div style="position:absolute;left:50px;right:50px;top:855px;display:flex;flex-wrap:wrap;gap:10px;justify-content:center">{chips}</div>
<div style="position:absolute;left:0;right:0;bottom:30px;text-align:center;font-size:24px;font-weight:800">
 <span class="pr" style="font-size:30px">$49.99</span> · {t["shop"]} <span class="ltr" style="color:#C2573B">tovinest.com</span></div>''')

def order(L):
    t = T[L]
    steps = "".join(f'''<div style="display:flex;gap:16px;align-items:flex-start"><b style="flex:none;width:50px;height:50px;border-radius:50%;background:#C2573B;color:#fff;
 display:grid;place-items:center;font-family:Fredoka,sans-serif;font-weight:600;font-size:27px">{i+1}</b><div><div class="disp" style="font-size:{30 if L=='en' else 30}px;line-height:1.2">{a}</div>
 <div style="font-size:21px;font-weight:600;color:#6B5A4B">{b}</div></div></div>''' for i, (a, b) in enumerate(t["steps"]))
    return frame(L, f'''
<div style="position:absolute;left:60px;right:60px;top:180px;display:grid;grid-template-columns:1fr 1fr;gap:18px">
 <div style="background:#fff;border-radius:30px;padding:24px 28px;box-shadow:0 18px 40px -28px rgba(59,42,28,.5)">
  <div class="eyebrow" style="font-size:{17 if L=='en' else 22}px;color:#4E6444">{t["one"]}</div>
  <div style="display:flex;align-items:baseline;gap:12px;margin-top:4px"><span class="pr" style="font-size:70px">$49.99</span>
   <span style="font-size:24px;font-weight:800;color:#A0907F">{t["was"]} <s class="ltr">$79.99</s></span></div>
  <div style="font-size:20px;font-weight:700;color:#6B5A4B">RainBoho · Ash Starlight</div></div>
 <div style="background:#4E6444;color:#FBF4EA;border-radius:30px;padding:24px 28px">
  <div class="eyebrow" style="font-size:{17 if L=='en' else 22}px;color:#F3C66B">{t["two"]}</div>
  <div class="pr" style="font-size:70px;margin-top:4px">$89.99</div>
  <div style="font-size:19px;font-weight:700;color:#DCE5D3;line-height:1.35">{t["two_sub"]}</div></div>
</div>
<div style="position:absolute;left:60px;right:60px;top:470px;background:#fff;border-radius:34px;padding:34px 36px;display:flex;gap:30px;align-items:center;
 box-shadow:0 26px 50px -30px rgba(59,42,28,.5)">
 <div style="flex:1;display:flex;flex-direction:column;gap:20px"><div class="disp" style="font-size:44px">{t["o_title"]}</div>{steps}</div>
 <div style="flex:none;text-align:center"><div style="width:250px;height:250px;padding:16px;border-radius:26px;background:#FBF4EA;border:4px solid #E9B041">{QR}</div>
  <div style="font-weight:900;font-size:{18 if L=='en' else 22}px;letter-spacing:{'.12em' if L=='en' else '0'};text-transform:uppercase;color:#C2573B;margin-top:10px">{t["scan"]}</div></div>
</div>
<img class="char" src="../img/dino.png" style="{'right' if L=='en' else 'left'}:40px;top:880px;width:120px;z-index:3">
<div style="position:absolute;left:60px;right:60px;bottom:40px;font-size:18px;font-weight:700;color:#8C7A6B;text-align:{'left' if L=='en' else 'right'}">{t["sup"]}</div>''')

PAGES = [("1-hero", hero), ("2-rainboho", lambda L: design(L, "rb")), ("3-ash-starlight", lambda L: design(L, "as")), ("4-how-to-order", order)]

if __name__ == "__main__":
    css = CSS + EXTRA
    jobs = [j for j in json.load(open(os.path.join(BUILD, "jobs.json"))) if "social-" not in j["name"]]
    for L in ("en", "ar"):
        for name, fn in PAGES:
            p = os.path.join(BUILD, f"social-{L}-{name}.html")
            open(p, "w").write(f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{fn(L)}</body></html>')
            jobs.append({"html": p, "name": f"tovinest-social-{L}-{name}", "w": 1080, "h": 1080})
    json.dump(jobs, open(os.path.join(BUILD, "jobs.json"), "w"), indent=1)
    print("ok")
