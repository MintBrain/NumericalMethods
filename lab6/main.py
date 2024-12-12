from colorsys import yiq_to_rgb

import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable


# Решение системы уравнений методом Крамера
def determinant(matrix):
    """Вычисление определителя 3x3 матрицы."""
    return (matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1]) -
            matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0]) +
            matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0]))

def linear_least_squares(x_values, y_values):
    """
    Линейная аппроксимация методом наименьших квадратов.
    :param x_values: Список значений x.
    :param y_values: Список значений y.
    :return: Коэффициенты a и b линейной функции y = ax + b.
    """
    n = len(x_values)

    # Проверяем, что длины списков совпадают
    if n != len(y_values):
        raise ValueError("Списки x_values и y_values должны быть одинаковой длины.")

    # Подготовка таблицы
    x_squared = [x ** 2 for x in x_values]  # x^2
    x_y = [x_values[i] * y_values[i] for i in range(n)]  # x * y

    # Суммы для системы уравнений
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_x_squared = sum(x_squared)
    sum_x_y = sum(x_y)

    # Вывод таблицы
    print("Расчетная таблица линейной аппроксимации")
    table = PrettyTable()
    table.field_names = ["i", "x", "y", "x^2", "x * y"]
    for i in range(n):
        table.add_row([i + 1, x_values[i], y_values[i], x_squared[i], x_y[i]])
    table.add_row(["Σ", sum_x, sum_y, sum_x_squared, sum_x_y])
    print(table)

    # Построение системы уравнений
    # a * sum_x_squared + b * sum_x = sum_x_y
    # a * sum_x + b * n = sum_y
    A = [[sum_x_squared, sum_x], [sum_x, n]]
    B = [sum_x_y, sum_y]

    # Решение системы линейных уравнений методом Крамера
    det_A = A[0][0] * A[1][1] - A[0][1] * A[1][0]
    det_a = B[0] * A[1][1] - B[1] * A[0][1]
    det_b = A[0][0] * B[1] - A[1][0] * B[0]

    if det_A == 0:
        raise ValueError("Детерминант системы равен нулю. Аппроксимация невозможна.")

    a = det_a / det_A
    b = det_b / det_A

    # Формула аппроксимации
    print(f"Линейная аппроксимация: y = {a:.3f}x + {b:.3f}")
    return a, b


def validate_approximation(x_values, y_values, a, b):
    """
    Проверка качества аппроксимации.
    :param x_values: Список значений x.
    :param y_values: Список значений y.
    :param a: Коэффициент наклона прямой.
    :param b: Свободный член.
    """
    n = len(x_values)
    predicted_y = [a * x + b for x in x_values]  # Рассчитанные значения y
    errors = [y_values[i] - predicted_y[i] for i in range(n)]  # Отклонения

    # Вывод таблицы проверки
    table = PrettyTable()
    table.field_names = ["i", "x", "y (исходное)", "y (аппроксимация)", "Ошибка"]
    for i in range(n):
        table.add_row([i + 1, x_values[i], y_values[i], round(predicted_y[i], 3), round(errors[i], 3)])
    print("\nПроверка линейной аппроксимации:")
    print(table)

    # Сумма квадратов ошибок
    sum_squared_error = sum(e ** 2 for e in errors)
    print(f"Сумма квадратов ошибок: {sum_squared_error:.3f}")


