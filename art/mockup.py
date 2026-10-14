from PIL import Image
import numpy as np, json, math
O='art/out2/'; L=lambda n:Image.open(O+n+'.png').convert('RGBA')
W=Image.open(O+'plaza_ground.png').convert('RGBA')
items=[('barrel',200,152),('barrel',284,152),('barrel',160,160),('crate',222,140),('crate',226,134),('vending',318,140),('bike',360,140),('butano',426,138),('hydrangea',92,140),('hydrangea',390,140),('tree',240,214),('bench',150,222),('lamp',240,286)]
def fr(n,col,row): return L(n).crop((col*24,row*32,col*24+24,row*32+32))
chars=[(fr('guela',0,2),170,222),(fr('neno',1,0),206,170),(fr('player',1,1),276,246),(fr('pescador',0,1),300,196)]
draw=[(L(n),x,y) for n,x,y in items]+chars
sh=L('shadow')
for im,x,y in sorted(draw,key=lambda t:t[2]):
    if im.size[0]==24: W.alpha_composite(sh,(x-8,y-4))
    W.alpha_composite(im,(x-im.size[0]//2,y-im.size[1]))
W.alpha_composite(L('plaza_fg'))
a=np.asarray(W.convert('RGB')).astype(float)/255
a*=np.array([0.85,0.66,0.58])
ys,xs=np.mgrid[0:a.shape[0],0:a.shape[1]]
for x,y,k in json.load(open(O+'meta.json'))['lights']+[[240,262,'lamp']]:
    r=48 if k=='lamp' else 30; s=0.5 if k!='win' else 0.25
    f=np.clip(1-np.hypot(xs-x,ys-y)/r,0,1)**2*s; f=np.round(f*6)/6
    a+=f[...,None]*np.array([214,150,82])/255
img=Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8)).crop((80,40,400,220))
v=L('vignette'); img=img.convert('RGBA'); img.alpha_composite(v)
img.convert('RGB').resize((1280,720),Image.NEAREST).save('shots/v2_mockup.png')
img.convert('RGB').save('art/out2/mockup_1x.png')
