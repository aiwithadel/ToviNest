"""End-to-end test of vlib + v01/v02 against the stand-in lib (tests/mock/lib.py) and generated
placeholder assets. Renders both videos, then runs qa_contact.py on them.
  python3 tests/run_mock.py            (from video-pipeline/)
Needs: ffmpeg, Pillow, numpy, opencv-python-headless, fonts in tests/fonts (see README)."""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__)); VP = os.path.dirname(HERE); REPO = os.path.dirname(VP)
B = os.environ.setdefault("TOVI_B", "/tmp/tovimock")
FONTS = {"Fredoka-600.ttf": "https://fonts.gstatic.com/s/fredoka/v17/X7nP4b87HvSqjb_WIi2yDCRwoQ_k7367_B-i2yQag0-mac3OLyXMFg.ttf",
         "Nunito-400.ttf": "https://fonts.gstatic.com/s/nunito/v32/XRXI3I6Li01BKofiOc5wtlZ2di8HDLshRTM.ttf",
         "Nunito-700.ttf": "https://fonts.gstatic.com/s/nunito/v32/XRXI3I6Li01BKofiOc5wtlZ2di8HDFwmRTM.ttf",
         "Nunito-800.ttf": "https://fonts.gstatic.com/s/nunito/v32/XRXI3I6Li01BKofiOc5wtlZ2di8HDDsmRTM.ttf"}
os.makedirs(f"{HERE}/fonts", exist_ok=True)
for n, u in FONTS.items():                       # OFL fonts, fetched on first run
    if not os.path.exists(f"{HERE}/fonts/{n}"):
        subprocess.check_call(["curl", "-sSL", "-o", f"{HERE}/fonts/{n}", u])
for d in ["assets", "ai", "audio", "/workspace/playmat/final", "/workspace/content-v2/posts"]:
    os.makedirs(d if d.startswith("/") else f"{B}/{d}", exist_ok=True)
BA = f"{REPO}/brand-assets"
Image.open(f"{BA}/tovinest-mascot.png").save(f"{B}/assets/mascot.png")
Image.open(f"{BA}/tovinest-primary-logo.png").save(f"{B}/assets/logo.png")
box = Image.open(f"{BA}/carousels/_src/img/box-rainboho.jpg").convert("RGBA").crop((150, 60, 1360, 1800)); box.save(f"{B}/assets/boxfront_rainboho.png")
mat = Image.open(f"{BA}/carousels/A/A03-assembled-size_1080x1350.png").convert("RGBA").crop((225, 485, 925, 985)); mat.save(f"{B}/assets/mat_rainboho.png")
life = Image.open(f"{BA}/carousels/D/D02-rainboho_1080x1920.png"); life.save("/workspace/playmat/final/rainboho-2-lifestyle.png")
bg = Image.new("RGB", (1080, 1920), (238, 226, 210)); d = ImageDraw.Draw(bg)
d.rectangle((0, 1250, 1080, 1920), fill=(196, 160, 122)); d.rectangle((60, 300, 420, 800), fill=(250, 244, 236)); bg.save(f"{B}/ai/bg_nursery_flux.png")
subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=s=480x854:r=24:d=5.2", f"{B}/ai/seedance_dino_box.mp4"])
json.dump([[[150, 330], [330, 330], [330, 560], [150, 560]]] * 130, open(f"{B}/ai/box_track.json", "w"))
def words(text, start=0.1, rate=0.31):
    out, t = [], start
    for w in text.split():
        out.append([w, round(t, 2), round(t + rate * .85, 2)]); t += rate + (0.25 if w[-1] in ".?!," else 0)
    return out
VO1 = ("Guess what dyno just got? A moonwalkers premium play mat! Sixteen soft tiles, half an inch thick, non -toxic, "
       "and waterproof. The Ranboho design looks like decor, not gym foam. Tap the shop link to get yours.")
VO2 = "Dino needs a new nest. The floor? Too hard. Too cold. Soft, cushy, and just his size. Little explorer. Big heart."
json.dump({"vo1_box": words(VO1), "vo2_nest": words(VO2, .3, .36)}, open(f"{B}/audio/words.json", "w"))
for n, dur in [("vo1_box", 14), ("vo2_nest", 13)]:
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"sine=f=220:d={dur}", "-af", "volume=0.05", f"{B}/audio/{n}.mp3"])
subprocess.check_call([sys.executable, f"{BA}/motion/_src/music.py", "20", f"{B}/audio/music_upbeat.wav"])
subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", f"{B}/audio/music_upbeat.wav", f"{B}/audio/music_upbeat.mp3"])
env = dict(os.environ, PYTHONPATH=f"{HERE}/mock:{VP}")
for s, out in [("v01.py", "/workspace/content-v2/posts/01/01_dino_got_a_delivery.mp4"), ("v02.py", "/workspace/content-v2/posts/02/02_dinos_new_nest.mp4")]:
    print("==", s); subprocess.check_call([sys.executable, f"{VP}/{s}"], env=env, cwd=VP)
    subprocess.check_call([sys.executable, f"{VP}/qa_contact.py", out, "--out", f"/tmp/tovimock/_qa/{s[:3]}"], env=env)
