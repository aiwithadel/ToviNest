"""Carousels E-L for Tovi Nest (same design system as gen.py A-D).

E gift guide · F every stage · G care guide · H layout ideas · I meet Dino · J FAQ ·
K decor, not gym foam · L why get two. Pricing: $49.99 each · 2 for $89.99. CTA: DM to order.
"""
from gen import (icon, mat_svg, mat3d, mat_flat, dino, page, price_block, cta_block, photo, feat, tile, pills,
                 BOX_RB, BOX_AS, MASCOT)

SUPERVISE = "Always supervise children during play."

def h1(txt, cls="", style=""):
    return f'<h1 class="{cls}" style="{style}">{txt}</h1>'

def big_num(n, col="var(--sage)"):
    return f'<div style="font-family:Fredoka;font-weight:600;font-size:150px;line-height:.9;color:{col}">{n}</div>'

def swatches(cols, size=58):
    return ('<div style="display:flex;gap:12px">' + "".join(
        f'<i style="width:{size}px;height:{size}px;border-radius:50%;background:{c};display:block;border:5px solid #fff;'
        f'box-shadow:0 6px 12px -6px rgba(0,0,0,.3)"></i>' for c in cols) + '</div>')

def qa_card(q, a, col="sage"):
    return (f'<div class="card" style="padding:30px 34px"><div style="display:flex;gap:18px;align-items:flex-start">'
            f'<div class="ico i-{col}" style="width:64px;height:64px;border-radius:20px;font-family:Fredoka;font-weight:600;font-size:34px">Q</div>'
            f'<div><h3 style="font-family:Fredoka;font-weight:600;font-size:40px;line-height:1.1">{q}</h3>'
            f'<p style="font-size:28px;color:var(--muted);font-weight:600;margin-top:10px;line-height:1.35">{a}</p></div></div></div>')

def tile_grid(cells, cols, rows, design="rb", cell=110, gap=8):
    """Layout diagram: `cells` = set of (col,row) that hold a tile."""
    out = []
    for r in range(rows):
        for c in range(cols):
            on = (c, r) in cells
            inner = mat_svg(design, 268, 192, grid=False) if on else ""
            style = ("box-shadow:0 5px 0 #CDBBA6;" if design == "rb" else "box-shadow:0 5px 0 #8E8882;") if on else \
                "border:3px dashed rgba(110,74,43,.18);"
            out.append(f'<div style="width:{cell}px;height:{int(cell*.72)}px;border-radius:8px;overflow:hidden;{style}">{inner}</div>')
    return (f'<div style="display:grid;grid-template-columns:repeat({cols},{cell}px);gap:{gap}px">' + "".join(out) + '</div>')

def center(html):
    return f'<div class="center" style="display:flex;flex-direction:column;align-items:center">{html}</div>'

