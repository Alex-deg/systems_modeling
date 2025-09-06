from math import e, cos, sin
import time
import os
import matplotlib.pyplot as plt

c = 6000
u = 50 
T = 10
h_tv = 8590
g = 9.81

def print_graphics(dict, title, x_label, y_label):

    plt.figure(figsize=(10, 6))
    plt.plot(dict.keys(), dict.values(), 'o-', linewidth=2, markersize=8)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    #plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def solver(h):

    x1 = {0: 100}
    x2 = {0: 0}
    x3 = {0: 1200}

    i = h

    while (i <= T):
        r = 0.1 * e ** (-x1[round(i - h,10)] / h_tv)
        x1[round(i,10)] = x1[round(i - h,10)] + x2[round(i - h,10)] * h
        x2[round(i,10)] = x2[round(i - h,10)] + (c*u/x3[round(i - h,10)] - g - r*x2[round(i - h,10)]*x2[round(i - h,10)]/x3[round(i - h,10)]) * h
        x3[round(i,10)] = x3[round(i - h,10)] - u * h
        i += h
    return [x1, x2, x3]

def check_char(char):
    if len(char) > 1:\
        raise ValueError(f"Длина символа = {len(char)}, а должна быть равна 1")
    if not (ord(char) == 110 or ord(char) == 121):
        raise ValueError('Символ не входит в множество ответов {y, n}')
    return True

def check_step(message):
    h = float(message)
    if h >= T:
        raise ValueError(f"Введенное значение h = {h} больше или равно интервалу интегрирования T = {T}")
    if h - 0.000001 < 0:
        raise ValueError(f"Значение шага не обоснованно малое\nПри введенном значении объем занимаемой оперативной памяти = {((T/h) * 3 * 4) / (1024*1024*1024)} Гб")
    return True

def additional_test(array, message):
    for el in array:
        flag = el(message)
        if not flag:
            return False
    return True

def get_valid_input(type, message, arr_of_checking_functions = []):
    while True:
        try:
            if type == 'float' and additional_test(arr_of_checking_functions, message):
                return float(message)
            elif type == 'int' and additional_test(arr_of_checking_functions, message):
                return int(message)
            elif type == 'char' and additional_test(arr_of_checking_functions, message):
                return message
        except ValueError as err:
            if os.name == 'nt':
                os.system('cls')
            elif os.name == 'posix':
                os.system('clear')
            if len(str(err)) > 0:
                print(str(err))
            else:
                print(f"Неверный ввод! Введенное выражение не соответствует типу {type} или не прошло проверку")
            print('Введите значение заново:')
            message = input()


if __name__ == "__main__":
    
    productivity_by_time = {}
    productivity_by_accuracy = {}

    print('Введите шаг интегрирования')
    h = input()
    h = get_valid_input('float', h, [check_step])

    cur_value = 0
    prev_value = 0

    graph_choise = 'y'

    values_at_the_reference_step = []

    while(True):

        start_time = time.time()
        list_of_values = solver(h)
        end_time = time.time()
        productivity_by_time[h] = (end_time-start_time) * 1000
        
        cur_value = list(list_of_values[0].values())[-1]

        error = abs(cur_value - prev_value) / cur_value

        productivity_by_accuracy[h] = error

        print(f"x1[T] = {cur_value}")
        print(f"Относительная погрешность = {error}")

        print('Вывести графики? y/n')
        graph_choise = input()
        graph_choise = get_valid_input('char', graph_choise, [check_char])
        if graph_choise == 'y':
            for i in range(len(list_of_values)):
                print_graphics(list_of_values[i], f"График x{i + 1}", 'T, c', f"x{i + 1}")

        if error <= 0.01:
            print(f"Оптимальный шаг h = {h * 2}")
            break
        else:
            h /= 2
            prev_value = cur_value
            values_at_the_reference_step = list_of_values

    for i in range(len(values_at_the_reference_step)):
        print_graphics(values_at_the_reference_step[i], f"График x{i + 1} при оптимальном шаге", 'T, c', f"x{i + 1}")

    print_graphics(productivity_by_time, 'Трудоемкость от h', 'h', 'Время выполнения программы, мс')
    print_graphics(productivity_by_accuracy, 'Точность от h', 'h', 'Погрешность, %')