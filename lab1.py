from math import e, cos, sin
import time

import matplotlib.pyplot as plt


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

    c = 6000
    u = 50 
    T = 10
    h_tv = 8590
    g = 9.81

    x1 = {0: 100}
    x2 = {0: 0}
    x3 = {0: 1200}

    i = h

    while (i <= T):
        r = 0.1 * e ** (-x1[i - h] / h_tv)
        x1[i] = x1[i - h] + x2[i - h] * h
        x2[i] = x2[i - h] + (c*u/x3[i - h] - g - r*x2[i - h]*x2[i - h]/x3[i - h]) * h
        x3[i] = x3[i - h] - u * h
        i += h
    
    return [x1, x2, x3]

def check_char(char):
    if len(char) > 1:
        return False
    if not (ord(char) == 110 or ord(char) == 121):
        return False
    return True

def get_valid_input(type, message, arr_of_checking_functions = []):
    while True:
        flag = False
        try:
            for el in arr_of_checking_functions:
                flag = el(message)
                if not flag:
                    break
            if flag:
                if type == 'float':
                    return float(message)
                elif type == 'int':
                    return int(message)
                elif type == 'char':
                    return message
        except ValueError:
            if flag:
                print(f"Неверный ввод! Введенное выражение не соответствует типу {type}")
            elif not flag:
                print('Введенное сообщение не прошло проверку')
            print('Введите заново:')
            message = input()


if __name__ == "__main__":
    
    productivity_by_time = {}
    productivity_by_accuracy = {}

    print('Введите шаг интегрирования')
    h = float(input())
    get_valid_input('float', h)

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

        print(cur_value)
        print(error)

        print('Вывести графики? y/n')
        graph_choise = input()
        get_valid_input('char', graph_choise, [check_char])
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

    print(productivity_by_accuracy)
    print(productivity_by_time)
    print_graphics(productivity_by_time, 'Трудоемкость от h', 'h', 'Время выполнения программы, мс')
    print_graphics(productivity_by_accuracy, 'Точность от h', 'h', 'Погрешность, %')