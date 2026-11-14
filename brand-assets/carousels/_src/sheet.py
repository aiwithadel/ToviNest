import sys, glob
from PIL import Image
S='/tmp/claude-0/-home-user-ToviNest/65d7fb13-c96e-52da-84af-d709eb75f4f7/scratchpad/'
for k in sys.argv[1:]:
    fs=sorted(glob.glob(f'{k[0]}/*_{"1080x1920" if k.endswith("s") else "1080x1350"}.png'))
    ims=[Image.open(f) for f in fs]; w=540; h=int(ims[0].height*w/1080)
    cols=3; rows=(len(ims)+cols-1)//cols
    c=Image.new('RGB',(cols*w+(cols-1)*10,rows*h+(rows-1)*10),'#333')
    for i,im in enumerate(ims): c.paste(im.resize((w,h)),((i%cols)*(w+10),(i//cols)*(h+10)))
    c.save(S+f'sheet_{k}.png')
