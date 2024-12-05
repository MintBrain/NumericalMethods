import numpy as np
from sympy import symbols, simplify, latex
from sympy.parsing.sympy_parser import parse_expr
import matplotlib

matplotlib.use('TkAgg')

import matplotlib.pyplot as plt


def evaluate_lagrange(x_points, y_points, x_eval):
    """
    Вычисляет значение интерполяционного полинома Лагранжа в точке x_eval.
    :param x_points: Список узлов интерполяции (x).
    :param y_points: Список значений функции (y).
    :param x_eval: Точка, в которой вычисляем значение.
    :return: Значение полинома в точке x_eval.
    """
    n = len(x_points)
    result = 0
    for i in range(n):
        if y_points[i] == 0:
            continue

        L_i = 1
        for j in range(n):
            if i != j:
                L_i *= (x_eval - x_points[j]) / (x_points[i] - x_points[j])
        result += y_points[i] * L_i
    return result


def evaluate_newton(x_points, y_points, x_eval):
    """
    Вычисляет значение интерполяционного полинома Ньютона в точке x_eval.
    :param x_points: Список узлов интерполяции (x).
    :param y_points: Список значений функции (y).
    :param x_eval: Точка, в которой вычисляем значение.
    :return: Значение полинома в точке x_eval.
    """
    n = len(x_points)
    divided_diff = [y_points[:]]
    for level in range(1, n):
        diffs = []
        for i in range(n - level):
            diff = (divided_diff[level - 1][i + 1] - divided_diff[level - 1][i]) / (x_points[i + level] - x_points[i])
            diffs.append(diff)
        divided_diff.append(diffs)

    result = divided_diff[0][0]
    product = 1
    for level in range(1, n):
        product *= (x_eval - x_points[level - 1])
        result += divided_diff[level][0] * product

    return result

def plot_polynomials(x_points, y_points):
    """
    Строит графики интерполяционных полиномов Лагранжа и Ньютона.
    :param x_points: Узлы интерполяции (x).
    :param y_points: Значения функции в узлах (y).
    """
    x_range = np.linspace(min(x_points) - 1, max(x_points) + 1, 500)

    lagrange_values = [evaluate_lagrange(x_points, y_points, x) for x in x_range]
    newton_values = [evaluate_newton(x_points, y_points, x) for x in x_range]

    plt.figure(figsize=(10, 6))

    # Исходные точки
    plt.scatter(x_points, y_points, color="red", label="Узлы интерполяции", linewidths=6)

    # Полином Ньютона
    plt.plot(x_range, newton_values, label="Полином Ньютона", linestyle="-", linewidth=3)
    # Полином Лагранжа
    plt.plot(x_range, lagrange_values, label="Полином Лагранжа", linestyle="--", linewidth=3)
    # Настройка графика
    plt.title("Интерполяционные полиномы Лагранжа и Ньютона")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.axvline(0, color="black", linewidth=0.8, linestyle="--")
    plt.legend()
    plt.grid(True)

    # Показать график
    plt.ion()
    plt.show()
    # plt.draw()
    plt.pause(0.3)

