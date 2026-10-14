# Generates ALL pixel art for Cimavilla 1992 prototype. Closed 32-colour warm muted palette.
from PIL import Image, ImageDraw
import random, json, math, os
OUT=os.path.join(os.path.dirname(__file__),'out'); os.makedirs(OUT,exist_ok=True)
P={'k':(26,20,24),'d1':(43,33,36),'d2':(61,46,45),'br1':(84,60,48),'br2':(112,80,58),'br3':(143,108,78),'br4':(173,138,98),
'sa1':(201,168,124),'sa2':(224,200,158),'cr':(240,226,192),'gr1':(70,66,68),'gr2':(98,94,92),'gr3':(128,122,114),'gr4':(160,150,134),
'rf1':(110,52,42),'rf2':(146,74,54),'rf3':(178,104,72),'oc1':(168,128,70),'oc2':(198,160,96),'gn1':(62,76,60),'gn2':(92,108,82),'gn3':(136,146,108),
'bl1':(40,48,62),'bl2':(64,80,94),'bl3':(104,120,124),'rd':(132,62,54),'or':(214,150,82),'yl':(236,200,122),'sk':(208,158,122),'sk2':(166,114,88),'wh':(248,238,212),'pk':(176,128,116)}
assert len(P)==32
R=random.Random(1992)
def px(im,x,y,c):
    if 0<=x<im.width and 0<=y<im.height: im.putpixel((x,y),P[c]+(255,) if im.mode=='RGBA' else P[c])
def rect(im,x,y,w,h,c):
    for j in range(y,y+h):
        for i in range(x,x+w): px(im,i,j,c)
def hline(im,x,y,w,c): rect(im,x,y,w,1,c)
def vline(im,x,y,h,c): rect(im,x,y,1,h,c)
def noise(im,x,y,w,h,c,p):
    for j in range(y,y+h):
        for i in range(x,x+w):
            if R.random()<p: px(im,i,j,c)
FONT={'C':".11 1.. 1.. 1.. .11",'H':"1.1 1.1 111 1.1 1.1",'I':"111 .1. .1. .1. 111",'G':".11 1.. 1.1 1.1 .11",'R':"11. 1.1 11. 1.1 1.1",
'E':"111 1.. 11. 1.. 111",'A':".1. 1.1 111 1.1 1.1",'S':".11 1.. .1. ..1 11.",'P':"11. 1.1 11. 1.. 1..",'U':"1.1 1.1 1.1 1.1 111",
'L':"1.. 1.. 1.. 1.. 111",'D':"11. 1.1 1.1 1.1 11.",'O':".1. 1.1 1.1 1.1 .1.",'N':"1.1 111 111 1.1 1.1",'T':"111 .1. .1. .1. .1.",' ':"... ... ... ... ..."}
def text(im,x,y,s,c):
    for ch in s:
        rows=FONT[ch].split()
        for j,r in enumerate(rows):
            for i,v in enumerate(r):
                if v=='1': px(im,x+i,y+j,c)
        x+=4
# ---------------- tiles ----------------
def cobble(im,ox,oy,w,h,warm=0):
    rect(im,ox,oy,w,h,'gr1')
    y=oy
    while y<oy+h:
        rh=R.choice([4,5,5,6]); x=ox-R.randint(0,4)
        while x<ox+w:
            sw=R.choice([5,6,6,7,8])
            base=R.choice(['gr2','gr2','gr2','gr2','gr3','gr3','gr3','gr4']) if R.random()<0.99 else 'sa1'
            for j in range(rh-1):
                for i in range(sw-1):
                    if (i in(0,sw-2)) and (j in(0,rh-2)): continue
                    px(im,x+i,y+j,base) if ox<=x+i<ox+w and oy<=y+j<oy+h else None
            if ox<=x<ox+w: (px(im,x+1,y,'gr4' if base=='gr3' else 'gr3') if R.random()<0.6 else None)
            if ox<=x+sw-3<ox+w and y+rh-2<oy+h: px(im,x+sw-3,y+rh-2,'gr1' if base=='gr2' else 'gr2')
            x+=sw
        y+=rh
# ---------------- plaza background ----------------
W,H=480,352
bg=Image.new('RGB',(W,H),P['gr1'])
cobble(bg,0,0,W,H)
# drain gutter centre line
for x in range(48,432): 
    if x%6==0: px(bg,x,240,'gr1')
