"""03 · Dino crawl test  ->  /workspace/content-v2/posts/03/03_dino_crawl_test.mp4 (+ cover.jpg)

Safe-zone rebuild (this was the worst reel):
  * captions were at y=1720 (fully under the IG caption bar / TikTok UI): now in the 1080-1340 band
    via vlib.draw_caption, grouped by clause and held >= 1.5 s;
  * "Dino tested it all!" stamp (was y=1450, over the caption and in the bottom UI) is now stamped
    over the milestone checklist (y~540) where it reads as a sign-off;
  * thickness card (was y 1180-1600) and "0.5 in · 1.2 cm thick" (was y=1440) moved to y 640-1040;
  * "Wipe clean · Waterproof" stamp moved to the upper safe area and re-timed (holds 1.6 s);
  * "APPROVED BY DINO" now starts at 10.6 s (holds 1.6 s); the tada Dino and the crawling Dino are
    clamped inside the safe box (feet <= y 1400, never off-screen);
  * endcard: DM CTA in the 1258-1344 band, captions continue in the endcard slot; AI label inside the box.

  python3 v03.py              render + mux + cover
  python3 v03.py 2 5 7.5 10 11.5 13   preview stills -> /tmp/v03_<t>.jpg
"""
from vlib import *
import random
W,H=1080,1920; FPS=30; DUR=14.0
mat=load(f'{B}/assets/mat_rainboho.png'); MW=980; matr=rounded_img(fit_w(mat,MW),16)
MX=(W-MW)//2; MY=300
bgbase=deco_bg(W,H,seed=33); shadow_paste(bgbase,matr,(MX,MY),blur=22)
dcrawl=fit_h(cut('dino_crawl'),300); dtada=fit_h(cut('dino_tada'),460)
G=chunks('vo3_crawl')
END=12.2
APPROVED=10.6
def check(d,cx,cy,r,col):
    d.ellipse((cx-r,cy-r,cx+r,cy+r),fill=col); d.line((cx-r*0.45,cy+r*0.02,cx-r*0.1,cy+r*0.38,cx+r*0.5,cy-r*0.35),fill=WHITE,width=int(r*0.22),joint='curve')
def milestone(im,lab,yy,kk,col):
    """Checklist row: card grows left->right from x=90 (never past x=560+), text at the 56 px floor."""
    kk=min(1.0,max(0.0,kk)); w=int(470*kk)
    if w<20: return
    card(im,(90,yy-48,90+w,yy+48),r=48,alpha=245)
    if kk>0.5:
        d=ImageDraw.Draw(im); f=fred(56,600)
        d.text((150,yy),lab,font=f,fill=BROWN,anchor='lm'); check(d,90+w-55,yy,32,col)
        QA.log('milestone',lab,(90,yy-48,90+w,yy+48))
