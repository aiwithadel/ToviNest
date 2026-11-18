"""Email-ready copies: 1200 px wide JPEG (shows crisp at 600 px in the email body), kept small."""
import glob, os
from PIL import Image
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
for f in sorted(glob.glob(os.path.join(OUT, "*@2x.png"))):
    im = Image.open(f).convert("RGB")
    tw = 1500 if "b2b-" in f else (1080 if ("social-" in f or "feature-" in f) else 1200)
    e = im.resize((tw, round(im.height * tw / im.width)), Image.LANCZOS)
    dst = f.replace("@2x.png", "-share.jpg" if ("community" in f or "social-" in f or "feature-" in f) else "-email.jpg")
    e.save(dst, quality=86, optimize=True, progressive=True)
    print(os.path.basename(dst), e.size, os.path.getsize(dst) // 1024, "KB")
