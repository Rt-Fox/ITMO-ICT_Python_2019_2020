print('____________________________')
print('|           MENU           |')
print('| 1) Ввод данных с нуля    |')
print('| 2) Вывод всего расписания|')
print('| 3) Дополнение расписания |')
print('| 4) Корректировка данных  |')
print('| 5) Сортировка по         |')
print('|   станции назначения     |')
print('| 6) Сортировка по         |')
print('|   времени отправления    |')
print('| 7) Вывод информации      |')
print('|   о поездах, отходящих   |')
print('| после введенного времени |')
print('| 8) Создание файла        |')
print('| 0) Выход                 |')
print('____________________________')

st = ''

while True:
    n = input('Выберете пункт меню: ')
    if n == '1':
        number = 0
        f = open("laba3.txt", "w", encoding="utf-8")
        while True:
            number = number + 1
            new = input(
                'Введите новую строку в формате: "Пункт назначения | Пометки (СВ/ПВ/КСВ) | Час отправления | Минуты отправления", если же вы уже ввели все данные введите "готово": ')
            if new == 'готово':
                f.close()
                break
            else:
                new = '%d'(number) + new + '\n'
                f.write(new)
    elif n == '2':
        f = open("laba3.txt", "r", encoding="utf-8")
        st += f.read()  # считать до конца файла
        print("File1: ", st)
        f.close()
    elif n == '3':
        f = open("laba3.txt", "a", encoding="utf-8")
        x = "да"
        while x == 'да':
            f.write(input(
                "введите данные в формате 'Пункт назначения | Пометки (СВ/ПВ/КСВ) | Час отправления (0-23) | Минуты отправления' "))
            f.write('\n')
            x = input("Хотите добавить информацию об еще 1 пункте назначения? (да/нет) ")
        else:
            f.close()
    elif n == '4':
        swap = []
        with open('laba3.txt', 'r', encoding="utf-8") as f:
            swap = f.readlines()
        for line in swap:
            print(line)
            x = input("Хотите изменить эту строчку? (да/нет)")
            if x == 'да':
                x = input("Введите новую строчку: ")
                swap[swap.index(line)] = x
        else:
            with open('laba3.txt', 'w', encoding="utf-8") as f:
                f.writelines(swap)
    elif n == '5':
        arr = []
        with open('laba3.txt', 'r', encoding="utf-8") as f:
            swap = f.readlines()
        for line in swap:
            name, top, hour, minute = line.split()
            arr.append((name, top, hour, minute))
        arr.sort()
        f.close()
        f = open("laba3.txt", "w", encoding="utf-8")
        for inf in arr:
            strok = inf[0] + ' ' + inf[1] + ' ' + inf[2] + ' ' + inf[3] + '\n'
            f.write(strok)
        f.close()
    elif n == '6':
        arr = []
        with open('laba3.txt', 'r', encoding="utf-8") as f:
            swap = f.readlines()
        for line in swap:
            name, top, hour, minute = line.split()
            x = int(hour) * 100 + int(minute)
            arr.append((name, top, hour, minute, x))
        arr.sort(key=lambda s: s[4])
        f.close()
        f = open("laba3.txt", "w", encoding="utf-8")
        for inf in arr:
            strok = inf[0] + ' ' + inf[1] + ' ' + inf[2] + ' ' + inf[3] + '\n'
            f.write(strok)
        f.close()
    elif n == '7':
        time = input("Введите время в формате 0000 (первые две цифры час, последние - минуты, без пробелов)")
        arr = []
        with open('laba3.txt', 'r', encoding="utf-8") as f:
            swap = f.readlines()
        for line in swap:
            name, top, hour, minute = line.split()
            x = int(hour) * 100 + int(minute)
            arr.append((name, top, hour, minute, x))
        arr.sort(key=lambda s: s[4])
        f.close()
        for i in arr:
            if i[4] >= int(time):
                print(i[0:4])
    elif n == '8':
        name = input("Введите название нового файла")
        f = open("laba3.txt", "r", encoding="utf-8")
        st += f.read()  # считать до конца файла
        f.close()
        f = open('%s'(name), 'w', encoding="utf-8")
        f.write(st)
        f.close()
    elif n == '0':
        break
    else:
        n = input('Такой команды не существует, повторите запрос: ')
