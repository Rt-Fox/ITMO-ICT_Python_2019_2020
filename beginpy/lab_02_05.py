import itertools

x = input("Введите любые символы: ")
c = list()
for i in range (1, len(x) + 1):
    c = c + list(map(''.join,itertools.permutations(x,i)))
print(set(c))

#lab_02_07.py
x = input("ВВедите число в 12ричной с.с.: ")
c = int(x, 12)
a = ''
while c > 0:
    if (c%14 == 13):
        a = a + 'D'
    elif (c%14 == 12):
        a = a + 'C'
    elif (c % 14 == 11):
        a = a + 'B'
    elif (c % 14 == 10):
        a = a + 'A'
    else:
        a = a + str(c%14)
    c = (c//14)
print(a[:: - 1])