def polynomial_least_squares(x_values, y_values):
    """
    Полиномиальная аппроксимация методом наименьших квадратов.
    :param x_values: Список значений x.
    :param y_values: Список значений y.
    :return: Коэффициенты a, b, c полинома y = ax^2 + bx + c.
    """
    n = len(x_values)

    if n != len(y_values):
        raise ValueError("Списки x_values и y_values должны быть одинаковой длины.")

    # Вычисление значений для таблицы
    x_squared = [x ** 2 for x in x_values]
    x_cubed = [x ** 3 for x in x_values]
    x_fourth = [x ** 4 for x in x_values]
    x_y = [x_values[i] * y_values[i] for i in range(n)]
    x_squared_y = [x_squared[i] * y_values[i] for i in range(n)]

    # Суммы для системы уравнений
    sum_x = sum(x_values)
    sum_y = sum(y_values)
    sum_x_squared = sum(x_squared)
    sum_x_cubed = sum(x_cubed)
    sum_x_fourth = sum(x_fourth)
    sum_x_y = sum(x_y)
    sum_x_squared_y = sum(x_squared_y)

    # Вывод таблицы
    print("Расчетная таблица полиномиальной аппроксимации")
    table = PrettyTable()
    table.field_names = ["i", "x", "y", "x^2", "x^3", "x^4", "x*y", "x^2*y"]
    for i in range(n):
        table.add_row([i + 1, x_values[i], y_values[i], x_squared[i], x_cubed[i], x_fourth[i], x_y[i], x_squared_y[i]])
    table.add_row(["Σ", sum_x, sum_y, sum_x_squared, sum_x_cubed, sum_x_fourth, sum_x_y, sum_x_squared_y])
    print(table)

    # Система линейных уравнений
    A = [
        [sum_x_fourth, sum_x_cubed, sum_x_squared],
        [sum_x_cubed, sum_x_squared, sum_x],
        [sum_x_squared, sum_x, n]
    ]
    B = [sum_x_squared_y, sum_x_y, sum_y]

    det_A = determinant(A)
    if det_A == 0:
        raise ValueError("Детерминант системы равен нулю. Аппроксимация невозможна.")

    A_a = [[B[0], A[0][1], A[0][2]],
           [B[1], A[1][1], A[1][2]],
           [B[2], A[2][1], A[2][2]]]

    A_b = [[A[0][0], B[0], A[0][2]],
           [A[1][0], B[1], A[1][2]],
           [A[2][0], B[2], A[2][2]]]

    A_c = [[A[0][0], A[0][1], B[0]],
           [A[1][0], A[1][1], B[1]],
           [A[2][0], A[2][1], B[2]]]

    det_a = determinant(A_a)
    det_b = determinant(A_b)
    det_c = determinant(A_c)

    a = det_a / det_A
    b = det_b / det_A
    c = det_c / det_A

    print(f"Полиномиальная аппроксимация: y = {a:.3f}x^2 + {b:.3f}x + {c:.3f}")
    return a, b, c


def validate_polynomial_approximation(x_values, y_values, a, b, c):
    """
    Проверка качества полиномиальной аппроксимации.
    :param x_values: Список значений x.
    :param y_values: Список значений y.
    :param a: Коэффициент при x^2.
    :param b: Коэффициент при x.
    :param c: Свободный член.
    """
    n = len(x_values)
    predicted_y = [a * x**2 + b * x + c for x in x_values]  # Рассчитанные значения y
    errors = [y_values[i] - predicted_y[i] for i in range(n)]  # Отклонения

    # Вывод таблицы проверки
    table = PrettyTable()
    table.field_names = ["i", "x", "y (исходное)", "y (аппроксимация)", "Ошибка"]
    for i in range(n):
        table.add_row([i + 1, x_values[i], y_values[i], round(predicted_y[i], 3), round(errors[i], 3)])
    print("\nПроверка полиномиальной аппроксимации:")
    print(table)

    # Сумма квадратов ошибок
    sum_squared_error = sum(e ** 2 for e in errors)
    print(f"Сумма квадратов ошибок: {sum_squared_error:.3f}")


def program(x, y):
    # Линейная аппроксимация (степень 1)
    linear_coeffs = linear_least_squares(x, y)
    validate_approximation(x, y, linear_coeffs[0], linear_coeffs[1])
    print()
    polynomial_coeffs = polynomial_least_squares(x, y)
    validate_polynomial_approximation(x, y, polynomial_coeffs[0], polynomial_coeffs[1], polynomial_coeffs[2])


def test():
    # 9 вариант
    # x_values = [-1, 0, 1, 2, 3]
    # y_values = [-4, -1, 2, 5, 8]

    # линейная в лекции
    # x_values = [0, 1,2, 4]
    # y_values = [0.2, 0.9, 2.1, 3.7]

    # полиномиальная в лекции
    x_values = [-2,-1,0,1,2]
    y_values = [6,2,-1,-2,-1]
    program(x_values, y_values)


def main():
    pass

if __name__ == '__main__':
    test()