# ------------------------------------------------------------------ E: gift guide
def E():
    T, tag = 5, "Holiday gift guide"
    s = []
    s.append(("cover", page(1, T, tag, center(f'''
<div class="kicker">Holiday gift guide</div>
{h1('The gift moms<br><em class="c">actually</em> want')}
<div class="sub">Soft, good-looking and used every single day.</div>
<div style="position:relative;width:900px;height:560px;margin-top:40px">
 <div style="position:absolute;left:40px;top:120px;transform:rotate(-5deg)">{mat_flat("rb", 520)}</div>
 <div style="position:absolute;right:60px;top:0">{photo(BOX_RB, 300, 400, 6)}</div>
</div>
{pills([("tag","coral","Black Friday · Nov 27–30"),("gift","sage","Order by Dec 17 for Christmas")])}''')
        + dino(left=-10, bottom=170, w=200, bubble="Gift idea!", bpos="tl", bstyle="left:110px;top:-66px"))))
    s.append(("why-gift", page(2, T, tag, f'''
<div class="kicker">Why it's a great gift</div>
{h1('Useful. Pretty.<br><em>Every day.</em>', 'md')}
<div class="feats" style="margin-top:40px">
 {feat("home","sage","Used every single day","Tummy time, play time, story time")}
 {feat("heart","pink","Looks like decor","Soft boho prints, not loud primary colors")}
 {feat("baby","mustard","Grows with baby","From first head lifts to first steps")}
 {feat("box","coral","Arrives ready to give","In a pretty printed box")}
</div>''')))
    s.append(("who-for", page(3, T, tag, f'''
<div class="kicker">Who it's for</div>
{h1('Perfect for…', 'md')}
<div class="grid2" style="margin-top:40px">
 {tile("baby","sage","New parents","The first thing they'll set up")}
 {tile("gift","pink","Baby showers","A big gift that gets used")}
 {tile("home","sky","Grandma's house","A cozy play spot for visits")}
 {tile("star","mustard","First birthdays","Room to crawl, play &amp; explore")}
</div>''')))
    def date_card(day, mon, title, sub, col):
        return (f'<div class="card" style="display:flex;align-items:center;gap:30px;padding:28px 34px">'
                f'<div style="width:150px;height:150px;border-radius:30px;background:var(--{col});color:#fff;display:flex;flex-direction:column;'
                f'align-items:center;justify-content:center;font-family:Fredoka;font-weight:600;flex:none"><div style="font-size:26px;letter-spacing:2px">{mon}</div>'
                f'<div style="font-size:{64 if len(day) <= 3 else 44}px;line-height:1">{day}</div></div><div><h3 style="font-family:Fredoka;font-weight:600;font-size:42px;line-height:1.1">{title}</h3>'
                f'<p style="font-size:28px;color:var(--muted);font-weight:600;margin-top:8px">{sub}</p></div></div>')
    s.append(("dates", page(4, T, tag, f'''
<div class="kicker">Save the dates</div>
{h1('Holiday <em class="c">timeline</em>', 'md')}
<div style="display:flex;flex-direction:column;gap:22px;margin-top:40px">
 {date_card("27–30", "NOV", "Black Friday – Cyber Monday", "The big gifting weekend", "coral")}
 {date_card("17", "DEC", "Order by Dec 17", "For Christmas delivery", "sage")}
 {date_card("USA", "SHIPS", "Ships across the USA", "Send it straight to the new parents", "sky")}
</div>''')))
    s.append(("shop", page(5, T, tag, center(f'''
{h1('Wrap up a<br><em>soft nest</em>', 'md')}
<div style="margin-top:20px">{mat3d("as", 560)}</div>
<div style="margin-top:30px">{price_block()}</div>
{cta_block("DM to order a gift")}''') + dino(right=-30, top=120, w=170, bubble="Merry!", bpos="tr", bstyle="right:40px;top:-62px"))))
    return s

# ------------------------------------------------------------------ F: every stage
def F():
    T, tag = 5, "Every stage"
    s = []
    s.append(("cover", page(1, T, tag, f'''
<div class="kicker">Grows with your baby</div>
{h1('From tummy time<br>to <em>first steps</em>')}
<div class="sub" style="max-width:640px">One soft, cushioned nest for every little milestone.</div>
{mat3d("rb", 760, mt=50)}''' + dino(right=-10, top=170, w=210, bubble="Every stage!", bpos="tr", bstyle="right:60px;top:-64px"))))
    def stage(n, num, title, sub, ic, col, design, bubble, tags):
        return page(n, T, tag, f'''
<div style="display:flex;align-items:flex-end;gap:24px">{big_num(num, f"var(--{col})")}<div class="kicker" style="margin-bottom:22px">Stage {num}</div></div>
{h1(title, 'md')}
<div class="sub">{sub}</div>
<div style="position:relative;margin-top:40px">{mat_flat(design, 760)}</div>
<div style="margin-top:44px">{pills(tags, center=False)}</div>''' + dino(right=-10, bottom=230, w=190, bubble=bubble, bpos="tr", bstyle="right:40px;top:-64px"))
    s.append(("tummy-time", stage(2, "01", 'Tummy <em>time</em>', "A soft, clean spot for those first head lifts and wiggles.", "baby", "sage", "rb",
                                  "Head up!", [("layers","sage","0.5 in soft EVA"),("drop","sky","Wipe-clean top")])))
    s.append(("crawling", stage(3, "02", '<em class="s">Crawling</em> &amp; rolling', "5.6 × 4 ft of soft, cushioned floor to roam and explore.", "puzzle", "sky", "as",
                                "Zoom zoom!", [("ruler","mustard","67 × 48 in"),("feet","coral","Non-slip surface")])))
    s.append(("first-steps", stage(4, "03", 'First <em class="c">steps</em>', "A soft cushioned landing for wobbly first steps. " + SUPERVISE, "feet", "coral", "rb",
                                   "Wobble…", [("heart","pink","Soft cushioned landing"),("puzzle","sage","Locking tiles")])))
    s.append(("toddler-play", page(5, T, tag, center(f'''
<div class="kicker">Stage 04 · and beyond</div>
{h1('Toddler <em class="m">play zone</em>', 'md')}
<div class="sub">Blocks, books, tea parties. A play corner that wipes clean.</div>
<div style="margin-top:34px">{price_block()}</div>
{cta_block()}'''))))
    return s

