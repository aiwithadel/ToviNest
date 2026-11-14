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
# extra assets for v03 / v04 / vprod
for d in ["/workspace/tiktok-upload", "/workspace/brand", "/workspace/content-v2/posts/dino-falls-01"]:
    os.makedirs(d, exist_ok=True)
Image.new("RGB", (1080, 1920), (186, 64, 58)).save(f"{B}/ai/bg_xmas_flux.png")
mat.save(f"{B}/assets/mat_ash-starlight.png")
for n in ["packaging-ash-starlight", "packaging-rainboho"]:
    box.convert("RGB").save(f"/workspace/tiktok-upload/{n}.jpg")
for n in ["ash-starlight-2-lifestyle", "ash-starlight-5-toddler", "ash-starlight-3-dimensions", "rainboho-5-toddler"]:
    life.save(f"/workspace/playmat/final/{n}.png")
Image.open(f"{BA}/carousels/_src/img/box-rainboho.jpg").save("/workspace/brand/IMG_6269.jpeg")
VO3 = ("Tummy time, crawling, big wobbly first steps, Dino tested it all. Half an inch of soft EVA, "
       "wipe clean and waterproof. Approved by Dino.")
VO4 = "Looking for a baby gift? Dino picked the playmat. RainBoho or Ash Starlight, two mats for eighty nine ninety nine, on our TikTok shop."
w = json.load(open(f"{B}/audio/words.json")); w.update({"vo3_crawl": words(VO3, .4, .36), "vo4_gift": words(VO4, .3, .38)})
json.dump(w, open(f"{B}/audio/words.json", "w"))
for n, dur in [("vo3_crawl", 12), ("vo4_gift", 13)]:
    subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"sine=f=220:d={dur}", "-af", "volume=0.05", f"{B}/audio/{n}.mp3"])
subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-i", f"{B}/audio/music_upbeat.mp3", f"{B}/audio/music_holiday.mp3"])
# dino-falls inputs: 4 stills, a packshot and an 8-row calendar
DF = "/workspace/content-v2/posts/dino-falls-01"
for i, n in enumerate(["01_wobble", "02_tumble", "03_laugh", "04_situp"]):
    Image.open(f"{BA}/carousels/{'ABCD'[i]}/{'ABCD'[i]}01-cover_1080x1920.png").convert("RGB").save(f"{DF}/{n}_9x16.jpg")
box.save(f"{DF}/05_packshot_box_9x16.png")
with open("/workspace/content-v2/calendar.csv", "w") as f:
    f.write("date,time,platform,format,concept,caption,asset_path_or_to_generate\n")
    for d, t in [("2026-11-14", "19:00"), ("2026-11-16", "19:00"), ("2026-11-21", "19:00"), ("2026-11-23", "19:00"),
                 ("2026-11-26", "13:00"), ("2026-12-06", "19:00"), ("2026-12-11", "13:00"), ("2026-12-20", "19:00")]:
        f.write(f"{d},{t},x,x,x,x,x\n")
env = dict(os.environ, PYTHONPATH=f"{HERE}/mock:{VP}", TOVI_FREDOKA=f"{HERE}/fonts/Fredoka-600.ttf",
           TOVI_NUNITO=f"{HERE}/fonts/Nunito-700.ttf", TOVI_LOGO=f"{BA}/tovinest-primary-logo.png")
ONLY = sys.argv[1:]                     # e.g. python3 tests/run_mock.py v03 dino
JOBS = [("v01", ["v01.py"], "/workspace/content-v2/posts/01/01_dino_got_a_delivery.mp4"),
        ("v02", ["v02.py"], "/workspace/content-v2/posts/02/02_dinos_new_nest.mp4"),
        ("v03", ["v03.py"], "/workspace/content-v2/posts/03/03_dino_crawl_test.mp4"),
        ("v04", ["v04.py"], "/workspace/content-v2/posts/04/04_dino_holiday_gift.mp4"),
        ("p09", ["vprod.py", "09"], "/workspace/content-v2/posts/09/09_ash_starlight_showcase.mp4"),
        ("p10", ["vprod.py", "10"], "/workspace/content-v2/posts/10/10_rainboho_pov.mp4"),
        ("dino", ["build_dino_falls.py"], f"{DF}/dino_tumbles_ep01_9x16.mp4")]
for name, cmd, out in JOBS:
    if ONLY and name not in ONLY:
        continue
    print("==", name); subprocess.check_call([sys.executable, f"{VP}/{cmd[0]}"] + cmd[1:], env=env, cwd=VP)
    subprocess.check_call([sys.executable, f"{VP}/qa_contact.py", out, "--out", f"/tmp/tovimock/_qa/{name}"], env=env)
