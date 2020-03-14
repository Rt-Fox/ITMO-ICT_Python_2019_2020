#15

m = 10
pi = 3.1415927
print("m = ", m)
print("m = %d" % m)
print("%7d" % m)
print("pi = ", pi)
print("%.3f" % pi)
print("%10.4f\n" % pi)
print("m = {}, pi = {}".format(m, pi))
ch = 'A'
print("ch = %c" % ch)
s = "Hello"
print("s = %s" % s)
print("\n\n")
code = input("Enter your position number in group: ")
n1, n2 = input("Enter two numbers splitted by space:").split()
d, m, y = input("Enter three numbers splitted by\'.\': ").split('.')
print("{} + {} = {}".format(n1, n2, float(n1) + float(n2)))
print("Your birthday is %s.%s.%s and you are %d in the group list" % (d, m, y, int(code)))
m = 10
pi = 3.1415927
#16
print("m = %.4d, pi = %.3f" % (m, pi))
#17
print("m = {0}; pi = {1}".format(m, pi))

# 18
year = input("Введите номер курса: ")
print(year)

# 19
r1, m1, p1 = input("Введите ваши балы за 3 экзамена через запятую: русский, математика, физика: ").split(',')
print(r1, m1, p1, sep=" ")

# 20
x = 20 % 8 + 2
z = input("Введите 12-разрядное число в системе счисления " + str(x) + ":")
print(int(z, x))

# 21
x = int(input("Введите число "))
z = (x << 1) >> 1
print(z)
