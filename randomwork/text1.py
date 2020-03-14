import PIL.ImageDraw as ImageDraw,PIL.Image as Image, PIL.ImageShow as ImageShow
img = Image.new('RGB', (600, 600), (255, 255, 255))
draw = ImageDraw.Draw(img)
f = open('text.txt', 'r')
l = [line.split(',') for line in f]
for i in range(len(l)):
    if int(l[i][2]) > 1000:
        l[i][2] = (int(l[i-1][2])+int(l[i+1][2]))/2
    print(i, int(l[i][2]))
    if l[i][0] == 'SINGLE':
        a = 'RED'
    elif l[i][0] == 'INTERRUPT':
        a = 'BLUE'
    else:
        a = 'GREEN'
    draw.point((i, int(l[i][2])), fill=(0,0,0))
    draw.point((i, int(l[i][1])), fill= a)
img.show()