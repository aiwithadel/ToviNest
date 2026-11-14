"""Safe-zone contact sheet for any 9:16 video.

Extracts one frame per second, draws the text safe box (red, x 40-900 / y 320-1400), the
IG grid crop (blue dashed, 1080x1350 at y 285-1635) and the IG/TikTok UI no-go zones (shaded),
and tiles them into <out>/contact-sheet.png (+ contact-sheet-raw.png without overlays).
If <video>.qa.json or /tmp/<name>_silent.mp4.qa.json from vlib exists, its summary is printed too.

  python3 qa_contact.py /workspace/content-v2/posts/01/01_dino_got_a_delivery.mp4 [--out _qa/01]
"""
import argparse, json, os, subprocess, tempfile, glob
from PIL import Image, ImageDraw

SAFE = (40, 320, 900, 1400)
GRID = (0, 285, 1080, 1635)
NO_GO = [(0, 0, 1080, 220), (0, 1500, 1080, 1920), (940, 0, 1080, 1920)]   # IG top/bottom, right rail (union w/ TikTok)

def frames(video, tmp):
    subprocess.check_call(["ffmpeg", "-v", "error", "-i", video, "-vf", "fps=1,scale=1080:1920", f"{tmp}/f_%03d.png"])
    return sorted(glob.glob(f"{tmp}/f_*.png"))

def overlay(im):
    im = im.convert("RGBA")
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for b in NO_GO:
        d.rectangle(b, fill=(255, 0, 0, 40))
    for i in range(GRID[0], GRID[2], 40):
        d.line((i, GRID[1], i + 20, GRID[1]), fill=(0, 90, 255, 230), width=5)
        d.line((i, GRID[3], i + 20, GRID[3]), fill=(0, 90, 255, 230), width=5)
    d.rectangle(SAFE, outline=(255, 0, 0, 255), width=6)
    im.alpha_composite(ov)
    return im.convert("RGB")

def sheet(paths, out, ov, cols=6, w=270):
    h = int(w * 1920 / 1080)
    rows = (len(paths) + cols - 1) // cols
    c = Image.new("RGB", (cols * w, rows * (h + 26)), "#1d1d1d"); d = ImageDraw.Draw(c)
    for i, p in enumerate(paths):
        im = Image.open(p)
        im = (overlay(im) if ov else im.convert("RGB")).resize((w, h))
        x, y = (i % cols) * w, (i // cols) * (h + 26)
        c.paste(im, (x, y + 26)); d.text((x + 8, y + 6), f"{i}s", fill="white")
    c.save(out)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--out", default=None)
    a = ap.parse_args()
    out = a.out or os.path.join(os.path.dirname(os.path.abspath(a.video)), "_qa")
    os.makedirs(out, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        ps = frames(a.video, tmp)
        sheet(ps, f"{out}/contact-sheet.png", True)
        sheet(ps, f"{out}/contact-sheet-raw.png", False)
    print("wrote", f"{out}/contact-sheet.png", f"{out}/contact-sheet-raw.png")
    name = os.path.basename(a.video)
    for q in [a.video + ".qa.json"] + glob.glob(f"/tmp/*{name.split('_')[0]}*_silent.mp4.qa.json"):
        if os.path.exists(q):
            r = json.load(open(q))
            print(f"{q}: {'PASS' if r['pass'] else 'CHECK'}  out-of-box={len(r['outside_safe_box'])}  "
                  f"short-holds={len(r['short_holds'])}  warnings={len(r['warnings'])}")
