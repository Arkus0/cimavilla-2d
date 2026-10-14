# v2: denser procedural pixel art. Drawn in free RGB, then quantized to a CLOSED 40-colour warm muted palette.
from PIL import Image, ImageDraw
import numpy as np, random, math, os, json
OUT=os.path.join(os.path.dirname(__file__),'out2'); os.makedirs(OUT,exist_ok=True)
PAL=[(26,20,24),(40,30,36),(58,44,46),(84,60,48),(112,80,58),(143,108,78),(173,138,98),(201,168,124),(224,200,158),(240,226,192),
(70,66,68),(98,94,92),(128,122,114),(160,150,134),(110,52,42),(146,74,54),(178,104,72),(168,128,70),(198,160,96),(62,76,60),
(92,108,82),(136,146,108),(40,48,62),(64,80,94),(104,120,124),(132,62,54),(214,150,82),(236,200,122),(208,158,122),(166,114,88),
(248,238,212),(176,128,116),(84,88,128),(124,128,168),(166,148,178),(48,54,62),(196,108,58),(150,52,46),(34,28,36),(120,98,96)]
assert len(PAL)==40
C=dict(k=0,d1=1,d2=2,br1=3,br2=4,br3=5,br4=6,sa1=7,sa2=8,cr=9,gr1=10,gr2=11,gr3=12,gr4=13,rf1=14,rf2=15,rf3=16,oc1=17,oc2=18,gn1=19,
gn2=20,gn3=21,bl1=22,bl2=23,bl3=24,rd=25,orr=26,yl=27,sk=28,sk2=29,wh=30,pk=31,hy1=32,hy2=33,hy3=34,wet=35,bu=36,vm=37,sh=38,mv=39)
def c(n): return PAL[C[n]] if isinstance(n,str) else n
R=random.Random(92)
PALIMG=Image.new('P',(1,1)); PALIMG.putpalette([v for p in PAL for v in p]+[0]*(768-120))
def quant(im):
    if im.mode=='RGBA':
        a=im.split()[3]; q=im.convert('RGB').quantize(palette=PALIMG,dither=Image.Dither.NONE).convert('RGB').convert('RGBA')
        q.putalpha(a.point(lambda v:255 if v>127 else 0)); return q
    return im.quantize(palette=PALIMG,dither=Image.Dither.NONE).convert('RGB')
class Cv:
    def __init__(s,w,h,bg=None):
        s.a=np.zeros((h,w,4),np.float32)
        if bg: s.a[:,:,:3]=c(bg); s.a[:,:,3]=255
        s.ww,s.hh=w,h
    def px(s,x,y,col,a=255):
        if 0<=x<s.ww and 0<=y<s.hh: s.a[y,x,:3]=c(col); s.a[y,x,3]=a
    def rect(s,x,y,w,h,col):
        x0,y0,x1,y1=max(0,x),max(0,y),min(s.ww,x+w),min(s.hh,y+h)
        if x1>x0 and y1>y0: s.a[y0:y1,x0:x1,:3]=c(col); s.a[y0:y1,x0:x1,3]=255
    def h(s,x,y,w,col): s.rect(x,y,w,1,col)
    def v(s,x,y,h,col): s.rect(x,y,1,h,col)
    def mul(s,x,y,w,h,f,tint=(1,1,1)):
        x0,y0,x1,y1=max(0,x),max(0,y),min(s.ww,x+w),min(s.hh,y+h)
        if x1>x0 and y1>y0: s.a[y0:y1,x0:x1,:3]*=np.array(tint)*f
    def noise(s,x,y,w,h,col,p):
        for j in range(y,y+h):
            for i in range(x,x+w):
                if R.random()<p: s.px(i,j,col)
    def line(s,x0,y0,x1,y1,col):
        n=max(abs(x1-x0),abs(y1-y0),1)
        for t in range(n+1): s.px(round(x0+(x1-x0)*t/n),round(y0+(y1-y0)*t/n),col)
    def sag(s,x0,y0,x1,y1,d,col):
        n=max(abs(x1-x0),1); pts=[]
        for t in range(n+1):
            u=t/n; x=round(x0+(x1-x0)*u); y=round(y0+(y1-y0)*u+4*d*u*(1-u)); s.px(x,y,col); pts.append((x,y))
        return pts
    def ellipse(s,x,y,w,h,col):
        for j in range(h):
            for i in range(w):
                if ((i+.5-w/2)/(w/2))**2+((j+.5-h/2)/(h/2))**2<=1: s.px(x+i,y+j,col)
    def glow(s,cx,cy,r,col,strength,squash=1.0,ymin=0):
        ys,xs=np.mgrid[0:s.hh,0:s.ww]; d=np.sqrt((xs-cx)**2+((ys-cy)/squash)**2)/r
        f=np.clip(1-d,0,1)**2*strength; f[ys<ymin]=0
        s.a[:,:,:3]+= f[...,None]*np.array(c(col))*(s.a[:,:,3:]/255)
    def img(s): return Image.fromarray(np.clip(s.a,0,255).astype(np.uint8),'RGBA')
