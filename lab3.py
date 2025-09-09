import random
from math import sqrt, floor
from functions import get_valid_input, additional_test

# def compare_double(x, y, accuracy):
#     if abs(x - y) < accuracy:
#         return True
#     return False

def binary_insert(array, value):
    l = 0
    r = len(array) - 1
    mid = 0
    while l < r:
        mid = (l + r) // 2
        if array[mid] == value:
            return mid
        if value < array[mid]:
            r = mid
        elif value > array[mid]:
            l = mid + 1
    return mid

def get_statistic_series(sample):
    val_min = min(sample)
    val_max = max(sample)
    R = val_max - val_min
    n = len(sample)
    m = 30
    if n <= 500:
        m = round(n / 17)
    step = floor(R / m * 10) / 10
    intervals = [floor(val_min * 10) / 10]
    for i in range(1, m):
        intervals.append(intervals[i - 1] + step)
    n_j = [0] * len(intervals)
    p_j = []
    for i in range(len(sample)):
        index = binary_insert(intervals, sample[i])
        n_j[index] += 1
    for i in range(len(n_j)):
        p_j.append(n_j[i] / n)
        print(f"n_j[i] = {n_j[i]}\t\tp_j[i] = {p_j[i]}")
    



if __name__ == "__main__":
    print('Введите объем выборки')
    n = input()
    n = get_valid_input('int', n, [])
    result_sample = []
    for i in range(n):
        eps = random.random()
        if eps >= 0 and eps <= 0.5:
            result_sample.append(eps - 0.5)
        elif eps > 0.5 and eps <= 1:
            result_sample.append(1 - sqrt(2*(1 - eps)))

    for i in range(len(result_sample)):
        print(f"x{i + 1} = {result_sample[i]}")
    
    get_statistic_series(result_sample)