def roof(im,x,y,w,h):
    rect(im,x,y,w,h,'rf2')
    for j in range(y,y+h):
        for i in range(x,x+w):
            m=(i-x)%6; r=(j-y+((i-x)//6)%2*3)%6
            if m==0: px(im,i,j,'rf1')
            elif m in(2,3) and r!=5: px(im,i,j,'rf3')
            if r==5 and m!=0: px(im,i,j,'rf1')
    noise(im,x,y,w,h,'gn1',0.012); noise(im,x,y,w,h,'br2',0.02)
    hline(im,x,y+h,w,'k'); hline(im,x,y+h+1,w,'d1')
def window(im,x,y,shut='gn2',balcony=False,lit=False,glows=None):
    rect(im,x-1,y-2,12,2,'gr4'); hline(im,x-1,y-2,12,'cr')  # lintel
    rect(im,x,y,10,15,'br1'); rect(im,x+1,y+1,8,13,'yl' if lit else 'bl1')
    vline(im,x+5,y+1,13,'br1'); hline(im,x+1,y+6,8,'br1')
    if lit:
        rect(im,x+1,y+1,4,5,'or'); glows.append((x+5,y+8))
    else:
        px(im,x+2,y+2,'bl3');px(im,x+3,y+2,'bl2');px(im,x+7,y+8,'bl2')
    for sx in (x-4,x+10):
        rect(im,sx,y,4,15,shut)
        for j in range(y+1,y+14,2): hline(im,sx,j,4,'gn1' if shut=='gn2' else 'br1')
        vline(im,sx+3 if sx<x else sx,y,15,'d2')
    if balcony:
        rect(im,x-6,y+15,22,2,'gr3'); hline(im,x-6,y+17,22,'d2'); hline(im,x-5,y+18,20,'d1')
        hline(im,x-6,y+7,22,'k')
        for i in range(x-6,x+16,3): vline(im,i,y+7,8,'k')
        px(im,x-3,y+6,'rd');px(im,x-2,y+5,'rd');px(im,x-4,y+6,'gn2');px(im,x-1,y+6,'gn2')
    else:
        rect(im,x-1,y+15,12,2,'gr4'); hline(im,x-1,y+17,12,'d2')
def galeria(im,x,y,w,h):
    rect(im,x,y+h,w,3,'d1')
    rect(im,x,y,w,h,'cr')
    for i in range(x+2,x+w-2,6):
        rect(im,i,y+2,4,h-8,'bl2')
        px(im,i,y+2,'bl3');px(im,i+1,y+2,'bl3');px(im,i,y+3,'bl3')
        hline(im,i,y+(h-8)//2+2,4,'cr')
    rect(im,x,y+h-6,w,6,'sa2'); hline(im,x,y+h-6,w,'wh')
    for i in range(x+3,x+w-3,5): rect(im,i,y+h-4,3,2,'sa1')
    vline(im,x,y,h,'gr4'); vline(im,x+w-1,y,h,'gr3'); hline(im,x,y,w,'wh')
def door(im,x,y,w=14,h=22,c='br2'):
    rect(im,x-2,y-3,w+4,3,'gr4'); hline(im,x-2,y-3,w+4,'cr')
    vline(im,x-2,y,h,'gr4');vline(im,x+w+1,y,h,'gr3')
    rect(im,x,y,w,h,c)
    for i in range(x+2,x+w,3): vline(im,i,y,h,'br1')
    hline(im,x,y+h//2,w,'br1'); px(im,x+w-3,y+h//2+2,'yl')
    rect(im,x-3,y+h,w+6,2,'gr3')
def facade(im,x,w,wall,wall2,windows,doorx=None,gal=None,y0=20,y1=128):
    rect(im,x,y0,w,y1-y0,wall)
    noise(im,x,y0,w,y1-y0,wall2,0.10)
    for i in range(x,x+w):   # damp stains / weathering low
        for j in range(y1-30,y1-10):
            if R.random()<0.06*((j-(y1-30))/20): px(im,i,j,wall2)
    vline(im,x,y0,y1-y0,'d2'); vline(im,x+w-1,y0,y1-y0,'gr4')
    # stone base
    rect(im,x,y1-12,w,12,'gr3')
    for j in range(y1-12,y1,4):
        hline(im,x,j,w,'gr1')
        off=(j//4)%2*5
        for i in range(x+off,x+w,10): vline(im,i,j,4,'gr1')
        hline(im,x,j+1,w,'gr4') if False else None
    noise(im,x,y1-12,w,12,'gr4',0.08)
    hline(im,x,y1-13,w,'gr4')
    for (wx,wy,b,lit) in windows: window(im,x+wx,wy,balcony=b,lit=lit,glows=GLOWS,shut=R.choice(['gn2','br3']) if not lit else 'br3')
    if gal: galeria(im,x+gal[0],gal[1],gal[2],gal[3])
    if doorx is not None: door(im,x+doorx,y1-22)
GLOWS=[]
roof(bg,0,0,W,18)
facade(bg,0,96,'oc2','oc1',[(10,74,False,False),(72,74,True,False)],doorx=40,gal=(6,26,84,34))
facade(bg,96,80,'sa2','sa1',[(12,32,True,False),(56,32,True,True),(12,74,True,False),(56,74,False,False)],doorx=34)
# chigre
facade(bg,176,128,'pk','sk2',[(14,32,True,True),(54,32,True,False),(100,32,True,True)])
cx=176
rect(bg,cx+4,82,120,46,'gn1')                 # painted wooden shopfront
noise(bg,cx+4,82,120,46,'gn2',0.05)
hline(bg,cx+4,82,120,'k'); hline(bg,cx+4,83,120,'gn2')
rect(bg,cx+20,86,88,11,'br1'); rect(bg,cx+21,87,86,9,'sa2')  # sign
text(bg,cx+25,89,'CHIGRE CASA PACHU','rf1')
for wx in (cx+10,cx+86):  # shop windows lit
    rect(bg,wx,100,30,20,'br2'); rect(bg,wx+2,102,26,16,'yl')
    rect(bg,wx+2,102,26,5,'or'); vline(bg,wx+15,102,16,'br2')
    for b in range(wx+4,wx+26,4): rect(bg,b,111,2,7,'gn1'); px(bg,b,110,'gn1'); px(bg,b,112,'gn3')
    hline(bg,wx+2,117,26,'br2')
    GLOWS.append((wx+15,110))
door(bg,cx+57,106,14,22,'br3'); rect(bg,cx+59,109,10,8,'or')
GLOWS.append((cx+64,116))
facade(bg,304,96,'gn3','gn2',[(12,32,False,False),(70,32,True,False),(12,74,True,True),(70,74,False,False)],doorx=44,gal=(30,26,40,30))
facade(bg,400,80,'oc2','sa1',[(14,32,True,False),(54,32,True,False),(54,74,False,False)],doorx=16)
# side roofs (west/east blocks seen from above)
def sideblock(im,x,y,w,h,edge):
    roof(im,x,y,w,h-10)
    rect(im,x,y+h-10,w,10,'sa1'); noise(im,x,y+h-10,w,10,'br4',0.2)
    rect(im,x,y+h,w,2,'d1')
    ex=x+w-1 if edge=='r' else x
    vline(im,ex,y,h,'k')
sideblock(bg,0,128,44,170,'r'); sideblock(bg,436,128,44,170,'l')
for (x,y) in ((44,140),(44,200),(44,260)): rect(bg,x,y,3,48,'d1')  # cast shadows
# south parapet & sea
rect(bg,0,312,W,40,'bl2')
for j in range(312,352):
    for i in range(W):
        r=R.random()
        if r<0.05: px(bg,i,j,'bl3')
        elif r<0.07 and j<330: px(bg,i,j,'pk')
        elif r<0.09: px(bg,i,j,'bl1')
for i in range(0,W,R.randint(9,14)): hline(bg,i,R.randint(318,348),R.randint(3,7),'yl' if R.random()<0.3 else 'bl3')
rect(bg,0,298,W,14,'gr3'); hline(bg,0,298,W,'gr4'); hline(bg,0,299,W,'cr')
for i in range(0,W,12): vline(bg,i,300,12,'gr1')
noise(bg,0,300,W,12,'gr2',0.15); hline(bg,0,312,W,'d1')
# plaza details: tree well + manhole
rect(bg,232,196,16,16,'br1'); rect(bg,233,197,14,14,'br2'); noise(bg,233,197,14,14,'br1',0.3)
for a in range(0,360,20):
    px(bg,int(140+6*math.cos(math.radians(a))),int(260+4*math.sin(math.radians(a))),'gr1')
# light warm wash on cobbles near chigre (baked)
for (gx,gy) in [(cx+25,128),(cx+101,128),(cx+64,128)]:
    for j in range(128,170):
        for i in range(gx-26,gx+26):
            d=((i-gx)/26)**2+((j-128)/40)**2
            if d<1 and R.random()<0.12*(1-d) and bg.getpixel((i,j)) in (P['gr3'],P['gr4']): px(bg,i,j,'br4')
bg.save(f'{OUT}/plaza.png')
# ---------------- tree (foreground) ----------------
tree=Image.new('RGBA',(56,72),(0,0,0,0))
rect(tree,26,44,5,26,'br1'); vline(tree,27,44,26,'br2')
for k in range(260):
    a=R.random()*6.283; r=R.random()**0.6*24
    x=int(28+math.cos(a)*r); y=int(26+math.sin(a)*r*0.8)
    c='gn1' if y>34 or x>36 else ('gn2' if R.random()<0.7 else 'gn3')
    rect(tree,x,y,3,3,c)
for k in range(30):
    a=R.random()*6.283; r=R.random()*16; px(tree,int(22+math.cos(a)*r),int(18+math.sin(a)*r*0.7),'oc2')
tree.save(f'{OUT}/tree.png')
# ---------------- props ----------------
lamp=Image.new('RGBA',(16,48),(0,0,0,0))
rect(lamp,5,44,6,4,'k'); rect(lamp,6,14,4,30,'d1'); vline(lamp,7,14,30,'gr1')
rect(lamp,4,24,8,2,'k'); rect(lamp,3,2,10,2,'k'); rect(lamp,4,4,8,9,'yl'); rect(lamp,4,4,2,9,'wh')
vline(lamp,7,4,9,'k'); rect(lamp,4,13,8,1,'k'); rect(lamp,6,0,4,2,'k')
lamp.save(f'{OUT}/lamp.png')
bench=Image.new('RGBA',(32,16),(0,0,0,0))
for y in (2,5): rect(bench,1,y,30,2,'br3'); hline(bench,1,y+1,30,'br2')
rect(bench,1,9,30,3,'br4'); hline(bench,1,11,30,'br2'); hline(bench,1,8,30,'br1')
for x in (3,27): rect(bench,x,8,2,8,'k')
bench.save(f'{OUT}/bench.png')
barrel=Image.new('RGBA',(16,20),(0,0,0,0))
rect(barrel,2,4,12,15,'br2'); rect(barrel,1,7,14,9,'br2')
for x in (4,7,10): vline(barrel,x,4,15,'br1')
vline(barrel,3,5,13,'br3');vline(barrel,2,8,7,'br4')
for y in (6,15): hline(barrel,1,y,14,'gr1')
rect(barrel,3,1,10,4,'br3'); hline(barrel,3,1,10,'br4'); hline(barrel,4,2,8,'br1'); px(barrel,8,3,'k')
hline(barrel,2,19,12,'d1')
barrel.save(f'{OUT}/barrel.png')
crate=Image.new('RGBA',(16,14),(0,0,0,0))
rect(crate,0,6,16,8,'br3'); hline(crate,0,9,16,'br2'); hline(crate,0,13,16,'br1')
for x in range(1,15,3): rect(crate,x,1,2,6,'gn1'); px(crate,x,1,'gn3'); px(crate,x,0,'k')
crate.save(f'{OUT}/crate.png')
pot=Image.new('RGBA',(12,14),(0,0,0,0))
rect(pot,2,8,8,6,'rf2'); hline(pot,1,8,10,'rf3'); vline(pot,8,9,5,'rf1')
for k in range(24): px(pot,R.randint(1,10),R.randint(1,8),R.choice(['gn1','gn2','gn2','rd','pk']))
pot.save(f'{OUT}/pot.png')
glow=Image.new('RGBA',(96,96),(0,0,0,0))
for j in range(96):
    for i in range(96):
        d=math.hypot(i-47.5,j-47.5)/48
        if d<1:
            a=(1-d)**2
            a=round(a*6)/6  # banded, pixel-art style
            glow.putpixel((i,j),P['or']+(int(a*255),))
glow.save(f'{OUT}/glow.png')
vig=Image.new('RGBA',(320,180),(0,0,0,0))
for j in range(180):
    for i in range(320):
        dx=(i-160)/170; dy=(j-90)/110; d=math.hypot(dx,dy)
        a=max(0,(d-0.55)/0.6); a=min(1,a)**1.5
        a=round(a*8)/8
        if (i+j)%2 and a>0: a=min(1,a+1/16)
        vig.putpixel((i,j),P['d1']+(int(a*200),))
vig.save(f'{OUT}/vignette.png')
# ---------------- characters ----------------
def person(spec):
    sheet=Image.new('RGBA',(64,96),(0,0,0,0))
    for row,d in enumerate(['down','left','right','up']):
        for f in range(4):
            fr=Image.new('RGBA',(16,24),(0,0,0,0))
            dd='right' if d=='left' else d
            bob=1 if f in(1,3) else 0
            step=[0,1,0,-1][f]
            sk,hair,top,tops,pants,shoes=spec['sk'],spec['hair'],spec['top'],spec['tops'],spec['pants'],spec['shoes']
            # legs
            if dd in('down','up'):
                ll=4-(1 if step==1 else 0); rl=4-(1 if step==-1 else 0)
                rect(fr,5,18,3,ll,pants); rect(fr,8,18,3,rl,pants)
                rect(fr,5,18+ll,3,2,shoes); rect(fr,8,18+rl,3,2,shoes)
                vline(fr,8,18,3,spec.get('pants2','d1'))
            else:
                if step==0: rect(fr,6,18,4,4,pants); rect(fr,6,22,5,2,shoes)
                else:
                    rect(fr,4,18,3,4,pants); rect(fr,3,21,3,2,shoes)
                    rect(fr,9,18,3,4,pants); rect(fr,10,21,3,2,shoes)
            if spec.get('skirt'):
                rect(fr,4,16,8,5 if dd!='right' else 5,spec['skirt']); hline(fr,4,20,8,'k' if spec['skirt']!='k' else 'd2')
            y=bob
            # torso
            if dd in('down','up'):
                rect(fr,4,11+y,8,7,top); vline(fr,11,11+y,7,tops); hline(fr,4,17+y,8,tops)
                if spec.get('stripes'):
                    for j in range(12+y,17+y,2): hline(fr,4,j,8,spec['stripes'])
                aL=1 if step==1 else 0; aR=1 if step==-1 else 0
                rect(fr,3,12+y-aL,1,5,top); rect(fr,12,12+y-aR,1,5,tops)
                px(fr,3,17+y-aL,sk); px(fr,12,17+y-aR,sk)
                if spec.get('apron') and dd=='down': rect(fr,5,14+y,6,6,spec['apron']); hline(fr,5,14+y,6,'wh')
                if spec.get('vest') and dd=='down': rect(fr,4,11+y,2,7,spec['vest']); rect(fr,10,11+y,2,7,spec['vest'])
            else:
                rect(fr,5,11+y,6,7,top); vline(fr,5,11+y,7,tops); hline(fr,5,17+y,6,tops)
                if spec.get('stripes'):
                    for j in range(12+y,17+y,2): hline(fr,5,j,6,spec['stripes'])
                if spec.get('vest'): rect(fr,5,11+y,3,7,spec['vest'])
                ax=7+step; rect(fr,ax,12+y,2,5,tops); px(fr,ax,17+y,sk); px(fr,ax+1,17+y,sk)
            # head
            rect(fr,5,4+y,6,7,sk); hline(fr,5,10+y,6,spec.get('sk2','sk2'))
            if dd=='down':
                rect(fr,4,2+y,8,3,hair); px(fr,4,5+y,hair); px(fr,11,5+y,hair); px(fr,4,6+y,hair); px(fr,11,6+y,hair)
                px(fr,6,7+y,'k'); px(fr,9,7+y,'k'); px(fr,5,8+y,'pk'); px(fr,10,8+y,'pk')
                if spec.get('beard'): rect(fr,5,9+y,6,2,spec['beard']); px(fr,7,9+y,sk); px(fr,8,9+y,sk)
                if spec.get('mous'): hline(fr,6,9+y,4,spec['mous'])
            elif dd=='up':
                rect(fr,4,2+y,8,8,hair); hline(fr,5,10+y,6,spec.get('sk2','sk2'))
            else:
                rect(fr,4,2+y,7,3,hair); rect(fr,4,4+y,3,5,hair)
                px(fr,9,7+y,'k'); px(fr,11,7+y,sk); px(fr,9,8+y,'pk')
                if spec.get('beard'): rect(fr,7,9+y,4,2,spec['beard'])
                if spec.get('mous'): hline(fr,9,9+y,2,spec['mous'])
            if spec.get('bun') and dd!='down': rect(fr,6 if dd=='up' else 3,1+y,4 if dd=='up' else 3,3,hair)
            if spec.get('cap'):
                rect(fr,4,1+y,8,3,spec['cap']); hline(fr,3,3+y,10,spec['cap']); px(fr,7,0+y,spec['cap'])
            if spec.get('scarf'): rect(fr,4,1+y,8,4,spec['scarf']); px(fr,4,5+y,spec['scarf']); px(fr,11,5+y,spec['scarf'])
            # outline
            a=fr.copy(); 
            for j in range(24):
                for i in range(16):
                    if a.getpixel((i,j))[3]==0 and any(0<=i+u<16 and 0<=j+v<24 and a.getpixel((i+u,j+v))[3] for u,v in((1,0),(-1,0),(0,1),(0,-1))):
                        fr.putpixel((i,j),P['k']+(255,))
            if d=='left': fr=fr.transpose(Image.FLIP_LEFT_RIGHT)
            sheet.paste(fr,(f*16,row*24))
    return sheet
C=P
person(dict(sk='sk',hair='br1',top='rd',tops='rf1',pants='bl2',pants2='bl1',shoes='cr')).save(f'{OUT}/player.png')
person(dict(sk='sk',hair='gr4',top='d1',tops='k',pants='d1',shoes='k',skirt='d2',apron='gr2',bun=1,scarf='d2')).save(f'{OUT}/guela.png')
person(dict(sk='sk2',sk2='br3',hair='gr3',top='bl2',tops='bl1',stripes='bl3',pants='br1',shoes='k',cap='k',beard='gr4')).save(f'{OUT}/pescador.png')
person(dict(sk='sk',hair='k',top='cr',tops='sa1',pants='d1',shoes='k',vest='d2',mous='d1')).save(f'{OUT}/chigrero.png')
person(dict(sk='sk',hair='oc1',top='gn2',tops='gn1',pants='bl1',shoes='rf1')).save(f'{OUT}/neno.png')
# ---------------- chigre interior ----------------
IW,IH=256,176
inn=Image.new('RGB',(IW,IH),P['br2'])
for y in range(48,IH,6):   # planks
    hline(inn,0,y,IW,'br1')
    off=(y//6)%3*11
    for x in range(off,IW,34): vline(inn,x,y,6,'br1')
noise(inn,0,48,IW,IH-48,'br3',0.06); noise(inn,0,48,IW,IH-48,'sa1',0.015)  # serrín
rect(inn,0,0,IW,48,'sa2'); noise(inn,0,0,IW,30,'sa1',0.15)
rect(inn,0,28,IW,20,'br2'); for_=None
for x in range(0,IW,8): vline(inn,x,28,20,'br1')
hline(inn,0,28,IW,'br4'); hline(inn,0,47,IW,'d1')
for sy in (8,20):  # shelves w/ bottles
    rect(inn,120,sy+6,104,2,'br1')
    for x in range(122,222,4):
        c=R.choice(['gn1','gn1','gn2','br1','cr'])
        rect(inn,x,sy,2,6,c); px(inn,x,sy-1,'k'); px(inn,x,sy+2,'cr' if c!='cr' else 'rd')
rect(inn,20,6,40,18,'br1'); rect(inn,22,8,36,14,'cr'); text(inn,24,10,'SIDRA','rf1'); text(inn,24,16,'NATURAL','gn1') if False else text(inn,24,16,'SIDRA','gn1')
rect(inn,70,6,30,20,'gr2'); rect(inn,72,8,26,16,'bl2'); rect(inn,74,10,10,6,'rd'); rect(inn,86,12,10,10,'cr') # football poster-ish
# bar counter
rect(inn,104,64,136,16,'br3'); hline(inn,104,64,136,'br4'); hline(inn,104,65,136,'sa1')
rect(inn,104,80,136,14,'br1'); 
for x in range(108,240,12): vline(inn,x,80,14,'d2')
hline(inn,104,94,136,'k')
for x in (124,150,180): rect(inn,x,58,2,6,'gn1'); px(inn,x,57,'k'); rect(inn,x+4,61,2,3,'yl')
hline(inn,0,IH-1,IW,'k'); rect(inn,112,IH-6,32,6,'k'); rect(inn,114,IH-5,28,5,'br1')
inn.save(f'{OUT}/interior.png')
table=Image.new('RGBA',(24,20),(0,0,0,0))
rect(table,1,2,22,9,'br3'); hline(table,1,2,22,'br4'); hline(table,1,10,22,'br1')
for x in (3,19): rect(table,x,11,2,9,'d1')
rect(table,10,0,2,6,'gn1'); px(table,10,0,'k'); rect(table,14,4,2,3,'yl'); rect(table,6,5,2,3,'yl')
table.save(f'{OUT}/table.png')
json.dump({'glows':GLOWS},open(f'{OUT}/meta.json','w'))
print('ok',len(GLOWS))
