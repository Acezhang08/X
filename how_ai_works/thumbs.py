from PIL import Image, ImageDraw, ImageFont
BG="#16181D"; BLUE="#58C4DD"; YELLOW="#F5D547"; GREEN="#83C167"; WHITE="#ECECEC"; GREY="#6B7080"
SER="/usr/share/fonts/truetype/cmu/cmunrm.ttf"; MONO="/usr/share/fonts/truetype/jetbrains-mono/JetBrainsMono-Bold.ttf"
def f(p,s): return ImageFont.truetype(p,s)
def rr(d,box,col,fill=None,w=6,r=18):
    d.rounded_rectangle(box,radius=r,outline=col,width=w,fill=fill)
def ctext(d,xy,t,font,fill):
    d.text(xy,t,font=font,fill=fill,anchor="mm")
def mix(c,a):
    c=tuple(int(c[i:i+2],16) for i in (1,3,5)); b=(0x16,0x18,0x1D)
    return tuple(int(c[i]*a+b[i]*(1-a)) for i in range(3))
# A
im=Image.new("RGB",(1280,720),BG); d=ImageDraw.Draw(im)
ctext(d,(640,150),"IT THINKS NOW",f(SER,128),WHITE)
words=["The","cat","sat"," ","on","the"]
xs=[50,220,390,None,810,985]
for w,x in zip(words,xs):
    if x is None: continue
    rr(d,(x,330,x+150,470),BLUE,mix(BLUE,.18)); ctext(d,(x+75,400),w,f(MONO,56),BLUE)
bx=(560,320,720,480); d.rounded_rectangle((575,325,725,475),radius=60,outline=YELLOW,width=7,fill=mix(YELLOW,.18))
for i in range(3): d.ellipse((605+i*40-13,400-13,605+i*40+13,400+13),fill=YELLOW)
im.save("thumbnail_A.png")
# B
im=Image.new("RGB",(1280,720),BG); d=ImageDraw.Draw(im)
d.text((50,100),"WHAT CHANGED?",font=f(SER,118),fill=WHITE,anchor="lm")
rr(d,(50,215,310,355),GREY,mix(GREY,.2)); ctext(d,(180,285),"12%",f(SER,100),GREY)
d.line((330,285,420,285),fill=WHITE,width=8); d.polygon([(440,285),(410,262),(410,308)],fill=WHITE)
rr(d,(450,195,830,355),YELLOW,mix(YELLOW,.18),w=8); ctext(d,(640,275),"74%",f(SER,130),YELLOW)
im.save("thumbnail_B.png")
