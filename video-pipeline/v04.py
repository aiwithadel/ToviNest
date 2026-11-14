"""04 · Dino holiday gift  ->  /workspace/content-v2/posts/04/04_dino_holiday_gift.mp4 (+ cover.jpg)

Safe-zone rebuild:
  * hook (was y=240, above the grid crop and stacked on the caption at y=470) is in the 320+ band;
    captions moved to the 1080-1340 band (>= 1.5 s holds);
  * price sticker (was at (850,760) r=150, reaching x~1020 under the like/share rail) is clamped
    inside x <= 900 and shows 2 MATS FOR $89.99;
  * Santa Dino / Dino-with-box scaled to fit with feet <= y 1400 (were at y 1760-1800), entrance
    without overshoot; endcard Santa (was at (40,1520)) is now inside the box;
  * endcard: DM CTA in the CTA band, captions continue in the endcard slot. Note: the VO still says
    "on our TikTok shop", and the burned-in caption transcribes it as spoken.

  python3 v04.py              render + mux + cover
  python3 v04.py 2 7 10.5 13  preview stills -> /tmp/v04_<t>.jpg
"""
from vlib import *
import random
W,H=1080,1920; FPS=30; DUR=14.6
bg=cover(load(f'{B}/ai/bg_xmas_flux.png'),W,H)
santa=fit_h(cut('dino_santa'),700)                                  # fits between the hook and y=1400
dbr=fit_h(cut('dino_box_rainboho'),760); dba=fit_h(cut('dino_box_ash-starlight'),760)
G=chunks('vo4_gift')
END=12.4
def snow(im,t):
    d=ImageDraw.Draw(im); random.seed(7)
    for i in range(40):
        x=(random.randint(0,W)+math.sin(t*0.8+i)*30)%W; y=(random.randint(0,H)+t*(60+random.randint(0,80)))%H; r=random.randint(3,8)
        d.ellipse((x-r,y-r,x+r,y+r),fill=(255,255,255,200))
def grow(img,k):
    """Scale-in without overshoot (k<=1), so the clamped box is never exceeded."""
    k=max(0.05,min(1.0,ease_out(k)))
    return img if k>=1 else scaled(img,k)
def frame(t):
    if t<END:
        im=kenburns(bg,W,H,t,END,1.0,1.06)
        ov=Image.new('RGBA',(W,H),(0,0,0,0)); snow(ov,t); im.alpha_composite(ov)
        if t<6.2:
            s=grow(santa,t/0.7)
            safe_paste(im,s,SAFE_CX-s.width/2,SAFE[3]-s.height+bounce(t,10,1.4),shadow_y=True)
            hook(im,'Baby gift idea from Dino',t,0.1,size=62)
            if t>4.9:
                # sparkle burst = gift opening (decoration, centred on the safe box)
                kk=(t-4.9)/1.3; d=ImageDraw.Draw(im)
                for i in range(12):
                    a=i*math.pi/6; r=100+kk*360; star(d,SAFE_CX+math.cos(a)*r,1000+math.sin(a)*r,26*(1-kk)+4,MUSTARD+(int(255*(1-kk)),))
        else:
            tt=t-6.2
            cur=dbr if tt<2.4 else dba; s=grow(cur,(tt if tt<2.4 else tt-2.4)/0.5)
            safe_paste(im,s,SAFE_CX-s.width/2,SAFE[3]-s.height+bounce(tt,10,1.6),shadow_y=True)
            hook(im,'RainBoho' if tt<2.4 else 'Ash Starlight',tt if tt<2.4 else tt-2.4,0.0,size=72,bg=CORAL if tt<2.4 else BLUE,fg=WHITE)
            if tt>3.6: price_sticker(im,SAFE[2]-150,640,r=145,old='2 MATS FOR',new=PRICE_DUO.replace('2 for ',''),sub='HOLIDAY BUNDLE',rot=8,k=(tt-3.6)/0.3)
        draw_caption(im,G,t,size=78)
    else:
        tt=t-END; im=deco_bg(W,H,seed=21)
        endcard(im,tt,0.0,tag='Merry & cozy from Dino',mascot=santa if tt>0.5 else None,groups=G,caption_t=t)
    ai_label(im)
    return im
if __name__=='__main__':
    import sys,os
    os.makedirs('/workspace/content-v2/posts/04',exist_ok=True)
    if len(sys.argv)>1:
        for t in map(float,sys.argv[1:]): frame(t).convert('RGB').save(f'/tmp/v04_{t}.jpg')
    else:
        v=Video('/tmp/v04_silent.mp4')
        for i in range(int(DUR*FPS)): v.add(frame(i/FPS))
        v.close()
        mux('/tmp/v04_silent.mp4','/workspace/content-v2/posts/04/04_dino_holiday_gift.mp4',vo=f'{B}/audio/vo4_gift.mp3',music=f'{B}/audio/music_holiday.mp3',music_vol=0.25,vo_delay=0.3)
        make_cover('/workspace/content-v2/posts/04/cover.jpg','Baby gift idea from Dino',hero=santa)
