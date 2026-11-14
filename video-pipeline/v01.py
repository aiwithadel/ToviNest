"""01 · Dino got a delivery  ->  /workspace/content-v2/posts/01/01_dino_got_a_delivery.mp4 (+ cover.jpg)

Safe-zone rebuild: hooks in the 320-520 band, feature chips under the hook (no longer colliding with
captions), captions in the 1080-1340 band and continued on the endcard, crawling Dino clamped
inside the safe box, endcard CTA in the 1258-1344 band, AI label inside the safe box.

  python3 v01.py              render + mux + cover
  python3 v01.py 2.0 6.5 13   save preview stills to /tmp/v01_<t>.jpg
"""
from vlib import *
import cv2, json
W,H=1080,1920; FPS=30; DUR=15.6
cap=cv2.VideoCapture(f'{B}/ai/seedance_dino_box.mp4'); SD=[]
while True:
    ok,f=cap.read()
    if not ok: break
    SD.append(f)
TR=json.load(open(f'{B}/ai/box_track.json'))
C=np.array([c if c else TR[i-1] for i,c in enumerate(TR)],float)
Cs=np.copy(C)
for i in range(len(C)):
    lo,hi=max(0,i-3),min(len(C),i+4); Cs[i]=C[lo:hi].mean(0)
BOX=cv2.imread(f'{B}/assets/boxfront_rainboho.png')
BOX=cv2.convertScaleAbs(BOX,alpha=1.06,beta=8)
sc=W/480
def sd_frame(t):
    i=min(len(SD)-1,int(t*24)); f=SD[i]
    up=cv2.resize(f,(W,int(854*sc)),interpolation=cv2.INTER_CUBIC)
    up=cv2.addWeighted(up,1.5,cv2.GaussianBlur(up,(0,0),2.0),-0.5,0)
    dst=np.float32(Cs[i]*sc); src=np.float32([[0,0],[BOX.shape[1],0],[BOX.shape[1],BOX.shape[0]],[0,BOX.shape[0]]])
    M=cv2.getPerspectiveTransform(src,dst)
    warped=cv2.warpPerspective(BOX,M,(up.shape[1],up.shape[0]),flags=cv2.INTER_AREA)
    mask=cv2.warpPerspective(np.full(BOX.shape[:2],255,np.uint8),M,(up.shape[1],up.shape[0]))
    mask=cv2.erode(mask,np.ones((3,3),np.uint8)); mask=cv2.GaussianBlur(mask,(0,0),1.2).astype(float)[...,None]/255
    # keep paws (green) on top
    hsv=cv2.cvtColor(up,cv2.COLOR_BGR2HSV); green=((hsv[...,0]>25)&(hsv[...,0]<55)&(hsv[...,1]>45)).astype(np.uint8)*255
    green=cv2.GaussianBlur(cv2.dilate(green,np.ones((3,3),np.uint8)),(0,0),1.5).astype(float)[...,None]/255
    m=mask*(1-green)
    out=(up*(1-m)+warped*m).astype(np.uint8)
    im=Image.fromarray(cv2.cvtColor(out,cv2.COLOR_BGR2RGB)).convert('RGBA')
    return cover(im,W,H)
G=chunks('vo1_box')
mat=load(f'{B}/assets/mat_rainboho.png'); matr=rounded_img(fit_w(mat,640),14)
boxf=rounded_img(fit_w(load(f'{B}/assets/boxfront_rainboho.png'),700),20)
life=load('/workspace/playmat/final/rainboho-2-lifestyle.png'); dcrawl=fit_h(cut('dino_crawl'),300)
bg2=deco_bg(W,H,seed=11)
END=12.4
def frame(t):
    if t<5.0:
        im=sd_frame(t); hook(im,'Guess what Dino just got?',t,0.15)
    elif t<9.2:
        tt=t-5.0; im=bg2.copy()
        k=ease_out(tt/0.9); my=int(1150-k*470)                       # mat lands at y=680, under the chips
        shadow_paste(im,matr,((W-matr.width)//2,my),blur=20)
        shadow_paste(im,boxf,((W-boxf.width)//2,1180),blur=18)
        hook(im,'Moon Walkers Premium Playmat',tt,0.0,size=54,bg=SAGE,fg=WHITE)
        # 2x2 chips under the hook, inside the safe box; re-timed so the last one still holds >= 1.5 s
        items=[('16 soft tiles',SAGE,0.05),('0.5 in thick',CORAL,0.6),('Non-toxic',MUSTARD,1.2),('Waterproof',BLUE,1.8)]
        for i,(lab,c,t0) in enumerate(items):
            chip(im,[SAFE_CX-215,SAFE_CX+215][i%2],[505,605][i//2],lab,c,tt,t0,size=48)
    elif t<END:
        tt=t-9.2; im=kenburns(life,W,H,tt,3.2,1.0,1.08)
        x=SAFE[2]-dcrawl.width-ease_out(tt/1.5)*120; y=SAFE[3]-dcrawl.height+bounce(tt,10,3)   # feet on the safe-box floor
        safe_paste(im,dcrawl,x,y,shadow_y=True)
        hook(im,'RainBoho design',tt,0.1,size=58)
    else:
        tt=t-END; im=deco_bg(W,H,seed=12); endcard(im,tt,0.0,groups=G,caption_t=t)
    if t<END: draw_caption(im,G,t,size=78)
    ai_label(im)
    return im
if __name__=='__main__':
    import sys,os
    os.makedirs('/workspace/content-v2/posts/01',exist_ok=True)
    if len(sys.argv)>1:
        for t in map(float,sys.argv[1:]): frame(t).convert('RGB').save(f'/tmp/v01_{t}.jpg')
    else:
        v=Video('/tmp/v01_silent.mp4')
        for i in range(int(DUR*FPS)): v.add(frame(i/FPS))
        v.close()
        mux('/tmp/v01_silent.mp4','/workspace/content-v2/posts/01/01_dino_got_a_delivery.mp4',vo=f'{B}/audio/vo1_box.mp3',music=f'{B}/audio/music_upbeat.mp3',music_vol=0.2,vo_delay=0.3)
        make_cover('/workspace/content-v2/posts/01/cover.jpg','Guess what Dino just got?',hero=boxf)
