"""Email-ready copies: 1200 px wide JPEG (shows crisp at 600 px in the email body), kept small."""
import glob, os
from PIL import Image
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
for f in sorted(glob.glob(os.path.join(OUT, "*@2x.png"))):
    im = Image.open(f).convert("RGB")
    e = im.resize((1200, round(im.height * 1200 / im.width)), Image.LANCZOS)
    dst = f.replace("@2x.png", "-email.jpg")
    e.save(dst, quality=86, optimize=True, progressive=True)
    print(os.path.basename(dst), e.size, os.path.getsize(dst) // 1024, "KB")
