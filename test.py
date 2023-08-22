import time
a = 0
b = 0
while True:
    while a <= 3:
        time.sleep(1)
        a += 1
        print(a)
        if a == 3:
            b += 1
            a = 0
        if b == 2:
            print("Всё")