# ------------------------------------------------------------------ G: care guide
def G():
    T, tag = 5, "Care guide"
    s = []
    drops = "".join(f'<svg style="position:absolute;left:{x}px;top:{y}px;width:{w}px" viewBox="0 0 24 30"><path fill="rgba(122,163,189,.92)" d="M12 1c4 5.5 9 10.5 9 16a9 9 0 0 1-18 0c0-5.5 5-10.5 9-16z"/><ellipse cx="8.5" cy="17" rx="2" ry="3.4" fill="rgba(255,255,255,.7)"/></svg>'
                    for x, y, w in [(120, 80, 56), (240, 160, 38), (420, 100, 46), (560, 190, 32)])
    s.append(("cover", page(1, T, tag, f'''
<div class="kicker">Care guide</div>
{h1('Spills?<br><em class="s">No stress.</em>')}
<div class="sub">The waterproof top wipes clean in seconds. Here's how.</div>
<div style="position:relative;width:700px;margin:50px auto 0">{mat_flat("rb", 700)}{drops}</div>''')))
    def step(n, num, title, sub, ic, col, items):
        lis = "".join(f'<div style="display:flex;gap:18px;align-items:center;font-size:36px;font-weight:700;color:var(--ink)">'
                      f'<span class="ico i-sage" style="width:60px;height:60px;border-radius:18px">{icon("check", 2.8)}</span>{t}</div>' for t in items)
        return page(n, T, tag, f'''
<div style="display:flex;align-items:flex-end;gap:24px">{big_num(num, f"var(--{col})")}<div class="kicker" style="margin-bottom:22px">Step {num}</div></div>
{h1(title, 'md')}
<div class="sub">{sub}</div>
<div style="display:flex;flex-direction:column;gap:30px;margin-top:50px">
 <div class="ico i-{col}" style="width:100%;height:300px;border-radius:44px">{icon(ic).replace("<svg", '<svg style="width:170px;height:170px"')}</div>
 <div class="card" style="padding:38px 40px;display:flex;flex-direction:column;gap:26px">{lis}</div>
</div>''')
    s.append(("wipe", step(2, "01", "Wipe", "Damp cloth + a drop of mild soap.", "sponge", "sky",
                           ["Juice &amp; milk", "Snack crumbs", "Crayon marks"])))
    s.append(("dry", step(3, "02", "Air dry", "Let it dry and you're back to play. Pop tiles apart to clean the edges.", "sun", "mustard",
                          ["No scrubbing", "Tiles come apart", "Back to play fast"])))
    s.append(("dont", step(4, "03", "Keep it happy", "A few simple don'ts keep your mat looking new.", "heart", "coral",
                           ["No washer or dryer", "Keep away from direct heat", "No sharp toys or scissors"])))
    s.append(("shop", page(5, T, tag, center(f'''
{h1('Easy-care<br><em>every day</em>', 'md')}
<div style="margin-top:20px">{pills([("drop","sky","Waterproof top"),("sponge","sage","Wipe clean"),("puzzle","mustard","16 tiles")])}</div>
<div style="margin-top:36px">{price_block()}</div>
{cta_block()}'''))))
    return s

