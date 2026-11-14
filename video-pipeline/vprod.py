"""Product slideshows 09 (Ash Starlight showcase) and 10 (RainBoho POV), music only.

  09 -> /workspace/content-v2/posts/09/09_ash_starlight_showcase.mp4 (+ cover.jpg)
  10 -> /workspace/content-v2/posts/10/10_rainboho_pov.mp4          (+ cover.jpg)

Safe-zone rebuild:
  * hooks (were y=260/300, often 2 lines, banner top inside the IG top UI / above the grid crop)
    go through vlib.hook: top band 320+, wrapped to <= 2 lines, auto-shrunk;
  * 'card' photos are fitted into the safe box below the hook (were centred on the full frame,
    up to 1250 px tall, running under the bottom UI);
  * every scene holds >= 2.2 s, so each hook holds >= 1.5 s; endcard CTA in the 1258-1344 band;
  * AI label inside the safe box (the lifestyle renders are AI-generated).

  python3 vprod.py 09
  python3 vprod.py 10
  python3 vprod.py 09 1.5 4 13    preview stills -> /tmp/09_<t>.jpg
"""
from vlib import *
import sys, os
W,H=1080,1920; FPS=30
CARD_TOP=500                                   # below a 2-line hook
def slide_photo(path,t,dur,z0=1.0,z1=1.1,dy=0,frame_style='full'):
    img=load(path)
    if frame_style=='full': return kenburns(img,W,H,t,dur,z0,z1,dy=dy)
    im=deco_bg(W,H,seed=hash(path)%100)
    k=ease_io(t/dur); s=z0+(z1-z0)*k
    box_w,box_h=SAFE_W-20,SAFE[3]-CARD_TOP-10           # 840 x 890 max (at s=1.0)
    ph=fit_w(img,int(box_w*min(1,s)))
    if ph.height>box_h*min(1,s): ph=fit_h(img,int(box_h*min(1,s)))
    ph=rounded_img(ph,40)
    x=SAFE_CX-ph.width//2; y=CARD_TOP+(box_h-ph.height)//2
    shadow_paste(im,ph,(x,y),blur=20); return im
def build(post,fname,scenes,music,end_tag,dur_end=3.0,preview=None):
    total=sum(s[1] for s in scenes)+dur_end
    def frame(t):
        acc=0
        for i,(path,d,cap,style,kw) in enumerate(scenes):
            if t<acc+d:
                tt=t-acc; im=slide_photo(path,tt,d,frame_style=style,**kw)
                if i>0 and tt<0.35:
                    pp,pd,pc,ps,pk=scenes[i-1]; prev=slide_photo(pp,pd-0.01,pd,frame_style=ps,**pk)
                    im=xfade(prev,im,tt/0.35)
                if cap: hook(im,cap,tt,0.15,size=78)
                ai_label(im)
                return im
            acc+=d
        tt=t-acc; im=deco_bg(W,H,seed=4); endcard(im,tt,0.0,tag=end_tag); ai_label(im); return im
    if preview:
        for t in preview: frame(t).convert('RGB').save(f'/tmp/{post}_{t}.jpg')
        return frame
    v=Video(f'/tmp/{post}_silent.mp4')
    for i in range(int(total*FPS)): v.add(frame(i/FPS))
    v.close()
    os.makedirs(f'/workspace/content-v2/posts/{post}',exist_ok=True)
    mux(f'/tmp/{post}_silent.mp4',f'/workspace/content-v2/posts/{post}/{fname}',music=music,music_vol=0.85)
    first=scenes[0]
    make_cover(f'/workspace/content-v2/posts/{post}/cover.jpg',first[2],hero=load(first[0]))
    return frame
P='/workspace/playmat/final'; T='/workspace/tiktok-upload'
def p09(preview=None):
    sc=[(f'{T}/packaging-ash-starlight.jpg',2.4,'Unboxing: Ash Starlight','card',{}),
        (f'{B}/assets/mat_ash-starlight.png',2.4,'16 tiles · 5.6 × 4 ft','card',{'z0':0.92,'z1':1.0}),
        (f'{P}/ash-starlight-2-lifestyle.png',2.6,'Fits right into the living room','full',{}),
        (f'{P}/ash-starlight-5-toddler.png',2.6,'0.5 in of soft EVA cushion','full',{}),
        (f'{P}/ash-starlight-3-dimensions.png',2.2,'67 × 48 in play space','card',{'z0':0.95,'z1':1.0})]
    return build('09','09_ash_starlight_showcase.mp4',sc,f'{B}/audio/music_upbeat.mp3','Soft. Secure. Cozy.',preview=preview)
def p10(preview=None):
    sc=[('/workspace/brand/IMG_6269.jpeg',2.2,'POV: the playmat finally arrived','full',{}),
        (f'{T}/packaging-rainboho.jpg',2.2,'RainBoho design','card',{}),
        (f'{B}/assets/mat_rainboho.png',2.4,'Rainbows, moons & baby dinos','card',{'z0':0.92,'z1':1.0}),
        (f'{P}/rainboho-2-lifestyle.png',2.6,'Looks like decor, not gym foam','full',{}),
        (f'{P}/rainboho-5-toddler.png',2.6,'Wipe clean · waterproof','full',{})]
    return build('10','10_rainboho_pov.mp4',sc,f'{B}/audio/music_upbeat.mp3','Little explorer. Big heart.',preview=preview)
if __name__=='__main__':
    pv=[float(x) for x in sys.argv[2:]] or None
    {'09':p09,'10':p10}[sys.argv[1]](pv)