FONT={'A':".1. 1.1 111 1.1 1.1",'B':"11. 1.1 11. 1.1 11.",'C':".11 1.. 1.. 1.. .11",'D':"11. 1.1 1.1 1.1 11.",'E':"111 1.. 11. 1.. 111",'F':"111 1.. 11. 1.. 1..",
'G':".11 1.. 1.1 1.1 .11",'H':"1.1 1.1 111 1.1 1.1",'I':"111 .1. .1. .1. 111",'J':"..1 ..1 ..1 1.1 .1.",'K':"1.1 1.1 11. 1.1 1.1",'L':"1.. 1.. 1.. 1.. 111",
'M':"1.1 111 111 1.1 1.1",'N':"11. 1.1 1.1 1.1 1.1",'O':".1. 1.1 1.1 1.1 .1.",'P':"11. 1.1 11. 1.. 1..",'R':"11. 1.1 11. 1.1 1.1",'S':".11 1.. .1. ..1 11.",
'T':"111 .1. .1. .1. .1.",'U':"1.1 1.1 1.1 1.1 111",'V':"1.1 1.1 1.1 1.1 .1.",'X':"1.1 1.1 .1. 1.1 1.1",'Y':"1.1 1.1 .1. .1. .1.",'Z':"111 ..1 .1. 1.. 111",
'0':"111 1.1 1.1 1.1 111",'1':".1. 11. .1. .1. 111",'2':"11. ..1 .1. 1.. 111",'9':"111 1.1 111 ..1 11.",'.':"... ... ... ... .1.",' ':"... ... ... ... ...",'-':"... ... 111 ... ..."}
def text(cv,x,y,s,col):
    for ch in s:
        for j,r in enumerate(FONT[ch].split()):
            for i,v in enumerate(r):
                if v=='1': cv.px(x+i,y+j,col)
        x+=4
def twidth(s): return len(s)*4-1
# ====================================================== GROUND LAYER
W,H=480,352; G=Cv(W,H,'gr1'); FG=Cv(W,H)
def cobbles(cv,x0,y0,x1,y1):
    y=y0; row=0
    while y<y1:
        rh=R.choice([5,5,6]); x=x0-R.randint(0,6)
        while x<x1:
            sw=R.choice([6,7,8,8,9,10])
            wear=math.exp(-(((x-240)/120)**2+((y-200)/70)**2))  # worn centre path
            base=np.array(c(R.choice(['gr2','gr2','gr3','gr3','gr3','gr4','br3'])),float)
            base=base*(1+0.18*wear)+R.uniform(-6,6)
            for j in range(rh-1):
                for i in range(sw-1):
                    if (i in(0,sw-2)) and (j in(0,rh-2)): continue
                    col=base*(1.15 if (j==0 or i==0) else 0.82 if (j==rh-2 or i==sw-2) else 1.0)
                    if x0<=x+i<x1 and y0<=y+j<y1: cv.a[y+j,x+i,:3]=col
            x+=sw
        y+=rh; row+=1
cobbles(G,0,0,W,H)
# granite slab gutter down the middle + manhole
for y in range(132,300,8):
    G.rect(236,y,9,7,'gr3'); G.h(236,y,9,'gr4'); G.h(236,y+6,9,'gr2'); G.v(240,y+2,3,'gr1')
G.ellipse(130,250,18,11,'gr1'); G.ellipse(131,251,16,9,'gr2')
for i in range(133,147,3): G.v(i,252,7,'gr1')
# moss in joints near walls
for y in range(128,300):
    for x in range(44,436):
        near=min(y-128,x-44,436-x)
        if near<14 and R.random()<0.08*(1-near/14) and tuple(G.a[y,x,:3])==c('gr1'): G.px(x,y,'gn1')
# puddles (wet stone)
def puddle(cx,cy,rx,ry):
    for y in range(cy-ry,cy+ry):
        for x in range(cx-rx,cx+rx):
            d=((x-cx)/rx)**2+((y-cy)/ry)**2+0.25*math.sin(x*0.7)*math.cos(y*0.9)
            if d<1: G.a[y,x,:3]=G.a[y,x,:3]*0.55+np.array(c('wet'))*0.45
            if d<0.5 and R.random()<0.05: G.px(x,y,'bl3')
