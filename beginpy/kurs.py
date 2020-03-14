import math

def perevod(x):
    c = int(x)
    a = ''
    while c > 16:
        if c % 16 == 15:
            a = a + 'F'
        elif c % 16 == 14:
            a = a + 'E'
        elif (c % 16 == 13):
            a = a + 'D'
        elif (c % 16 == 12):
            a = a + 'C'
        elif (c % 16 == 11):
            a = a + 'B'
        elif (c % 16 == 10):
            a = a + 'A'
        else:
            a = a + str(c % 16)
        c = c // 16
    else:
        if c % 16 == 15:
            a = a + 'F'
        elif c % 16 == 14:
            a = a + 'E'
        elif (c % 16 == 13):
            a = a + 'D'
        elif (c % 16 == 12):
            a = a + 'C'
        elif (c % 16 == 11):
            a = a + 'B'
        elif (c % 16 == 10):
            a = a + 'A'
        else:
            a = a + str(c)
    return a[:: - 1]

def factorial(x):
    a = 0
    k = 0
    for i in x[::-1]:
        k +=1
        a += math.factorial(k)*int(i)
    return a

swap = ''
with open('file1.txt', 'r', encoding="utf-8") as f:
    swap = f.readlines()
f.close()
f = open("file2.txt", "w", encoding="utf-8")
for line in swap:
    line = line.split()
    A = line[0]
    B = line[1]
    f.write(A + ' ' + B + ' ')
    if A == '10':
        for i in range(2, 7):
            f.write(line[i])
            f.write('->')
            f.write(perevod(line[i]))
            f.write(' ')
        f.write('\n')
    if A == 'Факториальная':
        for i in range(2, 7):
            f.write(line[i])
            f.write('->')
            f.write(str(factorial(line[i])))
            f.write(' ')
        f.write('\n')