# ------------------------------------------------------------------ H: layout ideas
def H():
    T, tag = 5, "Layout ideas"
    s = []
    full = {(c, r) for c in range(4) for r in range(4)}
    s.append(("cover", page(1, T, tag, center(f'''
<div class="kicker">Set it up your way</div>
{h1('16 tiles.<br><em>Endless</em> layouts.')}
<div class="sub">Snap the interlocking tiles into the shape your room needs.</div>
<div style="margin-top:50px">{tile_grid(full, 4, 4, "rb", 150, 10)}</div>''') + dino(right=-20, bottom=150, w=200, bubble="Your way!", bpos="tr", bstyle="right:40px;top:-64px"))))
    def layout(n, title, sub, cells, cols, rows, design, chip):
        return page(n, T, tag, center(f'''
<div class="kicker">Layout {n - 1:02d}</div>
{h1(title, 'md')}
<div class="sub">{sub}</div>
<div style="margin-top:50px">{tile_grid(cells, cols, rows, design, 130 if cols <= 6 else 102, 8)}</div>
<div style="margin-top:44px">{pills([chip])}</div>'''))
    s.append(("full", layout(2, 'The full <em>play space</em>', "All 16 tiles: a big 5.6 × 4 ft (67 × 48 in) nest.", full, 4, 4, "rb",
                             ("ruler","sage","67 × 48 in · 16 tiles"))))
    corner = {(c, r) for c in range(3) for r in range(3)} | {(3, 0), (3, 1), (3, 2), (0, 3), (1, 3), (2, 3), (3, 3)}
    nook = {(c, r) for c in range(3) for r in range(3)}
    s.append(("cozy-corner", layout(3, 'A <em class="c">cozy corner</em>', "Just 9 tiles for a reading or tummy-time nook. Keep the rest for later.",
                                    nook, 4, 4, "as", ("home","coral","9-tile nook"))))
    two = {(c, r) for c in range(2) for r in range(4)} | {(c, r) for c in range(4, 6) for r in range(4)}
    s.append(("two-zones", layout(4, 'Two <em class="s">play zones</em>', "8 + 8 tiles: one spot in the nursery, one in the living room.",
                                  two, 6, 4, "rb", ("puzzle","sky","8 + 8 tiles"))))
    s.append(("shop", page(5, T, tag, center(f'''
{h1('Snap. Press.<br><em>Play.</em>', 'md')}
<div style="margin-top:20px">{pills([("puzzle","sage","No tools"),("timer","mustard","Sets up in minutes"),("expand","sky","Rearrange anytime")])}</div>
<div style="margin-top:36px">{price_block()}</div>
{cta_block()}'''))))
    return s