puddle(300,190,22,7); puddle(110,280,16,5); puddle(380,250,12,4); puddle(200,160,10,3)
# ----------------------------------------------- facades
def roofband(cv,x,y,w,h):
    for j in range(y,y+h):
        for i in range(x,x+w):
            m=(i-x)%6; r=(j-y+((i-x)//6)%2*3)%6
            col='rf2'
            if m==0: col='rf1'
            elif m in(2,3) and r!=5: col='rf3'
            if r==5 and m!=0: col='rf1'
            cv.px(i,j,col)
    cv.noise(x,y,w,h,'gn1',0.02); cv.noise(x,y,w,h,'br2',0.03); cv.noise(x,y,w,h,'mv',0.02)
WALLS=[]
def window(cv,x,y,lit=False,bal=False,shut='gn2',laundry=False,flowers=False):
    cv.rect(x-2,y-3,14,3,'gr4'); cv.h(x-2,y-3,14,'cr'); cv.mul(x-2,y,14,1,0.7)          # lintel + shadow
    cv.rect(x,y,10,16,'d2'); cv.rect(x+1,y+1,8,15,'yl' if lit else 'bl1')               # recess
    if lit: cv.rect(x+1,y+1,8,5,'orr'); cv.rect(x+1,y+1,2,15,'br3'); LIGHTS.append((x+5,y+8,'win'))
    else:
        cv.px(x+3,y+3,'bl3');cv.px(x+4,y+3,'bl2');cv.px(x+3,y+4,'bl2'); cv.rect(x+1,y+1,8,2,'sh')
        cv.rect(x+1,y+1,2,15,'sh')       # deep reveal shadow (3/4 depth)
    cv.v(x+5,y+1,15,'cr' if not lit else 'br2'); cv.h(x+1,y+7,8,'cr' if not lit else 'br2')
    for sx in (x-5,x+10):
        cv.rect(sx,y,5,16,shut)
        for j in range(y+1,y+15,2): cv.h(sx,j,5,{'gn2':'gn1','br3':'br2','bl3':'bl2'}[shut])
        cv.v(sx+4 if sx<x else sx,y,16,'d2')
    cv.mul(x+15,y+1,1,16,0.75)    # shutter cast shadow on wall
    # rain streak under sill
    for k in range(3):
        sx=x+R.randint(1,8); cv.mul(sx,y+18,1,R.randint(6,14),0.88)
    if bal:
        cv.rect(x-7,y+16,24,2,'gr3'); cv.h(x-7,y+16,24,'gr4'); cv.mul(x-6,y+18,24,3,0.62)  # slab + cast shadow
        cv.h(x-7,y+8,24,'k')
        for i in range(x-7,x+17,3): cv.v(i,y+8,8,'k')
        for i in range(x-6,x+17,6): cv.px(i,y+10,'d2')
        if flowers:
            for i in range(x-6,x+16,2):
                cv.px(i,y+7,R.choice(['hy1','hy2','hy3','gn1'])); cv.px(i,y+6,R.choice(['hy2','gn2','hy3']))
        if laundry:
            pts=cv.sag(x-8,y-1,x+18,y-1,3,'gr2')
            for k,(px_,py_) in enumerate(pts[3:-3:5]):
                col=R.choice(['wh','cr','bl3','pk','hy2']); cv.rect(px_,py_+1,4,R.choice([4,6,7]),col); cv.mul(px_+3,py_+1,1,6,0.8)
    else:
        cv.rect(x-1,y+16,12,2,'gr4'); cv.h(x-1,y+16,12,'cr'); cv.mul(x-1,y+18,12,2,0.75)
def galeria(cv,x,y,w,h):
    cv.mul(x+w,y+3,4,h,0.6); cv.mul(x+2,y+h,w,4,0.55)    # cast shadow right & below (depth)
    cv.rect(x,y,w,h,'cr'); cv.rect(x+w,y+1,3,h-1,'sa1')     # side face
    for i in range(x+2,x+w-3,6):
        cv.rect(i,y+3,4,h-11,'bl2'); cv.px(i,y+3,'bl3'); cv.px(i+1,y+3,'bl3'); cv.px(i,y+4,'bl3')
        cv.h(i,y+3+(h-11)//2,4,'cr')
        if R.random()<0.35: cv.rect(i,y+3,4,3,'yl')  # a lit pane
        if R.random()<0.3: cv.rect(i+1,y+4,2,h-14,'wh')   # lace curtain
    cv.rect(x,y+h-7,w,7,'sa2'); cv.h(x,y+h-7,w,'wh')
    for i in range(x+3,x+w-3,5): cv.rect(i,y+h-5,3,3,'sa1')
    cv.h(x-1,y-1,w+2,'gr4'); cv.h(x-1,y-2,w+2,'k'); cv.v(x,y,h,'wh'); cv.h(x,y+h,w,'d2')
def door(cv,x,y,w=14,h=24,col='br2',arch=False):
    cv.rect(x-3,y-4,w+6,4,'gr4'); cv.h(x-3,y-4,w+6,'cr')
    cv.v(x-3,y,h,'gr4'); cv.v(x-2,y,h,'gr3'); cv.v(x+w,y,h,'gr3'); cv.v(x+w+1,y,h,'gr2')
    cv.rect(x,y,w,h,col)
    for i in range(x+2,x+w,3): cv.v(i,y,h,'br1')
    cv.h(x,y+h//2,w,'br1'); cv.px(x+w-3,y+h//2+2,'yl'); cv.rect(x,y,w,3,'sh')   # recess shadow
    cv.rect(x-4,y+h,w+8,2,'gr3'); cv.h(x-4,y+h,w+8,'gr4')
def facade(cv,x,w,wall,shade,wins,doors=(),gal=None,y0=22,y1=128,peel=True):
    cv.rect(x,y0,w,y1-y0,wall)
    for j in range(y0,y1):
        f=0.94+0.06*((j-y0)/(y1-y0))  # upper floors dimmer (evening)
        cv.mul(x,j,w,1,f)
    cv.noise(x,y0,w,y1-y0,shade,0.08)
    if peel:
        for k in range(3):  # flaked plaster showing stone
            px_,py_=x+R.randint(4,w-20),R.randint(y0+30,y1-30); pw,ph=R.randint(8,16),R.randint(5,9)
            for j in range(ph):
                for i in range(pw):
                    if ((i-pw/2)/(pw/2))**2+((j-ph/2)/(ph/2))**2<1-R.random()*0.3:
                        cv.px(px_+i,py_+j,R.choice(['gr3','gr3','gr2','gr4']) if (j%3) else 'gr1')
    for j in range(y1-40,y1-14):  # damp
        for i in range(x,x+w):
            if R.random()<0.25*((j-(y1-40))/26): cv.a[j,i,:3]*=0.9
    # cornice under roof + cast shadow
    cv.rect(x,y0,w,3,'gr4'); cv.h(x,y0,w,'cr'); cv.mul(x,y0+3,w,6,0.6); cv.mul(x,y0+9,w,3,0.8)
    # floor band
    cv.h(x,70,w,'gr4'); cv.mul(x,71,w,1,0.75)
    # stone plinth
    cv.rect(x,y1-14,w,14,'gr3')
    for j in range(y1-14,y1,5):
        cv.h(x,j,w,'gr1'); off=(j//5)%2*6
        for i in range(x+off,x+w,12): cv.v(i,j,5,'gr1')
        cv.h(x,j+1,w,'gr4') if R.random()<0.3 else None
    cv.noise(x,y1-14,w,14,'gr4',0.08); cv.noise(x,y1-14,w,14,'gn1',0.04); cv.h(x,y1-15,w,'gr4')
    cv.v(x,y0,y1-y0,'d2'); cv.v(x+w-1,y0,y1-y0,'gr4')
    # drainpipe
    px_=x+w-4; cv.v(px_,y0+2,y1-y0-2,'gr2'); cv.v(px_+1,y0+2,y1-y0-2,'gr1'); cv.mul(px_+2,y0+2,1,y1-y0-2,0.7)
    for j in range(y0+10,y1,18): cv.h(px_-1,j,3,'k')
    for wv in wins: window(cv,x+wv[0],wv[1],**wv[2])
    if gal: galeria(cv,x+gal[0],gal[1],gal[2],gal[3])
    for d in doors: door(cv,x+d[0],y1-24,**d[1])
LIGHTS=[]
roofband(G,0,0,W,20); G.h(0,20,W,'k'); G.h(0,21,W,'sh')
for x in range(0,W,R.randint(24,40)):  # chimneys
    G.rect(x+10,2,8,12,'gr3'); G.h(x+10,2,8,'gr4'); G.rect(x+11,0,6,3,'d1'); G.mul(x+18,4,3,10,0.6)
facade(G,0,96,'oc2','oc1',[(10,76,dict(shut='bl3')),(74,76,dict(bal=True,flowers=True))],doors=[(42,{})],gal=(6,28,84,36))
facade(G,96,80,'sa2','sa1',[(12,32,dict(bal=True,laundry=True)),(58,32,dict(bal=True,lit=True,shut='br3')),(58,78,dict(shut='br3'))])
# ultramarinos front in sa2 building
x=96; G.rect(x+4,88,72,40,'br2'); G.mul(x+4,88,72,4,0.6)
G.rect(x+8,92,64,10,'cr'); G.rect(x+9,93,62,8,'sa2'); text(G,x+40-twidth('ULTRAMARINOS')//2,95,'ULTRAMARINOS','bl1')
G.rect(x+8,104,26,22,'br1'); G.rect(x+10,106,22,18,'yl'); G.rect(x+10,106,22,6,'orr')
for i in range(x+11,x+31,3): G.rect(i,116,2,8,R.choice(['rd','gn2','oc2','cr','bl2']))
G.h(x+10,115,22,'br1'); LIGHTS.append((x+21,114,'shop'))
door(G,x+44,104,col='br3'); G.rect(x+46,107,10,8,'bl2')
for i in range(x+4,x+76,6):   # awning
    G.rect(i,82,6,7,'rd' if (i//6)%2 else 'cr'); G.px(i,89,'rd' if (i//6)%2 else 'cr')
G.h(x+4,81,72,'d2'); G.mul(x+4,89,72,4,0.55)
# chigre
cx=176; facade(G,cx,128,'pk','sk2',[(14,32,dict(bal=True,lit=True,shut='br3')),(56,32,dict(bal=True,flowers=True)),(100,32,dict(bal=True,lit=True,shut='br3'))])
G.rect(cx+4,80,120,48,'gn1'); G.noise(cx+4,80,120,48,'gn2',0.06); G.h(cx+4,80,120,'k'); G.h(cx+4,81,120,'gn2')
for i in range(cx+4,cx+124,10): G.v(i,100,28,'sh')
G.mul(cx+4,82,120,3,0.6)
G.rect(cx+18,84,92,13,'br1'); G.rect(cx+19,85,90,11,'sa2'); G.h(cx+19,95,90,'sa1')
s='CHIGRE CASA PACHU'; text(G,cx+64-twidth(s)//2,88,s,'rf1')
for wx in (cx+10,cx+86):
    G.rect(wx,100,32,22,'br2'); G.rect(wx+2,102,28,18,'yl'); G.rect(wx+2,102,28,6,'orr'); G.v(wx+16,102,18,'br2')
    for b in range(wx+4,wx+28,4): G.rect(b,111,2,9,'gn1'); G.px(b,110,'gn1'); G.px(b,112,'gn3')
    G.h(wx+2,119,28,'br2'); G.rect(wx+5,104,3,4,'k'); G.rect(wx+20,103,4,5,'sh')   # silhouettes inside
    LIGHTS.append((wx+16,112,'shop'))
door(G,cx+57,104,col='br3'); G.rect(cx+59,107,10,9,'orr'); G.rect(cx+59,107,10,3,'yl'); LIGHTS.append((cx+64,116,'door'))
# blackboard menu
G.rect(cx+46,100,8,12,'br1'); G.rect(cx+47,101,6,10,'d1'); G.h(cx+48,103,4,'cr'); G.h(cx+48,106,3,'cr'); G.h(cx+48,108,4,'cr')
facade(G,304,96,'gn3','gn2',[(12,32,dict(bal=True,laundry=True)),(72,32,dict(bal=True,flowers=True)),(12,78,dict(bal=True,lit=True,shut='br3')),(72,78,dict())],doors=[(44,{})],gal=(32,28,40,30))
facade(G,400,80,'oc2','sa1',[(14,32,dict(bal=True)),(56,32,dict(bal=True,laundry=True)),(56,78,dict(shut='bl3'))],doors=[(14,{'col':'bl2'})])
# posters & plaque
def poster(x,y,w,h,bg,txt,fg,torn=True):
    G.rect(x,y,w,h,bg); G.mul(x+w,y+1,1,h,0.7); G.mul(x+1,y+h,w,1,0.7)
    for k,t in enumerate(txt): text(G,x+(w-twidth(t))//2,y+2+k*6,t,fg)
    if torn:
        for k in range(4): G.px(x+R.randint(0,w-1),y+h-1,'gr3')
poster(372,94,22,20,'cr',['SEMA','NEGRA','92'],'k'); poster(400,100,18,16,'rd',['SPOR','TING'],'cr')
poster(22,96,18,14,'oc2',['FIES','TAS'],'rf1')
G.rect(332,58,36,9,'cr'); G.rect(333,59,34,7,'bl2'); text(G,335,60,'CORRADA','cr')
# cables across facades
G.sag(0,46,96,44,4,'k'); G.sag(96,44,176,48,5,'k'); G.sag(176,48,304,46,7,'k'); G.sag(304,46,480,50,6,'k')
G.sag(0,60,180,62,5,'d1'); G.sag(300,62,480,60,4,'d1')
for x_ in (96,176,304): G.rect(x_-1,43,3,3,'gr2')
# wall lanterns (farolas fernandinas)
def wall_lamp(x,y):
    G.h(x-3,y,8,'k'); G.v(x-3,y,4,'k'); G.rect(x,y+1,6,2,'k'); G.rect(x,y+3,6,7,'yl'); G.rect(x,y+3,2,7,'wh'); G.v(x+3,y+3,7,'k'); G.h(x,y+10,6,'k')
    LIGHTS.append((x+3,y+7,'lamp'))
wall_lamp(90,66); wall_lamp(300,66); wall_lamp(396,66)
# side blocks (roofs seen from above) with eave depth
def side(x,w,edge):
    roofband(G,x,128,w,162); G.rect(x,290,w,10,'sa1'); G.noise(x,290,w,10,'br4',0.2); G.h(x,300,w,'d1')
    ex=x+w-1 if edge=='r' else x; G.v(ex,128,172,'k'); G.v(ex+(1 if edge=='r' else -1),128,172,'rf1')
    sx=x+w if edge=='r' else x-8
    G.mul(sx,128,8,170,0.7)   # cast shadow on cobbles
side(0,44,'r'); side(436,44,'l')
G.mul(0,128,W,8,0.72); G.mul(0,136,W,4,0.86)   # facades' cast shadow on ground
# hydrangea planters along walls (part of ground layer; low)
def hydrangea(cv,x,y,w):
    cv.rect(x,y,w,8,'gr3'); cv.h(x,y,w,'gr4'); cv.mul(x,y+8,w,2,0.6)
    for k in range(w*3):
        i=x+R.randint(0,w-3); j=y-R.randint(1,9); col=R.choice(['hy1','hy2','hy3','hy2','gn1','gn2'])
        cv.rect(i,j,2,2,col)
hydrangea(G,48,130,28); hydrangea(G,404,130,28)
# parapet + sea
for j in range(312,H):
    for i in range(W):
        f=(j-312)/40; G.a[j,i,:3]=np.array(c('bl2'))*(1-f*0.3)+np.array(c('pk'))*0.15*(1-f)
G.noise(0,312,W,40,'bl3',0.05); G.noise(0,312,W,40,'bl1',0.03)
for k in range(60):
    G.h(R.randint(0,W),R.randint(316,350),R.randint(2,6),R.choice(['yl','bl3','pk']))
G.rect(0,298,W,14,'gr3'); G.h(0,298,W,'cr'); G.h(0,299,W,'gr4')
for i in range(0,W,12): G.v(i,300,12,'gr1')
G.noise(0,300,W,12,'gr2',0.15); G.noise(0,300,W,12,'gn1',0.05); G.h(0,311,W,'sh')
G.ellipse(232,196,16,14,'br1'); G.ellipse(233,197,14,12,'br2'); G.noise(233,197,14,12,'br1',0.3)
# ---------- baked lighting on ground layer
G.a[:,:,:3]*=np.array([0.98,0.93,0.92])
for (lx,ly,kind) in LIGHTS:
    if kind=='lamp': G.glow(lx,ly+62,50,'orr',0.2,0.8,ymin=128)
    elif kind in('shop','door'): G.glow(lx,ly+20,34,'orr',0.2,0.6,ymin=128)
for (lx,ly) in [(120,150),(360,150),(240,290)]: G.glow(lx,ly,60,'orr',0.22,0.6,ymin=128)
# ====================================================== FOREGROUND LAYER (always above player)
FG.sag(44,140,436,150,14,'k')   # overhead cable across plaza
# west/east eave overhang
for (x,w) in ((0,48),(432,48)):
    roofband(FG,x,124,w,6)
G.img(); 
quant(G.img().convert('RGB')).save(f'{OUT}/plaza_ground.png'); quant(FG.img()).save(f'{OUT}/plaza_fg.png')
json.dump({'lights':[(x,y,k) for x,y,k in LIGHTS]},open(f'{OUT}/meta.json','w'))
# ====================================================== PROPS (y-sorted sprites)
def save(cv,name): quant(cv.img()).save(f'{OUT}/{name}.png')
p=Cv(16,52); p.rect(6,47,5,5,'k'); p.rect(5,50,7,2,'d1'); p.rect(7,16,3,32,'d1'); p.v(7,16,32,'gr1')
p.rect(5,26,7,2,'k'); p.rect(3,4,11,2,'k'); p.rect(4,6,9,10,'yl'); p.rect(4,6,3,10,'wh'); p.v(8,6,10,'k'); p.h(4,10,9,'orr'); p.h(3,16,11,'k'); p.rect(6,0,5,4,'k'); p.px(8,0,'gr2')
save(p,'lamp')
b=Cv(34,20)
for y in (2,6): b.rect(1,y,32,3,'br3'); b.h(1,y,32,'br4'); b.h(1,y+2,32,'br2')
b.rect(1,11,32,3,'br4'); b.h(1,11,32,'sa1'); b.h(1,13,32,'br2'); b.h(1,10,32,'br1')
for x in (3,29): b.rect(x,2,2,18,'k'); b.px(x,1,'gr1')
b.mul(2,14,30,6,0.0); b.a[14:20,2:32,3]=0
for x in (3,29): b.rect(x,14,2,6,'k')
save(b,'bench')
bt=Cv(18,30)   # barrel-table with bottle & glasses (chigre outdoor)
bt.ellipse(1,8,16,22,'br2'); bt.rect(1,12,16,14,'br2')
for x in (4,8,12): bt.v(x,10,19,'br1')
bt.v(3,11,16,'br3'); bt.v(2,13,12,'br4'); bt.v(15,11,16,'br1')
for y in (13,24): bt.h(1,y,16,'gr1'); bt.h(1,y+1,16,'gr2')
bt.ellipse(2,6,14,6,'br3'); bt.ellipse(4,7,10,4,'br4')
bt.rect(8,0,3,8,'gn1'); bt.px(9,0,'k'); bt.px(8,3,'gn3'); bt.rect(8,4,3,2,'cr')
bt.rect(4,6,2,3,'yl'); bt.px(4,6,'wh'); bt.rect(13,6,2,3,'yl')
save(bt,'barrel')
cr=Cv(18,16); cr.rect(0,6,18,10,'br3'); cr.h(0,6,18,'br4'); cr.h(0,10,18,'br2'); cr.h(0,15,18,'br1'); cr.v(0,6,10,'br2'); cr.v(17,6,10,'br2')
for x in range(1,17,3): cr.rect(x,0,2,7,'gn1'); cr.px(x,1,'gn3'); cr.px(x,0,'k')
text(cr,3,8,'EL',  'cr') if False else None
save(cr,'crate')
vm=Cv(20,34)   # drinks vending machine
vm.rect(0,2,20,32,'vm'); vm.v(0,2,32,'rd'); vm.v(18,2,16,'rf1'); vm.v(19,2,32,'sh')
vm.rect(2,4,11,20,'cr'); vm.rect(3,5,9,18,'yl')
for j in range(6,22,4):
    for i in range(4,12,3): vm.rect(i,j,2,3,R.choice(['rd','bl2','oc2','gn2','orr']))
vm.rect(14,6,3,8,'d1'); vm.px(15,7,'yl'); vm.px(15,10,'gn3'); vm.rect(14,16,3,2,'gr3')
vm.rect(2,26,11,4,'d1'); vm.rect(3,27,9,2,'k'); vm.h(0,2,20,'pk'); vm.rect(1,0,18,2,'gr2'); vm.h(0,33,20,'k')
text(vm,3,30,'',  'cr')
save(vm,'vending')
bk=Cv(30,22)   # bicycle leaning on wall
for (wx) in (2,18):
    for a in range(0,360,8):
        bk.px(round(wx+5+5*math.cos(math.radians(a))),round(15+5*math.sin(math.radians(a))),'k')
    bk.px(wx+5,15,'gr3')
bk.line(7,15,14,8,'rd'); bk.line(14,8,23,9,'rd'); bk.line(23,9,23,15,'rd'); bk.line(7,15,16,15,'rd'); bk.line(16,15,14,8,'rd'); bk.line(16,15,23,9,'rd')
bk.rect(12,6,5,2,'k'); bk.line(23,9,22,4,'gr3'); bk.h(20,4,5,'gr2'); bk.rect(24,9,4,2,'gr2')
save(bk,'bike')
bu=Cv(12,18); bu.rect(1,4,10,13,'bu'); bu.v(2,5,11,'orr'); bu.v(9,5,11,'rf1'); bu.rect(3,1,6,3,'gr3'); bu.rect(4,0,4,1,'gr2'); bu.h(1,8,10,'rf1'); bu.h(1,17,10,'k'); bu.h(2,4,8,'rf1')
save(bu,'butano')
fc=Cv(24,18)   # fish crates + net
for k,(ox,oy) in enumerate(((0,6),(4,0))):
    fc.rect(ox,oy+3,18,9,'sa1'); fc.h(ox,oy+3,18,'sa2'); fc.h(ox,oy+7,18,'br4'); fc.h(ox,oy+11,18,'br3')
    for i in range(ox+2,ox+16,3): fc.rect(i,oy+1,3,3,'bl3'); fc.px(i,oy+1,'cr'); fc.px(i+2,oy+3,'gr4')
for i in range(0,24):
    for j in range(13,18):
        if (i+j)%2==0 and R.random()<0.8: fc.px(i,j,R.choice(['rf1','rd','br2']))
save(fc,'fishcrates')
cat=Cv(10,9); cat.rect(1,3,7,5,'d1'); cat.rect(6,0,4,4,'d1'); cat.px(6,0,'d1'); cat.px(9,0,'d1'); cat.px(7,2,'yl'); cat.v(0,4,4,'d1'); cat.px(0,3,'d1')
save(cat,'cat')
hp=Cv(16,18); hp.rect(3,11,10,7,'rf2'); hp.h(2,11,12,'rf3'); hp.v(11,12,6,'rf1')
for k in range(40): i,j=R.randint(1,13),R.randint(0,9); hp.rect(i,j,2,2,R.choice(['hy1','hy2','hy3','hy2','gn1','gn2']))
save(hp,'hydrangea')
tr=Cv(60,80); tr.rect(27,46,6,32,'br1'); tr.v(28,46,32,'br2'); tr.v(32,46,32,'d2')
for k in range(380):
    a=R.random()*6.283; r=R.random()**0.6*26; x=int(30+math.cos(a)*r); y=int(28+math.sin(a)*r*0.8)
    lit=(x<26 and y<30); col=('gn2' if R.random()<.6 else 'gn3') if lit else ('gn1' if y>34 or x>36 else 'gn2')
    tr.rect(x,y,3,3,col)
for k in range(40): a=R.random()*6.283; r=R.random()*20; tr.px(int(26+math.cos(a)*r),int(22+math.sin(a)*r*.7),'oc2')
save(tr,'tree')
sh=Cv(16,6); sh.ellipse(0,0,16,6,'sh'); sh.a[:,:,3]*=0.5; Image.fromarray(np.clip(sh.a,0,255).astype(np.uint8)).save(f'{OUT}/shadow.png')
# glow + vignette
g=Image.new('RGBA',(96,96),(0,0,0,0))
for j in range(96):
    for i in range(96):
        d=math.hypot(i-47.5,j-47.5)/48
        if d<1: g.putpixel((i,j),c('orr')+(int(round((1-d)**2*6)/6*255),))
g.save(f'{OUT}/glow.png')
vg=Image.new('RGBA',(320,180),(0,0,0,0))
for j in range(180):
    for i in range(320):
        d=math.hypot((i-160)/170,(j-90)/110); a=min(1,max(0,(d-0.55)/0.6))**1.5; a=round(a*8)/8
        if (i+j)%2 and a>0: a=min(1,a+1/16)
        vg.putpixel((i,j),c('sh')+(int(a*200),))
vg.save(f'{OUT}/vignette.png')
# ====================================================== CHARACTERS 24x32
def person(sp):
    sheet=Cv(96,128)
    for row,d in enumerate(['down','left','right','up']):
        for f in range(4):
            F=Cv(24,32); dd='right' if d=='left' else d
            step=[0,1,0,-1][f]; y=1 if f in(1,3) else 0
            top,tops,pants,pants2,shoes,sk,sk2,hair,hair2=[sp[k] for k in('top','tops','pants','pants2','shoes','sk','sk2','hair','hair2')]
            # legs
            if dd in('down','up'):
                ll=8-(2 if step==1 else 0); rl=8-(2 if step==-1 else 0)
                F.rect(8,22,4,ll,pants); F.rect(12,22,4,rl,pants2); F.v(11,22,ll,pants2)
                F.rect(7,22+ll,5,2,shoes); F.rect(12,22+rl,5,2,shoes); F.h(7,23+ll,5,'k'); F.h(12,23+rl,5,'k')
                if sp.get('boots'): F.rect(8,26,4,ll-4,shoes); F.rect(12,26,4,rl-4,shoes)
            else:
                if step==0: F.rect(10,22,5,8,pants); F.v(14,22,8,pants2); F.rect(10,29,7,2,shoes); F.h(10,30,7,'k')
                else:
                    F.line(11,22,8,29,pants); F.line(12,22,9,29,pants); F.line(13,22,10,29,pants2); F.rect(6,29,5,2,shoes)
                    F.line(13,22,16,29,pants); F.line(14,22,17,29,pants2); F.line(12,22,15,29,pants); F.rect(15,29,5,2,shoes)
                    if sp.get('boots'): F.rect(7,26,4,3,shoes); F.rect(15,26,4,3,shoes)
            if sp.get('skirt'):
                F.rect(6,19,12,8,sp['skirt']); F.h(6,26,12,'sh'); F.v(17,19,8,'sh')
            # torso
            if dd in('down','up'):
                F.rect(6,12+y,12,11,top); F.rect(15,12+y,3,11,tops); F.h(6,22+y,12,tops)
                if sp.get('stripes'):
                    for j in range(14+y,22+y,2): F.h(6,j,12,sp['stripes'])
                if dd=='down':
                    F.h(9,12+y,6,sp.get('collar',tops)); 
                    if sp.get('vest'): F.rect(6,12+y,4,11,sp['vest']); F.rect(14,12+y,4,11,sp['vest'])
                    if sp.get('apron'): F.rect(8,16+y,8,9,sp['apron']); F.h(8,16+y,8,'wh'); F.v(15,16+y,9,'gr3')
                    if sp.get('zip'): F.v(12,13+y,9,sp['zip'])
                    if sp.get('shawl'): F.rect(6,12+y,12,4,sp['shawl']); F.px(11,16+y,sp['shawl']); F.px(12,16+y,sp['shawl'])
                elif sp.get('shawl'): F.rect(6,12+y,12,6,sp['shawl'])
                aL=2 if step==1 else 0; aR=2 if step==-1 else 0
                F.rect(3,13+y-aL,3,9,top); F.v(3,13+y-aL,9,tops); F.rect(18,13+y-aR,3,9,tops)
                F.rect(3,22+y-aL,3,2,sk); F.rect(18,22+y-aR,3,2,sk2)
            else:
                F.rect(8,12+y,9,11,top); F.v(8,12+y,11,tops); F.h(8,22+y,9,tops)
                if sp.get('stripes'):
                    for j in range(14+y,22+y,2): F.h(8,j,9,sp['stripes'])
                if sp.get('vest'): F.rect(13,12+y,4,11,sp['vest'])
                if sp.get('apron'): F.rect(15,16+y,3,9,sp['apron'])
                if sp.get('shawl'): F.rect(8,12+y,9,5,sp['shawl'])
                ax=11+step*2; F.rect(ax,13+y,3,9,tops); F.v(ax+2,13+y,9,'sh'); F.rect(ax,22+y,3,2,sk)
            # head
            hx=7 if dd in('down','up') else 8
            F.ellipse(hx,2+y,10,11,sk); F.rect(hx+1,11+y,8,2,sk2) if dd!='up' else None
            if dd=='down':
                F.rect(7,1+y,10,4,hair); F.px(7,5+y,hair); F.px(16,5+y,hair); F.v(7,5+y,4,hair); F.v(16,5+y,4,hair); F.h(9,1+y,4,hair2)
                F.px(9,7+y,hair); F.px(10,7+y,hair); F.px(13,7+y,hair); F.px(14,7+y,hair)
                F.rect(9,8+y,2,2,'k'); F.rect(13,8+y,2,2,'k'); F.px(9,8+y,'wh'); F.px(13,8+y,'wh')
                F.px(11,10+y,sk2); F.px(12,10+y,sk2); F.h(11,12+y,2,'rf1'); F.px(8,10+y,'pk'); F.px(15,10+y,'pk')
                F.v(16,4+y,7,sk2)
                if sp.get('beard'): F.rect(8,10+y,8,3,sp['beard']); F.h(10,11+y,4,'rf1')
                if sp.get('mous'): F.h(10,11+y,4,sp['mous'])
                if sp.get('glasses'): F.h(8,8+y,8,'gr2')
            elif dd=='up':
                F.ellipse(7,1+y,10,11,hair); F.h(9,2+y,5,hair2); F.rect(8,11+y,8,2,sk2)
            else:
                F.rect(8,1+y,9,4,hair); F.rect(8,4+y,4,7,hair); F.h(10,1+y,5,hair2)
                F.rect(14,8+y,2,2,'k'); F.px(15,8+y,'wh'); F.px(18,9+y,sk); F.px(18,10+y,sk2); F.px(16,12+y,'rf1')
                F.v(12,6+y,3,sk2)
                if sp.get('beard'): F.rect(12,10+y,6,3,sp['beard'])
                if sp.get('mous'): F.h(15,11+y,3,sp['mous'])
            if sp.get('bun'):
                if dd=='up': F.ellipse(9,0+y,6,5,hair); F.px(11,1+y,hair2)
                elif dd=='right': F.ellipse(6,1+y,5,5,hair)
            if sp.get('cap'):
                F.rect(7,0+y,10,4,sp['cap']); F.h(6,3+y,12,sp['cap']); F.h(8,0+y,5,'d2')
                if dd=='right': F.h(15,4+y,4,sp['cap'])
            # selective outline
            a=F.a[:,:,3]>0; o=np.zeros_like(a)
            o[1:]|=a[:-1]; o[:-1]|=a[1:]; o[:,1:]|=a[:,:-1]; o[:,:-1]|=a[:,1:]
            o&=~a; F.a[o]=list(c('sh'))+[255]
            im=F.a
            if d=='left': im=im[:,::-1]
            sheet.a[row*32:row*32+32,f*24:f*24+24]=im
    return sheet
base=dict(sk='sk',sk2='sk2',hair='br1',hair2='br2',top='rd',tops='rf1',pants='bl2',pants2='bl1',shoes='cr')
def S(**k): d=dict(base); d.update(k); return d
save(person(S(zip='cr',collar='cr')),'player')
save(person(S(hair='gr4',hair2='cr',top='d1',tops='k',pants='d1',pants2='k',shoes='k',skirt='d2',apron='gr2',bun=1,shawl='mv')),'guela')
save(person(S(sk='sk2',sk2='br3',hair='gr3',hair2='gr4',top='bl2',tops='bl1',stripes='bl3',pants='br1',pants2='d2',shoes='k',boots=1,cap='k',beard='gr4')),'pescador')
save(person(S(hair='k',hair2='d2',top='cr',tops='sa1',pants='d1',pants2='k',shoes='k',vest='d2',mous='d1',apron='wh',collar='wh')),'chigrero')
save(person(S(hair='oc1',hair2='oc2',top='gn2',tops='gn1',pants='bl1',pants2='k',shoes='rf1',collar='cr')),'neno')
# ====================================================== INTERIOR v2 (reuse v1 + extra props)
inn=Cv(256,176,'br2'); 
for y in range(48,176,6):
    inn.h(0,y,256,'br1'); off=(y//6)%3*11
    for x in range(off,256,34): inn.v(x,y,6,'br1')
inn.noise(0,48,256,128,'br3',0.06); inn.noise(0,48,256,128,'sa1',0.02)
inn.rect(0,0,256,48,'sa2'); inn.noise(0,0,256,30,'sa1',0.15)
for x in range(0,256,8): inn.v(x,28,20,'br1')
inn.rect(0,28,256,1,'br4'); inn.h(0,47,256,'d1'); inn.mul(0,48,256,6,0.7)
for sy in (8,20):
    inn.rect(120,sy+6,104,2,'br1'); inn.mul(120,sy+8,104,2,0.7)
    for x in range(122,222,4):
        col=R.choice(['gn1','gn1','gn2','br1','cr']); inn.rect(x,sy,2,6,col); inn.px(x,sy-1,'k'); inn.px(x,sy+2,'cr' if col!='cr' else 'rd')
inn.rect(16,6,40,18,'br1'); inn.rect(18,8,36,14,'cr'); text(inn,20,10,'SIDRA','rf1'); text(inn,20,16,'VILLAVI','gn1')
inn.rect(66,4,30,22,'cr'); inn.rect(67,5,28,20,'bl2'); text(inn,69,7,'SPORT','cr'); text(inn,69,13,'ING','cr'); inn.rect(80,13,12,10,'wh'); inn.h(80,17,12,'rd')
inn.rect(232,6,20,16,'d1'); inn.rect(234,8,16,11,'bl2'); inn.rect(235,9,6,4,'bl3'); inn.h(232,22,20,'gr1')   # TV
inn.rect(104,64,136,16,'br3'); inn.h(104,64,136,'br4'); inn.h(104,65,136,'sa1')
inn.rect(104,80,136,14,'br1')
for x in range(108,240,12): inn.v(x,80,14,'d2')
inn.h(104,94,136,'k'); inn.mul(104,95,136,4,0.6)
for x in (124,150,180,205): inn.rect(x,58,2,6,'gn1'); inn.px(x,57,'k'); inn.rect(x+4,61,2,3,'yl')
inn.rect(112,170,32,6,'k'); inn.rect(114,171,28,5,'br1')
inn.glow(170,40,90,'orr',0.25,0.8); inn.glow(60,100,90,'orr',0.12)
quant(inn.img().convert('RGB')).save(f'{OUT}/interior.png')
tb=Cv(24,20); tb.rect(1,2,22,9,'br3'); tb.h(1,2,22,'br4'); tb.h(1,10,22,'br1')
for x in (3,19): tb.rect(x,11,2,9,'d1')
tb.rect(10,0,2,6,'gn1'); tb.px(10,0,'k'); tb.rect(14,4,2,3,'yl'); tb.rect(6,5,2,3,'yl')
save(tb,'table')
tm=Cv(16,30); tm.rect(0,0,16,30,'gr3'); tm.v(15,0,30,'gr2'); tm.rect(2,2,12,5,'rd'); text(tm,2,3,'',  'cr')
for j in range(9,23,3): tm.rect(2,j,12,2,R.choice(['cr','rd','bl3','oc2'])); tm.px(14,j,'gr1')
tm.rect(2,25,12,3,'d1'); tm.h(0,29,16,'k'); text(tm,2,2,'',  'cr')
save(tm,'tabaco')
print('done',len(LIGHTS))
