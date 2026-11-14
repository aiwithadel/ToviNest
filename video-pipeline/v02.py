"""02 · Dino's New Nest, Ep. 1  ->  /workspace/content-v2/posts/02/02_dinos_new_nest.mp4 (+ cover.jpg)

Safe-zone rebuild: the whole floor scene is lifted by LIFT px (background, floor quad, tiles,
Dino) so Dino's feet stay inside the safe box (y <= 1400); hook in the 320+ band; captions in the
1080-1340 band; endcard with the DM CTA in the 1258-1344 band and the tada Dino inside the box
(was at (780, 1500), in the IG bottom + right rail).

  python3 v02.py              render + mux + cover
  python3 v02.py 1 4 6 9 14   save preview stills to /tmp/v02_<t>.jpg
"""
from vlib import *
W,H=1080,1920; FPS=30; DUR=16.2
LIFT=330                                    # raise the floor line from ~1720 to ~1390
bg=lift_bg(cover(load(f'{B}/ai/bg_nursery_flux.png'),W,H),LIFT)
mat=load(f'{B}/assets/mat_rainboho.png')
QUAD=[(250,1230-LIFT),(830,1230-LIFT),(1030,1760-LIFT),(50,1760-LIFT)]
matfloor=mat_on_floor(mat,W,H,QUAD)
dstand=fit_h(MASCOT,560); dcrawl=fit_h(cut('dino_crawl'),330); dsleep=fit_h(cut('dino_sleep'),280)
dtada=fit_h(cut('dino_tada'),520)
FLOOR=SAFE[3]-8                             # feet line inside the safe box
G=chunks('vo2_nest')
def tint(im,col,a):
    ov=Image.new('RGBA',im.size,col+(int(255*a),)); m=im.split()[3]; ov.putalpha(m.point(lambda v:int(v*a))); out=im.copy(); out.alpha_composite(ov); return out
def frame(t):
    im=bg.copy()
    if t<12.9:
        # gentle push-in
        im=kenburns(bg,W,H,t,12.9,1.0,1.05)
        if t<3.2:
            x=W/2-dstand.width/2+(1-ease_out(t/0.8))*-600; y=FLOOR-dstand.height+bounce(t,14,1.6)
            safe_paste(im,dstand,x,y,shadow_y=True)                # slides in from the left edge of the safe box
        elif t<5.2:
            tt=t-3.2; shake=math.sin(tt*60)*10*max(0,1-tt/0.6) if tt>0.9 else 0
            x=W/2-dcrawl.width/2+shake; y=FLOOR-dcrawl.height
            safe_paste(im,dcrawl,x,y,shadow_y=True)
            if tt>0.9:
                d=ImageDraw.Draw(im); cx,cy=W/2+250,1300-LIFT; r=70; d.line((cx-r,cy-r,cx+r,cy+r),fill=CORAL,width=22); d.line((cx-r,cy+r,cx+r,cy-r),fill=CORAL,width=22)
        elif t<7.3:
            tt=t-5.2; shiver=math.sin(tt*70)*6
            dd=tint(dcrawl,(150,190,230),0.35 if tt>1.1 else 0)
            x=W/2-dd.width/2+shiver; y=FLOOR-dd.height
            ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)          # cold tiles overlay on floor
            for i in range(6):
                for j in range(4):
                    x0=60+i*165; y0=1450-LIFT+j*120; od.rectangle((x0,y0,x0+160,y0+115),fill=(225,235,242,200),outline=(190,205,215,255),width=3)
            im.alpha_composite(ov)
            safe_paste(im,dd,x,y,shadow_y=True)
            if tt>1.1:
                d=ImageDraw.Draw(im)
                for k in range(7):
                    sx=200+k*110+math.sin(tt*3+k)*20; sy=(tt*260+k*170)%700+900-LIFT; star(d,sx,sy,16,(255,255,255,230),pts=6)
        else:
            tt=t-7.3
            k=ease_out(tt/0.7); mf=matfloor
            if k<1:
                mf=mat_on_floor(mat,W,H,[(x,y+int((1-k)*500)) for x,y in QUAD]); mf=fade(mf,k)
            sh=Image.new('RGBA',(W,H),(0,0,0,0)); ImageDraw.Draw(sh).polygon([(x,y+12) for x,y in QUAD],fill=(80,60,40,70)); sh=sh.filter(ImageFilter.GaussianBlur(14))
            im.alpha_composite(fade(sh,k)); im.alpha_composite(mf)
            if tt<2.6:
                # dino crawls onto the mat (enters at the safe-box edge, never off-screen)
                kk=ease_io(min(1,(tt-0.4)/1.8)); x=-dcrawl.width+kk*(W/2-dcrawl.width/2+dcrawl.width)
                y=1560-LIFT-dcrawl.height+bounce(tt,10,3)
                safe_paste(im,dcrawl,x,y,shadow_y=True)
            else:
                t3=tt-2.6
                x,y=safe_paste(im,dsleep,W/2-dsleep.width/2,1560-LIFT-dsleep.height,shadow_y=True)
                d=ImageDraw.Draw(im)
                for k2 in range(3):
                    p=(t3*0.8+k2/3)%1; zx=x+dsleep.width*0.25-p*60+k2*10; zy=y-20-p*220
                    d.text((zx,zy),'z',font=fred(int(40+p*40),600),fill=BLUE+(int(255*(1-p)),),anchor='mm')
        hook(im,"Dino's New Nest  ·  Ep. 1",t+1,0.2,size=64)
        draw_caption(im,G,t,size=82)
    else:
        tt=t-12.9; im=deco_bg(W,H,seed=3)
        endcard(im,tt,0.0,price=False,line2='Follow for episode 2',mascot=dtada if tt>0.6 else None,groups=G,caption_t=t)
    if t<0.25: im=Image.blend(Image.new('RGB',(W,H),CREAM),im.convert('RGB'),t/0.25).convert('RGBA')
    ai_label(im)
    return im
if __name__=='__main__':
    import sys,os
    os.makedirs('/workspace/content-v2/posts/02',exist_ok=True)
    if len(sys.argv)>1:
        for t in map(float,sys.argv[1:]): frame(t).convert('RGB').save(f'/tmp/v02_{t}.jpg')
    else:
        v=Video('/tmp/v02_silent.mp4')
        for i in range(int(DUR*FPS)): v.add(frame(i/FPS))
        v.close()
        mux('/tmp/v02_silent.mp4','/workspace/content-v2/posts/02/02_dinos_new_nest.mp4',vo=f'{B}/audio/vo2_nest.mp3',music=f'{B}/audio/music_upbeat.mp3',music_vol=0.16,vo_delay=0.3)
        make_cover('/workspace/content-v2/posts/02/cover.jpg',"Dino's New Nest · Ep. 1",hero=fit_h(MASCOT,420))