# ------------------------------------------------------------------ I: meet Dino
def I():
    T, tag = 5, "Meet Dino"
    s = []
    s.append(("cover", page(1, T, tag, center(f'''
<div class="kicker">Hi, friend!</div>
{h1('Meet <em>Dino</em>')}
<div class="sub">The little explorer behind Tovi Nest.</div>
<img src="{MASCOT}" style="width:470px;margin-top:30px;filter:drop-shadow(0 26px 30px rgba(80,60,40,.25))">'''))))
    s.append(("story", page(2, T, tag, f'''
<div class="kicker">Our story</div>
{h1('Little explorer.<br><em>Big heart.</em>', 'md')}
<div class="card" style="margin-top:40px;padding:40px 44px;font-size:32px;line-height:1.45;font-weight:600;color:var(--ink)">
 Tovi Nest makes soft, good-looking play spaces for babies and kids, so every little explorer has a cozy place to wiggle,
 crawl and play. <br><br>We're starting with the <b>Moon Walkers Premium EVA Playmat</b>, and more little-explorer
 essentials are on the way.
</div>''' + dino(right=-10, top=90, w=190, bubble="That's me!", bpos="tr", bstyle="right:40px;top:-62px"))))
    s.append(("facts", page(3, T, tag, f'''
<div class="kicker">Dino fun facts</div>
{h1('All about <em>Dino</em>', 'md')}
<div class="feats" style="margin-top:40px">
 {feat("heart","pink","Favorite thing","Tummy time on the RainBoho mat")}
 {feat("star","mustard","Signature look","A cozy orange bandana")}
 {feat("home","sage","Superpower","Turning any floor into a soft nest")}
 {feat("moon","sky","Nap spot","Ash Starlight, under the stars &amp; moons")}
</div>''')))
    bow = ('<svg viewBox="0 0 120 70" style="width:180px"><path d="M60 35 L10 5 Q0 35 10 65 Z" fill="#E9B041"/>'
           '<path d="M60 35 L110 5 Q120 35 110 65 Z" fill="#E9B041"/><circle cx="60" cy="35" r="14" fill="#D49A2B"/></svg>')
    s.append(("new-friend", page(4, T, tag, center(f'''
<div class="kicker">Coming soon</div>
{h1('Dino has a<br><em class="c">new friend</em>…', 'md')}
<div class="sub">Someone pink with a mustard bow is joining the nest.</div>
<div style="position:relative;width:420px;height:420px;margin-top:50px;border-radius:50%;background:#F8E1DE;display:grid;place-items:center;
 box-shadow:0 30px 50px -24px rgba(180,99,92,.5)">
 <div style="font-family:Fredoka;font-weight:600;font-size:220px;color:#E9A6A1;line-height:1">?</div>
 <div style="position:absolute;top:-30px">{bow}</div>
</div>
<div style="margin-top:44px">{pills([("heart","pink","Follow @tovinest to meet her first")])}</div>'''))))
    s.append(("follow", page(5, T, tag, center(f'''
{h1('Join the <em>nest</em>', 'md')}
<div class="sub">Follow <b>@tovinest</b> for Dino's adventures, playtime ideas and new arrivals.</div>
<div style="margin-top:30px">{mat3d("rb", 560)}</div>
<div style="margin-top:24px">{price_block()}</div>
{cta_block()}'''))))
    return s

# ------------------------------------------------------------------ J: FAQ
def J():
    T, tag = 5, "FAQ"
    s = []
    s.append(("cover", page(1, T, tag, f'''
<div class="kicker">FAQ</div>
{h1('Your questions,<br><em>answered</em>')}
<div class="sub" style="max-width:640px">Everything parents ask us about the Moon Walkers playmat.</div>
{mat3d("as", 740, mt=50)}''' + dino(right=-10, top=160, w=210, bubble="Ask away!", bpos="tr", bstyle="right:50px;top:-64px"))))
    s.append(("size", page(2, T, tag, f'''
<div class="kicker">Size</div>
{h1('How big<br>is it?', 'md')}
<div style="display:flex;flex-direction:column;gap:22px;margin-top:40px">
 {qa_card("How big is the mat?", "67 × 48 in (5.6 × 4 ft) when all 16 tiles are snapped together. You can also build smaller shapes.", "sage")}
 {qa_card("How thick is it?", "0.5 in (1.2 cm) of soft EVA foam: a soft cushioned landing for crawling and play.", "sky")}
</div>''')))
    s.append(("care-safety", page(3, T, tag, f'''
<div class="kicker">Care &amp; testing</div>
{h1('Cleaning &amp;<br><em>testing</em>', 'md')}
<div style="display:flex;flex-direction:column;gap:22px;margin-top:40px">
 {qa_card("How do I clean it?", "The top is waterproof: wipe with a damp cloth and mild soap, then air dry.", "sky")}
 {qa_card("Is it tested?", "Yes, it's CPC / CPSIA tested. " + SUPERVISE, "coral")}
</div>''')))
    s.append(("order", page(4, T, tag, f'''
<div class="kicker">Ordering</div>
{h1('Bundles &amp;<br><em>shipping</em>', 'md')}
<div style="display:flex;flex-direction:column;gap:22px;margin-top:40px">
 {qa_card("How does the 2-pack work?", "2 mats for $89.99: Two RainBoho, Two Ash Starlight, or Mix (one of each).", "mustard")}
 {qa_card("Where do you ship?", "Across the USA. Order by Dec 17 for Christmas.", "sage")}
</div>''')))
    s.append(("returns", page(5, T, tag, center(f'''
{qa_card("What if it's not right?", "Unused items can be returned within 30 days of delivery.", "pink")}
<div style="margin-top:30px">{price_block()}</div>
{cta_block("DM us any question")}'''))))
    return s

