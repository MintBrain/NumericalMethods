import re
from typing import Literal

import sympy as sp

from lab1.funcs import Func

def choose_equation_type() -> int:
    print("Выберите тип уравнения:")
    print("1. Кубическое уравнение ax^3 + bx^2 + cx + d = 0")
    print("2. Пользовательское уравнение")

    equation_type = input("Введите номер типа уравнения (1 или 2): ")
    if equation_type not in ["1", "2"]:
        print("Некорректный ввод. Попробуйте снова.")
        return choose_equation_type()

    return int(equation_type)


def get_coefficients():
    while True:
        try:
            a = float(input("Введите коэффициент a для x^3: "))
            if a == 0:
                print("Коэффициент 'a' не может быть равен нулю. Пожалуйста, введите значение, отличное от нуля.")
                continue

            b = float(input("Введите коэффициент b для x^2: "))
            c = float(input("Введите коэффициент c для x: "))
            d = float(input("Введите свободный член d: "))
            return a, b, c, d
        except ValueError:
            print("Ошибка ввода, пожалуйста, введите числовые значения.")


def parse_equation(equation: str) -> Func:
    """Парсит строку уравнения и возвращает коэффициенты (a, b, c, d) для кубического уравнения."""
    # Приведение уравнения к стандартному виду (ax^3 + bx^2 + cx + d = 0)
    equation = equation.replace(" ", "").replace("=", "-(").replace("/(", ")*1/(")

    # Используем sympy для обработки уравнений
    x = sp.symbols('x')
    expr = sp.sympify(equation)  # Преобразуем строку в выражение sympy

    # Приводим уравнение к стандартному виду
    standard_form = sp.expand(expr)

    # Получаем коэффициенты для кубического уравнения
    coeffs = sp.Poly(standard_form, x).all_coeffs()

    # Дополняем до 4 коэффициентов
    while len(coeffs) < 4:
        coeffs.insert(0, 0)

    a, b, c, d = [float(coef) for coef in coeffs]

    return Func(a, b, c, d)


def get_user_equation():
    """Запрашивает у пользователя уравнение, парсит его и возвращает экземпляр класса Func."""
    while True:
        equation = input("Введите уравнение (например, (x + 1)^2 = 1/x): ")
        try:
            return parse_equation(equation)
        except Exception as e:
            print(f"Ошибка: {e}")
            print("Попробуйте ввести уравнение снова.")


def get_precision() -> float:
    while True:
        try:
            precision = float(input("Введите точность для вычислений (например: 0.01): "))
            if precision <= 0:
                print('Значение должно быть больше 0')
                continue
            return precision
        except ValueError:
            print("Ошибка ввода, пожалуйста, введите числа.")


def get_bisection_params() -> tuple[float, float]:
    """Запрашивает у пользователя границы интервала для метода бисекции."""
    while True:
        try:
            a = float(input("Введите начальное значение интервала (a): "))
            b = float(input("Введите конечное значение интервала (b): "))
            if a >= b:
                print("Начало интервала должно быть меньше конца. Попробуйте снова.")
                continue
            return a, b
        except ValueError:
            print("Ошибка ввода, пожалуйста, введите числа.")

def get_newton_params() -> tuple[float]:
    """Запрашивает у пользователя начальное приближение для метода Ньютона."""
    while True:
        try:
            initial_guess = float(input("Введите начальное приближение для метода Ньютона: "))
            return initial_guess,
        except ValueError:
            print("Ошибка ввода, пожалуйста, введите число.")

def get_method():
    """Запрашивает у пользователя выбор метода и возвращает его номер и параметры для него."""
    print("Выберите метод для нахождения корня уравнения:")
    print("1. Метод бисекции")
    print("2. Метод Ньютона")
    print("3. Оба метода")

    while True:
        try:
            method = int(input("Введите номер метода (1, 2 или 3): "))
            if method == 1:
                params = get_bisection_params()
                return method, params
            elif method == 2:
                params = get_newton_params()
                return method, params
            elif method == 3:
                bisection_params = get_bisection_params()
                newton_params = get_newton_params()
                return method, bisection_params, newton_params
            else:
                print("Пожалуйста, выберите один из вариантов (1, 2 или 3).")
        except ValueError:
            print("Ошибка ввода, пожалуйста, введите номер метода (1, 2 или 3).")
