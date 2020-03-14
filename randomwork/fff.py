import random

import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow
im = Image.new("RGB", (200,200), (255, 255, 255))
draw = ImageDraw.Draw(im)
for i in range(200):
    draw.point((i, 0), fill=(random.randint(1,256), random.randint(1,256),random.randint(1,256)))
    draw.point((0, i), fill=(random.randint(1,256), random.randint(1,256),random.randint(1,256)))
obj = im.load()
for i in range(1,200):
    for j in range(1,200):
        c = int((obj[i-1,j-1][0]+obj[i-1,j][0]+obj[i,j-1][0])/3)
        b = int((obj[i-1,j-1][1]+obj[i-1,j][1]+obj[i,j-1][1])/3)
        a = int((obj[i-1,j-1][2]+obj[i-1,j][2]+obj[i,j-1][2])/3)
        draw.point((i,j), (c,b,a))
im.show()