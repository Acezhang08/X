import sys,glob
from PIL import Image
fs=sorted(glob.glob(sys.argv[1]+'/t*.png')); w,h=640,360; cols=3; rows=(len(fs)+cols-1)//cols
S=Image.new('RGB',(cols*w,rows*h))
for i,f in enumerate(fs): S.paste(Image.open(f).convert('RGB').resize((w,h)),((i%cols)*w,(i//cols)*h))
S.save(sys.argv[1]+'/sheet.png')
