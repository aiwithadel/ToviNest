"""Make the 1080x1920 (9:16) version of every 4:5 slide for TikTok photo mode / Stories.

The 1080x1350 slide is scaled to 860x1075 and placed inside the IG Reels + TikTok text safe box
(x 40-900, y 320-1400), on a soft brand background, so nothing sits under the top bar,
the caption/CTA area at the bottom or the like/share rail on the right.
python3 story.py   (after node render.js)
"""
import glob, os
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..")
SAFE = (40, 320, 900, 1400)

def background():
    bg = Image.new("RGB", (1080, 1920), (255, 244, 230))
    ov = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for (x, y, r, c) in [(60, 120, 520, (233, 166, 161, 95)), (1000, 1800, 600, (122, 143, 106, 80)),
                         (980, 760, 380, (233, 176, 65, 55)), (120, 1700, 360, (122, 163, 189, 55))]:
        d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    bg.paste(ov.filter(ImageFilter.GaussianBlur(120)), (0, 0), ov.filter(ImageFilter.GaussianBlur(120)))
    return bg

def main():
    bg = background()
    sw = SAFE[2] - SAFE[0]
    sh = int(1350 * sw / 1080)                       # 1075
    x0, y0 = SAFE[0], SAFE[1] + (SAFE[3] - SAFE[1] - sh) // 2
    mask = Image.new("L", (sw, sh), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw - 1, sh - 1), 36, fill=255)
    shadow = Image.new("RGBA", (1080, 1920), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle((x0 + 6, y0 + 22, x0 + sw + 6, y0 + sh + 22), 36, fill=(80, 60, 40, 70))
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))
    n = 0
    for f in sorted(glob.glob(os.path.join(OUT, "[A-Z]", "*_1080x1350.png"))):
        slide = Image.open(f).convert("RGB").resize((sw, sh), Image.LANCZOS)
        im = bg.copy().convert("RGBA"); im.alpha_composite(shadow)
        im.paste(slide, (x0, y0), mask)
        im.convert("RGB").save(f.replace("_1080x1350.png", "_1080x1920.png"), optimize=True)
        n += 1
    print(n, "story slides")

if __name__ == "__main__":
    main()
