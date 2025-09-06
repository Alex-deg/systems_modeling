import os
from functions import get_valid_input, additional_test

# F = {{x1,x2}, {z1,z2,z3,z4}, {y1,y2,y3,y4}, TRANS, OUT, z0}

# Формат записи: вместо x1 - 1, вместо y4 - 4 (то есть только цифра без буквы) 

TRANS = [
    [2, 3, 1, 4],
    [1, 1, 3, 2]
]

OUT = [
    [1, 1, 3, 4],
    [2, 2, 1, 3]
]

def check_x(value):
    x = int(value)
    if x < 1:
        raise ValueError("Значение x слишком маленькое")
    if x > len(TRANS):
        raise ValueError("Значение x слишком большое")
    return True

def check_y(value):
    y = int(value)
    if y < 1:
        raise ValueError("Значение y слишком маленькое")
    if y > len(OUT[0]):
        raise ValueError("Значение y слишком большое")
    return True

def check_z(value):
    z = int(value)
    if z < 1:
        raise ValueError("Значение z слишком маленькое")
    if z > len(TRANS[0]):
        raise ValueError("Значение z слишком большое")
    return True

if __name__ == "__main__":
    print('Введите начальные значения:')
    print('z = ', end='')
    z = input()
    z = get_valid_input('int', z, [check_z])
    while (True):
        if os.name == 'nt':
            os.system('cls')
        elif os.name == 'posix':
            os.system('clear')
        print('Для того чтобы завершить выполнение моделирования введите Enter')
        print('x = ', end='')
        x = input()
        if len(x) < 1:
            break
        x = get_valid_input('int', x, [check_x])
        z = TRANS[x - 1][z - 1]
        y = OUT[x - 1][z - 1]
        print(f"Текущее состояние:\nx = {x}, y = {y}, z = {z}")
        print('Для продолжения нажмите любую клавишу...')
        input()