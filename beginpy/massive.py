p = [1, 2, 0, 0.4, 0.5, 0.6, 7, 8, 0.9, 10, 11, 0.12]
s = [1, 2, 3, 4, 0.5, 0.6, 7, 8, 9, 10]

def delete(a):
    for i in a:
        k = 0
        print(i)
        while 0<= i <= 1:
            a.remove(i)
            k +=1
    print(a)
delete(p)
#print("\n")
#delete(s)