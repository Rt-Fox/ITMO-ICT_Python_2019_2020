# lab_02_06.py
z = input("Введите шестнадцетиричное число на восемь разрядов: ")
z = int(z, 16)

if z >= 0:
    a = bin(z)
    print(a.replace('0b', '0'))
else:
    a = list(bin(-z))[2:]
    for i in range(0, len(a)):
        if a[i] == '0':
            a[i] = 1
        else:
            a[i] = 0
    i = len(a) - 1
    a[i] = a[i] + 1
    while (a[i] > 1) and (i > 0):
        a[i] = a[i] % 2
        a[i - 1] = a[i - 1] + 1
        i = i - 1
    print(1,end = "")
    if (a[i] > 1) and i == 0:
        print(1,end = "")
    for q in range(0, len(a)):
        print(a[q], end = "")
