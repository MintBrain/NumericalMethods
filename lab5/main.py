import matplotlib.pyplot as plt
import numpy as np


def plot_cubic_spline(x_values, y_values, cubic_spline_fn, num_points=100):
    """
    Строит график кубического сплайна.
    :param x_values: Список значений x (должен быть отсортирован).
    :param y_values: Список значений y, соответствующих x.
    :param cubic_spline_fn: Функция для интерполяции (например, cubic_spline_interpolation).
    :param num_points: Количество точек для построения плавной кривой.
    """
    # Подготовить данные для графика
    x_dense = np.linspace(x_values[0], x_values[-1], num_points)
    y_dense = [cubic_spline_fn(x_values, y_values, x) for x in x_dense]

    # Построить график
    plt.figure(figsize=(8, 6))
    plt.plot(x_dense, y_dense, label="Кубический сплайн", color="blue")
    plt.scatter(x_values, y_values, color="red", label="Исходные точки")  # Маркеры исходных точек
    plt.title("Интерполяция кубическим сплайном")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True)
    plt.ion()
    plt.show()
    plt.pause(0.2)


def verify_cubic_spline(cubic_spline_fn, x_values, y_values):
    """
    Проверяет корректность кубического сплайна.
    :param cubic_spline_fn: Функция для интерполяции (например, cubic_spline_interpolation).
    :param x_values: Список значений x.
    :param y_values: Список значений y.
    :return: True, если проверка пройдена, иначе False.
    """
    for x, y in zip(x_values, y_values):
        interpolated_value = cubic_spline_fn(x_values, y_values, x)
        if not abs(interpolated_value - y) < 1e-6:  # Допустимая погрешность
            print(f"Ошибка: в точке x = {x}, ожидается y = {y}, получено {interpolated_value}")
            return False

    print("Проверка успешно пройдена: все узловые точки совпадают.")
    return True


def solve_tridiagonal(n, _a, _b, _c, _d):
    u: list[float] = [0] * n
    v: list[float] = [0] * n
    c: list[float] = [0] * (n + 1)

    # Прямой ход метода прогонки
    for i in range(2, n):
        denominator = _a[i] * u[i - 1] + _b[i]
        if denominator == 0:
            raise ZeroDivisionError("Обнаружена нулевая диагональ, система неразрешима.")
        u[i] = -_c[i] / denominator
        v[i] = (_d[i] - _a[i] * v[i - 1]) / denominator

    # Назначение краевых условий
    c[1] = 0
    c[n] = 0

    # Обратный ход метода прогонки
    for i in range(n - 1, 1, -1):
        c[i] = u[i] * c[i + 1] + v[i]

    return c


def cubic_spline_interpolation(x_points: list[float], y_points: list[float], x_new: float):
    n = len(x_points)
    if n < 2:
        raise ValueError("Должно быть хотя бы два узла интерполяции.")

    # Инициализация массивов
    h: list[float] = [0] * n
    a: list[float] = [0] * n
    b: list[float] = [0] * n
    d: list[float] = [0] * n
    _a: list[float] = [0] * n
    _b: list[float] = [0] * n
    _c: list[float] = [0] * n
    _d: list[float] = [0] * n

    # Вычисление h[i]
    for i in range(1, n):
        h[i] = x_points[i] - x_points[i - 1]

    # Формирование трёхдиагональной системы
    for i in range(2, n):
        _a[i] = h[i - 1]
        _b[i] = 2 * (h[i - 1] + h[i])
        _c[i] = h[i]
        _d[i] = 3 * ((y_points[i] - y_points[i - 1]) / h[i] - (y_points[i - 1] - y_points[i - 2]) / h[i - 1])

    c = solve_tridiagonal(n, _a, _b, _c, _d)

    # Вычисление коэффициентов a, b, d
    for i in range(1, n):
        a[i] = y_points[i - 1]
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])
        b[i] = (y_points[i] - y_points[i - 1]) / h[i] - h[i] / 3 * (c[i + 1] + 2 * c[i])

    # Поиск подходящего интервала для x_new
    for k in range(1, n):
        if x_points[k - 1] <= x_new <= x_points[k]:
            break
    else:
        raise ValueError("Значение x_new выходит за пределы интервала.")

    # Интерполяция
    dx = x_new - x_points[k - 1]
    result = a[k] + b[k] * dx + c[k] * dx ** 2 + d[k] * dx ** 3
    return result


# Ввод данных
def input_points():
    while True:
        try:
            n = int(input("Введите количество точек: "))
            if n < 2:
                print("Должно быть как минимум две точки.")
                continue

            x_values = []
            y_values = []

            print("Введите точки в формате x y (через пробел):")
            for _ in range(n):
                x, y = map(float, input().split())
                x_values.append(x)
                y_values.append(y)

            if sorted(x_values) != x_values:
                print("Значения x должны быть отсортированы.")
                continue

            return x_values, y_values
        except ValueError:
            print("Некорректный ввод. Попробуйте снова.")


def program(x, y):
    print("Кубическая интерполяция сплайнами")

    # Проверка корректности
    is_valid = verify_cubic_spline(cubic_spline_interpolation, x, y)
    if is_valid:
        print("Сплайн корректен.")
    else:
        print("В сплайне есть ошибки.")
        return

    plot_cubic_spline(x, y, cubic_spline_interpolation)

    while True:
        try:
            query_point = float(input("Введите точку для интерполяции (или 'q' для выхода): "))
            if query_point < min(x) or query_point > max(x):
                print("Точка вне диапазона входных данных.")
                continue

            result = cubic_spline_interpolation(x, y, query_point)
            print(f"Интерполированное значение в точке {query_point}: {result}")

            plt.scatter(query_point, result, color="blue", label=f"Точка ({query_point}, {result:.2f})", linewidths=6)
            plt.legend()
            plt.draw()
            plt.pause(0.3)
        except ValueError as e:
            print("Выход из программы.")
            print(e)
            break


def test():
    x = [1, 1.2, 1.4, 1.6, 1.8, 2]
    y = [1.2, 2, 3, 3.8, 5, 6.1]

    program(x, y)


def main():
    x, y = input_points()
    program(x, y)


if __name__ == "__main__":
    try:
        test()
    except Exception as e:
        print('Ошибка выполнения программы')
        print(e)