# ------------------------------------------------------------------ K: decor, not gym foam
def K():
    T, tag = 5, "Style"
    s = []
    s.append(("cover", page(1, T, tag, f'''
<div class="kicker">Style</div>
{h1('Looks like <em>decor</em>,<br>not gym foam')}
<div class="sub">A playmat you'll happily leave out when friends come over.</div>
{mat3d("rb", 780, mt=60)}''')))
    s.append(("palettes", page(2, T, tag, f'''
<div class="kicker">Soft boho prints</div>
{h1('Neutral tones,<br><em>calm</em> rooms', 'md')}
<div class="grid2" style="margin-top:40px">
 <div class="card tile" style="align-items:center;text-align:center">{mat_flat("rb", 340)}<h3 style="color:var(--coral);margin-top:10px">RainBoho</h3>
  {swatches(["#E8D9C6","#C3A386","#D2AE98","#F7F0E7"], 50)}<p>Sand, cream &amp; blush</p></div>
 <div class="card tile" style="align-items:center;text-align:center">{mat_flat("as", 340)}<h3 style="color:var(--sky);margin-top:10px">Ash Starlight</h3>
  {swatches(["#ADA7A0","#8E8882","#E6E1DA","#F4F1EC"], 50)}<p>Ash grey &amp; soft white</p></div>
</div>''')))
    s.append(("room-match", page(3, T, tag, f'''
<div class="kicker">Match your room</div>
{h1('Pick the one that<br><em>fits your home</em>', 'md')}
<div class="feats" style="margin-top:40px">
 {feat("home","coral","Wood, beige &amp; rattan?","RainBoho's warm sand tones blend right in")}
 {feat("moon","sky","Grey, white &amp; modern?","Ash Starlight keeps it calm and dreamy")}
 {feat("heart","pink","Can't choose?","Get both: 2 for $89.99")}
</div>''')))
    rows = [("Colors", "Loud primary colors", "Soft boho neutrals"), ("Size", "Small &amp; patchy", "5.6 × 4 ft"),
            ("Thickness", "Often thin", "0.5 in soft EVA"), ("When guests come", "Hide it", "Leave it out")]
    tr = "".join(f'<div style="display:contents"><div style="padding:18px 0;color:var(--muted);font-weight:800;font-size:26px;border-top:2px dashed var(--line)">{a}</div>'
                 f'<div style="padding:18px 0;font-size:28px;font-weight:700;color:#A99684;border-top:2px dashed var(--line)">{b}</div>'
                 f'<div style="padding:18px 0;font-family:Fredoka;font-weight:600;font-size:30px;color:var(--ink);border-top:2px dashed var(--line)">{c}</div></div>' for a, b, c in rows)
    s.append(("compare", page(4, T, tag, f'''
<div class="kicker">The difference</div>
{h1('Typical foam vs<br><em>Tovi Nest</em>', 'md')}
<div class="card" style="margin-top:40px;padding:30px 36px;display:grid;grid-template-columns:200px 1fr 1fr;column-gap:22px">
 <div></div><div style="font-family:Fredoka;font-weight:600;font-size:32px;color:#A99684;padding-bottom:16px">Typical foam</div>
 <div style="font-family:Fredoka;font-weight:600;font-size:32px;color:var(--sage);padding-bottom:16px">Tovi Nest</div>{tr}
</div>''')))
    s.append(("shop", page(5, T, tag, center(f'''
{h1('Bring home<br>the <em>nest</em>', 'md')}
<div style="display:flex;gap:26px;margin-top:30px"><div style="transform:rotate(-3deg)">{mat_flat("rb", 380)}</div><div style="transform:rotate(3deg)">{mat_flat("as", 380)}</div></div>
<div style="margin-top:36px">{price_block()}</div>
{cta_block()}'''))))
    return s

