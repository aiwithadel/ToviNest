"""STAND-IN for the real lib.py (not in this repo). Only for tests/run_mock.py: it provides the
same names vlib/v01/v02 use, with simple implementations and placeholder assets, so the layout
code can be exercised end to end. Do not ship; your real lib.py replaces this."""
import math, os, subprocess, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

B = os.environ.get("TOVI_B", "/tmp/tovimock")
HERE = os.path.dirname(os.path.abspath(__file__))
FONTS = os.path.join(HERE, "..", "fonts")
WHITE, BROWN, CORAL, MUSTARD, SAGE, BLUE, CREAM = (255,255,255), (110,74,43), (224,122,95), (233,176,65), (122,143,106), (122,163,189), (255,244,230)

def fred(size, w=600): return ImageFont.truetype(f"{FONTS}/Fredoka-600.ttf", int(size))
def nun(size, w=700):
    w = 800 if w >= 800 else (700 if w >= 600 else 400)
    return ImageFont.truetype(f"{FONTS}/Nunito-{w}.ttf", int(size))
def load(p): return Image.open(p).convert("RGBA")
def cover(img, W, H):
    s = max(W / img.width, H / img.height); im = img.resize((int(img.width*s)+1, int(img.height*s)+1))
    x, y = (im.width - W)//2, (im.height - H)//2
    return im.crop((x, y, x+W, y+H)).convert("RGBA")
def fit_h(img, h): return img.resize((max(1, int(img.width*h/img.height)), int(h)), Image.LANCZOS)
def fit_w(img, w): return img.resize((int(w), max(1, int(img.height*w/img.width))), Image.LANCZOS)
def rounded_img(img, r):
    m = Image.new("L", img.size, 0); ImageDraw.Draw(m).rounded_rectangle((0,0,img.width-1,img.height-1), r, fill=255)
    out = img.copy(); out.putalpha(m); return out
MASCOT = load(f"{B}/assets/mascot.png")
LOGO = load(f"{B}/assets/logo.png")
def cut(name): return MASCOT.copy()
def deco_bg(W, H, seed=0):
    im = Image.new("RGBA", (W, H), CREAM + (255,)); d = ImageDraw.Draw(im)
    rng = np.random.default_rng(seed)
    for _ in range(6):
        x, y, r = rng.integers(0, W), rng.integers(0, H), rng.integers(120, 300)
        d.ellipse((x-r, y-r, x+r, y+r), fill=(250, 226, 214, 255))
    return im.filter(ImageFilter.GaussianBlur(40))
def shadow_paste(im, layer, xy, blur=12, off=(0, 8), alpha=60):
    x, y = int(xy[0]), int(xy[1])
    sh = Image.new("RGBA", layer.size, (60, 40, 20, 0)); sh.putalpha(layer.split()[3].point(lambda v: v*alpha//255))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)), (max(0, x+off[0]), max(0, y+off[1])))
    im.alpha_composite(layer, (x, y))
def scaled(layer, k): return layer.resize((max(1, int(layer.width*k)), max(1, int(layer.height*k))))
def ground_shadow(im, cx, cy, w, alpha=70):
    sh = Image.new("RGBA", im.size, (0,0,0,0)); ImageDraw.Draw(sh).ellipse((cx-w/2, cy-14, cx+w/2, cy+14), fill=(60,40,20,alpha))
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
def star(d, x, y, r, fill, pts=5): d.ellipse((x-r/3, y-r/3, x+r/3, y+r/3), fill=fill)
def mat_on_floor(mat, W, H, quad):
    xs, ys = [p[0] for p in quad], [p[1] for p in quad]
    out = Image.new("RGBA", (W, H), (0,0,0,0)); m = mat.resize((max(xs)-min(xs), max(1, max(ys)-min(ys))))
    out.alpha_composite(m, (min(xs), min(ys))); return out
def fade(im, k):
    out = im.copy(); out.putalpha(im.split()[3].point(lambda v: int(v*max(0, min(1, k))))); return out
def ease_out(k): k = max(0, min(1, k)); return 1-(1-k)**3
def ease_io(k): k = max(0, min(1, k)); return k*k*(3-2*k)
def ease_out_back(k):
    k = max(0, min(1, k)); c = 1.70158; return 1 + (c+1)*(k-1)**3 + c*(k-1)**2
class Video:
    def __init__(self, path, fps=30):
        self.p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "1080x1920",
                                   "-r", str(fps), "-i", "-", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", path], stdin=subprocess.PIPE)
    def add(self, im): self.p.stdin.write(im.convert("RGB").tobytes())
    def close(self): self.p.stdin.close(); self.p.wait()
def mux(*a, **k): raise RuntimeError("vlib.mux should be used")
