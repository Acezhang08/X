import sys, skia
from PIL import Image
# usage: sheet.py out.png file1 file2 ... (2 columns, half-size)
files = sys.argv[2:]
cols = 2; w, h = 960, 540
rows = (len(files) + cols - 1) // cols
im = Image.new("RGB", (cols*w, rows*h), "white")
for i, f in enumerate(files):
    a = Image.open(f).convert("RGB").resize((w, h))
    im.paste(a, ((i % cols)*w, (i//cols)*h))
im.save(sys.argv[1])
