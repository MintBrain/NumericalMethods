import numpy as np
from sympy import symbols, simplify, latex
from sympy.parsing.sympy_parser import parse_expr
import matplotlib.pyplot as plt
import matplotlib
from sympy.printing.pretty.pretty_symbology import line_width


# for alg in ['gtk3agg', 'gtk3cairo', 'gtk4agg', 'gtk4cairo', 'macosx', 'nbagg', 'notebook', 'qtagg', 'qtcairo', 'qt5agg',
#             'qt5cairo',
#             'tkagg', 'tkcairo', 'webagg', 'wx', 'wxagg', 'wxcairo', 'agg', 'cairo', 'pdf', 'pgf', 'ps', 'svg',
#             'template']:
#     try:
#         matplotlib.use(alg)
#         print(alg)
#
#     except Exception as e:
#         # print(e)
#         continue
# agg
# pdf
# pgf
# ps
# svg
# template


# matplotlib.use('ps')

def pretty_display(expression, title="Полином"):
    """
    Красиво отображает выражение с использованием SymPy.
    :param expression: Выражение в виде строки.
    :param title: Заголовок.
    """
    print(f"{title}:")
    expr = parse_expr(expression.replace("^", "**"))  # Преобразуем строку в SymPy-выражение
    print(latex(expr))  # Выводим в формате LaTeX


def display_polynomial_console(expression, title="Полином"):
    """
    Отображает полином в виде текстового выражения для консоли.
    :param expression: Полином в виде строки.
    :param title: Заголовок.
    """
    print(f"{title}:\n")
    print(expression.replace("*", "⋅").replace("/", " ÷ ").replace("-", "−"))
    print("\n" + "-" * 50 + "\n")

def simplify_polynomial(expression):
    """
    Раскрывает скобки, упрощает полином и объединяет подобные члены.
    :param expression: Полином в виде строки.
    :return: Упрощённый полином в виде строки.
    """
    terms = expression.replace(" ", "").split("+")  # Разделяем на слагаемые
    simplified_terms = {}

    for term in terms:
        coeff, vars = 1, ""  # Коэффициент и переменные
        parts = term.split("*")
        for part in parts:
            if "x" in part:
                vars += part  # Переменные
            else:
                coeff *= float(part)  # Коэффициенты

        # Группируем по переменным
        if vars in simplified_terms:
            simplified_terms[vars] += coeff
        else:
            simplified_terms[vars] = coeff

    # Формируем упрощённый полином
    simplified = []
    for vars, coeff in simplified_terms.items():
        if coeff != 0:
            simplified.append(f"{coeff}*{vars}" if vars else f"{coeff}")

    return " + ".join(simplified)

def lagrange_polynomial(x_values, y_values):
    """
    Строит интерполяционный полином Лагранжа.
    :param x_values: Список значений x.
    :param y_values: Список значений y.
    :return: Строка, представляющая полином Лагранжа.
    """
    n = len(x_values)
    terms = []  # Для хранения членов полинома

    for i in range(n):
        if y_values[i] == 0:  # Пропускаем, если вклад нулевой
            continue

        # Построение базисного полинома L_i(x)
        numerator_terms = []  # Члены числителя
        denominator = 1  # Знаменатель

        for j in range(n):
            if i != j:
                numerator_terms.append(f"(x - {x_values[j]})")
                denominator *= (x_values[i] - x_values[j])

        # Базисный полином L_i(x)
        L_i = f"({' * '.join(numerator_terms)}) / {denominator}"
        terms.append(f"{y_values[i]} * {L_i}")

    # Полный полином Лагранжа
    L = " + ".join(terms)
    return L


def newton_polynomial(x_values, y_values):
    """
    Строит интерполяционный полином Ньютона.
    :param x_values: Список значений x.
    :param y_values: Список значений y.
    :return: Строка, представляющая полином Ньютона.
    """
    n = len(x_values)

    # Вычисление разделенных разностей
    divided_diff = [y_values[:]]
    for level in range(1, n):
        diffs = []
        for i in range(n - level):
            diff = (divided_diff[level - 1][i + 1] - divided_diff[level - 1][i]) / (x_values[i + level] - x_values[i])
            diffs.append(diff)
        divided_diff.append(diffs)

    # Формирование полинома Ньютона
    terms = []
    for level in range(n):
        if divided_diff[level][0] == 0:  # Пропускаем нулевые коэффициенты
            continue

        term = [f"{divided_diff[level][0]}"]
        for i in range(level):
            term.append(f"(x - {x_values[i]})")
        terms.append(" * ".join(term))

    # Полный полином Ньютона
    N = " + ".join(terms)
    return N


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
    plt.show()



def test():
    # Ввод данных
    x_values = [-1, 2, 5]
    y_values = [3, 0, 2]
    # x_values = [-1, 0,0.5,1]
    # y_values = [0,2,9/8,0]

    plot_polynomials(x_values, y_values)
    # Построение полиномов
    lagrange = lagrange_polynomial(x_values, y_values)
    newton = newton_polynomial(x_values, y_values)

    # Вывод результатов
    print("Интерполяционный полином Лагранжа:")
    print(lagrange)

    print("\nИнтерполяционный полином Ньютона:")
    print(newton)
    print()
    # Отображение формул
    pretty_display(lagrange, "Интерполяционный полином Лагранжа")
    pretty_display(newton, "Интерполяционный полином Ньютона")
    # # Упрощение полиномов
    # lagrange_simplified = simplify_polynomial(lagrange)
    # newton_simplified = simplify_polynomial(newton)
    #
    # # Вывод результатов
    # print("\nИнтерполяционный полином Лагранжа (упрощённый):")
    # print(lagrange_simplified)
    #
    # print("\nИнтерполяционный полином Ньютона (упрощённый):")
    # print(newton_simplified)


def main():
    pass


# Пример использования
if __name__ == "__main__":
    test()
