#8
'''
 Логические операции
'''
f = True
g = False
print("f: ", f)
print("not f: ", not f)
print("f and g: ", f and g)
print("f or g: ", f or g)
print("f == g: ", f == g)
print("f != g: ", f != g)
print("\n")
h = 3
i = 5
print("h = ", h)
print("i = ", i)
print("h > i: ", h > i)
print("h < i: ", h < i)
print("h >= i: ", h >= i)
print("0 < h <= i: ", 0 < h <= i)
print("\n\n")

'''
 Побитовые операции
'''
j = 7
k = 20
print("j = %d; j in binary format: %s" % (j, bin(j)))
print("k = %d; k in binary format: %s" % (k, bin(k)))
print("j & k: %d; binary: %s" % (j & k, bin(j & k)))  # побитовое AND
print("j | k: %d; binary: %s" % (j | k, bin(j | k)))  # побитовое OR
print("j ^ k: %d; binary: %s" % (j ^ k, bin(j ^ k)))  # побитовое XOR
print("~k: %d; binary: %s" % (~k, bin(~k)))  # инверсия двоичного числа
print("k>>1: %d; binary: %s" % (k >> 1, bin(k >> 1)))  # сдвиг на один бит вправо
print("k<<1: %d; binary: %s" % (k << 1, bin(k << 1)))  # сдвиг на один бит влево
print("\n\n")
#9
A = 5
B = 10
C = True
D = False
#10
print(not (C and D))
print(C and D or (not (C and D)))
print(not C or D)
#11
print(A <= B)
print(A > B or A == B)
print(not (A < B))
#12
s = 154
p = 6
print("s = %d; j in binary format: %s" % (s, bin(s)))
print("p = %d; k in binary format: %s" % (p, bin(p)))
#13
print("s | p: %d; binary: %s" % (s | p, bin(s | p)))  # побитовое OR
s = s|p
#14
print("s>>2: %d; binary: %s" % (s >> 2, bin(s >> 2)))
print("p>>2: %d; binary: %s" % (p >> 2, bin(p >> 2)))

