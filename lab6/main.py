import matplotlib.pyplot as plt
import numpy as np
from prettytable import PrettyTable


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
    print("\nПроверка аппроксимации:")
    print(table)

    # Сумма квадратов ошибок
    sum_squared_error = sum(e ** 2 for e in errors)
    print(f"\nСумма квадратов ошибок: {sum_squared_error:.3f}")

def least_squares(x_values, y_values, degree):
    """
    Метод наименьших квадратов для нахождения полиномиальной аппроксимации.
    :param x_values: Список значений x.
    :param y_values: Список значений y.
    :param degree: Степень полинома.
    :return: Коэффициенты аппроксимирующего полинома.
    """
    n = len(x_values)
    # Матрица для системы нормальных уравнений
    A = [[sum(x ** (i + j) for x in x_values) for j in range(degree + 1)] for i in range(degree + 1)]
    b = [sum(y * (x ** i) for x, y in zip(x_values, y_values)) for i in range(degree + 1)]

    # Решаем систему линейных уравнений
    coefficients = solve_linear_system(A, b)
    return coefficients


def evaluate_polynomial(coefficients, x):
    """
    Вычисление значения полинома в точке x.
    :param coefficients: Коэффициенты полинома.
    :param x: Точка, в которой вычисляется значение.
    :return: Значение полинома.
    """
    return sum(c * x ** i for i, c in enumerate(coefficients))


def print_polynomial(coefficients):
    """
    Форматирует полином в виде строки.
    :param coefficients: Коэффициенты полинома.
    """
    terms = [f"{c:.3f}x^{i}" if i > 0 else f"{c:.3f}" for i, c in enumerate(coefficients)]
    print(" + ".join(terms).replace("x^1", "x"))


def program(x, y):
    # Линейная аппроксимация (степень 1)
    linear_coeffs = linear_least_squares(x, y)
    validate_approximation(x, y, linear_coeffs[0], linear_coeffs[1])
    # print("Линейная аппроксимация:")
    # print_polynomial(linear_coeffs)
    #
    # # Квадратичная аппроксимация (степень 2)
    # quadratic_coeffs = least_squares(x, y, degree=2)
    # print("Квадратичная аппроксимация:")
    # print_polynomial(quadratic_coeffs)
    #
    # # Построение аппроксимирующего полинома
    # print("\nПример вычислений для x = 1.5:")
    # print(f"Линейная аппроксимация: {evaluate_polynomial(linear_coeffs, 1.5):.3f}")
    # print(f"Квадратичная аппроксимация: {evaluate_polynomial(quadratic_coeffs, 1.5):.3f}")


def test():
    # Ввод данных
    # x_values = [-1, 0, 1, 2, 3]
    # y_values = [-4, -1, 2, 5, 8]
    x_values = [0, 1,2, 4]
    y_values = [0.2, 0.9, 2.1, 3.7]
    program(x_values, y_values)


def main():
    pass

if __name__ == '__main__':
    test()