def frame(t):
    if t<END:
        if t<6.3:
            im=bgbase.copy()
            # Dino crawls across the mat, bottom-right to top-left, inside the safe box
            k=ease_io(min(1,t/6.0))
            x=SAFE[2]-dcrawl.width - k*(SAFE[2]-dcrawl.width-SAFE[0]-20)
            y=SAFE[3]-dcrawl.height - k*560 + bounce(t,12,3.2)
            safe_paste(im,dcrawl,x,y,shadow_y=True)
            for i,(lab,t0,col) in enumerate([('Tummy time',0.3,SAGE),('Crawling',1.3,BLUE),('First steps',2.3,CORAL)]):
                if t>t0: milestone(im,lab,430+i*110,ease_out((t-t0)/0.35),col)
            if t>4.4: stamp(im,'Dino tested it all!',SAFE_CX,540,(t-4.4)/0.3)
        elif t<8.6:
            tt=t-6.3; im=kenburns(bgbase,W,H,tt,2.3,1.0,1.25,dx=0,dy=180)
            # thickness graphic, inside the safe box above the caption band
            k=ease_out(tt/0.4); card(im,(70,640,870,1040),r=40,alpha=245)
            d=ImageDraw.Draw(im)
            sx0,sx1=170,740; sy=800; th=int(110*min(1,k))
            d.rounded_rectangle((sx0,sy,sx1,sy+th),14,fill=(232,226,218),outline=(200,190,180),width=3)
            for i in range(8): d.line((sx0+i*72,sy+3,sx0+i*72+36,sy+3),fill=WHITE,width=4)
            d.line((sx1+40,sy,sx1+40,sy+110),fill=CORAL,width=6); d.line((sx1+25,sy,sx1+55,sy),fill=CORAL,width=6); d.line((sx1+25,sy+110,sx1+55,sy+110),fill=CORAL,width=6)
            safe_text(im,'Soft EVA cushion',fred(58,600),top=670,fill=BROWN,max_lines=1)
            safe_text(im,'0.5 in · 1.2 cm thick',fred(66,600),top=940,fill=CORAL,max_lines=1)
        else:
            tt=t-8.6; im=bgbase.copy()
            random.seed(4); drops=[(random.randint(MX+80,MX+MW-80),random.randint(MY+300,MY+1100)) for _ in range(14)]
            wipe_x=MX-200+ (tt-1.0)/1.6*(MW+400) if tt>1.0 else -9999
            for (x,y) in drops:
                if x<wipe_x: continue
                a=min(1,tt/0.4); ov=Image.new('RGBA',(80,90),(0,0,0,0)); od=ImageDraw.Draw(ov)
                od.ellipse((10,25,70,85),fill=(122,163,189,int(170*a))); od.polygon([(40,0),(14,45),(66,45)],fill=(122,163,189,int(170*a))); od.ellipse((26,40,40,54),fill=(255,255,255,int(200*a)))
                im.alpha_composite(ov,(x-40,y-45))
            if tt>1.0 and wipe_x<MX+MW+200:
                card(im,(wipe_x-120,MY+250,wipe_x+120,MY+1150),r=60,fill=(250,250,250),alpha=235)
            if tt>0.4 and t<APPROVED:                          # 9.0 -> 10.6 s = 1.6 s hold
                stamp(im,'Wipe clean · Waterproof',SAFE_CX,470,(tt-0.4)/0.3,col=BLUE,rot=-6,size=64)
        if t>APPROVED:
            tt=t-APPROVED; ov=Image.new('RGBA',(W,H),(255,244,230,int(200*min(1,tt/0.3)))); im.alpha_composite(ov)
            safe_paste(im,dtada,SAFE_CX-dtada.width/2,SAFE[3]-dtada.height+bounce(tt,25,2),shadow_y=True)
            stamp(im,'APPROVED BY DINO',SAFE_CX,560,tt/0.3,col=SAGE,rot=-8,size=84)
        draw_caption(im,G,t,size=78)
    else:
        tt=t-END; im=deco_bg(W,H,seed=5); endcard(im,tt,0.0,groups=G,caption_t=t)
    ai_label(im)
    return im
if __name__=='__main__':
    import sys,os
    os.makedirs('/workspace/content-v2/posts/03',exist_ok=True)
    if len(sys.argv)>1:
        for t in map(float,sys.argv[1:]): frame(t).convert('RGB').save(f'/tmp/v03_{t}.jpg')
    else:
        v=Video('/tmp/v03_silent.mp4')
        for i in range(int(DUR*FPS)): v.add(frame(i/FPS))
        v.close()
        mux('/tmp/v03_silent.mp4','/workspace/content-v2/posts/03/03_dino_crawl_test.mp4',vo=f'{B}/audio/vo3_crawl.mp3',music=f'{B}/audio/music_upbeat.mp3',music_vol=0.2,vo_delay=0.3)
        make_cover('/workspace/content-v2/posts/03/cover.jpg','Dino crawl test',hero=dcrawl)