# ------------------------------------------------------------------ L: why get two
def L():
    T, tag = 5, "2-pack"
    s = []
    badge = ('<div style="width:300px;height:300px;border-radius:50%;background:var(--mustard);color:#fff;display:flex;flex-direction:column;'
             'align-items:center;justify-content:center;font-family:Fredoka;box-shadow:0 26px 40px -16px rgba(169,118,27,.75);border:9px solid #fff">'
             '<div style="font-size:32px;font-weight:500;letter-spacing:3px">2 FOR</div><div style="font-size:84px;font-weight:600;line-height:.95">$89.99</div>'
             '<div style="font-size:24px;font-weight:500">mix &amp; match</div></div>')
    s.append(("cover", page(1, T, tag, center(f'''
<div class="kicker">The 2-pack</div>
{h1('Why parents<br>get <em class="m">two</em>')}
<div style="position:relative;width:900px;height:560px;margin-top:40px">
 <div style="position:absolute;left:10px;top:60px;transform:rotate(-6deg)">{mat_flat("rb", 470)}</div>
 <div style="position:absolute;right:10px;top:120px;transform:rotate(5deg)">{mat_flat("as", 470)}</div>
 <div style="position:absolute;left:50%;top:150px;transform:translateX(-50%) rotate(-5deg)">{badge}</div>
</div>'''))))
    s.append(("two-rooms", page(2, T, tag, f'''
<div class="kicker">Reason 01</div>
{h1('Nursery <em>+</em><br>living room', 'md')}
<div class="sub">Baby plays where you are. No more dragging one mat around the house.</div>
<div class="grid2" style="margin-top:44px">
 {tile("baby","sage","In the nursery","Tummy time &amp; quiet play")}
 {tile("home","coral","In the living room","Play while you cook &amp; chat")}
</div>''' + dino(right=-10, top=90, w=190, bubble="Two nests!", bpos="tr", bstyle="right:40px;top:-62px"))))
    s.append(("grandma", page(3, T, tag, f'''
<div class="kicker">Reason 02</div>
{h1('Grandma&#39;s house<br><em class="c">needs one too</em>', 'md')}
<div class="sub">Keep a soft play spot ready at the grandparents' or the sitter's.</div>
<div style="margin-top:40px">{tile_grid({(c, r) for c in range(4) for r in range(4)}, 4, 4, "as", 150, 10)}</div>''')))
    s.append(("math", page(4, T, tag, center(f'''
<div class="kicker">Reason 03</div>
{h1('The <em>math</em>', 'md')}
<div class="card" style="margin-top:40px;padding:40px 50px;width:820px">
 <div style="display:flex;justify-content:space-between;font-size:34px;font-weight:700;color:var(--muted)"><span>Mat 1</span><span>$49.99</span></div>
 <div style="display:flex;justify-content:space-between;font-size:34px;font-weight:700;color:var(--muted);margin-top:14px"><span>Mat 2</span><span>$49.99</span></div>
 <div style="border-top:3px dashed var(--line);margin:24px 0"></div>
 <div style="display:flex;justify-content:space-between;font-family:Fredoka;font-weight:600;font-size:56px;color:var(--ink)"><span>2-pack</span><span style="color:var(--coral)">$89.99</span></div>
 <div class="pill p-sage" style="margin-top:22px;font-size:32px">{icon("tag")}You save $9.99</div>
</div>
<div style="margin-top:34px">{pills([("rainbow","coral","Two RainBoho"),("moon","sky","Two Ash Starlight"),("heart","pink","Mix")])}</div>'''))))
    s.append(("shop", page(5, T, tag, center(f'''
{h1('Get <em class="m">both</em>', 'md')}
<div style="margin-top:20px">{badge}</div>
<div style="font-size:30px;font-weight:700;color:var(--muted);margin-top:26px">Single mat $49.99</div>
{cta_block("DM to get the 2-pack")}'''))))
    return s

ALL = [("E", E), ("F", F), ("G", G), ("H", H), ("I", I), ("J", J), ("K", K), ("L", L)]
