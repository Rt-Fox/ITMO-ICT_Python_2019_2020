import math


def y(x, n=0):
    z1 = 1
    a = math.pow(-1, n) * math.pow(x, 2 * n) / math.factorial(2 * n)
    while (abs(a) > math.pow(10, -3)):
        n = n + 1
        a = -(a * x**2) / (2*n*(2*n-1))
        z1 = z1 + a
    return z1


def z(x):
    z = math.cos(x)
    return z


for i in range(11):
    print(i , end="   ")
    print("%.4f" %(y(i)), end="   ")
    print("%.4f"%(z(i)))
