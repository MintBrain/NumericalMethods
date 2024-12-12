import matplotlib.pyplot as plt
import numpy as np


def solve_linear_system(A, b):
    """
    Решение системы линейных уравнений Ax = b методом Гаусса.
    :param A: Квадратная матрица коэффициентов.
    :param b: Вектор правой части.
    :return: Вектор решений x.
    """
    n = len(A)
    # Прямой ход
    for i in range(n):
        # Нормализация строки
        for j in range(i + 1, n):
            factor = A[j][i] / A[i][i]
            for k in range(i, n):
                A[j][k] -= factor * A[i][k]
            b[j] -= factor * b[i]

    # Обратный ход
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(A[i][j] * x[j] for j in range(i + 1, n))) / A[i][i]
    return x


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
    linear_coeffs = least_squares(x, y, degree=1)
    print("Линейная аппроксимация:")
    print_polynomial(linear_coeffs)

    # Квадратичная аппроксимация (степень 2)
    quadratic_coeffs = least_squares(x, y, degree=2)
    print("Квадратичная аппроксимация:")
    print_polynomial(quadratic_coeffs)

    # Построение аппроксимирующего полинома
    print("\nПример вычислений для x = 1.5:")
    print(f"Линейная аппроксимация: {evaluate_polynomial(linear_coeffs, 1.5):.3f}")
    print(f"Квадратичная аппроксимация: {evaluate_polynomial(quadratic_coeffs, 1.5):.3f}")


def test():
    # Ввод данных
    x_values = [-1, 0, 1, 2, 3]
    y_values = [-4, -1, 2, 5, 8]
    program(x_values, y_values)


def main():
    pass

if __name__ == '__main__':
    test()
